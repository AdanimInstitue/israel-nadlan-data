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
PUBLISHED_FILES = ["geography_reference.csv", "locality_crosswalk.csv"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def csv_header(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle).fieldnames or [])


def csv_row_count(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def release_snapshot_dir(release_version: str) -> Path:
    return ROOT / "data" / "releases" / release_version


def build_release_files(
    *, release_version: str = RELEASE_VERSION, schema_version: str = SCHEMA_VERSION
) -> list[dict[str, object]]:
    rows = []
    snapshot_dir = release_snapshot_dir(release_version)
    for base_dir in [CURRENT_DIR, snapshot_dir]:
        for name in PUBLISHED_FILES:
            path = base_dir / name
            rows.append(
                {
                    "release_version": release_version,
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": sha256(path),
                    "bytes": path.stat().st_size,
                    "rows": csv_row_count(path),
                    "schema_version": schema_version,
                }
            )
    return rows


def build_data_dictionary() -> list[dict[str, object]]:
    descriptions = {
        "geography_reference.csv": "Canonical geography reference field.",
        "locality_crosswalk.csv": "Locality context and compatibility field.",
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


def build_manifest(
    release_files: list[dict[str, object]],
    *,
    release_version: str = RELEASE_VERSION,
    schema_version: str = SCHEMA_VERSION,
    release_date: str = RELEASE_DATE,
) -> dict[str, object]:
    current_row_counts = {
        Path(str(row["path"])).name: int(row["rows"])
        for row in release_files
        if str(row["path"]).startswith("data/current/")
    }
    return {
        "dataset_name": "israel-nadlan-data",
        "release_version": release_version,
        "release_date": release_date,
        "schema_version": schema_version,
        "data_quality_summary": {
            "geography_rows": current_row_counts["geography_reference.csv"],
            "locality_crosswalk_rows": current_row_counts["locality_crosswalk.csv"],
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
