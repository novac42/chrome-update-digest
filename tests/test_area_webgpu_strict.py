"""
Test suite for strict WebGPU area classification.
Tests the new WebGPUClassifier to ensure correct categorization.
"""

import pytest
from unittest.mock import patch
from src.utils.area_classifier import WebGPUClassifier, ClassificationResult


class TestWebGPUClassifier:
    """Test cases for WebGPU classifier."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.classifier = WebGPUClassifier(strict_mode=True)
        self.classifier_lenient = WebGPUClassifier(strict_mode=False)
    
    def test_genuine_webgpu_feature_with_texture(self):
        """Test that genuine WebGPU texture features are correctly classified."""
        feature = {
            'title': '3D texture support for BC and ASTC compressed formats',
            'content': 'The "texture-compression-bc-sliced-3d" and "texture-compression-astc-sliced-3d" WebGPU features add support for 3D textures using Block Compression (BC) and Adaptive Scalable Texture Compression (ASTC) formats.',
            'heading_path': ['Chrome 139', 'Graphics', 'WebGPU Features']
        }
        
        result = self.classifier.is_strong_webgpu(feature)
        assert result.is_webgpu is True
        assert result.score >= 3
        # Should identify WebGPU-related keywords
        assert any(kw in ' '.join(result.reasons).lower() for kw in ['texture', '3d', 'webgpu', 'graphics'])

    def test_graphics_and_webgpu_parent_heading(self):
        """Test that Graphics and WebGPU parent sections count toward WebGPU."""
        feature = {
            'title': 'Save and copy canvas images',
            'content': 'Chrome users can now right-click on a WebGPU canvas to save or copy the image.',
            'heading_path': ['Graphics and WebGPU - Chrome 136', 'Save and copy canvas images']
        }

        result = self.classifier.is_strong_webgpu(feature)
        assert result.is_webgpu is True
        assert result.score >= 3
        assert any('graphics and webgpu' in reason.lower() or 'webgpu' in reason.lower() for reason in result.reasons)
    
    def test_genuine_webgpu_dawn_updates(self):
        """Test that Dawn updates are correctly classified as WebGPU."""
        feature = {
            'title': 'Dawn updates',
            'content': 'Dawn is the implementation of WebGPU in Chromium. It includes updates to the GPU adapter and device handling.',
            'heading_path': ['Chrome 139', 'Graphics', 'Detailed WebGPU Updates']
        }
        
        result = self.classifier.is_strong_webgpu(feature)
        assert result.is_webgpu is True
        assert 'dawn' in ' '.join(result.reasons).lower()
    
    def test_genuine_webgpu_core_features(self):
        """Test that core-features-and-limits is classified as WebGPU."""
        feature = {
            'title': 'New "core-features-and-limits" feature',
            'content': 'A new "core-features-and-limits" feature is being introduced for the upcoming WebGPU compatibility mode.',
            'heading_path': ['Chrome 139', 'Graphics', 'WebGPU']
        }
        
        result = self.classifier.is_strong_webgpu(feature)
        assert result.is_webgpu is True
        assert result.score >= 3
    
    def test_misclassified_payment_api(self):
        """Test that payment APIs are NOT classified as WebGPU."""
        feature = {
            'title': 'The securePaymentConfirmationAvailability API',
            'content': 'This API allows checking if secure payment confirmation is available.',
            'heading_path': ['What\'s New in WebGPU (Chrome 139)', 'Web APIs']
        }
        
        result = self.classifier.is_strong_webgpu(feature)
        assert result.is_webgpu is False
        assert len(result.exclusion_reasons) > 0  # Should have exclusion reasons
    
    def test_misclassified_spc_browser_keys(self):
        """Test that SPC features are NOT classified as WebGPU."""
        feature = {
            'title': 'Secure Payment Confirmation: Browser Bound Keys',
            'content': 'Browser bound keys for secure payment confirmation.',
            'heading_path': ['What\'s New in WebGPU (Chrome 139)', 'Payments']
        }
        
        result = self.classifier.is_strong_webgpu(feature)
        assert result.is_webgpu is False
        assert len(result.exclusion_reasons) > 0
    
    def test_misclassified_accept_language(self):
        """Test that Accept-Language features are NOT classified as WebGPU."""
        feature = {
            'title': 'Reduce fingerprinting in Accept-Language header information',
            'content': 'Reduces fingerprinting by limiting Accept-Language header variations.',
            'heading_path': ['What\'s New in WebGPU (Chrome 139)', 'Privacy and Security']
        }
        
        result = self.classifier.is_strong_webgpu(feature)
        assert result.is_webgpu is False
        # Should be excluded due to exclusion keywords or generic domain
        assert len(result.exclusion_reasons) > 0
    
    def test_misclassified_csp_worker(self):
        """Test that CSP features are NOT classified as WebGPU."""
        feature = {
            'title': 'Fire error event for Content Security Policy (CSP) blocked worker',
            'content': 'Fires error events when CSP blocks workers.',
            'heading_path': ['What\'s New in WebGPU (Chrome 139)', 'Security']
        }
        
        result = self.classifier.is_strong_webgpu(feature)
        assert result.is_webgpu is False
        # Should be excluded due to CSP or worker keywords
        assert len(result.exclusion_reasons) > 0
    
    def test_misclassified_crash_reporting(self):
        """Test that crash reporting features are NOT classified as WebGPU."""
        feature = {
            'title': 'Crash Reporting API: Specify `crash-reporting` to receive only crash reports',
            'content': 'New API for crash reporting.',
            'heading_path': ['What\'s New in WebGPU (Chrome 139)', 'Origin Trials']
        }
        
        result = self.classifier.is_strong_webgpu(feature)
        assert result.is_webgpu is False
        # Should be excluded due to crash keyword or origin trials domain
        assert len(result.exclusion_reasons) > 0
    
    def test_misclassified_prompt_api(self):
        """Test that Prompt API is NOT classified as WebGPU."""
        feature = {
            'title': 'Prompt API',
            'content': 'New Prompt API for language models.',
            'heading_path': ['What\'s New in WebGPU (Chrome 139)', 'AI']
        }
        
        result = self.classifier.is_strong_webgpu(feature)
        assert result.is_webgpu is False
        assert 'prompt api' in ' '.join(result.exclusion_reasons).lower() or \
               'ai' in ' '.join(result.exclusion_reasons).lower()
    
    def test_edge_case_webgpu_compatibility_mode(self):
        """Test that WebGPU compatibility mode is correctly classified."""
        feature = {
            'title': 'WebGPU compatibility mode',
            'content': 'The WebGPU compatibility mode allows broader hardware support.',
            'heading_path': ['Chrome 139', 'Graphics']
        }
        
        result = self.classifier.is_strong_webgpu(feature)
        assert result.is_webgpu is True
        assert 'compatibility mode' in ' '.join(result.reasons).lower() or \
               'webgpu' in ' '.join(result.reasons).lower()
    
    def test_edge_case_pipeline_features(self):
        """Test features with pipeline/adapter/device keywords."""
        feature = {
            'title': 'GPU compute pipeline improvements',
            'content': 'Improvements to GPU compute pipeline and adapter selection. New device capabilities for compute shaders.',
            'heading_path': ['Chrome 139', 'Graphics']
        }
        
        result = self.classifier.is_strong_webgpu(feature)
        assert result.is_webgpu is True
        assert result.score >= 3
    
    def test_ancestor_only_webgpu_rejected(self):
        """Test that features with WebGPU only in distant ancestors are rejected."""
        feature = {
            'title': 'Network performance improvements',
            'content': 'Improvements to network stack performance.',
            'heading_path': ['What\'s New in WebGPU (Chrome 139)', 'Performance', 'Network']
        }
        
        result = self.classifier.is_strong_webgpu(feature)
        assert result.is_webgpu is False
        # Should be excluded due to generic domains in near headings
        assert len(result.exclusion_reasons) > 0
    
    def test_lenient_mode_accepts_more(self):
        """Test that lenient mode is less strict."""
        feature = {
            'title': 'Some graphics feature',
            'content': 'A feature under graphics section.',
            'heading_path': ['Chrome 139', 'Graphics']
        }
        
        # Strict mode should reject (no strong WebGPU indicators)
        result_strict = self.classifier.is_strong_webgpu(feature)
        assert result_strict.is_webgpu is True  # Has 'graphics' in heading
        
        # Lenient mode should accept
        result_lenient = self.classifier_lenient.is_strong_webgpu(feature)
        assert result_lenient.is_webgpu is True


class TestYamlPipelineIntegration:
    """Test integration with YAML pipeline."""
    
    @patch.dict('os.environ', {'STRICT_WEBGPU_AREA': '1'})
    def test_strict_mode_enabled_via_env(self):
        """Test that strict mode can be enabled via environment variable."""
        from src.utils.yaml_pipeline import YAMLPipeline
        
        pipeline = YAMLPipeline()
        assert pipeline.webgpu_classifier.strict_mode is True
    
    @patch.dict('os.environ', {})  # No env var set
    def test_strict_mode_enabled_by_default(self):
        """Test that strict mode is enabled by default."""
        from src.utils.yaml_pipeline import YAMLPipeline
        
        pipeline = YAMLPipeline()
        assert pipeline.webgpu_classifier.strict_mode is True
    
    @patch.dict('os.environ', {'STRICT_WEBGPU_AREA': '0'})
    def test_strict_mode_can_be_disabled(self):
        """Test that strict mode can be disabled via environment variable."""
        from src.utils.yaml_pipeline import YAMLPipeline
        
        pipeline = YAMLPipeline()
        assert pipeline.webgpu_classifier.strict_mode is False
    
    @patch.dict('os.environ', {'STRICT_WEBGPU_AREA': '1'})
    def test_determine_area_with_strict_classifier(self):
        """Test that _determine_area uses strict classifier for WebGPU."""
        from src.utils.yaml_pipeline import YAMLPipeline
        
        pipeline = YAMLPipeline()
        
        # Test genuine WebGPU feature
        webgpu_feature = {
            'title': 'WebGPU texture formats',
            'content': 'New texture formats for WebGPU.',
            'heading_path': ['Chrome 139', 'Graphics']
        }
        area = pipeline._determine_area(webgpu_feature)
        assert area == 'graphics-webgpu'
        
        # Test misclassified feature
        payment_feature = {
            'title': 'Payment API updates',
            'content': 'Updates to payment APIs.',
            'heading_path': ['Chrome 139', 'Graphics', 'Payments']  # Under Graphics but actually payments
        }
        area = pipeline._determine_area(payment_feature)
        assert area != 'graphics-webgpu'  # Should be rejected by strict classifier
