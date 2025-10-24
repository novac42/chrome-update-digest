#!/usr/bin/env python3
"""
Test script for the updated focus areas configuration.
Tests heading-first matching and Web API exception.
"""

import sys
from pathlib import Path

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from chrome_update_digest.utils.focus_area_manager import FocusAreaManager


def test_focus_area_manager():
    """Test the new focus area configuration and matching logic."""
    
    # Initialize manager with new config
    config_path = Path('config/focus_areas.yaml')
    manager = FocusAreaManager(config_path)
    
    print("Focus Areas Configuration Test")
    print("=" * 60)
    
    # List all configured areas
    print("\nConfigured Focus Areas:")
    print("-" * 40)
    areas = manager.list_areas()
    for area in areas:
        info = manager.get_area_info(area)
        print(f"  {area}: {info.get('name', area)}")
    
    # Test cases for heading-first matching
    print("\n" + "=" * 60)
    print("Testing Heading-First Matching")
    print("=" * 60)
    
    test_features = [
        {
            "title": "New CSS Grid Feature",
            "heading": "CSS and UI",
            "content": "A new CSS grid property has been added."
        },
        {
            "title": "WebGPU Compute Shaders",
            "heading": "WebGPU",
            "content": "WebGPU now supports compute shaders."
        },
        {
            "title": "New Fetch API Method",
            "heading": "Web APIs",
            "content": "The Fetch API has a new method for streaming."
        },
        {
            "title": "On-device Translation API",
            "heading": "Web APIs",
            "content": "New on-device AI translation capabilities."
        },
        {
            "title": "Feature Being Removed",
            "heading": "Deprecations and removals",
            "content": "This old API is being deprecated."
        },
        {
            "title": "Random Feature",
            "heading": "JavaScript",
            "content": "Some JavaScript feature."
        },
        {
            "title": "No Heading Feature",
            "heading": "",
            "content": "This feature has no heading but mentions CSS styling."
        }
    ]
    
    for i, feature in enumerate(test_features, 1):
        tags = manager.tag_feature(feature)
        print(f"\nTest {i}: {feature['title']}")
        print(f"  Heading: '{feature['heading']}'")
        print(f"  Tags: {tags}")
        
        # Verify expected behavior
        if feature['heading'] == 'Web APIs':
            # Should check for additional tags due to Web API exception
            if 'on-device' in feature['content'].lower():
                assert 'on-device-ai' in tags or len(tags) > 1, "Web API should allow multiple tags"
        elif feature['heading']:
            # Should use heading match primarily
            assert len(tags) >= 1, "Should have at least one tag from heading"
    
    # Test keyword fallback when no heading
    print("\n" + "=" * 60)
    print("Testing Keyword Fallback (No Heading)")
    print("=" * 60)
    
    no_heading_tests = [
        {
            "title": "Performance Optimization",
            "heading": "",
            "content": "This improves performance and speed."
        },
        {
            "title": "Media Codec Update",
            "heading": "",
            "content": "New audio and video codecs supported."
        },
        {
            "title": "Security Fix",
            "heading": "",
            "content": "Important security vulnerability patched."
        }
    ]
    
    for feature in no_heading_tests:
        tags = manager.tag_feature(feature)
        print(f"\n{feature['title']}")
        print(f"  Content keywords: {feature['content'][:50]}...")
        print(f"  Tags: {tags}")
    
    # Test filtering
    print("\n" + "=" * 60)
    print("Testing Feature Filtering")
    print("=" * 60)
    
    # Create features with tags
    tagged_features = [
        {"title": "CSS Feature", "primary_tags": [{"name": "css"}]},
        {"title": "WebGPU Feature", "primary_tags": [{"name": "graphics-webgpu"}]},
        {"title": "AI Feature", "primary_tags": [{"name": "on-device-ai"}]},
        {"title": "Security Feature", "primary_tags": [{"name": "security-privacy"}]},
        {"title": "Other Feature", "primary_tags": [{"name": "others"}]}
    ]
    
    # Test filtering by specific areas
    focus_areas = ["css", "ai", "webgpu"]
    filtered = manager.filter_features(tagged_features, focus_areas)
    
    print(f"\nFiltering by: {focus_areas}")
    print(f"Original features: {len(tagged_features)}")
    print(f"Filtered features: {len(filtered)}")
    print("Filtered titles:")
    for f in filtered:
        print(f"  - {f['title']}")
    
    # Test area splitting
    print("\n" + "=" * 60)
    print("Testing Feature Splitting by Area")
    print("=" * 60)
    
    area_split = manager.split_features_by_area(tagged_features)
    for area, features in area_split.items():
        print(f"\n{area}: {len(features)} features")
        for f in features:
            print(f"  - {f['title']}")
    
    print("\n" + "=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    test_focus_area_manager()