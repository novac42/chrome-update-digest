---
name: chrome-update-digest
description: Transform Chrome and WebGPU release notes into multilingual digests for 23 focus areas. Trigger phrases "process Chrome X", "what's the latest Chrome version".
---

# Chrome Update Digest

Process Chrome release notes into structured, multilingual digests for 23 focus areas.

## Design Principles

**Stateless Processing**:
- No version history tracking - each run is independent
- Only processes the specified version (e.g., "Process Chrome 143")
- Does not track what versions have been processed before

**Self-contained & Portable**:
- Vendored dependencies - no external package dependencies
- Bundled prompts for AI digest generation
- No dependencies on repo files outside the skill directory
- Works independently after MCP separation

**Dual-source Release Notes**:
- **Chrome release notes** (required): `chrome-{version}-{channel}.md`
- **WebGPU release notes** (optional): `webgpu-{version}.md`
- WebGPU enhances the `graphics-webgpu` area when available but is not required

**Agent Delegation**:
- Skill orchestrates the workflow (download → extract → generate navigation)
- AI digest generation delegated to agents with bundled prompts
- Agents process all 23 areas in parallel for efficiency

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

## Quick Reference (For Claude Agent)

### Workflow Overview

When user says **"Process Chrome 143"**:

```bash
# Step 1: Extract areas (automatic download if missing)
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py --version 143

# Step 2: Get area list
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py --version 143 --list-areas
# Output: 23 areas (css, webapi, graphics-webgpu, etc.)

# Step 3: Generate digests (spawn agents in parallel)
# For each area:
#   - English: Read prompts/webplatform-prompt-en.md → Generate EN digest
#   - Chinese: Read prompts/webplatform-translation-prompt-zh.md → Generate ZH digest

# Step 4: Done! Navigation auto-generated in step 1
```

### Commands Cheat Sheet

| Command | Purpose |
|---------|---------|
| `--check-latest` | Check latest Chrome stable/beta versions |
| `--version 143` | Process Chrome version 143 |
| `--channel beta` | Process beta channel (default: stable) |
| `--list-areas` | List extracted areas for a version |

### Agent Integration

**Generate English Digest**:
1. Read: `prompts/webplatform-prompt-en.md`
2. Replace: `[AREA]` → area name, `[version]` → 143, `[channel]` → stable
3. Input: `upstream_docs/.../areas/{area}/chrome-143-stable.yml`
4. Output: `digest_markdown/webplatform/{area}/chrome-143-stable-en.md`

**Generate Chinese Translation**:
1. Read: `prompts/webplatform-translation-prompt-zh.md`
2. Replace: `[AREA]`, `[version]`, `[channel]` with actual values
3. Input: English digest from previous step
4. Output: `digest_markdown/webplatform/{area}/chrome-143-stable-zh.md`

Process all 23 areas in parallel for efficiency.

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

## Reference Documentation

- **[Focus Areas](references/focus_areas.md)** - 23 focus areas definition
- **[Implementation Guide](references/implementation_guide.md)** - Detailed step-by-step implementation
- **[Error Handling](references/error_handling.md)** - Comprehensive error scenarios and solutions
- **[Testing & Validation](references/testing_validation.md)** - Post-processing validation checklist
- **[Common Issues](references/common_issues.md)** - Troubleshooting guide
- **[Prompts Usage](prompts/README.md)** - Prompt template documentation

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

### Example 2: Check latest version
```
User: "What's the latest Chrome version?"
Assistant:
  Checking latest Chrome versions...

  Latest Chrome versions:
    Stable: 143 (2026-01-15)
    Beta:   144 (2026-01-10)

  To process: "Process Chrome 143" or "Process Chrome 144 beta"
```

### Example 3: Beta channel
```
User: "Process Chrome 143 beta"
Assistant:
  Parsing request: version=143, channel=beta
  Validating inputs... ✓

  [Processing output similar to Example 1, but for beta channel...]
```

### Example 4: Error handling
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

- **Stateless Design**: No version history tracking - each run is independent
- **Self-contained**: Vendored dependencies, no external package requirements
- **Dual-source Release Notes**:
  * Chrome WebPlatform (required): Main release notes
  * WebGPU (optional): Enhances graphics-webgpu area when available
- The skill orchestrates processing workflow via `process_chrome.py`
- Uses `uv run` to ensure correct environment and dependencies
- Progress is streamed in real-time
- **AI Digest Generation**:
  * Uses Task tool with general-purpose agents
  * Processes all areas in parallel for efficiency
  * Bundled prompts: English digest + Chinese translation (see [prompts/README.md](prompts/README.md))
  * Each agent receives YAML content and produces markdown digest
- **Helper Functions**:
  * `--check-latest`: Query latest Chrome stable/beta versions (stateless)
  * `--list-areas`: List areas extracted for a specific version
  * `get_areas_to_process()`: Python helper for agent integration
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
