# Implementation Guide

Detailed step-by-step guide for implementing the chrome-update-digest skill.

## Overview

This guide provides detailed implementation steps for Claude Agent when executing the skill.

## Request Parsing

When the user triggers this skill with a request like "Process Chrome 143", extract:

- **Version number** (required): e.g., 143, 144
- **Channel** (optional): stable (default) or beta
- **Language** (optional): bilingual (default), en, or zh
- **Areas** (optional): specific areas or all (default)

## Step-by-Step Implementation

### Step 1: Validate Inputs

Check version format is valid (digits only: 143, 144, etc.)

Optionally check latest available version:
```bash
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py --check-latest
```

**Note**: Release notes will be auto-downloaded if missing, so validation is optional.

### Step 2: Execute Processing Script

Run the main orchestration script:
```bash
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
  --version {version} \
  --channel {channel}
```

This step:
- Downloads missing release notes (Chrome + WebGPU if available)
- Extracts area-specific YAML and markdown
- Generates GitHub Pages navigation

### Step 3: Get Extracted Areas

Query which areas were extracted:
```bash
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
  --version {version} \
  --channel {channel} \
  --list-areas
```

Expected output: ~23 areas (css, webapi, graphics-webgpu, javascript, etc.)

### Step 4: Generate AI Digests

For each area from Step 3, launch agents to generate digests in parallel.

#### English Digest Generation

For each area:

1. **Read prompt template**: `.claude/skills/chrome-update-digest/prompts/webplatform-prompt-en.md`

2. **Replace variables**:
   - `[AREA]` → area name (e.g., "css", "webapi")
   - `[version]` → version number (e.g., "143")
   - `[channel]` → channel (e.g., "stable", "beta")

3. **Read input YAML**: `upstream_docs/processed_releasenotes/processed_forwebplatform/areas/{area}/chrome-{version}-{channel}.yml`

4. **Generate digest**: Use Task tool with general-purpose agent

5. **Save output**: `digest_markdown/webplatform/{area}/chrome-{version}-{channel}-en.md`

#### Chinese Translation

For each area:

1. **Read prompt template**: `.claude/skills/chrome-update-digest/prompts/webplatform-translation-prompt-zh.md`

2. **Replace variables**: Same as English (`[AREA]`, `[version]`, `[channel]`)

3. **Read input**: English digest from previous step

4. **Generate translation**: Use Task tool with general-purpose agent

5. **Save output**: `digest_markdown/webplatform/{area}/chrome-{version}-{channel}-zh.md`

**Performance Optimization**: Process all areas in parallel for maximum efficiency.

### Step 5: Verify Completion

Navigation is auto-generated in Step 2, so no additional action needed.

### Step 6: Report Results

Stream progress updates and show completion status:
- Processed areas count
- Output paths
- Next steps (review, commit)

If errors occur, provide troubleshooting guidance (see [error_handling.md](error_handling.md)).

## Agent Integration Details

### Task Tool Parameters

**For English digest generation**:
```
tool: Task
subagent_type: general-purpose
prompt: {processed prompt with variables replaced}
description: "Generate English digest for {area}"
```

**For Chinese translation**:
```
tool: Task
subagent_type: general-purpose
prompt: {processed prompt with variables replaced}
description: "Translate {area} digest to Chinese"
```

### Parallel Processing Strategy

Launch all agents simultaneously:
- 23 English digest agents
- 23 Chinese translation agents
- Total: 46 parallel agents

Monitor progress and handle failures gracefully.

## Variable Replacement Rules

1. **Exact match**: Replace all occurrences of template variables
2. **Case sensitive**: Use exact casing (`[AREA]`, not `[area]`)
3. **Context preservation**: Keep surrounding text unchanged
4. **No escaping**: Plain text replacement

## Error Handling

See [error_handling.md](error_handling.md) for comprehensive error scenarios and solutions.

## Validation

See [testing_validation.md](testing_validation.md) for post-processing validation steps.

## Examples

See SKILL.md Examples section for complete execution examples.
