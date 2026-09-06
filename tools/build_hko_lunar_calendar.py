from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path
from typing import Any, cast

DRAFT_SHA256 = "e5f1d2303e245b1e5d3dd014d7512dd9add206e054b749e399a832c41ab818a6"
RAW_INVENTORY_SHA256 = "5439eb70e5a9556c8ffa9794e34cd0c0c63d0a118ea30ceb3b0c7175777e3df9"
RAW_INVENTORY_SELF_HASH = "53e55d78b1ad400417e07b0d745dc8613d791faf0fd7e6f56f5c9dd7797dcdec"
RAW_AGGREGATE_SHA256 = "39c18f06dbe81203fe9551a048bd1d4a757a7a71adf94c76a608d71282c1d552"
PARSER_REPORT_SHA256 = "ae92e9c9c95a4001aea9ebfb620c2099e962376b0e4b3c61f698b36076558b16"
BOUNDARY_SEMANTICS_SHA256 = "3e16dc39fe52d6b84c4f3bf48a6cfe73ac883f619e717f58f7b578e2d9b8afac"
RECORD_FIELDS = {
    "gregorian_date",
    "lunar_year",
    "lunar_month",
    "lunar_day",
    "is_leap_month",
    "solar_term",
    "source_year",
    "source_filename",
    "source_line_number",
}
RUNTIME_FIELDS = {
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


def canonical_bytes(value: object) -> bytes:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (serialized + "\n").encode("utf-8")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def parse_date(value: object) -> date:
    if not isinstance(value, str):
        raise ValueError("calendar record date is invalid")
    return date.fromisoformat(value)


def record_key(record: dict[str, Any]) -> tuple[int, int, bool]:
    return (
        cast(int, record["lunar_year"]),
        cast(int, record["lunar_month"]),
        cast(bool, record["is_leap_month"]),
    )


def validate_records(records: object) -> list[dict[str, Any]]:
    if not isinstance(records, list) or len(records) != 73049:
        raise ValueError("calendar draft record count is invalid")
    validated: list[dict[str, Any]] = []
    previous: date | None = None
    terms_by_year: dict[int, list[str]] = defaultdict(list)
    groups: dict[tuple[int, int, bool], list[dict[str, Any]]] = defaultdict(list)
    for raw_record in records:
        if not isinstance(raw_record, dict) or set(raw_record) != RECORD_FIELDS:
            raise ValueError("calendar draft fields are invalid")
        record = cast(dict[str, Any], raw_record)
        current = parse_date(record["gregorian_date"])
        if current.year != record["source_year"]:
            raise ValueError("calendar draft source year is invalid")
        if record["source_filename"] != f"T{current.year}c.txt":
            raise ValueError("calendar draft source filename is invalid")
        if not isinstance(record["source_line_number"], int) or record["source_line_number"] < 1:
            raise ValueError("calendar draft source line is invalid")
        if not isinstance(record["lunar_year"], int):
            raise ValueError("calendar draft lunar year is invalid")
        if not isinstance(record["lunar_month"], int) or not 1 <= record["lunar_month"] <= 12:
            raise ValueError("calendar draft lunar month is invalid")
        if not isinstance(record["lunar_day"], int) or not 1 <= record["lunar_day"] <= 30:
            raise ValueError("calendar draft lunar day is invalid")
        if not isinstance(record["is_leap_month"], bool):
            raise ValueError("calendar draft leap flag is invalid")
        if record["solar_term"] is not None and record["solar_term"] not in SOLAR_TERMS:
            raise ValueError("calendar draft solar term is invalid")
        if previous is not None and current != previous + timedelta(days=1):
            raise ValueError("calendar draft dates are not continuous")
        previous = current
        if record["solar_term"] is not None:
            terms_by_year[current.year].append(cast(str, record["solar_term"]))
        groups[record_key(record)].append(record)
        validated.append(record)
    if parse_date(validated[0]["gregorian_date"]) != date(1901, 1, 1):
        raise ValueError("calendar draft start date is invalid")
    if parse_date(validated[-1]["gregorian_date"]) != date(2100, 12, 31):
        raise ValueError("calendar draft end date is invalid")
    for year in range(1901, 2101):
        if len(terms_by_year[year]) != 24 or set(terms_by_year[year]) != SOLAR_TERMS:
            raise ValueError("calendar draft solar term coverage is invalid")
    closed_count = 0
    for group in groups.values():
        first = group[0]
        last = group[-1]
        first_date = parse_date(first["gregorian_date"])
        last_date = parse_date(last["gregorian_date"])
        if first_date == date(1901, 1, 1):
            if record_key(first) != (1900, 11, False):
                raise ValueError("calendar left boundary is invalid")
            continue
        if last_date == date(2100, 12, 31):
            if record_key(last) != (2100, 12, False) or last["lunar_day"] != 1:
                raise ValueError("calendar right boundary is invalid")
            continue
        if (
            first["lunar_day"] != 1
            or last["lunar_day"] not in (29, 30)
            or len(group) != last["lunar_day"]
        ):
            raise ValueError("calendar closed month is invalid")
        closed_count += 1
    leap_counts = Counter(key[0] for key in groups if key[2])
    if any(count > 1 for count in leap_counts.values()):
        raise ValueError("calendar draft has multiple leap months in a lunar year")
    for lunar_year, lunar_month, is_leap_month in groups:
        if is_leap_month and (lunar_year, lunar_month, False) not in groups:
            raise ValueError("calendar draft leap month lacks an ordinary month")
    if closed_count != 2473 or len(groups) != 2475:
        raise ValueError("calendar month classification is invalid")
    return validated


def runtime_record(record: dict[str, Any]) -> dict[str, Any]:
    return {field: record[field] for field in RUNTIME_FIELDS}


def build_table(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "boundary_semantics": {
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
        },
        "coverage": {"end": "2100-12-31", "start": "1901-01-01"},
        "record_count": 73049,
        "records": [runtime_record(record) for record in records],
        "schema_version": "1.0.0",
        "source": {
            "dataset": "Gregorian-Lunar Calendar Conversion Table",
            "provider": "Hong Kong Observatory",
            "source_format": "annual_traditional_chinese_text_files",
            "source_language": "zh-Hant",
        },
        "table_id": "calendar.hko_gregorian_lunar_1901_2100",
        "validation_status": "passed_with_explicit_coverage_boundary",
    }


def build_manifest(asset_bytes: bytes) -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "assets": [
            {
                "boundary_semantics_report_sha256": BOUNDARY_SEMANTICS_SHA256,
                "coverage_end": "2100-12-31",
                "coverage_start": "1901-01-01",
                "filename": "hong_kong_lunar_calendar_1901_2100.json",
                "local_path": (
                    "src/ziwei_qimen/data/calendar/hong_kong_lunar_calendar_1901_2100.json"
                ),
                "logical_id": "calendar.hko_gregorian_lunar_1901_2100",
                "parser_revalidation_draft_sha256": DRAFT_SHA256,
                "parser_revalidation_report_sha256": PARSER_REPORT_SHA256,
                "provider": "Hong Kong Observatory",
                "raw_inventory_file_sha256": RAW_INVENTORY_SHA256,
                "raw_inventory_self_hash": RAW_INVENTORY_SELF_HASH,
                "raw_payload_aggregate_sha256": RAW_AGGREGATE_SHA256,
                "record_count": 73049,
                "runtime_status": "package_runtime_asset",
                "sha256": digest(asset_bytes),
                "size_bytes": len(asset_bytes),
                "source_kind": "official_gregorian_lunar_conversion_table",
                "source_language": "zh-Hant",
                "validation_status": "passed_with_explicit_coverage_boundary",
            }
        ],
        "build": {
            "canonical_json": {
                "encoding": "utf-8",
                "ensure_ascii": False,
                "separators": [",", ":"],
                "sort_keys": True,
                "trailing_newline": True,
            }
        },
        "integrity": {"manifest_sha256": ""},
        "manifest_id": "calendar.asset_manifest",
        "schema_version": "1.0.0",
    }
    manifest["integrity"]["manifest_sha256"] = digest(canonical_bytes(manifest))
    return manifest


def write_atomic(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(payload)
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--asset", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    arguments = parser.parse_args()
    draft_bytes = arguments.draft.read_bytes()
    if digest(draft_bytes) != DRAFT_SHA256:
        raise ValueError("calendar draft SHA-256 does not match the locked audit")
    records = validate_records(json.loads(draft_bytes.decode("utf-8")))
    table = build_table(records)
    asset_bytes = canonical_bytes(table)
    manifest = build_manifest(asset_bytes)
    write_atomic(arguments.asset, asset_bytes)
    write_atomic(arguments.manifest, canonical_bytes(manifest))


if __name__ == "__main__":
    main()
