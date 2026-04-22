from __future__ import annotations

import csv
import json
import runpy
from pathlib import Path

from scripts import validate_release as vr


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def sample_fact_row() -> dict[str, str]:
    return {
        "record_id": "nadlan_gov_il__1000__3__average_rent_published__2025-Q2",
        "geography_id": "1000",
        "geography_type": "locality",
        "geography_name_he": "א",
        "geography_name_en": "A",
        "room_group": "3",
        "metric_type": "average_rent_published",
        "value_nis": "5000",
        "currency": "ILS",
        "period_type": "quarterly",
        "period_year": "2025",
        "period_quarter": "2",
        "period_label": "2025-Q2",
        "source_id": "nadlan.gov.il",
        "source_series_id": "series",
        "source_url": "https://example.com",
        "source_release_date": "",
        "source_accessed_at": "",
        "is_official_published_value": "true",
        "is_modeled_value": "false",
        "suppressed": "false",
        "observations_count": "",
        "qa_status": "pass",
        "notes": "",
    }


def sample_geo_row() -> dict[str, str]:
    return {
        "geography_id": "1000",
        "geography_type": "locality",
        "locality_code": "1000",
        "district_code": "",
        "geography_name_he": "א",
        "geography_name_en": "A",
        "district_he": "מחוז",
        "district_en": "District",
        "population_approx": "",
        "source": "data.gov.il",
        "is_active": "true",
    }


def sample_manifest() -> dict:
    return {
        "data_quality_summary": {
            "fact_rows": 1,
            "geography_rows": 1,
            "distinct_geographies_by_type": {"locality": 1, "district": 0},
        },
        "files": {"locality_crosswalk.csv": {"rows": 1}},
    }


def install_fixture_repo(tmp_path: Path, monkeypatch) -> None:
    fact = tmp_path / "rent_benchmarks.csv"
    geo = tmp_path / "geography_reference.csv"
    cross = tmp_path / "locality_crosswalk.csv"
    manifest = tmp_path / "manifest.json"

    write_csv(fact, list(sample_fact_row().keys()), [sample_fact_row()])
    write_csv(geo, list(sample_geo_row().keys()), [sample_geo_row()])
    write_csv(
        cross,
        [
            "locality_code",
            "locality_name_he",
            "locality_name_en",
            "district_he",
            "district_en",
            "population_approx",
            "source",
        ],
        [
            {
                "locality_code": "1000",
                "locality_name_he": "א",
                "locality_name_en": "A",
                "district_he": "מחוז",
                "district_en": "District",
                "population_approx": "",
                "source": "data.gov.il",
            }
        ],
    )
    manifest.write_text(json.dumps(sample_manifest()), encoding="utf-8")

    monkeypatch.setattr(vr, "FACT_PATH", fact)
    monkeypatch.setattr(vr, "GEOGRAPHY_PATH", geo)
    monkeypatch.setattr(vr, "LOCALITY_CROSSWALK_PATH", cross)
    monkeypatch.setattr(vr, "MANIFEST_PATH", manifest)

def test_release_validation_passes() -> None:
    assert vr.validate_release() == []


def test_summary_matches_expected_release_shape() -> None:
    summary = vr.build_summary()
    assert summary["fact_rows"] == 10472
    assert summary["geography_rows"] == 1312
    assert summary["distinct_fact_sources"] == ["boi_hedonic", "cbs_table49", "nadlan.gov.il"]


def test_record_id_helpers_apply_documented_normalization() -> None:
    assert vr.normalize_source_id_for_record_id("nadlan.gov.il") == "nadlan_gov_il"
    assert vr.normalize_room_group_for_record_id("5+") == "5plus"
    assert (
        vr.build_record_id(
            {
                "source_id": "nadlan.gov.il",
                "geography_id": "5000",
                "room_group": "5+",
                "metric_type": "average_rent_published",
                "period_label": "2025-Q2",
            }
        )
        == "nadlan_gov_il__5000__5plus__average_rent_published__2025-Q2"
    )


def test_validate_release_reports_structural_errors(tmp_path: Path, monkeypatch) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    fact = sample_fact_row()
    fact["record_id"] = "dup"
    duplicate = dict(fact)
    duplicate["geography_type"] = "bad_geography"
    duplicate["metric_type"] = "bad_metric"
    duplicate["geography_id"] = "9999"
    duplicate["value_nis"] = ""
    write_csv(vr.FACT_PATH, list(fact.keys()), [fact | {"record_id": "dup"}, duplicate])

    manifest = sample_manifest()
    manifest["data_quality_summary"]["fact_rows"] = 99
    manifest["data_quality_summary"]["geography_rows"] = 77
    manifest["data_quality_summary"]["distinct_geographies_by_type"] = {"locality": 2, "district": 7}
    manifest["files"]["locality_crosswalk.csv"]["rows"] = 7
    manifest["collector_repo"] = {"collector_run_artifact": "/Users/example/private/path"}
    vr.MANIFEST_PATH.write_text(json.dumps(manifest) + "\n", encoding="utf-8")

    errors = vr.validate_release()
    assert any("duplicate record_id" in error for error in errors)
    assert any("blank value_nis" in error for error in errors)
    assert any("invalid geography_type" in error for error in errors)
    assert any("invalid metric_type" in error for error in errors)
    assert any("missing geography_reference" in error for error in errors)
    assert any("internal absolute paths" in error for error in errors)
    assert any("fact_rows" in error for error in errors)
    assert any("geography_rows" in error for error in errors)
    assert any("locality_crosswalk row count" in error for error in errors)
    assert any("distinct_geographies_by_type" in error for error in errors)


def test_main_returns_zero_for_clean_fixture(tmp_path: Path, monkeypatch, capsys) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    monkeypatch.setattr("sys.argv", ["validate_release.py", "--check"])
    assert vr.main() == 0
    captured = capsys.readouterr()
    assert '"fact_rows": 1' in captured.out


def test_main_returns_nonzero_for_invalid_fixture(tmp_path: Path, monkeypatch, capsys) -> None:
    install_fixture_repo(tmp_path, monkeypatch)
    bad_fact = sample_fact_row()
    bad_fact["period_type"] = "other"
    write_csv(vr.FACT_PATH, list(bad_fact.keys()), [bad_fact])
    monkeypatch.setattr("sys.argv", ["validate_release.py", "--check"])
    assert vr.main() == 1
    captured = capsys.readouterr()
    assert "Release validation failed:" in captured.out


def test_module_main_raises_system_exit_when_run_as_script(monkeypatch) -> None:
    monkeypatch.setattr(vr, "main", lambda: 0)
    try:
        runpy.run_module("scripts.validate_release", run_name="__main__")
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("expected SystemExit")
