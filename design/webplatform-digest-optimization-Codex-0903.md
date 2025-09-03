# WebPlatform Digest Sampling Performance & Progress Improvements (Codex-0903)

## Summary
- Goal: Reduce digest generation latency and provide useful interim progress for MCP clients.
- Scope: `EnhancedWebplatformDigestTool`, `EnterpriseDigestTool`, FastMCP server glue.
- Approach: Concurrency for per-area generation, prompt/truncation tuning, configurable token caps, and progress reporting via a JSON status file and optional MCP tool.

## Current Behavior & Hot Spots
- Serial area processing: Per-area EN generation then ZH translation runs sequentially.
  - `src/mcp_tools/enhanced_webplatform_digest.py:920` in `_generate_per_area_digests` uses a simple for-loop.
- No streaming/interim outputs: Sampling returns only after the full completion.
  - `src/mcp_tools/enhanced_webplatform_digest.py:541` `_safe_sample_with_retry`
  - `src/mcp_tools/enterprise_digest.py:33` `_safe_sample_with_retry`
- Over-long prompts in non-split mode: No content truncation before LLM call.
  - `src/mcp_tools/enhanced_webplatform_digest.py:520` `_generate_digest_from_yaml`
- Aggressive token cap: `max_tokens=50000` can slow down completion time.
  - `src/mcp_tools/enhanced_webplatform_digest.py:565`
  - `src/mcp_tools/enterprise_digest.py:47`
- Progress is not surfaced to MCP clients: only stdout prints; no structured status API.

## Recommendations
1) Bounded concurrency for per-area generation
- Use `asyncio.Semaphore` to run multiple areas in parallel (2–4 workers), reducing wall-clock time while avoiding overload.
- Keep results updates thread-safe with an `asyncio.Lock`.

2) Truncate content in non-split mode
- Apply the same `_truncate_features(..., max_content_length=300)` used for area mode before `_format_features_for_llm` in `_generate_digest_from_yaml`.
- Substantially reduces tokens and completion latency.

3) Configurable, lower `max_tokens`
- Use env-driven defaults to avoid over-large responses:
  - `WEBPLATFORM_MAX_TOKENS` default `12000`
  - `ENTERPRISE_MAX_TOKENS` default `12000`
- Optionally adjust down for area mode (e.g., 6000–12000), keep a slightly higher default for non-split.

4) Structured progress reporting for polling
- Maintain `.monitoring/webplatform-progress.json` with fields like:
  - `version`, `channel`, `total_areas`, `completed_areas`, `languages`, `areas`, `per_area: { [area]: { en: status, zh: status, en_path, zh_path, error } }`, timestamps.
- Update after each major milestone: area start, EN saved, ZH saved, failures.
- Provide a parallel `.monitoring/enterprise-progress.json` for enterprise.

5) MCP progress tool (pollable)
- In `fast_mcp_server.py`, add `@mcp.tool()` to read and return the JSON progress so UIs can poll and show a progress bar.
- Optional: also expose a resource `file://webplatform-progress` for resource browsing UIs.

6) Optional streaming (feature-gated)
- Add `_stream_sample_with_callbacks()` that tries `ctx.sample(..., stream=True)` or `ctx.stream_sample(...)`; progressively write content to file and throttle updates.
- Fallback to `_safe_sample_with_retry` if streaming isn’t supported by `Context`.

7) Enterprise parity
- Mirror token caps, progress JSON, and optional streaming in `EnterpriseDigestTool` to keep UX consistent.

## Implementation Sketch

1. Concurrency in `_generate_per_area_digests`
- File: `src/mcp_tools/enhanced_webplatform_digest.py:920`
- Replace the sequential loop with:
  - `max_concurrency = int(os.getenv("WEBPLATFORM_MAX_CONCURRENCY", "3"))`
  - `sem = asyncio.Semaphore(max_concurrency)` and `lock = asyncio.Lock()`
  - `async def process_area(area):`
    - `async with sem:`
      - Generate EN, validate, save, update `results` and progress JSON under `lock`.
      - If ZH required, translate, validate, save, update `results` and progress JSON.
  - `await asyncio.gather(*(process_area(a) for a in areas))`

