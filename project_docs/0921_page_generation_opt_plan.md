# 0921 Page Generation Optimization Plan

## Immediate Improvements
- Run `python src/tools/generate_github_pages_navigation.py` after each release so `digest_markdown/index.md`, `/versions`, and `/areas` stay current and the legacy `webplatform/` directory is cleaned automatically.
- Update navigation copy during generation (correct pluralisation, descriptive page titles) and drop placeholder Quick Links such as “Version Comparison” until the destination exists.
- Remove obsolete navigation buttons in `digest_markdown/_layouts/default.html` and rewrite `config/output_configuration.md` to describe the single webplatform flow only.
- Ensure Chrome 140+ content lands in `/versions/chrome-{version}` and `/areas/*/chrome-{version}.md`; plug any gaps if the scripted pass misses them.

## Single Source of Truth for Areas
- Replace the hard-coded `area_display_names` in the navigation generator with data loaded from `config/focus_areas.yaml`, keeping names, descriptions, and ordering in one authoritative file.
- When new focus areas (for example `isolated-web-apps`) are added to the config, the generator should pick them up automatically without code edits.

## Automation & MCP Integration (Option B)
- Introduce a new orchestrator MCP tool that first calls the digest-generation tool (enhanced webplatform digest) and, on success, invokes the GitHub Pages navigation generator.
- Extend the orchestrator to run `src/tools/validate_github_pages.py` and surface any validation errors through MCP so issues are caught before publish.
- Expose optional flags (e.g., force regenerate, skip clean) on the MCP wrapper while keeping defaults aligned with the release pipeline.

## Additional Cleanup Targets
- **Duplicate MCP tools**: remove the copies under `src/chrome_update_digest/mcp_tools/` once callers point to `src/mcp_tools/`; keep a single implementation in `src/mcp_tools/`.
- **Legacy generator script**: archive or delete `src/generate_github_pages_structure.py` after confirming `src/tools/generate_github_pages_navigation.py` (MCP wrapped) covers all functionality.
- **Legacy digest output**: after the orchestration integrates the new generator, delete `digest_markdown/webplatform/` from source so only `/versions` and `/areas` remain.
- **Documentation drift**: update `project_docs/tech_docs/github-pages-version-selection-design.md` (and similar) to describe the current dual-navigation structure and automation path.

*Updated: 2024-09-21*
