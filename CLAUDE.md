# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important Notes

- **Virtual Environment**: All dependencies are installed in `.venv`. Always activate the virtual environment before running any commands:
  ```bash
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
  ```
- **Testing**: Always use the `.venv` environment when running tests to ensure all dependencies are available.
- **Project Planning**: When creating timelines or roadmaps, use phase-based planning (Phase 1, Phase 2, etc.) or sprint-based planning instead of week-based timelines.
- **Windows WSL Environment**: When running from WSL on Windows, use `python3` command instead of `python`. The .venv activation might not be available in WSL.

## Common Development Commands

### Testing
```bash
# IMPORTANT: Always activate .venv first!
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_process_enterprise_release.py -v

# Run with coverage report
pytest tests/ --cov=. --cov-report=html

# Run test suite using the provided script
python tests/run_tests.py

# Run a single test method
pytest tests/test_convert.py::TestChromeDigestConverter::test_extract_version_info -v
```

### Running the MCP Server
```bash
# Activate virtual environment first
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the FastMCP server
python fast_mcp_server.py
```

### Processing Release Notes
```bash
# IMPORTANT: Always ensure .venv is activated first!
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Convert markdown to HTML
python src/convert_md2html.py  # Automatically finds latest file
python src/convert_md2html.py digest-chrome-138-stable.md  # Specific file

# Process enterprise release notes
python src/process_enterprise_release_note.py

# Process WebPlatform release notes (RECOMMENDED)
python3 src/processors/clean_data_pipeline.py --version 139  # Advanced pipeline with focus_areas.yaml mapping

# Legacy pipeline (DEPRECATED - use clean_data_pipeline.py instead)
# python3 src/processors/split_and_process_release_notes.py --version 139

# Extract profile features
python src/processors/extract_profile_features.py

# Monitor releases
python src/processors/monitor_releases.py

# Generate WebPlatform per-area digests (default behavior)
# Note: split_by_area=True is now the default, generating separate digests for each focus area
python -c "
import asyncio
from src.mcp_tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool
from unittest.mock import AsyncMock

async def run():
    tool = EnhancedWebplatformDigestTool()
    ctx = AsyncMock()
    # Add mock sampling function as needed
    result = await tool.run(ctx, version='139', channel='stable')
    print(result)

asyncio.run(run())
"
```

## High-Level Architecture

### MCP Server Architecture
The project implements a Model Context Protocol (MCP) server using FastMCP framework that provides:

1. **Tools** - Accessible via MCP protocol:
   - `enterprise_digest`: Generates enterprise-focused digests with AI sampling
   - `webplatform_digest`: Creates web platform digests with focus areas
   - `merged_digest_html`: Produces combined HTML output
   - `split_features_by_heading`: Splits markdown by heading levels
   - `list_release_notes`: Lists available release note resources

2. **Resources** - Static content served via MCP:
   - Enterprise and WebPlatform prompts
   - Profile keywords
   - Processed release notes (dynamically discovered)

3. **Sampling Integration**: Uses FastMCP's sampling capabilities for intelligent content analysis

### Core Processing Pipeline

1. **Input Processing**:
   - Raw release notes stored in `upstream_docs/release_notes/`
   - Enterprise and WebPlatform notes processed separately
   - WebGPU notes merged with WebPlatform updates

2. **Processing Flow**:
   - `process_enterprise_release_note.py`: Extracts enterprise features
   - `merge_webgpu_release_notes.py`: Combines WebGPU with platform notes
   - Tools in `src/mcp_tools/` handle digest generation via MCP

3. **Output Generation**:
   - Markdown digests in `digest_markdown/`
   - HTML output in `digest_html/`
   - Feature splits in `feature_details/`

### Key Design Patterns

1. **Tool Classes**: Each MCP tool is a class with:
   - Async methods for MCP compatibility
   - Error handling with retry mechanisms
   - Resource loading via Context
   - Sampling integration for AI processing

2. **Resource Discovery**: Dynamic file discovery with:
   - Multiple naming pattern support
   - Channel fallback (beta → stable)
   - Version tolerance

3. **Fault Tolerance**:
   - Graceful handling of missing files
   - Retry logic for sampling calls
   - Fallback to file system when resources fail

### File Organization

