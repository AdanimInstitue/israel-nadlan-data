from __future__ import annotations

import csv
import json
import runpy
from pathlib import Path

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


def test_main_returns_zero_for_clean_fixture(tmp_path: Path, monkeypatch, capsys) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    monkeypatch.setattr("sys.argv", ["validate_release.py", "--check"])
    assert vr.main() == 0
    assert '"fact_rows": 1' in capsys.readouterr().out


def test_module_main_raises_system_exit_when_run_as_script(monkeypatch) -> None:
    monkeypatch.setattr(vr, "main", lambda: 0)
    monkeypatch.setattr("sys.argv", ["validate_release.py"])
    try:
        runpy.run_module("scripts.validate_release", run_name="__main__")
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("expected SystemExit")
