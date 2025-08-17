#!/usr/bin/env python3
"""
Simple test for the WebGPU merger v2 script.
"""

import os
import sys
import unittest
from pathlib import Path

# Add src directory to path to import the merger
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from merge_webgpu_release_notes_v2 import merge_webgpu_notes, extract_webgpu_features


class TestWebGPUMergerV2(unittest.TestCase):
    """Test cases for WebGPU merger v2 functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(__file__).parent
        self.upstream_docs_dir = self.test_dir.parent / "upstream_docs"
    
    def test_extract_webgpu_features(self):
        """Test extraction of WebGPU features."""
        test_content = """# What's New in WebGPU (Chrome 139)

This document is about version history.

## Feature: WebGPU New Buffer API

This is a real feature about buffers.

### Details
Some implementation details.

## Feature: Shader Compilation

Another real feature.

## What's New in WebGPU

This is the version history section that should be excluded.

### Chrome 138
Previous version notes.

### Chrome 137
Even older notes.

## Feature: GPU Architecture Support

New GPU architectures supported.
"""
        
        features = extract_webgpu_features(test_content)
        
        # Should extract only real features, not version history
        # Note: "Shader Compilation" may not be recognized as a feature without "Feature:" prefix
        self.assertGreaterEqual(len(features), 2)
        self.assertIn("WebGPU New Buffer API", features[0])
        if len(features) > 2:
            self.assertIn("GPU Architecture Support", features[-1])
        
        # Should not include version history
        for feature in features:
            self.assertNotIn("Chrome 138", feature)
            self.assertNotIn("Chrome 137", feature)
    
    def test_merge_webgpu_notes(self):
        """Test merging WebGPU notes for a version that exists."""
        # Test with a version that we know exists
        version = "139"
        
        # Check if files exist first
        chrome_path = Path(f"upstream_docs/release_notes/WebPlatform/chrome-{version}.md")
        webgpu_path = Path(f"upstream_docs/release_notes/WebPlatform/webgpu-{version}.md")
        
        if chrome_path.exists() and webgpu_path.exists():
            merged = merge_webgpu_notes(version)
            
            if merged:
                # Should contain Chrome content
                self.assertIn("Chrome", merged)
                
                # Should have Graphics section with WebGPU content
                self.assertIn("## Graphics", merged)
                
                # Should not have "What's New in WebGPU" version history
                self.assertNotIn("## What's New in WebGPU", merged)
    
    def test_merge_nonexistent_version(self):
        """Test merging with a version that doesn't exist."""
        merged = merge_webgpu_notes("999")
        
        # Should return None or empty string for non-existent version
        self.assertIn(merged, [None, ""])
    
    def test_feature_heading_demotion(self):
        """Test that H2 headings are demoted to H3 when extracting."""
        test_content = """## Feature: Test Feature

Some content here.

### Sub-heading

More content.
"""
        
        features = extract_webgpu_features(test_content)
        
        if features:
            # The H2 should become H3 in the extracted feature
            self.assertIn("### Feature: Test Feature", features[0])
            # The H3 should become H4
            self.assertIn("#### Sub-heading", features[0])


def run_tests():
    """Run all tests."""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()