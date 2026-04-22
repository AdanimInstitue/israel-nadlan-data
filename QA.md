# QA

This file documents the release checks expected for the public dataset repository.

## Release Validation Checks

The patched repository is expected to satisfy these checks:

- no null `value_nis` in `rent_benchmarks.csv`
- `record_id` is unique
- `metric_type` values are valid
- `geography_type` values are valid
- every fact-table `geography_id` joins to `geography_reference.csv`
- no internal absolute workstation paths remain in public metadata
- `README.md`, `SCHEMA.md`, and `manifest.json` agree on row counts and schema version
- all published sources are documented in `SOURCES.md`

## Current Patch Outcome

For the patched repository state prepared on `2026-04-22`:

- `rent_benchmarks.csv` rows: `10,472`
- `geography_reference.csv` rows: `1,312`
- fact-table geographies covered by reference table: `100%`
- `record_id` duplicates: `0`
- null `value_nis` rows: `0`
- internal `/Users/...` paths in `manifest.json`: `0`

## Sanity Checks

Recommended pre-release sanity checks:

- review source distribution by `source_id`
- review geography distribution by `geography_type`
- review period distribution by `period_label`
- confirm district rows are labeled `district`
- confirm `locality_crosswalk.csv` is still documented as compatibility-only

## Known Warning Conditions

- `nadlan.gov.il` terms are not yet pinned to a dedicated open-license page in this patch, so rights posture remains conservative
- `boi_hedonic` rows are modeled estimates and should not be treated as directly published official values
- `source_release_date` and `source_accessed_at` are not yet tracked per row
- the public snapshot remains 2025-heavy and should not be interpreted as a longitudinal historical panel

## Manual Review Checklist

Before tagging a release:

- confirm docs still match the shipped CSV columns
- confirm file hashes in `manifest.json` were regenerated after the final file edits
- confirm no internal paths appear anywhere in public files
- confirm the release notes mention the schema break from `v0.1.0`
- confirm rights files do not overclaim a blanket license over source-derived data

## Publication Checklist

- [ ] `record_id` unique
- [ ] no null `value_nis`
- [ ] valid `metric_type`
- [ ] valid `geography_type`
- [ ] all fact rows join to `geography_reference.csv`
- [ ] `README.md` matches actual file inventory
- [ ] `SCHEMA.md` matches actual columns
- [ ] `SOURCES.md` covers each source used in the release
- [ ] no internal machine paths remain in `manifest.json`
- [ ] file hashes updated after final docs edits
