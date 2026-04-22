# Data License And Rights Posture

This file describes the rights posture for the `israel-rent-data` repository. It does not govern the separate collector code repository.

## Scope

This repository contains:

- repository-authored documentation
- repository-authored release metadata and schema documentation
- original normalization metadata and geography-reference structure
- source-derived tabular data compiled from upstream official or public sources

Those categories should not be treated as having identical rights.

## Repository-Authored Materials

Unless otherwise noted, the repository-authored documentation and original release metadata in this repository are made available under the Creative Commons Attribution 4.0 International license (`CC BY 4.0`).

This statement applies to repository-authored materials such as:

- `README.md`
- `SCHEMA.md`
- `METHODOLOGY.md`
- `QA.md`
- `LIMITATIONS.md`
- `ATTRIBUTION.md`
- repository-authored portions of `manifest.json`
- repository-authored normalization notes and migration notes

It does not by itself grant rights over source-derived rows or over third-party material embedded in upstream sources.

## Source-Derived Data

The tabular data in:

- `rent_benchmarks.csv`
- `geography_reference.csv`
- `locality_crosswalk.csv`

contains values, labels, or structured information derived from upstream official or public sources. Those materials remain subject to the terms, conditions, attribution obligations, and any other applicable restrictions of the respective upstream publishers.

This repository does not claim that the full combined dataset can be relicensed under a single blanket open-data license. In particular, this repository does not claim a blanket `CC BY` grant over all source-derived rows.

## No Blanket Override

No repository-level statement in this file is intended to override:

- upstream source terms
- source-specific attribution requirements
- third-party rights retained by an upstream publisher
- applicable statutory restrictions

## Where To Check Source Terms

Use these files together:

- [SOURCES.md](SOURCES.md)
- [ATTRIBUTION.md](ATTRIBUTION.md)

These files document the current source inventory, known terms pointers, attribution language, and open questions.

## User Responsibility

Downstream users are responsible for determining whether their intended reuse complies with:

- the relevant upstream terms
- applicable copyright and database-rights rules
- attribution obligations
- any other legal requirements

This repository provides documentation and provenance, not legal advice.

## Current Posture Summary

The current release uses a conservative, source-aware posture:

- repo-authored text and metadata: reusable under `CC BY 4.0`
- source-derived compiled tables: source-specific rights still apply
- unclear or incomplete source-rights questions: documented conservatively instead of guessed

Future relicensing of the full combined data product should happen only after a source-by-source audit confirms that a broader licensing claim is supportable.
