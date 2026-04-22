# Methodology

This file explains how the public dataset is structured and how the released observations were normalized.

## Source Overview

### `nadlan.gov.il`

Used for locality-level rent values published on the public settlement rent page. In the current collector and release, these rows are treated as `average_rent_published` because that matches the live payload shape observed by the collector.

### `cbs_table49`

Used for published CBS Table 4.9 rent values. This source contributes both locality rows and district rows.

### `boi_hedonic`

Used for modeled fallback estimates derived from Bank of Israel source material. These rows are explicit modeled estimates and are not treated as directly published official values.

### `data.gov.il_locality_registry`

Used only for supporting geography metadata such as locality names and district labels. It is not part of the main fact-table source mix.

## Source Priority And Public Release Semantics

The collector prioritizes more direct official/public locality observations before modeled fallback values. However, the public data repository is not a single-source collapsed table. It publishes the source-specific observations that result from collection and fallback logic.

That means:

- different sources may coexist for the same geography and year
- not every source covers every geography or room group
- `metric_type` and `source_id` must be checked before comparison

## Metric Typing

This release uses explicit metric typing:

- `average_rent_published`: directly published average rent value from an upstream source
- `hedonic_rent_estimate`: repository-generated estimate derived from Bank of Israel source material

The current patched release does not publish any `median_rent_published` rows because the shipped `v0.1.0` snapshot did not contain a reliable, populated median series in the public table.

## Geography Normalization

The fact table uses `geography_id` plus `geography_type`.

- locality rows keep their CBS locality code as `geography_id`
- district rows use explicit pseudo-codes such as `DIST_TA`
- all fact-table geographies must exist in `geography_reference.csv`

The new geography reference file exists because the old `locality_crosswalk.csv` was locality-only and silently failed to cover the six district rows coming from CBS Table 4.9.

## Room Group Normalization

Room groups are normalized into the canonical string buckets used in the release:

- `2`
- `2.5`
- `3`
- `3.5`
- `4`
- `4.5`
- `5`
- `5+`

Legacy formatting such as `2.0` was normalized to `2`.

## Period Modeling

The patched schema separates period semantics into:

- `period_type`
- `period_year`
- `period_quarter`
- `period_label`

Current release behavior:

- `boi_hedonic` rows are modeled as annual observations for `2025`
- `nadlan.gov.il` and `cbs_table49` rows are modeled as quarterly observations where a quarter is present in the release

The release does not infer missing quarter values where the source row did not provide one.

## Missing Data And Suppression

Current release rules:

- `value_nis` is always populated for published rows
- `observations_count` remains null because the shipped release did not carry usable counts through
- `suppressed` is always `false` in this patched snapshot
- `source_release_date` and `source_accessed_at` are left null where the public release did not pin reliable per-row values

## Transformation Notes

This patch intentionally makes breaking changes for clarity:

- removes dead value columns from `v0.1.0`
- renames the primary numeric field to `value_nis`
- makes metric type and geography type explicit
- replaces implicit period semantics with explicit period columns
- introduces a canonical geography dimension

## Reproducibility Notes

This repository is meant to be understandable without reading collector code, but not every transformation artifact is reproducible from this repo alone.

What this repo provides directly:

- the released CSVs
- schema documentation
- rights and attribution notes
- public-safe provenance metadata in `manifest.json`

What still depends on the collector repo:

- live source retrieval
- validated run logs
- collector implementation details
- future refreshes or re-runs against upstream sites
