# Methodology

## Scope

This repository publishes geography reference and locality context only. It does not publish rent benchmark observations, modeled estimates, or a source inventory.

## Source Roles

- `cbs_table49`: public geography reference support
- `data.gov.il`: locality metadata support

## Geography Modeling

- locality rows use CBS locality codes as `geography_id`
- district rows use explicit district identifiers
- the geography table is the canonical join point for public reference work

## Reproducibility

This repository is self-describing as a public data product. Release consumers do not need any private workspace to understand the published files.
