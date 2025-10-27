#!/usr/bin/env python3
"""
Tests for the clean data pipeline MCP tool.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from chrome_update_digest.mcp.tools.clean_data_pipeline_tool import (
    CleanDataPipelineTool,
)


@pytest.fixture
def mock_base_path(tmp_path):
    """Create a mock base path with necessary directory structure."""
    # Create directory structure
    (tmp_path / "upstream_docs" / "release_notes" / "WebPlatform").mkdir(
        parents=True, exist_ok=True
    )
    (tmp_path / "upstream_docs" / "processed_releasenotes" / "processed_forwebplatform" / "areas").mkdir(
        parents=True, exist_ok=True
    )
    (tmp_path / "config").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".monitoring").mkdir(parents=True, exist_ok=True)
    
    # Create a minimal focus_areas.yaml
    focus_areas = """focus_areas:
  css:
    heading_patterns: ["CSS"]
    keywords: ["css", "style"]
  webapi:
    heading_patterns: ["Web APIs"]
    keywords: ["api", "webapi"]
  graphics-webgpu:
    heading_patterns: ["WebGPU", "Graphics"]
    keywords: ["webgpu", "graphics"]
"""
    (tmp_path / "config" / "focus_areas.yaml").write_text(focus_areas)
    
    # Create a sample release note
    sample_release = """# Chrome 138 Release Notes

## CSS

### New CSS Feature
This is a test CSS feature.

## Web APIs

### New Web API
This is a test Web API feature.

## Graphics

