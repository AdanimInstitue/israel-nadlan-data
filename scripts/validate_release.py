from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath


ROOT = Path(os.getenv("ISRAEL_NADLAN_DATA_ROOT", Path(__file__).resolve().parent.parent))
FACT_PATH = ROOT / "data" / "current" / "rent_benchmarks.csv"
GEOGRAPHY_PATH = ROOT / "data" / "current" / "geography_reference.csv"
LOCALITY_CROSSWALK_PATH = ROOT / "data" / "current" / "locality_crosswalk.csv"
MANIFEST_PATH = ROOT / "metadata" / "manifest.json"
RELEASE_FILES_PATH = ROOT / "metadata" / "release_files.csv"

VALID_GEOGRAPHY_TYPES = {"locality", "district"}
VALID_METRIC_TYPES = {"average_rent_published", "hedonic_rent_estimate"}
VALID_PERIOD_TYPES = {"annual", "quarterly"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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
    try:
        fact_rows = read_csv(FACT_PATH)
        geography_rows = read_csv(GEOGRAPHY_PATH)
        locality_rows = read_csv(LOCALITY_CROSSWALK_PATH)
        release_files = read_csv(RELEASE_FILES_PATH)
    except FileNotFoundError as exc:
        return [f"required release file is missing: {exc.filename}"]
    except OSError as exc:
        return [f"failed to read release files: {exc}"]

    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return ["metadata/manifest.json is missing"]
    except json.JSONDecodeError:
        return ["metadata/manifest.json is not valid JSON"]
    except OSError as exc:
        return [f"failed to read metadata/manifest.json: {exc}"]

    geography_ids = {row["geography_id"] for row in geography_rows}
    record_ids = [row["record_id"] for row in fact_rows]

    if len(record_ids) != len(set(record_ids)):
        errors.append("duplicate record_id values found in rent_benchmarks.csv")
    if any(not row["value_nis"] for row in fact_rows):
        errors.append("rent_benchmarks.csv contains blank value_nis fields")
    if any(row["geography_type"] not in VALID_GEOGRAPHY_TYPES for row in fact_rows):
        errors.append("rent_benchmarks.csv contains invalid geography_type values")
    if any(row["metric_type"] not in VALID_METRIC_TYPES for row in fact_rows):
        errors.append("rent_benchmarks.csv contains invalid metric_type values")
    if any(row["period_type"] not in VALID_PERIOD_TYPES for row in fact_rows):
        errors.append("rent_benchmarks.csv contains invalid period_type values")

    missing_geographies = sorted(
        {row["geography_id"] for row in fact_rows if row["geography_id"] not in geography_ids}
    )
    if missing_geographies:
        errors.append(
            f"fact rows missing geography_reference join keys: {', '.join(missing_geographies[:10])}"
        )

    if contains_absolute_path(manifest):
        errors.append("metadata manifest contains internal absolute paths")

    try:
        quality_summary = manifest["data_quality_summary"]
        expected_fact_rows = quality_summary["fact_rows"]
        expected_geo_rows = quality_summary["geography_rows"]
        expected_crosswalk_rows = quality_summary["locality_crosswalk_rows"]
    except (KeyError, TypeError):
        errors.append("manifest.json is missing required data_quality_summary fields")
        quality_summary = None

    if quality_summary is None:
        return errors

    if expected_fact_rows != len(fact_rows):
        errors.append("manifest fact row count does not match rent_benchmarks.csv")
    if expected_geo_rows != len(geography_rows):
        errors.append("manifest geography row count does not match geography_reference.csv")
    if expected_crosswalk_rows != len(locality_rows):
        errors.append("manifest locality row count does not match locality_crosswalk.csv")

    expected_paths = {
        "data/current/rent_benchmarks.csv",
        "data/current/geography_reference.csv",
        "data/current/locality_crosswalk.csv",
    }
    actual_paths = {row["path"] for row in release_files}
    if expected_paths - actual_paths:
        errors.append("release_files.csv is missing one or more canonical file paths")
    if any(contains_absolute_path(row["path"]) for row in release_files):
        errors.append("release_files.csv contains absolute paths")

    return errors


def build_summary() -> dict[str, object]:
    fact_rows = read_csv(FACT_PATH)
    geography_rows = read_csv(GEOGRAPHY_PATH)
    return {
        "fact_rows": len(fact_rows),
        "geography_rows": len(geography_rows),
        "distinct_fact_sources": sorted({row["source_id"] for row in fact_rows}),
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
