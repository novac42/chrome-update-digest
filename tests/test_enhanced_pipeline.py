"""
Comprehensive tests for the enhanced pipeline components.
Tests FocusAreaManager, YAMLPipeline, and EnhancedWebplatformDigestTool.
"""

import pytest
import yaml
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import tempfile

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.focus_area_manager import FocusAreaManager, FocusAreaConfig, MatchingConfig
from src.utils.yaml_pipeline import YAMLPipeline, PipelineStatistics
from src.utils.link_extractor import LinkExtractor, ExtractedFeature, ExtractedLink
from src.models.feature_tagging import HeadingBasedTagger, TaggedFeature, FeatureTag, TagPriority
from src.mcp_tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool


class TestFocusAreaManager:
    """Test the FocusAreaManager class."""
    
    def test_init_with_default_config(self):
        """Test initialization with default configuration."""
        manager = FocusAreaManager()
        
        # Check default focus areas exist
        assert 'ai' in manager.focus_areas
        assert 'webgpu' in manager.focus_areas
        assert 'security' in manager.focus_areas
        
        # Check AI focus area configuration
        ai_config = manager.focus_areas['ai']
        assert ai_config.name == "AI & Machine Learning"
        assert 'ai' in ai_config.keywords['primary']
        assert 'translator api' in ai_config.keywords['secondary']
    
    def test_filter_features_by_ai(self):
        """Test filtering features by AI focus area."""
        manager = FocusAreaManager()
        
        features = [
            {
                'title': 'Translator API Released',
                'content': 'New translation API for language processing',
                'primary_tags': [{'name': 'webapi'}]
            },
            {
                'title': 'CSS Grid Improvements',
                'content': 'Better grid layout support',
                'primary_tags': [{'name': 'css'}]
            },
            {
                'title': 'AI Language Model Support',
                'content': 'Built-in LLM capabilities',
                'primary_tags': [{'name': 'webapi'}]
            }
        ]
        
        filtered = manager.filter_features(features, ['ai'])
        
        # Should match AI-related features
        assert len(filtered) == 2
        assert filtered[0]['title'] == 'AI Language Model Support'  # Higher score
        assert filtered[1]['title'] == 'Translator API Released'
    
    def test_filter_features_multiple_areas(self):
        """Test filtering with multiple focus areas."""
        manager = FocusAreaManager()
        
        features = [
            {
                'title': 'WebGPU Compute Shaders',
                'content': 'New compute shader support in WebGPU',
                'primary_tags': [{'name': 'webgpu'}]
            },
            {
                'title': 'Security Headers Update',
                'content': 'Enhanced CSP and CORS support',
                'primary_tags': [{'name': 'security'}]
            },
            {
                'title': 'DOM API Updates',
                'content': 'Minor DOM improvements',
                'primary_tags': [{'name': 'webapi'}]
            }
        ]
        
        filtered = manager.filter_features(features, ['webgpu', 'security'])
        
        assert len(filtered) == 2
        titles = [f['title'] for f in filtered]
        assert 'WebGPU Compute Shaders' in titles
        assert 'Security Headers Update' in titles
        assert 'DOM API Updates' not in titles
    
    def test_keyword_matching_case_insensitive(self):
        """Test case-insensitive keyword matching."""
        manager = FocusAreaManager()
        
        features = [
            {
                'title': 'AI Feature',
                'content': 'Some AI content'
            },
            {
                'title': 'ai feature',
                'content': 'lowercase ai content'
            },
            {
                'title': 'Ai Feature',
                'content': 'Mixed case Ai content'
            }
        ]
        
        filtered = manager.filter_features(features, ['ai'])
        
        # All should match regardless of case
        assert len(filtered) == 3
    
    def test_scoring_weights(self):
        """Test that scoring weights work correctly."""
        manager = FocusAreaManager()
        
        features = [
            {
                'title': 'Primary keyword: ai',
                'content': 'Direct AI mention'
            },
            {
                'title': 'Secondary keyword',
                'content': 'translator api feature'
            },
            {
                'title': 'Related keyword',
                'content': 'model inference'
            }
        ]
        
        filtered = manager.filter_features(features, ['ai'], min_score=0.0)
        
        # All should be included but with different scores
        assert len(filtered) == 3
        # Primary keyword should have highest score
        assert filtered[0]['_match_score'] > filtered[1]['_match_score']
        assert filtered[1]['_match_score'] > filtered[2]['_match_score']


