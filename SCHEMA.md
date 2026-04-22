# Schema

## Published Tables

### `data/current/rent_benchmarks.csv`

Main benchmark fact table.

Key columns:

- `record_id`
- `geography_id`
- `geography_type`
- `geography_name_he`
- `geography_name_en`
- `room_group`
- `metric_type`
- `value_nis`
- `currency`
- `period_type`
- `period_year`
- `period_quarter`
- `period_label`
- `source_id`
- `source_series_id`
- `source_url`
- `source_release_date`
- `source_accessed_at`
- `is_official_published_value`
- `is_modeled_value`
- `suppressed`
- `observations_count`
- `qa_status`
- `notes`

### `data/current/geography_reference.csv`

Canonical geography dimension covering every `geography_id` used in the fact table.

### `data/current/locality_crosswalk.csv`

Locality-only compatibility artifact retained for convenience. It is not the canonical geography table for the full release.

## Enums

- `geography_type`: `locality`, `district`
- `metric_type`: `average_rent_published`, `hedonic_rent_estimate`
- `period_type`: `annual`, `quarterly`

## Units

- `value_nis`: Israeli new shekels per month

## Key Relationships

- `rent_benchmarks.csv.geography_id` joins to `geography_reference.csv.geography_id`
- `locality_crosswalk.csv.locality_code` covers locality rows only

## Machine-Readable Dictionary

The release also ships [`metadata/data_dictionary.csv`](metadata/data_dictionary.csv) for file-by-file column definitions.
