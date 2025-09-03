# 0901 TODO - Chrome Release Notes Processing & Digest Generation

## Objective
Generate processed files for additional Chrome versions and create WebPlatform digests using the refined clean data pipeline.

## Priority Tasks

### 1. Process Additional Chrome Versions
**Goal**: Generate area-specific YAML files for Chrome versions beyond 137

**Versions to Process**:
- [ ] Chrome 138 (stable)
- [ ] Chrome 139 (stable) 
- [ ] Chrome 136 (for WebGPU compatibility verification)

**Command Template**:
```bash
source .venv/bin/activate
# For stable channel (default):
PYTHONPATH=/Users/lyzh/Documents/EMSCodingTool/chrome-update-digest python3 src/processors/clean_data_pipeline.py --version [VERSION] --with-yaml

# For beta channel:
PYTHONPATH=/Users/lyzh/Documents/EMSCodingTool/chrome-update-digest python3 src/processors/clean_data_pipeline.py --version [VERSION] --channel beta --with-yaml
```

**Note**: The pipeline now supports `--channel` parameter (stable/beta) to handle versions with both stable and beta releases.

**Expected Outputs**:
- `upstream_docs/processed_releasenotes/processed_forwebplatform/areas/{area}/chrome-{version}-stable.md`
- `upstream_docs/processed_releasenotes/processed_forwebplatform/areas/{area}/chrome-{version}-stable.yml`

**Key Areas to Verify**:
- **graphics-webgpu**: All WebGPU features properly merged and deduplicated
- **on-device-ai**: Only AI features (no non-AI origin trials content)
- **css**: Complete CSS and UI features
- **webapi**: Web API features properly classified

### 2. WebGPU Multi-version Compatibility Check
**Goal**: Ensure WebGPU processing works across different file structures

**Tasks**:
- [ ] Verify Chrome 136 WebGPU processing (different structure)
- [ ] Verify Chrome 138 WebGPU processing 
- [ ] Verify Chrome 139 WebGPU processing
- [ ] Check WebGPU feature count consistency (should be 5+ features per version)

**Validation Points**:
- All 5 WebGPU features extracted from `webgpu-{version}.md`
- No duplicate features between Chrome Graphics and WebGPU sections
- Proper heading hierarchy preservation
- Clean metadata removal without content loss

### 3. Generate WebPlatform Digests
**Goal**: Create comprehensive WebPlatform digests using processed YAML files

**Current Status Check**: 
- [ ] Verify existing digest generation pipeline capabilities
- [ ] Check if by-area to full-version digest consolidation exists

**Approach Options**:
1. **MCP Tools Route** (Recommended):
   ```bash
   python fast_mcp_server.py
   # Use enhanced_webplatform_digest tool via MCP
   ```

2. **Direct Processing Route**:
   ```python
   from src.mcp_tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool
   # Process each version individually
   ```

**Digest Specifications**:
- **Format**: Single markdown file per version (consolidated from all areas)
- **Language**: English and Chinese versions  
- **Scope**: All focus areas (css, webapi, graphics-webgpu, on-device-ai, etc.)
- **Organization**: Version-based structure with area sections

### 4. Area Consolidation Pipeline Investigation & Development
**Goal**: Create/verify pipeline to combine by-area digests into full version digest

**Investigation Tasks**:
- [ ] **Current State Analysis**:
  - Review `enhanced_webplatform_digest.py` - currently generates per-area digests (`split_by_area=True`)
  - Review `merged_digest_html.py` - combines enterprise+webplatform but expects pre-made digest files
  - Check if version-level consolidation already exists
  
- [ ] **Gap Analysis**:
  - Identify missing script to combine area-specific digests into full version digest
  - Determine if `split_by_area=False` generates full digest or needs development
  
