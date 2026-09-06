"""不可變領域資料模型。"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .enums import Gender, QuestionCategory


@dataclass(frozen=True, slots=True)
class CityLocation:
    """使用者提交的城市名稱與可選地區代碼。"""

    city: str
    country_code: str | None = None

    def __post_init__(self) -> None:
        if not self.city.strip():
            raise ValueError("city must not be empty")
        if self.country_code is not None and len(self.country_code) != 2:
            raise ValueError("country_code must be an ISO 3166-1 alpha-2 code")


@dataclass(frozen=True, slots=True)
class Coordinates:
    """由受控城市資料解析後使用的 WGS 84 經緯度。"""

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not -90.0 <= self.latitude <= 90.0:
            raise ValueError("latitude must be between -90 and 90")
        if not -180.0 <= self.longitude <= 180.0:
            raise ValueError("longitude must be between -180 and 180")


@dataclass(frozen=True, slots=True)
class ZiweiBirthInput:
    """紫微本命與限運的唯一 transport input。"""

    birth_civil_datetime: datetime
    birth_location: CityLocation
    gender: Gender
    analysis_civil_datetime: datetime
    analysis_timezone: str


@dataclass(frozen=True, slots=True)
class QimenQueryInput:
    """時家奇門的唯一 transport input。"""

    question_civil_datetime: datetime
    qimen_location: CityLocation
    question_category: QuestionCategory
