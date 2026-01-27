---
name: chrome-update-digest
description: Process Chrome release notes into multilingual, area-specific digests. Use when the user wants to (1) Process Chrome release notes for a specific version, (2) Generate digests for Web Platform updates, (3) Translate Chrome features to Chinese, (4) Prepare area-specific summaries (CSS, WebAPI, WebGPU, AI, etc.). Trigger phrases "process Chrome X", "digest Chrome release notes", "translate Chrome X features".
---

# Chrome Update Digest

Process Chrome release notes into structured, multilingual digests for 23 focus areas.

## Quick Start

**Simple usage (smart defaults)**:
```
Process Chrome 143
```
Uses: stable channel, bilingual (en+zh), all 23 areas

**Custom usage**:
```
Process Chrome 143 beta in English for CSS and WebAPI
```

**✨ Phase 2 Complete**: Full bilingual digest generation now supported!
- ✓ Extracts structured YAML data from release notes
- ✓ Generates English digests using LLM
- ✓ Translates to Chinese with structure preservation

## Workflow

The skill executes these steps automatically:

1. **Validate**: Check version format and input files exist
2. **Clean Pipeline**: Run clean data pipeline to extract area-specific YAML
3. **Generate**: Create English digests using LLM for each area
4. **Translate**: Convert to Chinese (if bilingual/Chinese mode)
5. **Write**: Save outputs to `upstream_docs/processed_releasenotes/`

## Processing Options

**Channel**: stable (default) or beta
**Language**: bilingual (default), en, or zh
**Areas**: all (default) or specific subset

For area details, see [references/focus_areas.md](references/focus_areas.md).

## Common Issues

See [references/common_issues.md](references/common_issues.md) for troubleshooting.

## Implementation

When the user triggers this skill with a request like "Process Chrome 139", you should:

1. **Parse the request** to extract:
   - Version number (required)
   - Channel (stable or beta, default: stable)
   - Language (bilingual, en, or zh, default: bilingual)
   - Areas (list of specific areas or None for all)

2. **Validate inputs**:
   - Check version format is valid (e.g., 139, 140)
   - Verify input files exist in `upstream_docs/release_notes/WebPlatform/`
   - If files missing, provide helpful error with download instructions

3. **Execute the processing script**:
   ```bash
   uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
     --version {version} \
     --channel {channel} \
     --language {language} \
     --verbose
   ```

   If specific areas requested, add: `--areas {area1} {area2} ...`

4. **Report progress and results**:
   - Stream progress updates from the script
   - Show completion status with output paths
   - If errors occur, provide troubleshooting guidance

## Examples

### Example 1: Simple request with defaults
```
User: "Process Chrome 139"
Assistant:
  Parsing request: version=139, channel=stable, language=bilingual, areas=all
  Validating inputs... ✓

  Running: uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py --version 139 --channel stable --language bilingual --verbose

  [1/4] Running clean data pipeline...
  [2/4] Generating English digests (23 areas)...
  [3/4] Translating to Chinese...
  [4/4] Complete!

  ✓ Generated digests: upstream_docs/processed_releasenotes/processed_forwebplatform/areas/
```

### Example 2: Custom parameters
```
User: "Process Chrome 139 beta in English for CSS and WebAPI"
Assistant:
  Parsing request: version=139, channel=beta, language=en, areas=[css, webapi]
  Validating inputs... ✓

  Running: uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py --version 139 --channel beta --language en --areas css webapi --verbose

  [1/4] Running clean data pipeline...
  [2/4] Generating English digests (2 areas)...
    1/2 complete: css
    2/2 complete: webapi
  [3/4] Skipping translation (English only mode)
  [4/4] Complete!

  ✓ Generated digests for 2 areas
```

### Example 3: Error handling
```
User: "Process Chrome 999"
Assistant:
  Parsing request: version=999, channel=stable, language=bilingual, areas=all
  Validating inputs... ✗

  Error: Chrome 999 release notes not found.
  Expected: upstream_docs/release_notes/WebPlatform/chrome-999.md

  Solutions:
  1. Check if version 999 is released yet (latest is 143)
  2. Try a different version: "Process Chrome 143"
  3. Download release notes from: https://developer.chrome.com/release-notes/
```

## Technical Notes

- The skill calls the processing pipeline directly via Python imports
- Uses `uv run` to ensure correct environment and dependencies
- Progress is streamed in real-time via print statements
- All outputs written to `upstream_docs/processed_releasenotes/processed_forwebplatform/areas/`
- Supports both stable and beta channels
- Handles 23 predefined focus areas (see config/focus_areas.yaml)
