from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import zipfile
from importlib.resources import files
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import shapefile

NATURAL_EARTH_SHA256 = "cd149186f03d2603e0410da399b980a4357d0ac32d3a2305a49ed3dffcc41d7b"
NATURAL_EARTH_MEMBERS = (
    "ne_10m_populated_places.shp",
    "ne_10m_populated_places.shx",
    "ne_10m_populated_places.dbf",
)
CITY_DATASET_VERSION = "natural-earth-10m-populated-places-5.1.2-primary-cities-v1"
APPROVED_CITIES = (
    ("Adelaide", "AU", "Australia/Adelaide", "NAME"),
    ("Amsterdam", "NL", "Europe/Amsterdam", "NAME"),
    ("Auckland", "NZ", "Pacific/Auckland", "NAME"),
    ("Bangkok", "TH", "Asia/Bangkok", "NAME"),
    ("Beijing", "CN", "Asia/Shanghai", "NAME"),
    ("Berlin", "DE", "Europe/Berlin", "NAME"),
    ("Boston", "US", "America/New_York", "NAME"),
    ("Brisbane", "AU", "Australia/Brisbane", "NAME"),
    ("Calgary", "CA", "America/Edmonton", "NAME"),
    ("Chengdu", "CN", "Asia/Shanghai", "NAME"),
    ("Chicago", "US", "America/Chicago", "NAME"),
    ("Chongqing", "CN", "Asia/Shanghai", "NAME"),
    ("Copenhagen", "DK", "Europe/Copenhagen", "NAME_EN"),
    ("Darwin", "AU", "Australia/Darwin", "NAME"),
    ("Denpasar", "ID", "Asia/Makassar", "NAME"),
    ("Denver", "US", "America/Denver", "NAME"),
    ("Dubai", "AE", "Asia/Dubai", "NAME"),
    ("Dublin", "IE", "Europe/Dublin", "NAME"),
    ("Guangzhou", "CN", "Asia/Shanghai", "NAME"),
    ("Helsinki", "FI", "Europe/Helsinki", "NAME"),
    ("Ho Chi Minh City", "VN", "Asia/Ho_Chi_Minh", "NAME"),
    ("Hong Kong", "HK", "Asia/Hong_Kong", "NAME"),
    ("Honolulu", "US", "Pacific/Honolulu", "NAME"),
    ("Houston", "US", "America/Chicago", "NAME"),
    ("Jakarta", "ID", "Asia/Jakarta", "NAME"),
    ("Kaohsiung", "TW", "Asia/Taipei", "NAME"),
    ("Kuala Lumpur", "MY", "Asia/Kuala_Lumpur", "NAME"),
    ("Lisbon", "PT", "Europe/Lisbon", "NAME"),
    ("London", "GB", "Europe/London", "NAME"),
    ("Los Angeles", "US", "America/Los_Angeles", "NAME"),
    ("Macau", "MO", "Asia/Macau", "NAME"),
    ("Madrid", "ES", "Europe/Madrid", "NAME"),
    ("Manila", "PH", "Asia/Manila", "NAME"),
    ("Melbourne", "AU", "Australia/Melbourne", "NAME"),
    ("Montreal", "CA", "America/Toronto", "NAMEASCII"),
    ("Mumbai", "IN", "Asia/Kolkata", "NAME"),
    ("New York", "US", "America/New_York", "NAME"),
    ("Osaka", "JP", "Asia/Tokyo", "NAMEASCII"),
    ("Oslo", "NO", "Europe/Oslo", "NAME"),
    ("Paris", "FR", "Europe/Paris", "NAME"),
    ("Perth", "AU", "Australia/Perth", "NAME"),
    ("Phoenix", "US", "America/Phoenix", "NAME"),
    ("Prague", "CZ", "Europe/Prague", "NAME"),
    ("Rome", "IT", "Europe/Rome", "NAME"),
    ("San Francisco", "US", "America/Los_Angeles", "NAME"),
    ("Sapporo", "JP", "Asia/Tokyo", "NAME"),
    ("Seattle", "US", "America/Los_Angeles", "NAME"),
    ("Seoul", "KR", "Asia/Seoul", "NAME"),
    ("Shanghai", "CN", "Asia/Shanghai", "NAME"),
    ("Shenzhen", "CN", "Asia/Shanghai", "NAME"),
    ("Singapore", "SG", "Asia/Singapore", "NAME"),
    ("Stockholm", "SE", "Europe/Stockholm", "NAME"),
    ("Sydney", "AU", "Australia/Sydney", "NAME"),
    ("Taipei", "TW", "Asia/Taipei", "NAME"),
    ("Tokyo", "JP", "Asia/Tokyo", "NAME"),
    ("Toronto", "CA", "America/Toronto", "NAME"),
    ("Vancouver", "CA", "America/Vancouver", "NAME"),
    ("Vienna", "AT", "Europe/Vienna", "NAME"),
    ("Warsaw", "PL", "Europe/Warsaw", "NAME"),
    ("Washington, D.C.", "US", "America/New_York", "NAMEASCII"),
    ("Wellington", "NZ", "Pacific/Auckland", "NAME"),
    ("Zurich", "CH", "Europe/Zurich", "NAMEASCII"),
)
IANA_TIMEZONE = re.compile(r"^[A-Za-z_+\-]+(?:/[A-Za-z_+\-]+)+$")


