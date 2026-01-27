# Implementation Plan: Chrome Update Digest as Claude Skill

## Overview

Convert the Chrome Update Digest workflow from MCP-based orchestration to a Claude Code Skill-based implementation. The skill will provide a streamlined, conversational interface while calling the processing pipeline directly for better performance.

## Architecture Comparison

### Current (MCP-Based)
```
User → MCP Client → MCP Server Tools → Processing Pipeline
                   ↓
        (Manual tool orchestration)
```

### Proposed (Skill-Based)
```
User → Claude Skill → Processing Pipeline (direct Python imports)
       ↓
   (Conversational, adaptive interaction)
```

## Key Design Decisions

### 1. Skill Scope
**Decision**: Create a **single workflow-oriented skill** with adaptive interaction

**Rationale**:
- Skills excel at multi-step workflows with conversational guidance
- Users want to say "process Chrome 139" not manually orchestrate steps
- Skill handles simple cases with smart defaults, asks questions for complex cases
- MCP tools remain available for programmatic/automation usage

### 2. Skill Implementation Strategy
**Decision**: Direct implementation (bypasses MCP layer)

**Chosen Approach**:
- Skill imports and calls processing pipeline Python modules directly
- Better performance (no MCP server overhead, no serialization)
- Cleaner architecture for skill-based workflows
- Simpler error handling and progress reporting

**Trade-offs Accepted**:
- Some orchestration logic duplicated between MCP and Skill
- Need to keep both interfaces updated if core processing changes
- Migration path: MCP deprecation after skill adoption (6-12 months)

### 3. User Interaction Model
**Decision**: Adaptive interaction (minimal for simple, guided for complex)

**Simple Request (Smart Defaults)**:
```
User: "Process Chrome 139"
Skill: [Validates inputs, uses defaults: stable + bilingual + all areas]
       "Processing Chrome 139 (stable, bilingual)...

       [1/4] Running clean data pipeline
       [2/4] Generating English digests (23 areas)
       [3/4] Translating to Chinese
       [4/4] Writing outputs

       ✓ Complete! Generated digests for 23 areas."
```

**Complex Request (Guided)**:
```
User: "Process Chrome 139 for specific areas in English only"
Skill: "Which areas do you want to process?
       Common: css, webapi, graphics-webgpu, on-device-ai, security-privacy
       All 23 areas: [shows full list]"

User: "Just css and webapi"
Skill: "Processing Chrome 139 (stable, English only, 2 areas)...
       [Progress...]"
```

### 4. Migration Strategy
**Decision**: Replace MCP over 6-12 months

**Approach**:
- Phase 1: Skill + MCP coexist (both functional)
- Phase 2: Skill becomes primary interface
- Phase 3: MCP marked deprecated after skill adoption
- Phase 4: MCP removal (if warranted)

**Coexistence Benefits**:
- No breaking changes for existing MCP users
- Gradual migration at user's pace
- Skill and MCP can share processing pipeline code
- Safety net if skill has issues

## Implementation Structure

### Skill Directory Layout

```
.claude/skills/chrome-update-digest/
├── SKILL.md                          # Required: Skill definition
├── scripts/
│   ├── init_skill.py                 # Helper: Initialize skill skeleton
│   └── package_skill.py              # Helper: Package into .skill file
└── references/
    ├── focus_areas.md                # Reference: 23 area definitions
    └── common_issues.md              # Reference: Troubleshooting guide
```

### SKILL.md Structure

```markdown
---
name: chrome-update-digest
description: Process Chrome release notes into multilingual, area-specific digests. Use when the user wants to: (1) Process Chrome release notes for a specific version, (2) Generate digests for Web Platform updates, (3) Translate Chrome features to Chinese, (4) Prepare area-specific summaries (CSS, WebAPI, WebGPU, AI, etc.). Trigger phrases: "process Chrome X", "digest Chrome release notes", "translate Chrome X features".
---

# Chrome Update Digest

Process Chrome release notes into structured, multilingual digests for 23 focus areas.

## Quick Start

**Simple usage (smart defaults)**:
```
Process Chrome 139
```
Uses: stable channel, bilingual (en+zh), all 23 areas

**Custom usage**:
```
Process Chrome 139 beta in English for CSS and WebAPI
```

## Workflow

The skill executes these steps automatically:

1. **Validate**: Check version format and input files exist
2. **Clean Pipeline**: Run `clean_data_pipeline.py` to extract area-specific YAML
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
```

