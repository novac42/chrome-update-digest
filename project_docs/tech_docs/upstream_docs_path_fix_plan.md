# Upstream Docs Output Path Handling

## Problem Statement
Running the WebPlatform processing scripts from inside `src/` causes their default output to land in `src/upstream_docs/...` instead of the repository root `upstream_docs/...`. This breaks the expected directory layout and confuses downstream tooling.

## Root Cause
Multiple scripts build default paths with bare `Path('upstream_docs/...')` literals. Those relative paths are resolved against the current working directory, so the output directory moves whenever the command is launched from a subdirectory (for example, IDE run configurations that set `src` as the working directory).

## Proposed Fix
- Introduce a shared helper (e.g. `src/utils/project_paths.py`) that exposes `PROJECT_ROOT` and convenience getters for `upstream_docs` and other shared directories.
- Update the pipelines that currently hardcode the relative paths—`CleanDataPipeline` (`src/processors/clean_data_pipeline.py`), `YAMLPipeline` (`src/utils/yaml_pipeline.py`), tooling such as `GitHubPagesNavigationGenerator` (`src/tools/generate_github_pages_navigation.py`), and other modules flagged by `rg`—so they derive defaults from the shared helper while still allowing callers to override the directories.
- Make sure any `base_path` parameters default to `PROJECT_ROOT` so tests can inject temporary paths without extra changes.

## Follow-up
- After refactoring, run the existing unit tests and perform a smoke run of the pipelines from the repository root to confirm outputs now land in `PROJECT_ROOT/upstream_docs/...` regardless of where the command is invoked.
