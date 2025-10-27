#!/usr/bin/env python3
"""
Integration tests for auto-regeneration of processed files in DigestYAMLCache.
"""

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from chrome_update_digest.mcp.tools._digest_yaml_cache import DigestYAMLCache
from chrome_update_digest.utils.yaml_pipeline import YAMLPipeline


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
    (tmp_path / "upstream_docs" / "processed_releasenotes" / "processed_forwebplatform" / "processed_yaml" / "areas").mkdir(
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
This is a test CSS feature with [documentation](https://example.com/css).

## Web APIs

### New Web API
This is a test Web API feature with [spec](https://example.com/api).

## Graphics

### WebGPU Update
This is a test WebGPU feature with [chromestatus](https://chromestatus.com/feature/123).
"""
    (tmp_path / "upstream_docs" / "release_notes" / "WebPlatform" / "chrome-138-stable.md").write_text(
        sample_release
    )
    
    return tmp_path


@pytest.fixture
def yaml_cache(mock_base_path):
    """Create a DigestYAMLCache instance."""
    cache_dir = (
        mock_base_path
        / "upstream_docs"
        / "processed_releasenotes"
        / "processed_forwebplatform"
        / "processed_yaml"
    )
    yaml_pipeline = YAMLPipeline()
    return DigestYAMLCache(mock_base_path, cache_dir, yaml_pipeline)


@pytest.mark.asyncio
async def test_auto_regeneration_when_files_missing(yaml_cache, mock_base_path):
    """Test that missing files trigger auto-regeneration."""
    # Mock context
    mock_ctx = MagicMock()
    
    # Initially, no processed files exist
    areas_dir = (
        mock_base_path
        / "upstream_docs"
        / "processed_releasenotes"
        / "processed_forwebplatform"
        / "areas"
    )
    assert not (areas_dir / "css" / "chrome-138-stable.md").exists()
    
    # Call get_yaml_data - should trigger auto-regeneration
    result = await yaml_cache.get_yaml_data(
        ctx=mock_ctx,
        version="138",
        channel="stable",
        use_cache=True,
        split_by_area=True,
        target_area="css",
        debug=True,
    )
    
    # Check that files were auto-generated
    assert (areas_dir / "css" / "chrome-138-stable.md").exists()
    assert result is not None

    notice = yaml_cache.consume_last_regeneration_notice()
    assert notice is not None
    assert notice.get("triggered") is True
    assert notice.get("success") is True
    assert "css" in notice.get("areas_missing", [])


@pytest.mark.asyncio
async def test_no_regeneration_when_files_exist(yaml_cache, mock_base_path):
    """Test that existing files prevent regeneration."""
    # Mock context
    mock_ctx = MagicMock()
    
    # Pre-create processed files
    areas_dir = (
        mock_base_path
        / "upstream_docs"
        / "processed_releasenotes"
        / "processed_forwebplatform"
        / "areas"
    )
    css_dir = areas_dir / "css"
    css_dir.mkdir(parents=True, exist_ok=True)
    (css_dir / "chrome-138-stable.md").write_text("# Existing CSS content")
    
    # Pre-create YAML file
    yaml_dir = (
        mock_base_path
        / "upstream_docs"
        / "processed_releasenotes"
        / "processed_forwebplatform"
        / "processed_yaml"
        / "areas"
        / "css"
    )
    yaml_dir.mkdir(parents=True, exist_ok=True)
    (yaml_dir / "chrome-138-stable.yml").write_text("""
version: "138"
channel: "stable"
area: "css"
features:
  - title: "Existing CSS Feature"
    content: "# Existing CSS Feature\\nThis is existing content."
    primary_tags: ["css"]
    links: []
statistics:
  total_features: 1
  total_links: 0
""")
    
    # Track telemetry to verify no regeneration occurred
    telemetry_file = mock_base_path / ".monitoring" / "webplatform-telemetry.jsonl"
    initial_size = telemetry_file.stat().st_size if telemetry_file.exists() else 0
    
    # Call get_yaml_data
    result = await yaml_cache.get_yaml_data(
        ctx=mock_ctx,
        version="138",
        channel="stable",
        use_cache=True,
        split_by_area=True,
        target_area="css",
        debug=False,
    )
    
    # Verify result loaded from cache
    assert result is not None
    assert result.get("area") == "css"

    # Ensure no regeneration notice is left behind
    assert yaml_cache.consume_last_regeneration_notice() is None
    
    # Check that no new telemetry events were added for regeneration
    # (some events may be added for normal cache operations)
    if telemetry_file.exists():
        content = telemetry_file.read_text()
        # Should not contain clean_data_pipeline_run events
        assert "clean_data_pipeline_run" not in content or content.count("clean_data_pipeline_run") == 0


@pytest.mark.asyncio
async def test_auto_regeneration_disabled(yaml_cache, mock_base_path):
    """Test behavior when auto-regeneration is disabled."""
    # Disable auto-regeneration
    yaml_cache._auto_regeneration_enabled = False
    
    # Mock context
    mock_ctx = MagicMock()
    
    # No processed files exist
    areas_dir = (
        mock_base_path
        / "upstream_docs"
        / "processed_releasenotes"
        / "processed_forwebplatform"
        / "areas"
    )
    assert not (areas_dir / "css" / "chrome-138-stable.md").exists()
    
    # Call get_yaml_data - should NOT trigger auto-regeneration
    result = await yaml_cache.get_yaml_data(
        ctx=mock_ctx,
        version="138",
        channel="stable",
        use_cache=True,
        split_by_area=True,
        target_area="css",
        debug=False,
    )
    
    # Result may still be generated through normal pipeline
    # but no pre-emptive regeneration should occur
    assert yaml_cache.consume_last_regeneration_notice() is None


@pytest.mark.asyncio
async def test_auto_regeneration_for_all_areas(yaml_cache, mock_base_path):
    """Test auto-regeneration when requesting all areas."""
    # Mock context
    mock_ctx = MagicMock()
    
    # No processed files exist initially
    areas_dir = (
        mock_base_path
        / "upstream_docs"
        / "processed_releasenotes"
        / "processed_forwebplatform"
        / "areas"
    )
    
    # Call get_yaml_data for all areas
    result = await yaml_cache.get_yaml_data(
        ctx=mock_ctx,
        version="138",
        channel="stable",
        use_cache=True,
        split_by_area=True,
        target_area=None,  # All areas
        debug=True,
    )
    
    # Check that multiple area files were generated
    assert result is not None
    if result.get("areas"):
        # Some areas should have been processed
        assert len(result["areas"]) > 0

    notice = yaml_cache.consume_last_regeneration_notice()
    assert notice is not None and notice.get("triggered")


@pytest.mark.asyncio
async def test_auto_regeneration_failure_handling(yaml_cache, mock_base_path):
    """Test graceful handling of regeneration failures."""
    # Mock context
    mock_ctx = MagicMock()
    
    # Delete the release notes to cause regeneration to fail
    release_note = (
        mock_base_path
        / "upstream_docs"
        / "release_notes"
        / "WebPlatform"
        / "chrome-138-stable.md"
    )
    release_note.unlink()
    
    # Call get_yaml_data - regeneration should fail gracefully
    result = await yaml_cache.get_yaml_data(
        ctx=mock_ctx,
        version="138",
        channel="stable",
        use_cache=True,
        split_by_area=True,
        target_area="css",
        debug=True,
    )
    
    # Should return None or handle failure gracefully
    assert result is None

    notice = yaml_cache.consume_last_regeneration_notice()
    assert notice is not None
    assert notice.get("triggered") is True
    assert notice.get("success") is False


@pytest.mark.asyncio
async def test_cache_hit_after_regeneration(yaml_cache, mock_base_path):
    """Test that cache hits work properly after auto-regeneration."""
    # Mock context
    mock_ctx = MagicMock()
    
    # First call - triggers regeneration
    result1 = await yaml_cache.get_yaml_data(
        ctx=mock_ctx,
        version="138",
        channel="stable",
        use_cache=True,
        split_by_area=True,
        target_area="css",
        debug=False,
    )

    initial_cache_hits = yaml_cache.cache_hits

    notice = yaml_cache.consume_last_regeneration_notice()
    assert notice is not None and notice.get("triggered")
    
    # Second call - should hit cache
    result2 = await yaml_cache.get_yaml_data(
        ctx=mock_ctx,
        version="138",
        channel="stable",
        use_cache=True,
        split_by_area=True,
        target_area="css",
        debug=False,
    )
    
    # Cache hits should increase
    assert yaml_cache.cache_hits > initial_cache_hits
    assert result1 is not None
    assert result2 is not None


@pytest.mark.asyncio
async def test_partial_files_trigger_regeneration(yaml_cache, mock_base_path):
    """Test that having only markdown (without YAML) triggers regeneration."""
    # Mock context
    mock_ctx = MagicMock()
    
    # Create only markdown file, not YAML
    areas_dir = (
        mock_base_path
        / "upstream_docs"
        / "processed_releasenotes"
        / "processed_forwebplatform"
        / "areas"
    )
    css_dir = areas_dir / "css"
    css_dir.mkdir(parents=True, exist_ok=True)
    (css_dir / "chrome-138-stable.md").write_text("# CSS content")
    
    # YAML file does not exist
    yaml_path = (
        mock_base_path
        / "upstream_docs"
        / "processed_releasenotes"
        / "processed_forwebplatform"
        / "processed_yaml"
        / "areas"
        / "css"
        / "chrome-138-stable.yml"
    )
    assert not yaml_path.exists()
    
    # Call get_yaml_data - should trigger regeneration to create YAML
    result = await yaml_cache.get_yaml_data(
        ctx=mock_ctx,
        version="138",
        channel="stable",
        use_cache=True,
        split_by_area=True,
        target_area="css",
        debug=True,
    )
    
    # Check that YAML was generated
    assert yaml_path.exists()
    assert result is not None

    notice = yaml_cache.consume_last_regeneration_notice()
    assert notice is not None and notice.get("triggered")


@pytest.mark.asyncio
async def test_telemetry_for_auto_regeneration(yaml_cache, mock_base_path):
    """Test that telemetry is properly recorded during auto-regeneration."""
    # Mock context
    mock_ctx = MagicMock()
    
    # Ensure telemetry file doesn't exist initially
    telemetry_file = mock_base_path / ".monitoring" / "webplatform-telemetry.jsonl"
    if telemetry_file.exists():
        telemetry_file.unlink()
    
    # Call get_yaml_data - triggers auto-regeneration
    result = await yaml_cache.get_yaml_data(
        ctx=mock_ctx,
        version="138",
        channel="stable",
        use_cache=True,
        split_by_area=True,
        target_area="css",
        debug=True,
    )

    # Check telemetry was recorded
    assert telemetry_file.exists()
    content = telemetry_file.read_text()
    
    # Should contain clean_data_pipeline_run event
    assert "clean_data_pipeline_run" in content
    assert '"triggered_by": "mcp_tool"' in content

    notice = yaml_cache.consume_last_regeneration_notice()
    assert notice is not None and notice.get("triggered")
