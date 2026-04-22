# Attribution Guidance

This file provides reusable attribution language for this repository. It is a baseline, not a substitute for checking upstream source terms.

## Short Attribution

Recommended short-form attribution for dashboards, notebooks, and quick visualizations:

> Source: Adanim Institute, `israel-rent-data` (release candidate for v0.2.0), compiling and normalizing official/public Israeli rent indicators from multiple upstream sources. Source-specific terms and attribution obligations remain applicable.

## Full Attribution

Recommended long-form attribution for reports, research papers, and derived datasets:

> This analysis uses the Adanim Institute `israel-rent-data` repository, release candidate for v0.2.0, which compiles and normalizes benchmark rent observations from multiple official or public upstream Israeli sources, including the Israeli government real-estate portal (`nadlan.gov.il`), Central Bureau of Statistics Table 4.9, Bank of Israel source material used for modeled hedonic estimates, and supporting locality metadata from data.gov.il / CBS. The repository documents source-specific terms and attribution notes in `SOURCES.md` and does not claim to override upstream rights.

## Source-Specific Notes

- `nadlan.gov.il`: identify the portal and, where practical, link the locality page or landing page used for the figure.
- `cbs_table49`: include the CBS product/table name, the access date, the source URL, and the CBS license page.
- `boi_hedonic`: identify the series as a modeled estimate derived from Bank of Israel source material, not as a directly published official benchmark table.
- `data.gov.il_locality_registry`: attribute geography metadata to data.gov.il / CBS locality registry when reusing those labels in a supporting dimension table.

## Reuse Reminder

Downstream users remain responsible for complying with upstream source terms. This repository-level attribution guidance does not erase any source-specific conditions.