- `src/mcp_tools/`: MCP tool implementations
- `src/mcp_resources/`: Resource handlers
- `src/utils/`: Shared utilities
- `src/processors/`: Processing scripts for release notes
  - `split_and_process_release_notes.py`: Main pipeline for splitting and processing
  - `clean_data_pipeline.py`: Advanced pipeline with focus_areas.yaml-driven area classification
  - `merge_webgpu_graphics.py`: Three-source WebGPU merger
- `prompts/`: AI prompts for digest generation
- `upstream_docs/processed_releasenotes/processed_forwebplatform/`:
  - `split_by_heading/`: Chrome notes split by heading2 sections
  - `merged/graphics-webgpu/`: Merged WebGPU content
  - `{area}/`: Area-specific YAML files (css, webapi, graphics-webgpu, etc.)
- `feature_details/`: Split feature documentation
- `project_docs/product_docs/`: All product-related documentation (PRDs, roadmaps, etc.)
- `project_docs/tech_docs/`: Technical documentation (architecture designs, optimization plans, implementation guides)

### Testing Strategy

Tests use pytest with comprehensive coverage:
- Unit tests for individual components
- Integration tests for MCP server
- Pipeline tests for end-to-end flows
- Fault tolerance tests for error handling

The test suite validates both traditional file processing and MCP server functionality.

## Clean Data Pipeline (Updated 2025-08-31)

The `src/processors/clean_data_pipeline.py` provides an advanced data processing pipeline with improved area classification:

### Key Features:
- **Configuration-driven**: Uses `config/focus_areas.yaml` for area mapping
- **Smart area classification**: Implements sophisticated matching logic with fallbacks
- **WebGPU deduplication**: Prioritizes WebGPU content over Chrome graphics content
- **YAML output integration**: Seamlessly integrates with existing YAML processing pipeline
- **Header-agnostic parsing**: Handles h2-h5 hierarchies without format dependency

### Usage:
```bash
python3 src/processors/clean_data_pipeline.py --version 139
```

### Architecture:
- **Section parsing**: Extracts h2 sections with content boundaries
- **Area mapping**: Uses `_map_area_name()` with priority-based matching
- **Feature deduplication**: Compares titles and issue IDs for duplicate detection
- **YAML generation**: Produces area-specific YAML files with proper metadata

### Benefits over legacy pipeline:
- Eliminates over-broad "others" categorization
- Preserves semantic area names from original headings
- Reduces classification errors through strict matching
- Supports flexible addition of new focus areas

## Known Issues and Solutions

### WebGPU Processing Pipeline
**Updated Solution (2025-08-18)**: The pipeline now uses a split-first, then merge approach with strict classification:

```bash
# Run the integrated pipeline that handles everything
python3 src/processors/split_and_process_release_notes.py --version 139
```

This pipeline:
1. **Splits** Chrome release notes by heading2 sections first
2. **Merges** WebGPU content from three sources:
   - Dedicated WebGPU release notes (`webgpu-{version}.md`)
   - WebGPU heading2 section (Chrome 136-137 only)
   - Graphics/Rendering section
3. **Generates** YAML with the merged content for graphics-webgpu area

**Key Learnings**:
- Always split BEFORE merging to avoid incorrect categorization
- Extract ALL content from dedicated WebGPU notes except "What's New in WebGPU" history section
- Apply deduplication only during YAML generation for graphics-webgpu area
- File organization: `/merged` and `/split_by_heading` folders under `/processed_forwebplatform`
- **NEW**: Strict WebGPU classification is now enabled by default (as of 2025-08-18)
  - Reduces misclassification from 72.4% to ~0%
  - To disable (not recommended): `export STRICT_WEBGPU_AREA=0`
  - See `docs/webgpu_strict_classification.md` for details

### Area Classification
**Issue**: Features may be incorrectly classified into wrong areas due to broad heading detection.

**Best Practice**: 
- Use selective extraction rather than full document merge
- Verify heading paths in generated YAML files
- Check that area-specific YAML only contains relevant features

### Focus Areas and Area Classification
**Configuration**: Focus areas are defined in `config/focus_areas.yaml` with keywords and heading patterns.

**Area Classification Logic** (Updated 2025-08-31):
- **Most areas**: Only match h2 headings using `heading_patterns` (strict matching)
- **on-device-ai**: Uses both `heading_patterns` AND searches feature content for keywords (`search_content_keywords: true`)
- **payment**: Partial matching - any heading containing "payment" → payment area
- **devtools**: Partial matching - any heading containing "developer tools" → devtools area
- **Unmapped headings**: Use original h2 title as area name (lowercase, spaces→hyphens, &→and)

