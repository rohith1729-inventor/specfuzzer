"""OpenAPI parser utilities."""
from __future__ import annotations

import json
from typing import List

import yaml
from openapi_spec_validator import validate_spec
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError

from .schemas import EndpointSpec, HTTP_METHODS, Parameter


class SpecParseError(ValueError):
    """Raised when the uploaded OpenAPI document cannot be processed."""


def _load_raw_spec(data: bytes) -> dict:
    text = data.decode("utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        spec = yaml.safe_load(text)
        if not isinstance(spec, dict):
            raise SpecParseError("Uploaded spec is not valid JSON or YAML.")
        return spec


def parse_openapi_document(data: bytes) -> List[EndpointSpec]:
    """Return a simplified list of endpoints extracted from an OpenAPI spec."""

    spec = _load_raw_spec(data)
    try:
        validate_spec(spec)
    except OpenAPIValidationError as exc:
        raise SpecParseError(f"Invalid OpenAPI document: {exc}") from exc

    paths = spec.get("paths")
    if not isinstance(paths, dict):
        raise SpecParseError("Spec does not define any paths.")

    endpoints: List[EndpointSpec] = []
    for raw_path, operations in paths.items():
        if not isinstance(operations, dict):
            continue
        for method, operation in operations.items():
            method_lower = method.lower()
            if method_lower not in HTTP_METHODS:
                continue
            if not isinstance(operation, dict):
                continue

            parameters = operation.get("parameters", [])
            endpoint_parameters = []
            if isinstance(parameters, list):
                for param in parameters:
                    if not isinstance(param, dict):
                        continue
                    endpoint_parameters.append(
                        Parameter(
                            name=param.get("name", "unknown"),
                            location=param.get("in", "query"),
                            required=bool(param.get("required", False)),
                            schema=param.get("schema") or {},
                        )
                    )

            responses = []
            raw_responses = operation.get("responses", {})
            if isinstance(raw_responses, dict):
                for status_code, _ in raw_responses.items():
                    try:
                        responses.append(int(status_code))
                    except (TypeError, ValueError):
                        continue

            endpoints.append(
                EndpointSpec(
                    method=method_lower.upper(),
                    path=raw_path,
                    parameters=endpoint_parameters,
                    responses=responses,
                    description=operation.get("summary") or operation.get("description"),
                )
            )

    if not endpoints:
        raise SpecParseError("No valid endpoints were found in the spec.")

    return endpoints