def canonical_bytes(value: dict[str, Any]) -> bytes:
    content = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (content + "\n").encode("utf-8")


def load_timezone(name: str) -> None:
    if IANA_TIMEZONE.fullmatch(name) is None:
        raise ValueError(f"invalid IANA timezone: {name}")
    resource = files("tzdata").joinpath("zoneinfo", *name.split("/"))
    with resource.open("rb") as handle:
        ZoneInfo.from_file(handle, key=name)


def read_records(source_zip: Path) -> list[dict[str, Any]]:
    payload = source_zip.read_bytes()
    if hashlib.sha256(payload).hexdigest() != NATURAL_EARTH_SHA256:
        raise ValueError("Natural Earth SHA-256 mismatch")
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        members = set(archive.namelist())
        if archive.testzip() is not None or not set(NATURAL_EARTH_MEMBERS) <= members:
            raise ValueError("Natural Earth ZIP structure mismatch")
        reader = shapefile.Reader(
            shp=io.BytesIO(archive.read(NATURAL_EARTH_MEMBERS[0])),
            shx=io.BytesIO(archive.read(NATURAL_EARTH_MEMBERS[1])),
            dbf=io.BytesIO(archive.read(NATURAL_EARTH_MEMBERS[2])),
        )
        records = []
        for item in reader.iterShapeRecords():
            if len(item.shape.points) != 1:
                raise ValueError("Natural Earth city geometry is not one point")
            record = item.record.as_dict()
            longitude, latitude = item.shape.points[0]
            records.append(record | {"latitude": latitude, "longitude": longitude})
        return records


def build_records(source_zip: Path) -> list[dict[str, Any]]:
    source_records = read_records(source_zip)
    records = []
    for city, country_code, iana_timezone, name_field in APPROVED_CITIES:
        matches = [
            source_record
            for source_record in source_records
            if source_record["ISO_A2"] == country_code and source_record[name_field] == city
        ]
        if len(matches) != 1:
            source_ids = [source_record.get("NE_ID") for source_record in matches]
            raise ValueError(
                f"source record count for {city}, {country_code}: "
                f"{len(matches)}; candidates: {source_ids}"
            )
        source_record = matches[0]
        load_timezone(iana_timezone)
        city_id = re.sub(r"[^a-z0-9]+", "-", city.lower()).strip("-")
        records.append(
            {
                "canonical_city_id": f"{city_id}-{country_code.lower()}",
                "city_dataset_version": CITY_DATASET_VERSION,
                "city_display_name": city,
                "country_code": country_code,
                "latitude_degrees_north": source_record["latitude"],
                "longitude_degrees_east": source_record["longitude"],
                "iana_timezone": iana_timezone,
                "location_resolution": "controlled_city_dataset",
                "coordinate_source_record": str(source_record["NE_ID"]),
            }
        )
    records.sort(key=lambda record: record["canonical_city_id"])
    if len(records) != len({record["canonical_city_id"] for record in records}):
        raise ValueError("canonical city IDs are not unique")
    pairs = {(record["city_display_name"], record["country_code"]) for record in records}
    if len(records) != len(pairs):
        raise ValueError("city and country pairs are not unique")
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--natural-earth-zip", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    table = {
        "table_id": "astronomy.city_coordinates",
        "schema_version": "1.0.0",
        "source": {
            "name": "Natural Earth 10m Populated Places",
            "version": "5.1.2",
            "license": "public_domain",
            "asset_logical_id": "natural_earth.ne_10m_populated_places",
        },
        "records": build_records(arguments.natural_earth_zip),
    }
    payload = canonical_bytes(table)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_bytes(payload)
    result = {"record_count": len(table["records"]), "sha256": hashlib.sha256(payload).hexdigest()}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
