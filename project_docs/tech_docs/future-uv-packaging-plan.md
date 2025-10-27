# UV Packaging Hardening Plan

This document tracks follow-up work now that the `chrome_update_digest`
package is already managed by `uv` (`pyproject.toml`, `uv.lock`, CLI entry
points, and FastMCP server module are in place).

## Current Status
- `uv sync` is the canonical setup flow; `README` and `CLAUDE.md` already
  reference `uv run` commands.
- `chrome_update_digest.cli` and `chrome_update_digest.mcp.server` ship via
  `[project.scripts]`, with `fast_mcp_server.py` and legacy `src/processors`
  modules acting as compatibility shims.
- Tests still manipulate `sys.path` directly, and several runbooks reference
  legacy `python -m src.processors...` execution.

## Remaining Workstreams
1. **Retire compatibility layers**
   - Update any remaining docs, automation, and notebooks to rely on
     `uv run chrome-update-digest-cli …` or direct package imports.
   - Drop the `src/processors/*.py` shims after confirming no callers depend on
     them; remove the `sys.path` insert logic while cleaning up.
   - Remove the root-level `fast_mcp_server.py` shim once external scripts are
     migrated to `chrome-update-digest-mcp`.
2. **Normalize imports and tests**
   - Replace ad-hoc `sys.path.*` tweaks across `tests/` with proper package
     imports (`from chrome_update_digest...`).
   - Ensure `uv run pytest` succeeds without test-side path injection by
     relying on the editable install produced by `uv sync`.
3. **Distribution validation**
   - Build a wheel via `uv build`, install it into a clean environment, and
     smoke-test both CLI (`chrome-update-digest-cli process …`) and MCP server
     (`chrome-update-digest-mcp --base-path …`).
   - Capture the validation steps in `project_docs/runbooks` so release
     sign-off includes packaging verification.
4. **Documentation alignment**
   - Consolidate the packaging narrative with
     `project_docs/tech_docs/2.0-uv-packaging-plan.md` to avoid drift; treat
     this file as the tactical checklist and the 2.0 plan as the architectural
     overview.
   - Refresh onboarding notes to highlight the new CLI subcommands and any
     required environment variables (`CHROME_UPDATE_DIGEST_BASE_PATH`, data
     locations, etc.).
5. **Optional hardening**
   - Add smoke tests that import `chrome_update_digest.mcp.server` and call
     `create_app()` to guard against future refactors.
   - Consider publishing prebuilt artefacts (wheel + lockfile) for downstream
     automation once the cleanup above is complete.

## Validation Checklist
- `uv run pytest` without compatibility shims or manual path patches.
- `uv build` followed by install-and-run smoke tests in a clean directory.
- Documentation diff reviewed alongside the code changes that remove the
  compatibility layer.
