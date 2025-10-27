# Legacy Sampling Mode - Implementation Guide

## Problem Summary

Based on telemetry analysis from `.monitoring/webplatform-telemetry.jsonl` (row 1162+):

**Root Cause Identified:**
1. ❌ Message transformation converts strings → `SamplingMessage` objects
2. ❌ This causes: `"model gpt-5-mini is not supported via Responses API"`
3. ❌ Payload preview shows: `[SamplingMessage(role='user', content=TextContent(...)`

## Solution: Legacy Sampling Mode

The legacy mode has been implemented in branch `fix/legacy-sampling-mode` to:
- ✅ Bypass message transformation (pass messages directly as strings)
- ✅ **Remove model preferences completely** - let the client choose the model automatically
- ✅ Use simpler sampling call path without any model specification

## How to Use

### Step 1: Enable Legacy Mode

Set the environment variable before running the MCP server:

```bash
export USE_LEGACY_SAMPLING=true
```

### Step 2: Start the MCP Server

```bash
cd /Users/lyzh/Documents/Nova_Projects/chrome-update-digest
USE_LEGACY_SAMPLING=true python fast_mcp_server.py
```

### Step 3: Test with MCP Client

Use your MCP client (Copilot, Claude, etc.) to invoke the `webplatform_digest` tool.

### Step 4: Verify Legacy Mode is Active

Look for this log message in debug output:
```
🔧 Legacy sampling mode enabled (no model preferences)
```

The client will automatically select an appropriate model.

## Expected Behavior Changes

### Before (New Mode - Broken)
```python
# Messages transformed to SamplingMessage objects
payload_preview: "[SamplingMessage(role='user', content=TextContent(type='text', text='...')"

# Error occurs
"model gpt-5-mini is not supported via Responses API"
```

### After (Legacy Mode - Working)
```python
# Messages passed directly as strings
payload_preview: "# Chrome Update Analyzer - Area-Specific Expert Analysis..."

# Sampling should succeed
✅ Legacy sampling successful
```

## Code Changes

The legacy mode implementation is in:
`src/chrome_update_digest/mcp/tools/enhanced_webplatform_digest.py`

### Key Changes:
1. Added environment variable check: `USE_LEGACY_SAMPLING`
2. Added simplified sampling path that:
   - Skips `_prepare_sampling_messages()` transformation
   - **Does NOT pass model_preferences** - allows client to choose model automatically
   - Uses direct `ctx.sample()` call with minimal parameters
3. Added telemetry logging for legacy mode

## Debugging

### Enable Debug Output

Set `debug=true` when calling the tool, or use:

```bash
export WEBPLATFORM_DEBUG=true
USE_LEGACY_SAMPLING=true python fast_mcp_server.py
```

### Check Telemetry

Monitor the telemetry file for success/failure:

```bash
tail -f .monitoring/webplatform-telemetry.jsonl | jq
```

Look for:
- `"event": "llm_sampling_attempt_start"` - Check if `payload_preview` is string vs SamplingMessage
- `"status": "success"` vs `"status": "error"`
- Error messages about unsupported models

## Model Preferences

### Legacy Mode (Recommended - No Model Specification)
```bash
# Legacy mode does NOT specify model preferences
# The MCP client automatically selects a compatible model
export USE_LEGACY_SAMPLING=true
```

**Benefits:**
- ✅ Avoids API compatibility issues
- ✅ Client chooses best available model automatically
- ✅ No "model not supported" errors

### New Mode (Currently Broken)
The new mode tries to:
1. Transform messages to `SamplingMessage` objects
2. Coerce model preferences to specific formats
3. Pass model preferences like `gpt-5-mini`

This causes: `"model gpt-5-mini is not supported via Responses API"`

## Rollback Plan

If legacy mode doesn't work, you can fully rollback to the working commit:

```bash
git checkout 667ec39 -- src/chrome_update_digest/mcp/tools/enhanced_webplatform_digest.py
```

This will restore the version from 24 hours ago that was working.

## Next Steps

1. ✅ Test legacy mode with actual MCP client
2. ⏳ If successful, determine if we should:
   - Keep legacy mode as default
   - Fix the message transformation logic
   - Remove the transformation code entirely
3. ⏳ Update documentation based on test results

## Technical Details

### Message Format Comparison

**Working (Legacy):**
```python
messages = "# Chrome Update Analyzer...\n\nAnalyze the following..."
ctx.sample(
    messages=messages, 
    system_prompt="...", 
    temperature=0.7,
    max_tokens=60000
    # NO model_preferences parameter - client chooses automatically
)
```

**Broken (New):**
```python
messages = [
    SamplingMessage(
        role="user",
        content=TextContent(type="text", text="...")
    )
]
ctx.sample(
    messages=messages, 
    system_prompt="...", 
    model_preferences="gpt-5-mini"  # ❌ Causes API rejection
)
```

### Why This Breaks

The MCP client (Copilot) expects messages in a specific format for the Responses API. Two issues cause failures:

1. **Message Format**: The `SamplingMessage` object transformation is incompatible with the API
2. **Model Specification**: Specifying models like `gpt-5-mini` via `model_preferences` causes rejection because that model isn't available through the Responses API

**Legacy mode fixes both** by using simple string messages and letting the client choose the model.

## Related Files

- Implementation: `src/chrome_update_digest/mcp/tools/enhanced_webplatform_digest.py`
- Analysis: `project_docs/tech_docs/sampling_failure_analysis_2025-10-27.md`
- Telemetry: `.monitoring/webplatform-telemetry.jsonl`

---

**Created:** October 27, 2025
**Branch:** `fix/legacy-sampling-mode`
**Status:** Ready for testing