### Python Script Structure (scripts/process_chrome.py)

This is the main orchestration script called by the skill:

```python
#!/usr/bin/env python3
"""Chrome Update Digest Processing Script"""
import sys
from pathlib import Path
from typing import List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from chrome_update_digest.processors.clean_data_pipeline import (
    process_version_with_yaml
)
from chrome_update_digest.utils.digest_generation import generate_area_digest
from chrome_update_digest.utils.digest_translation import translate_digest
from chrome_update_digest.utils.io_utils import persist_output


def process_chrome_release(
    version: str,
    channel: str = "stable",
    language: str = "bilingual",
    areas: Optional[List[str]] = None,
    verbose: bool = False
) -> dict:
    """Main processing function"""

    # Step 1: Validate inputs
    _validate_inputs(version, channel)

    # Step 2: Run clean data pipeline
    if verbose:
        print(f"[1/4] Running clean data pipeline for Chrome {version}...")
    process_version_with_yaml(version, channel)

    # Step 3: Load processed areas
    areas_to_process = areas or _get_all_areas()

    # Step 4: Generate English digests
    if verbose:
        print(f"[2/4] Generating English digests ({len(areas_to_process)} areas)...")
    for area in areas_to_process:
        generate_area_digest(version, channel, area, "en")

    # Step 5: Translate if needed
    if language in ("bilingual", "zh"):
        if verbose:
            print(f"[3/4] Translating to Chinese...")
        for area in areas_to_process:
            translate_digest(version, channel, area)

    # Step 6: Report completion
    if verbose:
        print(f"[4/4] Complete!")

    return {
        "version": version,
        "channel": channel,
        "language": language,
        "areas": areas_to_process,
        "output_path": _get_output_path(version, channel)
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--channel", default="stable")
    parser.add_argument("--language", default="bilingual")
    parser.add_argument("--areas", nargs="+")
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()
    result = process_chrome_release(
        args.version,
        args.channel,
        args.language,
        args.areas,
        args.verbose
    )
    print(f"✓ Generated digests: {result['output_path']}")
```

## Implementation Phases

### Phase 1: Skill Skeleton & Core Workflow
**Goal**: Create functional skill with basic Chrome processing

**Tasks**:
1. Run `scripts/init_skill.py chrome-update-digest --path .claude/skills/`
2. Write SKILL.md frontmatter (name + description with triggers)
3. Write SKILL.md body (workflow overview, usage examples)
4. Create `scripts/process_chrome.py` orchestration script
5. Implement core processing flow (validate → clean pipeline → generate)
6. Test with Chrome 139 stable (full workflow)

**Success Criteria**:
- User says "Process Chrome 139" → skill triggers
- Skill validates input files exist
- Runs clean data pipeline
- Generates English digests for all 23 areas
- No errors, outputs written to correct paths

### Phase 2: Enhanced User Experience
**Goal**: Add translation support, adaptive interaction, and error handling

**Tasks**:
1. Implement translation module (calls LLM with translation prompts)
2. Add adaptive interaction logic (detect "specific areas" requests)
3. Implement graceful error handling with recovery suggestions
4. Add progress reporting (real-time status updates)
5. Create reference files (focus_areas.md, common_issues.md)
6. Test bilingual workflow and partial area processing

**Success Criteria**:
- Bilingual workflow generates both en/zh outputs
- "Process Chrome 139 for CSS" → only processes CSS area
- Missing input files show helpful error with guidance
- Progress updates visible during long-running generation

### Phase 3: Advanced Features & Polish
**Goal**: Support complex workflows and edge cases

**Tasks**:
1. Auto-detect latest Chrome version ("process latest Chrome")
2. Batch processing support ("process Chrome 138, 139, 140")
3. Differential analysis ("compare Chrome 138 vs 139")
4. Link validation after generation
5. Integration with GitHub Pages workflow
6. Performance optimization for large-scale processing

**Success Criteria**:
- "Process latest Chrome" auto-detects version 143
- Batch processing handles multiple versions sequentially
- Compare functionality shows feature differences
- All links validated after digest generation

### Phase 4: Testing & Documentation
**Goal**: Production-ready skill with comprehensive docs and tests

**Tasks**:
1. Create user documentation (usage examples, troubleshooting)
2. Write integration tests (test full workflow)
3. Performance benchmarks (compare to MCP workflow)
4. Migration guide (MCP → Skill transition)
5. Package skill into .skill file for distribution

