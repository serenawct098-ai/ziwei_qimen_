import hashlib
import json
from importlib.resources import files
from importlib.resources.abc import Traversable

from ziwei_qimen.time.location import CITY_DATASET_VERSION

EXPECTED_CITY_SHA256 = "c79b404c202d43f9d38a8e052dfdb1309dba40408b03b8580536ec379a559916"
EXPECTED_MANIFEST_SHA256 = "a5da6c3f62b3dde1af7c75357315acaebb2de59364cbe1236d38eb2ac2b80392"


def _resource(filename: str) -> Traversable:
    return files("ziwei_qimen").joinpath("data", "astronomy", filename)


def _canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def test_city_table_is_packaged_and_versioned() -> None:
    payload = _resource("city_coordinates.json").read_bytes()
    table = json.loads(payload.decode("utf-8"))

    assert len(table["records"]) == 62
    assert all(
        record["city_dataset_version"] == CITY_DATASET_VERSION for record in table["records"]
    )
    assert hashlib.sha256(payload).hexdigest() == EXPECTED_CITY_SHA256


def test_manifest_is_packaged_and_self_verifying() -> None:
    payload = _resource("asset_manifest.json").read_bytes()
    manifest = json.loads(payload.decode("utf-8"))

    assert _canonical_bytes(manifest) == payload
    assert manifest["integrity"]["manifest_sha256"] == EXPECTED_MANIFEST_SHA256
    manifest["integrity"]["manifest_sha256"] = ""
    assert hashlib.sha256(_canonical_bytes(manifest)).hexdigest() == EXPECTED_MANIFEST_SHA256


def test_city_table_has_unique_display_name_and_country_pairs() -> None:
    payload = _resource("city_coordinates.json").read_text(encoding="utf-8")
    table = json.loads(payload)
    pairs = [(record["city_display_name"], record["country_code"]) for record in table["records"]]

    assert len(pairs) == len(set(pairs))
