# Release Monitor MCP Tool - Merged Implementation Plan

## Overview
This document outlines the implementation of an MCP tool that checks for the latest available release notes for Chrome WebPlatform and Enterprise releases, compares them with locally saved versions, and provides interactive crawling capabilities.

## Core Requirements

The release monitor tool should:
1. Check URLs to identify the latest versions for enterprise and webplatform
2. Compare with local release notes folder to identify which latest versions are missing
3. Focus only on latest versions (not older historical versions)
4. Ask the user if they want to crawl missing release notes before proceeding
5. If user confirms, call the crawl script to fetch the missing content

## Architecture Overview

### MCP Tool Integration
- **Tool Name**: `release_monitor`
- **Location**: `/src/mcp_tools/release_monitor.py`
- **Integration**: Registered in `fast_mcp_server.py` following existing patterns
- **Core Logic**: Extracted to `/src/utils/release_monitor_core.py` for reusability

### Workflow Design
```
User calls tool → Check latest versions → Compare with local files → 
Report missing → Ask user to crawl → User confirms → Crawl content
```

## Implementation Plan

### Phase 1: Core Utility Module

#### File: `/src/utils/release_monitor_core.py`

Extract and consolidate logic from existing components:
- Version detection from `scripts/monitor_releases.py`
- Enterprise URL patterns from `src/crawl_script.py`
- Unified error handling patterns

```python
class ReleaseMonitorCore:
    def __init__(self, base_path: Path)
    
    async def get_latest_webplatform_version(self) -> dict
    async def get_latest_enterprise_version(self) -> dict
    async def scan_local_versions(self, release_type: str) -> list
    async def compare_versions(self, latest: dict, local: list) -> dict
    
    # Integration with existing crawl infrastructure
    async def crawl_missing_releases(self, missing_versions: list) -> dict
```

### Phase 2: MCP Tool Implementation

#### File: `/src/mcp_tools/release_monitor.py`

```python
class ReleaseMonitorTool:
    def __init__(self, base_path: Path)
    
    async def check_latest_releases(self, ctx: Context, arguments: dict) -> str:
        """
        Check latest versions and compare with local files.
        Returns status without automatically crawling.
        """
        
    async def crawl_missing_releases(self, ctx: Context, arguments: dict) -> str:
        """
        Interactive crawling after user confirmation.
        Only called when user explicitly requests it.
        """
```

### Phase 3: Registration in FastMCP Server

#### Update: `fast_mcp_server.py`

```python
from src.mcp_tools.release_monitor import ReleaseMonitorTool

# Initialize tool
release_monitor_tool = ReleaseMonitorTool(base_path)

@mcp.tool()
async def check_latest_releases(ctx: Context, arguments: dict) -> str:
    """Check for latest release versions and compare with local files"""
    return await release_monitor_tool.check_latest_releases(ctx, arguments)

@mcp.tool()
async def crawl_missing_releases(ctx: Context, arguments: dict) -> str:
    """Crawl missing release notes after user confirmation"""
    return await release_monitor_tool.crawl_missing_releases(ctx, arguments)
```

## Tool Methods Specification

### 1. `check_latest_releases`

**Purpose**: Check latest versions and report status without automatic crawling

**Parameters**:
- `release_type`: "webplatform" | "enterprise" | "both" (default: "both")

**Returns**: JSON response with:
```json
{
  "webplatform": {
    "latest_chrome_version": "140",
    "latest_webgpu_version": "139",
    "status": "missing_locally",
    "missing_versions": ["140"]
  },
  "enterprise": {
    "latest_version": "140.0.6086.133",
    "status": "up_to_date",
    "missing_versions": []
  },
  "summary": {
    "has_missing_releases": true,
    "total_missing": 1,
    "recommendation": "Use crawl_missing_releases to download missing versions"
  }
}
```

### 2. `crawl_missing_releases`

**Purpose**: Interactive crawling tool that requires explicit user confirmation

**Parameters**:
- `release_type`: "webplatform" | "enterprise" | "both"
- `versions`: array of specific versions to crawl (optional, defaults to all missing)
- `confirmed`: boolean - user must set to true to proceed

**Behavior**:
- If `confirmed` is not true, return message asking for user confirmation
- Only proceed with crawling when user explicitly confirms
- Use existing crawl infrastructure from `src/crawl_script.py`

**Returns**: JSON response with crawling results and saved file paths

## URL Sources and Detection

