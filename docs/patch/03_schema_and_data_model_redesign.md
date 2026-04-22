# Schema and Data Model Redesign

## Design Goal

Redesign the published dataset so that each row has one unambiguous meaning and the schema is stable enough for external research use.

## Problems in the Current Published Schema

Current observed issues:
- multiple value columns exist (`median_rent_nis`, `avg_rent_nis`, `rent_nis`) but only `rent_nis` is actually populated across the release
- `median_rent_nis` is empty, which invites misinterpretation
- `observations_count` is empty, which suggests unfinished metadata
- geography level is implicit instead of explicit
- district rows are mixed into the same file without a dedicated geography model
- period representation is too thin for mixed annual / quarterly source data
- the schema does not explicitly say whether a value is a direct official published figure or a modeled estimate

## Recommended Design Principles

1. One row = one observation.
2. One primary numeric value column.
3. Metric meaning must be explicit.
4. Geography type must be explicit.
5. Period semantics must be explicit.
6. Missingness and suppression must be explicit.
7. Source and rights metadata must be machine-readable.

## Recommended Main Fact Table

Keep the file name `rent_benchmarks.csv`, but redesign the columns to the following:

### Required Columns

| Column | Type | Description |
|---|---|---|
| `record_id` | string | Stable unique row identifier for the published dataset. |
| `geography_id` | string | Canonical geography key. May be locality code or a district pseudo-code. |
| `geography_type` | enum | One of: `locality`, `district`. |
| `geography_name_he` | string | Hebrew geography name as published / normalized. |
| `geography_name_en` | string | English geography name as published / normalized. |
| `room_group` | string | Canonical room bucket, e.g. `2`, `2.5`, `3`, `3.5`, `4`, `4.5`, `5`, `5+`, `all`. |
| `metric_type` | enum | One of: `median_rent_published`, `average_rent_published`, `hedonic_rent_estimate`. |
| `value_nis` | number | Numeric rent value in NIS. |
| `currency` | string | Always `ILS` for now. |
| `period_type` | enum | One of: `annual`, `quarterly`, `monthly`, `other_published_period`. |
| `period_year` | integer | Year of the observation. |
| `period_quarter` | integer/null | Quarter number when relevant. |
| `period_label` | string | Human-readable label, e.g. `2025`, `2025-Q2`. |
| `source_id` | enum/string | Canonical source key, e.g. `boi_hedonic`, `nadlan_gov_il`, `cbs_table49`. |
| `source_series_id` | string/null | Source table / series identifier when applicable. |
| `source_url` | string | URL to the specific source page / table / dataset. |
| `source_release_date` | date/null | Publication or effective date of the source artifact, if available. |
| `source_accessed_at` | datetime/null | Access timestamp used for the release, if tracked. |
| `is_official_published_value` | boolean | `true` if directly published as an official figure in the upstream source. |
| `is_modeled_value` | boolean | `true` if this value is a modeled / estimated value rather than a directly published summary figure. |
| `suppressed` | boolean | `true` if published but suppressed for quality / privacy / small-cell reasons. |
| `observations_count` | integer/null | Underlying count if officially available and publishable. |
| `qa_status` | enum | One of: `pass`, `warn`, `fail_excluded`. For published rows, normally `pass` or `warn`. |
| `notes` | string/null | Human-readable release note for unusual cases. |

### Optional Columns

| Column | Type | Description |
|---|---|---|
| `value_lower_nis` | number/null | Optional lower bound if a source publishes ranges or confidence bands. |
| `value_upper_nis` | number/null | Optional upper bound if available. |
| `normalization_version` | string | Version of normalization logic used for this row. |
| `source_license_id` | string/null | Foreign key to a source-license registry if implemented. |

## Columns to Remove or Deprecate

### Remove
- `median_rent_nis`
- `avg_rent_nis`
- `rent_nis` (replace with `value_nis`)

Reason:
The current three-column pattern is not working in practice and encourages misuse.

### Rename / Transform
- `locality_code` → `geography_id`
- `source` → `source_id`
- `quarter` → `period_quarter`
- `year` → `period_year`

### Preserve Semantically
- `locality_name_he` / `locality_name_en` become geography names
- `notes` can remain

## Metric-Type Mapping Rules

The migration logic should map current sources as follows:

- `boi_hedonic` → `metric_type = hedonic_rent_estimate`
- `nadlan.gov.il` → `metric_type = median_rent_published`
- `cbs_table49` → `metric_type = average_rent_published`

Also set:
- `is_modeled_value = true` only for modeled sources such as `boi_hedonic`
- `is_official_published_value = true` for directly published official source summaries

## Geography Modeling

### Preferred Approach
Introduce a canonical `geography_reference.csv` with the following columns:

| Column | Type | Description |
|---|---|---|
| `geography_id` | string | Canonical key used in fact tables. |
| `geography_type` | enum | `locality`, `district`. |
| `locality_code` | string/null | Original locality code where applicable. |
| `district_code` | string/null | Optional district code. |
| `geography_name_he` | string | Hebrew name. |
| `geography_name_en` | string | English name. |
| `district_he` | string/null | Parent district name if applicable. |
| `district_en` | string/null | Parent district name if applicable. |
| `population_approx` | integer/null | Population metadata if retained. |
| `source` | string | Metadata source for the geography row. |
| `is_active` | boolean | Optional convenience field. |

### Locality Crosswalk Policy
If `locality_crosswalk.csv` is kept:
- document it as locality-only
- state that it is **not** the canonical geography table for the full dataset

## Period Modeling

The dataset currently mixes:
- annual source observations
- quarterly source observations

Recommended fields:
- `period_type`
- `period_year`
- `period_quarter`
- `period_label`

Optional but recommended:
- `period_start_date`
- `period_end_date`

## Missingness and Suppression Semantics

Document these exact rules:

- `value_nis` must never be null for published rows.
- `observations_count` may be null if the source does not publish it.
- `suppressed = true` means a row exists as a known combination but the value is intentionally not published.
- `notes` should explain suppression or unusual transformations when relevant.
- Empty strings should not be used instead of nulls.

## Record Identifier

Add a stable `record_id`, for example:

```text
{source_id}__{geography_id}__{room_group}__{metric_type}__{period_label}
```

Use a normalized, deterministic format.

## Suggested Companion Tables

### `geography_reference.csv`
Canonical dimension table.

### `source_catalog.csv` (optional but recommended)
Columns:
- `source_id`
- `source_name`
- `publisher`
- `source_url`
- `terms_url`
- `license_summary`
- `attribution_text`
- `metric_notes`

### `release_summary.json` (optional)
Public-safe derived release summary.

## Migration Guidance from v0.1.0

### Old → New

| Old Column | New Column |
|---|---|
| `locality_code` | `geography_id` |
| `locality_name_he` | `geography_name_he` |
| `locality_name_en` | `geography_name_en` |
| `rent_nis` | `value_nis` |
| `source` | `source_id` |
| `quarter` | `period_quarter` |
| `year` | `period_year` |

### Derived New Columns
- `record_id`
- `geography_type`
- `metric_type`
- `currency`
- `period_type`
- `period_label`
- `source_url`
- `is_official_published_value`
- `is_modeled_value`
- `suppressed`
- `qa_status`

## Acceptance Criteria

The redesign is complete when:
- every published row has one clear metric meaning
- no dead / misleading value columns remain
- geography type is explicit
- metric type is explicit
- the main fact table can be joined cleanly to a canonical geography reference table
