# Documentation Pack Specification

## Goal

This document specifies the exact content that the public data repository documentation should contain after the patch.

The repository documentation should allow an external researcher, journalist, civic-tech user, or AI agent to answer all of the following without inspecting collector code:
- What is this dataset?
- What does one row mean?
- Which sources are included?
- What is modeled versus directly published?
- What are the major limitations?
- What rights and attribution requirements apply?
- How should I interpret and cite the release?

## Required Documentation Files

- `README.md`
- `SCHEMA.md`
- `METHODOLOGY.md`
- `QA.md`
- `LIMITATIONS.md`
- `DATA-LICENSE.md`
- `SOURCES.md`
- `ATTRIBUTION.md`

## 1. `README.md` Specification

### Required Sections

#### Title and One-Sentence Summary
Example structure:
- dataset name
- one-sentence purpose statement
- explicit statement that the release is based on official/public sources only

#### What This Repository Publishes
Explain:
- what tables are included
- what benchmark means in this context
- that the dataset covers published rent indicators, not live listing inventory

#### Current Release Snapshot
Include:
- release version
- publication date
- schema version
- row counts
- geography counts
- source mix
- collector commit / run reference

#### File Inventory
For each file:
- file name
- purpose
- row count if relevant
- whether it is canonical or compatibility-only

#### Quick Interpretation Guide
Explain:
- one row = one geography × room group × metric × period × source observation
- `metric_type` must be checked before comparing rows
- `geography_type` must be checked
- annual and quarterly rows should not be merged blindly

#### Coverage Summary
State:
- time coverage
- geography coverage
- source coverage
- notable gaps

#### Rights / Attribution Notice
Link:
- `DATA-LICENSE.md`
- `SOURCES.md`
- `ATTRIBUTION.md`

#### Provenance
Explain:
- collector repo
- collector commit
- validated run
- manifest role

#### Change Log / Release Notes
At least a short summary of what changed in the release.

#### How to Cite
Short repository citation guidance.

#### Limitations Pointer
Link to `LIMITATIONS.md`.

### README Style Rules
- concise but complete
- no giant walls of text
- use tables for file inventory and source summary
- avoid legal overclaims
- explicitly warn users against treating the dataset as live rental listing inventory

## 2. `SCHEMA.md` Specification

### Required Sections
- overview of all files
- canonical vs compatibility files
- column dictionary for each CSV
- enums and allowed values
- null semantics
- units
- key relationships
- migration notes from previous schema version

### Minimum Required Tables in `SCHEMA.md`
- `rent_benchmarks.csv`
- `geography_reference.csv`
- `locality_crosswalk.csv` if retained

### Column Dictionary Requirements
For each column:
- name
- type
- required / nullable
- description
- allowed values if enum
- examples
- notes

## 3. `METHODOLOGY.md` Specification

### Required Sections

#### Source Overview
What each source contributes.

#### Source Priority / Merge Logic
Explain whether rows are merged, unioned, deduplicated, or coexist as parallel benchmark observations.

#### Metric Typing
Explain:
- direct official published median
- direct official published average
- modeled / hedonic estimate

#### Geography Normalization
Explain:
- locality normalization
- district handling
- code normalization
- naming normalization

#### Room Group Normalization
Explain canonical buckets and any source-specific mapping.

#### Period Modeling
Explain annual vs quarterly handling and how period fields are derived.

#### Missing Data / Suppression
Explain nulls, suppression, and optional counts.

#### Transformation Notes
Explain any nontrivial transformations.

#### Reproducibility Notes
Explain what part is reproducible from the data repo alone and what depends on the collector repo.

## 4. `QA.md` Specification

### Required Sections

#### Release Validation Checks
Examples:
- no null primary values
- valid enums
- unique `record_id`
- all fact geographies exist in geography reference
- all source IDs exist in source catalog if implemented
- no internal filesystem paths in manifest

#### Sanity Checks
Examples:
- expected source distribution
- expected room-group distribution
- period field consistency
- geography-type consistency

#### Known Warning Conditions
Examples:
- partial source refresh
- source page format changes
- publishable but incomplete companion metadata

#### Manual Review Checklist
Short human review list before tagging a release.

## 5. `LIMITATIONS.md` Specification

### Required Sections

#### Not a Live Market Inventory Dataset
This must be stated plainly.

#### Mixed Metric Types
Explain that averages, medians, and modeled estimates coexist.

#### Source Coverage Differences
Explain that not all geographies / room groups / periods are equally covered by all sources.

#### Interpretation Limits
Warn against:
- direct apples-to-apples comparison across metric types
- over-precise causal inference
- assuming vacancy / listing counts

#### Temporal Limits
Explain release date versus source date.

#### Geography Limits
Explain district rows and locality rows separately.

#### Rights / Source Limits
Point to rights docs.

## 6. `DATA-LICENSE.md` Specification

Must follow the rights plan document.

## 7. `SOURCES.md` Specification

Include:
- source table
- source details sections
- terms / attribution references
- open questions

## 8. `ATTRIBUTION.md` Specification

Include:
- short attribution
- full attribution
- source-specific notes
- reuse reminder

## Documentation Quality Bar

The documentation pack is complete only if:
- an external researcher can use the repo without reading collector code
- an external agent can map any value to source + metric type + period
- the repo does not overclaim rights
- the repo clearly states what it does **not** measure
