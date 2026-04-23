from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath


ROOT = Path(os.getenv("ISRAEL_NADLAN_DATA_ROOT", Path(__file__).resolve().parent.parent))
GEOGRAPHY_PATH = ROOT / "data" / "current" / "geography_reference.csv"
LOCALITY_CROSSWALK_PATH = ROOT / "data" / "current" / "locality_crosswalk.csv"
MANIFEST_PATH = ROOT / "metadata" / "manifest.json"
RELEASE_FILES_PATH = ROOT / "metadata" / "release_files.csv"
SOURCE_INVENTORY_PATH = ROOT / "metadata" / "source_inventory.csv"
LEGACY_CURRENT_FACT_PATH = ROOT / "data" / "current" / "rent_benchmarks.csv"

VALID_GEOGRAPHY_TYPES = {"locality", "district"}
GEOGRAPHY_REQUIRED_COLUMNS = {
    "geography_id",
    "geography_type",
    "locality_code",
    "district_code",
    "geography_name_he",
    "geography_name_en",
    "district_he",
    "district_en",
    "population_approx",
    "source",
    "is_active",
}
LOCALITY_REQUIRED_COLUMNS = {
    "locality_code",
    "locality_name_he",
    "locality_name_en",
    "district_he",
    "district_en",
    "population_approx",
    "source",
}
RELEASE_FILES_REQUIRED_COLUMNS = {
    "path",
    "release_version",
    "schema_version",
    "sha256",
    "bytes",
    "rows",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_fieldnames(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle).fieldnames or [])


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def csv_row_count(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def relative_display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.name


def missing_required_columns(path: Path, required: set[str]) -> list[str]:
    fieldnames = set(csv_fieldnames(path))
    return sorted(required - fieldnames)


def contains_absolute_path(value: object) -> bool:
    if isinstance(value, str):
        return PurePosixPath(value).is_absolute() or PureWindowsPath(value).is_absolute()
    if isinstance(value, list):
        return any(contains_absolute_path(item) for item in value)
    if isinstance(value, dict):
        return any(
            contains_absolute_path(item) for item in [*value.keys(), *value.values()]
        )
    return False


def validate_release() -> list[str]:
    errors: list[str] = []
    header_validation_failed = False
    csv_inputs = [
        GEOGRAPHY_PATH,
        LOCALITY_CROSSWALK_PATH,
        RELEASE_FILES_PATH,
    ]
    csv_rows: dict[Path, list[dict[str, str]]] = {}
    for path in csv_inputs:
        try:
            csv_rows[path] = read_csv(path)
        except FileNotFoundError as exc:
            filename = Path(exc.filename) if exc.filename else path
            return [f"required release file is missing: {relative_display_path(filename)}"]
        except OSError as exc:
            return [f"failed to read {relative_display_path(path)}: {exc}"]

    geography_rows = csv_rows[GEOGRAPHY_PATH]
    locality_rows = csv_rows[LOCALITY_CROSSWALK_PATH]
    release_files = csv_rows[RELEASE_FILES_PATH]

    header_checks = [
        (GEOGRAPHY_PATH, GEOGRAPHY_REQUIRED_COLUMNS),
        (LOCALITY_CROSSWALK_PATH, LOCALITY_REQUIRED_COLUMNS),
        (RELEASE_FILES_PATH, RELEASE_FILES_REQUIRED_COLUMNS),
    ]
    for path, required_columns in header_checks:
        missing_columns = missing_required_columns(path, required_columns)
        if missing_columns:
            header_validation_failed = True
            errors.append(
                "missing required columns in "
                f"{relative_display_path(path)}: {', '.join(missing_columns)}"
            )

    if SOURCE_INVENTORY_PATH.exists():
        errors.append(
            "forbidden legacy file still present: "
            f"{relative_display_path(SOURCE_INVENTORY_PATH)}"
        )

    if header_validation_failed:
        return errors

    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return ["metadata/manifest.json is missing"]
    except json.JSONDecodeError:
        return ["metadata/manifest.json is not valid JSON"]
    except OSError as exc:
        return [f"failed to read metadata/manifest.json: {exc}"]

    geography_ids = {row["geography_id"] for row in geography_rows}
    if len(geography_ids) != len(geography_rows):
        errors.append("duplicate geography_id values found in geography_reference.csv")
    if any(not row["geography_id"].strip() for row in geography_rows):
        errors.append("geography_reference.csv contains blank geography_id fields")
    if any(row["geography_type"] not in VALID_GEOGRAPHY_TYPES for row in geography_rows):
        errors.append("geography_reference.csv contains invalid geography_type values")

    locality_codes = [row["locality_code"] for row in locality_rows]
    if len(locality_codes) != len(set(locality_codes)):
        errors.append("duplicate locality_code values found in locality_crosswalk.csv")
    if any(not row["locality_code"].strip() for row in locality_rows):
        errors.append("locality_crosswalk.csv contains blank locality_code fields")

    if contains_absolute_path(manifest):
        errors.append("metadata manifest contains internal absolute paths")

    try:
        quality_summary = manifest["data_quality_summary"]
        release_version = str(manifest["release_version"])
        schema_version = str(manifest["schema_version"])
        expected_geo_rows = quality_summary["geography_rows"]
        expected_crosswalk_rows = quality_summary["locality_crosswalk_rows"]
    except (KeyError, TypeError):
        errors.append("manifest.json is missing required release metadata fields")
        quality_summary = None
        release_version = None
        schema_version = None

    if quality_summary is None or release_version is None or schema_version is None:
        return errors

    if expected_geo_rows != len(geography_rows):
        errors.append("manifest geography row count does not match geography_reference.csv")
    if expected_crosswalk_rows != len(locality_rows):
        errors.append("manifest locality row count does not match locality_crosswalk.csv")

    expected_paths = {
        "data/current/geography_reference.csv",
        "data/current/locality_crosswalk.csv",
        f"data/releases/{release_version}/geography_reference.csv",
        f"data/releases/{release_version}/locality_crosswalk.csv",
    }
    actual_paths = {row["path"] for row in release_files}
    if expected_paths - actual_paths:
        errors.append("release_files.csv is missing one or more canonical file paths")
    if actual_paths - expected_paths:
        errors.append("release_files.csv contains unexpected legacy file paths")
    if any(contains_absolute_path(row["path"]) for row in release_files):
        errors.append("release_files.csv contains absolute paths")
    if len(actual_paths) != len(release_files):
        errors.append("release_files.csv contains duplicate path rows")

    for row in release_files:
        if row.get("release_version") != release_version:
            errors.append("release_files.csv contains inconsistent release_version values")
            break
    for row in release_files:
        if row.get("schema_version") != schema_version:
            errors.append("release_files.csv contains inconsistent schema_version values")
            break

    for legacy_path in [
        LEGACY_CURRENT_FACT_PATH,
        ROOT / "data" / "releases" / release_version / "rent_benchmarks.csv",
    ]:
        if legacy_path.exists():
            errors.append(f"forbidden legacy file still present: {relative_display_path(legacy_path)}")

    if errors:
        return errors

    for name in ["geography_reference.csv", "locality_crosswalk.csv"]:
        current_path = f"data/current/{name}"
        snapshot_path = f"data/releases/{release_version}/{name}"
        current_entry = next((row for row in release_files if row["path"] == current_path), None)
        snapshot_entry = next((row for row in release_files if row["path"] == snapshot_path), None)
        if current_entry and snapshot_entry and current_entry.get("sha256") != snapshot_entry.get(
            "sha256"
        ):
            errors.append(f"release snapshot does not match current file for {name}")

    for relative_path in sorted(expected_paths):
        actual_path = ROOT / relative_path
        release_entry = next((row for row in release_files if row["path"] == relative_path), None)
        if release_entry is None:
            errors.append(f"release_files.csv is missing metadata for {relative_path}")
            continue
        if not actual_path.exists():
            errors.append(f"missing file on disk: {relative_path}")
            continue

        expected_bytes = str(actual_path.stat().st_size)
        expected_rows = str(csv_row_count(actual_path))
        expected_sha = sha256(actual_path)
        if release_entry.get("bytes") != expected_bytes:
            errors.append(f"release_files.csv bytes mismatch for {relative_path}")
        if release_entry.get("rows") != expected_rows:
            errors.append(f"release_files.csv row count mismatch for {relative_path}")
        if release_entry.get("sha256") != expected_sha:
            errors.append(f"release_files.csv sha256 mismatch for {relative_path}")

    return errors


def build_summary() -> dict[str, object]:
    geography_rows = read_csv(GEOGRAPHY_PATH)
    locality_rows = read_csv(LOCALITY_CROSSWALK_PATH)
    return {
        "geography_rows": len(geography_rows),
        "locality_crosswalk_rows": len(locality_rows),
        "distinct_reference_sources": sorted(
            {row["source"] for row in geography_rows}.union(
                {row["source"] for row in locality_rows}
            )
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate public dataset release files.")
    parser.add_argument("--check", action="store_true", help="Exit non-zero on validation errors.")
    args = parser.parse_args()

    errors = validate_release()
    if errors:
        print("Release validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1 if args.check else 0

    print(json.dumps(build_summary(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