class TestYAMLPipeline:
    """Test the YAML Pipeline class."""
    
    def test_process_release_notes(self):
        """Test processing release notes through pipeline."""
        pipeline = YAMLPipeline()
        
        markdown_content = """
# Chrome 138 Release Notes

## Web APIs

### Translator API
New API for language translation.

**References:**
- [MDN Docs](https://developer.mozilla.org/docs/Web/API/Translator)
- [Chrome Status](https://chromestatus.com/feature/123456)
"""
        
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline.output_dir = Path(tmpdir)
            
            result = pipeline.process_release_notes(
                markdown_content=markdown_content,
                version="138",
                channel="stable",
                save_yaml=True
            )
            
            # Check result structure
            assert result['version'] == "138"
            assert result['channel'] == "stable"
            assert 'features' in result
            assert 'statistics' in result
            
            # Check YAML file was created
            yaml_file = Path(tmpdir) / "chrome-138-stable-tagged.yml"
            assert yaml_file.exists()
    
    def test_filter_by_focus_areas(self):
        """Test filtering YAML data by focus areas."""
        pipeline = YAMLPipeline()
        
        yaml_data = {
            'version': '138',
            'features': [
                {
                    'title': 'AI Feature',
                    'content': 'AI-related content',
                    'primary_tags': [{'name': 'webapi'}]
                },
                {
                    'title': 'CSS Feature',
                    'content': 'CSS improvements',
                    'primary_tags': [{'name': 'css'}]
                }
            ],
            'statistics': {
                'total_features': 2
            }
        }
        
        filtered = pipeline.filter_by_focus_areas(yaml_data, ['ai'])
        
        assert len(filtered['features']) == 1
        assert filtered['features'][0]['title'] == 'AI Feature'
        assert 'applied_filters' in filtered
        assert filtered['applied_filters']['focus_areas'] == ['ai']
    
    def test_calculate_statistics(self):
        """Test statistics calculation."""
        pipeline = YAMLPipeline()
        
        # Create mock tagged features
        feature1 = Mock(spec=ExtractedFeature)
        feature1.links = [Mock(), Mock()]  # 2 links
        
        tagged1 = Mock(spec=TaggedFeature)
        tagged1.feature = feature1
        tagged1.primary_tags = [
            Mock(name='css'),
            Mock(name='webapi')
        ]
        tagged1.primary_tags[0].name = 'css'
        tagged1.primary_tags[1].name = 'webapi'
        tagged1.cross_cutting_concerns = ['security']
        
        stats = pipeline._calculate_statistics([tagged1])
        
        assert stats.total_features == 1
        assert stats.total_links == 2
        assert stats.primary_tags['css'] == 1
        assert stats.primary_tags['webapi'] == 1
        assert stats.cross_cutting['security'] == 1
    
    def test_yaml_save_and_load(self):
        """Test saving and loading YAML files."""
        pipeline = YAMLPipeline()
        
        data = {
            'version': '138',
            'features': [
                {
                    'title': 'Test Feature',
                    'links': [
                        {'url': 'https://example.com', 'type': 'mdn'}
                    ]
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(suffix='.yml', delete=False) as tmp:
            tmp_path = Path(tmp.name)
            
            try:
                # Save
                pipeline.save_to_yaml(data, tmp_path)
                assert tmp_path.exists()
                
                # Load
                loaded = pipeline.load_from_yaml(tmp_path)
                assert loaded['version'] == '138'
                assert len(loaded['features']) == 1
                assert loaded['features'][0]['title'] == 'Test Feature'
            finally:
                tmp_path.unlink()
    
    def test_validate_yaml_data(self):
        """Test YAML data validation."""
        pipeline = YAMLPipeline()
        
        # Valid data
        valid_data = {
            'version': '138',
            'features': [
                {'title': 'Feature', 'links': []}
            ],
            'statistics': {}
        }
        
        errors = pipeline.validate_yaml_data(valid_data)
        assert len(errors) == 0
        
        # Invalid data - missing version
        invalid_data = {
            'features': [],
            'statistics': {}
        }
        
        errors = pipeline.validate_yaml_data(invalid_data)
        assert len(errors) > 0
        assert any('version' in e for e in errors)


class TestEnhancedWebplatformDigestTool:
    """Test the Enhanced WebPlatform Digest Tool."""
    
    @pytest.mark.asyncio
    async def test_tool_initialization(self):
        """Test tool initialization."""
        tool = EnhancedWebplatformDigestTool()
        
        assert tool.yaml_pipeline is not None
        assert tool.focus_manager is not None
        assert tool.cache_dir.exists()
    
    @pytest.mark.asyncio
    async def test_generate_fallback_digest(self):
        """Test fallback digest generation without LLM."""
        tool = EnhancedWebplatformDigestTool()
        
        yaml_data = {
            'version': '138',
            'statistics': {
                'total_features': 2,
                'total_links': 4
            },
            'features': [
                {
                    'title': 'Feature 1',
                    'content': 'Content 1',
                    'primary_tags': [{'name': 'css'}],
                    'links': [
                        {'url': 'https://example.com', 'title': 'Example'}
                    ]
                },
                {
                    'title': 'Feature 2',
                    'content': 'Content 2',
                    'primary_tags': [{'name': 'webapi'}],
                    'links': []
                }
            ]
        }
        
        digest = tool._generate_fallback_digest(yaml_data)
        
        assert 'Chrome 138 WebPlatform Digest' in digest
        assert 'Feature 1' in digest
        assert 'Feature 2' in digest
        assert 'https://example.com' in digest
        assert 'css' in digest.lower()
        assert 'webapi' in digest.lower()
    
    @pytest.mark.asyncio
    async def test_format_features_for_llm(self):
        """Test formatting features for LLM processing."""
        tool = EnhancedWebplatformDigestTool()
        
        yaml_data = {
            'features': [
                {
                    'title': 'Test Feature',
                    'content': 'Feature content',
                    'primary_tags': [
                        {'name': 'css'},
                        {'name': 'ui'}
                    ],
                    'links': [
                        {
                            'url': 'https://mdn.com/feature',
                            'title': 'MDN Documentation',
                            'type': 'mdn'
                        }
                    ]
                }
            ]
        }
        
        formatted = tool._format_features_for_llm(yaml_data)
        
        assert '#### Test Feature' in formatted
        assert '**Tags:** css, ui' in formatted
        assert 'Feature content' in formatted
        assert '[MDN Documentation](https://mdn.com/feature) (mdn)' in formatted
    
    @pytest.mark.asyncio
    async def test_validate_links(self):
        """Test link validation functionality."""
        tool = EnhancedWebplatformDigestTool()
        
        # Mock the _get_yaml_data method
        mock_yaml_data = {
            'version': '138',
            'channel': 'stable',
            'features': [
                {
                    'title': 'Feature 1',
                    'links': [
                        {'url': 'https://valid.com', 'type': 'mdn'},
                        {'url': 'invalid-url', 'type': 'other'}
                    ]
                }
            ]
        }
        
        ctx = Mock()
        
        with patch.object(tool, '_get_yaml_data', return_value=mock_yaml_data):
            report = await tool.validate_links(ctx, "138", "stable")
        
        assert report['version'] == '138'
        assert report['total_features'] == 1
        assert report['total_links'] == 2
        assert report['link_types']['mdn'] == 1
        assert report['link_types']['other'] == 1
        assert len(report['invalid_links']) == 1
        assert report['invalid_links'][0]['url'] == 'invalid-url'


def test_integration_pipeline():
    """Integration test for the full pipeline."""
    # Create test markdown content
    markdown = """
# Chrome 138 Release Notes

## Web APIs

### AI Translation API
New API for AI-powered translation with language detection.

**References:**
- [MDN: Translation API](https://developer.mozilla.org/docs/Web/API/Translation)
- [Chrome Status](https://chromestatus.com/feature/translation-api)

### WebGPU Compute
Enhanced compute shader support in WebGPU.

**References:**
- [WebGPU Spec](https://gpuweb.github.io/gpuweb/)

## CSS

### CSS Grid Improvements
Better grid layout with subgrid support.

**References:**
- [MDN: CSS Grid](https://developer.mozilla.org/docs/Web/CSS/grid)
"""
    
    # Process through pipeline
    pipeline = YAMLPipeline()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        pipeline.output_dir = Path(tmpdir)
        
        # Process release notes
        result = pipeline.process_release_notes(
            markdown_content=markdown,
            version="138",
            channel="stable",
            save_yaml=True
        )
        
        # Verify extraction
        assert len(result['features']) == 3
        assert result['statistics']['total_features'] == 3
        assert result['statistics']['total_links'] == 4
        
        # Filter by AI focus area
        filtered = pipeline.filter_by_focus_areas(result, ['ai'])
        assert len(filtered['features']) == 1
        assert 'Translation API' in filtered['features'][0]['title']
        
        # Filter by WebGPU
        filtered = pipeline.filter_by_focus_areas(result, ['webgpu'])
        assert len(filtered['features']) == 1
        assert 'WebGPU' in filtered['features'][0]['title']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])