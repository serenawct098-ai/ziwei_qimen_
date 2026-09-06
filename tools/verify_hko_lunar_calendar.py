from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path
from typing import Any, cast

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
ASSET_FIELDS = {
    "boundary_semantics_report_sha256",
    "coverage_end",
    "coverage_start",
    "filename",
    "local_path",
    "logical_id",
    "parser_revalidation_draft_sha256",
    "parser_revalidation_report_sha256",
    "provider",
    "raw_inventory_file_sha256",
    "raw_inventory_self_hash",
    "raw_payload_aggregate_sha256",
    "record_count",
    "runtime_status",
    "sha256",
    "size_bytes",
    "source_kind",
    "source_language",
    "validation_status",
}
FIXED_ASSET = {
    "boundary_semantics_report_sha256": (
        "3e16dc39fe52d6b84c4f3bf48a6cfe73ac883f619e717f58f7b578e2d9b8afac"
    ),
    "coverage_end": "2100-12-31",
    "coverage_start": "1901-01-01",
    "filename": "hong_kong_lunar_calendar_1901_2100.json",
    "local_path": "src/ziwei_qimen/data/calendar/hong_kong_lunar_calendar_1901_2100.json",
    "logical_id": "calendar.hko_gregorian_lunar_1901_2100",
    "parser_revalidation_draft_sha256": (
        "e5f1d2303e245b1e5d3dd014d7512dd9add206e054b749e399a832c41ab818a6"
    ),
    "parser_revalidation_report_sha256": (
        "ae92e9c9c95a4001aea9ebfb620c2099e962376b0e4b3c61f698b36076558b16"
    ),
    "provider": "Hong Kong Observatory",
    "raw_inventory_file_sha256": (
        "5439eb70e5a9556c8ffa9794e34cd0c0c63d0a118ea30ceb3b0c7175777e3df9"
    ),
    "raw_inventory_self_hash": ("53e55d78b1ad400417e07b0d745dc8613d791faf0fd7e6f56f5c9dd7797dcdec"),
    "raw_payload_aggregate_sha256": (
        "39c18f06dbe81203fe9551a048bd1d4a757a7a71adf94c76a608d71282c1d552"
    ),
    "record_count": 73049,
    "runtime_status": "package_runtime_asset",
    "source_kind": "official_gregorian_lunar_conversion_table",
    "source_language": "zh-Hant",
    "validation_status": "passed_with_explicit_coverage_boundary",
}


def canonical_bytes(value: object) -> bytes:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (serialized + "\n").encode("utf-8")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def parse_date(value: object) -> date:
    if not isinstance(value, str):
        raise ValueError("invalid Gregorian date")
    return date.fromisoformat(value)


def record_key(record: dict[str, Any]) -> tuple[int, int, bool]:
    return (
        cast(int, record["lunar_year"]),
        cast(int, record["lunar_month"]),
        cast(bool, record["is_leap_month"]),
    )


