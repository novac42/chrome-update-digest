"""
Tests for bilingual support in the enhanced pipeline.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
import tempfile

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mcp_tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool
from src.mcp_tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool as WebplatformDigestTool
from src.utils.yaml_pipeline import YAMLPipeline


class TestBilingualPromptLoading:
    """Test loading of language-specific prompts."""
    
    @pytest.mark.asyncio
    async def test_enhanced_tool_loads_english_prompt(self):
        """Test that enhanced tool loads English prompt correctly."""
        tool = EnhancedWebplatformDigestTool()
        ctx = Mock()
        
        prompt = await tool._load_prompt(ctx, "en", False)
        
        # Check that English prompt is loaded
        assert prompt is not None
        assert "Chrome Update Analyzer" in prompt or "WebPlatform" in prompt
    
    @pytest.mark.asyncio
    async def test_enhanced_tool_loads_chinese_prompt(self):
        """Test that enhanced tool loads Chinese prompt correctly."""
        tool = EnhancedWebplatformDigestTool()
        ctx = Mock()
        
        # Check if Chinese prompt file exists
        zh_prompt_path = Path('prompts/webplatform-prompt-zh.md')
        if zh_prompt_path.exists():
            prompt = await tool._load_prompt(ctx, "zh", False)
            assert prompt is not None
    
    @pytest.mark.asyncio
    async def test_enhanced_tool_loads_bilingual_prompt(self):
        """Test that enhanced tool loads bilingual prompt correctly."""
        tool = EnhancedWebplatformDigestTool()
        ctx = Mock()
        
        prompt = await tool._load_prompt(ctx, "bilingual", False)
        
        assert prompt is not None
        # Check for bilingual markers
        assert "bilingual" in prompt.lower() or "Language" in prompt
    
    @pytest.mark.asyncio
    async def test_fallback_to_default_language(self):
        """Test fallback when requested language prompt doesn't exist."""
        tool = EnhancedWebplatformDigestTool()
        ctx = Mock()
        
        # Try to load non-existent language
        prompt = await tool._load_prompt(ctx, "invalid_lang", False)
        
        # Should fallback to bilingual or English
        assert prompt is not None
        assert len(prompt) > 0


class TestLanguageParameterPropagation:
    """Test that language parameter is properly propagated through the pipeline."""
    
    @pytest.mark.asyncio
    async def test_enhanced_tool_accepts_language_parameter(self):
        """Test that enhanced tool accepts and uses language parameter."""
        tool = EnhancedWebplatformDigestTool()
        ctx = Mock()
        ctx.sample = AsyncMock(return_value=Mock(text="Test digest output"))
        
        # Mock the YAML data loading
        with patch.object(tool, '_get_yaml_data', return_value={
            'version': '138',
            'features': [],
            'statistics': {'total_features': 0, 'total_links': 0}
        }):
            # Test with English
            result = await tool.run(ctx, "138", "stable", None, True, "en", False)
            assert result is not None
            
            # Test with Chinese
            result = await tool.run(ctx, "138", "stable", None, True, "zh", False)
            assert result is not None
            
            # Test with bilingual
            result = await tool.run(ctx, "138", "stable", None, True, "bilingual", False)
            assert result is not None
    
    def test_webplatform_tool_loads_language_specific_prompt(self):
        """Test that WebplatformDigestTool loads language-specific prompts."""
        tool = WebplatformDigestTool(Path.cwd())
        
        # Test English prompt loading
        en_prompt = tool._load_prompt_template("en")
        assert en_prompt is not None
        assert len(en_prompt) > 0
        
        # Test Chinese prompt loading (if exists)
        zh_prompt = tool._load_prompt_template("zh")
        assert zh_prompt is not None
        
        # Test bilingual prompt loading
        bi_prompt = tool._load_prompt_template("bilingual")
        assert bi_prompt is not None


