# Sources

This file lists the upstream sources used by the public data release and the current rights/provenance posture for each one.

## Source Summary

| `source_id` | Publisher | What this repo uses | Metric type in this repo | Terms pointer | Reuse note |
| --- | --- | --- | --- | --- | --- |
| `nadlan.gov.il` | Israeli government real-estate portal | locality-by-room public rent page values | `average_rent_published` | public site page; no source-specific open license pinned in this patch | yellow |
| `cbs_table49` | Central Bureau of Statistics | Table 4.9 locality and district rent values | `average_rent_published` | CBS end-user license | green/yellow |
| `boi_hedonic` | Bank of Israel | modeled estimates derived from published hedonic-paper coefficients and methodology | `hedonic_rent_estimate` | Bank of Israel terms of use | yellow/red |
| `data.gov.il_locality_registry` | data.gov.il / CBS locality registry | geography names and district metadata used in supporting tables | metadata support only | portal dataset page, labeled `other-open` | yellow |

## `nadlan.gov.il`

- Source name: Israeli government real-estate portal settlement rent page
- Publisher: Government real-estate portal (`nadlan.gov.il`)
- Source artifact used here: public settlement-level rent page and JSON payload behind that page
- URL pattern used in this repo: `https://www.nadlan.gov.il/?id={locality_code}&page=rent&view=settlement_rent`
- Access method: public website and collector-discovered JSON endpoint
- Access date for the validated collector run: 2026-04-21
- Geographic scope in this repo: locality
- Metric type in this repo: `average_rent_published`
- Room-group handling in this repo: canonical buckets `3`, `4`, `5` where present in the source
- Terms / license pointer: no separate, source-specific open-license page was pinned during this patch; downstream users should review the live site footer and current site terms before redistribution
- Attribution baseline: attribute the figures to the Israeli government real-estate portal (`nadlan.gov.il`) and link the locality page or landing page where practical
- Reuse / republication note: this patch treats nadlan-derived rows conservatively because the repo did not pin an explicit open-data license for the current rent page payload
- Open questions:
  - whether the rent page payload is formally covered by an open government-data license
  - whether the current public page terms distinguish between viewing and redistribution

## `cbs_table49`

- Source name: CBS Table 4.9, Average Monthly Prices of Rent (NIS), by residential district, big cities and size group
- Publisher: Central Bureau of Statistics (CBS)
- Source artifact used here: `a4_9_e.xlsx`
- URL used in this release: `https://www.cbs.gov.il/he/publications/madad/doclib/2025/price09a/a4_9_e.xlsx`
- Access method: direct download from the CBS publication library
- Access date for the validated collector run: 2026-04-21
- Geographic scope in this repo: locality and district
- Metric type in this repo: `average_rent_published`
- Room-group handling in this repo: `2`, `3`, `4`, `5+`
- Terms / license URL: `https://www.cbs.gov.il/en/Pages/Enduser-license.aspx`
- Attribution baseline: identify the CBS, the table/product name, the access date, the source URL, and the CBS license page
- Reuse / republication note: the CBS license is materially more explicit than the other sources used here, but downstream users still need to satisfy its attribution conditions and preserve source distinctions
- Open questions:
  - none blocking for this patch, but a future audit should pin the exact publication date for the specific 2025 table artifact

## `boi_hedonic`

- Source name: Bank of Israel hedonic rent paper / appendix coefficients used by the collector fallback model
- Publisher: Bank of Israel
- Source artifact used here: `https://www.boi.org.il/media/yulnw1sl/part-3n.pdf`
- Access method: direct PDF download
- Access date for the validated collector run: 2026-04-21
- Geographic scope in this repo: locality
- Metric type in this repo: `hedonic_rent_estimate`
- Room-group handling in this repo: canonical buckets `2`, `2.5`, `3`, `3.5`, `4`, `4.5`, `5`, `5+`
- Terms / license URL: `https://www.boi.org.il/en/terms-of-use/`
- Attribution baseline: attribute the modeled series to the Bank of Israel paper and identify it as a repository-generated estimate derived from that source, not as a directly published official table
- Reuse / republication note: this repo publishes derived estimates rather than reproducing the paper verbatim, but the underlying source terms are restrictive enough that downstream reuse should be treated carefully and source-specific legal review may still be appropriate
- Open questions:
  - whether all downstream redistribution scenarios for the derived modeled series are comfortably supported without additional permission
  - whether a future release should separate modeled outputs more strongly from directly published official values

## `data.gov.il_locality_registry`

- Source name: `רשימת ישובים בישראל` / Israel locality registry
- Publisher: data.gov.il, based on the CBS locality registry
- Dataset page: `https://data.gov.il/dataset/citiesandsettelments`
- Resource used by the collector: `https://data.gov.il/dataset/3fc54b81-25b3-4ac7-87db-248c3e1602de/resource/5c78e9fa-c2e2-4771-93ff-7f400a12f7ba/download/5c78e9fa-c2e2-4771-93ff-7f400a12f7ba__2026_04_19_03_30_4_207.csv`
- Access method: direct download from data.gov.il CKAN resource metadata
- Access date for the validated collector run: 2026-04-21
- Geographic scope in this repo: supporting geography metadata only
- Terms / license pointer: the dataset is currently labeled `other-open` on data.gov.il; downstream users should review the dataset page and portal terms before assuming broader relicensing rights
- Attribution baseline: attribute the locality metadata to data.gov.il / CBS locality registry
- Reuse / republication note: retained conservatively because the current portal label is not a precise standalone license text
- Open questions:
  - whether the current `other-open` label maps to a stable, source-specific license text appropriate for republication

## Rights Reminder

The source notes above are operational guidance for this repository, not legal advice. Where rights are unclear, this repository intentionally documents uncertainty instead of making a stronger claim.
