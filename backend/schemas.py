"""Shared data models for SpecFuzzer backend."""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


HTTP_METHODS = {"get", "post", "put", "delete", "patch", "options", "head"}


class Parameter(BaseModel):
    name: str
    location: str = Field(alias="in")
    required: bool = False
    schema: Dict[str, Any] | None = None

    class Config:
        populate_by_name = True


class EndpointSpec(BaseModel):
    method: str
    path: str
    parameters: List[Parameter] = Field(default_factory=list)
    responses: List[int] = Field(default_factory=list)
    description: Optional[str] = None


class Severity(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class TestCase(BaseModel):
    method: str
    path: str
    description: str
    payload: Dict[str, Any]
    expected_status: int


class TestStatus(str, Enum):
    passed = "passed"
    failed = "failed"
    skipped = "skipped"
    error = "error"


class TestResult(BaseModel):
    case: TestCase
    status: TestStatus
    actual_status: Optional[int] = None
    response_body: Any = None
    error: Optional[str] = None
    latency_ms: Optional[float] = None


class Finding(BaseModel):
    endpoint: str
    method: str
    severity: Severity
    description: str
    details: Dict[str, Any]


class Report(BaseModel):
    summary: Dict[str, Any]
    findings: List[Finding]
