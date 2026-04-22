# Schema

This file documents the released data files for the patched repository state.

## File Roles

| File | Role | Canonical? |
| --- | --- | --- |
| `rent_benchmarks.csv` | Main fact table | yes |
| `geography_reference.csv` | Canonical geography dimension | yes |
| `locality_crosswalk.csv` | Legacy locality-only lookup | no, compatibility-only |

## `rent_benchmarks.csv`

One row is one geography x room group x metric type x period x source observation.

### Column Dictionary

| Column | Type | Required | Description | Allowed values / examples |
| --- | --- | --- | --- | --- |
| `record_id` | string | yes | Stable row identifier for this published release schema. | `cbs_table49__DIST_TA__5plus__average_rent_published__2025-Q2` |
| `geography_id` | string | yes | Canonical geography key used for joins. | locality code like `5000`, district pseudo-code like `DIST_TA` |
| `geography_type` | enum | yes | Geography level. | `locality`, `district` |
| `geography_name_he` | string | yes | Hebrew geography label used in the release. | `מחוז תל אביב` |
| `geography_name_en` | string | yes | English geography label used in the release. | `Tel Aviv District` |
| `room_group` | string | yes | Canonical room bucket. | `2`, `2.5`, `3`, `3.5`, `4`, `4.5`, `5`, `5+` |
| `metric_type` | enum | yes | Meaning of `value_nis`. | `average_rent_published`, `hedonic_rent_estimate` |
| `value_nis` | number | yes | Primary rent value in Israeli shekels. | `5100` |
| `currency` | string | yes | Currency code for the value column. | `ILS` |
| `period_type` | enum | yes | Period semantics. | `annual`, `quarterly` |
| `period_year` | integer | yes | Observation year. | `2025` |
| `period_quarter` | integer or null | no | Quarter number when relevant. | `1`, `2`, null |
| `period_label` | string | yes | Human-readable period label. | `2025`, `2025-Q2` |
| `source_id` | string | yes | Canonical source identifier. | `boi_hedonic`, `nadlan.gov.il`, `cbs_table49` |
| `source_series_id` | string | yes | Source or series identifier used inside this release. | `table_4_9_average_monthly_prices_of_rent` |
| `source_url` | string | yes | Source page or artifact URL associated with the row. | nadlan locality page, CBS table URL, BOI PDF URL |
| `source_release_date` | date or null | no | Upstream publication date if pinned in the release. | null in this patch |
| `source_accessed_at` | datetime or null | no | Source access timestamp if tracked per row. | null in this patch |
| `is_official_published_value` | boolean | yes | Whether the row is directly published by the upstream source. | `true`, `false` |
| `is_modeled_value` | boolean | yes | Whether the row is modeled rather than directly published. | `true`, `false` |
| `suppressed` | boolean | yes | Whether the row is intentionally published without a value. | always `false` in this release |
| `observations_count` | integer or null | no | Underlying count if published and carried through. | null in this release |
| `qa_status` | enum | yes | Release QA disposition for the row. | `pass`, `warn`, `fail_excluded` |
| `notes` | string or null | no | Release note for unusual or source-specific context. | `nadlan settlement rent page JSON` |

### Enum Notes

- `metric_type`
  - `average_rent_published`: directly published average rent value from an upstream source
  - `hedonic_rent_estimate`: modeled estimate generated from Bank of Israel source material
- `geography_type`
  - `locality`
  - `district`
- `period_type`
  - `annual`
  - `quarterly`
- `qa_status`
  - `pass`: row passed release checks
  - `warn`: row published with a documented warning
  - `fail_excluded`: row failed checks and was excluded from publication

### Null Semantics

- `value_nis` must not be null for published rows.
- `period_quarter` is null for annual rows.
- `source_release_date` and `source_accessed_at` are null when the public release does not pin a reliable per-row value.
- `observations_count` is null when the source does not publish or the release does not carry through that count.
- Empty strings from `v0.1.0` were normalized to null-equivalent blank fields in CSV output.

## `geography_reference.csv`

Canonical geography dimension for every `geography_id` used in `rent_benchmarks.csv`.

### Column Dictionary

| Column | Type | Required | Description | Examples |
| --- | --- | --- | --- | --- |
| `geography_id` | string | yes | Join key used by fact tables. | `5000`, `DIST_TA` |
| `geography_type` | enum | yes | Geography level. | `locality`, `district` |
| `locality_code` | string or null | no | Original locality code when the row is a locality. | `5000` |
| `district_code` | string or null | no | Canonical district code when the row is a district. | `TEL_AVIV` |
| `geography_name_he` | string | yes | Hebrew geography label. | `תל אביב-יפו`, `מחוז תל אביב` |
| `geography_name_en` | string | yes | English geography label. | `TEL AVIV-YAFO`, `Tel Aviv District` |
| `district_he` | string or null | no | Parent district name in Hebrew. | `מחוז תל אביב` |
| `district_en` | string or null | no | Parent district name in English. | `Tel Aviv` |
| `population_approx` | integer or null | no | Approximate population when carried through from the locality registry. | null in many current rows |
| `source` | string | yes | Supporting metadata source for the geography row. | `data.gov.il`, `cbs_table49` |
| `is_active` | boolean | yes | Convenience flag for active rows in the reference table. | `true` |

## `locality_crosswalk.csv`

Legacy compatibility file retained for one release cycle after the schema redesign.

### Important Scope Note

- locality-only
- not the canonical geography table for the full dataset
- does not contain district pseudo-geographies that appear in `rent_benchmarks.csv`

### Columns

| Column | Description |
| --- | --- |
| `locality_code` | Locality code carried over from `v0.1.0` |
| `locality_name_he` | Hebrew locality name |
| `locality_name_en` | English locality name |
| `district_he` | Hebrew district name |
| `district_en` | English district name |
| `population_approx` | Approximate population when available |
| `source` | Supporting metadata source |

## Key Relationships

- `rent_benchmarks.csv.geography_id` -> `geography_reference.csv.geography_id`
- `locality_crosswalk.csv.locality_code` is a partial compatibility lookup for locality rows only

## Migration Notes From `v0.1.0`

| `v0.1.0` column | New field |
| --- | --- |
| `locality_code` | `geography_id` |
| `locality_name_he` | `geography_name_he` |
| `locality_name_en` | `geography_name_en` |
| `rent_nis` | `value_nis` |
| `source` | `source_id` |
| `quarter` | `period_quarter` |
| `year` | `period_year` |

Removed fields:

- `median_rent_nis`
- `avg_rent_nis`
- `rent_nis`

Added fields:

- `record_id`
- `geography_type`
- `metric_type`
- `currency`
- `period_type`
- `period_label`
- `source_series_id`
- `source_url`
- `source_release_date`
- `source_accessed_at`
- `is_official_published_value`
- `is_modeled_value`
- `suppressed`
- `qa_status`
