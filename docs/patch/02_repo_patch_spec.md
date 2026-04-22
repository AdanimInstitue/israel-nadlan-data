# Repository Patch Specification

## Goal

This document specifies the exact repository-level changes to make in `israel-rent-data`.

## Current Root State

Observed current root files:
- `README.md`
- `manifest.json`
- `rent_benchmarks.csv`
- `locality_crosswalk.csv`

## Target Repository Structure

The target structure after the patch should be:

```text
/
├── README.md
├── DATA-LICENSE.md
├── SOURCES.md
├── ATTRIBUTION.md
├── SCHEMA.md
├── METHODOLOGY.md
├── QA.md
├── LIMITATIONS.md
├── manifest.json
├── rent_benchmarks.csv
├── geography_reference.csv
├── locality_crosswalk.csv              # optional compatibility artifact
└── docs/
    └── patch/
        ├── 01_overview_and_execution_plan.md
        ├── 02_repo_patch_spec.md
        ├── 03_schema_and_data_model_redesign.md
        ├── 04_rights_licensing_and_provenance_plan.md
        ├── 05_documentation_pack_spec.md
        └── 06_data_expansion_and_release_checklist.md
```

## Required File Actions

### 1. Update `README.md`
Replace the thin release note style README with a true dataset landing page containing:
- what the dataset is
- what official/public sources it uses
- what one row means
- current coverage
- important limitations
- rights / attribution notice
- file inventory
- versioning and provenance summary
- change log snippet / release summary
- how to cite / how to attribute

### 2. Add `DATA-LICENSE.md`
Purpose:
- define what rights the repository grants over repository-authored materials
- avoid overstating rights over upstream source-derived data
- explain source-specific rights dependencies
- explain current licensing posture and future relicensing gate

### 3. Add `SOURCES.md`
One section per source with:
- `source_id`
- source name
- dataset / page title
- URL
- access method
- access date or publication date
- geographic scope
- metric type(s)
- room-group handling
- terms / license URL
- attribution text
- reuse / republication note
- open questions if any

### 4. Add `ATTRIBUTION.md`
Provide:
- a short attribution block for general reuse
- a full attribution block for academic / public report use
- source-specific attributions if needed
- note that users remain responsible for complying with upstream source terms

### 5. Add `SCHEMA.md`
Document all released data files and all columns.

### 6. Add `METHODOLOGY.md`
Explain:
- what each source contributes
- how room groups are normalized
- how geography is normalized
- how annual vs quarterly observations are represented
- how duplicates / conflicts are handled
- which fields are raw vs derived vs normalized

### 7. Add `QA.md`
Document validation checks, expected invariants, and release QA gates.

### 8. Add `LIMITATIONS.md`
Document interpretation limits and known caveats.

### 9. Update `manifest.json`
Patch manifest structure so that it includes:
- schema version
- release version
- published timestamp
- collector repo and commit
- collector run identifier or public-safe relative path
- file hashes
- row counts
- distinct geography counts by geography type
- distinct source counts
- source catalog summary
- source terms / license references
- release notes summary
- compatibility notes

### 10. Add `geography_reference.csv`
This should become the canonical geography dimension covering all geography entities used by the dataset, including:
- localities
- district pseudo-geographies if retained in the main fact table

### 11. Keep or Deprecate `locality_crosswalk.csv`
Options:
- keep it as a compatibility artifact and document it as locality-only
- or deprecate it in favor of `geography_reference.csv`

Preferred path:
- keep it for one release cycle
- add a deprecation note in `README.md` and `SCHEMA.md`

## Recommended Root-Level File Inventory After Patch

### Data Files
- `rent_benchmarks.csv`
- `geography_reference.csv`
- `locality_crosswalk.csv` (optional compatibility)
- optional future companion tables

### Metadata / Documentation Files
- `README.md`
- `SCHEMA.md`
- `METHODOLOGY.md`
- `QA.md`
- `LIMITATIONS.md`
- `DATA-LICENSE.md`
- `SOURCES.md`
- `ATTRIBUTION.md`
- `manifest.json`

## File-by-File Patch Notes

### `rent_benchmarks.csv`
Must be regenerated or transformed to fit the redesigned schema in the schema doc.

### `geography_reference.csv`
Must include rows for:
- every locality code present in fact data
- every district pseudo-code present in fact data if those rows remain published

### `locality_crosswalk.csv`
If retained:
- clearly document that it is locality-only
- do not imply that it covers all fact-table geographies

### `README.md`
Must explicitly state:
- this dataset currently does **not** represent live listing inventory
- this dataset blends multiple official/public sources with different metric types
- users should inspect `metric_type`, `source`, and period fields before comparing rows

### `manifest.json`
Must not include internal workstation paths such as `/Users/...`

## Recommended Backward-Compatibility Policy

For the next release:
- keep `rent_benchmarks.csv` as the main fact file name
- keep `locality_crosswalk.csv` if easy
- document breaking schema changes clearly
- add `schema_version`
- add a migration note mapping old columns to new columns

## Acceptance Criteria

This patch spec is satisfied when:
- all target files exist
- the main table schema matches `SCHEMA.md`
- the repository is understandable without reading the collector code
- the rights situation is clearly documented
- no internal paths remain in public metadata
