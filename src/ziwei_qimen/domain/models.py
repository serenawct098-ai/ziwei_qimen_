from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .enums import Gender, QuestionCategory


@dataclass(frozen=True, slots=True)
class CityLocation:
    city: str
    country_code: str | None = None

    def __post_init__(self) -> None:
        if not self.city.strip():
            raise ValueError("city must not be empty")
        if self.country_code is not None and len(self.country_code) != 2:
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
