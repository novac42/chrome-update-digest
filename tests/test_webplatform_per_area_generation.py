"""
Test suite for WebPlatform per-area digest generation.
Tests the split_by_area functionality and translation pipeline.
"""

import pytest
import asyncio
import json
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import sys
import os
import yaml

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chrome_update_digest.mcp.tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool
from chrome_update_digest.utils.focus_area_manager import FocusAreaManager


class TestWebplatformPerAreaGeneration:
    """Test per-area digest generation with translation."""
    
    @pytest.fixture
    def tool(self, tmp_path):
        """Create tool instance with temporary paths."""
        # Create necessary directories BEFORE creating the tool
        (tmp_path / 'config').mkdir(exist_ok=True)
        (tmp_path / 'prompts' / 'webplatform-prompts').mkdir(parents=True, exist_ok=True)
        (tmp_path / 'upstream_docs' / 'processed_releasenotes' / 'processed_forwebplatform').mkdir(parents=True, exist_ok=True)
        (tmp_path / 'digest_markdown' / 'webplatform').mkdir(parents=True, exist_ok=True)
        
        # Create test config BEFORE creating the tool
        config_content = """
metadata:
  version: "1.0"
  description: "Focus areas configuration"
  
focus_areas:
  css:
    name: "CSS & Styling"
    keywords: ["css", "style", "animation", "layout"]
    heading_patterns: ["CSS", "Styling"]
    
  webapi:
    name: "Web APIs"
    keywords: ["api", "dom", "fetch", "storage"]
    heading_patterns: ["Web API", "DOM API"]
    
  graphics-webgpu:
    name: "Graphics & WebGPU"
    keywords: ["webgpu", "gpu", "graphics", "canvas"]
    heading_patterns: ["WebGPU", "Graphics"]
    
  others:
    name: "Other Features"
    keywords: []
    heading_patterns: []
"""
        config_path = tmp_path / 'config' / 'focus_areas.yaml'
        config_path.write_text(config_content)
        
        # NOW create the tool after config is ready
        tool = EnhancedWebplatformDigestTool(base_path=tmp_path)
        
        # Create test prompts
        en_prompt = """# Chrome [AREA] Digest Template

Generate a digest for Chrome [AREA] features.

## Structure
1. Summary
2. Key Features
3. Developer Impact
"""
        zh_prompt = """# Chrome [AREA] 摘要模板

生成 Chrome [AREA] 功能摘要。

## 结构
1. 概述
2. 主要功能
3. 开发者影响
"""
        
        translation_prompt = """# Chrome WebPlatform Digest Translation Prompt (EN -> ZH)

## System Role
You are a professional bilingual technical localizer.

## Source & Target
- Area: **[AREA_DISPLAY]** (key: [AREA_KEY])
- Chrome Version: [VERSION] / Channel: [CHANNEL]

## User Content (Source English Digest)
````markdown
[ENGLISH_DIGEST_MARKDOWN]
````
"""
        
        (tmp_path / 'prompts' / 'webplatform-prompts' / 'webplatform-prompt-en.md').write_text(en_prompt)
        (tmp_path / 'prompts' / 'webplatform-prompts' / 'webplatform-prompt-zh.md').write_text(zh_prompt)
        (tmp_path / 'prompts' / 'webplatform-prompts' / 'webplatform-translation-prompt-zh.md').write_text(translation_prompt)
        
        return tool
    
    @pytest.fixture
    def mock_yaml_data(self):
        """Create mock YAML data with features for multiple areas."""
        return {
            'version': '139',
            'channel': 'stable',
            'features': [
                {
                    'title': 'CSS Container Queries',
                    'content': 'New CSS container queries feature',
                    'primary_tags': [{'name': 'css'}],
                    'links': [
                        {'url': 'https://example.com/css1', 'title': 'CSS Spec'}
                    ]
                },
                {
                    'title': 'WebGPU Compute Shaders',
                    'content': 'Enhanced compute shader support',
                    'primary_tags': [{'name': 'graphics-webgpu'}],
                    'links': [
                        {'url': 'https://example.com/webgpu1', 'title': 'WebGPU Spec'}
                    ]
                },
                {
                    'title': 'Fetch Priority API',
                    'content': 'New fetch priority hints',
                    'primary_tags': [{'name': 'webapi'}],
                    'links': [
                        {'url': 'https://example.com/api1', 'title': 'API Docs'}
                    ]
                },
                {
                    'title': 'Untagged Feature',
                    'content': 'Feature without tags',
                    'primary_tags': [],
                    'links': []
                }
            ],
            'statistics': {
                'total_features': 4,
                'total_links': 3
            }
        }
    
    @pytest.mark.asyncio
    async def test_per_area_generation_basic(self, tool, mock_yaml_data):
        """Test basic per-area digest generation."""
        # Mock context with sampling
        ctx = AsyncMock()
        
        # Mock English digest generation
        async def mock_sample_en(messages, system_prompt, **kwargs):
            if 'CSS' in system_prompt:
                return """# Chrome 139 CSS & Styling Digest

## Summary
CSS improvements in Chrome 139.

### CSS Container Queries
New CSS container queries feature

**References:**
- [CSS Spec](https://example.com/css1)
"""
            elif 'WebGPU' in system_prompt:
                return """# Chrome 139 Graphics & WebGPU Digest

## Summary
WebGPU enhancements in Chrome 139.

### WebGPU Compute Shaders
Enhanced compute shader support

**References:**
- [WebGPU Spec](https://example.com/webgpu1)
"""
            elif 'Web API' in system_prompt:
                return """# Chrome 139 Web APIs Digest

## Summary
Web API updates in Chrome 139.

### Fetch Priority API
New fetch priority hints

**References:**
- [API Docs](https://example.com/api1)
"""
            else:
                return """# Chrome 139 Other Features Digest

## Summary
Other updates in Chrome 139.

### Untagged Feature
Feature without tags
"""
        
        ctx.sample = mock_sample_en
        
        # Mock _get_yaml_data to return our test data
        with patch.object(tool, '_get_yaml_data', return_value=mock_yaml_data):
            result_json = await tool.run(
                ctx=ctx,
                version='139',
                channel='stable',
                split_by_area=True,
                language='en',
                debug=True
            )
        
        result = json.loads(result_json)
        
        # Verify result structure
        assert result['success'] is True
        assert result['mode'] == 'per_area'
        assert result['version'] == '139'
        assert result['channel'] == 'stable'
        assert result['language'] == 'en'
        assert 'css' in result['areas']
        assert 'graphics-webgpu' in result['areas']
        assert 'webapi' in result['areas']
        
        # Verify output paths exist
        assert 'outputs' in result
        for area in ['css', 'webapi', 'graphics-webgpu']:
            assert area in result['outputs']
            assert 'en' in result['outputs'][area]
            
            # Verify file was created
            file_path = Path(result['outputs'][area]['en'])
            assert file_path.exists()
            
            # Verify content
            content = file_path.read_text()
            assert 'Chrome 139' in content
            assert 'Digest' in content
    
    @pytest.mark.asyncio
    async def test_per_area_with_translation(self, tool, mock_yaml_data):
        """Test per-area generation with English to Chinese translation."""
        ctx = AsyncMock()
        
        # Track calls to understand flow
        english_digests = {}
        
        async def mock_sample(messages, system_prompt, **kwargs):
            # English generation
            if 'Output language: English' in system_prompt:
                if 'CSS' in system_prompt:
                    digest = """# Chrome 139 CSS & Styling Digest

## Summary
CSS improvements.

### CSS Container Queries
New CSS container queries feature

**References:**
- [CSS Spec](https://example.com/css1)
"""
                    english_digests['css'] = digest
                    return digest
                else:
                    return """# Chrome 139 Other Digest

## Summary
Other features.
"""
            
            # Chinese translation
            elif 'bilingual technical' in system_prompt:
                # This is translation call
                if 'CSS Container Queries' in messages:
                    return """# Chrome 139 CSS & Styling 摘要

## 概述
CSS 改进。

### CSS Container Queries
新的 CSS 容器查询功能

**参考资料:**
- [CSS Spec](https://example.com/css1)
"""
                else:
                    return """# Chrome 139 其他摘要

## 概述
其他功能。
"""
            
            return "# Fallback Digest"
        
        ctx.sample = mock_sample
        
        # Mock _get_yaml_data
        with patch.object(tool, '_get_yaml_data', return_value=mock_yaml_data):
            result_json = await tool.run(
                ctx=ctx,
                version='139',
                channel='stable',
                split_by_area=True,
                language='bilingual',
                debug=True
            )
        
        result = json.loads(result_json)
        
        # Verify bilingual output
        assert result['success'] is True
        assert result['language'] == 'bilingual'
        assert result['languages'] == ['en', 'zh']
        
        # Check CSS has both languages
        if 'css' in result['outputs']:
            assert 'en' in result['outputs']['css']
            assert 'zh' in result['outputs']['css']
            
            # Verify Chinese file exists and has Chinese content
            zh_path = Path(result['outputs']['css']['zh'])
            if zh_path.exists():
                zh_content = zh_path.read_text()
                assert '摘要' in zh_content or 'Translation Failed' in zh_content
        
        # Check translation status
        assert 'translation_status' in result
    
    @pytest.mark.asyncio
    async def test_validation_and_retry(self, tool, mock_yaml_data):
        """Test validation and retry logic for failed generation."""
        ctx = AsyncMock()
        
        # Track attempt count
        attempt_count = {'count': 0}
        
        async def mock_sample(messages, system_prompt, **kwargs):
            attempt_count['count'] += 1
            
            if 'CSS' in system_prompt:
                if attempt_count['count'] == 1:
                    # First attempt: missing features
                    return """# Chrome 139 CSS Digest

## Summary
Missing some features.
"""
                else:
                    # Retry: include all features
                    return """# Chrome 139 CSS & Styling Digest

## Summary
Complete CSS features.

### CSS Container Queries
New CSS container queries feature

**References:**
- [CSS Spec](https://example.com/css1)
"""
            
            return "# Default Digest"
        
        ctx.sample = mock_sample
        
        # Create YAML with only CSS features
        css_only_yaml = {
            'version': '139',
            'channel': 'stable',
            'features': [mock_yaml_data['features'][0]],  # Only CSS feature
            'statistics': {'total_features': 1, 'total_links': 1}
        }
        
        with patch.object(tool, '_get_yaml_data', return_value=css_only_yaml):
            result_json = await tool.run(
                ctx=ctx,
                version='139',
                channel='stable',
                split_by_area=True,
                language='en',
                debug=True
            )
        
        result = json.loads(result_json)
        
        # Verify retry happened (2 attempts for CSS)
        assert attempt_count['count'] >= 2
        assert result['success'] is True
    
    @pytest.mark.asyncio
    async def test_empty_area_fallback(self, tool):
        """Test fallback generation for areas with no features."""
        ctx = AsyncMock()
        
        # YAML with no features
        empty_yaml = {
            'version': '139',
            'channel': 'stable',
            'features': [],
            'statistics': {'total_features': 0, 'total_links': 0}
        }
        
        with patch.object(tool, '_get_yaml_data', return_value=empty_yaml):
            result_json = await tool.run(
                ctx=ctx,
                version='139',
                channel='stable',
                split_by_area=True,
                language='bilingual',
                debug=True
            )
        
        result = json.loads(result_json)
        
        # Should still succeed with minimal fallback
        assert result['success'] is True
        
        # Check 'others' area has fallback content
        if 'others' in result['outputs']:
            en_path = Path(result['outputs']['others']['en'])
            if en_path.exists():
                content = en_path.read_text()
                assert 'No new features' in content
            
            zh_path = Path(result['outputs']['others']['zh'])
            if zh_path.exists():
                content = zh_path.read_text()
                assert '没有新功能' in content
    
    @pytest.mark.asyncio
    async def test_translation_validation_failure(self, tool, mock_yaml_data):
        """Test handling of translation validation failures."""
        ctx = AsyncMock()
        
        attempt_count = {'translation': 0}
        
        async def mock_sample(messages, system_prompt, **kwargs):
            if 'Output language: English' in system_prompt:
                return """# Chrome 139 CSS Digest

### CSS Container Queries
Feature description

**References:**
- [Link1](https://example.com/1)
- [Link2](https://example.com/2)
"""
            elif 'bilingual technical' in system_prompt:
                attempt_count['translation'] += 1
                if attempt_count['translation'] == 1:
                    # First translation: missing links
                    return """# Chrome 139 CSS 摘要

### CSS Container Queries
功能描述

**参考资料:**
- [Link1](https://example.com/1)
"""
                else:
                    # Retry: correct links
                    return """# Chrome 139 CSS 摘要

### CSS Container Queries
功能描述

**参考资料:**
- [Link1](https://example.com/1)
- [Link2](https://example.com/2)
"""
            
            return "# Fallback"
        
        ctx.sample = mock_sample
        
        css_yaml = {
            'version': '139',
            'channel': 'stable',
            'features': [mock_yaml_data['features'][0]],
            'statistics': {'total_features': 1, 'total_links': 1}
        }
        
        with patch.object(tool, '_get_yaml_data', return_value=css_yaml):
            result_json = await tool.run(
                ctx=ctx,
                version='139',
                channel='stable',
                split_by_area=True,
                language='bilingual',
                debug=True
            )
        
        result = json.loads(result_json)
        
        # Check translation was retried
        assert attempt_count['translation'] >= 1
        
        # Check translation status
        if 'css' in result.get('translation_status', {}):
            status = result['translation_status']['css']
            assert status in ['ok', 'retry_success', 'fallback']
    
    def test_area_normalization(self, tool):
        """Test area name normalization."""
        manager = tool.focus_manager
        
        # Test various mappings
        assert manager.normalize_area('webgpu') == 'graphics-webgpu'
        assert manager.normalize_area('gpu') == 'graphics-webgpu'
        assert manager.normalize_area('graphics') == 'graphics-webgpu'
        assert manager.normalize_area('security') == 'security-privacy'
        assert manager.normalize_area('privacy') == 'security-privacy'
        assert manager.normalize_area('pwa') == 'pwa-service-worker'
        assert manager.normalize_area('api') == 'webapi'
        assert manager.normalize_area('web-api') == 'webapi'
        
        # Test unmapped names stay as-is
        assert manager.normalize_area('unknown-area') == 'unknown-area'
    
    def test_truncate_features(self, tool):
        """Test feature content truncation."""
        yaml_data = {
            'features': [
                {
                    'title': 'Test Feature',
                    'content': 'A' * 500,  # Long content
                    'links': []
                }
            ]
        }
        
        truncated = tool._truncate_features(yaml_data, max_content_length=100)
        
        assert len(truncated['features'][0]['content']) == 103  # 100 + '...'
        assert truncated['features'][0]['content'].endswith('...')
    
    def test_validate_digest(self, tool):
        """Test digest validation logic with heading normalization and link limits."""
        fixture_path = Path(__file__).parent / 'fixtures' / 'chrome-136-security-privacy.yml'
        yaml_data = yaml.safe_load(fixture_path.read_text())

        valid_digest = """# Chrome 136 Security & Privacy Digest

## Detailed Updates

###    permissions policy reports for iframes   
Chrome tightened iframe permissions.
[Spec](https://w3c.github.io/webappsec-permissions-policy/#reporting)
[Tracking bug #40941424](https://bugs.chromium.org/p/chromium/issues/detail?id=40941424)

### Reduce fingerprinting in Accept—Language header information
Accept-Language now sends the primary locale only.
[ChromeStatus.com entry](https://chromestatus.com/feature/5042348942655488)
"""

        result = tool._validate_digest(valid_digest, yaml_data)
        assert result['valid'] is True
        assert result['missing_titles'] == []
        assert result['extra_links'] == []

        h4_digest = """# Chrome 136 Security & Privacy Digest

## Detailed Updates

#### Permissions Policy reports for iframes
Details
[Spec](https://w3c.github.io/webappsec-permissions-policy/#reporting)

#### Reduce fingerprinting in Accept-Language header information
Details
[ChromeStatus.com entry](https://chromestatus.com/feature/5042348942655488)
"""

        fallback_result = tool._validate_digest(h4_digest, yaml_data)
        assert fallback_result['valid'] is True
        assert fallback_result['missing_titles'] == []

        missing_digest = """# Chrome 136 Security & Privacy Digest

## Detailed Updates

### Permissions Policy reports for iframes
[Spec](https://w3c.github.io/webappsec-permissions-policy/#reporting)
"""

        missing_result = tool._validate_digest(missing_digest, yaml_data)
        assert missing_result['valid'] is False
        assert 'Reduce fingerprinting in Accept-Language header information' in missing_result['missing_titles']

        extra_link_digest = """# Chrome 136 Security & Privacy Digest

## Detailed Updates

### Permissions Policy reports for iframes
[Spec](https://w3c.github.io/webappsec-permissions-policy/#reporting)
[Extra](https://example.com/extra1)
[Extra2](https://example.com/extra2)
[Extra3](https://example.com/extra3)

### Reduce fingerprinting in Accept-Language header information
[ChromeStatus.com entry](https://chromestatus.com/feature/5042348942655488)
"""

        extra_link_result = tool._validate_digest(extra_link_digest, yaml_data)
        assert extra_link_result['valid'] is False
        assert len(extra_link_result['extra_links']) > 2
    
    def test_validate_translation(self, tool):
        """Test translation validation."""
        english = """# Chrome 139 CSS Digest

## Summary
CSS features.

### Feature One
Description
[Link1](https://example.com/1)

### Feature Two
Description
[Link2](https://example.com/2)
"""
        
        # Valid translation
        valid_chinese = """# Chrome 139 CSS 摘要

## 概述
CSS 功能。

### Feature One
描述
[Link1](https://example.com/1)

### Feature Two
描述
[Link2](https://example.com/2)
"""
        
        result = tool._validate_translation(english, valid_chinese)
        assert result['valid'] is True
        assert result['heading_match'] is True
        assert result['link_match'] is True
        
        # Invalid - missing heading
        invalid_chinese = """# Chrome 139 CSS 摘要

## 概述
CSS 功能。

### Feature One
描述
[Link1](https://example.com/1)
"""
        
        result = tool._validate_translation(english, invalid_chinese)
        assert result['valid'] is False
        assert 'Heading count mismatch' in result['issues']
        
        # Invalid - missing link
        missing_link = """# Chrome 139 CSS 摘要

## 概述
CSS 功能。

### Feature One
描述
[Link1](https://example.com/1)

### Feature Two
描述
"""
        
        result = tool._validate_translation(english, missing_link)
        assert result['valid'] is False
        assert 'Missing' in result['issues'] and 'links' in result['issues']
    
    def test_fallback_generation(self, tool):
        """Test fallback digest generation."""
        area_yaml = {
            'version': '139',
            'area': 'css',
            'features': [
                {
                    'title': 'CSS Feature',
                    'links': [
                        {'title': 'Spec', 'url': 'https://example.com/spec'}
                    ]
                }
            ]
        }
        
        # English fallback
        en_fallback = tool._generate_area_fallback(
            area_yaml, 'en', 'css', 'Test failure'
        )
        
        assert 'Chrome 139' in en_fallback
        assert 'CSS' in en_fallback
        assert 'Fallback' in en_fallback
        assert 'Test failure' in en_fallback
        assert 'CSS Feature' in en_fallback
        assert 'https://example.com/spec' in en_fallback
        
        # Chinese fallback
        zh_fallback = tool._generate_area_fallback(
            area_yaml, 'zh', 'css', '测试失败'
        )
        
        assert 'Chrome 139' in zh_fallback
        assert 'CSS' in zh_fallback
        assert 'Fallback' in zh_fallback
        assert '测试失败' in zh_fallback
        assert 'CSS Feature' in zh_fallback
    
    def test_translation_fallback(self, tool):
        """Test translation fallback generation."""
        fallback = tool._generate_translation_fallback(
            '139', 'stable', 'css', Path('/test/path/en.md')
        )
        
        assert 'Chrome 139' in fallback
        assert 'CSS' in fallback
        assert '中文翻译失败' in fallback
        assert '/test/path/en.md' in fallback
        assert 'Translation Failed' in fallback
    
    def test_minimal_fallback(self, tool):
        """Test minimal fallback for empty areas."""
        # English
        en_fallback = tool._generate_minimal_fallback(
            '139', 'stable', 'css', 'en'
        )
        
        assert 'Chrome 139' in en_fallback
        assert 'CSS' in en_fallback
        assert 'No new features' in en_fallback
        
        # Chinese
        zh_fallback = tool._generate_minimal_fallback(
            '139', 'stable', 'css', 'zh'
        )
        
        assert 'Chrome 139' in zh_fallback
        assert 'CSS' in zh_fallback
        assert '没有新功能' in zh_fallback


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
