#!/usr/bin/env python3
"""
Test script for WebGPU merge functionality in YAML pipeline.
"""

import sys
from pathlib import Path
import yaml

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.yaml_pipeline import YAMLPipeline


def test_webgpu_merge():
    """Test WebGPU merge functionality with Chrome 139."""
    
    print("=" * 50)
    print("Testing WebGPU Merge for Chrome 139")
    print("=" * 50)
    
    # Initialize pipeline
    pipeline = YAMLPipeline()
    
    # Test with Chrome 139
    chrome_path = Path('upstream_docs/release_notes/WebPlatform/chrome-139.md')
    webgpu_path = Path('upstream_docs/release_notes/WebPlatform/webgpu-139.md')
    
    if not chrome_path.exists():
        print(f"❌ Chrome release notes not found: {chrome_path}")
        return False
    
    print(f"✓ Found Chrome release notes: {chrome_path}")
    
    if webgpu_path.exists():
        print(f"✓ Found WebGPU release notes: {webgpu_path}")
    else:
        print(f"❌ WebGPU release notes not found: {webgpu_path}")
    
    # Read Chrome content
    with open(chrome_path, 'r', encoding='utf-8') as f:
        chrome_content = f.read()
    
    print("\n" + "=" * 50)
    print("Processing WITHOUT WebGPU merge...")
    print("=" * 50)
    
    # Process without merge
    result_no_merge = pipeline.process_release_notes(
        markdown_content=chrome_content,
        version="139",
        channel="stable",
        save_yaml=False,
        split_by_area=True,
        merge_webgpu=False  # Disable merge
    )
    
    # Count WebGPU features without merge
    webgpu_features_no_merge = 0
    for feature in result_no_merge.get('features', []):
        area = pipeline._determine_area(feature)
        if area == 'webgpu':
            webgpu_features_no_merge += 1
    
    print(f"Total features: {result_no_merge['statistics']['total_features']}")
    print(f"WebGPU features (without merge): {webgpu_features_no_merge}")
    
    print("\n" + "=" * 50)
    print("Processing WITH WebGPU merge...")
    print("=" * 50)
    
    # Process with merge
    result_with_merge = pipeline.process_release_notes(
        markdown_content=chrome_content,
        version="139",
        channel="stable",
        save_yaml=True,
        split_by_area=True,
        merge_webgpu=True  # Enable merge
    )
    
    # Count WebGPU features with merge
    webgpu_features_with_merge = 0
    for feature in result_with_merge.get('features', []):
        area = pipeline._determine_area(feature)
        if area == 'webgpu':
            webgpu_features_with_merge += 1
    
    print(f"Total features: {result_with_merge['statistics']['total_features']}")
    print(f"WebGPU features (with merge): {webgpu_features_with_merge}")
    
    print("\n" + "=" * 50)
    print("Verification")
    print("=" * 50)
    
    # Load the generated WebGPU YAML file
    webgpu_yaml_path = Path('upstream_docs/processed_releasenotes/processed_forwebplatform/webgpu/chrome-139-stable.yml')
    
    if webgpu_yaml_path.exists():
        with open(webgpu_yaml_path, 'r', encoding='utf-8') as f:
            webgpu_yaml = yaml.safe_load(f)
        
        webgpu_yaml_features = len(webgpu_yaml.get('features', []))
        print(f"✓ WebGPU YAML file generated: {webgpu_yaml_path}")
        print(f"  Features in YAML: {webgpu_yaml_features}")
        
        # Show first few feature titles
        print("\n  Sample features:")
        for i, feature in enumerate(webgpu_yaml.get('features', [])[:5]):
            print(f"    {i+1}. {feature.get('title', 'N/A')}")
        
        if webgpu_yaml_features > 5:
            print(f"    ... and {webgpu_yaml_features - 5} more")
    else:
        print(f"❌ WebGPU YAML file not generated: {webgpu_yaml_path}")
    
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)
    
    improvement = webgpu_features_with_merge - webgpu_features_no_merge
    
    if improvement > 0:
        print(f"✅ SUCCESS: WebGPU merge added {improvement} features!")
        print(f"   Before: {webgpu_features_no_merge} features")
        print(f"   After:  {webgpu_features_with_merge} features")
        return True
    else:
        print(f"⚠️  WARNING: No improvement detected")
        print(f"   Before: {webgpu_features_no_merge} features")
        print(f"   After:  {webgpu_features_with_merge} features")
        return False


def verify_all_versions():
    """Verify WebGPU merge for all available versions."""
    
    print("\n" + "=" * 50)
    print("Verifying All Versions with WebGPU Notes")
    print("=" * 50)
    
    pipeline = YAMLPipeline()
    release_notes_dir = Path('upstream_docs/release_notes/WebPlatform')
    
    # Find all Chrome versions with WebGPU notes
    webgpu_files = list(release_notes_dir.glob('webgpu-*.md'))
    versions_to_check = []
    
    for webgpu_file in webgpu_files:
        version_match = webgpu_file.stem.split('-')[1]
        if version_match.isdigit():
            chrome_file = release_notes_dir / f'chrome-{version_match}.md'
            if chrome_file.exists():
                versions_to_check.append(version_match)
    
    versions_to_check.sort(key=int)
    
    print(f"Found {len(versions_to_check)} versions with WebGPU notes: {', '.join(versions_to_check)}")
    
    for version in versions_to_check[-3:]:  # Check last 3 versions
        print(f"\nProcessing Chrome {version}...")
        
        chrome_path = release_notes_dir / f'chrome-{version}.md'
        with open(chrome_path, 'r', encoding='utf-8') as f:
            chrome_content = f.read()
        
        # Process with merge
        result = pipeline.process_release_notes(
            markdown_content=chrome_content,
            version=version,
            channel="stable",
            save_yaml=True,
            split_by_area=True,
            merge_webgpu=True
        )
        
        # Check generated WebGPU YAML
        yaml_path = Path(f'upstream_docs/processed_releasenotes/processed_forwebplatform/webgpu/chrome-{version}-stable.yml')
        
        if yaml_path.exists():
            with open(yaml_path, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)
            feature_count = len(yaml_data.get('features', []))
            print(f"  ✓ Generated WebGPU YAML with {feature_count} features")
        else:
            print(f"  ❌ Failed to generate WebGPU YAML")


if __name__ == "__main__":
    success = test_webgpu_merge()
    
    if success:
        verify_all_versions()
        print("\n✅ WebGPU merge implementation successful!")
        sys.exit(0)
    else:
        print("\n❌ WebGPU merge implementation needs review")
        sys.exit(1)