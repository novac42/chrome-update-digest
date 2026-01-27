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

**Core Features**:
- ✓ Extracts structured data from release notes into 23+ focus areas
- ✓ Generates AI-powered bilingual digests (English + Chinese)
- ✓ Creates GitHub Pages navigation (dual structure: by-version & by-area)

## Workflow

The skill executes these steps automatically:

1. **Validate**: Check version format and input files exist
2. **Clean Pipeline**: Extract area-specific YAML and markdown from raw release notes
3. **Generate AI Digests**: Use agent with bundled prompts to create bilingual summaries
   - English digest: Use agent with `prompts/webplatform-prompt-en.md`
   - Chinese translation: Use agent with `prompts/webplatform-translation-prompt-zh.md`
4. **Generate Navigation**: Create GitHub Pages navigation structure (by-version & by-area)
5. **Output**: Save digest files and navigation to respective directories

## Processing Options

**Channel**: stable (default) or beta
**Output**: Area-specific markdown + YAML files + GitHub Pages navigation

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
     --verbose
   ```
   This extracts area-specific YAML and markdown from raw release notes.

4. **Generate AI digests for each area** (bilingual: English + Chinese):
   - For each area found in step 3, launch agents to generate digests
   - **English digest**: Use Task tool with general-purpose agent
     - Provide the area's YAML file content
     - Use the bundled English prompt: `.claude/skills/chrome-update-digest/prompts/webplatform-prompt-en.md`
     - Save output to: `digest_markdown/webplatform/{area}/chrome-{version}-{channel}-en.md`
   - **Chinese translation**: Use Task tool with general-purpose agent
     - Provide the English digest content
     - Use the bundled Chinese prompt: `.claude/skills/chrome-update-digest/prompts/webplatform-translation-prompt-zh.md`
     - Save output to: `digest_markdown/webplatform/{area}/chrome-{version}-{channel}-zh.md`
   - Process all areas in parallel for efficiency

5. **Generate GitHub Pages navigation**:
   ```bash
   uv run python .claude/skills/chrome-update-digest/scripts/generate_navigation.py
   ```
   This creates the dual navigation structure (by-version and by-area).

6. **Report progress and results**:
   - Stream progress updates from the script
   - Show completion status with output paths
   - If errors occur, provide troubleshooting guidance

## Examples

### Example 1: Simple request with defaults
```
User: "Process Chrome 143"
Assistant:
  Parsing request: version=143, channel=stable
  Validating inputs... ✓

  🚀 Processing Chrome 143 (stable)

  [1/4] Running clean data pipeline...
    ✓ Extracted 23 focus areas
    ✓ Generated YAML and markdown files

  [2/4] Generating AI digests for 23 areas...
    Launching agents in parallel for English digests...
    ✓ css (English)
    ✓ webapi (English)
    ✓ graphics-webgpu (English)
    ... (20 more areas)

    Launching agents in parallel for Chinese translations...
    ✓ css (Chinese)
    ✓ webapi (Chinese)
    ✓ graphics-webgpu (Chinese)
    ... (20 more areas)

  [3/4] Generating GitHub Pages navigation...
    ✓ Created version-centric pages
    ✓ Created area-centric pages

  [4/4] Validation...
    ✓ All digest files generated
    ✓ Navigation includes Chrome 143

  ✅ Processing complete!
     Processed areas: upstream_docs/processed_releasenotes/processed_forwebplatform/areas/
     AI Digests: digest_markdown/webplatform/
     Navigation: digest_markdown/areas/ and digest_markdown/versions/

  💡 Next steps:
     1. Review generated digests in digest_markdown/webplatform/
     2. Commit changes to trigger GitHub Pages deployment
```

### Example 2: Beta channel
```
User: "Process Chrome 143 beta"
Assistant:
  Parsing request: version=143, channel=beta
  Validating inputs... ✓

  [Processing output similar to Example 1, but for beta channel...]
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

- The skill orchestrates existing CLI tools (chrome-update-digest-cli)
- Uses `uv run` to ensure correct environment and dependencies
- Progress is streamed in real-time
- **AI Digest Generation**:
  * Uses Task tool with general-purpose agents
  * Processes all areas in parallel for efficiency
  * Bundled prompts: English digest + Chinese translation
  * Each agent receives YAML content and produces markdown digest
- Outputs:
  * Processed files: `upstream_docs/processed_releasenotes/processed_forwebplatform/areas/`
  * AI Digests: `digest_markdown/webplatform/{area}/chrome-{version}-{channel}-{lang}.md`
  * Navigation: `digest_markdown/areas/` and `digest_markdown/versions/`
- Supports both stable and beta channels
- Handles 23+ predefined focus areas (see config/focus_areas.yaml)
- Bundles configuration and prompts for portability
- Integrates with GitHub Actions for automatic deployment

## Prompt Details

The skill includes two bundled prompts for AI digest generation:

1. **English Digest Prompt** ([prompts/webplatform-prompt-en.md](prompts/webplatform-prompt-en.md))
   - Input: Area-specific YAML file
   - Output: Structured English digest with feature descriptions
   - Format: Markdown with consistent structure

2. **Chinese Translation Prompt** ([prompts/webplatform-translation-prompt-zh.md](prompts/webplatform-translation-prompt-zh.md))
   - Input: English digest content
   - Output: Chinese translation maintaining technical accuracy
   - Format: Preserves markdown structure and links
