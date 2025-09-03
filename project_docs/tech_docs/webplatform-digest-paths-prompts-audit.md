# WebPlatform Digest – File Paths & Prompt Instructions Audit

Version: 2025-09-03

## Summary
This document captures path/prompt issues discovered in the WebPlatform digest generation flow, their OS sensitivity, and recommended fixes. The YAML pipeline structure was recently optimized; these checks ensure the toolchain reads/writes the right locations and that prompts match the pipeline’s conventions.

## Findings

- Area YAML path assembly uses a parent directory that skips the intended `areas/` folder.
  - Code: `src/mcp_tools/enhanced_webplatform_digest.py:225`
  - Code: `src/mcp_tools/enhanced_webplatform_digest.py:286`
  - Expected: `upstream_docs/processed_releasenotes/processed_forwebplatform/areas/{area}/chrome-{version}-{channel}.yml`
  - Actual: Code resolves `self.cache_dir.parent / 'areas' / ...` (one level too high)
  - OS impact: OS-agnostic bug (fails on Windows and Linux)

- Chinese translation prompt path does not match the repo layout.
  - Code: `src/mcp_tools/enhanced_webplatform_digest.py:1303`
  - Code expects: `prompts/webplatform-prompts/webplatform-translation-prompt-zh.md`
  - Actual file: `prompts/webplatform-prompts/archive/webplatform-translation-prompt-zh.md`
  - OS impact: OS-agnostic (FileNotFoundError)

- YAML bilingual fallback prompt path does not match the repo layout.
  - Code: `src/mcp_tools/enhanced_webplatform_digest.py:650`
  - Code expects: `prompts/webplatform-prompt-yaml-bilingual.md`
  - Actual file: `prompts/webplatform-prompts/archive/webplatform-prompt-yaml-bilingual.md`
  - OS impact: OS-agnostic (FileNotFoundError)

- Release notes directory casing is inconsistent across components.
  - Enhanced tool uses: `upstream_docs/release_notes/WebPlatform` (matches repo).
  - LinkExtractionService uses: `upstream_docs/release_notes/webplatform`.
    - Code: `src/services/link_extraction_service.py:27`
  - OS impact: Windows is case-insensitive (may pass), Linux is case-sensitive (will fail in CI/containers).

- Prompt output path guidance vs. implementation.
  - Prompts specify: `digest_markdown/webplatform/[AREA]/chrome-[version]-[channel]-[lang].md`.
  - Code paths: consistent with the above (no change required).

## Recommendations

1) Fix Area YAML path (minimal, OS-neutral)
- Change references to use `self.cache_dir / 'areas' / {area}` instead of `self.cache_dir.parent / 'areas' / {area}`.
- Files: `src/mcp_tools/enhanced_webplatform_digest.py:225`, `:286`.

2) Make prompt file resolution robust with archive fallback (OS-neutral)
- Lookup order for Chinese translation prompt:
  - Try `prompts/webplatform-prompts/webplatform-translation-prompt-zh.md`
  - Fallback to `prompts/webplatform-prompts/archive/webplatform-translation-prompt-zh.md`
- Lookup order for YAML bilingual fallback prompt:
  - Try `prompts/webplatform-prompts/webplatform-prompt-yaml-bilingual.md`
  - Fallback to `prompts/webplatform-prompts/archive/webplatform-prompt-yaml-bilingual.md`
- Files: `src/mcp_tools/enhanced_webplatform_digest.py:650`, `:1303`.

3) Case-insensitive resolution for Release Notes directory (prefer logic over manual casing or central config)
- Implement a small utility to join path components in a case-insensitive way by scanning directory entries when exact-case match is absent.
- Use this resolver wherever we access `upstream_docs/release_notes/<platform>` to neutralize case sensitivity across OS.

### Proposed helper (design sketch)

- Module: `src/utils/path_utils.py`
- Function: `resolve_case_insensitive(base: Path, *parts) -> Path`
- Behavior:
  - For each path segment, if `base/segment` exists, use it.
  - Else, scan `base.iterdir()` and pick the first entry with `entry.name.lower() == segment.lower()`.
  - If none found, return the non-existing `base/segment` and let caller handle “not found”.

Example usage in LinkExtractionService:
- Replace direct `self.base_path / 'upstream_docs' / 'release_notes' / 'WebPlatform'` with:
  - `resolve_case_insensitive(self.base_path, 'upstream_docs', 'release_notes', 'WebPlatform')`.
- This allows inputs like `webplatform` or `WebPlatform` to be resolved on Linux.

### Why not manual rename or central config?
- Manual casing is brittle and regresses easily.
- Central config reduces duplication but still fails if filesystem casing drifts; the resolver addresses the root cause by normalizing at access time.

## Implementation Plan

- Step 1: Correct YAML path joins
  - Update two lines in `src/mcp_tools/enhanced_webplatform_digest.py` to use `self.cache_dir / 'areas'`.

- Step 2: Add case-insensitive resolver
  - Add `src/utils/path_utils.py` with `resolve_case_insensitive`.
  - Cover with a small unit test that creates mixed-case temp dirs to ensure portability.

- Step 3: Apply resolver in path consumers
  - In `src/services/link_extraction_service.py:27`, build `release_notes_dir` via resolver.
  - In `src/mcp_tools/enhanced_webplatform_digest.py` `_load_release_notes`, compute `base_dir` via the resolver as well.

- Step 4: Prompt path fallback
  - In `src/mcp_tools/enhanced_webplatform_digest.py:650` and `:1303`, attempt primary path then archive fallback.

## Testing Checklist

- Windows and Linux (container) runs:
  - Ensure per-area YAML is found and loaded for a known version.
  - Ensure missing-primary-prompt scenarios succeed via archive fallback.
  - Validate release notes loaded when casing is intentionally altered (e.g., `webplatform`).

- Unit tests (where applicable):
  - Path resolver: resolves correct existing entries; returns non-existing path when no match.
  - Enhanced tool: mocked filesystem verifying fallback to archive prompt.

- End-to-end sanity:
  - Run EnhancedWebplatformDigestTool for a known version; confirm outputs saved to `digest_markdown/webplatform/[area]/chrome-<v>-<channel>-<lang>.md`.

## Risk & Mitigation

- Resolver may pick the first match when multiple entries collide (rare on typical repos). Mitigate by predictable ordering (sorted by name) if needed.
- Fallback logic could mask missing primary prompts; log which path was chosen for traceability.

## Action Items

- Correct YAML area paths in enhanced tool (2 lines).
- Add case-insensitive path resolver and adopt in consumers.
- Add prompt lookup fallback to include `archive/` variants.
- Optional: add debug logs on chosen paths for diagnostics.

