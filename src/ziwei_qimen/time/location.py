from __future__ import annotations

from ziwei_qimen.domain.models import Coordinates
from ziwei_qimen.errors import DomainError, ErrorCode


def resolve_coordinates(latitude: float, longitude: float) -> Coordinates:
    try:
        return Coordinates(latitude=latitude, longitude=longitude)
    except ValueError as error:
        raise DomainError(ErrorCode.INVALID_COORDINATES, str(error)) from error


def resolve_city(*_: object) -> None:
    raise DomainError(
        ErrorCode.LOCATION_RESOLUTION_FAILED,
        "controlled city dataset is unavailable",
    )