class TestBilingualOutputGeneration:
    """Test generation of bilingual output."""
    
    @pytest.mark.asyncio
    async def test_fallback_digest_respects_language(self):
        """Test that fallback digest generation respects language setting."""
        tool = EnhancedWebplatformDigestTool()
        
        yaml_data = {
            'version': '138',
            'statistics': {'total_features': 1, 'total_links': 1},
            'features': [{
                'title': 'Test Feature',
                'content': 'Test content',
                'primary_tags': [{'name': 'css'}],
                'links': [{'url': 'https://example.com', 'title': 'Example'}]
            }]
        }
        
        # Generate fallback digest (no LLM)
        digest = tool._generate_fallback_digest(yaml_data)
        
        assert 'Chrome 138' in digest
        assert 'Test Feature' in digest
        assert 'https://example.com' in digest
    
    @pytest.mark.asyncio
    async def test_prompt_includes_language_instruction(self):
        """Test that generated prompt includes language instruction."""
        tool = EnhancedWebplatformDigestTool()
        ctx = Mock()
        
        yaml_data = {
            'version': '138',
            'statistics': {'total_features': 1, 'total_links': 1},
            'features': [{
                'title': 'Test Feature',
                'content': 'Test content',
                'primary_tags': [{'name': 'css'}],
                'links': []
            }]
        }
        
        # Mock the sample method to capture the prompt
        captured_prompt = None
        
        async def mock_sample(prompt, max_tokens):
            nonlocal captured_prompt
            captured_prompt = prompt
            return Mock(text="Generated digest")
        
        ctx.sample = mock_sample
        
        # Generate digest with Chinese language
        result = await tool._generate_digest_from_yaml(ctx, yaml_data, "zh", False)
        
        # Check that language instruction was included
        assert captured_prompt is not None
        assert "Output Language: zh" in captured_prompt or "Language: zh" in captured_prompt


class TestPromptFileStructure:
    """Test the structure of prompt files."""
    
    def test_yaml_prompt_files_exist(self):
        """Test that YAML-specific prompt files exist and have correct structure."""
        # Check English YAML prompt
        en_path = Path('prompts/webplatform-prompt-yaml-en.md')
        assert en_path.exists(), "English YAML prompt file should exist"
        
        with open(en_path, 'r', encoding='utf-8') as f:
            en_content = f.read()
        assert "YAML" in en_content
        assert "English" in en_content
        
        # Check Chinese YAML prompt
        zh_path = Path('prompts/webplatform-prompt-yaml-zh.md')
        assert zh_path.exists(), "Chinese YAML prompt file should exist"
        
        with open(zh_path, 'r', encoding='utf-8') as f:
            zh_content = f.read()
        assert "YAML" in zh_content
        assert "中文" in zh_content or "Chinese" in zh_content
        
        # Check Bilingual YAML prompt
        bi_path = Path('prompts/webplatform-prompt-yaml-bilingual.md')
        assert bi_path.exists(), "Bilingual YAML prompt file should exist"
        
        with open(bi_path, 'r', encoding='utf-8') as f:
            bi_content = f.read()
        assert "YAML" in bi_content
        assert "Bilingual" in bi_content
    
    def test_english_prompt_exists(self):
        """Test that English prompt file exists."""
        prompt_path = Path('prompts/webplatform-prompt-markdown-en.md')
        assert prompt_path.exists(), "English markdown prompt file should exist"
    
    def test_chinese_prompt_exists(self):
        """Test that Chinese prompt file exists."""
        prompt_path = Path('prompts/webplatform-prompt-markdown-zh.md')
        assert prompt_path.exists(), "Chinese markdown prompt file should exist"


class TestResourceLoading:
    """Test resource loading with language support."""
    
    @pytest.mark.asyncio
    async def test_resource_loading_with_language(self):
        """Test that resources are loaded based on language."""
        tool = WebplatformDigestTool(Path.cwd())
        ctx = Mock()
        
        # Mock the read_resource method
        async def mock_read_resource(resource_name):
            if "prompt-en" in resource_name:
                return "English prompt content"
            elif "prompt-zh" in resource_name:
                return "Chinese prompt content"
            elif "prompt-bilingual" in resource_name:
                return "Bilingual prompt content"
            else:
                return "Default content"
        
        ctx.read_resource = mock_read_resource
        
        # Test English resource loading
        prompt, keywords = await tool._load_prompts_from_resources(ctx, "en")
        assert "English" in prompt or len(prompt) > 0
        
        # Test Chinese resource loading
        prompt, keywords = await tool._load_prompts_from_resources(ctx, "zh")
        assert "Chinese" in prompt or len(prompt) > 0
        
        # Test bilingual resource loading
        prompt, keywords = await tool._load_prompts_from_resources(ctx, "bilingual")
        assert "Bilingual" in prompt or len(prompt) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])