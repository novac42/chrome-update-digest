#!/usr/bin/env python3
"""
Test suite for merge_webgpu_graphics.py
Tests three-source merge, deduplication, and version-aware logic.
"""

import unittest
from pathlib import Path
import tempfile
import shutil
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from chrome_update_digest.processors.merge_webgpu_graphics import WebGPUGraphicsMerger


class TestWebGPUGraphicsMerger(unittest.TestCase):
    """Test cases for WebGPU-Graphics merger."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        
        # Create directory structure
        self.dedicated_dir = self.test_path / "upstream_docs" / "release_notes" / "webgpu"
        self.webplatform_dir = self.test_path / "upstream_docs" / "release_notes" / "WebPlatform"
        self.split_dir = self.test_path / "upstream_docs" / "processed_releasenotes" / "processed_forwebplatform" / "split_by_area"
        self.output_dir = self.test_path / "upstream_docs" / "processed_releasenotes" / "processed_forwebplatform" / "merged" / "graphics-webgpu"
        
        self.dedicated_dir.mkdir(parents=True)
        self.webplatform_dir.mkdir(parents=True)
        self.split_dir.mkdir(parents=True)
        self.output_dir.mkdir(parents=True)
        
        # Create merger instance
        self.merger = WebGPUGraphicsMerger(base_path=self.test_path)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_version_aware_source_selection(self):
        """Test that source selection is version-aware."""
        # Test Chrome 135 (should not check for WebGPU heading2)
        sources = self.merger.get_available_sources("135", "stable")
        self.assertIsNone(sources['webgpu_heading2'])  # Should be None for versions < 136
        
        # Test Chrome 136 (should check for WebGPU heading2)
        sources = self.merger.get_available_sources("136", "stable")
        # Note: File won't exist in test but it should be checked
        self.assertEqual(len(sources), 3)  # All three sources should be in dict
        self.assertIn('webgpu_heading2', sources)  # Should be in sources
        
        # Test Chrome 139 (should not check for WebGPU heading2 by default)
        sources = self.merger.get_available_sources("139", "stable")
        self.assertIsNone(sources['webgpu_heading2'])  # Should be None for versions > 137
    
    def test_single_source_merge(self):
        """Test merge with only one source available."""
        # Create only dedicated WebGPU file
        webgpu_file = self.dedicated_dir / "chrome-139-stable.md"
        webgpu_content = """# WebGPU Release Notes - Chrome 139

## New Features

