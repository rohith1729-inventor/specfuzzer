"""Validation helpers for interpreting executor outcomes."""
from __future__ import annotations

from collections import Counter
from typing import Dict, List

from .schemas import Finding, Report, Severity, TestResult, TestStatus


def summarize_results(results: List[TestResult]) -> Dict[str, object]:
    severity_counter: Counter[str] = Counter()
    findings: List[Finding] = []

    for result in results:
        if result.status == TestStatus.passed:
            continue
        severity = _infer_severity(result)
        severity_counter[severity.value] += 1
        findings.append(
            Finding(
                endpoint=result.case.path,
                method=result.case.method,
                severity=severity,
                description=result.case.description,
                details={
                    "expected_status": result.case.expected_status,
                    "actual_status": result.actual_status,
                    "status": result.status.value,
                    "error": result.error,
                    "payload": result.case.payload,
                },
            )
        )

    summary = {
        "tests": len(results),
        "issues": len(findings),
        "severity": {
            "high": severity_counter.get("high", 0),
            "medium": severity_counter.get("medium", 0),
            "low": severity_counter.get("low", 0),
        },
    }

    report = Report(summary=summary, findings=findings)
    return report.model_dump()


def _infer_severity(result: TestResult) -> Severity:
    if result.status == TestStatus.error:
        return Severity.high
    if result.actual_status is None:
        return Severity.low
    if result.actual_status >= 500:
        return Severity.high
    if result.actual_status >= 400:
        return Severity.medium
    return Severity.low

