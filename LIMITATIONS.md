# Limitations

## Not A Live Market Inventory Dataset

This repository does not measure live asking-rent inventory, active listings, or vacancy. It is a benchmark dataset built from published official or public sources and a modeled fallback series.

## Mixed Metric Types

The main table mixes:

- directly published average rent values
- modeled hedonic rent estimates

These should not be treated as identical measurements. Always inspect `metric_type` and `source_id` before comparison.

## Source Coverage Differences

Not every source covers every geography, room group, or period.

- `boi_hedonic` is much broader geographically
- `nadlan.gov.il` covers only a subset of locality-room combinations in the current release
- `cbs_table49` contributes both localities and district pseudo-geographies

## Interpretation Limits

Users should avoid:

- treating all rows as directly comparable across metric types
- inferring listing volume or market depth from this table
- treating modeled rows as if they were directly published official observations
- making overly precise causal claims from a compiled benchmark table alone

## Temporal Limits

This repository has a release date and separate source periods. Those are not the same thing.

- the patched repository state was prepared on `2026-04-22`
- most rows refer to `2025`
- quarterly rows should not be blindly merged with annual rows

## Geography Limits

The fact table contains both locality and district rows.

- district rows are explicit in the patched schema
- `locality_crosswalk.csv` does not cover district rows
- `geography_reference.csv` is the canonical join table for all published geographies

## Rights And Source Limits

The repository intentionally uses a conservative rights posture. Source-specific terms may apply, and the repository does not claim to override them.

See:

- [DATA-LICENSE.md](DATA-LICENSE.md)
- [SOURCES.md](SOURCES.md)
- [ATTRIBUTION.md](ATTRIBUTION.md)
