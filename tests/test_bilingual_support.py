"""Tests for bilingual support in the enhanced WebPlatform digest tool."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict
from unittest.mock import AsyncMock, Mock, patch

import pytest

from chrome_update_digest.mcp.tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool


@pytest.fixture
def base_path(tmp_path: Path) -> Path:
    """Provide an isolated base path with minimal config and prompt files."""
    config_src = Path(__file__).resolve().parent.parent / "config" / "focus_areas.yaml"

    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_dir.joinpath("focus_areas.yaml").write_text(config_src.read_text(encoding="utf-8"), encoding="utf-8")

    prompts_dir = tmp_path / "prompts" / "webplatform-prompts"
    prompts_dir.mkdir(parents=True)
    prompts_dir.joinpath("webplatform-prompt-en.md").write_text("English prompt for [AREA]", encoding="utf-8")
    prompts_dir.joinpath("webplatform-prompt-zh.md").write_text("中文提示 [AREA]", encoding="utf-8")
    prompts_dir.joinpath("webplatform-translation-prompt-zh.md").write_text(
        "Translate the markdown: [ENGLISH_DIGEST_MARKDOWN]", encoding="utf-8"
    )

    (tmp_path / "upstream_docs" / "processed_releasenotes" / "processed_forwebplatform").mkdir(parents=True)
    (tmp_path / "digest_markdown" / "webplatform").mkdir(parents=True)

    return tmp_path


@pytest.fixture
def tool(base_path: Path) -> EnhancedWebplatformDigestTool:
    """Return a tool instance pointing at the temporary base path."""
    return EnhancedWebplatformDigestTool(base_path=base_path)


@pytest.mark.asyncio
async def test_load_prompt_returns_language_specific_template(tool: EnhancedWebplatformDigestTool) -> None:
    """_load_prompt should return language specific templates when available."""
    ctx = Mock()

    en_prompt = await tool._load_prompt(ctx, "en", None, False)
    zh_prompt = await tool._load_prompt(ctx, "zh", None, False)

    assert "English prompt" in en_prompt
    assert "中文提示" in zh_prompt


@pytest.mark.asyncio
async def test_load_prompt_falls_back_when_language_missing(tool: EnhancedWebplatformDigestTool, base_path: Path) -> None:
    """If a language template is missing, the tool should fall back to the generic template."""
    (base_path / "prompts" / "webplatform-prompts" / "webplatform-prompt-zh.md").unlink()

    ctx = Mock()
    zh_prompt = await tool._load_prompt(ctx, "zh", None, False)

    assert "Language: zh" in zh_prompt


@pytest.mark.asyncio
async def test_generate_digest_from_yaml_calls_sample(tool: EnhancedWebplatformDigestTool) -> None:
    """_generate_digest_from_yaml should call ctx.sample with structured input."""
    captured_payload: Dict[str, str] = {}

    async def sample(messages=None, **kwargs):
        captured_payload["messages"] = messages
        return "# Generated Digest\n\nContent"

    ctx = Mock()
    ctx.sample = sample

    yaml_data = {
        "version": "139",
        "channel": "stable",
        "features": [
            {
                "title": "CSS Feature",
                "content": "Details",
                "primary_tags": [{"name": "css"}],
                "links": [{"url": "https://example.com", "title": "Example"}],
            }
        ],
        "statistics": {"total_features": 1, "total_links": 1},
    }

    digest = await tool._generate_digest_from_yaml(ctx, yaml_data, "en", None, False)

    assert "Generated Digest" in digest
    assert isinstance(captured_payload["messages"], str)


@pytest.mark.asyncio
async def test_generate_fallback_digest_contains_area(tool: EnhancedWebplatformDigestTool) -> None:
    """Fallback digest should include contextual information."""
    area_yaml = {
        "version": "139",
        "features": [
            {
                "title": "CSS Feature",
                "primary_tags": [{"name": "css"}],
                "links": [{"title": "Spec", "url": "https://example.com/spec"}],
            }
        ],
        "statistics": {"total_features": 1, "total_links": 1},
    }

    digest = tool._generate_fallback_digest(area_yaml, "en")

    assert "Chrome 139" in digest
    assert "https://example.com/spec" in digest


@pytest.mark.asyncio
async def test_run_supports_language_parameter(tool: EnhancedWebplatformDigestTool) -> None:
    """run should accept a language parameter and return a digest string."""
    ctx = Mock()
    ctx.sample = AsyncMock(return_value="# Digest\nContent")

    with patch.object(tool, "_get_yaml_data", return_value={
        "version": "139",
        "channel": "stable",
        "features": [],
        "statistics": {"total_features": 0, "total_links": 0},
    }):
        result = await tool.run(ctx, version="139", channel="stable", language="en", split_by_area=False)

    payload = json.loads(result)
    assert payload["success"] is True
    assert payload["language"] == "en"