**Success Criteria**:
- All tests pass on Chrome 135-143
- Documentation covers all use cases
- Skill performs ≥20% faster than MCP workflow
- Package validates and installs successfully

## Critical Files

### New Files to Create

1. [.claude/skills/chrome-update-digest/SKILL.md](.claude/skills/chrome-update-digest/SKILL.md)
   - Skill metadata and workflow instructions
   - Core skill definition and triggers

2. [.claude/skills/chrome-update-digest/scripts/process_chrome.py](.claude/skills/chrome-update-digest/scripts/process_chrome.py)
   - Main orchestration script
   - Direct Python calls to processing pipeline

3. [.claude/skills/chrome-update-digest/references/focus_areas.md](.claude/skills/chrome-update-digest/references/focus_areas.md)
   - Documentation of 23 focus areas
   - Area descriptions and extraction patterns

4. [.claude/skills/chrome-update-digest/references/common_issues.md](.claude/skills/chrome-update-digest/references/common_issues.md)
   - Troubleshooting guide
   - Common errors and solutions

### Existing Files to Reference (No Modifications)

These files contain the core processing logic that the skill will call:

1. [src/chrome_update_digest/processors/clean_data_pipeline.py](src/chrome_update_digest/processors/clean_data_pipeline.py)
   - `process_version_with_yaml()` - Main pipeline entry point

2. [src/chrome_update_digest/utils/release_note_locator.py](src/chrome_update_digest/utils/release_note_locator.py)
   - `find_chrome_release_note()` - Locate input files

3. [src/chrome_update_digest/processors/area_extractors.py](src/chrome_update_digest/processors/area_extractors.py)
   - Area extraction strategies

4. [config/focus_areas.yaml](config/focus_areas.yaml)
   - Area definitions and patterns

5. [src/chrome_update_digest/mcp/](src/chrome_update_digest/mcp/)
   - MCP server (preserved for coexistence)

## Technical Implementation Details

### Parameter Parsing Strategy

The skill needs to parse natural language requests into structured parameters:

```
"Process Chrome 139"
  → version=139, channel=stable, language=bilingual, areas=None

"Process Chrome 139 beta"
  → version=139, channel=beta, language=bilingual, areas=None

"Process Chrome 139 in English for CSS and WebAPI"
  → version=139, channel=stable, language=en, areas=["css", "webapi"]

"Translate Chrome 138 to Chinese"
  → version=138, channel=stable, language=zh, areas=None
```

**Implementation**: Use Claude's natural language understanding + regex extraction

### Progress Reporting Approach

Since skill execution blocks Claude's conversation, progress must be streamed:

```python
def process_chrome_release(...):
    print(f"[1/4] Running clean data pipeline...")
    process_version_with_yaml(version, channel)

    print(f"[2/4] Generating English digests (0/{len(areas)} complete)...")
    for i, area in enumerate(areas, 1):
        generate_area_digest(...)
        print(f"  {i}/{len(areas)} complete: {area}")
```

**Output Visible to User**: All `print()` statements from scripts appear in Claude's response

### Error Handling Philosophy

**Fail Fast with Actionable Guidance**:

```python
# Bad
raise FileNotFoundError("chrome-139.md not found")

# Good
raise FileNotFoundError(
    f"Chrome 139 release notes not found.\n"
    f"Expected: upstream_docs/release_notes/WebPlatform/chrome-139.md\n\n"
    f"Solutions:\n"
    f"1. Download from: https://developer.chrome.com/release-notes/139\n"
    f"2. Check if version 139 is released yet\n"
    f"3. Try beta channel: 'Process Chrome 139 beta'"
)
```

### LLM Call Strategy for Digest Generation

**Problem**: Skill needs to call LLM for generating/translating digests

**Approach**: Use existing MCP LLM sampling infrastructure

```python
# Import from MCP modules
from chrome_update_digest.mcp._digest_generation import generate_area_digest_impl

# Reuse LLM sampling logic
english_digest = await generate_area_digest_impl(
    yaml_data=yaml_data,
    area=area,
    language="en",
    prompt_template=load_prompt("webplatform-prompt.txt")
)
```

**Benefits**:
- Reuses model preference resolution
- Preserves rate limiting and circuit breaker logic
- Shares prompt templates
- Minimal code duplication

## Testing Strategy

### Unit Tests (Optional for Phase 1)
- Focus on integration tests first
- Unit tests if time permits

