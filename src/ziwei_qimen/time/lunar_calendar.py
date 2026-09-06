from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import date, timedelta
from functools import cache
from importlib.resources import files
from typing import Any, cast

from ziwei_qimen.domain.models import LunarDateResolution
from ziwei_qimen.errors import DomainError, ErrorCode

ASSET_NAME = "hong_kong_lunar_calendar_1901_2100.json"
MANIFEST_NAME = "calendar_asset_manifest.json"
RECORD_FIELDS = {
    "gregorian_date",
    "lunar_year",
    "lunar_month",
    "lunar_day",
    "is_leap_month",
    "solar_term",
}
SOLAR_TERMS = {
    "小寒",
    "大寒",
    "立春",
    "雨水",
    "驚蟄",
    "春分",
    "清明",
    "穀雨",
    "立夏",
    "小滿",
    "芒種",
    "夏至",
    "小暑",
    "大暑",
    "立秋",
    "處暑",
    "白露",
    "秋分",
    "寒露",
    "霜降",
    "立冬",
    "小雪",
    "大雪",
    "冬至",
}
SOURCE = {
    "dataset": "Gregorian-Lunar Calendar Conversion Table",
    "provider": "Hong Kong Observatory",
    "source_format": "annual_traditional_chinese_text_files",
    "source_language": "zh-Hant",
}


def _canonical_bytes(value: object) -> bytes:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (serialized + "\n").encode("utf-8")


def _digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _date(value: object) -> date:
    if not isinstance(value, str):
        raise ValueError
    return date.fromisoformat(value)


def _month_key(record: dict[str, Any]) -> tuple[int, int, bool]:
    return (
        cast(int, record["lunar_year"]),
        cast(int, record["lunar_month"]),
        cast(bool, record["is_leap_month"]),
    )


def _load_manifest(asset_bytes: bytes) -> None:
    manifest_bytes = files("ziwei_qimen").joinpath("data", "calendar", MANIFEST_NAME).read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    if manifest_bytes != _canonical_bytes(manifest) or not isinstance(manifest, dict):
        raise ValueError
    if set(manifest) != {"assets", "build", "integrity", "manifest_id", "schema_version"}:
        raise ValueError
    if (
        manifest["manifest_id"] != "calendar.asset_manifest"
        or manifest["schema_version"] != "1.0.0"
    ):
        raise ValueError
    if manifest["build"] != {
        "canonical_json": {
            "encoding": "utf-8",
            "ensure_ascii": False,
            "separators": [",", ":"],
            "sort_keys": True,
            "trailing_newline": True,
        }
    }:
        raise ValueError
    integrity = manifest["integrity"]
    if not isinstance(integrity, dict) or set(integrity) != {"manifest_sha256"}:
        raise ValueError
    expected_hash = integrity["manifest_sha256"]
    if not isinstance(expected_hash, str):
        raise ValueError
    preimage = json.loads(manifest_bytes.decode("utf-8"))
    preimage["integrity"]["manifest_sha256"] = ""
    if _digest(_canonical_bytes(preimage)) != expected_hash:
        raise ValueError
    assets = manifest["assets"]
    if not isinstance(assets, list) or len(assets) != 1 or not isinstance(assets[0], dict):
        raise ValueError
    asset = cast(dict[str, Any], assets[0])
    if asset["logical_id"] != "calendar.hko_gregorian_lunar_1901_2100":
        raise ValueError
    if asset["filename"] != ASSET_NAME:
        raise ValueError
    if asset["local_path"] != f"src/ziwei_qimen/data/calendar/{ASSET_NAME}":
        raise ValueError
    if asset["runtime_status"] != "package_runtime_asset":
        raise ValueError
    if asset["record_count"] != 73049:
        raise ValueError
    if asset["coverage_start"] != "1901-01-01" or asset["coverage_end"] != "2100-12-31":
        raise ValueError
    if asset["sha256"] != _digest(asset_bytes) or asset["size_bytes"] != len(asset_bytes):
        raise ValueError


