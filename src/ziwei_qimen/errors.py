from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ErrorCode(StrEnum):
    UNSUPPORTED_DATE_RANGE = "unsupported_date_range"
    INVALID_TIMEZONE = "invalid_timezone"
    AMBIGUOUS_LOCAL_TIME = "ambiguous_local_time"
    NONEXISTENT_LOCAL_TIME = "nonexistent_local_time"
    INVALID_COORDINATES = "invalid_coordinates"
    LOCATION_RESOLUTION_FAILED = "location_resolution_failed"
    ASTRONOMY_ASSET_UNAVAILABLE = "astronomy_asset_unavailable"


@dataclass(frozen=True, slots=True)
class DomainError(Exception):
    code: ErrorCode
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"
