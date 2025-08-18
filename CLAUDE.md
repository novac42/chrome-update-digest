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

# Process release notes with integrated WebGPU merge
python3 src/processors/split_and_process_release_notes.py --version 139  # Main pipeline with WebGPU merge

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

### Focus Areas and Tagging
**Configuration**: Focus areas are defined in `config/focus_areas.yaml` with keywords and heading patterns.

**Key Areas**:
- **on-device-ai**: Keywords include "language model", "ai", "llm", "on-device"
- **graphics-webgpu**: Merged from three sources for comprehensive coverage
- **css**, **webapi**, **security-privacy**, etc.

**Known Issues** (as of 2025-08-18):
- Missing on-device-ai area in YAML pipeline's area_mappings
- WebGPU YAML may not extract all features from merged markdown
- YAML files scattered across area subdirectories (planned consolidation to processed_yaml/)

### Command Execution in WSL
**Issue**: Python commands may fail with "command not found" in WSL.

**Solution**: Always use `python3` instead of `python` in WSL environment.
- save one-time test scripts for debugging and its output to the folder /temp-save