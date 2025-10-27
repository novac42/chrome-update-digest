# Digest Sampling Suggestion

- Update `_safe_sample_with_retry` in `src/chrome_update_digest/mcp/tools/enhanced_webplatform_digest.py` to pass the original string payload to `ctx.sample` (or convert to real `SamplingMessage`/`TextContent` objects) instead of wrapping it in plain dicts. The current dict-based messages violate FastMCP 2.x validation, so sampling never actually runs.
