#!/usr/bin/env python3
"""
Chrome Digest FastMCP Server
Modern MCP server implementation using FastMCP with sampling and resource management.
Provides tools for generating web platform digests from processed Chrome release notes.
"""

import json
import sys
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from fastmcp import FastMCP, Context
from fastmcp.resources import FileResource

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

# Import tool classes
from mcp_tools._digest_runtime import DigestRuntimeRegistry
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
digest_registry = DigestRuntimeRegistry(BASE_PATH)


def _jsonify(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


async def _json_tool_call(coro) -> str:
    try:
        result = await coro
    except Exception as exc:  # pragma: no cover - defensive path
        return _jsonify({"success": False, "error": str(exc)})
    return _jsonify(result)


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
    return await _json_tool_call(digest_registry.summarize_progress())


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
    result = await digest_registry.run_full_digest(
        ctx,
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
    if isinstance(result, (dict, list)):
        return _jsonify({"success": True, "payload": result})
    return result


@mcp.tool("digest_prepare_yaml")
async def digest_prepare_yaml(
    ctx: Context,
    version: str,
    channel: str = "stable",
    focus_areas: Optional[str] = None,
    use_cache: bool = True,
    language: Optional[str] = "bilingual",
    split_by_area: bool = True,
    target_area: Optional[str] = None,
    debug: bool = False,
    model: Optional[str] = None,
    model_preferences: Optional[Any] = None,
) -> str:
    """Preload YAML data, initialise shared run state, and return run metadata."""
    return await _json_tool_call(
        digest_registry.prepare_yaml(
            ctx,
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
    )


@mcp.tool("digest_generate_area")
async def digest_generate_area(
    ctx: Context,
    run_id: str,
    area: str,
    debug: Optional[bool] = None,
) -> str:
    """Generate the English digest for a specific area within an active run."""
    return await _json_tool_call(
        digest_registry.generate_area(
            ctx,
            run_id=run_id,
            area=area,
            debug=debug,
        )
    )


@mcp.tool("digest_translate_area")
async def digest_translate_area(
    ctx: Context,
    run_id: str,
    area: str,
    debug: Optional[bool] = None,
) -> str:
    """Translate a previously generated English digest to Chinese for an area."""
    return await _json_tool_call(
        digest_registry.translate_area(
            ctx,
            run_id=run_id,
            area=area,
            debug=debug,
        )
    )


@mcp.tool("digest_write_outputs")
async def digest_write_outputs(ctx: Context, run_id: str) -> str:
    """Finalize a run by flushing progress data and returning the output manifest."""
    return await _json_tool_call(digest_registry.write_outputs(run_id=run_id))


@mcp.tool("digest_inspect_cache")
async def digest_inspect_cache(area: Optional[str] = None) -> str:
    """Inspect in-memory YAML cache statistics, optionally focusing on one area."""
    return await _json_tool_call(digest_registry.inspect_cache(area=area))


@mcp.tool("digest_validate_links")
async def digest_validate_links(ctx: Context, version: str, channel: str = "stable") -> str:
    """Validate all extracted links for the specified release notes dataset."""
    return await _json_tool_call(
        digest_registry.validate_links(ctx, version=version, channel=channel)
    )


@mcp.tool("digest_summarize_progress")
async def digest_summarize_progress() -> str:
    """Return the latest digest progress snapshot from the monitoring store."""
    return await _json_tool_call(digest_registry.summarize_progress())


@mcp.tool("digest_list_outputs")
async def digest_list_outputs(run_id: Optional[str] = None) -> str:
    """List generated digest files on disk, optionally restricted to a run."""
    return await _json_tool_call(digest_registry.list_outputs(run_id=run_id))


@mcp.tool("digest_describe_run_config")
async def digest_describe_run_config(run_id: str) -> str:
    """Describe the configuration and status of an active or cached run."""
    return await _json_tool_call(digest_registry.describe_run_config(run_id))


@mcp.tool("digest_reset_run_state")
async def digest_reset_run_state(run_id: Optional[str] = None, reset_cache: bool = False) -> str:
    """Clear tracked run state and optionally reset the per-process YAML cache."""
    return await _json_tool_call(
        digest_registry.reset_run_state(run_id=run_id, reset_cache=reset_cache)
    )


@mcp.tool("digest_available_prompts")
async def digest_available_prompts() -> str:
    """List available prompt templates that the digest pipeline can reference."""
    return await _json_tool_call(digest_registry.available_prompts())


@mcp.tool("digest_register_release_resources")
async def digest_register_release_resources(include_release_notes: bool = True) -> str:
    """Register processed release note resources on demand for MCP clients."""
    count = register_dynamic_resources(include_release_notes=include_release_notes)
    payload = {
        "success": True,
        "release_resources_registered": count,
        "lazy_mode": not include_release_notes,
    }
    return _jsonify(payload)


@mcp.tool("telemetry_report_metrics")
async def telemetry_report_metrics() -> str:
    """Return per-tool runtime metrics collected by the shared digest registry."""
    return await _json_tool_call(digest_registry.report_metrics())


@mcp.tool("progress_watch")
async def progress_watch() -> str:
    """Convenience wrapper that mirrors digest_summarize_progress for watchers."""
    return await _json_tool_call(digest_registry.summarize_progress())


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

    async def handler():
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
            debug=debug,
        )

    result = await digest_registry.run_serialized("generate_github_pages", handler)
    if isinstance(result, (dict, list)):
        return _jsonify(result)
    return result


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
def register_dynamic_resources(include_release_notes: bool = False) -> int:
    """Register processed release notes as FastMCP resources when requested."""
    if not include_release_notes:
        return 0

    resources = release_notes_resource.list_resources()
    registered = 0
    
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
        registered += 1

    return registered

PRELOAD_RELEASE_RESOURCES = os.getenv("DIGEST_PRELOAD_RELEASE_RESOURCES", "0") == "1"
PRELOADED_RELEASE_RESOURCES = (
    register_dynamic_resources(include_release_notes=True) if PRELOAD_RELEASE_RESOURCES else 0
)


def main():
    """Initialize and run the FastMCP server"""
    
    print("Starting FastMCP Digest Server...")
    print("Resources registered:")
    print("- file://webplatform-prompt")
    if PRELOAD_RELEASE_RESOURCES:
        print(f"- {PRELOADED_RELEASE_RESOURCES} dynamic release note resources (preloaded)")
    else:
        print("- Release note resources registered lazily on first request")
    print("\nTools available:")
    print("- webplatform_digest (monolithic fallback)")
    print("- digest_prepare_yaml / digest_generate_area / digest_translate_area / digest_write_outputs")
    print("- digest_inspect_cache / digest_validate_links / digest_list_outputs")
    print("- digest_describe_run_config / digest_reset_run_state / digest_available_prompts")
    print("- digest_summarize_progress / progress_watch / telemetry_report_metrics")
    print("- digest_register_release_resources")
    print("- generate_github_pages")
    print("- split_features_by_heading")
    print("- check_latest_releases / crawl_missing_releases")
    print("\nServer starting...")
    
    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()
