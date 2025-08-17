# WebGPU-Graphics Merge and Pipeline Redesign

## Executive Summary

This document consolidates the WebGPU-Graphics merge plan and pipeline update recommendations to address the current issue where WebGPU content is merged BEFORE splitting by heading2, causing features to appear in wrong categories. The new approach splits first, then merges WebGPU with Graphics content specifically.

## Problem Statement

### Current Issues
1. WebGPU content is merged into main Chrome release notes BEFORE splitting by heading2
2. This causes WebGPU features to potentially appear in wrong areas (CSS, WebAPI, etc.)
3. No proper handling of WebGPU when it appears as its own heading2 (Chrome 136-137)
4. Lack of three-source deduplication for WebGPU content

### WebGPU Content Sources
WebGPU content can appear in three places:
1. **Dedicated WebGPU release notes** (separate markdown files)
2. **WebGPU heading2 section** in main release notes (Chrome 136-137)
3. **"Rendering and graphics" heading2 section** in main release notes

## Proposed Solution

### New Pipeline Architecture

```
1. Raw Chrome Release Notes
   ↓
2. Split by heading2 (split_and_process_release_notes.py)
   ↓
3. Save split markdown files to:
   - upstream_docs/processed_releasenotes/split_by_area/css/
   - upstream_docs/processed_releasenotes/split_by_area/webapi/
   - upstream_docs/processed_releasenotes/split_by_area/rendering/
   - upstream_docs/processed_releasenotes/split_by_area/webgpu/ (if exists)
   ↓
4. Merge WebGPU and Graphics (merge_webgpu_graphics.py) [NEW]
   - Inputs: rendering/, webgpu/, dedicated WebGPU files
   - Output: merged/graphics-webgpu/
   ↓
5. Generate YAML from split/merged files (yaml_pipeline.py - updated)
   - Process each area independently
   - Use merged graphics-webgpu instead of separate files
   ↓
6. Generate digests (enhanced_webplatform_digest.py)
   - Per-area digests from YAML
```

### Key Principle
**Split First, Merge Later**: By splitting release notes by heading2 BEFORE merging WebGPU content, we ensure accurate categorization and prevent content mixing across areas.

## Implementation Plan

### Phase 1: Analysis and Design (2-3 hours)

#### 1.1 Understand Current State
- [ ] Review existing merge_webgpu_release_notes_v2.py logic
- [ ] Analyze Graphics area split output structure (from "Rendering and graphics")
- [ ] Analyze WebGPU area split output structure (when WebGPU appears as heading2)
- [ ] Identify WebGPU content patterns in all three sources
- [ ] Document overlap and unique content across sources
- [ ] Map version ranges for each source type (e.g., WebGPU heading2 in 136-137)

#### 1.2 Define Merge Strategy
- [ ] Determine merge precedence for three sources:
  1. Dedicated WebGPU release notes (highest priority)
  2. WebGPU heading2 split (medium priority)
  3. Rendering and graphics split (lowest priority)
- [ ] Define deduplication rules for overlapping features across all sources
- [ ] Establish heading hierarchy for merged output
- [ ] Create merge conflict resolution approach
- [ ] Handle version-specific logic (e.g., check for WebGPU heading2 only in 136+)

#### 1.3 Design Output Format
- [ ] Define merged file naming convention
- [ ] Establish directory structure for merged outputs
- [ ] Determine metadata preservation strategy
- [ ] Plan for version/channel tracking

### Phase 2: Implementation (4-5 hours)

#### 2.1 Create New Merge Script: `merge_webgpu_graphics.py`
**Location**: `src/processors/merge_webgpu_graphics.py`

**Core Functionality**:
- Load content from three sources (dedicated WebGPU, WebGPU heading2, Rendering/Graphics)
- Version-aware source selection
- Three-way deduplication
- Proper heading hierarchy management
- Source attribution in output

**Technical Specifications**:

##### Input Files
1. **WebGPU Dedicated Release Notes**
   - Path: `upstream_docs/release_notes/webgpu/chrome-{version}-{channel}.md`
   - Availability: Most versions

2. **WebGPU Heading2 Split Output** (Chrome 136+ only)
   - Path: `upstream_docs/processed_releasenotes/split_by_area/webgpu/chrome-{version}-{channel}.md`
   - Availability: Chrome 136-137 (may expand in future)

