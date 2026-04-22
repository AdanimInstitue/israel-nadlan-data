# israel-nadlan-data

Public dataset repository for Israeli housing-rent benchmark observations derived from named public sources.

This repository is a data product, not an exploratory workspace. It publishes release snapshots, schema and methodology documentation, conservative rights notes, and machine-readable metadata needed to understand each release on its own.

## What This Repository Publishes

The repository publishes:

- `data/current/rent_benchmarks.csv`: canonical benchmark table
- `data/current/geography_reference.csv`: canonical geography dimension
- `data/current/locality_crosswalk.csv`: locality-only compatibility table
- `metadata/manifest.json`: release manifest
- `metadata/source_inventory.csv`: source inventory
- `metadata/data_dictionary.csv`: column dictionary
- `metadata/release_files.csv`: file-level checksums and row counts

## Current Release

| Field | Value |
| --- | --- |
| Release version | `v0.2.0` |
| Release date | `2026-04-22` |
| Schema version | `2.1.0` |
| Main fact rows | `10,472` |
| Geography rows | `1,312` |
| Locality crosswalk rows | `1,306` |

## Interpretation Guide

- One row in `rent_benchmarks.csv` is one benchmark observation for one geography, one room bucket, one source, and one period.
- `metric_type` must be checked before comparing values.
- `geography_type` must be checked before ranking or joining places.
- The repository contains both direct published values and modeled estimates.
- This is not a live inventory or listing-feed dataset.

## Release Layout

```text
data/
  current/
  releases/v0.2.0/
metadata/
  manifest.json
  source_inventory.csv
  data_dictionary.csv
  release_files.csv
```

## Rights And Attribution

The repository uses a conservative, source-aware rights posture.

- Code and repository-authored release metadata are separate from upstream source rights.
- Source-derived tables remain subject to source-specific terms and attribution requirements.
- This repository does not claim to override upstream permissions.

See:

- [DATA-LICENSE.md](DATA-LICENSE.md)
- [SOURCES.md](SOURCES.md)
- [ATTRIBUTION.md](ATTRIBUTION.md)

## Documentation

- [SCHEMA.md](SCHEMA.md)
- [METHODOLOGY.md](METHODOLOGY.md)
- [QA.md](QA.md)
- [LIMITATIONS.md](LIMITATIONS.md)
- [CHANGELOG.md](CHANGELOG.md)

## Validation

```bash
python scripts/build_release_metadata.py
python scripts/validate_release.py --check
```
