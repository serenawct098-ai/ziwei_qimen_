import pytest

from ziwei_qimen.domain.models import CityLocation, CoordinatesLocation, LocationResolution
from ziwei_qimen.errors import DomainError, ErrorCode
from ziwei_qimen.time.location import CITY_DATASET_VERSION, resolve_location


def test_resolves_direct_coordinates_with_explicit_timezone() -> None:
    result = resolve_location(
        CoordinatesLocation(latitude=22.3193, longitude=114.1694, iana_timezone="Asia/Hong_Kong")
    )

    assert result.coordinates.latitude == 22.3193
    assert result.coordinates.longitude == 114.1694
    assert result.iana_timezone == "Asia/Hong_Kong"
    assert result.resolution == LocationResolution.COORDINATES_SUPPLIED
    assert result.city_dataset_version is None


@pytest.mark.parametrize(
    ("latitude", "longitude"),
    [
        (-90.0001, 0.0),
        (90.0001, 0.0),
        (0.0, -180.0001),
        (0.0, 180.0001),
    ],
)
def test_rejects_invalid_direct_coordinates(latitude: float, longitude: float) -> None:
    with pytest.raises(ValueError):
        CoordinatesLocation(latitude=latitude, longitude=longitude, iana_timezone="Asia/Hong_Kong")


def test_rejects_unknown_direct_timezone() -> None:
    with pytest.raises(DomainError) as error:
        resolve_location(
            CoordinatesLocation(latitude=22.3193, longitude=114.1694, iana_timezone="Asia/Unknown")
        )

    assert error.value.code == ErrorCode.INVALID_TIMEZONE


def test_resolves_city_only_with_a_unique_registry_record() -> None:
    result = resolve_location(CityLocation(city="Hong Kong", country_code="HK"))

    assert result.iana_timezone == "Asia/Hong_Kong"
    assert result.resolution == LocationResolution.CONTROLLED_CITY_DATASET
    assert result.city_dataset_version == CITY_DATASET_VERSION


@pytest.mark.parametrize(
    "location",
    [
        CityLocation(city="Hong Kong", country_code="TW"),
        CityLocation(city="Unlisted City", country_code="US"),
    ],
)
def test_rejects_unresolved_city_without_inference(location: CityLocation) -> None:
    with pytest.raises(DomainError) as error:
        resolve_location(location)

    assert error.value.code == ErrorCode.LOCATION_RESOLUTION_FAILED


def test_rejects_country_code_without_city() -> None:
    with pytest.raises(ValueError):
        CityLocation(city="", country_code="HK")
