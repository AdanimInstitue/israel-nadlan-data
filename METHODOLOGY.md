# Methodology

## Source Roles

- `nadlan.gov.il`: locality observations from the public government portal
- `cbs_table49`: direct published CBS benchmark observations
- `boi_hedonic`: modeled fallback estimates derived from published Bank of Israel source material
- `data.gov.il`: geography metadata support

## Observation Semantics

The fact table is source-aware. Different sources may coexist for the same geography and room bucket. Users should check `source_id` and `metric_type` before comparing rows.

## Geography Modeling

- localities use CBS locality codes as `geography_id`
- district rows use explicit district identifiers
- all fact geographies must appear in `geography_reference.csv`

## Room Groups

The release uses normalized room buckets such as `2`, `2.5`, `3`, `3.5`, `4`, `4.5`, and `5+`.

## Period Modeling

- annual rows use `period_type = annual`
- quarterly rows use `period_type = quarterly`
- the release keeps explicit `period_year`, `period_quarter`, and `period_label`

## Reproducibility

This repository is self-describing as a public data product. Future refreshes depend on the public collector project, but release consumers do not need that repository open to understand the published files.
