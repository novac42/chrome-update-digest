# Technical Overview - Chrome WebPlatform Digest

**Last Updated**: 2025-09-30

## Project Summary
The Chrome WebPlatform Digest project ingests Chrome WebPlatform release notes, normalises them into a structured YAML format, and produces bilingual area digests and site navigation for GitHub Pages. The codebase exposes the same pipeline by command-line scripts and by FastMCP tools so it can power automation as well as interactive workflows.

## High-Level Data Flow
1. **Monitor & Fetch Releases** – `src/mcp_tools/release_monitor.ReleaseMonitorTool` and `src/utils/release_monitor_core` detect new versions and download upstream markdown into `upstream_docs/release_notes/`.
2. **Structure & Clean Data** – `src/chrome_update_digest/processors/clean_data_pipeline.CleanDataPipeline` loads raw notes, applies focus-area rules from `config/focus_areas.yaml`, merges WebGPU updates, and writes area markdown plus structured YAML to `upstream_docs/processed_releasenotes/processed_forwebplatform/`.
3. **Tag Features into YAML** – `src/utils/yaml_pipeline.YAMLPipeline` extracts links with `LinkExtractor`, tags headings with `HeadingBasedTagger`, and persists deterministic YAML payloads used by downstream sampling.
4. **Generate Digests** – `src/mcp_tools/enhanced_webplatform_digest.EnhancedWebplatformDigestTool` consumes the YAML, optionally filters focus areas, calls FastMCP sampling for English/Chinese summaries, and stores results in `digest_markdown/webplatform/`.
5. **Publish Navigation** – `src/tools/generate_github_pages_navigation.py` copies staged digests into the version/area navigation tree, while `src/tools/validate_github_pages.py` enforces structural rules and GitHub Pages (Jekyll) renders the staged markdown into HTML.

## Core Architecture

### Data Acquisition & Monitoring
- `fast_mcp_server.py` registers `check_latest_releases` and `crawl_missing_releases` tools that delegate to `ReleaseMonitorTool` for version tracking, RSS parsing, and optional crawling.
- `src/utils/release_note_locator` and `src/utils/chrome_version_detector` locate raw WebPlatform and WebGPU files and resolve channel-specific filenames.
- Monitoring metadata (run history, progress) lives under `.monitoring/` so automated jobs can report status to clients.

### Normalisation Pipeline
- `CleanDataPipeline` orchestrates end-to-end processing: validating H2 structure, instantiating area-specific extractors from `AreaExtractorFactory`, merging dedicated WebGPU notes through `WebGPUAreaExtractor`, and emitting per-area markdown plus optional YAML.
- `src/chrome_update_digest/processors/area_extractors` defines the `Section` dataclass and extractor implementations for headings, feature detection, and safe markdown trimming.
- `src/utils/focus_area_manager` and `src/utils/area_classifier.WebGPUClassifier` supply configurable mappings and strict WebGPU classification rules. The configuration lives in `config/focus_areas.yaml` and can extend areas without code changes.

### YAML & Feature Tagging Layer
- `YAMLPipeline` produces deterministic feature documents with statistics, link inventories, and heading paths. It merges WebGPU updates ahead of extraction to keep the "graphics-webgpu" area authoritative.
- Tagged data is cached per version/channel (`*-webplatform-with-webgpu.yml`) and optionally split per area for reuse by tooling.

### Digest Generation & Publication
- `EnhancedWebplatformDigestTool` exposes the primary MCP entry point (`webplatform_digest`). It resolves sampling preferences, reuses cached YAML when possible, generates per-area or single-area digests, and writes bilingual files to `digest_markdown/webplatform/{area}/chrome-{version}-{channel}-{lang}.md`.
- `FeatureSplitterTool` provides finer-grained sampling utilities by splitting markdown along heading paths for client workflows that need per-feature prompts.
- `GithubPagesOrchestratorTool` (invoked by the `generate_github_pages` MCP tool) ties together digest regeneration, navigation refresh, and validation into one command that can skip expensive steps when outputs already exist.
- GitHub Pages helpers live under `src/tools/`: the navigation generator emits the final directory tree (`digest_markdown/versions/` and `digest_markdown/areas/`), while the validator scans for broken links, missing language pairs, or stale metadata.

