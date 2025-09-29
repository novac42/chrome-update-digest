#!/usr/bin/env python3
"""
Chrome Digest FastMCP Server
Modern MCP server implementation using FastMCP with sampling and resource management.
Provides tools for generating web platform digests from processed Chrome release notes.
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime

from fastmcp import FastMCP, Context
from fastmcp.resources import FileResource

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

# Import tool classes
from mcp_tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool
from mcp_tools.feature_splitter import FeatureSplitterTool
from mcp_tools.github_pages_orchestrator import GithubPagesOrchestratorTool
from mcp_tools.release_monitor import ReleaseMonitorTool
# WebGPU tools removed - functionality integrated into main pipeline

# Import resource classes
from mcp_resources.processed_releasenotes import ProcessedReleaseNotesResource

# Initialize FastMCP server
mcp = FastMCP("DigestServer")

# Base path for the server
BASE_PATH = Path(__file__).parent


# Setup static resources
@mcp.resource("file://webplatform-prompt", mime_type="text/markdown")
def get_webplatform_prompt() -> str:
    """WebPlatform digest generation prompt (bilingual)"""
    webplatform_prompt_path = BASE_PATH / "prompts" / "webplatform-prompts" / "webplatform-prompt-bilingual.md"
    if webplatform_prompt_path.exists():
        with open(webplatform_prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return "WebPlatform prompt file not found"



# Initialize tool instances
feature_splitter = FeatureSplitterTool(BASE_PATH)
release_monitor_tool = ReleaseMonitorTool(BASE_PATH)
# Navigation orchestrator ties digest generation, page refresh, and validation together
github_pages_orchestrator = GithubPagesOrchestratorTool(BASE_PATH)
# WebGPU tools initialization removed - use split_and_process_release_notes.py instead

# Initialize resource handler
release_notes_resource = ProcessedReleaseNotesResource(BASE_PATH)


async def load_prompt_from_resource(resource_name: str) -> str:
    """从本地文件读取prompt内容（暂时直接读取文件，后续可改为resource读取）"""
    try:
        if resource_name == "webplatform-prompt":
            file_path = BASE_PATH / "prompts" / "webplatform-prompts" / "webplatform-prompt-bilingual.md"
        else:
            raise ValueError(f"Unknown resource: {resource_name}")
        
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise FileNotFoundError(f"Resource file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Failed to load resource '{resource_name}': {str(e)}")


def load_processed_data(data_type: str, version: int, channel: str = "stable") -> str:
    """加载处理过的release notes数据"""
    try:
        if data_type == "webplatform":
            data_path = BASE_PATH / "upstream_docs" / "processed_releasenotes" / "processed_forwebplatform" / f"{version}-webplatform-with-webgpu.md"
        else:
            raise ValueError(f"Unknown data type: {data_type}")
        
        if not data_path.exists():
            raise FileNotFoundError(f"Data file not found: {data_path}")
        
        with open(data_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    except Exception as e:
        raise Exception(f"Failed to load {data_type} data for version {version}: {str(e)}")


async def save_digest_to_file(content: str, output_path: Path) -> None:
    """保存digest内容到文件"""
    try:
        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存内容
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        raise Exception(f"Failed to save digest to {output_path}: {str(e)}")




@mcp.tool()
async def get_webplatform_progress() -> str:
    """Get the current progress of WebPlatform digest generation
    
    Returns progress information from the monitoring JSON file if available.
    """
    progress_file = BASE_PATH / ".monitoring" / "webplatform-progress.json"
    
    if not progress_file.exists():
        return json.dumps({
            "status": "idle",
            "message": "No digest generation in progress"
        })
    
    try:
        with open(progress_file, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)
        
        # Calculate percentage
        total = progress_data.get("total_areas", 0)
        completed = progress_data.get("completed_areas", 0)
        
        if total > 0:
            percentage = (completed / total) * 100
            progress_data["percentage"] = f"{percentage:.0f}%"
        
        return json.dumps(progress_data, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Failed to read progress: {str(e)}"
        })


@mcp.tool()
async def webplatform_digest(ctx: Context, version: str = "138", channel: str = "stable",
                                     focus_areas: Optional[str] = None, use_cache: bool = True,
                                     language: str = "bilingual", split_by_area: bool = True,
                                     target_area: Optional[str] = None, debug: bool = False,
                                     model: Optional[str] = None,
                                     model_preferences: Optional[Any] = None) -> str:
    """Generate webplatform digest with deterministic link extraction
    
    This tool provides 100% link accuracy through script-based extraction and
    supports configuration-driven focus area filtering with bilingual output.
    
    Args:
        version: Chrome version number (e.g., "138")
        channel: Chrome release channel (default: stable)
        focus_areas: Comma-separated focus areas (e.g., "ai,webgpu,security")
                    Available areas: ai, webgpu, security, performance, css, webapi, 
                    devtools, pwa, accessibility, media
        use_cache: Whether to use cached YAML extraction if available
        language: Output language ("en" for English, "zh" for Chinese, "bilingual" for both)
        split_by_area: Split features into separate YAML files by area (css, webapi, etc.)
        target_area: Analyze a specific area (css, webapi, security, javascript, etc.)
                    When set, uses area-specific expert prompts
        debug: Enable debug output for troubleshooting
        
    Returns:
        Generated digest in markdown format with accurate links in specified language
    """
    enhanced_tool = EnhancedWebplatformDigestTool(BASE_PATH)
    return await enhanced_tool.run(
        ctx=ctx,
        version=version,
        channel=channel,
        focus_areas=focus_areas,
        use_cache=use_cache,
        language=language,
        split_by_area=split_by_area,
        target_area=target_area,
        debug=debug,
        model=model,
        model_preferences=model_preferences,
    )




@mcp.tool()
async def split_features_by_heading(content: str, target_heading_level: int = 3) -> str:
    """Split content by heading level"""
    return await feature_splitter.split_features(
        {"content": content, "target_heading_level": target_heading_level}
    )


@mcp.tool()
async def check_latest_releases(ctx: Context, release_type: str = "webplatform", channel: str = "stable") -> str:
    """Check for latest available release versions and compare with local files

    Args:
        release_type: Type of releases to check ("webplatform")
        channel: Release channel for webplatform ("stable", "beta", "dev", "canary")

    Returns:
        JSON with latest versions and missing releases
    """
    return await release_monitor_tool.check_latest_releases(
        ctx, {"release_type": release_type, "channel": channel}
    )


@mcp.tool()
async def generate_github_pages(
    ctx: Context,
    version: str,
    channel: str = "stable",
    focus_areas: Optional[str] = None,
    language: str = "bilingual",
    force_regenerate: bool = False,
    skip_clean: bool = False,
    skip_digest: bool = False,
    skip_validation: bool = False,
    target_area: Optional[str] = None,
    debug: bool = False
) -> str:
    """Orchestrate digest generation, navigation refresh, and validation.

    Reuses existing per-area digests when available, and only re-runs the
    sampling pipeline when outputs are missing or force_regenerate is true.
    """

    return await github_pages_orchestrator.run(
        ctx,
        version=version,
        channel=channel,
        focus_areas=focus_areas,
        language=language,
        force_regenerate=force_regenerate,
        skip_clean=skip_clean,
        skip_digest=skip_digest,
        skip_validation=skip_validation,
        target_area=target_area,
        debug=debug
    )


@mcp.tool()
async def crawl_missing_releases(ctx: Context, release_type: str = "webplatform", channel: str = "stable",
                               confirmed: bool = False, force_redownload: bool = False) -> str:
    """Crawl missing release notes after user confirmation
    
    Args:
        release_type: Type of releases to crawl ("webplatform")
        channel: Release channel for webplatform ("stable", "beta", "dev", "canary")
        confirmed: Must be true to proceed with crawling
        force_redownload: Download even if file exists
        
    Returns:
        JSON with download results
    """
    return await release_monitor_tool.crawl_missing_releases(
        ctx, {"release_type": release_type, "channel": channel, "confirmed": confirmed, "force_redownload": force_redownload}
    )






# WebGPU YAML processing removed - use split_and_process_release_notes.py instead
# python3 src/processors/split_and_process_release_notes.py --version VERSION


# WebGPU merge removed - use split_and_process_release_notes.py instead
# python3 src/processors/split_and_process_release_notes.py --version VERSION


# Register all processed release notes as individual resources
def register_dynamic_resources():
    """Register all processed release notes as FastMCP resources"""
    resources = release_notes_resource.list_resources()
    
    for resource in resources:
        uri = resource["uri"]
        
        # Create a closure to capture the current URI
        def make_resource_getter(resource_uri):
            @mcp.resource(resource_uri, 
                         name=resource["name"],
                         description=resource["description"],
                         mime_type=resource["mimeType"])
            def get_resource() -> str:
                return release_notes_resource.read_resource(resource_uri)
            
            # Add metadata to the resource
            if hasattr(get_resource, "_resource"):
                get_resource._resource._meta = resource.get("_meta", {})
            
            return get_resource
        
        # Register the resource
        make_resource_getter(uri)

# Call the registration function when the server starts
register_dynamic_resources()


def main():
    """Initialize and run the FastMCP server"""
    
    print("Starting FastMCP Digest Server...")
    print("Resources registered:")
    print("- file://webplatform-prompt") 
    print(f"- {len(release_notes_resource.list_resources())} dynamic release note resources")
    print("\nTools available:")
    print("- webplatform_digest") 
    print("- split_features_by_heading")
    print("- check_latest_releases")
    print("- crawl_missing_releases")
    print("\nServer starting...")
    
    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()
