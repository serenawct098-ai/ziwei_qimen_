import pytest

from ziwei_qimen.errors import DomainError, ErrorCode
from ziwei_qimen.time.location import resolve_city, resolve_coordinates


def test_accepts_valid_coordinates() -> None:
    result = resolve_coordinates(latitude=22.3193, longitude=114.1694)

    assert result.latitude == 22.3193
    assert result.longitude == 114.1694


@pytest.mark.parametrize(
    ("latitude", "longitude"),
    [
        (-90.0001, 0.0),
        (90.0001, 0.0),
        (0.0, -180.0001),
        (0.0, 180.0001),
    ],
)
def test_rejects_invalid_coordinates(latitude: float, longitude: float) -> None:
    with pytest.raises(DomainError) as error:
        resolve_coordinates(latitude=latitude, longitude=longitude)

    assert error.value.code == ErrorCode.INVALID_COORDINATES


def test_city_resolution_halts_without_controlled_dataset() -> None:
    with pytest.raises(DomainError) as error:
        resolve_city("Hong Kong", "HK")

    assert error.value.code == ErrorCode.LOCATION_RESOLUTION_FAILED