### Resource Exposure
- `src/mcp_resources/processed_releasenotes.ProcessedReleaseNotesResource` turns markdown and YAML artefacts into FastMCP resources so clients can read them over the protocol. `fast_mcp_server.register_dynamic_resources()` registers every discovered file with accurate mime types and metadata.
- Prompts and other static assets are exposed through `file://` resources, with canonical copies stored under `prompts/webplatform-prompts/`.

## Directory Map
- `src/chrome_update_digest/` – Canonical package for processors, tools, and shared utilities used by the pipeline.
- `src/mcp_tools/` – FastMCP tool wrappers that adapt the package modules for interactive use.
- `src/utils/` – Reusable helpers: link extraction, focus-area configuration, YAML pipeline, project path resolution, and release monitoring core logic.
- `src/tools/` – CLI-centric scripts for GitHub Pages navigation and validation.
- `digest_markdown/` – Staging output for digests (`webplatform/`) and the generated GitHub Pages site (`versions/`, `areas/`).
- `upstream_docs/` – Source release notes (raw under `release_notes/` and processed under `processed_releasenotes/`).
- `.monitoring/` – Run metadata captured during long-running tasks.

## Execution Modes
- **CLI**
  - `python -m chrome_update_digest.processors.clean_data_pipeline --version 140 --channel stable --with-yaml`
  - `python -m mcp_tools.enhanced_webplatform_digest --version 140 --split-by-area`
  - `python src/tools/generate_github_pages_navigation.py --language bilingual --clean`
  - `bundle exec jekyll serve --source digest_markdown --destination _site` (Local preview of the GitHub Pages site)
- **FastMCP Tools**
  - `webplatform_digest` → `EnhancedWebplatformDigestTool.run`
  - `split_features_by_heading` → `FeatureSplitterTool` utilities
  - `check_latest_releases` / `crawl_missing_releases` → `ReleaseMonitorTool`
  - `generate_github_pages` → `GithubPagesOrchestratorTool`
  - `get_webplatform_progress` → progress reader backed by `.monitoring/webplatform-progress.json`

## Configuration & Environment
- `config/focus_areas.yaml` defines area metadata, display names, heading patterns, and keywords that drive both extraction and site navigation.
- Environment variables recognized by the pipeline include `WEBPLATFORM_MODEL`, `WEBPLATFORM_MODEL_PREFERENCES`, `WEBPLATFORM_MAX_CONCURRENCY`, `STRICT_WEBGPU_AREA`, and MCP resource hosting settings (`MCP_RESOURCE_MODE`, `MCP_CDN_BASE`).
- Cached outputs are organised by version and channel so re-runs can skip redundant work while still allowing forced regeneration (`force_regenerate=True`).

## Validation, Testing, and Monitoring
- Structural checks run inside `CleanDataPipeline.validate_structure` before processing to catch missing focus areas.
- `src/tools/validate_github_pages.py` enforces navigation invariants (paired languages, breadcrumb coverage, link integrity).
- Tests under `tests/` focus on strict WebGPU classification, focus-area mapping, and utility behaviour; they rely on the package namespace rather than legacy import paths.
- Progress JSON files under `.monitoring/` allow long-running MCP operations to surface status updates to clients.

## Future Considerations
- `todo-yaml-resources-and-remote-hosting-plan.md` tracks work to expose YAML via MCP resources and optional CDN hosting.
- `future-uv-packaging-plan.md` documents the packaging path that will convert the project into a proper `uv` package with console entry points.
- Additional FastMCP tools can reuse the existing YAML pipeline for analytics or diffing without reprocessing raw release notes.
