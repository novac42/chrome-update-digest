#!/usr/bin/env python3
"""
Test script for area-based YAML splitting functionality.
"""

import sys
from pathlib import Path
import asyncio

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.yaml_pipeline import YAMLPipeline


def test_area_splitting():
    """Test splitting Chrome release notes by area."""
    
    # Initialize pipeline
    pipeline = YAMLPipeline()
    
    # Test with Chrome 138
    release_notes_path = Path('upstream_docs/release_notes/webplatform/chrome-138.md')
    
    if not release_notes_path.exists():
        print(f"Release notes not found: {release_notes_path}")
        return
    
    print(f"Processing {release_notes_path.name}...")
    
    with open(release_notes_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process with area splitting
    result = pipeline.process_release_notes(
        markdown_content=content,
        version="138",
        channel="stable",
        save_yaml=True,
        split_by_area=True  # Enable area splitting
    )
    
    print(f"\nProcessing complete!")
    print(f"Total features: {result['statistics']['total_features']}")
    print(f"Total links: {result['statistics']['total_links']}")
    
    if 'areas' in result:
        print(f"\nAreas found: {', '.join(result['areas'])}")
    
    # Check generated files
    output_dir = Path('upstream_docs/processed_releasenotes/tagged_features')
    area_files = list(output_dir.glob('chrome-138-stable-*.yml'))
    
    print(f"\nGenerated YAML files:")
    for file in sorted(area_files):
        # Get file size
        size = file.stat().st_size
        print(f"  - {file.name} ({size:,} bytes)")
    
    # Load and analyze one area file as example
    if area_files:
        example_file = None
        # Try to find css area file
        for f in area_files:
            if 'css' in f.name:
                example_file = f
                break
        
        if not example_file:
            example_file = area_files[0]
        
        print(f"\nExample - {example_file.name}:")
        
        import yaml
        with open(example_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        print(f"  Area: {data.get('area', 'N/A')}")
        print(f"  Features: {len(data.get('features', []))}")
        print(f"  Statistics: {data.get('statistics', {})}")
        
        # Show first feature as example
        if data.get('features'):
            feature = data['features'][0]
            print(f"\n  First feature:")
            print(f"    Title: {feature.get('title', 'N/A')}")
            print(f"    Links: {len(feature.get('links', []))}")
            print(f"    Tags: {[t['name'] for t in feature.get('primary_tags', [])]}")


def list_all_areas():
    """List all areas found across multiple Chrome versions."""
    
    pipeline = YAMLPipeline()
    all_areas = set()
    
    # Process multiple versions
    versions = ['136', '137', '138']
    
    for version in versions:
        release_notes_path = Path(f'upstream_docs/release_notes/webplatform/chrome-{version}.md')
        
        if not release_notes_path.exists():
            continue
        
        print(f"Analyzing Chrome {version}...")
        
        with open(release_notes_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract features to analyze areas
        from src.utils.link_extractor import LinkExtractor
        extractor = LinkExtractor()
        features = extractor.extract_from_content(content)
        
        # Convert to dict format
        features_dict = [f.to_dict() for f in features]
        
        # Split by area
        area_features = pipeline.split_features_by_area(features_dict)
        
        for area in area_features.keys():
            all_areas.add(area)
        
        print(f"  Areas: {', '.join(sorted(area_features.keys()))}")
    
    print(f"\n{'-'*50}")
    print(f"All unique areas across versions: {', '.join(sorted(all_areas))}")
    print(f"Total unique areas: {len(all_areas)}")


if __name__ == '__main__':
    print("Testing area-based YAML splitting...")
    print("="*50)
    
    # Test splitting
    test_area_splitting()
    
    print("\n" + "="*50)
    print("Analyzing all areas across versions...")
    print("="*50)
    
    # List all areas
    list_all_areas()