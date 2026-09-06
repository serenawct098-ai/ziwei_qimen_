from __future__ import annotations

from ziwei_qimen.domain.models import (
    CivilTimeInput,
    ResolvedLocation,
    TimeCalculationStatus,
    TrueSolarTimeProvenance,
)
from ziwei_qimen.errors import DomainError, ErrorCode
from ziwei_qimen.time.civil_time import resolve_civil_time


def true_solar_time(
    civil_time: CivilTimeInput,
    location: ResolvedLocation,
) -> TrueSolarTimeProvenance:
    resolved_civil_time = resolve_civil_time(civil_time)
    provenance = TrueSolarTimeProvenance(
        civil_datetime=resolved_civil_time.civil_datetime,
        iana_timezone=resolved_civil_time.iana_timezone,
        timezone_data_version=resolved_civil_time.timezone_data_version,
        utc_datetime=resolved_civil_time.utc_datetime,
        latitude_degrees_north=location.coordinates.latitude,
        longitude_degrees_east=location.coordinates.longitude,
        location_resolution=location.resolution,
        longitude_correction_seconds=None,
        equation_of_time_seconds=None,
        true_solar_datetime=None,
        precision="second",
        ephemeris_id=None,
        ephemeris_version=None,
        iers_data_version=None,
        calculation_status=TimeCalculationStatus.BLOCKED,
    )
    raise DomainError(
        ErrorCode.ASTRONOMY_ASSET_UNAVAILABLE,
        f"true solar time unavailable: {provenance.calculation_status}",
    )
