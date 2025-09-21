# 0922 Test Fixing Plan

## Context
Full-suite pytest execution stops during collection because several long-lived tests reference legacy tools and import paths that no longer exist after the recent refactor toward `src/`-scoped modules. Until the tests are aligned with the current structure, CI cannot give a meaningful signal.

## Affected Test Modules
- `tests/test_convert.py`: expects a top-level `convert_md2html` module instead of `src/convert_md2html.py`.
- `tests/test_fastmcp_pipeline.py`: imports `enterprise_digest` and `merged_digest_html` helpers removed from `fast_mcp_server.py`.
- `tests/test_fastmcp_resources_client.py`: targets the deprecated `fastmcp.AsyncClient` API.
- `tests/test_fault_tolerance.py`, `tests/test_fastmcp_html.py`, `tests/test_html_generation.py`: rely on a missing `mcp_tools.merged_digest_html` module and legacy digest file layouts.
- `tests/test_format_compliance.py`: depends on `src.mcp_tools.enterprise_digest` which is no longer present.
- `tests/test_webgpu_merger.py`: references `merge_webgpu_release_notes_v2`, superseded by `src/chrome_update_digest/processors/merge_webgpu_graphics.py`.

## Workstreams
1. **Path & Import Shims**
   - Introduce a `tests/conftest.py` that appends `src/` to `sys.path` and exports compatibility aliases (e.g., expose `convert_md2html` package-style import).
   - Validate that the shims do not interfere with modern entry points (FastMCP, CLI scripts).

2. **Deprecation Cleanup**
   - Update FastMCP resource tests to use the supported `fastmcp.Client` helpers or mark the tests as skipped when the legacy API is unavailable.
   - Remove or rewrite Enterprise digest expectations now that the enterprise tool has been retired; coordinate with product owners before deletion.

3. **HTML Merger Replacement**
   - Either restore a lightweight `MergedDigestHtmlTool` wrapper that consumes `ChromeDigestConverter`, or rewrite the tests to exercise the new orchestration flow provided by `GithubPagesOrchestratorTool`.
   - Refresh fixtures/path checks so they point at the current `digest_markdown/webplatform` layout.

4. **WebGPU Merger Alignment**
   - Port `tests/test_webgpu_merger.py` to import and exercise `WebGPUGraphicsMerger` from `src/chrome_update_digest/processors/merge_webgpu_graphics.py`.
   - Confirm expected behavior (feature extraction, heading demotion, history trimming) still matches requirements.

## Deliverables
- Updated tests that import only shipped modules.
- Optional shim modules (if we decide to maintain backwards compatibility) documented in `project_docs/tech_docs`.
- Passing pytest run (or documented skip list) captured in CI notes.

## Open Questions & Decisions
- **Enterprise e2e coverage**: No longer required. Action: decommission the enterprise pipeline tests and update documentation to note their retirement.
- **FastMCP integration scope**: Recommend replacing network-style integration tests with deterministic unit tests that instantiate our tool classes directly. Where `FastMCP` wiring must be exercised, provide local fixtures that construct a minimal `FastMCP` app with in-memory resources and patch outbound calls—no external dependencies or legacy client APIs.
- **Backward compatibility**: Not needed. Align all tests with the current `EnhancedWebplatformDigestTool` and supporting modules only.
