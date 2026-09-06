from datetime import datetime

import pytest

from ziwei_qimen.domain.models import (
    CivilTimeInput,
    Coordinates,
    LocationResolution,
    ResolvedLocation,
)
from ziwei_qimen.errors import DomainError, ErrorCode
from ziwei_qimen.time.true_solar_time import true_solar_time


def test_halts_without_astronomy_assets() -> None:
    civil_time = CivilTimeInput(
        civil_datetime=datetime(2026, 9, 6, 14, 31, 0),
        iana_timezone="Asia/Hong_Kong",
    )
    location = ResolvedLocation(
        coordinates=Coordinates(latitude=22.3193, longitude=114.1694),
        iana_timezone="Asia/Hong_Kong",
        resolution=LocationResolution.COORDINATES_SUPPLIED,
    )

    with pytest.raises(DomainError) as error:
        true_solar_time(civil_time, location)

    assert error.value.code == ErrorCode.ASTRONOMY_ASSET_UNAVAILABLE
