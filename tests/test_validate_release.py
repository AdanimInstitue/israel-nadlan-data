from __future__ import annotations

import csv
import json
import runpy
from pathlib import Path

from scripts import build_release_metadata as brm
from scripts import validate_release as vr


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def install_fixture_repo(tmp_path: Path, monkeypatch) -> None:
    fact = tmp_path / "data" / "current" / "rent_benchmarks.csv"
    geo = tmp_path / "data" / "current" / "geography_reference.csv"
    cross = tmp_path / "data" / "current" / "locality_crosswalk.csv"
    release_fact = tmp_path / "data" / "releases" / "v0.2.0" / "rent_benchmarks.csv"
    release_geo = tmp_path / "data" / "releases" / "v0.2.0" / "geography_reference.csv"
    release_cross = tmp_path / "data" / "releases" / "v0.2.0" / "locality_crosswalk.csv"
    manifest = tmp_path / "metadata" / "manifest.json"
    release_files = tmp_path / "metadata" / "release_files.csv"

    write_csv(
        fact,
        ["record_id", "geography_id", "geography_type", "metric_type", "value_nis", "period_type", "source_id"],
        [
            {
                "record_id": "r1",
                "geography_id": "1000",
                "geography_type": "locality",
                "metric_type": "average_rent_published",
                "value_nis": "5000",
                "period_type": "quarterly",
                "source_id": "nadlan.gov.il",
            }
        ],
    )
    write_csv(
        geo,
        ["geography_id"],
        [{"geography_id": "1000"}],
    )
    write_csv(
        cross,
        ["locality_code"],
        [{"locality_code": "1000"}],
    )
    write_csv(
        release_fact,
        ["record_id", "geography_id", "geography_type", "metric_type", "value_nis", "period_type", "source_id"],
        [
            {
                "record_id": "r1",
                "geography_id": "1000",
                "geography_type": "locality",
                "metric_type": "average_rent_published",
                "value_nis": "5000",
                "period_type": "quarterly",
                "source_id": "nadlan.gov.il",
            }
        ],
    )
    write_csv(release_geo, ["geography_id"], [{"geography_id": "1000"}])
    write_csv(release_cross, ["locality_code"], [{"locality_code": "1000"}])
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(
            {
                "release_version": "v0.2.0",
                "data_quality_summary": {
                    "fact_rows": 1,
                    "geography_rows": 1,
                    "locality_crosswalk_rows": 1,
                }
            }
        ),
        encoding="utf-8",
    )
    write_csv(
        release_files,
        ["path", "sha256"],
        [
            {"path": "data/current/rent_benchmarks.csv", "sha256": "same-rent"},
            {"path": "data/current/geography_reference.csv", "sha256": "same-geo"},
            {"path": "data/current/locality_crosswalk.csv", "sha256": "same-cross"},
            {"path": "data/releases/v0.2.0/rent_benchmarks.csv", "sha256": "same-rent"},
            {"path": "data/releases/v0.2.0/geography_reference.csv", "sha256": "same-geo"},
            {
                "path": "data/releases/v0.2.0/locality_crosswalk.csv",
                "sha256": "same-cross",
            },
        ],
    )

    monkeypatch.setattr(vr, "FACT_PATH", fact)
    monkeypatch.setattr(vr, "GEOGRAPHY_PATH", geo)
    monkeypatch.setattr(vr, "LOCALITY_CROSSWALK_PATH", cross)
    monkeypatch.setattr(vr, "MANIFEST_PATH", manifest)
    monkeypatch.setattr(vr, "RELEASE_FILES_PATH", release_files)
    monkeypatch.setattr(brm, "ROOT", tmp_path)
    monkeypatch.setattr(brm, "CURRENT_DIR", tmp_path / "data" / "current")
    monkeypatch.setattr(brm, "METADATA_DIR", tmp_path / "metadata")


