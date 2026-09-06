from __future__ import annotations

import hashlib
import inspect
import json
from datetime import date
from importlib.resources import files

import pytest

import ziwei_qimen.time.lunar_calendar as lunar_calendar
from ziwei_qimen.errors import DomainError, ErrorCode
from ziwei_qimen.time.lunar_calendar import _calendar_table, resolve_hko_lunar_date


class BrokenResource:
    def joinpath(self, *parts: str) -> BrokenResource:
        return self

    def read_bytes(self) -> bytes:
        return b"{}"


class ResourceRoot:
    def __init__(self, resources: dict[str, bytes]) -> None:
        self.resources = resources

    def joinpath(self, *parts: str) -> ResourceValue:
        return ResourceValue(self.resources[parts[-1]])


class ResourceValue:
    def __init__(self, value: bytes) -> None:
        self.value = value

    def read_bytes(self) -> bytes:
        return self.value


def _canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def _resources_for_table(table: dict[str, object]) -> dict[str, bytes]:
    asset_bytes = _canonical_bytes(table)
    manifest = json.loads(
        files("ziwei_qimen")
        .joinpath("data", "calendar", "calendar_asset_manifest.json")
        .read_bytes()
    )
    manifest["assets"][0]["sha256"] = hashlib.sha256(asset_bytes).hexdigest()
    manifest["assets"][0]["size_bytes"] = len(asset_bytes)
    manifest["integrity"]["manifest_sha256"] = ""
    manifest["integrity"]["manifest_sha256"] = hashlib.sha256(
        _canonical_bytes(manifest)
    ).hexdigest()
    return {
        "calendar_asset_manifest.json": _canonical_bytes(manifest),
        "hong_kong_lunar_calendar_1901_2100.json": asset_bytes,
    }


def test_calendar_asset_and_manifest_are_packaged_and_canonical() -> None:
    asset = files("ziwei_qimen").joinpath(
        "data", "calendar", "hong_kong_lunar_calendar_1901_2100.json"
    )
    manifest = files("ziwei_qimen").joinpath("data", "calendar", "calendar_asset_manifest.json")
    asset_bytes = asset.read_bytes()
    manifest_bytes = manifest.read_bytes()
    table = json.loads(asset_bytes)
    manifest_value = json.loads(manifest_bytes)
    manifest_preimage = json.loads(manifest_bytes)
    manifest_preimage["integrity"]["manifest_sha256"] = ""

    assert asset_bytes == (
        json.dumps(table, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    assert manifest_bytes == (
        json.dumps(manifest_value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    assert (
        hashlib.sha256(
            (
                json.dumps(
                    manifest_preimage, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                )
                + "\n"
            ).encode("utf-8")
        ).hexdigest()
        == manifest_value["integrity"]["manifest_sha256"]
    )
    assert len(table["records"]) == 73049
    assert manifest_value["assets"] == [
        {
            **manifest_value["assets"][0],
            "sha256": hashlib.sha256(asset_bytes).hexdigest(),
            "size_bytes": len(asset_bytes),
        }
    ]


def test_calendar_table_has_exact_fields_and_boundary_metadata() -> None:
    table = _calendar_table()
    records = table["records"]

    assert len(records) == 73049
    assert table["coverage"] == {"start": "1901-01-01", "end": "2100-12-31"}
    assert table["table_id"] == "calendar.hko_gregorian_lunar_1901_2100"
    assert table["schema_version"] == "1.0.0"
    assert all(
        set(record)
        == {
            "gregorian_date",
            "lunar_year",
            "lunar_month",
            "lunar_day",
            "is_leap_month",
            "solar_term",
        }
        for record in records
    )
    assert table["boundary_semantics"]["closed_month_count"] == 2473
    assert table["boundary_semantics"]["left_boundary_partial_month"]["month_length"] is None
    assert table["boundary_semantics"]["right_boundary_partial_month"]["month_length"] is None


def test_calendar_loader_rejects_broken_package_asset(monkeypatch: pytest.MonkeyPatch) -> None:
    lunar_calendar._calendar_index.cache_clear()
    lunar_calendar._calendar_table.cache_clear()
    monkeypatch.setattr(lunar_calendar, "files", lambda package: BrokenResource())

    with pytest.raises(DomainError) as error:
        resolve_hko_lunar_date(date(1901, 1, 1))

    lunar_calendar._calendar_table.cache_clear()
    assert error.value.code is ErrorCode.CALENDAR_ASSET_UNAVAILABLE


@pytest.mark.parametrize(
    ("field", "value"),
    [("table_id", "calendar.invalid"), ("schema_version", "9.9.9")],
)
def test_calendar_loader_rejects_invalid_table_identity(
    monkeypatch: pytest.MonkeyPatch, field: str, value: str
) -> None:
    table = json.loads(
        files("ziwei_qimen")
        .joinpath("data", "calendar", "hong_kong_lunar_calendar_1901_2100.json")
        .read_bytes()
    )
    table[field] = value
    lunar_calendar._calendar_index.cache_clear()
    lunar_calendar._calendar_table.cache_clear()
    monkeypatch.setattr(
        lunar_calendar, "files", lambda package: ResourceRoot(_resources_for_table(table))
    )

    with pytest.raises(DomainError) as error:
        resolve_hko_lunar_date(date(1901, 1, 1))

    lunar_calendar._calendar_index.cache_clear()
    lunar_calendar._calendar_table.cache_clear()
    assert error.value.code is ErrorCode.CALENDAR_ASSET_UNAVAILABLE


def test_calendar_loader_has_no_network_or_audit_path_dependency() -> None:
    source = inspect.getsource(lunar_calendar)

    assert "/home/ubuntu/audits" not in source
    assert "http" not in source
    assert "socket" not in source
