# Digest Generation Prompts

This directory contains the AI prompts used to generate bilingual Chrome update digests.

## Prompt Files

### 1. English Digest: `webplatform-prompt-en.md`

Generates English digests from area-specific YAML data.

**Template Variables**:
- `[AREA]`: Focus area name (e.g., `css`, `webapi`, `graphics-webgpu`)
- `[version]`: Chrome version number (e.g., `143`)
- `[channel]`: Release channel (`stable` or `beta`)

**Input**:
```
upstream_docs/processed_releasenotes/processed_forwebplatform/areas/{area}/chrome-{version}-{channel}.yml
```

**Output**:
```
digest_markdown/webplatform/{area}/chrome-{version}-{channel}-en.md
```

**Agent Usage**:
1. Read the prompt file
2. Replace `[AREA]`, `[version]`, `[channel]` with actual values
3. Provide the YAML file content as input
4. Save generated markdown to output path

**Example**:
```
Area: css
Version: 143
Channel: stable

Input:  upstream_docs/.../areas/css/chrome-143-stable.yml
Output: digest_markdown/webplatform/css/chrome-143-stable-en.md
```

---

### 2. Chinese Translation: `webplatform-translation-prompt-zh.md`

Translates English digests to Chinese while preserving technical accuracy.

**Template Variables**:
- `[AREA]`: Focus area name
- `[version]`: Chrome version number
- `[channel]`: Release channel

**Input**:
```
digest_markdown/webplatform/{area}/chrome-{version}-{channel}-en.md
```

**Output**:
```
digest_markdown/webplatform/{area}/chrome-{version}-{channel}-zh.md
```

**Agent Usage**:
1. Read the prompt file
2. Replace `[AREA]`, `[version]`, `[channel]` with actual values
3. Provide the English digest markdown as input
4. Save translated markdown to output path

**Example**:
```
Area: css
Version: 143
Channel: stable

Input:  digest_markdown/webplatform/css/chrome-143-stable-en.md
Output: digest_markdown/webplatform/css/chrome-143-stable-zh.md
```

---

## Workflow Integration

The skill orchestrates digest generation through these steps:

### Step 1: Extract Areas (Automated)
```bash
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
  --version 143 \
  --channel stable
```

This extracts YAML files for all 23 focus areas.

### Step 2: Check Extracted Areas
```bash
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
  --version 143 \
  --channel stable \
  --list-areas
```

Output example:
```
Found 23 areas:
  - css
  - webapi
  - graphics-webgpu
  - javascript
  - ...
```

### Step 3: Generate Digests (Agent Delegation)

For each area, the skill spawns agents in parallel:

**English Digest Agent**:
- Prompt: `prompts/webplatform-prompt-en.md`
- Replace: `[AREA]` → actual area name
- Input: YAML file from Step 1
- Output: English markdown digest

**Chinese Translation Agent**:
- Prompt: `prompts/webplatform-translation-prompt-zh.md`
- Replace: `[AREA]` → actual area name
- Input: English markdown from previous agent
- Output: Chinese markdown digest

### Step 4: Verify Outputs

Expected structure:
```
digest_markdown/webplatform/
├── css/
│   ├── chrome-143-stable-en.md
│   └── chrome-143-stable-zh.md
├── webapi/
│   ├── chrome-143-stable-en.md
│   └── chrome-143-stable-zh.md
├── graphics-webgpu/
│   ├── chrome-143-stable-en.md
│   └── chrome-143-stable-zh.md
└── ... (20 more areas)
```

---

## Variable Replacement Rules

1. **Exact Match**: Replace all occurrences of template variables
2. **Case Sensitive**: Variables are case-sensitive (use exact casing)
3. **Context Preservation**: Keep surrounding text unchanged
4. **No Escaping**: Variables don't need escaping (plain text replacement)

**Template Variables**:
- `[AREA]` → Area name from config/focus_areas.yaml
- `[version]` → Chrome version number (digits only, e.g., "143")
- `[channel]` → Either "stable" or "beta"

**Common Mistakes to Avoid**:
- ❌ `[VERSION]` (wrong casing)
- ❌ `Chrome 143` for `[version]` (should be just "143")
- ❌ Forgetting to replace variables in file paths

---

## Quality Checks

After digest generation, verify:

1. **File Existence**: All expected digest files created
2. **Content Structure**: Markdown has correct heading hierarchy
3. **Links**: All links formatted as `[text](url)`, no bare URLs
4. **Language**: English digests contain no Chinese, and vice versa
5. **Completeness**: All features from YAML included in digest

---

## Troubleshooting

**Problem**: Agent generates incomplete digest

**Solution**:
- Check YAML file has all features
- Verify prompt variables were replaced correctly
- Ensure agent has access to full YAML content

**Problem**: Links not formatted correctly

**Solution**:
- Prompts explicitly require `[text](url)` format
- Check agent output matches format requirements
- Re-run with explicit link formatting instruction

**Problem**: Mixed language content

**Solution**:
- English prompt specifies "English only"
- Chinese prompt preserves English technical terms
- Verify correct prompt was used for each language

---

## Notes

- **Stateless**: Each digest generation is independent
- **Parallel Processing**: All areas processed simultaneously
- **Idempotent**: Re-running overwrites previous digests
- **Self-contained**: Prompts bundle all necessary instructions