**Key Areas**:
- **on-device-ai**: Special area with content keyword search ("language model", "ai api", "prompt api", etc.)
- **graphics-webgpu**: Merged from three sources for comprehensive coverage
- **css**: CSS and UI features
- **payment**: Payment and payment-related features  
- **devtools**: Developer Tools and debugging features
- **devices**, **webapi**, **security-privacy**, etc.

**Area Mapping Priority**:
1. Exact `heading_patterns` match
2. Special partial matches (payment, devtools)
3. Content keyword search (on-device-ai only)
4. Device fallback (if heading contains "device")
5. Original heading name transformation

### Multi-area Feature Classification
**Issue**: Features with cross-cutting concerns (e.g., AI features in Origin Trials) need to appear in multiple areas.

**Solution (Updated 2025-08-31)**: 
- Use **feature-level keyword matching** instead of section-level matching
- Implement `_extract_keyword_features()` method for precise content analysis
- Areas like `on-device-ai` use `search_content_keywords: true` to enable content-based feature extraction
- This ensures semantic accuracy: only actual AI features appear in AI area, while maintaining complete context in original sections

### Command Execution in WSL
**Issue**: Python commands may fail with "command not found" in WSL.

**Solution**: Always use `python3` instead of `python` in WSL environment.
- save one-time test scripts for debugging and its output to the folder /temp-save

## Data Processing Best Practices

### Raw Data Characteristics (Learned 2025-08-31)

1. **Structural Evolution**: Chrome release notes structure changes between versions
   - Expected sections (Security, Performance, etc.) may be missing in some versions
   - Use validation warnings but continue processing (fail-safe approach)
   - Structure validation threshold: >50% missing areas indicates potential format change

2. **Multi-source Data Fusion**: 
   - Chrome release notes + dedicated WebGPU files
   - WebGPU content may appear in both Chrome Graphics section and standalone files
   - Requires intelligent deduplication with WebGPU priority

3. **Hierarchical Complexity**:
   - H2 sections contain multiple H3 features
   - Features may have cross-cutting concerns (e.g., AI features in multiple areas)
   - Need precise granularity control for semantic accuracy

### Data Cleaning Core Principles

1. **Semantic Accuracy Over Technical Convenience**
   ```python
   # Wrong: Section-level keyword matching (easy but semantically incorrect)
   if 'ai language model' in section.content:
       areas['on-device-ai'] = section.content  # Includes non-AI content
   
   # Right: Feature-level keyword matching (complex but semantically correct)
   for feature in section.features:
       if 'ai language model' in feature.content:
           areas['on-device-ai'] += feature.content  # Only AI features
   ```

2. **Configuration-Driven Flexibility**:
   - Use `focus_areas.yaml` configuration instead of hardcoded mappings
   - Support mixed matching strategies: exact, partial, and content-based
   - Enable `search_content_keywords` flag for cross-cutting features

3. **Multi-Version Compatibility**:
   - Handle different WebGPU file structures (versions 136-139)
   - Clean metadata while preserving content and heading hierarchy
   - Implement version-tolerant content cleaning logic

4. **Intelligent Deduplication**:
   ```python
   # Multi-criteria deduplication strategy
   title_similarity = calculate_similarity(chrome_title, webgpu_title)
   issue_overlap = chrome_issues & webgpu_issues
   is_duplicate = title_similarity > 0.7 or bool(issue_overlap)
   ```

5. **Validation Without Blocking**:
   - Warn about structural changes but continue processing
   - Use tolerance thresholds (e.g., 50% missing sections) for robustness
   - Prefer degraded functionality over complete failure

### Critical Success Factors

- **Granularity Precision**: Match keywords at the appropriate level (feature vs section)
- **Multi-area Support**: Allow features to appear in multiple relevant areas
- **Semantic Preservation**: Maintain meaning and context during transformation
- **Error Tolerance**: Handle missing or changed data gracefully
- **Configuration Management**: Use external config files for flexible area definitions

This approach ensures that:
- Origin trials contains complete context (all 4 features)
- On-device AI contains only semantically relevant features (2 AI features)
- Graphics-WebGPU preserves all WebGPU content with proper deduplication
- System remains robust across Chrome version changes