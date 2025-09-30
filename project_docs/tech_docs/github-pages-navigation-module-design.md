# GitHub Pages Navigation Module Design

**Status**: Active
**Last Updated**: 2025-09-30

## Module Purpose
The navigation module publishes the processed WebPlatform digests to a GitHub Pages-compatible site. It reorganises staged area digests into version- and area-centric navigation trees, keeps bilingual content in sync, and validates the resulting site structure before deployment. The module can be run directly by CLI scripts or orchestrated through FastMCP so release automation and ad-hoc workflows share the same implementation.

## Responsibilities
- Consume digests emitted by `digest_markdown/webplatform/` and construct the public site under `digest_markdown/versions/` and `digest_markdown/areas/`.
- Preserve bilingual outputs (English/Chinese) in a single directory tree with language-specific leaf files.
- Generate hub pages (`index.md`) with links, metadata, and breadcrumbs that mirror `config/focus_areas.yaml` ordering.
- Provide validation hooks that detect missing language pairs, broken navigation links, and stale version references.
- Expose an orchestration entry point that can run digest regeneration, navigation refresh, and validation in a single operation.

## Scope & Out-of-Scope
- **In Scope**: File generation for GitHub Pages, navigation metadata, validation, optional cleanup of stale files.
- **Out of Scope**: LLM-based digest creation (handled earlier in the pipeline), CDN upload, and HTML theming beyond what Jekyll provides.

## Inputs and Dependencies
- Processed digests under `digest_markdown/webplatform/{area}/chrome-{version}-{channel}-{lang}.md`.
- Focus area configuration from `config/focus_areas.yaml` (display names, order, descriptions).
- Optional layout assets in `digest_markdown/_layouts/` and `_config.yml` for Jekyll.
- Version metadata and progress files in `.monitoring/` (used by the orchestrator for status reporting).

## Outputs
- Version-oriented tree: `digest_markdown/versions/chrome-{version}/index.md` plus `{area}-{lang}.md` leaves.
- Area-oriented tree: `digest_markdown/areas/{area}/index.md` plus `chrome-{version}-{lang}.md` leaves.
- Landing page `digest_markdown/index.md` with quick links to latest versions and areas.
- Optional bilingual companion files (e.g., `css-en.md`, `css-zh.md`) living side by side in the same directory.

## Execution Flow
1. **Inventory staged digests** – `GitHubPagesNavigationGenerator` scans the staging tree, groups files by version, area, and language, and discovers the latest version.
2. **Build navigation model** – focus-area metadata is combined with inventory results to decide link ordering, display titles, and breadcrumbs.
3. **Emit version pages** – generator writes per-version hubs and per-area leaves, embedding previous/next navigation and language toggles.
4. **Emit area pages** – generator writes area hubs showing version history plus one leaf per version and language.
5. **Write landing page** – refreshed index surfaces latest stable release and links to both navigation modes.
6. **Validate** – `src/tools/validate_github_pages.py` checks link references, bilingual parity, and ensures every staged digest is reachable.

## Key Components
- `src/tools/generate_github_pages_navigation.py`
  - `GitHubPagesNavigationGenerator` – main entry point with `run()` and helper methods for generating version and area trees.
  - Command-line arguments: `--language` (`en`, `zh`, `bilingual`), `--clean`, `--skip-webplatform`, `--target-version`, `--target-area`.
- `src/tools/validate_github_pages.py`
  - `GithubPagesValidator` – walks the generated tree, checks links, validates breadcrumbs, and reports inconsistencies.
  - CLI arguments: `--strict` to treat warnings as errors, `--language` filters.
- `src/mcp_tools/github_pages_orchestrator.GithubPagesOrchestratorTool`
  - Coordinates digest regeneration via `EnhancedWebplatformDigestTool`, navigation generation, and validation.
  - Parameters include `force_regenerate`, `skip_clean`, `skip_digest`, `skip_validation`, `target_area`, and `language`.

## CLI Usage
```bash
# Generate navigation (English only)
python src/tools/generate_github_pages_navigation.py

# Generate bilingual navigation and clean stale files first
python src/tools/generate_github_pages_navigation.py --language bilingual --clean

# Validate the generated site
python src/tools/validate_github_pages.py --strict

# Optional HTML conversion for local preview
python src/convert_md2html.py
```

## MCP Orchestration
```python
# Inside an MCP client session
await ctx.call_tool(
    "generate_github_pages",
    version="140",
    channel="stable",
    language="bilingual",
    force_regenerate=False,
    skip_clean=False,
    skip_digest=False,
    skip_validation=False
)
```
- The orchestrator streams progress by updating `.monitoring/webplatform-progress.json` so clients can poll status via `get_webplatform_progress`.
- When `skip_digest=True`, the tool reuses existing digests and only refreshes navigation/validation.

## Cleanup and Idempotency
- The generator can run with `--clean` to remove outdated navigation prior to regeneration. Without the flag, it performs targeted updates and leaves unrelated files untouched.
- Language-specific files are overwritten atomically so repeated runs produce deterministic results.

## Validation Guarantees
- Every staged digest must surface in at least one navigation tree; missing mappings trigger validator errors.
- Breadcrumbs follow the pattern `Home > Versions > Chrome {version} > {Area}` and `Home > Areas > {Area} > Chrome {version}`.
- The validator checks that bilingual runs emit `{suffix}-en.md` and `{suffix}-zh.md` pairs or explicitly warns when a translation is missing.

## Deployment Notes
- After generation, the site can be previewed locally via `bundle exec jekyll serve` from `digest_markdown/`.
- Automation typically commits the refreshed `digest_markdown` directory and pushes to the GitHub Pages branch.
- Future CDN or remote hosting work will reuse the generated markdown; HTML conversion remains optional.

## Future Enhancements
- Automated diff view between adjacent versions.
- RSS feeds per area and per version.
- Search index generation for client-side filtering.
- Integration with planned resource hosting (`MCP_RESOURCE_MODE=remote`).

## Revision History
- **2025-09-30** – Consolidated navigation plan and design docs into this module design; documented orchestrator parameters and validation rules.
- **2024-09-21** – Initial dual navigation design (`github-pages-version-selection-design.md`).
- **2024-09-22** – Added operational guide for navigation generator (`github-pages-navigation.md`).
