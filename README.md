# israel-rent-data

Published CSV snapshots for the Adanim Institute Israel rent benchmark dataset.

## Files

- `rent_benchmarks.csv`
  Locality-by-room-group rent benchmarks.
- `locality_crosswalk.csv`
  Locality metadata used by the benchmark pipeline.
- `manifest.json`
  Machine-readable release metadata, provenance, row counts, and file hashes.

## Versioning

Dataset releases are published as Git tags and GitHub releases in this repository.

The first public snapshot is `v0.1.0`, built from a validated collector run on April 21, 2026.

## Current Snapshot

- Version: `v0.1.0`
- Publication commit: release-tagged in this repository as `v0.1.0`
- Source collector repo: `AdanimInstitue/israel-rent-data-collector`
- Collector commit used for the validated run: `0cdfd62`
- Validated command:
  `rent-collector --source all --output data/output/rent_benchmarks.csv --validate`

## Snapshot Summary

- `rent_benchmarks.csv`
  - Rows: `10,472`
  - Localities covered: `1,312`
  - Source mix:
    - `boi_hedonic`: `10,117`
    - `nadlan.gov.il`: `297`
    - `cbs_table49`: `58`
- `locality_crosswalk.csv`
  - Rows: `1,306`
  - Columns:
    - `locality_code`
    - `locality_name_he`
    - `locality_name_en`
    - `district_he`
    - `district_en`
    - `population_approx`
    - `source`

## Provenance

This snapshot was generated from the validated live collector run recorded at:

`../israel-rent-data-collector/var/runs/2026-04-21T18-54-55Z/run.json`

The manifest in this repo captures the exact file hashes for the published CSVs.
