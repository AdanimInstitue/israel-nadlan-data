# Patch Plan Overview and Execution Plan

## Purpose

This patch plan is for turning the current `israel-rent-data` repository from a valid first public snapshot into a stable, legally careful, researcher-friendly public dataset.

The current `v0.1.0` release is a good MVP because it is:
- public
- versioned
- release-tagged
- accompanied by a machine-readable manifest
- linked to a specific validated collector run and collector commit

However, it is not yet a mature public data product. The main gaps are:
- ambiguous dataset licensing / source-rights communication
- under-specified schema
- weak end-user documentation
- mixed geography levels in one table without explicit modeling
- partially redundant and partially empty value columns
- insufficient provenance fields for downstream auditing

## Current Observed Repository State

The current repository root contains:
- `README.md`
- `manifest.json`
- `rent_benchmarks.csv`
- `locality_crosswalk.csv`

Observed structural issues in the published data product:
- `median_rent_nis` is entirely empty
- `observations_count` is entirely empty
- `rent_nis` carries the actual numeric value across sources
- district-level rows are present in `rent_benchmarks.csv` but not modeled explicitly as a separate geography type
- `locality_crosswalk.csv` is locality-only and does not cover the district pseudo-codes present in the fact table
- the public README is too thin for external users
- provenance currently exposes an internal local filesystem path
- the data repo does not yet provide a clear data-specific license or source-rights explanation

## Objectives

The patch should achieve all of the following:

1. Make the repository self-explanatory to an external researcher.
2. Make source-by-source rights and attribution obligations explicit.
3. Redesign the schema so each row has one clear numeric meaning.
4. Model geography, metric type, and period explicitly.
5. Preserve the repository’s provenance strengths and improve them.
6. Add enough QA and release discipline that future snapshots are repeatable and auditable.

## Non-Goals

This patch is **not** primarily about:
- building a brand new ingestion pipeline
- switching to private/commercial sources
- adding scraping from Yad2 / Madlan
- introducing speculative modeled enrichments not grounded in official/public data
- promising a blanket CC BY license before source-rights review is completed

## Recommended Work Phases

### Phase 1 — Repository Productization
Create the missing repository-level documentation and rights files:
- `DATA-LICENSE.md`
- `SOURCES.md`
- `ATTRIBUTION.md`
- `SCHEMA.md`
- `METHODOLOGY.md`
- `QA.md`
- `LIMITATIONS.md`

Update:
- `README.md`
- `manifest.json` schema / contents as needed

### Phase 2 — Schema Repair
Redesign the main fact table so that:
- one row = one geography × one room bucket × one metric × one period × one source observation
- exactly one primary numeric value field is used
- geography level is explicit
- metric type is explicit
- period semantics are explicit

### Phase 3 — Metadata Expansion
Add:
- source URLs
- source release/access metadata
- source license / terms references
- provenance references
- quality flags
- suppression / missingness semantics

### Phase 4 — Geography Normalization
Normalize geography handling by either:
- introducing a general `geography_reference.csv`, or
- splitting district-level rows into a separate benchmark file

The preferred path is to add `geography_reference.csv` and keep `locality_crosswalk.csv` only if backward compatibility is needed.

### Phase 5 — Release Hardening
Add a repeatable release checklist and ensure:
- no internal machine paths leak into public artifacts
- all published files have hashes
- documentation and schema stay in sync
- release tags correspond to a documented schema version

### Phase 6 — Optional Expansion
After the patch lands, add additional official/public companion tables, especially:
- rental stock / ownership context
- sale-price context
- richer geography metadata

## Priority Order

Implement in this order:

1. rights / licensing / provenance docs
2. schema redesign
3. README and documentation overhaul
4. geography normalization
5. QA and release checklist
6. optional companion tables

## Definition of Done

The patch is done only when all of the following are true:

### A. Legal / Rights Clarity
- The repo contains a data-specific rights document.
- Every upstream source used in the release is listed in `SOURCES.md`.
- Each source has a terms / license reference and an internal reuse note.
- The repo does not falsely imply a blanket CC BY grant unless the audit supports it.

### B. Schema Clarity
- The main fact table has a single primary numeric value column.
- `metric_type` is explicit.
- `geography_type` is explicit.
- period fields are explicit and documented.
- null semantics are documented.

### C. Documentation Quality
- `README.md` explains what the dataset is, what one row means, and what users should not infer.
- `SCHEMA.md` documents every column.
- `METHODOLOGY.md` explains source priority and normalization rules.
- `LIMITATIONS.md` explains known coverage gaps and interpretation limits.
- `QA.md` explains release validation.

### D. Provenance
- `manifest.json` records enough to audit the release.
- no internal local filesystem paths are exposed
- checksums remain available
- collector commit / run metadata remain linkable

### E. Usability
- An external researcher can understand and use the data without reading the collector code.
- An external agent can answer "what is this row?" and "what rights apply?" from the data repo alone.

## Recommended Deliverable Set

Minimum deliverables for the patch:
- updated `README.md`
- `DATA-LICENSE.md`
- `SOURCES.md`
- `ATTRIBUTION.md`
- `SCHEMA.md`
- `METHODOLOGY.md`
- `QA.md`
- `LIMITATIONS.md`
- updated `manifest.json`
- redesigned fact table and normalized geography reference table

## Implementation Notes for the Agent

- Prefer clarity over backward compatibility where the current schema is misleading.
- If backward compatibility is preserved, document it explicitly.
- Do not invent legal conclusions; where uncertain, document uncertainty conservatively.
- Do not claim upstream data is relicensable under CC BY unless the source audit actually supports that claim.
- Where a source mixes officially published figures and modeled estimates, preserve that distinction in the schema.

## Suggested First Patch Target

The first implementation pass should aim for:
- repository docs + rights docs
- schema repair
- geography normalization
- manifest cleanup

Leave broader data expansion for a second pass if needed.