def _validate_table(value: object) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError
    table = cast(dict[str, Any], value)
    if set(table) != {
        "boundary_semantics",
        "coverage",
        "record_count",
        "records",
        "schema_version",
        "source",
        "table_id",
        "validation_status",
    }:
        raise ValueError
    if table["table_id"] != "calendar.hko_gregorian_lunar_1901_2100":
        raise ValueError
    if table["schema_version"] != "1.0.0" or table["source"] != SOURCE:
        raise ValueError
    if table["coverage"] != {"end": "2100-12-31", "start": "1901-01-01"}:
        raise ValueError
    if (
        table["record_count"] != 73049
        or table["validation_status"] != "passed_with_explicit_coverage_boundary"
    ):
        raise ValueError
    records = table["records"]
    if not isinstance(records, list) or len(records) != 73049:
        raise ValueError
    groups: dict[tuple[int, int, bool], list[dict[str, Any]]] = defaultdict(list)
    terms_by_year: dict[int, list[str]] = defaultdict(list)
    previous: date | None = None
    for raw_record in records:
        if not isinstance(raw_record, dict) or set(raw_record) != RECORD_FIELDS:
            raise ValueError
        record = cast(dict[str, Any], raw_record)
        current = _date(record["gregorian_date"])
        if current.year not in range(1901, 2101):
            raise ValueError
        if previous is not None and current != previous + timedelta(days=1):
            raise ValueError
        previous = current
        if not isinstance(record["lunar_year"], int):
            raise ValueError
        if not isinstance(record["lunar_month"], int) or not 1 <= record["lunar_month"] <= 12:
            raise ValueError
        if not isinstance(record["lunar_day"], int) or not 1 <= record["lunar_day"] <= 30:
            raise ValueError
        if not isinstance(record["is_leap_month"], bool):
            raise ValueError
        solar_term = record["solar_term"]
        if solar_term is not None and solar_term not in SOLAR_TERMS:
            raise ValueError
        if solar_term is not None:
            terms_by_year[current.year].append(cast(str, solar_term))
        groups[_month_key(record)].append(record)
    if _date(cast(dict[str, Any], records[0])["gregorian_date"]) != date(1901, 1, 1):
        raise ValueError
    if _date(cast(dict[str, Any], records[-1])["gregorian_date"]) != date(2100, 12, 31):
        raise ValueError
    for year in range(1901, 2101):
        if len(terms_by_year[year]) != 24 or set(terms_by_year[year]) != SOLAR_TERMS:
            raise ValueError
    closed_month_count = 0
    for key, month_records in groups.items():
        first = month_records[0]
        last = month_records[-1]
        first_date = _date(first["gregorian_date"])
        last_date = _date(last["gregorian_date"])
        if first_date == date(1901, 1, 1):
            if key != (1900, 11, False):
                raise ValueError
            continue
        if last_date == date(2100, 12, 31):
            if key != (2100, 12, False) or last["lunar_day"] != 1:
                raise ValueError
            continue
        if first["lunar_day"] != 1 or last["lunar_day"] not in (29, 30):
            raise ValueError
        if len(month_records) != last["lunar_day"]:
            raise ValueError
        closed_month_count += 1
    leap_counts = Counter(key[0] for key in groups if key[2])
    if any(count > 1 for count in leap_counts.values()):
        raise ValueError
    for lunar_year, lunar_month, is_leap_month in groups:
        if is_leap_month and (lunar_year, lunar_month, False) not in groups:
            raise ValueError
    if len(groups) != 2475 or closed_month_count != 2473:
        raise ValueError
    if table["boundary_semantics"] != {
        "closed_month_count": 2473,
        "left_boundary_partial_month": {
            "is_leap_month": False,
            "lunar_month": 11,
            "lunar_year": 1900,
            "month_length": None,
        },
        "right_boundary_partial_month": {
            "is_leap_month": False,
            "lunar_month": 12,
            "lunar_year": 2100,
            "month_length": None,
        },
    }:
        raise ValueError
    return table


@cache
def _calendar_table() -> dict[str, Any]:
    try:
        asset_bytes = files("ziwei_qimen").joinpath("data", "calendar", ASSET_NAME).read_bytes()
        table = json.loads(asset_bytes.decode("utf-8"))
        if asset_bytes != _canonical_bytes(table):
            raise ValueError
        _load_manifest(asset_bytes)
        return _validate_table(table)
    except (FileNotFoundError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise DomainError(
            ErrorCode.CALENDAR_ASSET_UNAVAILABLE,
            "HKO calendar asset is unavailable",
        ) from error


@cache
def _calendar_index() -> dict[date, dict[str, Any]]:
    records = _calendar_table()["records"]
    return {_date(record["gregorian_date"]): record for record in records}


def resolve_hko_lunar_date(gregorian_date: date) -> LunarDateResolution:
    if type(gregorian_date) is not date:
        raise TypeError("gregorian_date must be datetime.date")
    if not date(1901, 1, 1) <= gregorian_date <= date(2100, 12, 31):
        raise DomainError(
            ErrorCode.CALENDAR_DATE_OUT_OF_RANGE,
            "gregorian_date is outside HKO calendar coverage",
        )
    record = _calendar_index().get(gregorian_date)
    if record is None:
        raise DomainError(
            ErrorCode.CALENDAR_ASSET_UNAVAILABLE,
            "HKO calendar asset does not resolve a coverage date",
        )
    return LunarDateResolution(
        gregorian_date=gregorian_date,
        lunar_year=record["lunar_year"],
        lunar_month=record["lunar_month"],
        lunar_day=record["lunar_day"],
        is_leap_month=record["is_leap_month"],
        solar_term=record["solar_term"],
        dataset_version="1.0.0",
        source_provider="Hong Kong Observatory",
    )
