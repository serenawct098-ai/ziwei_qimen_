from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .enums import Gender, QuestionCategory


class LocationResolution(StrEnum):
    COORDINATES_SUPPLIED = "coordinates_supplied"
    CONTROLLED_CITY_DATASET = "controlled_city_dataset"


class TimeCalculationStatus(StrEnum):
    RESOLVED = "resolved"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class CityLocation:
    city: str
    country_code: str | None = None

    def __post_init__(self) -> None:
        if not self.city.strip():
            raise ValueError("city must not be empty")
        if self.country_code is not None:
            if len(self.country_code) != 2 or not self.country_code.isalpha():
                raise ValueError("country_code must be an ISO 3166-1 alpha-2 code")


@dataclass(frozen=True, slots=True)
class Coordinates:
    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not -90.0 <= self.latitude <= 90.0:
            raise ValueError("latitude must be between -90 and 90")
        if not -180.0 <= self.longitude <= 180.0:
            raise ValueError("longitude must be between -180 and 180")


@dataclass(frozen=True, slots=True)
class ResolvedLocation:
    coordinates: Coordinates
    iana_timezone: str
    resolution: LocationResolution
    canonical_city_id: str | None = None
    city_display_name: str | None = None
    country_code: str | None = None
    city_dataset_version: str | None = None


@dataclass(frozen=True, slots=True)
class CivilTimeInput:
    civil_datetime: datetime
    iana_timezone: str


@dataclass(frozen=True, slots=True)
class CivilTimeResolution:
    civil_datetime: datetime
    iana_timezone: str
    utc_datetime: datetime
    timezone_data_version: str


@dataclass(frozen=True, slots=True)
class TrueSolarTimeProvenance:
    civil_datetime: datetime
    iana_timezone: str
    timezone_data_version: str
    utc_datetime: datetime
    latitude_degrees_north: float
    longitude_degrees_east: float
    location_resolution: LocationResolution
    longitude_correction_seconds: float | None
    equation_of_time_seconds: float | None
    true_solar_datetime: datetime | None
    precision: str
    ephemeris_id: str | None
    ephemeris_version: str | None
    iers_data_version: str | None
    calculation_status: TimeCalculationStatus


@dataclass(frozen=True, slots=True)
class ZiweiBirthInput:
    birth_civil_datetime: datetime
    birth_location: CityLocation
    gender: Gender
    analysis_civil_datetime: datetime
    analysis_timezone: str


@dataclass(frozen=True, slots=True)
class QimenQueryInput:
    question_civil_datetime: datetime
    question_location: CityLocation
    question_category: QuestionCategory
    primary_residence_location: CityLocation | None = None
