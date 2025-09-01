# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment Setup

- **Virtual Environment**: All dependencies are installed in `.venv`. Always activate before running commands:
  ```bash
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
  ```
- **WSL Environment**: Use `python3` command instead of `python`
- **Project Planning**: Use phase-based planning (Phase 1, Phase 2, etc.) instead of week-based timelines

## Chrome Release Notes Data Characteristics

### File Structure and Channels
Chrome releases follow a structured pattern with multiple channels:

```
upstream_docs/release_notes/WebPlatform/
├── chrome-{version}.md          # Stable channel (most common)
├── chrome-{version}-stable.md   # Explicit stable channel  
├── chrome-{version}-beta.md     # Beta channel (earlier features)
└── webgpu-{version}.md          # Dedicated WebGPU release notes
```

**Channel Differences**:
- **Beta**: Earlier release (e.g., Chrome 139 beta in June 2025)
- **Stable**: Later release (e.g., Chrome 139 stable in August 2025)
- **Content**: Beta may have fewer features, different focus areas

### Heading Hierarchy Patterns

Chrome release notes use **inconsistent heading hierarchies** across versions:

**Pattern 1: Standard (Most Chrome releases)**
```
# Chrome {version}           # h1 - main title
## CSS and UI               # h2 - feature areas/sections  
### Feature Name            # h3 - individual features
```

**Pattern 2: WebGPU-style (WebGPU 138, some versions)**
```
# What's New in WebGPU      # h1 - main title
## Feature Name             # h2 - individual features (no sections)
```

**Pattern 3: Mixed (WebGPU 139, complex releases)**
```
# What's New in WebGPU      # h1 - main title
## Feature Name             # h2 - individual features
### Enable the feature      # h3 - sub-content within feature
```

**Critical Rule**: Always detect hierarchy dynamically. Never assume h2 = sections and h3 = features.

### WebGPU Special Characteristics

WebGPU has **dual release note structure**:
1. **Chrome Graphics section**: WebGPU features mixed with other graphics features
2. **Dedicated WebGPU notes**: `webgpu-{version}.md` with detailed WebGPU-specific content

**WebGPU Processing Requirements**:
- Extract from both sources
- Deduplicate with WebGPU-specific content taking priority
- Handle different heading structures (h2-only vs h2+h3)
- Clean metadata but preserve technical content and code examples

### Content Structure Evolution

**Stable Patterns**:
- CSS and UI (most versions)
- Web APIs (most versions) 
- Security (most versions)
- Origin Trials (most versions)

**Variable Patterns**:
- Graphics (sometimes merged with WebGPU)
- Performance (not always present)
- JavaScript (inconsistent)
- Deprecations and Removals (most versions)

**Special Areas**:
- **on-device-ai**: Keyword-based extraction from multiple sections
- **graphics-webgpu**: Multi-source merging with deduplication

## Processing Pipeline Commands

### Clean Data Pipeline (Recommended)
```bash
# Process stable channel
python3 src/processors/clean_data_pipeline.py --version {VERSION} --with-yaml

# Process beta channel
python3 src/processors/clean_data_pipeline.py --version {VERSION} --channel beta --with-yaml

# Validation only
python3 src/processors/clean_data_pipeline.py --version {VERSION} --validate-only
```

### Legacy Pipeline (Deprecated)
```bash
python3 src/processors/split_and_process_release_notes.py --version {VERSION}
```

## Architecture Overview

### MCP Server
FastMCP-based server providing:
- **Tools**: `enterprise_digest`, `webplatform_digest`, `merged_digest_html`
- **Resources**: Prompts, keywords, processed release notes
- **Sampling**: AI-powered content analysis

### Processing Flow
```
Raw Release Notes → Clean Data Pipeline → Area-Specific YAML → Digest Generation
                                      → Area-Specific Markdown
```

### Output Structure
```
upstream_docs/processed_releasenotes/processed_forwebplatform/areas/
├── css/
│   ├── chrome-{version}-{channel}.md                    # Human-readable content  
│   └── chrome-{version}-{channel}.yml                   # Structured data
├── webapi/
│   ├── chrome-{version}-{channel}.md                    # Human-readable content
│   └── chrome-{version}-{channel}.yml                   # Structured data
└── graphics-webgpu/
    ├── chrome-{version}-{channel}.md                    # Human-readable content
    └── chrome-{version}-{channel}.yml                   # Structured data
```

## Key Implementation Patterns

### Dynamic Hierarchy Detection
```python
# Never hardcode hierarchy assumptions
hierarchy = detect_heading_hierarchy(content)  # Analyze first
sections = parse_sections_dynamic(content, hierarchy)  # Then parse
```

### Multi-Channel Support
```python
# Smart file discovery with fallbacks
if channel == "stable":
    try chrome-{version}.md, fallback to chrome-{version}-stable.md
else:
    use chrome-{version}-{channel}.md
```

### WebGPU Deduplication
```python
# Priority: WebGPU-specific > Chrome Graphics
unique_features = deduplicate_features(chrome_features, webgpu_features)
# WebGPU features take precedence when duplicates found
```

## Area Classification Logic

Areas are defined in `config/focus_areas.yaml`:

- **Most areas**: Exact h2 heading pattern matching
- **on-device-ai**: Content keyword search across multiple sections
- **graphics-webgpu**: Multi-source merging with deduplication
- **payment**: Partial heading matching ("payment" substring)
- **devtools**: Partial heading matching ("developer tools" substring)

## Quality Assurance Checklist

### WebGPU Validation
- Feature count: 3-6 features per version expected
- Content completeness: Technical details and code examples preserved  
- Deduplication working: No duplicate features between Chrome/WebGPU sources

### Multi-Area Features
- AI features appear in both origin-trials and on-device-ai areas
- Feature content includes complete context and references
- Cross-cutting concerns properly tagged

### Structural Integrity  
- Heading hierarchy preserved in processed files
- Links and references maintained
- No truncated content or missing sections

## Testing

```bash
# Run all tests
pytest tests/ -v

# Test specific functionality
pytest tests/test_process_enterprise_release.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## Debugging

- **Temp scripts**: Save debugging scripts to `/temp-save/`
- **Hierarchy analysis**: Use test scripts to verify heading detection
- **Content validation**: Check area-specific YAML for semantic accuracy
- **Multi-version comparison**: Compare feature counts across versions for consistency

## Critical Success Factors

1. **Content-driven parsing**: Analyze document structure before applying logic
2. **Semantic accuracy**: Features must include complete context (including sub-headings)
3. **Multi-version compatibility**: Single pipeline handles different release note formats
4. **Channel awareness**: Process both stable and beta channels appropriately
5. **WebGPU specialization**: Handle dual-source WebGPU content correctly