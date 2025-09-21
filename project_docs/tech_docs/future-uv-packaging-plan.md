# UV Packaging Transition Plan

## Goals
- Maintain a working pipeline command immediately, without waiting for packaging refactors.
- Prepare the codebase to become a proper `uv`-managed package with clean import semantics.
- Eliminate ad-hoc path hacks once the package namespace is established.

## Immediate Actions (Working Code Now)
1. **Adopt module execution**: run tooling via `python -m src.processors.clean_data_pipeline ...` and update CLAUDE.md/scripts accordingly.
2. **Harden script entry points**: make sure every runnable script has `if __name__ == "__main__": main()` so module execution behaves correctly.
3. **Smoke-test pipeline**: with the virtualenv active (`pyyaml` installed), run the stable and beta commands to confirm imports succeed under the new convention.

## Phase 1: Prep for Package Namespace
1. **Introduce package directory**: choose a canonical name (e.g., `chrome_update_digest`) under `src/` and add `__init__.py` files.
2. **Move modules**: relocate current code into `src/chrome_update_digest/` (or alias via `__init__.py` if a gradual move is required).
3. **Standardize imports**: convert remaining bare imports (`utils.*`, `processors.*`, etc.) to `from chrome_update_digest...` and remove `sys.path.insert` shims in both code and tests.
4. **Regression tests**: run the pipeline command (`python -m chrome_update_digest.processors.clean_data_pipeline ...`) and full test suite to ensure import graph stability.

## Phase 2: UV Package Setup
1. **Create `pyproject.toml`** with project metadata, `tool.uv` section, and dependencies (e.g., `pyyaml`).
2. **Editable install**: use `uv pip install -e .` so local development mirrors package consumers; update docs to prefer `uv run` invocations.
3. **Entry points (optional)**: define console scripts if you want `uv run clean-data-pipeline ...` shortcuts.
4. **CI/automation update**: switch any automation to `uv run python -m chrome_update_digest.processors.clean_data_pipeline ...` (or the console script) and ensure virtualenv bootstrap uses `uv`.

## Validation & Risk Mitigation
- After each phase, rerun `python -m pytest` (or project test harness) to catch import regressions.
- For the directory move, plan a short-lived branch to avoid long-lived drift—tests should run before merging.
- Keep documentation (`CLAUDE.md`, internal runbooks) in sync with the new commands to avoid stale guidance.

## Notes
- The module-execution change is safe to deploy ahead of the packaging work and immediately resolves the current `ModuleNotFoundError`.
- `uv` expects a real package namespace; finishing Phase 1 before `uv init` keeps the packaging step straightforward.
