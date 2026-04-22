# Agent Rules

## Scope
- Work in `israel-rent-data` unless a task explicitly requires a tiny cross-reference to `../israel-rent-data-collector`.
- Do not modify or delete the detailed planning docs under `docs/patch/` when creating short agent-facing context files.

## Required Commands
- Data integrity check: `python scripts/validate_release.py --check`
- Tests: `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest`
- Coverage run: `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m coverage run -m pytest`
- Coverage report: `python -m coverage report`
- Coverage XML: `python -m coverage xml`

## Branch And PR Rules
- Feature branches should use the `codex/` prefix by default.
- Use the repo-specific GitHub MCPs first when they support the action.
- Fall back to `gh` only for unsupported GitHub operations.
- Treat feature work as incomplete until the branch is pushed and a non-draft PR exists.
- If a relevant milestone exists, assign it before handoff.

## Repository Boundaries
- Canonical fact table: `rent_benchmarks.csv`
- Canonical geography dimension: `geography_reference.csv`
- Compatibility-only locality lookup: `locality_crosswalk.csv`
- Release metadata: `manifest.json`
- Public documentation: root `*.md`
- Detailed patch plans: `docs/patch/*.md`
- Validation logic: `scripts/validate_release.py`
- Tests: `tests/`
- CI and PR automation: `.github/workflows/`

## Data Rules
- Main fact table must use the schema documented in `SCHEMA.md`.
- `locality_crosswalk.csv` is locality-only and must not be treated as the canonical geography dimension.
- Do not introduce internal workstation paths into public files.
- Do not overclaim blanket licensing rights over source-derived data.
- Keep rights, provenance, and schema documentation synchronized with the shipped files.

## Editing Rules
- Prefer minimal structural changes that improve public clarity and correctness.
- Preserve current file names unless there is a strong reason to break them.
- If a schema change is breaking, document it in `README.md`, `SCHEMA.md`, and `manifest.json`.
- Keep agent-context files concise and static:
  - `AGENTS.md` for hard constraints
  - `llms.txt` for architecture index
  - `.agent-plan.md` for current branch state and immediate next steps
