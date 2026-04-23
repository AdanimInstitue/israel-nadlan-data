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
- Keep `pr-agent-context` on floating `@v4` in workflow `uses:` lines.
- Do not pin `pr-agent-context` to a commit SHA or point release such as `v4.0.19`; floating `v4` is intentional and must stay that way.

## Workflow Guardrails

- `pr-agent-context` must track floating major version `v4` in both CI and refresh workflows.
- Treat any change from `@v4` to a SHA or fixed tag as a regression unless there is an explicit tracked decision to do otherwise.

## Architecture Boundaries

- Published data lives under `data/current/` and `data/releases/`.
- Release metadata lives under `metadata/`.
- Validation and metadata generation scripts live under `scripts/`.
- Public docs live at repo root and under `docs/`.
