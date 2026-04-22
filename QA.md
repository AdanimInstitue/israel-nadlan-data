# QA

## Release Checks

- `geography_id` values are unique in `geography_reference.csv`
- `locality_code` values are unique in `locality_crosswalk.csv`
- `geography_type` values are valid
- required reference columns are present
- manifest file counts match the published CSVs
- metadata paths are repository-relative
- legacy benchmark and source-inventory files are absent

## Validation Command

```bash
python scripts/validate_release.py --check
```

## Known Warnings

- the release is reference-only
- rights and attribution notes remain source-specific
- locality context is not a substitute for the canonical geography table
