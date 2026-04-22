# israel-nadlan-data

Public geography and reference dataset for Israeli housing data.

This repository is a self-contained public data product. It publishes geography reference tables, locality context, machine-readable metadata, and documentation needed to understand the release without relying on any private workspace.

## What This Repository Publishes

- `data/current/geography_reference.csv`: canonical geography reference table
- `data/current/locality_crosswalk.csv`: locality context and compatibility table
- `metadata/manifest.json`: release manifest
- `metadata/data_dictionary.csv`: column dictionary
- `metadata/release_files.csv`: file-level checksums and row counts

## Current Release

| Field | Value |
| --- | --- |
| Release version | `v0.2.0` |
| Release date | `2026-04-22` |
| Schema version | `2.1.0` |
| Geography rows | `1,312` |
| Locality crosswalk rows | `1,306` |

## Interpretation Guide

- `geography_reference.csv` is the canonical geography dimension.
- `locality_crosswalk.csv` is contextual support for locality lookups and joins.
- `geography_type` must be checked before ranking or joining places.
- This repository does not publish rent benchmark observations, modeled estimates, or source inventories.

## Release Layout

```text
data/
  current/
  releases/v0.2.0/
metadata/
  manifest.json
  data_dictionary.csv
  release_files.csv
```

## Rights And Attribution

The repository keeps rights language conservative and source-specific.

- Repository-authored metadata and documentation are separate from upstream public source terms.
- Geographic reference tables may still point at their upstream public data sources in the docs.
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
