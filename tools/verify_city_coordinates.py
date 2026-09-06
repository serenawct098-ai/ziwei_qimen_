from __future__ import annotations

import argparse
import hashlib
import json
import re
from importlib.resources import files
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

REQUIRED_RECORD_COUNT = 62
CITY_DATASET_VERSION = "natural-earth-10m-populated-places-5.1.2-primary-cities-v1"
IANA_TIMEZONE = re.compile(r"^[A-Za-z_+\-]+(?:/[A-Za-z_+\-]+)+$")
FORBIDDEN_FIELDS = {
    "utc_offset",
    "dst_offset",
    "current_offset",
    "fallback",
    "alias",
    "deprecated",
    "confidence",
    "residence_qualified",
    "qimen_location",
}
REQUIRED_RECORD_FIELDS = {
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


def canonical_bytes(value: dict[str, Any]) -> bytes:
    content = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (content + "\n").encode("utf-8")


def load_timezone(name: str) -> None:
    if IANA_TIMEZONE.fullmatch(name) is None:
        raise ValueError(f"invalid IANA timezone: {name}")
    resource = files("tzdata").joinpath("zoneinfo", *name.split("/"))
    with resource.open("rb") as handle:
        ZoneInfo.from_file(handle, key=name)


def verify(table_path: Path) -> str:
    payload = table_path.read_bytes()
    table = json.loads(payload.decode("utf-8"))
    if canonical_bytes(table) != payload:
        raise ValueError("city table is not canonical JSON")
    if (
        table.get("table_id") != "astronomy.city_coordinates"
        or table.get("schema_version") != "1.0.0"
    ):
        raise ValueError("city table identity mismatch")
    if table.get("source") != {
        "name": "Natural Earth 10m Populated Places",
        "version": "5.1.2",
        "license": "public_domain",
        "asset_logical_id": "natural_earth.ne_10m_populated_places",
    }:
        raise ValueError("city table source mismatch")
    records = table.get("records")
    if not isinstance(records, list) or len(records) != REQUIRED_RECORD_COUNT:
        raise ValueError("city table record count mismatch")
    if records != sorted(records, key=lambda record: record["canonical_city_id"]):
        raise ValueError("city table records are not sorted")
    if len({record["canonical_city_id"] for record in records}) != len(records):
        raise ValueError("canonical city IDs are not unique")
    pairs = {(record["city_display_name"], record["country_code"]) for record in records}
    if len(pairs) != len(records):
        raise ValueError("city and country pairs are not unique")
    for record in records:
        if set(record) != REQUIRED_RECORD_FIELDS or set(record) & FORBIDDEN_FIELDS:
            raise ValueError("city table fields are invalid")
        if not isinstance(record["canonical_city_id"], str) or not record["canonical_city_id"]:
            raise ValueError("canonical city ID is invalid")
        if record["city_dataset_version"] != CITY_DATASET_VERSION:
            raise ValueError("city dataset version is invalid")
        if not record["city_display_name"]:
            raise ValueError("city name is empty")
        if re.fullmatch(r"[A-Z]{2}", record["country_code"]) is None:
            raise ValueError("country code is invalid")
        if not -90 <= record["latitude_degrees_north"] <= 90:
            raise ValueError("latitude is invalid")
        if not -180 <= record["longitude_degrees_east"] <= 180:
            raise ValueError("longitude is invalid")
        if not record["coordinate_source_record"]:
            raise ValueError("source record identifier is empty")
        if record["location_resolution"] != "controlled_city_dataset":
            raise ValueError("location resolution is invalid")
        load_timezone(record["iana_timezone"])
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("table_path", type=Path)
    arguments = parser.parse_args()
    print(json.dumps({"sha256": verify(arguments.table_path)}, sort_keys=True))


if __name__ == "__main__":
    main()
