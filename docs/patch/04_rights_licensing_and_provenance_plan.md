# Rights, Licensing, and Provenance Plan

## Purpose

This document defines how to handle licensing, source-rights communication, attribution, and provenance for the public dataset repository.

## Core Position

Do **not** assume that because the repository authors created the packaging, the entire combined dataset can automatically be relicensed under a blanket CC BY license.

The repository should distinguish between:
1. repository-authored materials
2. normalized / compiled source-derived data
3. upstream source rights and terms

## Recommended Licensing Posture for the Next Release

### Immediate Recommendation
Use a **conservative, source-aware posture** until a source-by-source audit is complete.

That means:
- do not state that the full combined data table is licensed under blanket CC BY
- do not imply that all numeric rows are freely relicensable under your chosen license
- do clearly grant rights over repository-authored text and original metadata where appropriate

### What Can Be Licensed More Confidently
Usually safe to license separately, if desired:
- repository-authored documentation
- manually written methodology text
- repo-authored release notes
- repo-authored schema docs
- repo-authored attribution templates
- repo-authored manifest structure
- repo-authored normalization notes
- repo-authored crosswalk enrichments to the extent they are original

### What Must Remain Source-Aware
- source-derived data tables
- rows that compile values from official/public sources with their own terms
- any republished source-specific labels, notes, or other nontrivial textual content

## Recommended `DATA-LICENSE.md` Structure

The file should contain these sections:

### 1. Scope
Explain that this file governs the data repository contents, not the collector code repository.

### 2. Repository-Authored Materials
State what rights are granted over:
- documentation
- original metadata
- release notes
- schema docs
- provenance summaries

### 3. Source-Derived Data
State that source-derived data remains subject to the terms, conditions, and attribution requirements of the respective upstream sources.

### 4. No Blanket Override
State explicitly that no repository-level license is intended to override upstream restrictions or attribution obligations.

### 5. Source Inventory Pointer
Point users to `SOURCES.md` and `ATTRIBUTION.md`.

### 6. User Responsibility
State that downstream users are responsible for ensuring their use complies with applicable upstream source terms and law.

## Recommended `SOURCES.md` Structure

Create one section per source, for example:

```md
## boi_hedonic
- Publisher:
- Source artifact:
- URL:
- Access method:
- Geographic scope:
- Period coverage:
- Metric type in this repository:
- Upstream terms / license URL:
- Attribution requirement:
- Internal reuse assessment:
- Open questions:
```

Required fields per source:
- `source_id`
- source name
- publisher
- exact URL
- terms / license URL
- access date
- access method
- whether the repo uses direct values, modeled values, or derived aggregates
- required attribution language if known
- internal reuse note:
  - `green`
  - `yellow`
  - `red`
  or a textual equivalent

## Recommended `ATTRIBUTION.md` Structure

Provide reusable attribution blocks:

### Short Attribution
For dashboards / quick reuse.

### Full Attribution
For reports, research papers, and derived datasets.

### Source-Specific Notes
List any source-specific wording or constraints.

### Example Wording
Include a generic example such as:

> This dataset compiles and normalizes official/public Israeli housing-rent indicators from multiple upstream sources. Source-specific rights, attribution obligations, and terms remain applicable. See `SOURCES.md` and `DATA-LICENSE.md`.

Do not assert that this wording is legally sufficient for every source; label it as a recommended baseline.

## Provenance Requirements

The public data repo should preserve provenance strongly but safely.

### Required Provenance Fields
In `manifest.json`, include:
- `schema_version`
- `release_version`
- `published_at`
- `data_repo`
- `collector_repo`
- `collector_commit`
- `collector_run_id` or equivalent public-safe identifier
- `validated_command`
- file hashes
- file row counts
- source mix
- source inventory
- source terms references
- build notes

### What Not to Expose
Do **not** publish:
- local absolute filesystem paths
- workstation usernames
- secrets
- ephemeral temp paths that are not meaningful outside the build environment

Replace any local path with:
- a run ID
- a relative path
- or a collector artifact reference

## Rights / Provenance Metadata in Data Tables

Recommended additions to main fact tables:
- `source_id`
- `source_url`
- `source_series_id`
- `source_release_date`
- optional `source_license_id`

Recommended companion table:
- `source_catalog.csv`

## Recommended License / Terms Audit Process

Before any future blanket CC BY claim, the agent should produce a source audit matrix with these columns:

| Column | Meaning |
|---|---|
| `source_id` | Canonical source key |
| `publisher` | Publishing body |
| `artifact_url` | Specific page / table used |
| `terms_url` | Specific terms / license page |
| `terms_checked_at` | Date checked |
| `explicit_open_license` | yes / no / unclear |
| `attribution_required` | yes / no / unclear |
| `redistribution_allowed` | yes / no / unclear |
| `relicense_under_cc_by` | yes / no / unclear |
| `notes` | Human review notes |

## Recommended Interim Language for README

Until the audit is complete, README language should say something like:

- the repository publishes normalized public/official housing-rent benchmark data
- source-specific terms and attribution obligations may apply
- users should consult `DATA-LICENSE.md`, `SOURCES.md`, and `ATTRIBUTION.md`
- the repository does not claim to override upstream rights

## Decision Gate for Future CC BY Release

A future blanket CC BY release should happen only if all of the following are true:
- each upstream source has been audited
- redistribution rights are confirmed or risk-accepted
- attribution obligations are documented
- no upstream source blocks the relicensing posture
- the repository owners are comfortable making a uniform licensing representation

If this is not true, keep the source-aware posture.

## Acceptance Criteria

This plan is implemented when:
- the repo stops implying undocumented blanket reuse rights
- users can see which sources apply to which rows
- provenance is auditable and public-safe
- a future relicensing decision can be made from explicit evidence rather than assumption