3. **Rendering and Graphics Split Output**
   - Path: `upstream_docs/processed_releasenotes/split_by_area/rendering/chrome-{version}-{channel}.md`
   - Alternative: `upstream_docs/processed_releasenotes/split_by_area/graphics/chrome-{version}-{channel}.md`
   - Availability: Most versions (6/15 analyzed)

##### Output File
- Path: `upstream_docs/processed_releasenotes/merged/graphics-webgpu/chrome-{version}-{channel}.md`
- Format: Markdown with proper heading hierarchy
- Structure:
  ```markdown
  # Graphics and WebGPU - Chrome {version} {channel}
  
  ## Rendering and Graphics
  [Content from Rendering/Graphics split, excluding WebGPU duplicates]
  
  ## WebGPU Features
  ### From Dedicated Release Notes
  [Content from dedicated WebGPU release notes]
  
  ### From Chrome Release Notes
  [Content from WebGPU heading2 split, if available]
  
  ## Deduplicated Features
  [Features that appeared in multiple sources, consolidated]
  ```

##### Deduplication Rules
1. Compare feature titles across all three sources (fuzzy matching)
2. Check for identical issue/bug IDs (e.g., crbug.com links)
3. Priority for content preservation:
   - Dedicated WebGPU notes (most detailed)
   - WebGPU heading2 split
   - Rendering/Graphics split (least detailed)
4. Preserve most detailed description when merging
5. Maintain all unique metadata from each source
6. Log duplicates for review with source tracking

##### Error Handling
- Missing dedicated WebGPU file: Check WebGPU heading2 split, then Graphics split
- Missing WebGPU heading2 split: Expected for versions < 136, use other sources
- Missing Graphics split: Use WebGPU sources only
- All sources missing: Log warning and create minimal placeholder
- Malformed content: Attempt repair or flag for manual review
- Version-specific logic: Only check WebGPU heading2 for Chrome 136+

#### 2.2 Update Existing Scripts

##### yaml_pipeline.py (CRITICAL UPDATE)
- **Current State**: Has built-in `_merge_webgpu_content()` method that merges WebGPU directly into main content
- **Required Changes**:
  - Remove or disable the `merge_webgpu` parameter and `_merge_webgpu_content()` method
  - Update area_mappings to handle merged graphics-webgpu files
  - Rely on the new graphics-webgpu merge that happens AFTER splitting

##### split_and_process_release_notes.py (UPDATE)
- **Current State**: Has `merge_webgpu_section()` but only merges from dedicated WebGPU files
- **Required Changes**:
  - Update `merge_webgpu_section()` to handle all three sources
  - Add version-aware logic for WebGPU heading2 (Chrome 136+)
  - Implement proper deduplication across sources
  - Save split files before merging

##### enhanced_webplatform_digest.py (MINOR UPDATE)
- **Current State**: Works with split YAML files, supports `split_by_area=True`
- **Required Changes**:
  - Ensure it can find and use the new merged graphics-webgpu YAML files
  - Update path resolution for merged content

### Phase 3: Testing and Validation (2-3 hours)

#### 3.1 Unit Tests
- [ ] Test content extraction from WebGPU notes
- [ ] Test Graphics split parsing
- [ ] Test three-way deduplication algorithm
- [ ] Test heading hierarchy preservation
- [ ] Test version-aware source selection

#### 3.2 Integration Tests
- [ ] Test with Chrome 139 stable release (no WebGPU heading2)
- [ ] Test with Chrome 136 stable release (has WebGPU heading2)
- [ ] Verify no content loss during merge
- [ ] Validate output format compatibility
- [ ] Test edge cases (missing files, empty sections)

#### 3.3 End-to-End Validation
- [ ] Process through entire pipeline
- [ ] Generate digest from merged content
- [ ] Compare with manual verification
- [ ] Performance testing (target: < 5 seconds per version)

### Phase 4: Documentation and Deployment (1-2 hours)

#### 4.1 Update Documentation
- [ ] Update CLAUDE.md with new merge process
- [ ] Document command usage and parameters
- [ ] Add troubleshooting guide
- [ ] Create example workflows

#### 4.2 Deprecate Old Scripts
The following scripts will be deprecated:

1. **merge_webgpu_release_notes_v2.py**
   - Reason: Merges WebGPU into main content BEFORE splitting
   - Replacement: New merge_webgpu_graphics.py