2. Truncation in `_generate_digest_from_yaml`
- File: `src/mcp_tools/enhanced_webplatform_digest.py:520`
- Before `_format_features_for_llm(yaml_data)`, do `yaml_data = self._truncate_features(yaml_data, max_content_length=300)`.

3. Token caps via env
- Files:
  - `src/mcp_tools/enhanced_webplatform_digest.py:565`
  - `src/mcp_tools/enterprise_digest.py:47`
- Read `max_tokens = int(os.getenv("WEBPLATFORM_MAX_TOKENS", "12000"))` (and `ENTERPRISE_MAX_TOKENS`).

4. Progress JSON helper
- New private helpers in `EnhancedWebplatformDigestTool`:
  - `_init_progress(version, channel, languages, areas)`
  - `_update_progress(area, lang, status, path=None, error=None)`
  - Write to `.monitoring/webplatform-progress.json` with `parents=True`.

5. MCP status tools
- `fast_mcp_server.py`
  - `@mcp.tool()` `get_webplatform_progress()` -> read `.monitoring/webplatform-progress.json` and return JSON or a friendly message if missing.
  - Optional `@mcp.tool()` `get_enterprise_progress()` for the enterprise path.

6. Optional streaming
- Add `_stream_sample_with_callbacks()` next to `_safe_sample_with_retry` in both tools;
- Feature-gate by `WEBPLATFORM_ENABLE_STREAM=1` or `ENTERPRISE_ENABLE_STREAM=1`.

## Example Progress JSON
```json
{
  "version": "138",
  "channel": "stable",
  "languages": ["en", "zh"],
  "areas": ["css", "webapi", "graphics-webgpu"],
  "total_areas": 3,
  "completed_areas": 1,
  "per_area": {
    "css": { "en": "done", "zh": "done", "en_path": "digest_markdown/webplatform/css/chrome-138-stable-en.md", "zh_path": "digest_markdown/webplatform/css/chrome-138-stable-zh.md" },
    "webapi": { "en": "in_progress" },
    "graphics-webgpu": { "en": "pending" }
  },
  "updated_at": "2025-09-03T12:34:56Z"
}
```

## Risks & Mitigations
- API rate limiting under concurrency: cap concurrency via `WEBPLATFORM_MAX_CONCURRENCY` and backoff in `_safe_sample_with_retry` (already present); consider per-model quotas.
- File contention: protect progress writes with an `asyncio.Lock`.
- Larger repos: progress JSON can grow; keep it small and overwrite in place.

## Validation Plan
- Unit-level dry runs with mocked `ctx.sample` to verify concurrency order and progress JSON transitions.
- Real run on a version with multiple areas; confirm EN markdowns appear early, ZH follows; progress tool returns increasing completion.
- Confirm token usage drops in non-split mode after truncation.

## Config Knobs
- `WEBPLATFORM_MAX_CONCURRENCY` (default: `3`)
- `WEBPLATFORM_MAX_TOKENS` (default: `12000`)
- `WEBPLATFORM_ENABLE_STREAM` (`0`/`1`, default: `0`)
- `ENTERPRISE_MAX_TOKENS` (default: `12000`)
- `ENTERPRISE_ENABLE_STREAM` (`0`/`1`, default: `0`)

## Suggested Defaults
- Keep `split_by_area=True` for faster first outputs per area.
- Default `language="en"` if you need the fastest users’ perceived first content, or keep bilingual with concurrency.

## Future Enhancements
- Persist per-area YAML caching improvements (e.g., hashing feature arrays) to skip unchanged areas.
- Add optional HTML progress dashboard under `digest_markdown/` for local preview.
- Add rate-limit aware queue to share budgets across tools.

---
References
- `src/mcp_tools/enhanced_webplatform_digest.py:520`
- `src/mcp_tools/enhanced_webplatform_digest.py:541`
- `src/mcp_tools/enhanced_webplatform_digest.py:565`
- `src/mcp_tools/enhanced_webplatform_digest.py:920`
- `src/mcp_tools/enterprise_digest.py:33`
- `src/mcp_tools/enterprise_digest.py:47`
- `fast_mcp_server.py:1`
