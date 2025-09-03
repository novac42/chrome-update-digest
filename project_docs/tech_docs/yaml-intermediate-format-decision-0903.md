# Decision: Use YAML as Intermediate Cache/Config for WebPlatform Digest

- Status: Accepted
- Date: 2025-09-03

## Context

The WebPlatform digest pipeline extracts features and links from Markdown release notes, tags them, and then generates digests. The pipeline already uses YAML as its intermediate cached representation and for area-split artifacts.

- Tool entry point and `use_cache` flag: `fast_mcp_server.py:188`–`fast_mcp_server.py:215`
- Enhanced tool run signature (includes `use_cache`): `src/mcp_tools/enhanced_webplatform_digest.py:44`–`src/mcp_tools/enhanced_webplatform_digest.py:55`
- Cache read path decision (`use_cache` short-circuit): `src/mcp_tools/enhanced_webplatform_digest.py:220`–`src/mcp_tools/enhanced_webplatform_digest.py:234`
- Area aggregation when no `target_area`: `src/mcp_tools/enhanced_webplatform_digest.py:260`–`src/mcp_tools/enhanced_webplatform_digest.py:340`
- YAML save/load: `src/utils/yaml_pipeline.py:245`–`src/utils/yaml_pipeline.py:266`, `src/utils/yaml_pipeline.py:268`–`src/utils/yaml_pipeline.py:279`
- Area-split YAML path convention: `src/utils/yaml_pipeline.py:353`–`src/utils/yaml_pipeline.py:376`

Cache locations:

- Root: `upstream_docs/processed_releasenotes/processed_forwebplatform`
- Area files: `processed_forwebplatform/areas/{area}/chrome-{version}-{channel}.yml`
- Combined (non-split): `processed_forwebplatform/processed_yaml/chrome-{version}-{channel}-tagged.yml`

## Decision

Continue using YAML as the intermediate cache/config format for the WebPlatform digest pipeline.

## Rationale

- Readability and diffs: YAML artifacts are easy to review and diff during development and content validation.
- LLM-friendly: YAML serializes cleanly for prompt construction and inspection without extra transformation.
- Simple, dependency-light: Avoids introducing a DB for a read-mostly cache; matches current workflow and repo conventions.
- Existing structure: The pipeline and tooling already implement consistent paths and area partitioning.

## Trade-offs / Risks

- Type coercion footguns: YAML 1.1 values like `on/off`, `yes/no` can coerce to booleans unexpectedly.
- Scale/performance: Many or large YAML files can be slower to scan/aggregate versus JSONL/SQLite when data grows.
- Schema looseness: YAML by default lacks enforced schema; malformed content can slip through without validation.

## Mitigations and Improvements

1) Validation on load
- Call `validate_yaml_data` after loading to fail fast on malformed caches.
  - Function: `src/utils/yaml_pipeline.py:490`

2) Safer serialization
- Prefer `yaml.safe_dump` for symmetry with `safe_load` to reduce risk of emitting tagged Python objects.

3) Scalar safety
- Ensure long, multi-line `content` fields dump with block scalars and quote ambiguous scalars where needed.

4) Versioning
- Add a top-level `schema_version` to YAML files and enforce on load for forward/backward compatibility.

5) Operational guardrails
- Keep area-split caches (already in place) to limit file size and speed up partial regeneration.
- Add a lightweight CLI or MCP tool action to re-generate caches for a given `{version, channel, area}` to avoid stale artifacts.

## When to Reconsider

- Data volume increases substantially, requiring faster random access or analytics. Consider:
  - JSONL per-feature for streaming/append workloads and simple map/filter tasks.
  - SQLite for indexed queries, dedup, and transactional updates across releases.
  - Parquet only if you need columnar analytics at scale (out of scope for current pipeline).

## Summary

YAML remains a good fit here: it’s human-auditable, LLM-friendly, and integrates cleanly with the existing `use_cache` flow and area-split outputs. Add validation, safer dumping, and a minimal schema/version to increase robustness without changing the overall design.

