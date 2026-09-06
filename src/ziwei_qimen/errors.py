"""系統錯誤碼與例外。"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ErrorCode(StrEnum):
    """公開、穩定且可序列化的錯誤碼。"""

    UNSUPPORTED_DATE_RANGE = "unsupported_date_range"
    INVALID_IANA_TIMEZONE = "invalid_iana_timezone"
    AMBIGUOUS_LOCAL_TIME = "ambiguous_local_time"
    NONEXISTENT_LOCAL_TIME = "nonexistent_local_time"
    LOCATION_RESOLUTION_FAILED = "location_resolution_failed"
    INVALID_COORDINATES = "invalid_coordinates"
    MISSING_REQUIRED_INPUT = "missing_required_input"
    SOURCE_NOT_FOUND = "source_not_found"
    TABLE_NOT_FOUND = "table_not_found"
    TABLE_SCHEMA_INVALID = "table_schema_invalid"
    TABLE_SOURCE_REFERENCE_MISSING = "table_source_reference_missing"
    INCOMPLETE_GRADING_RULES = "incomplete_grading_rules"
    INTEGRATION_UNAVAILABLE = "integration_unavailable"


@dataclass(frozen=True, slots=True)
class DomainError(Exception):
    """可安全輸出給呼叫端的領域錯誤。"""

    code: ErrorCode
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"