def validate_table(asset_bytes: bytes) -> dict[str, Any]:
    table = json.loads(asset_bytes.decode("utf-8"))
    if asset_bytes != canonical_bytes(table) or not isinstance(table, dict):
        raise ValueError("runtime table is not canonical JSON")
    expected_table_fields = {
        "boundary_semantics",
        "coverage",
        "record_count",
        "records",
        "schema_version",
        "source",
        "table_id",
        "validation_status",
    }
    if set(table) != expected_table_fields:
        raise ValueError("runtime table fields are invalid")
    if table["table_id"] != "calendar.hko_gregorian_lunar_1901_2100":
        raise ValueError("runtime table identity is invalid")
    if table["schema_version"] != "1.0.0":
        raise ValueError("runtime table schema is invalid")
    if table["source"] != {
        "dataset": "Gregorian-Lunar Calendar Conversion Table",
        "provider": "Hong Kong Observatory",
        "source_format": "annual_traditional_chinese_text_files",
        "source_language": "zh-Hant",
    }:
        raise ValueError("runtime table source is invalid")
    if table["coverage"] != {"end": "2100-12-31", "start": "1901-01-01"}:
        raise ValueError("runtime table coverage is invalid")
    records = table["records"]
    if table["record_count"] != 73049 or not isinstance(records, list) or len(records) != 73049:
        raise ValueError("runtime table record count is invalid")
    terms_by_year: dict[int, list[str]] = defaultdict(list)
    groups: dict[tuple[int, int, bool], list[dict[str, Any]]] = defaultdict(list)
    previous_date: date | None = None
    for raw_record in records:
        if not isinstance(raw_record, dict) or set(raw_record) != RECORD_FIELDS:
            raise ValueError("runtime record fields are invalid")
        record = cast(dict[str, Any], raw_record)
        current_date = parse_date(record["gregorian_date"])
        if not 1901 <= current_date.year <= 2100:
            raise ValueError("runtime record is outside coverage")
        if previous_date is not None and current_date != previous_date + timedelta(days=1):
            raise ValueError("runtime Gregorian records are not continuous")
        previous_date = current_date
        if not isinstance(record["lunar_year"], int):
            raise ValueError("runtime lunar year is invalid")
        if not isinstance(record["lunar_month"], int) or not 1 <= record["lunar_month"] <= 12:
            raise ValueError("runtime lunar month is invalid")
        if not isinstance(record["lunar_day"], int) or not 1 <= record["lunar_day"] <= 30:
            raise ValueError("runtime lunar day is invalid")
        if not isinstance(record["is_leap_month"], bool):
            raise ValueError("runtime leap flag is invalid")
        solar_term = record["solar_term"]
        if solar_term is not None and solar_term not in SOLAR_TERMS:
            raise ValueError("runtime solar term is invalid")
        if solar_term is not None:
            terms_by_year[current_date.year].append(cast(str, solar_term))
        key = record_key(record)
        groups[key].append(record)
    if parse_date(cast(dict[str, Any], records[0])["gregorian_date"]) != date(1901, 1, 1):
        raise ValueError("runtime start is invalid")
    if parse_date(cast(dict[str, Any], records[-1])["gregorian_date"]) != date(2100, 12, 31):
        raise ValueError("runtime end is invalid")
    leap_counts = Counter(key[0] for key in groups if key[2])
    if any(count > 1 for count in leap_counts.values()):
        raise ValueError("multiple leap months in lunar year")
    for lunar_year, lunar_month, is_leap_month in groups:
        if is_leap_month and (lunar_year, lunar_month, False) not in groups:
            raise ValueError("leap month lacks an ordinary month")
    for year in range(1901, 2101):
        if len(terms_by_year[year]) != 24 or set(terms_by_year[year]) != SOLAR_TERMS:
            raise ValueError("runtime solar term coverage is invalid")
    closed_months = 0
    for key, group in groups.items():
        first = group[0]
        last = group[-1]
        first_date = parse_date(first["gregorian_date"])
        last_date = parse_date(last["gregorian_date"])
        if first_date == date(1901, 1, 1):
            if key != (1900, 11, False):
                raise ValueError("left boundary partial month is invalid")
            continue
        if last_date == date(2100, 12, 31):
            if key != (2100, 12, False) or last["lunar_day"] != 1:
                raise ValueError("right boundary partial month is invalid")
            continue
        if (
            first["lunar_day"] != 1
            or last["lunar_day"] not in (29, 30)
            or len(group) != last["lunar_day"]
        ):
            raise ValueError("closed month length is invalid")
        closed_months += 1
    if len(groups) != 2475 or closed_months != 2473:
        raise ValueError("runtime month counts are invalid")
    expected_boundary = {
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
    }
    if table["boundary_semantics"] != expected_boundary:
        raise ValueError("runtime boundary metadata is invalid")
    if table["validation_status"] != "passed_with_explicit_coverage_boundary":
        raise ValueError("runtime validation status is invalid")
    return table


def validate_manifest(manifest_bytes: bytes, asset_bytes: bytes) -> None:
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    if manifest_bytes != canonical_bytes(manifest) or not isinstance(manifest, dict):
        raise ValueError("calendar manifest is not canonical JSON")
    if set(manifest) != {"assets", "build", "integrity", "manifest_id", "schema_version"}:
        raise ValueError("calendar manifest fields are invalid")
    if (
        manifest["manifest_id"] != "calendar.asset_manifest"
        or manifest["schema_version"] != "1.0.0"
    ):
        raise ValueError("calendar manifest identity is invalid")
    if manifest["build"] != {
        "canonical_json": {
            "encoding": "utf-8",
            "ensure_ascii": False,
            "separators": [",", ":"],
            "sort_keys": True,
            "trailing_newline": True,
        }
    }:
        raise ValueError("calendar manifest build metadata is invalid")
    integrity = manifest["integrity"]
    if not isinstance(integrity, dict) or set(integrity) != {"manifest_sha256"}:
        raise ValueError("calendar manifest integrity field is invalid")
    preimage = json.loads(manifest_bytes.decode("utf-8"))
    preimage["integrity"]["manifest_sha256"] = ""
    if integrity["manifest_sha256"] != digest(canonical_bytes(preimage)):
        raise ValueError("calendar manifest self hash is invalid")
    assets = manifest["assets"]
    if not isinstance(assets, list) or len(assets) != 1 or not isinstance(assets[0], dict):
        raise ValueError("calendar manifest asset count is invalid")
    asset = cast(dict[str, Any], assets[0])
    if set(asset) != ASSET_FIELDS:
        raise ValueError("calendar manifest asset fields are invalid")
    for field, value in FIXED_ASSET.items():
        if asset[field] != value:
            raise ValueError(f"calendar manifest asset field is invalid: {field}")
    if asset["sha256"] != digest(asset_bytes) or asset["size_bytes"] != len(asset_bytes):
        raise ValueError("calendar manifest asset checksum is invalid")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    arguments = parser.parse_args()
    asset_bytes = arguments.asset.read_bytes()
    validate_table(asset_bytes)
    validate_manifest(arguments.manifest.read_bytes(), asset_bytes)
    print(f"asset_bytes={len(asset_bytes)}")
    print(f"asset_sha256={digest(asset_bytes)}")
    print("verification_status=passed")


if __name__ == "__main__":
    main()