### Integration Tests (Priority)

```bash
# Test 1: Basic workflow
test_process_chrome_139_stable_bilingual()

# Test 2: Custom parameters
test_process_chrome_139_beta_english_only()

# Test 3: Partial areas
test_process_chrome_139_css_only()

# Test 4: Error handling
test_missing_input_file_error()

# Test 5: Translation
test_translation_quality()
```

### Manual Testing Checklist

- [ ] Skill triggers on "Process Chrome 139"
- [ ] Smart defaults work (stable, bilingual, all areas)
- [ ] Custom parameters parsed correctly
- [ ] Progress visible during execution
- [ ] Error messages helpful and actionable
- [ ] Outputs written to correct paths
- [ ] Bilingual mode generates both en/zh
- [ ] Partial area processing works
- [ ] Performance acceptable (<5 min for full workflow)

## Success Metrics

### Adoption Targets (Phase 1)
- 5+ successful user workflows in first month
- 80%+ success rate (workflows completing without errors)
- <5 minutes for full workflow (23 areas, bilingual)

### Performance Baseline (Current MCP)
- Full workflow: ~8-10 minutes (from manual testing)
- Target: <5 minutes with direct Python calls

### User Experience Goals
- Zero manual tool orchestration (vs. 4+ MCP tool calls)
- Natural language requests (vs. structured tool parameters)
- Adaptive interaction (minimal questions for simple cases)

## Risk Mitigation

### Risk 1: LLM Sampling Complexity
**Issue**: Skill may not have direct access to Claude API for digest generation

**Mitigation**:
- Reuse existing MCP LLM sampling infrastructure
- Import `_digest_generation.py` functions directly
- Share model preferences and prompt templates

### Risk 2: Long Execution Time
**Issue**: Full workflow may take 5+ minutes, user waiting

**Mitigation**:
- Stream progress updates via print statements
- Show completion status after each area
- Consider async processing for future optimization

### Risk 3: Parameter Parsing Ambiguity
**Issue**: Natural language requests may be ambiguous

**Mitigation**:
- Smart defaults cover 80% of cases
- Adaptive questioning for ambiguous requests
- Clear examples in SKILL.md

### Risk 4: MCP-Skill Synchronization
**Issue**: Changes to processing pipeline affect both MCP and Skill

**Mitigation**:
- Share maximum code (both call same pipeline modules)
- Document integration points clearly
- Run integration tests for both interfaces

## Next Steps After Planning

1. Initialize skill directory structure
2. Create SKILL.md with frontmatter and workflow
3. Implement `scripts/process_chrome.py` orchestration
4. Test basic workflow (Chrome 139 stable, English only, all areas)
5. Add translation support
6. Create reference documentation
7. Package and distribute

## Open Questions

### Q1: Model Preferences in Skills
How should the skill handle model preferences for LLM calls?

**Options**:
- A: Use environment variables (WEBPLATFORM_MODEL)
- B: Add skill parameter (--model flag)
- C: Hardcode to gpt-4o-mini for cost efficiency

**Recommendation**: Option A (use existing env vars)

### Q2: Progress Updates
Should progress be real-time or batch reported?

**Options**:
- A: Real-time print() statements
- B: Batch report after each phase
- C: No progress (silent until complete)

**Recommendation**: Option A (real-time for transparency)

### Q3: Skill Distribution
How should the skill be distributed?

**Options**:
- A: Check into repo (.claude/skills/)
- B: Package as .skill file
- C: Both (repo for development, .skill for distribution)

**Recommendation**: Option C (both approaches)

## Summary

This plan converts Chrome Update Digest from MCP-based to skill-based with:

1. **Direct implementation**: Bypasses MCP layer for better performance
2. **Adaptive interaction**: Minimal prompts for simple cases, guided for complex
3. **Natural language**: "Process Chrome 139" instead of tool orchestration
4. **Migration path**: Coexistence → Primary → MCP deprecation over 6-12 months

**Key Benefits**:
- Faster execution (direct Python calls, no MCP serialization)
- Better UX (conversational, adaptive)
- Simpler for users (no tool orchestration knowledge needed)

**Key Trade-offs**:
- Some code duplication between MCP and Skill
- Both interfaces need maintenance during transition
- Eventual MCP deprecation requires user migration

The skill leverages Claude Code Skills' strengths (workflow orchestration, natural language) while preserving the robust processing pipeline already implemented.
