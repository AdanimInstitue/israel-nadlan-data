# AGENTS

## Commands

- Build metadata: `python scripts/build_release_metadata.py`
- Validate release: `python scripts/validate_release.py --check`
- Run tests: `pytest`

## Branching

- Use `codex/<topic>` or `refactor/<topic>` for agent branches.
- Keep changes scoped to this repository only.

## Hard Constraints

- Treat this repository as a complete public data product.
- Keep docs self-contained and public-facing.
- Do not mention private repositories, hidden enrichment, sibling paths, or internal workflows in tracked public files.
- Keep rights language conservative and source-specific.
- Keep machine-readable metadata relative-path-safe.

## Architecture Boundaries

- Published data lives under `data/current/` and `data/releases/`.
- Release metadata lives under `metadata/`.
- Validation and metadata generation scripts live under `scripts/`.
- Public docs live at repo root and under `docs/`.
