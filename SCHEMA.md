# Schema

## Published Tables

### `data/current/geography_reference.csv`

Canonical geography reference table.

### `data/current/locality_crosswalk.csv`

Locality context and compatibility table.

## Enums

- `geography_type`: `locality`, `district`

## Key Relationships

- `locality_crosswalk.csv.locality_code` supports locality lookups
- `geography_reference.csv` is the canonical join point for geography identifiers

## Machine-Readable Dictionary

The release also ships [`metadata/data_dictionary.csv`](metadata/data_dictionary.csv) for file-by-file column definitions.