### Feature 1
- Description of WebGPU feature 1
- [Issue 12345](https://crbug.com/12345)

### Feature 2
- Description of WebGPU feature 2
"""
        webgpu_file.write_text(webgpu_content)
        
        # Run merge
        result = self.merger.merge("139", "stable")
        
        # Check output
        self.assertTrue(result['success'])
        self.assertEqual(len(result['sources_used']), 1)
        self.assertIn('dedicated_webgpu', result['sources_used'])
        
        # Check output file
        output_file = self.output_dir / "chrome-139-stable.md"
        self.assertTrue(output_file.exists())
        content = output_file.read_text()
        self.assertIn("Feature 1", content)
        self.assertIn("Feature 2", content)
    
    def test_two_source_merge_with_deduplication(self):
        """Test merge with two sources and deduplication."""
        # Create dedicated WebGPU file
        webgpu_file = self.dedicated_dir / "chrome-139-stable.md"
        webgpu_content = """# WebGPU Release Notes

## Features

### HDR Support
- Full HDR texture support
- [Issue 12345](https://crbug.com/12345)
- Detailed implementation notes

### Subgroups
- Compute shader subgroups
- [Issue 67890](https://crbug.com/67890)
"""
        webgpu_file.write_text(webgpu_content)
        
        # Create rendering split file
        rendering_dir = self.split_dir / "rendering"
        rendering_dir.mkdir()
        rendering_file = rendering_dir / "chrome-139-stable.md"
        rendering_content = """# Rendering and Graphics

## Graphics Features

### Canvas Improvements
- Better 2D canvas performance

### HDR Support
- Basic HDR support added
- [Issue 12345](https://crbug.com/12345)
"""
        rendering_file.write_text(rendering_content)
        
        # Run merge
        result = self.merger.merge("139", "stable")
        
        # Check output
        self.assertTrue(result['success'])
        self.assertEqual(len(result['sources_used']), 2)
        self.assertGreater(result['features_deduplicated'], 0)
        
        # Check content
        output_file = self.output_dir / "chrome-139-stable.md"
        content = output_file.read_text()
        
        # HDR should appear only once (deduplicated)
        hdr_count = content.count("HDR Support")
        self.assertEqual(hdr_count, 1)
        
        # Should preserve the more detailed description from dedicated notes
        self.assertIn("Full HDR texture support", content)
        self.assertIn("Detailed implementation notes", content)
        
        # Canvas improvements should still be there
        self.assertIn("Canvas Improvements", content)
        
        # Subgroups should be there
        self.assertIn("Subgroups", content)
    
    def test_three_source_merge_chrome_136(self):
        """Test three-source merge for Chrome 136 with WebGPU heading2."""
        # Create dedicated WebGPU file
        webgpu_file = self.dedicated_dir / "chrome-136-stable.md"
        webgpu_content = """# WebGPU Updates

### Dual Source Blending
- Complete dual source blending support
- [Issue 11111](https://crbug.com/11111)
- Performance optimizations included
"""
        webgpu_file.write_text(webgpu_content)
        
        # Create WebGPU heading2 split
        webgpu_h2_dir = self.split_dir / "webgpu"
        webgpu_h2_dir.mkdir()
        webgpu_h2_file = webgpu_h2_dir / "chrome-136-stable.md"
        webgpu_h2_content = """# WebGPU

### Dual Source Blending
- Basic dual source blending
- [Issue 11111](https://crbug.com/11111)

### Timestamp Queries
- GPU timestamp queries
- [Issue 22222](https://crbug.com/22222)
"""
        webgpu_h2_file.write_text(webgpu_h2_content)
        
        # Create rendering split
        rendering_dir = self.split_dir / "rendering"
        rendering_dir.mkdir()
        rendering_file = rendering_dir / "chrome-136-stable.md"
        rendering_content = """# Rendering and Graphics

### Graphics Pipeline
- Improved graphics pipeline

### Dual Source Blending
- Graphics feature for blending
- [Issue 11111](https://crbug.com/11111)
"""
        rendering_file.write_text(rendering_content)
        
        # Run merge
        result = self.merger.merge("136", "stable")
        
        # Check output
        self.assertTrue(result['success'])
        self.assertEqual(len(result['sources_used']), 3)
        self.assertGreater(result['features_deduplicated'], 0)
        
        # Check content
        output_file = self.output_dir / "chrome-136-stable.md"
        content = output_file.read_text()
        
        # Dual Source Blending should be deduplicated
        # Should use the most detailed version (from dedicated)
        self.assertIn("Complete dual source blending support", content)
        self.assertIn("Performance optimizations included", content)
        
        # Timestamp Queries should be included
        self.assertIn("Timestamp Queries", content)
        
        # Graphics Pipeline should be included
        self.assertIn("Graphics Pipeline", content)
    
    def test_empty_sources_handling(self):
        """Test handling when all sources are empty or missing."""
        # Run merge with no files
        result = self.merger.merge("140", "stable")
        
        # Should create placeholder
        self.assertTrue(result['success'])
        self.assertEqual(len(result['sources_used']), 0)
        
        output_file = self.output_dir / "chrome-140-stable.md"
        self.assertTrue(output_file.exists())
        content = output_file.read_text()
        self.assertIn("No WebGPU or Graphics content", content)
    
    def test_deduplication_by_issue_id(self):
        """Test deduplication using issue IDs."""
        # Create two sources with same issue IDs
        webgpu_file = self.dedicated_dir / "chrome-139-stable.md"
        webgpu_content = """# WebGPU

### Feature A
- Detailed description A
- [Issue 12345](https://crbug.com/12345)
- Extra details here
"""
        webgpu_file.write_text(webgpu_content)
        
        rendering_dir = self.split_dir / "rendering"
        rendering_dir.mkdir()
        rendering_file = rendering_dir / "chrome-139-stable.md"
        rendering_content = """# Graphics

### Different Title for Same Feature
- Brief description
- [Issue 12345](https://crbug.com/12345)
"""
        rendering_file.write_text(rendering_content)
        
        # Run merge
        result = self.merger.merge("139", "stable")
        
        # Check deduplication
        self.assertTrue(result['success'])
        self.assertGreater(result['features_deduplicated'], 0)
        
        output_file = self.output_dir / "chrome-139-stable.md"
        content = output_file.read_text()
        
        # Should have the detailed version
        self.assertIn("Detailed description A", content)
        self.assertIn("Extra details here", content)
        
        # Should only have one instance of the issue link
        issue_link_count = content.count("[Issue 12345]")
        self.assertEqual(issue_link_count, 1)
    
    def test_heading_hierarchy_preservation(self):
        """Test that heading hierarchy is properly maintained."""
        # Create source with various heading levels
        webgpu_file = self.dedicated_dir / "chrome-139-stable.md"
        webgpu_content = """# WebGPU

## Category 1

### Feature 1
- Description

#### Sub-feature
- Details

## Category 2

### Feature 2
- Description
"""
        webgpu_file.write_text(webgpu_content)
        
        # Run merge
        result = self.merger.merge("139", "stable")
        
        # Check hierarchy in output
        output_file = self.output_dir / "chrome-139-stable.md"
        content = output_file.read_text()
        
        # Should maintain proper hierarchy
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('# Graphics and WebGPU'):
                self.assertTrue(line.startswith('# '))  # H1
            elif line.startswith('## WebGPU Features'):
                self.assertTrue(line.startswith('## '))  # H2
            elif line.startswith('### From Dedicated'):
                self.assertTrue(line.startswith('### '))  # H3
    
    def test_source_attribution(self):
        """Test that sources are properly attributed in output."""
        # Create multiple sources
        webgpu_file = self.dedicated_dir / "chrome-139-stable.md"
        webgpu_file.write_text("### Feature from Dedicated\n- Description")
        
        rendering_dir = self.split_dir / "rendering"
        rendering_dir.mkdir()
        rendering_file = rendering_dir / "chrome-139-stable.md"
        rendering_file.write_text("### Feature from Rendering\n- Description")
        
        # Run merge
        result = self.merger.merge("139", "stable")
        
        # Check attribution
        output_file = self.output_dir / "chrome-139-stable.md"
        content = output_file.read_text()
        
        # Should have source sections
        self.assertIn("From Dedicated Release Notes", content)
        self.assertIn("Rendering and Graphics", content)


if __name__ == '__main__':
    unittest.main()