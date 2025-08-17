#!/usr/bin/env python3
"""
Unit tests for process_enterprise_release.py
"""

import unittest
from pathlib import Path
import sys
import tempfile
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process_enterprise_release import ReleaseNotesProcessorV2, Feature


class TestReleaseNotesProcessorV2(unittest.TestCase):
    """Test cases for ReleaseNotesProcessorV2"""
    
    def setUp(self):
        """Set up test environment"""
        self.processor = ReleaseNotesProcessorV2()
        
    def test_extract_current_version(self):
        """Test version extraction"""
        content = """
## Chrome 138 release summary

Some content here
"""
        version = self.processor.extract_current_version(content)
        self.assertEqual(version, 138)
        
        # Test with no version
        content_no_version = "No version here"
        version = self.processor.extract_current_version(content_no_version)
        self.assertIsNone(version)
    
    def test_parse_tables_basic(self):
        """Test basic table parsing"""
        content = """
## Chrome browser changes

| Feature | Security/Privacy | User productivity/Apps | Management |
|---------|-----------------|----------------------|-------------|
| [Feature One](link) | ✓ | | ✓ |
| [Feature Two](link) | | ✓ | |
"""
        feature_info = self.processor.parse_tables(content)
        
        self.assertIn("Feature One", feature_info)
        self.assertIn("Feature Two", feature_info)
        
        self.assertEqual(feature_info["Feature One"]["categories"], ["Security/Privacy", "Management"])
        self.assertEqual(feature_info["Feature One"]["change_type"], "Chrome Browser changes")
        self.assertEqual(feature_info["Feature One"]["status"], "current")
        
        self.assertEqual(feature_info["Feature Two"]["categories"], ["User productivity/Apps"])
    
    def test_parse_tables_with_upcoming(self):
        """Test table parsing with upcoming sections"""
        content = """
## Chrome browser changes

| Feature | Security/Privacy | User productivity/Apps | Management |
|---------|-----------------|----------------------|-------------|
| [Current Feature](link) | ✓ | | |

### Upcoming Chrome browser changes

| Feature | Security/Privacy | User productivity/Apps | Management |
|---------|-----------------|----------------------|-------------|
| [Upcoming Feature](link) | | ✓ | |
"""
        feature_info = self.processor.parse_tables(content)
        
        self.assertEqual(feature_info["Current Feature"]["status"], "current")
        self.assertEqual(feature_info["Upcoming Feature"]["status"], "upcoming")
    
    def test_identify_upcoming_features(self):
        """Test identification of upcoming features"""
        content = """
## Current features

### Feature A
Some content

## Upcoming Chrome browser changes

### Feature B
Some upcoming content

#### Feature C
Another upcoming feature

## Download Release Notes
End of document
"""
        upcoming = self.processor.identify_upcoming_features(content)
        
        self.assertIn("Feature B", upcoming)
        self.assertIn("Feature C", upcoming)
        self.assertNotIn("Feature A", upcoming)
        self.assertNotIn("Upcoming Chrome browser changes", upcoming)
    
    def test_extract_feature_from_section(self):
        """Test feature extraction from section"""
        content = """### Test Feature

This is a test feature description with some details.

The feature is controlled by the [TestPolicy](https://chromeenterprise.google/policies/#TestPolicy) policy.

- Chrome 138 on Windows, macOS, and Linux
- Chrome 139 on Android

More content here.
"""
        feature_info = {"Test Feature": {
            "categories": ["Security/Privacy"],
            "change_type": "Chrome Browser changes",
            "status": "current"
        }}
        
        # Find the start position of the feature
        start_pos = content.find("### Test Feature")
        
        feature = self.processor.extract_feature_from_section(
            "Test Feature", content, start_pos, feature_info, set()
        )
        
        self.assertIsNotNone(feature)
        self.assertEqual(feature.title, "Test Feature")
        self.assertEqual(feature.categories, ["Security/Privacy"])
        self.assertEqual(feature.status, "current")
        self.assertEqual(feature.policy, "TestPolicy")
        self.assertIn("Windows", feature.platforms)
        self.assertIn("macOS", feature.platforms)
        self.assertIn("Linux", feature.platforms)
        self.assertIn("test feature description", feature.description)
    
    def test_extract_feature_skip_headers(self):
        """Test that section headers are skipped"""
        skip_titles = [
            "Chrome browser changes",
            "Chrome Enterprise Core changes",
            "Chrome Enterprise Premium changes",
            "Upcoming Chrome browser changes"
        ]
        
        for title in skip_titles:
            feature = self.processor.extract_feature_from_section(
                title, "", 0, {}, set()
            )
            self.assertIsNone(feature)
    
    def test_handle_special_features_new_policies(self):
        """Test handling of new policies section"""
        content = """
### New policies in Chrome browser

[PolicyOne](link) - Description
[PolicyTwo](link) - Another description

### Other section
"""
        special_features = self.processor.handle_special_features(content)
        
        self.assertEqual(len(special_features), 1)
        feature = special_features[0]
        self.assertEqual(feature.title, "New policies in Chrome browser")
        self.assertIn("PolicyOne", feature.description)
        self.assertIn("PolicyTwo", feature.description)
        self.assertEqual(feature.categories, ["Management"])
    
    def test_format_feature(self):
        """Test feature formatting"""
        feature = Feature(
            title="Test Feature",
            change_type="Chrome Browser changes",
            categories=["Security/Privacy", "Management"],
            status="current",
            platforms=["Windows", "macOS"],
            description="Test description",
            policy="TestPolicy"
        )
        
        formatted = self.processor.format_feature(feature)
        
        self.assertIn("**Test Feature**", formatted)
        self.assertIn("Type: Chrome Browser changes", formatted)
        self.assertIn("Platform: Desktop (Windows, macOS)", formatted)
        self.assertIn("Test description", formatted)
        self.assertIn("`TestPolicy` policy", formatted)
    
    def test_format_feature_upcoming(self):
        """Test formatting of upcoming features"""
        self.processor.current_version = 138
        feature = Feature(
            title="Upcoming Feature",
            change_type="Chrome Browser changes",
            categories=["User productivity/Apps"],
            status="upcoming",
            version_info="Chrome 139"
        )
        
        formatted = self.processor.format_feature(feature)
        
        self.assertIn("**Upcoming Feature** (Chrome 139)", formatted)
    
    def test_extract_feature_with_rollout_info(self):
        """Test feature extraction including rollout information"""
        content = """### Lens overlay for image search

Google Lens is adding an overlay feature that allows users to search images on a page.

- Chrome 138 on ChromeOS, Linux, macOS, Windows: Feature starts rollout
- Chrome 140 on ChromeOS, Linux, macOS, Windows: If the LensOverlaySettings policy is not set this feature will respect the GenAiDefaultSettings policy if present.

This feature is controlled by the [LensOverlaySettings](https://chromeenterprise.google/policies/#LensOverlaySettings) policy.
"""
        feature_info = {"Lens overlay for image search": {
            "categories": ["User productivity/Apps"],
            "change_type": "Chrome Browser changes",
            "status": "current"
        }}
        
        start_pos = content.find("### Lens overlay")
        feature = self.processor.extract_feature_from_section(
            "Lens overlay for image search", content, start_pos, feature_info, set()
        )
        
        self.assertIsNotNone(feature)
        self.assertEqual(feature.title, "Lens overlay for image search")
        
        # Check that rollout information is included in description
        self.assertIn("Chrome 138 on ChromeOS, Linux, macOS, Windows: Feature starts rollout", feature.description)
        self.assertIn("Chrome 140 on ChromeOS, Linux, macOS, Windows:", feature.description)
        self.assertIn("GenAiDefaultSettings policy if present", feature.description)
        
        # Check policy extraction
        self.assertEqual(feature.policy, "LensOverlaySettings")
        
        # Check platforms were extracted
        self.assertIn("ChromeOS", feature.platforms)
        self.assertIn("Linux", feature.platforms)
        self.assertIn("macOS", feature.platforms)
        self.assertIn("Windows", feature.platforms)
    
    def test_format_feature_with_multiline_description(self):
        """Test formatting features with multi-line descriptions"""
        feature = Feature(
            title="Test Feature",
            change_type="Chrome Browser changes",
            categories=["Security/Privacy"],
            status="current",
            platforms=["Windows", "macOS"],
            description="This is the main description.\n\n- Chrome 138: Feature starts rollout\n- Chrome 139: Feature fully available",
            policy="TestPolicy"
        )
        
        formatted = self.processor.format_feature(feature)
        
        # Check basic formatting
        self.assertIn("**Test Feature**", formatted)
        
        # Check that multi-line description is preserved
        lines = formatted.split('\n')
        # Find the Update line
        update_line_idx = None
        for i, line in enumerate(lines):
            if "Update:" in line:
                update_line_idx = i
                break
        
        self.assertIsNotNone(update_line_idx)
        # Check that rollout info is indented properly
        self.assertIn("This is the main description", lines[update_line_idx])
        # Check subsequent lines are indented
        found_rollout_info = False
        for line in lines[update_line_idx + 1:]:
            if "Chrome 138: Feature starts rollout" in line:
                found_rollout_info = True
                self.assertTrue(line.startswith("    "))  # Should be indented
        
        self.assertTrue(found_rollout_info, "Rollout information should be included")
    
    def test_format_feature_platform_labels(self):
        """Test platform labeling with Desktop/Mobile categories"""
        # Test all platforms
        feature_all = Feature(
            title="All Platform Feature",
            change_type="Chrome Browser changes",
            categories=["Security/Privacy"],
            status="current",
            platforms=["Android", "ChromeOS", "Linux", "macOS", "Windows", "iOS"],
            description="Test feature"
        )
        
        formatted = self.processor.format_feature(feature_all)
        self.assertIn("Desktop (ChromeOS, Linux, Windows, macOS)", formatted)
        self.assertIn("Mobile (Android, iOS)", formatted)
        
        # Test desktop only
        feature_desktop = Feature(
            title="Desktop Feature",
            change_type="Chrome Browser changes", 
            categories=["Security/Privacy"],
            status="current",
            platforms=["Windows", "macOS", "Linux"],
            description="Desktop only feature"
        )
        
        formatted_desktop = self.processor.format_feature(feature_desktop)
        self.assertIn("Desktop (Linux, Windows, macOS)", formatted_desktop)
        self.assertNotIn("Mobile", formatted_desktop)
        
        # Test mobile only
        feature_mobile = Feature(
            title="Mobile Feature",
            change_type="Chrome Browser changes",
            categories=["Security/Privacy"], 
            status="current",
            platforms=["Android", "iOS"],
            description="Mobile only feature"
        )
        
        formatted_mobile = self.processor.format_feature(feature_mobile)
        self.assertIn("Mobile (Android, iOS)", formatted_mobile)
        self.assertNotIn("Desktop", formatted_mobile)
        
        # Test single platform
        feature_single = Feature(
            title="Single Platform Feature",
            change_type="Chrome Browser changes",
            categories=["Security/Privacy"],
            status="current", 
            platforms=["ChromeOS"],
            description="ChromeOS only feature"
        )
        
        formatted_single = self.processor.format_feature(feature_single)
        self.assertIn("Desktop (ChromeOS)", formatted_single)
        self.assertNotIn("Mobile", formatted_single)
    
    def test_generate_organized_output(self):
        """Test organized output generation"""
        self.processor.current_version = 138
        self.processor.features = {
            "Feature A": Feature(
                title="Feature A",
                change_type="Chrome Browser changes",
                categories=["Security/Privacy"],
                status="current",
                description="Feature A description"
            ),
            "Feature B": Feature(
                title="Feature B",
                change_type="Chrome Enterprise Core changes",
                categories=["User productivity/Apps"],
                status="upcoming",
                description="Feature B description"
            )
        }
        
        output = self.processor.generate_organized_output()
        
        # Check structure
        self.assertIn("### User productivity/Apps", output)
        self.assertIn("### Security/Privacy", output)
        self.assertIn("**Current — Chrome 138**", output)
        self.assertIn("**Upcoming — Chrome 139 and beyond**", output)
        
        # Check features appear in correct sections
        self.assertIn("Feature A", output)
        self.assertIn("Feature B", output)
    
    def test_full_processing_with_file(self):
        """Test full processing with a sample file"""
        # Create a temporary test file
        test_content = """
## Chrome 138 release summary

## Chrome browser changes

| Feature | Security/Privacy | User productivity/Apps | Management |
|---------|-----------------|----------------------|-------------|
| [Test Feature](link) | ✓ | | |

### Test Feature

This is a test feature for Chrome 138.

It's controlled by [TestPolicy](https://chromeenterprise.google/policies/#TestPolicy).

- Chrome 138 on Windows and macOS

### Upcoming Chrome browser changes

#### Future Feature

Coming in Chrome 139.
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(test_content)
            temp_file = f.name
        
        try:
            # Process the file
            self.processor.process_release_notes(temp_file)
            
            # Verify results
            self.assertEqual(self.processor.current_version, 138)
            self.assertIn("Test Feature", self.processor.features)
            self.assertIn("Future Feature", self.processor.features)
            
            # Check feature properties
            test_feature = self.processor.features["Test Feature"]
            self.assertEqual(test_feature.status, "current")
            self.assertEqual(test_feature.policy, "TestPolicy")
            
            future_feature = self.processor.features["Future Feature"]
            self.assertEqual(future_feature.status, "upcoming")
            
        finally:
            # Clean up
            os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main()