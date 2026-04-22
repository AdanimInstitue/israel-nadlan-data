# Data Expansion and Release Checklist

## Purpose

This document covers:
1. what should be added to the dataset after the core patch
2. what metadata should be added
3. what QA / release checks should gate publication

## Part I — Recommended Data Additions

These additions should remain official/public-source only.

## A. Add a Canonical Geography Table

### Required
Add `geography_reference.csv`.

Reason:
The current release uses locality rows and district pseudo-geographies, but only publishes a locality-only crosswalk.

### Recommended Columns
- `geography_id`
- `geography_type`
- `locality_code`
- `district_code`
- `geography_name_he`
- `geography_name_en`
- `district_he`
- `district_en`
- `population_approx`
- `source`
- optional `population_year`
- optional `municipality_type`
- optional `is_deprecated`

## B. Add a Source Catalog

### Recommended File
`source_catalog.csv`

### Recommended Columns
- `source_id`
- `source_name`
- `publisher`
- `source_url`
- `terms_url`
- `license_summary`
- `metric_type_default`
- `attribution_text`
- `notes`

Reason:
This makes rights / provenance machine-readable and joinable.

## C. Add Rental Stock Context

### Recommended File
`rental_stock_context.csv`

### Candidate Content
Locality-level or district-level indicators such as:
- number of rented dwellings
- share of rented dwellings
- period / year
- source details

Reason:
This provides context for interpreting rent levels and supports policy / welfare analysis.

## D. Add Sale-Price Context as a Separate Table

### Recommended File
`sale_price_context.csv`

Possible indicators:
- median or average sale price by geography / period where officially available
- source IDs and periods

Reason:
This enables rent-to-price and affordability context, but should remain separate from the rent benchmark table.

## E. Add Richer Geography Metadata

Potential public metadata additions:
- sub-district
- municipality type
- population and population year
- socio-economic cluster if from a public source
- peripherality / centrality indicator if from a public source
- regional / metro grouping
- centroid coordinates or shape references if publicly publishable

These should go into `geography_reference.csv`, not the main fact table, unless absolutely necessary.

## Part II — Recommended Metadata Additions

## A. Add Stronger Per-Row Metadata
To `rent_benchmarks.csv`, add:
- `record_id`
- `metric_type`
- `geography_type`
- `period_type`
- `period_label`
- `source_url`
- `source_release_date`
- `is_official_published_value`
- `is_modeled_value`
- `suppressed`
- `qa_status`

## B. Add Manifest Metadata
To `manifest.json`, add:
- `schema_version`
- `release_notes`
- `source_catalog_summary`
- `terms_checked_at` per source if available
- `compatibility_notes`
- `data_quality_summary`

## C. Add Citation Metadata
Optional but recommended:
- `CITATION.cff`
- a short citation section in `README.md`

## Part III — Data Quality Improvements

## A. Fix Empty / Misleading Columns
The next release should not contain dead columns such as:
- always-empty metric columns
- always-empty observations columns unless intentionally retained and documented

## B. Normalize Metric Representation
Use a single `value_nis` column and explicit `metric_type`.

## C. Normalize Period Representation
Avoid ambiguous annual / quarterly mixing.

## D. Normalize Geography Representation
Do not leave district rows modeled as if they were localities.

## Part IV — Release Checklist

The agent should implement a release checklist and include it in `QA.md` or a dedicated release section.

### Pre-Release Data Checks
- [ ] No null `value_nis` for published rows
- [ ] `record_id` is unique
- [ ] `metric_type` values are valid
- [ ] `geography_type` values are valid
- [ ] all fact rows join to `geography_reference.csv`
- [ ] all sources are documented in `SOURCES.md`
- [ ] all source IDs are valid and consistent
- [ ] period fields are consistent
- [ ] no impossible room groups
- [ ] no internal machine paths in public files

### Pre-Release Documentation Checks
- [ ] `README.md` matches the actual schema
- [ ] `SCHEMA.md` matches actual columns
- [ ] `METHODOLOGY.md` reflects actual source logic
- [ ] `LIMITATIONS.md` states that the dataset is not live inventory data
- [ ] rights / attribution docs are present and linked

### Pre-Release Rights Checks
- [ ] each source has a terms / license reference
- [ ] attribution text is documented where needed
- [ ] no blanket CC BY claim is made unless audit supports it
- [ ] source uncertainties are documented conservatively

### Publication Checks
- [ ] release tag created
- [ ] manifest hashes updated
- [ ] release notes written
- [ ] dataset version bumped
- [ ] schema version bumped if needed

## Part V — Suggested Release Roadmap

### Release `v0.2.0`
Focus:
- docs overhaul
- rights / provenance clarity
- schema redesign
- geography normalization

### Release `v0.3.0`
Focus:
- source catalog
- geography enrichment
- rental stock companion table

### Release `v0.4.0`
Focus:
- additional official/public companion tables
- stronger machine-readable metadata
- potential citation / packaging improvements

## Final Guidance

Prefer:
- stable semantics
- explicitness
- conservative rights language
- documented limitations

Avoid:
- implicit schema meanings
- vague licensing claims
- mixing incompatible metric types without labels
- publishing metadata that only the maintainers can decode