**Development Tasks** (if needed):
- [ ] **Create Area Consolidation Script**:
  ```python
  # New script: src/processors/consolidate_area_digests.py
  # Combines: areas/{css,webapi,graphics-webgpu,...}/chrome-{version}-stable.md
  # Into: digest_markdown/webplatform/digest-chrome-{version}-webplatform-stable.md
  ```

- [ ] **Integration Points**:
  - Read from: `upstream_docs/processed_releasenotes/processed_forwebplatform/areas/`
  - Output to: `digest_markdown/webplatform/`
  - Maintain consistent naming: `digest-chrome-{version}-webplatform-{channel}.md`

**Command Template** (once verified/developed):
```bash
# Generate per-area digests first  
python3 src/processors/clean_data_pipeline.py --version [VERSION] --with-yaml

# Consolidate areas into full version digest
python3 src/processors/consolidate_area_digests.py --version [VERSION] --channel stable

# Or use enhanced tool with split_by_area=False (if supported)
# [Tool investigation needed]
```

### 5. Quality Assurance Checks
**Goal**: Ensure data quality and semantic accuracy

**QA Checklist**:
- [ ] **Multi-area Classification**: AI features appear in both origin-trials and on-device-ai
- [ ] **Feature Count Validation**: WebGPU area has 5+ features per version
- [ ] **Content Completeness**: No truncated or missing feature descriptions
- [ ] **Link Integrity**: All tracking bugs and ChromeStatus links preserved
- [ ] **Heading Structure**: H2/H3 hierarchy maintained in processed files

### 6. Documentation Updates
**Goal**: Update project documentation based on processing results

**Tasks**:
- [ ] Update version compatibility notes in CLAUDE.md
- [ ] Document any new issues discovered during multi-version processing
- [ ] Update area classification statistics
- [ ] Record processing performance metrics

## Success Criteria

### Data Processing Success
- [ ] All target versions processed without errors
- [ ] Feature extraction accuracy: >95% for each area
- [ ] WebGPU deduplication working correctly
- [ ] Multi-area classification functioning (AI features in multiple areas)

### Digest Generation Success
- [ ] Comprehensive WebPlatform digests generated
- [ ] Both English and Chinese versions available
- [ ] Proper area-based organization
- [ ] All feature details and references included

### Quality Metrics
- [ ] **on-device-ai**: Only contains actual AI features (no false positives)
- [ ] **graphics-webgpu**: Contains 5+ features per version with proper deduplication
- [ ] **origin-trials**: Contains complete feature context
- [ ] **css**: All CSS and UI features properly classified

## Potential Challenges & Solutions

### Challenge: Version-specific Structure Differences
**Solution**: The `clean_webgpu_content()` method is designed for multi-version compatibility (136-139)

### Challenge: Missing WebGPU Files for Some Versions
**Solution**: Pipeline will gracefully handle missing WebGPU files and continue with Chrome-only processing

### Challenge: Memory Usage for Large Batch Processing
**Solution**: Process versions sequentially rather than in parallel

### Challenge: MCP Server Resource Management
**Solution**: Use individual tool calls rather than batch processing for digest generation

## File Organization
```
upstream_docs/processed_releasenotes/processed_forwebplatform/
├── areas/
│   ├── css/chrome-{version}-stable.md
│   ├── graphics-webgpu/chrome-{version}-stable.md  
│   ├── on-device-ai/chrome-{version}-stable.md
│   └── ...
└── processed_yaml/
    ├── css/chrome-{version}-stable.yml
    ├── graphics-webgpu/chrome-{version}-stable.yml
    ├── on-device-ai/chrome-{version}-stable.yml
    └── ...
```

## Next Steps (Post-0901)
- Analyze processing results for patterns across versions
- Optimize pipeline performance based on multi-version insights
- Plan digest distribution and integration workflows
- Consider automation for future version processing

---
**Created**: 2025-08-31  
**Updated**: 2025-08-31  
**Status**: Ready for execution  
**Estimated Time**: 4-6 hours (depending on version count and digest complexity)