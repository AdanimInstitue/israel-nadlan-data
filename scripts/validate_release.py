from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FACT_PATH = ROOT / "rent_benchmarks.csv"
GEOGRAPHY_PATH = ROOT / "geography_reference.csv"
LOCALITY_CROSSWALK_PATH = ROOT / "locality_crosswalk.csv"
MANIFEST_PATH = ROOT / "manifest.json"

VALID_GEOGRAPHY_TYPES = {"locality", "district"}
VALID_METRIC_TYPES = {"average_rent_published", "hedonic_rent_estimate"}
VALID_PERIOD_TYPES = {"annual", "quarterly"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def validate_release() -> list[str]:
    fact_rows = read_csv(FACT_PATH)
    geography_rows = read_csv(GEOGRAPHY_PATH)
    locality_rows = read_csv(LOCALITY_CROSSWALK_PATH)
    manifest = read_manifest()

    errors: list[str] = []
    geography_ids = {row["geography_id"] for row in geography_rows}
    record_ids = [row["record_id"] for row in fact_rows]

    if len(record_ids) != len(set(record_ids)):
        errors.append("duplicate record_id values found in rent_benchmarks.csv")
    if any(not row["value_nis"] for row in fact_rows):
        errors.append("rent_benchmarks.csv contains blank value_nis fields")

    bad_geography_types = sorted(
        {row["geography_type"] for row in fact_rows if row["geography_type"] not in VALID_GEOGRAPHY_TYPES}
    )
    if bad_geography_types:
        errors.append(f"invalid geography_type values: {', '.join(bad_geography_types)}")

    bad_metric_types = sorted(
        {row["metric_type"] for row in fact_rows if row["metric_type"] not in VALID_METRIC_TYPES}
    )
    if bad_metric_types:
        errors.append(f"invalid metric_type values: {', '.join(bad_metric_types)}")

    bad_period_types = sorted(
        {row["period_type"] for row in fact_rows if row["period_type"] not in VALID_PERIOD_TYPES}
    )
    if bad_period_types:
        errors.append(f"invalid period_type values: {', '.join(bad_period_types)}")

    missing_geographies = sorted({row["geography_id"] for row in fact_rows if row["geography_id"] not in geography_ids})
    if missing_geographies:
        errors.append(f"fact rows missing geography_reference join keys: {', '.join(missing_geographies[:10])}")

    if "/Users/" in json.dumps(manifest, ensure_ascii=False):
        errors.append("manifest.json contains internal absolute paths")

    expected_fact_rows = manifest.get("data_quality_summary", {}).get("fact_rows")
    if expected_fact_rows != len(fact_rows):
        errors.append("manifest data_quality_summary.fact_rows does not match rent_benchmarks.csv")

    expected_geo_rows = manifest.get("data_quality_summary", {}).get("geography_rows")
    if expected_geo_rows != len(geography_rows):
        errors.append("manifest data_quality_summary.geography_rows does not match geography_reference.csv")

    locality_crosswalk_rows = manifest.get("files", {}).get("locality_crosswalk.csv", {}).get("rows")
    if locality_crosswalk_rows != len(locality_rows):
        errors.append("manifest locality_crosswalk row count does not match locality_crosswalk.csv")

    fact_distinct_by_type = Counter(row["geography_type"] for row in fact_rows)
    manifest_distinct_by_type = manifest.get("data_quality_summary", {}).get("distinct_geographies_by_type", {})
    for geography_type in VALID_GEOGRAPHY_TYPES:
        expected = manifest_distinct_by_type.get(geography_type)
        actual = len({row["geography_id"] for row in fact_rows if row["geography_type"] == geography_type})
        if expected != actual:
            errors.append(
                f"manifest distinct_geographies_by_type[{geography_type!r}]={expected} does not match actual {actual}"
            )

    return errors


def build_summary() -> dict[str, object]:
    fact_rows = read_csv(FACT_PATH)
    geography_rows = read_csv(GEOGRAPHY_PATH)
    return {
        "fact_rows": len(fact_rows),
        "geography_rows": len(geography_rows),
        "distinct_sources": sorted({row["source_id"] for row in fact_rows}),
        "distinct_periods": sorted({row["period_label"] for row in fact_rows}),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate public release files in the data repo.")
    parser.add_argument("--check", action="store_true", help="Exit non-zero if validation errors exist.")
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