### WebPlatform Release Notes
- **Chrome Releases**: `https://developer.chrome.com/release-notes/`
- **WebGPU Releases**: `https://developer.chrome.com/docs/web-platform/webgpu/news`
- **Detection Method**: Parse main pages to identify latest version numbers
- **Content URLs**: 
  - Chrome: `https://developer.chrome.com/release-notes/{version}`
  - WebGPU: `https://developer.chrome.com/blog/new-in-webgpu-{version}`

### Enterprise Release Notes
- **Main Page**: `https://support.google.com/chrome/a/topic/9025817`
- **Content URLs**: `https://support.google.com/chrome/a/answer/{answer_id}`
- **Detection Method**: Parse support topic page for latest version links
- **Content Extraction**: Use existing logic from `crawl_script.py`

## Local File Comparison

### File Structure Analysis
```
upstream_docs/release_notes/
├── WebPlatform/
│   ├── chrome-release-notes-139.md
│   ├── webgpu-release-notes-138.md
│   └── ...
└── Enterprise/
    ├── enterprise-release-notes-140.0.6086.133.md
    └── ...
```

### Version Extraction Logic
- Parse existing filenames to extract version numbers
- Compare against latest detected versions
- Identify missing versions for user notification

## Interactive Workflow Design

### User Experience Flow
1. **User calls `check_latest_releases`**
   - Tool reports current status
   - Shows missing versions if any
   - Provides clear next steps

2. **If missing versions found**:
   - Tool recommends using `crawl_missing_releases`
   - Does NOT automatically crawl

3. **User decides to crawl**:
   - Calls `crawl_missing_releases` with `confirmed: true`
   - Tool proceeds with downloading
   - Reports success/failure for each version

### Error Handling Strategy

Based on existing script patterns:
- **Network Errors**: Graceful handling with retry logic
- **HTTP Errors**: Use `response.raise_for_status()` with proper exception handling
- **Parsing Errors**: Fallback strategies for content extraction
- **File System Errors**: Clear error messages in JSON responses
- **User Interaction**: Clear prompts and confirmation requirements

## Integration with Existing Systems

### Reuse Existing Components
- **Crawl Logic**: Leverage `src/crawl_script.py` for Enterprise content
- **Monitoring Logic**: Adapt `scripts/monitor_releases.py` for version detection
- **Version Tracking**: Update `.monitoring/versions.json` when crawling
- **File Organization**: Follow existing patterns in `upstream_docs/release_notes/`

### Maintain Compatibility
- Keep existing scripts functional
- Don't modify core crawl infrastructure
- Use existing error handling patterns
- Follow established file naming conventions

## Implementation Steps

1. **Create Core Utility** (`src/utils/release_monitor_core.py`)
   - Extract version detection from `scripts/monitor_releases.py`
   - Integrate Enterprise URL patterns from `src/crawl_script.py`
   - Implement local file scanning and comparison logic

2. **Implement MCP Tool** (`src/mcp_tools/release_monitor.py`)
   - Create tool class following FastMCP patterns
   - Implement interactive workflow with user confirmation
   - Format all responses as structured JSON

3. **Register in FastMCP Server**
   - Import and initialize the tool
   - Add method decorators following existing patterns
   - Test integration with MCP protocol

4. **Testing and Validation**
   - Test latest version detection for both release types
   - Verify local file comparison accuracy
   - Test interactive crawling workflow
   - Validate JSON response formats
   - Ensure error handling works correctly

## Success Criteria

1. **Latest Version Detection**: Tool accurately identifies current Chrome, WebGPU, and Enterprise versions
2. **Local Comparison**: Correctly identifies which versions are missing locally
3. **Interactive Workflow**: Requires explicit user confirmation before crawling
4. **Content Integration**: Downloaded content matches existing file format and structure
5. **Error Resilience**: Handles network issues and parsing errors gracefully
6. **User Experience**: Provides clear status information and next steps
7. **System Integration**: Works seamlessly with existing FastMCP infrastructure

## Design Decisions

1. **Interactive Over Automatic**: Tool asks before crawling, doesn't assume user intent
2. **Latest-Only Focus**: Ignores older versions, only checks for newest releases
3. **JSON Communication**: All responses structured for easy parsing and display
4. **Reuse Existing Logic**: Leverages proven crawl and monitoring infrastructure
5. **No Authentication**: Public URLs only, consistent with existing approach
6. **Filesystem Caching**: Uses local files as source of truth for version tracking