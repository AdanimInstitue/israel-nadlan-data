from __future__ import annotations

import csv
import json
import runpy
from pathlib import Path

from scripts import build_release_metadata as brm
from scripts import validate_release as vr


GEOGRAPHY_HEADER = [
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
]
LOCALITY_HEADER = [
    "locality_code",
    "locality_name_he",
    "locality_name_en",
    "district_he",
    "district_en",
    "population_approx",
    "source",
]


def write_fixture_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def install_fixture_repo(tmp_path: Path, monkeypatch) -> None:
    geo = tmp_path / "data" / "current" / "geography_reference.csv"
    cross = tmp_path / "data" / "current" / "locality_crosswalk.csv"
    release_geo = tmp_path / "data" / "releases" / "v0.2.0" / "geography_reference.csv"
    release_cross = tmp_path / "data" / "releases" / "v0.2.0" / "locality_crosswalk.csv"
    manifest = tmp_path / "metadata" / "manifest.json"
    release_files = tmp_path / "metadata" / "release_files.csv"
    source_inventory = tmp_path / "metadata" / "source_inventory.csv"
    legacy_current_fact = tmp_path / "data" / "current" / "rent_benchmarks.csv"

    write_fixture_csv(
        geo,
        GEOGRAPHY_HEADER,
        [
            {
                "geography_id": "DIST_CENTER",
                "geography_type": "district",
                "locality_code": "",
                "district_code": "CENTER",
                "geography_name_he": "מחוז המרכז",
                "geography_name_en": "Center District",
                "district_he": "מחוז המרכז",
                "district_en": "Center",
                "population_approx": "",
                "source": "cbs_table49",
                "is_active": "true",
            },
            {
                "geography_id": "1000",
                "geography_type": "locality",
                "locality_code": "1000",
                "district_code": "CENTER",
                "geography_name_he": "מבשרת ציון",
                "geography_name_en": "MEVASSERET ZIYYON",
                "district_he": "מחוז המרכז",
                "district_en": "Center",
                "population_approx": "12000",
                "source": "cbs_table49",
                "is_active": "true",
            },
        ],
    )
    write_fixture_csv(
        cross,
        LOCALITY_HEADER,
        [
            {
                "locality_code": "1000",
                "locality_name_he": "מבשרת ציון",
                "locality_name_en": "MEVASSERET ZIYYON",
                "district_he": "מחוז המרכז",
                "district_en": "Center",
                "population_approx": "12000",
                "source": "data.gov.il",
            }
        ],
    )
    write_fixture_csv(
        release_geo,
        GEOGRAPHY_HEADER,
        [
            {
                "geography_id": "DIST_CENTER",
                "geography_type": "district",
                "locality_code": "",
                "district_code": "CENTER",
                "geography_name_he": "מחוז המרכז",
                "geography_name_en": "Center District",
                "district_he": "מחוז המרכז",
                "district_en": "Center",
                "population_approx": "",
                "source": "cbs_table49",
                "is_active": "true",
            },
            {
                "geography_id": "1000",
                "geography_type": "locality",
                "locality_code": "1000",
                "district_code": "CENTER",
                "geography_name_he": "מבשרת ציון",
                "geography_name_en": "MEVASSERET ZIYYON",
                "district_he": "מחוז המרכז",
                "district_en": "Center",
                "population_approx": "12000",
                "source": "cbs_table49",
                "is_active": "true",
            },
        ],
    )
    write_fixture_csv(
        release_cross,
        LOCALITY_HEADER,
        [
            {
                "locality_code": "1000",
                "locality_name_he": "מבשרת ציון",
                "locality_name_en": "MEVASSERET ZIYYON",
                "district_he": "מחוז המרכז",
                "district_en": "Center",
                "population_approx": "12000",
                "source": "data.gov.il",
            }
        ],
    )
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(
            {
                "dataset_name": "israel-nadlan-data",
                "release_version": "v0.2.0",
                "release_date": "2026-04-22",
                "schema_version": "2.1.0",
                "data_quality_summary": {
                    "geography_rows": 2,
                    "locality_crosswalk_rows": 1,
                },
            }
        ),
        encoding="utf-8",
    )
    release_file_rows = []
    for path in [geo, cross, release_geo, release_cross]:
        with path.open(encoding="utf-8", newline="") as handle:
            rows = len(list(csv.DictReader(handle)))
        release_file_rows.append(
            {
                "release_version": "v0.2.0",
                "path": path.relative_to(tmp_path).as_posix(),
                "sha256": brm.sha256(path),
                "bytes": path.stat().st_size,
                "rows": rows,
                "schema_version": "2.1.0",
            }
        )
    write_fixture_csv(
        release_files,
        ["release_version", "path", "sha256", "bytes", "rows", "schema_version"],
        release_file_rows,
    )

    monkeypatch.setattr(vr, "ROOT", tmp_path)
    monkeypatch.setattr(vr, "GEOGRAPHY_PATH", geo)
    monkeypatch.setattr(vr, "LOCALITY_CROSSWALK_PATH", cross)
    monkeypatch.setattr(vr, "MANIFEST_PATH", manifest)
    monkeypatch.setattr(vr, "RELEASE_FILES_PATH", release_files)
    monkeypatch.setattr(vr, "SOURCE_INVENTORY_PATH", source_inventory)
    monkeypatch.setattr(vr, "LEGACY_CURRENT_FACT_PATH", legacy_current_fact)
    monkeypatch.setattr(brm, "ROOT", tmp_path)
    monkeypatch.setattr(brm, "CURRENT_DIR", tmp_path / "data" / "current")
    monkeypatch.setattr(brm, "METADATA_DIR", tmp_path / "metadata")


