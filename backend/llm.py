"""Model orchestration routed through the remote LLM gateway."""
from __future__ import annotations

import json
import logging
from typing import Iterable, List

from .llm_client import generate_for_specfuzzer
from .schemas import EndpointSpec, TestCase

logger = logging.getLogger(__name__)


def generate_tests(endpoints: List[EndpointSpec]) -> List[TestCase]:
    """Generate adversarial tests via the remote model."""

    structured = [_endpoint_to_payload(ep) for ep in endpoints]
    prompt = _build_prompt(structured)

    try:
        response = generate_for_specfuzzer(prompt)
        return _coerce_test_cases(response, endpoints)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Remote LLM failed, falling back to heuristics: %s", exc)
        return _local_fallback(endpoints)


def _endpoint_to_payload(endpoint: EndpointSpec) -> dict:
    return {
        "method": endpoint.method,
        "path": endpoint.path,
        "parameters": [param.model_dump() for param in endpoint.parameters],
        "responses": endpoint.responses,
        "description": endpoint.description,
    }


def _build_prompt(endpoints: List[dict]) -> str:
    return (
        "You are a security adversarial test generator. For each endpoint, generate "
        "3 JSON test cases that attempt to break it. Return ONLY an array of JSON "
        "test cases, no explanation.\n\n"
        f"Endpoints:\n{json.dumps(endpoints, indent=2)}"
    )


def _coerce_test_cases(raw_response: str, endpoints: List[EndpointSpec]) -> List[TestCase]:
    try:
        payload = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Model response was not valid JSON") from exc

    if not isinstance(payload, list):
        raise RuntimeError("Model response must be a JSON array")

    cases: List[TestCase] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        case = TestCase(
            method=(item.get("method") or _guess_method(item, endpoints)).upper(),
            path=item.get("path") or _guess_path(item, endpoints),
            description=item.get("description") or "Adversarial input",
            payload=item.get("payload") or item.get("body") or {},
            expected_status=int(item.get("expected_status", 400)),
        )
        cases.append(case)

    if not cases:
        raise RuntimeError("Model response did not contain any usable test cases")
    return cases


def _guess_method(item: dict, endpoints: Iterable[EndpointSpec]) -> str:
    hinted = item.get("endpoint") or item.get("path")
    for endpoint in endpoints:
        if hinted and hinted in endpoint.path:
            return endpoint.method
    return next(iter(endpoints)).method if endpoints else "GET"


def _guess_path(item: dict, endpoints: Iterable[EndpointSpec]) -> str:
    hinted = item.get("endpoint") or item.get("path")
    if hinted:
        return hinted
    return next(iter(endpoints)).path if endpoints else "/"


def _local_fallback(endpoints: List[EndpointSpec]) -> List[TestCase]:
    cases: List[TestCase] = []
    for endpoint in endpoints:
        base_description = endpoint.description or "Generic endpoint"
        cases.extend(
            [
                TestCase(
                    method=endpoint.method,
                    path=endpoint.path,
                    description=f"{base_description} | oversized payload fuzz",
                    payload={"fuzz": "X" * 2048},
                    expected_status=400,
                ),
                TestCase(
                    method=endpoint.method,
                    path=endpoint.path,
                    description=f"{base_description} | SQL injection",
                    payload={"fuzz": "' OR 1=1 --"},
                    expected_status=400,
                ),
                TestCase(
                    method=endpoint.method,
                    path=endpoint.path,
                    description=f"{base_description} | type confusion",
                    payload={"fuzz": [None, 123, {"nested": "oops"}]},
                    expected_status=422,
                ),
            ]
        )
    return cases
