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
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(
            {
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
        ["path"],
        [
            {"path": "data/current/rent_benchmarks.csv"},
            {"path": "data/current/geography_reference.csv"},
            {"path": "data/current/locality_crosswalk.csv"},
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
                "data_quality_summary": {
                    "fact_rows": 2,
                    "geography_rows": 1,
                    "locality_crosswalk_rows": 1,
                },
                "bad_path": "/abs/path",
            }
        ),
        encoding="utf-8",
    )
    errors = vr.validate_release()
    assert any("internal absolute paths" in error for error in errors)
    assert any("fact row count" in error for error in errors)


def test_release_validation_reports_absolute_release_file_paths(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    write_csv(
        vr.RELEASE_FILES_PATH,
        ["path"],
        [
            {"path": "data/current/rent_benchmarks.csv"},
            {"path": "data/current/geography_reference.csv"},
            {"path": "data/current/locality_crosswalk.csv"},
            {"path": "C:\\temp\\internal.csv"},
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

    assert "manifest.json is missing required data_quality_summary fields" in errors


def test_main_returns_zero_for_clean_fixture(tmp_path: Path, monkeypatch, capsys) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    monkeypatch.setattr("sys.argv", ["validate_release.py", "--check"])
    assert vr.main() == 0
    assert '"fact_rows": 1' in capsys.readouterr().out


def test_build_release_metadata_main_writes_expected_outputs(
    tmp_path: Path, monkeypatch
) -> None:
    install_fixture_repo(tmp_path, monkeypatch)

    assert brm.main() == 0

    release_files = list(csv.DictReader((tmp_path / "metadata" / "release_files.csv").open()))
    assert [row["path"] for row in release_files] == [
        "data/current/rent_benchmarks.csv",
        "data/current/geography_reference.csv",
        "data/current/locality_crosswalk.csv",
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


def test_module_main_raises_system_exit_when_run_as_script(monkeypatch) -> None:
    monkeypatch.setattr(vr, "main", lambda: 0)
    monkeypatch.setattr("sys.argv", ["validate_release.py"])
    try:
        runpy.run_module("scripts.validate_release", run_name="__main__")
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("expected SystemExit")
