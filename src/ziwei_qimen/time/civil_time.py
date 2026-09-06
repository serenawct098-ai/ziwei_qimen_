from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

import tzdata

from ziwei_qimen.domain.models import CivilTimeInput, CivilTimeResolution
from ziwei_qimen.errors import DomainError, ErrorCode
from ziwei_qimen.time.timezone import load_iana_timezone

MIN_SUPPORTED_DATE = datetime(1901, 1, 1)
MAX_SUPPORTED_DATE = datetime(2100, 12, 31, 23, 59, 59)


def resolve_civil_time(value: CivilTimeInput) -> CivilTimeResolution:
    _validate_naive(value.civil_datetime)
    _validate_date_range(value.civil_datetime)
    timezone = load_iana_timezone(value.iana_timezone)
    _validate_local_time(value.civil_datetime, timezone)
    utc_datetime = value.civil_datetime.replace(tzinfo=timezone).astimezone(UTC)
    return CivilTimeResolution(
        civil_datetime=value.civil_datetime,
        iana_timezone=value.iana_timezone,
        utc_datetime=utc_datetime,
        timezone_data_version=tzdata.__version__,
    )


def _validate_naive(value: datetime) -> None:
    if value.tzinfo is not None:
        raise ValueError("civil_datetime must be naive")


def _validate_date_range(value: datetime) -> None:
    if not MIN_SUPPORTED_DATE <= value <= MAX_SUPPORTED_DATE:
        raise DomainError(
            ErrorCode.UNSUPPORTED_DATE_RANGE,
            "civil_datetime must be within 1901-01-01 through 2100-12-31",
        )


def _validate_local_time(value: datetime, timezone: ZoneInfo) -> None:
    earlier = value.replace(tzinfo=timezone, fold=0)
    later = value.replace(tzinfo=timezone, fold=1)
    earlier_utc = earlier.astimezone(UTC)
    later_utc = later.astimezone(UTC)
    earlier_round_trip = earlier_utc.astimezone(timezone).replace(tzinfo=None)
    later_round_trip = later_utc.astimezone(timezone).replace(tzinfo=None)
    if earlier_round_trip != value and later_round_trip != value:
        raise DomainError(
            ErrorCode.NONEXISTENT_LOCAL_TIME,
            f"nonexistent local time: {value.isoformat()} in {timezone.key}",
        )
    if earlier_round_trip == value and later_round_trip == value and earlier_utc != later_utc:
        raise DomainError(
            ErrorCode.AMBIGUOUS_LOCAL_TIME,
            f"ambiguous local time: {value.isoformat()} in {timezone.key}",
        )
