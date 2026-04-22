from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path


ROOT = Path(os.getenv("ISRAEL_NADLAN_DATA_ROOT", Path(__file__).resolve().parent.parent))
CURRENT_DIR = ROOT / "data" / "current"
METADATA_DIR = ROOT / "metadata"
RELEASE_VERSION = "v0.2.0"
SCHEMA_VERSION = "2.1.0"
RELEASE_DATE = "2026-04-22"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_header(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle).fieldnames or [])


def release_snapshot_dir(release_version: str) -> Path:
    return ROOT / "data" / "releases" / release_version


def build_release_files(
    *, release_version: str = RELEASE_VERSION, schema_version: str = SCHEMA_VERSION
) -> list[dict[str, object]]:
    rows = []
    snapshot_dir = release_snapshot_dir(release_version)
    for base_dir in [CURRENT_DIR, snapshot_dir]:
        for name in ["rent_benchmarks.csv", "geography_reference.csv", "locality_crosswalk.csv"]:
            path = base_dir / name
            csv_rows = read_csv(path)
            rows.append(
                {
                    "release_version": release_version,
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": sha256(path),
                    "bytes": path.stat().st_size,
                    "rows": len(csv_rows),
                    "schema_version": schema_version,
                }
            )
    return rows


def build_data_dictionary() -> list[dict[str, object]]:
    descriptions = {
        "rent_benchmarks.csv": "Published benchmark observation field.",
        "geography_reference.csv": "Canonical geography dimension field.",
        "locality_crosswalk.csv": "Locality-only compatibility field.",
    }
    rows: list[dict[str, object]] = []
    for file_name in descriptions:
        path = CURRENT_DIR / file_name
        header = csv_header(path)
        for column_name in header:
            rows.append(
                {
                    "file_name": file_name,
                    "column_name": column_name,
                    "description": descriptions[file_name],
                }
            )
    return rows


def build_source_inventory() -> list[dict[str, object]]:
    return [
        {
            "source_id": "nadlan.gov.il",
            "display_name": "Israeli government real-estate portal",
            "homepage_url": "https://www.nadlan.gov.il/",
            "terms_url": "",
            "license_url": "",
            "access_method": "public_website",
            "public_status": "active",
            "attribution_required": "true",
        },
        {
            "source_id": "cbs_table49",
            "display_name": "CBS Table 4.9",
            "homepage_url": "https://www.cbs.gov.il/",
            "terms_url": "https://www.cbs.gov.il/en/Pages/Enduser-license.aspx",
            "license_url": "",
            "access_method": "direct_download",
            "public_status": "active",
            "attribution_required": "true",
        },
        {
            "source_id": "boi_hedonic",
            "display_name": "Bank of Israel hedonic source material",
            "homepage_url": "https://www.boi.org.il/",
            "terms_url": "https://www.boi.org.il/en/terms-of-use/",
            "license_url": "",
            "access_method": "public_pdf",
            "public_status": "active",
            "attribution_required": "true",
        },
        {
            "source_id": "data.gov.il",
            "display_name": "data.gov.il / CBS locality registry",
            "homepage_url": "https://data.gov.il/dataset/citiesandsettelments",
            "terms_url": "",
            "license_url": "",
            "access_method": "public_dataset",
            "public_status": "active",
            "attribution_required": "true",
        },
    ]


def build_manifest(
    release_files: list[dict[str, object]],
    *,
    release_version: str = RELEASE_VERSION,
    schema_version: str = SCHEMA_VERSION,
    release_date: str = RELEASE_DATE,
) -> dict[str, object]:
    fact_rows = read_csv(CURRENT_DIR / "rent_benchmarks.csv")
    geo_rows = read_csv(CURRENT_DIR / "geography_reference.csv")
    cross_rows = read_csv(CURRENT_DIR / "locality_crosswalk.csv")
    return {
        "dataset_name": "israel-nadlan-data",
        "release_version": release_version,
        "release_date": release_date,
        "schema_version": schema_version,
        "data_quality_summary": {
            "fact_rows": len(fact_rows),
            "geography_rows": len(geo_rows),
            "locality_crosswalk_rows": len(cross_rows),
        },
        "files": release_files,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build public release metadata files.")
    parser.add_argument("--release-version", default=RELEASE_VERSION)
    parser.add_argument("--schema-version", default=SCHEMA_VERSION)
    parser.add_argument("--release-date", default=RELEASE_DATE)
    args = parser.parse_args(argv)

    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    release_files = build_release_files(
        release_version=args.release_version,
        schema_version=args.schema_version,
    )
    write_csv(
        METADATA_DIR / "release_files.csv",
        ["release_version", "path", "sha256", "bytes", "rows", "schema_version"],
        release_files,
    )
    write_csv(
        METADATA_DIR / "data_dictionary.csv",
        ["file_name", "column_name", "description"],
        build_data_dictionary(),
    )
    write_csv(
        METADATA_DIR / "source_inventory.csv",
        [
            "source_id",
            "display_name",
            "homepage_url",
            "terms_url",
            "license_url",
            "access_method",
            "public_status",
            "attribution_required",
        ],
        build_source_inventory(),
    )
    manifest = build_manifest(
        release_files,
        release_version=args.release_version,
        schema_version=args.schema_version,
        release_date=args.release_date,
    )
    (METADATA_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
