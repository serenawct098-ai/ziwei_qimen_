from datetime import date, datetime
from typing import cast

import pytest

from ziwei_qimen.errors import DomainError, ErrorCode
from ziwei_qimen.time.lunar_calendar import resolve_hko_lunar_date


@pytest.mark.parametrize(
    ("gregorian_date", "lunar_year", "lunar_month", "lunar_day", "is_leap_month", "solar_term"),
    [
        (date(1901, 1, 1), 1900, 11, 11, False, None),
        (date(1901, 2, 19), 1901, 1, 1, False, "雨水"),
        (date(1950, 2, 17), 1950, 1, 1, False, None),
        (date(2000, 2, 5), 2000, 1, 1, False, None),
        (date(2011, 1, 1), 2010, 11, 27, False, None),
        (date(2011, 2, 3), 2011, 1, 1, False, None),
        (date(1903, 5, 27), 1903, 5, 1, False, None),
        (date(1903, 6, 25), 1903, 5, 1, True, None),
        (date(1903, 7, 23), 1903, 5, 29, True, None),
        (date(2026, 2, 17), 2026, 1, 1, False, None),
        (date(2050, 1, 23), 2050, 1, 1, False, None),
        (date(2100, 12, 31), 2100, 12, 1, False, None),
    ],
)
def test_resolve_hko_lunar_date(
    gregorian_date: date,
    lunar_year: int,
    lunar_month: int,
    lunar_day: int,
    is_leap_month: bool,
    solar_term: str | None,
) -> None:
    result = resolve_hko_lunar_date(gregorian_date)

    assert result.gregorian_date == gregorian_date
    assert result.lunar_year == lunar_year
    assert result.lunar_month == lunar_month
    assert result.lunar_day == lunar_day
    assert result.is_leap_month is is_leap_month
    assert result.solar_term == solar_term
    assert result.dataset_version == "1.0.0"
    assert result.source_provider == "Hong Kong Observatory"


@pytest.mark.parametrize("gregorian_date", [date(1900, 12, 31), date(2101, 1, 1)])
def test_resolve_hko_lunar_date_rejects_out_of_range(gregorian_date: date) -> None:
    with pytest.raises(DomainError) as error:
        resolve_hko_lunar_date(gregorian_date)

    assert error.value.code is ErrorCode.CALENDAR_DATE_OUT_OF_RANGE


@pytest.mark.parametrize("value", ["1901-01-01", 0, None, datetime(1901, 1, 1)])
def test_resolve_hko_lunar_date_rejects_non_date_input(value: object) -> None:
    with pytest.raises(TypeError):
        resolve_hko_lunar_date(cast(date, value))