2. **process_merged_webgpu.py**
   - Reason: Uses the deprecated v2 merger
   - Replacement: Updated pipeline with proper merge logic

3. **regenerate_webgpu_yamls.py**
   - Reason: Uses old merge approach with `merge_webgpu=True` parameter
   - Replacement: New pipeline automatically handles WebGPU merging

4. **webgpu_merger.py** (MCP tool)
   - Reason: Implements old merge strategy
   - Replacement: New merge logic in updated pipeline

5. **webgpu_yaml_processor.py** (MCP tool)
   - Action: Review and update or deprecate if redundant

## Source Priority Matrix

| Version Range | Primary Source | Secondary Source | Tertiary Source |
|--------------|----------------|------------------|-----------------|
| < 136 | Dedicated WebGPU | Rendering/Graphics | N/A |
| 136-137 | Dedicated WebGPU | WebGPU heading2 | Rendering/Graphics |
| 138+ | Dedicated WebGPU | Rendering/Graphics | WebGPU heading2 (if exists) |

## File Discovery Strategy

1. Check all three potential sources in parallel
2. Build available source list dynamically
3. Apply version-specific filtering
4. Log source availability for debugging
5. Proceed with available sources only

## Success Criteria

- [ ] Zero content loss during three-way merge
- [ ] Proper deduplication without removing unique features
- [ ] Correctly handles version-specific source availability
- [ ] Maintains searchability and structure
- [ ] Compatible with downstream tools
- [ ] Performance: < 5 seconds per version
- [ ] Test coverage > 80%
- [ ] Accurate source attribution in merged output

## Benefits of New Approach

1. **Accurate Categorization**: WebGPU features stay in graphics area
2. **No Content Mixing**: Each area contains only relevant features
3. **Better Deduplication**: Three-way merge handles all sources
4. **Version Awareness**: Properly handles WebGPU heading2 when present
5. **Clear Pipeline**: Split → Merge → YAML → Digest
6. **Maintainability**: Cleaner separation of concerns

## Risks and Mitigations

1. **Risk**: Feature deduplication too aggressive across three sources
   - **Mitigation**: Conservative matching, source tracking, manual review

2. **Risk**: Breaking existing workflows
   - **Mitigation**: Parallel run period, gradual migration

3. **Risk**: Heading hierarchy conflicts with three-level merge
   - **Mitigation**: Clear precedence rules, validation checks

4. **Risk**: Performance issues with multiple file reads
   - **Mitigation**: Parallel loading, caching strategies

5. **Risk**: Version-specific logic causing edge cases
   - **Mitigation**: Comprehensive version range testing, fallback logic

6. **Risk**: Missing WebGPU heading2 misinterpreted as error
   - **Mitigation**: Version-aware expectations, clear logging

7. **Risk**: YAML structure changes
   - **Mitigation**: Ensure backward compatibility in digest tools

## Migration Timeline

- **Week 1**: Implement merge_webgpu_graphics.py
- **Week 2**: Update yaml_pipeline.py and split_and_process_release_notes.py
- **Week 3**: Testing and validation
- **Week 4**: Deprecate old scripts and documentation update

**Total Estimated Development Time**: ~12 hours

## Next Steps

1. Review and approve this consolidated plan
2. Begin Phase 1 analysis of three source types
3. Create test data from Chrome 139 (no WebGPU heading2) and 136 (has WebGPU heading2)
4. Prototype three-way deduplication algorithm
5. Implement version-aware source selection logic
6. Implement core merge logic with source attribution
7. Run parallel validation with old pipeline
8. Deploy new pipeline with monitoring

## Appendix: Scripts Reference

### Scripts to Keep (No Changes)
- `focus_area_manager.py` - Already maps webgpu/graphics correctly

### Scripts to Update
- `yaml_pipeline.py` - Remove merge_webgpu functionality
- `split_and_process_release_notes.py` - Update merge logic
- `enhanced_webplatform_digest.py` - Path updates

### Scripts to Create
- `merge_webgpu_graphics.py` - New three-source merger

### Scripts to Deprecate
- `merge_webgpu_release_notes_v2.py`
- `process_merged_webgpu.py`
- `regenerate_webgpu_yamls.py`
- `webgpu_merger.py`
- `webgpu_yaml_processor.py` (review first)

---

*Document Version: 1.0*  
*Date: 2025-01-18*  
*Status: Draft - Pending Review*