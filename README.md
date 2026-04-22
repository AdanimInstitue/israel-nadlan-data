# israel-rent-data

Public release repository for normalized Israeli rent benchmark observations built from official or public upstream sources.

This repository publishes source-aware rent benchmark tables. It is not a live listings feed, not a transaction log, and not a single harmonized "market price" series.

## What This Repository Publishes

The repository packages one main fact table plus supporting metadata:

- `rent_benchmarks.csv`: canonical fact table. One row is one geography x room group x metric type x period x source observation.
- `geography_reference.csv`: canonical geography dimension for every geography ID used in the fact table, including district pseudo-geographies from CBS Table 4.9.
- `locality_crosswalk.csv`: locality-only compatibility artifact retained from `v0.1.0`. It is not the canonical geography dimension for the full dataset.
- `manifest.json`: public-safe release metadata, provenance, file hashes, row counts, and compatibility notes.

## Current Release Snapshot

This patch prepares the next breaking schema release after `v0.1.0`.

| Field | Value |
| --- | --- |
| Recommended release version | `v0.2.0` |
| Schema version | `2.0.0` |
| Patch date | `2026-04-22` |
| Collector repo | `AdanimInstitue/israel-rent-data-collector` |
| Collector commit used for the validated run | `0cdfd6210156263cbbf260b76b869a3a3fc68ba4` |
| Collector run ID | `2026-04-21T18-54-55Z` |
| Validated command | `rent-collector --source all --output data/output/rent_benchmarks.csv --validate` |

## File Inventory

| File | Role | Rows | Status |
| --- | --- | ---: | --- |
| `rent_benchmarks.csv` | Main fact table | 10,472 | canonical |
| `geography_reference.csv` | Geography dimension | 1,312 | canonical |
| `locality_crosswalk.csv` | Locality-only lookup from `v0.1.0` | 1,306 | compatibility-only |
| `manifest.json` | Release and provenance metadata | n/a | canonical |
| `DATA-LICENSE.md` | Rights posture for this repo | n/a | canonical |
| `SOURCES.md` | Source inventory and terms pointers | n/a | canonical |
| `ATTRIBUTION.md` | Reuse attribution templates | n/a | canonical |
| `SCHEMA.md` | Data dictionary and migration notes | n/a | canonical |
| `METHODOLOGY.md` | Normalization and merge logic | n/a | canonical |
| `QA.md` | Validation checks and release checklist | n/a | canonical |
| `LIMITATIONS.md` | Interpretation limits and caveats | n/a | canonical |

## Quick Interpretation Guide

- One row means one published or modeled observation for one geography, one room bucket, one period, and one source.
- Always inspect `metric_type` before comparing rows. This release mixes directly published averages with modeled hedonic estimates.
- Always inspect `geography_type` before joining or ranking rows. District rows are present and are explicitly labeled as districts.
- Always inspect `period_type`, `period_year`, `period_quarter`, and `period_label` before aggregating. Annual and quarterly observations coexist.
- `value_nis` is the single primary numeric value column. `v0.1.0` value columns such as `rent_nis`, `median_rent_nis`, and `avg_rent_nis` are no longer used.

## Coverage Summary

### Geography

- Distinct geographies: `1,312`
- Localities: `1,306`
- Districts: `6`

### Sources

| `source_id` | Rows | `metric_type` | Geography coverage |
| --- | ---: | --- | --- |
| `boi_hedonic` | 10,117 | `hedonic_rent_estimate` | locality |
| `nadlan.gov.il` | 297 | `average_rent_published` | locality |
| `cbs_table49` | 58 | `average_rent_published` | locality and district |

### Periods

| `period_label` | Rows |
| --- | ---: |
| `2025` | 10,117 |
| `2025-Q2` | 354 |
| `2025-Q1` | 1 |

## Rights And Attribution

This repository uses a conservative, source-aware rights posture:

- Repository-authored documentation and original release metadata are described separately in [DATA-LICENSE.md](DATA-LICENSE.md).
- Source-derived tables remain subject to upstream source terms, attribution requirements, and any other applicable restrictions.
- This repository does not claim to override upstream rights and does not claim a blanket CC BY license for the full combined dataset.

Read:

- [DATA-LICENSE.md](DATA-LICENSE.md)
- [SOURCES.md](SOURCES.md)
- [ATTRIBUTION.md](ATTRIBUTION.md)

## Provenance

The repository keeps auditable but public-safe provenance:

- collector repository and commit are retained
- validated collector command is retained
- file hashes and row counts are retained in `manifest.json`
- internal workstation paths from `v0.1.0` were removed from public metadata

For the release metadata, see [manifest.json](manifest.json).

## Breaking Change From `v0.1.0`

This patch is a breaking schema revision intended for `v0.2.0`.

- `rent_nis` was replaced by `value_nis`
- dead value columns were removed
- `metric_type` is now explicit
- `geography_type` is now explicit
- period semantics are now explicit
- district pseudo-geographies now live in `geography_reference.csv`
- `locality_crosswalk.csv` is retained only for compatibility

Migration details are documented in [SCHEMA.md](SCHEMA.md).

## How To Cite

Recommended short citation:

> Adanim Institute. israel-rent-data, release candidate for v0.2.0, accessed 2026-04-22. Derived from official/public Israeli housing-rent sources with source-specific terms and attribution obligations.

If publishing analysis or a derived dataset, also cite the relevant upstream sources listed in [SOURCES.md](SOURCES.md).

## Limitations

This repository is best used as a benchmark dataset, not as a direct measure of current asking rents or listing volume. Important interpretation limits are collected in [LIMITATIONS.md](LIMITATIONS.md).