def rewrite_release_file_metadata(path: Path, rows: list[dict[str, object]]) -> None:
    write_fixture_csv(
        path,
        ["release_version", "path", "sha256", "bytes", "rows", "schema_version"],
        rows,
    )


def test_release_validation_passes(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    assert vr.validate_release() == []


def test_release_validation_reports_path_and_count_errors(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    vr.MANIFEST_PATH.write_text(
        json.dumps(
            {
                "dataset_name": "israel-nadlan-data",
                "release_version": "v0.2.0",
                "data_quality_summary": {
                    "geography_rows": 3,
                    "locality_crosswalk_rows": 2,
                },
                "bad_path": "/abs/path",
            }
        ),
        encoding="utf-8",
    )
    errors = vr.validate_release()
    assert any("internal absolute paths" in error for error in errors)
    assert any("geography row count" in error for error in errors)
    assert any("locality row count" in error for error in errors)


def test_release_validation_reports_absolute_release_file_paths(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    write_fixture_csv(
        vr.RELEASE_FILES_PATH,
        ["release_version", "path", "sha256", "bytes", "rows", "schema_version"],
        [
            {
                "release_version": "v0.2.0",
                "path": "data/current/geography_reference.csv",
                "sha256": "same-geo",
                "bytes": "1",
                "rows": "1",
                "schema_version": "2.1.0",
            },
            {
                "release_version": "v0.2.0",
                "path": "data/current/locality_crosswalk.csv",
                "sha256": "same-cross",
                "bytes": "1",
                "rows": "1",
                "schema_version": "2.1.0",
            },
            {
                "release_version": "v0.2.0",
                "path": "data/releases/v0.2.0/geography_reference.csv",
                "sha256": "same-geo",
                "bytes": "1",
                "rows": "1",
                "schema_version": "2.1.0",
            },
            {
                "release_version": "v0.2.0",
                "path": "data/releases/v0.2.0/locality_crosswalk.csv",
                "sha256": "same-cross",
                "bytes": "1",
                "rows": "1",
                "schema_version": "2.1.0",
            },
            {
                "release_version": "v0.2.0",
                "path": "C:\\temp\\internal.csv",
                "sha256": "other",
                "bytes": "1",
                "rows": "1",
                "schema_version": "2.1.0",
            },
        ],
    )

    errors = vr.validate_release()

    assert "release_files.csv contains absolute paths" in errors


def test_release_validation_reports_missing_quality_summary(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    vr.MANIFEST_PATH.write_text(json.dumps({}), encoding="utf-8")

    errors = vr.validate_release()

    assert "manifest.json is missing required release metadata fields" in errors


def test_release_validation_reports_missing_manifest_file(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    vr.MANIFEST_PATH.unlink()

    assert vr.validate_release() == ["metadata/manifest.json is missing"]


def test_release_validation_reports_invalid_manifest_json(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    vr.MANIFEST_PATH.write_text("{", encoding="utf-8")

    assert vr.validate_release() == ["metadata/manifest.json is not valid JSON"]


def test_release_validation_reports_missing_file_without_absolute_path(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    vr.GEOGRAPHY_PATH.unlink()

    assert vr.validate_release() == [
        "required release file is missing: data/current/geography_reference.csv"
    ]


def test_relative_display_path_returns_basename_for_out_of_tree_path() -> None:
    assert vr.relative_display_path(Path("/tmp/external.csv")) == "external.csv"


def test_contains_absolute_path_handles_nested_structures() -> None:
    assert vr.contains_absolute_path(
        {"files": [{"path": "C:\\temp\\internal.csv"}], "extra": ["relative/path.csv"]}
    )
    assert vr.contains_absolute_path({"C:\\temp\\internal.csv": "relative/path.csv"})
    assert not vr.contains_absolute_path({"files": [{"path": "data/current/geography_reference.csv"}]})


def test_release_validation_reports_dataset_shape_errors(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    write_fixture_csv(
        vr.GEOGRAPHY_PATH,
        GEOGRAPHY_HEADER,
        [
            {
                "geography_id": "dup",
                "geography_type": "bad",
                "locality_code": "",
                "district_code": "CENTER",
                "geography_name_he": "מחוז המרכז",
                "geography_name_en": "Center District",
                "district_he": "מחוז המרכז",
                "district_en": "Center",
                "population_approx": "",
                "source": "cbs_table49",
                "is_active": "true",
            },
            {
                "geography_id": "dup",
                "geography_type": "locality",
                "locality_code": "1000",
                "district_code": "CENTER",
                "geography_name_he": "מבשרת ציון",
                "geography_name_en": "MEVASSERET ZIYYON",
                "district_he": "מחוז המרכז",
                "district_en": "Center",
                "population_approx": "12000",
                "source": "cbs_table49",
                "is_active": "true",
            },
        ],
    )
    write_fixture_csv(
        vr.LOCALITY_CROSSWALK_PATH,
        LOCALITY_HEADER,
        [
            {
                "locality_code": "",
                "locality_name_he": "מבשרת ציון",
                "locality_name_en": "MEVASSERET ZIYYON",
                "district_he": "מחוז המרכז",
                "district_en": "Center",
                "population_approx": "12000",
                "source": "data.gov.il",
            },
            {
                "locality_code": "",
                "locality_name_he": "מבשרת ציון",
                "locality_name_en": "MEVASSERET ZIYYON",
                "district_he": "מחוז המרכז",
                "district_en": "Center",
                "population_approx": "12000",
                "source": "data.gov.il",
            },
        ],
    )

    errors = vr.validate_release()

    assert "duplicate geography_id values found in geography_reference.csv" in errors
    assert "geography_reference.csv contains invalid geography_type values" in errors
    assert "duplicate locality_code values found in locality_crosswalk.csv" in errors
    assert "locality_crosswalk.csv contains blank locality_code fields" in errors


def test_release_validation_reports_blank_geography_id(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    geography_rows = [
        {
            "geography_id": "",
            "geography_type": "district",
            "locality_code": "",
            "district_code": "CENTER",
            "geography_name_he": "מחוז המרכז",
            "geography_name_en": "Center District",
            "district_he": "מחוז המרכז",
            "district_en": "Center",
            "population_approx": "",
            "source": "cbs_table49",
            "is_active": "true",
        },
        {
            "geography_id": "1000",
            "geography_type": "locality",
            "locality_code": "1000",
            "district_code": "CENTER",
            "geography_name_he": "מבשרת ציון",
            "geography_name_en": "MEVASSERET ZIYYON",
            "district_he": "מחוז המרכז",
            "district_en": "Center",
            "population_approx": "12000",
            "source": "cbs_table49",
            "is_active": "true",
        },
    ]
    write_fixture_csv(vr.GEOGRAPHY_PATH, GEOGRAPHY_HEADER, geography_rows)
    write_fixture_csv(
        tmp_path / "data" / "releases" / "v0.2.0" / "geography_reference.csv",
        GEOGRAPHY_HEADER,
        geography_rows,
    )

    with vr.RELEASE_FILES_PATH.open(encoding="utf-8", newline="") as handle:
        release_files = list(csv.DictReader(handle))
    for row in release_files:
        if row["path"] in {
            "data/current/geography_reference.csv",
            "data/releases/v0.2.0/geography_reference.csv",
        }:
            file_path = tmp_path / row["path"]
            row["sha256"] = brm.sha256(file_path)
            row["bytes"] = str(file_path.stat().st_size)
            with file_path.open(encoding="utf-8", newline="") as handle:
                row["rows"] = str(sum(1 for _ in csv.DictReader(handle)))
    rewrite_release_file_metadata(vr.RELEASE_FILES_PATH, release_files)

    errors = vr.validate_release()

    assert "geography_reference.csv contains blank geography_id fields" in errors


def test_release_validation_reports_missing_canonical_paths(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    write_fixture_csv(
        vr.RELEASE_FILES_PATH,
        ["release_version", "path", "sha256", "bytes", "rows", "schema_version"],
        [
            {
                "release_version": "v0.2.0",
                "path": "data/current/geography_reference.csv",
                "sha256": "same-geo",
                "bytes": "1",
                "rows": "1",
                "schema_version": "2.1.0",
            }
        ],
    )

    errors = vr.validate_release()

    assert "release_files.csv is missing one or more canonical file paths" in errors


def test_release_validation_reports_duplicate_release_file_paths(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    rows = list(csv.DictReader(vr.RELEASE_FILES_PATH.open(encoding="utf-8", newline="")))
    rows.append(dict(rows[0]))
    write_fixture_csv(
        vr.RELEASE_FILES_PATH,
        ["release_version", "path", "sha256", "bytes", "rows", "schema_version"],
        rows,
    )

    errors = vr.validate_release()

    assert "release_files.csv contains duplicate path rows" in errors


def test_release_validation_reports_release_file_read_errors(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    original_read_csv = vr.read_csv

    def raise_for_release_files(path: Path) -> list[dict[str, str]]:
        if path == vr.RELEASE_FILES_PATH:
            raise OSError("release files unavailable")
        return original_read_csv(path)

    monkeypatch.setattr(vr, "read_csv", raise_for_release_files)

    assert vr.validate_release() == ["failed to read release files: release files unavailable"]


def test_release_validation_reports_manifest_read_errors(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)

    class BrokenManifest:
        def read_text(self, encoding: str = "utf-8") -> str:
            raise OSError("manifest unavailable")

    monkeypatch.setattr(vr, "MANIFEST_PATH", BrokenManifest())

    assert vr.validate_release() == ["failed to read metadata/manifest.json: manifest unavailable"]


def test_release_validation_reports_missing_snapshot_file_on_disk(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    (tmp_path / "data" / "releases" / "v0.2.0" / "geography_reference.csv").unlink()

    errors = vr.validate_release()

    assert "missing file on disk: data/releases/v0.2.0/geography_reference.csv" in errors


def test_release_validation_reports_missing_required_columns(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    write_fixture_csv(vr.GEOGRAPHY_PATH, ["geography_id"], [{"geography_id": "1000"}])

    errors = vr.validate_release()

    assert (
        "missing required columns in data/current/geography_reference.csv: district_code, district_en, "
        "district_he, geography_name_en, geography_name_he, geography_type, is_active, "
        "locality_code, population_approx, source"
    ) in errors


def test_release_validation_reports_forbidden_legacy_files(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    vr.SOURCE_INVENTORY_PATH.write_text("source_id\nlegacy\n", encoding="utf-8")
    vr.LEGACY_CURRENT_FACT_PATH.write_text("legacy\n", encoding="utf-8")
    (tmp_path / "data" / "releases" / "v0.2.0" / "rent_benchmarks.csv").write_text(
        "legacy\n", encoding="utf-8"
    )

    errors = vr.validate_release()

    assert "forbidden legacy file still present: metadata/source_inventory.csv" in errors
    assert "forbidden legacy file still present: data/current/rent_benchmarks.csv" in errors
    assert "forbidden legacy file still present: data/releases/v0.2.0/rent_benchmarks.csv" in errors


def test_build_summary_reads_fixture_contents(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)

    summary = vr.build_summary()

    assert summary == {
        "geography_rows": 2,
        "locality_crosswalk_rows": 1,
        "distinct_reference_sources": ["cbs_table49", "data.gov.il"],
    }


def test_main_returns_zero_without_check_on_validation_errors(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    vr.MANIFEST_PATH.write_text(json.dumps({"bad_path": "/abs/path"}), encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["validate_release.py"])

    assert vr.main() == 0
    assert "Release validation failed:" in capsys.readouterr().out


def test_main_returns_zero_for_clean_fixture(tmp_path: Path, monkeypatch, capsys) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    monkeypatch.setattr("sys.argv", ["validate_release.py", "--check"])
    assert vr.main() == 0
    assert '"geography_rows": 2' in capsys.readouterr().out


def test_build_release_metadata_main_writes_expected_outputs(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)

    assert brm.main([]) == 0

    release_files = list(csv.DictReader((tmp_path / "metadata" / "release_files.csv").open()))
    assert [row["path"] for row in release_files] == [
        "data/current/geography_reference.csv",
        "data/current/locality_crosswalk.csv",
        "data/releases/v0.2.0/geography_reference.csv",
        "data/releases/v0.2.0/locality_crosswalk.csv",
    ]

    assert not (tmp_path / "metadata" / "source_inventory.csv").exists()

    manifest = json.loads((tmp_path / "metadata" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["files"][0]["path"] == "data/current/geography_reference.csv"
    assert manifest["data_quality_summary"]["locality_crosswalk_rows"] == 1


def test_build_release_files_and_manifest_helpers(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)

    release_files = brm.build_release_files()
    manifest = brm.build_manifest(release_files)

    assert [row["path"] for row in release_files] == [
        "data/current/geography_reference.csv",
        "data/current/locality_crosswalk.csv",
        "data/releases/v0.2.0/geography_reference.csv",
        "data/releases/v0.2.0/locality_crosswalk.csv",
    ]
    assert all(row["release_version"] == brm.RELEASE_VERSION for row in release_files)
    assert manifest["release_version"] == brm.RELEASE_VERSION
    assert manifest["schema_version"] == brm.SCHEMA_VERSION
    assert manifest["data_quality_summary"]["geography_rows"] == 2


def test_release_validation_reports_snapshot_mismatch(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    write_fixture_csv(
        vr.RELEASE_FILES_PATH,
        ["release_version", "path", "sha256", "bytes", "rows", "schema_version"],
        [
            {
                "release_version": "v0.2.0",
                "path": "data/current/geography_reference.csv",
                "sha256": "same-geo",
                "bytes": "1",
                "rows": "1",
                "schema_version": "2.1.0",
            },
            {
                "release_version": "v0.2.0",
                "path": "data/current/locality_crosswalk.csv",
                "sha256": "same-cross",
                "bytes": "1",
                "rows": "1",
                "schema_version": "2.1.0",
            },
            {
                "release_version": "v0.2.0",
                "path": "data/releases/v0.2.0/geography_reference.csv",
                "sha256": "other-geo",
                "bytes": "1",
                "rows": "1",
                "schema_version": "2.1.0",
            },
            {
                "release_version": "v0.2.0",
                "path": "data/releases/v0.2.0/locality_crosswalk.csv",
                "sha256": "same-cross",
                "bytes": "1",
                "rows": "1",
                "schema_version": "2.1.0",
            },
        ],
    )

    errors = vr.validate_release()

    assert "release snapshot does not match current file for geography_reference.csv" in errors


def test_build_data_dictionary_handles_header_only_csv(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    (brm.CURRENT_DIR / "geography_reference.csv").write_text(
        "geography_id\n", encoding="utf-8"
    )

    data_dictionary = brm.build_data_dictionary()

    assert {
        row["column_name"] for row in data_dictionary if row["file_name"] == "geography_reference.csv"
    } == {"geography_id"}


def test_sha256_and_write_csv_helpers(tmp_path: Path) -> None:
    sample = tmp_path / "sample.csv"
    brm.write_csv(sample, ["col"], [{"col": "1"}])

    assert brm.read_csv(sample) == [{"col": "1"}]
    assert (
        brm.sha256(sample)
        == "6ec84fc3052b7304e7d446acecbac55fac0192a9f9386e40f10aaa7e00edcf1e"
    )


def test_build_release_metadata_module_main_raises_system_exit(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    monkeypatch.setenv("ISRAEL_NADLAN_DATA_ROOT", str(tmp_path))
    monkeypatch.setattr("sys.argv", ["build_release_metadata.py"])

    try:
        runpy.run_module("scripts.build_release_metadata", run_name="__main__")
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("expected SystemExit")


def test_validate_release_module_main_raises_system_exit_when_run_as_script(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    monkeypatch.setenv("ISRAEL_NADLAN_DATA_ROOT", str(tmp_path))
    monkeypatch.setattr("sys.argv", ["validate_release.py"])
    try:
        runpy.run_module("scripts.validate_release", run_name="__main__")
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("expected SystemExit")
