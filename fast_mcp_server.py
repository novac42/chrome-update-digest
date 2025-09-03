#!/usr/bin/env python3
"""
Chrome Digest FastMCP Server
Modern MCP server implementation using FastMCP with sampling and resource management.
Provides tools for generating enterprise and web platform digests from processed Chrome release notes.
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
from mcp_tools.enterprise_digest import EnterpriseDigestTool
from mcp_tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool
from mcp_tools.feature_splitter import FeatureSplitterTool
from mcp_tools.release_monitor import ReleaseMonitorTool
from mcp_tools.profile_feature_extractor import ProfileFeatureExtractorTool
from mcp_tools.enterprise_notes_processor import EnterpriseNotesProcessorTool
# WebGPU tools removed - functionality integrated into main pipeline

# Import resource classes
from mcp_resources.processed_releasenotes import ProcessedReleaseNotesResource

# Initialize FastMCP server
mcp = FastMCP("DigestServer")

# Base path for the server
BASE_PATH = Path(__file__).parent


# Setup static resources
@mcp.resource("file://enterprise-prompt", mime_type="text/markdown")
def get_enterprise_prompt() -> str:
    """Enterprise digest generation prompt (bilingual)"""
    enterprise_prompt_path = BASE_PATH / "prompts" / "enterprise-prompts" / "enterprise-prompt-bilingual.md"
    if enterprise_prompt_path.exists():
        with open(enterprise_prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Enterprise prompt file not found"

@mcp.resource("file://webplatform-prompt", mime_type="text/markdown")
def get_webplatform_prompt() -> str:
    """WebPlatform digest generation prompt (bilingual)"""
    webplatform_prompt_path = BASE_PATH / "prompts" / "webplatform-prompts" / "webplatform-prompt-bilingual.md"
    if webplatform_prompt_path.exists():
        with open(webplatform_prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return "WebPlatform prompt file not found"

@mcp.resource("file://profile-keywords", mime_type="text/plain")
def get_profile_keywords() -> str:
    """Profile keywords for feature identification"""
    profile_keywords_path = BASE_PATH / "prompts" / "profile-keywords.txt"
    if profile_keywords_path.exists():
        with open(profile_keywords_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Profile keywords file not found"


# Initialize tool instances
enterprise_tool = EnterpriseDigestTool(BASE_PATH)
feature_splitter = FeatureSplitterTool(BASE_PATH)
release_monitor_tool = ReleaseMonitorTool(BASE_PATH)
profile_extractor_tool = ProfileFeatureExtractorTool(BASE_PATH)
enterprise_processor_tool = EnterpriseNotesProcessorTool(BASE_PATH)
# WebGPU tools initialization removed - use split_and_process_release_notes.py instead

# Initialize resource handler
release_notes_resource = ProcessedReleaseNotesResource(BASE_PATH)


async def load_prompt_from_resource(resource_name: str) -> str:
    """从本地文件读取prompt内容（暂时直接读取文件，后续可改为resource读取）"""
    try:
        if resource_name == "enterprise-prompt":
            file_path = BASE_PATH / "prompts" / "enterprise-prompts" / "enterprise-prompt-bilingual.md"
        elif resource_name == "webplatform-prompt":
            file_path = BASE_PATH / "prompts" / "webplatform-prompts" / "webplatform-prompt-bilingual.md"
        elif resource_name == "profile-keywords":
            file_path = BASE_PATH / "prompts" / "profile-keywords.txt"
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
        if data_type == "enterprise":
            data_path = BASE_PATH / "upstream_docs" / "processed_releasenotes" / "processed_forenterprise" / f"{version}-organized_chromechanges-enterprise.md"
        elif data_type == "webplatform":
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
async def enterprise_digest(ctx: Context, version: int, channel: str = "stable", 
                          focus_area: str = "all", custom_instruction: str = "") -> str:
    """Generate enterprise digest using FastMCP sampling and resources
    
    Args:
        version: Chrome version number (e.g., 138)
        channel: Chrome release channel (default: stable)  
        focus_area: Enterprise area to emphasize (productivity, security, management, all)
        custom_instruction: Additional custom instructions for digest generation
    """
    return await enterprise_tool.generate_digest_with_sampling(
        ctx, {"version": version, "channel": channel, "focus_area": focus_area, "custom_instruction": custom_instruction}
    )


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
                                     target_area: Optional[str] = None, debug: bool = False) -> str:
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
    return await enhanced_tool.run(ctx, version, channel, focus_areas, use_cache, language, 
                                  split_by_area, target_area, debug)




@mcp.tool()
async def split_features_by_heading(content: str, target_heading_level: int = 3) -> str:
    """Split content by heading level"""
    return await feature_splitter.split_features(
        {"content": content, "target_heading_level": target_heading_level}
    )


@mcp.tool()
async def check_latest_releases(ctx: Context, release_type: str = "both", channel: str = "stable") -> str:
    """Check for latest available release versions and compare with local files
    
    Args:
        release_type: Type of releases to check ("webplatform", "enterprise", "both")
        channel: Release channel for webplatform ("stable", "beta", "dev", "canary")
        
    Returns:
        JSON with latest versions and missing releases
    """
    return await release_monitor_tool.check_latest_releases(
        ctx, {"release_type": release_type, "channel": channel}
    )


@mcp.tool()
async def crawl_missing_releases(ctx: Context, release_type: str = "both", channel: str = "stable",
                               confirmed: bool = False, force_redownload: bool = False) -> str:
    """Crawl missing release notes after user confirmation
    
    Args:
        release_type: Type of releases to crawl ("webplatform", "enterprise", "both")
        channel: Release channel for webplatform ("stable", "beta", "dev", "canary")
        confirmed: Must be true to proceed with crawling
        force_redownload: Download even if file exists
        
    Returns:
        JSON with download results
    """
    return await release_monitor_tool.crawl_missing_releases(
        ctx, {"release_type": release_type, "channel": channel, "confirmed": confirmed, "force_redownload": force_redownload}
    )


@mcp.tool()
async def extract_profile_features(ctx: Context, version: int, 
                                  output_format: str = "markdown",
                                  keywords_override: Optional[str] = None) -> str:
    """Extract profile-related features from Chrome Enterprise Release Notes
    
    Args:
        version: Chrome version number
        output_format: Output format ("markdown", "json", "yaml")
        keywords_override: Optional custom keywords (comma-separated)
    
    Returns:
        Formatted profile features report
    """
    return await profile_extractor_tool.extract_profile_features(
        ctx, version, output_format, keywords_override
    )


@mcp.tool()
async def process_enterprise_notes(ctx: Context, version: int,
                                  format_override: Optional[str] = None,
                                  generate_organized: bool = True) -> str:
    """Process Chrome Enterprise release notes to extract and organize features
    
    Args:
        version: Chrome version number
        format_override: Override format detection ("new", "legacy", None for auto)
        generate_organized: Whether to generate organized markdown output
    
    Returns:
        JSON with processing results
    """
    return await enterprise_processor_tool.process_enterprise_notes(
        ctx, version, format_override, generate_organized
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
    print("- file://enterprise-prompt")
    print("- file://webplatform-prompt") 
    print("- file://profile-keywords")
    print(f"- {len(release_notes_resource.list_resources())} dynamic release note resources")
    print("\nTools available:")
    print("- enterprise_digest")
    print("- webplatform_digest") 
    print("- split_features_by_heading")
    print("- check_latest_releases")
    print("- crawl_missing_releases")
    print("\nServer starting...")
    
    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()