### WebGPU Update
This is a test WebGPU feature.
"""
    (tmp_path / "upstream_docs" / "release_notes" / "WebPlatform" / "chrome-138.md").write_text(
        sample_release
    )
    
    return tmp_path


@pytest.mark.asyncio
async def test_run_pipeline_success(mock_base_path):
    """Test successful pipeline execution."""
    tool = CleanDataPipelineTool(mock_base_path)
    
    result = await tool.run_pipeline(
        version="138",
        channel="stable",
        with_yaml=False,  # Skip YAML for simplicity
        debug=False,
    )
    
    assert result["success"] is True
    assert result["version"] == "138"
    assert result["channel"] == "stable"
    assert "markdown_files" in result
    assert result["markdown_files_count"] >= 0
    assert "duration_seconds" in result
    assert "timestamp" in result


@pytest.mark.asyncio
async def test_run_pipeline_with_yaml(mock_base_path):
    """Test pipeline execution with YAML generation."""
    tool = CleanDataPipelineTool(mock_base_path)
    
    result = await tool.run_pipeline(
        version="138",
        channel="stable",
        with_yaml=True,
        debug=False,
    )
    
    assert result["success"] is True
    assert "yaml_files" in result
    assert "yaml_files_count" in result


@pytest.mark.asyncio
async def test_run_pipeline_file_not_found(mock_base_path):
    """Test pipeline behavior when release notes are missing."""
    tool = CleanDataPipelineTool(mock_base_path)
    
    result = await tool.run_pipeline(
        version="999",  # Non-existent version
        channel="stable",
        with_yaml=False,
        debug=False,
    )
    
    assert result["success"] is False
    assert result["error_type"] == "FileNotFoundError"
    assert "Release notes not found" in result["message"]


@pytest.mark.asyncio
async def test_run_pipeline_debug_mode(mock_base_path, capsys):
    """Test pipeline execution with debug logging."""
    tool = CleanDataPipelineTool(mock_base_path)
    
    result = await tool.run_pipeline(
        version="138",
        channel="stable",
        with_yaml=False,
        debug=True,
    )
    
    assert result["success"] is True
    
    # Check that debug output was produced
    captured = capsys.readouterr()
    assert "Running clean data pipeline" in captured.out or len(captured.out) > 0


def test_check_processed_files_exist_all_present(mock_base_path):
    """Test checking for processed files when all are present."""
    tool = CleanDataPipelineTool(mock_base_path)
    
    # Create some processed files
    areas_dir = (
        mock_base_path
        / "upstream_docs"
        / "processed_releasenotes"
        / "processed_forwebplatform"
        / "areas"
    )
    
    for area in ["css", "webapi", "graphics-webgpu"]:
        area_dir = areas_dir / area
        area_dir.mkdir(parents=True, exist_ok=True)
        (area_dir / "chrome-138-stable.md").write_text(f"# {area} content")
    
    # Create YAML files
    yaml_dir = (
        mock_base_path
        / "upstream_docs"
        / "processed_releasenotes"
        / "processed_forwebplatform"
        / "processed_yaml"
        / "areas"
    )
    
    for area in ["css", "webapi", "graphics-webgpu"]:
        area_yaml_dir = yaml_dir / area
        area_yaml_dir.mkdir(parents=True, exist_ok=True)
        (area_yaml_dir / "chrome-138-stable.yml").write_text(f"# {area} yaml")
    
    result = tool.check_processed_files_exist(
        version="138",
        channel="stable",
        split_by_area=True,
    )
    
    assert result["markdown_exists"] is True
    assert result["yaml_exists"] is True
    assert len(result["missing_areas"]) == 0


def test_check_processed_files_exist_some_missing(mock_base_path):
    """Test checking for processed files when some are missing."""
    tool = CleanDataPipelineTool(mock_base_path)
    
    # Create only some processed files
    areas_dir = (
        mock_base_path
        / "upstream_docs"
        / "processed_releasenotes"
        / "processed_forwebplatform"
        / "areas"
    )
    
    # Only create CSS area
    css_dir = areas_dir / "css"
    css_dir.mkdir(parents=True, exist_ok=True)
    (css_dir / "chrome-138-stable.md").write_text("# CSS content")
    
    result = tool.check_processed_files_exist(
        version="138",
        channel="stable",
        split_by_area=True,
    )
    
    assert result["markdown_exists"] is False
    assert result["yaml_exists"] is False
    assert len(result["missing_areas"]) > 0
    assert "webapi" in result["missing_markdown_areas"]


def test_check_processed_files_exist_none_present(mock_base_path):
    """Test checking for processed files when none are present."""
    tool = CleanDataPipelineTool(mock_base_path)
    
    result = tool.check_processed_files_exist(
        version="138",
        channel="stable",
        split_by_area=True,
    )
    
    assert result["markdown_exists"] is False
    assert result["yaml_exists"] is False
    assert "all" in result["missing_areas"] or len(result["missing_areas"]) > 0


@pytest.mark.asyncio
async def test_telemetry_recorded_on_success(mock_base_path):
    """Test that telemetry events are recorded on successful execution."""
    tool = CleanDataPipelineTool(mock_base_path)
    
    result = await tool.run_pipeline(
        version="138",
        channel="stable",
        with_yaml=False,
        debug=False,
    )
    
    # Check that telemetry file was created
    telemetry_file = mock_base_path / ".monitoring" / "webplatform-telemetry.jsonl"
    assert telemetry_file.exists()
    
    # Read and verify telemetry content
    content = telemetry_file.read_text()
    assert "clean_data_pipeline_run" in content
    assert '"success": true' in content


@pytest.mark.asyncio
async def test_telemetry_recorded_on_failure(mock_base_path):
    """Test that telemetry events are recorded on failed execution."""
    tool = CleanDataPipelineTool(mock_base_path)
    
    result = await tool.run_pipeline(
        version="999",  # Non-existent version
        channel="stable",
        with_yaml=False,
        debug=False,
    )
    
    # Check that telemetry file was created
    telemetry_file = mock_base_path / ".monitoring" / "webplatform-telemetry.jsonl"
    assert telemetry_file.exists()
    
    # Read and verify telemetry content
    content = telemetry_file.read_text()
    assert "clean_data_pipeline_run" in content
    assert '"success": false' in content


def test_check_single_file_mode(mock_base_path):
    """Test checking for processed files in single-file mode."""
    tool = CleanDataPipelineTool(mock_base_path)
    
    # Create single aggregated file
    single_file = (
        mock_base_path
        / "upstream_docs"
        / "processed_releasenotes"
        / "processed_forwebplatform"
        / "138-webplatform-with-webgpu.md"
    )
    single_file.parent.mkdir(parents=True, exist_ok=True)
    single_file.write_text("# Aggregated content")
    
    result = tool.check_processed_files_exist(
        version="138",
        channel="stable",
        split_by_area=False,
    )
    
    assert result["markdown_exists"] is True
    assert result["yaml_exists"] is False  # Single file mode doesn't use YAML
    assert len(result["missing_areas"]) == 0


@pytest.mark.asyncio
async def test_custom_output_directories(mock_base_path):
    """Test pipeline execution with custom output directories."""
    custom_md_dir = mock_base_path / "custom" / "markdown"
    custom_yaml_dir = mock_base_path / "custom" / "yaml"
    
    tool = CleanDataPipelineTool(mock_base_path)
    
    result = await tool.run_pipeline(
        version="138",
        channel="stable",
        with_yaml=False,
        markdown_output_dir=custom_md_dir,
        yaml_output_dir=custom_yaml_dir,
        debug=False,
    )
    
    assert result["success"] is True
    
    # Verify custom directories were used
    assert custom_md_dir.exists()


@pytest.mark.asyncio
async def test_beta_channel_processing(mock_base_path):
    """Test processing beta channel release notes."""
    # Create a beta release note
    beta_release = """# Chrome 138 Beta Release Notes

## CSS

### Beta CSS Feature
This is a beta CSS feature.
"""
    (
        mock_base_path / "upstream_docs" / "release_notes" / "WebPlatform" / "chrome-138-beta.md"
    ).write_text(beta_release)
    
    tool = CleanDataPipelineTool(mock_base_path)
    
    result = await tool.run_pipeline(
        version="138",
        channel="beta",
        with_yaml=False,
        debug=False,
    )
    
    assert result["success"] is True
    assert result["channel"] == "beta"
