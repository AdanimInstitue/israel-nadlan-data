from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CURRENT_DIR = ROOT / "data" / "current"
METADATA_DIR = ROOT / "metadata"
RELEASE_VERSION = "v0.2.0"
SCHEMA_VERSION = "2.1.0"


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


def build_release_files() -> list[dict[str, object]]:
    rows = []
    for name in ["rent_benchmarks.csv", "geography_reference.csv", "locality_crosswalk.csv"]:
        path = CURRENT_DIR / name
        csv_rows = read_csv(path)
        rows.append(
            {
                "release_version": RELEASE_VERSION,
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
                "rows": len(csv_rows),
                "schema_version": SCHEMA_VERSION,
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
        header = list(read_csv(path)[0].keys())
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


def build_manifest(release_files: list[dict[str, object]]) -> dict[str, object]:
    fact_rows = read_csv(CURRENT_DIR / "rent_benchmarks.csv")
    geo_rows = read_csv(CURRENT_DIR / "geography_reference.csv")
    cross_rows = read_csv(CURRENT_DIR / "locality_crosswalk.csv")
    return {
        "dataset_name": "israel-nadlan-data",
        "release_version": RELEASE_VERSION,
        "release_date": "2026-04-22",
        "schema_version": SCHEMA_VERSION,
        "data_quality_summary": {
            "fact_rows": len(fact_rows),
            "geography_rows": len(geo_rows),
            "locality_crosswalk_rows": len(cross_rows),
        },
        "files": release_files,
    }


def main() -> int:
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    release_files = build_release_files()
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
    manifest = build_manifest(release_files)
    (METADATA_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
