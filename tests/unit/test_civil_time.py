from datetime import UTC, datetime

import pytest

from ziwei_qimen.domain.models import CivilTimeInput
from ziwei_qimen.errors import DomainError, ErrorCode
from ziwei_qimen.time.civil_time import resolve_civil_time


def test_resolves_hong_kong_civil_time_to_utc() -> None:
    result = resolve_civil_time(
        CivilTimeInput(
            civil_datetime=datetime(2026, 9, 6, 14, 31, 0),
            iana_timezone="Asia/Hong_Kong",
        )
    )

    assert result.utc_datetime == datetime(2026, 9, 6, 6, 31, 0, tzinfo=UTC)
    assert result.iana_timezone == "Asia/Hong_Kong"
    assert result.timezone_data_version


@pytest.mark.parametrize(
    "civil_datetime",
    [
        datetime(1900, 12, 31, 23, 59, 59),
        datetime(2101, 1, 1, 0, 0, 0),
    ],
)
def test_rejects_unsupported_date_range(civil_datetime: datetime) -> None:
    with pytest.raises(DomainError) as error:
        resolve_civil_time(
            CivilTimeInput(
                civil_datetime=civil_datetime,
                iana_timezone="Asia/Hong_Kong",
            )
        )

    assert error.value.code == ErrorCode.UNSUPPORTED_DATE_RANGE


def test_rejects_invalid_timezone() -> None:
    with pytest.raises(DomainError) as error:
        resolve_civil_time(
            CivilTimeInput(
                civil_datetime=datetime(2026, 9, 6, 14, 31, 0),
                iana_timezone="Asia/Unknown",
            )
        )

    assert error.value.code == ErrorCode.INVALID_TIMEZONE


def test_rejects_ambiguous_new_york_local_time() -> None:
    with pytest.raises(DomainError) as error:
        resolve_civil_time(
            CivilTimeInput(
                civil_datetime=datetime(2026, 11, 1, 1, 30, 0),
                iana_timezone="America/New_York",
            )
        )

    assert error.value.code == ErrorCode.AMBIGUOUS_LOCAL_TIME


def test_rejects_nonexistent_new_york_local_time() -> None:
    with pytest.raises(DomainError) as error:
        resolve_civil_time(
            CivilTimeInput(
                civil_datetime=datetime(2026, 3, 8, 2, 30, 0),
                iana_timezone="America/New_York",
            )
        )

    assert error.value.code == ErrorCode.NONEXISTENT_LOCAL_TIME


def test_rejects_timezone_aware_civil_datetime() -> None:
    with pytest.raises(ValueError, match="civil_datetime must be naive"):
        resolve_civil_time(
            CivilTimeInput(
                civil_datetime=datetime(2026, 9, 6, 14, 31, 0, tzinfo=UTC),
                iana_timezone="Asia/Hong_Kong",
            )
        )