def test_release_validation_passes(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    assert vr.validate_release() == []


def test_release_validation_reports_path_and_count_errors(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    vr.MANIFEST_PATH.write_text(
        json.dumps(
            {
                "release_version": "v0.2.0",
                "data_quality_summary": {
                    "fact_rows": 2,
                    "geography_rows": 2,
                    "locality_crosswalk_rows": 2,
                },
                "bad_path": "/abs/path",
            }
        ),
        encoding="utf-8",
    )
    errors = vr.validate_release()
    assert any("internal absolute paths" in error for error in errors)
    assert any("fact row count" in error for error in errors)
    assert any("geography row count" in error for error in errors)
    assert any("locality row count" in error for error in errors)


def test_release_validation_reports_absolute_release_file_paths(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    write_csv(
        vr.RELEASE_FILES_PATH,
        ["path", "sha256"],
        [
            {"path": "data/current/rent_benchmarks.csv", "sha256": "same-rent"},
            {"path": "data/current/geography_reference.csv", "sha256": "same-geo"},
            {"path": "data/current/locality_crosswalk.csv", "sha256": "same-cross"},
            {"path": "data/releases/v0.2.0/rent_benchmarks.csv", "sha256": "same-rent"},
            {"path": "data/releases/v0.2.0/geography_reference.csv", "sha256": "same-geo"},
            {
                "path": "data/releases/v0.2.0/locality_crosswalk.csv",
                "sha256": "same-cross",
            },
            {"path": "C:\\temp\\internal.csv", "sha256": "other"},
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


def test_contains_absolute_path_handles_nested_structures() -> None:
    assert vr.contains_absolute_path(
        {"files": [{"path": "C:\\temp\\internal.csv"}], "extra": ["relative/path.csv"]}
    )
    assert vr.contains_absolute_path({"C:\\temp\\internal.csv": "relative/path.csv"})
    assert not vr.contains_absolute_path({"files": [{"path": "data/current/rent_benchmarks.csv"}]})


def test_release_validation_reports_dataset_shape_errors(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    write_csv(
        vr.FACT_PATH,
        [
            "record_id",
            "geography_id",
            "geography_type",
            "metric_type",
            "value_nis",
            "period_type",
            "source_id",
        ],
        [
            {
                "record_id": "dup",
                "geography_id": "9999",
                "geography_type": "bad",
                "metric_type": "bad",
                "value_nis": "",
                "period_type": "bad",
                "source_id": "nadlan.gov.il",
            },
            {
                "record_id": "dup",
                "geography_id": "1000",
                "geography_type": "locality",
                "metric_type": "average_rent_published",
                "value_nis": "5200",
                "period_type": "quarterly",
                "source_id": "nadlan.gov.il",
            },
        ],
    )

    errors = vr.validate_release()

    assert "duplicate record_id values found in rent_benchmarks.csv" in errors
    assert "rent_benchmarks.csv contains blank value_nis fields" in errors
    assert "rent_benchmarks.csv contains invalid geography_type values" in errors
    assert "rent_benchmarks.csv contains invalid metric_type values" in errors
    assert "rent_benchmarks.csv contains invalid period_type values" in errors
    assert any("fact rows missing geography_reference join keys" in error for error in errors)


def test_release_validation_reports_missing_canonical_paths(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    write_csv(
        vr.RELEASE_FILES_PATH,
        ["path", "sha256"],
        [{"path": "data/current/rent_benchmarks.csv", "sha256": "same-rent"}],
    )

    errors = vr.validate_release()

    assert "release_files.csv is missing one or more canonical file paths" in errors


def test_build_summary_reads_fixture_contents(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)

    summary = vr.build_summary()

    assert summary == {
        "fact_rows": 1,
        "geography_rows": 1,
        "distinct_fact_sources": ["nadlan.gov.il"],
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
    assert '"fact_rows": 1' in capsys.readouterr().out


def test_build_release_metadata_main_writes_expected_outputs(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)

    assert brm.main([]) == 0

    release_files = list(csv.DictReader((tmp_path / "metadata" / "release_files.csv").open()))
    assert [row["path"] for row in release_files] == [
        "data/current/rent_benchmarks.csv",
        "data/current/geography_reference.csv",
        "data/current/locality_crosswalk.csv",
        "data/releases/v0.2.0/rent_benchmarks.csv",
        "data/releases/v0.2.0/geography_reference.csv",
        "data/releases/v0.2.0/locality_crosswalk.csv",
    ]

    source_inventory = list(
        csv.DictReader((tmp_path / "metadata" / "source_inventory.csv").open())
    )
    assert {row["source_id"] for row in source_inventory} == {
        "nadlan.gov.il",
        "cbs_table49",
        "boi_hedonic",
        "data.gov.il",
    }

    manifest = json.loads((tmp_path / "metadata" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["files"][0]["path"] == "data/current/rent_benchmarks.csv"
    assert manifest["data_quality_summary"]["locality_crosswalk_rows"] == 1


def test_build_release_files_and_manifest_helpers(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)

    release_files = brm.build_release_files()
    manifest = brm.build_manifest(release_files)

    assert [row["path"] for row in release_files] == [
        "data/current/rent_benchmarks.csv",
        "data/current/geography_reference.csv",
        "data/current/locality_crosswalk.csv",
        "data/releases/v0.2.0/rent_benchmarks.csv",
        "data/releases/v0.2.0/geography_reference.csv",
        "data/releases/v0.2.0/locality_crosswalk.csv",
    ]
    assert all(row["release_version"] == brm.RELEASE_VERSION for row in release_files)
    assert manifest["release_version"] == brm.RELEASE_VERSION
    assert manifest["schema_version"] == brm.SCHEMA_VERSION
    assert manifest["data_quality_summary"]["fact_rows"] == 1


def test_release_validation_reports_snapshot_mismatch(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    write_csv(
        vr.RELEASE_FILES_PATH,
        ["path", "sha256"],
        [
            {"path": "data/current/rent_benchmarks.csv", "sha256": "same-rent"},
            {"path": "data/current/geography_reference.csv", "sha256": "same-geo"},
            {"path": "data/current/locality_crosswalk.csv", "sha256": "same-cross"},
            {"path": "data/releases/v0.2.0/rent_benchmarks.csv", "sha256": "other-rent"},
            {"path": "data/releases/v0.2.0/geography_reference.csv", "sha256": "same-geo"},
            {
                "path": "data/releases/v0.2.0/locality_crosswalk.csv",
                "sha256": "same-cross",
            },
        ],
    )

    errors = vr.validate_release()

    assert "release snapshot does not match current file for rent_benchmarks.csv" in errors


def test_build_data_dictionary_and_source_inventory(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)

    data_dictionary = brm.build_data_dictionary()
    source_inventory = brm.build_source_inventory()

    assert data_dictionary[0]["file_name"] == "rent_benchmarks.csv"
    assert {row["column_name"] for row in data_dictionary if row["file_name"] == "geography_reference.csv"} == {
        "geography_id"
    }
    assert {row["source_id"] for row in source_inventory} == {
        "nadlan.gov.il",
        "cbs_table49",
        "boi_hedonic",
        "data.gov.il",
    }


def test_build_data_dictionary_handles_header_only_csv(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    (brm.CURRENT_DIR / "geography_reference.csv").write_text("geography_id\n", encoding="utf-8")

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
        == "d08c2f9873cf4e38ab7e9846bba35522cdb517c00be5035ab9c6e6ec22dc28cb"
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
