from __future__ import annotations

import json
import re
from functools import cache
from importlib.resources import files
from typing import Any, cast

from ziwei_qimen.domain.models import (
    CityLocation,
    Coordinates,
    CoordinatesLocation,
    LocationInput,
    LocationResolution,
    ResolvedLocation,
)
from ziwei_qimen.errors import DomainError, ErrorCode
from ziwei_qimen.time.timezone import load_iana_timezone

CITY_TABLE_SOURCE = {
    "name": "Natural Earth 10m Populated Places",
    "version": "5.1.2",
    "license": "public_domain",
    "asset_logical_id": "natural_earth.ne_10m_populated_places",
}
CITY_DATASET_VERSION = "natural-earth-10m-populated-places-5.1.2-primary-cities-v1"
CITY_RECORD_FIELDS = {
    "canonical_city_id",
    "city_dataset_version",
    "city_display_name",
    "country_code",
    "latitude_degrees_north",
    "longitude_degrees_east",
    "iana_timezone",
    "location_resolution",
    "coordinate_source_record",
}


def resolve_location(value: LocationInput) -> ResolvedLocation:
    if isinstance(value, CoordinatesLocation):
        load_iana_timezone(value.iana_timezone)
        return ResolvedLocation(
            coordinates=Coordinates(latitude=value.latitude, longitude=value.longitude),
            iana_timezone=value.iana_timezone,
            resolution=LocationResolution.COORDINATES_SUPPLIED,
        )
    if isinstance(value, CityLocation):
        matches = [
            record
            for record in _city_records()
            if (
                record["city_display_name"] == value.city
                and record["country_code"] == value.country_code
            )
        ]
        if len(matches) != 1:
            raise DomainError(
                ErrorCode.LOCATION_RESOLUTION_FAILED,
                "controlled city record did not uniquely resolve",
            )
        record = matches[0]
        return ResolvedLocation(
            coordinates=Coordinates(
                latitude=record["latitude_degrees_north"],
                longitude=record["longitude_degrees_east"],
            ),
            iana_timezone=record["iana_timezone"],
            resolution=LocationResolution.CONTROLLED_CITY_DATASET,
            canonical_city_id=record["canonical_city_id"],
            city_display_name=record["city_display_name"],
            country_code=record["country_code"],
            city_dataset_version=record["city_dataset_version"],
        )
    raise TypeError("unsupported location input")


@cache
def _city_table() -> dict[str, Any]:
    try:
        resource = files("ziwei_qimen").joinpath("data", "astronomy", "city_coordinates.json")
        value = json.loads(resource.read_text(encoding="utf-8"))
        if (
            value["table_id"] != "astronomy.city_coordinates"
            or value["schema_version"] != "1.0.0"
            or value["source"] != CITY_TABLE_SOURCE
        ):
            raise ValueError
        records = value["records"]
        if not isinstance(records, list) or not records:
            raise ValueError
        for record in records:
            if not isinstance(record, dict) or set(record) != CITY_RECORD_FIELDS:
                raise ValueError
            if not isinstance(record["canonical_city_id"], str) or not record["canonical_city_id"]:
                raise ValueError
            if not isinstance(record["city_dataset_version"], str):
                raise ValueError
            if record["city_dataset_version"] != CITY_DATASET_VERSION:
                raise ValueError
            if not isinstance(record["city_display_name"], str) or not record["city_display_name"]:
                raise ValueError
            if re.fullmatch(r"[A-Z]{2}", record["country_code"]) is None:
                raise ValueError
            if not isinstance(record["latitude_degrees_north"], float | int):
                raise ValueError
            if not isinstance(record["longitude_degrees_east"], float | int):
                raise ValueError
            Coordinates(
                latitude=record["latitude_degrees_north"],
                longitude=record["longitude_degrees_east"],
            )
            if not isinstance(record["iana_timezone"], str) or not record["iana_timezone"]:
                raise ValueError
            load_iana_timezone(record["iana_timezone"])
            if record["location_resolution"] != "controlled_city_dataset":
                raise ValueError
            source_record = record["coordinate_source_record"]
            if not isinstance(source_record, str) or not source_record:
                raise ValueError
        if records != sorted(records, key=lambda record: record["canonical_city_id"]):
            raise ValueError
        if len(records) != len({record["canonical_city_id"] for record in records}):
            raise ValueError
        pairs = {(record["city_display_name"], record["country_code"]) for record in records}
        if len(records) != len(pairs):
            raise ValueError
        return cast(dict[str, Any], value)
    except (
        FileNotFoundError,
        KeyError,
        TypeError,
        ValueError,
        json.JSONDecodeError,
        DomainError,
    ) as error:
        raise DomainError(
            ErrorCode.LOCATION_RESOLUTION_FAILED,
            "controlled city dataset is unavailable",
        ) from error


def _city_records() -> tuple[dict[str, Any], ...]:
    return tuple(_city_table()["records"])
