# QA

## Release Checks

- `record_id` values are unique
- `value_nis` is present for all published fact rows
- `geography_type` values are valid
- `metric_type` values are valid
- every fact geography joins to `geography_reference.csv`
- manifest file counts match the published CSVs
- metadata paths are repository-relative

## Validation Command

```bash
python scripts/validate_release.py --check
```

## Known Warnings

- direct and modeled values coexist in the same release
- source-specific rights positions differ
- most rows in this release are for 2025
