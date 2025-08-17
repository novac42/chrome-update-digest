#!/usr/bin/env python3
"""
Process merged WebGPU markdown files to generate YAML with correct area classification.
"""

import sys
from pathlib import Path
import yaml

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.yaml_pipeline import YAMLPipeline
from merge_webgpu_release_notes_v2 import merge_webgpu_notes


def process_merged_webgpu(version: str):
    """
    Process a specific Chrome version with WebGPU merge.
    
    1. First merge WebGPU into Chrome release notes using v2 merger
    2. Then process the merged markdown to generate YAML
    """
    
    print(f"Processing Chrome {version}...")
    
    # Step 1: Merge WebGPU with Chrome release notes using v2
    merged_content = merge_webgpu_notes(version)
    
    if not merged_content:
        print(f"  ❌ Failed to merge WebGPU for version {version}")
        return False
    
    # Save merged markdown
    merged_path = Path(f'upstream_docs/processed_releasenotes/processed_forwebplatform/{version}-merged-webgpu.md')
    merged_path.parent.mkdir(parents=True, exist_ok=True)
    with open(merged_path, 'w', encoding='utf-8') as f:
        f.write(merged_content)
    print(f"  ✓ Saved merged markdown: {merged_path}")
    
    # Step 2: Process the merged markdown to generate YAML
    pipeline = YAMLPipeline()
    
    # Process WITHOUT the merge_webgpu flag since we already merged
    result = pipeline.process_release_notes(
        markdown_content=merged_content,
        version=version,
        channel="stable",
        save_yaml=True,
        split_by_area=True,
        merge_webgpu=False  # Important: Don't merge again!
    )
    
    print(f"  ✓ Generated YAML files from merged content")
    print(f"    Total features: {result['statistics']['total_features']}")
    
    # Check WebGPU YAML
    webgpu_yaml_path = Path(f'upstream_docs/processed_releasenotes/processed_forwebplatform/webgpu/chrome-{version}-stable.yml')
    
    if webgpu_yaml_path.exists():
        with open(webgpu_yaml_path, 'r', encoding='utf-8') as f:
            webgpu_data = yaml.safe_load(f)
        
        feature_count = len(webgpu_data.get('features', []))
        print(f"  ✓ WebGPU YAML: {feature_count} features")
        
        # Show sample features
        print("    Sample WebGPU features:")
        for i, feature in enumerate(webgpu_data.get('features', [])[:5]):
            title = feature.get('title', 'N/A')
            print(f"      {i+1}. {title}")
    else:
        print(f"  ⚠️  No WebGPU YAML generated")
    
    return True


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Process merged WebGPU release notes")
    parser.add_argument("--version", required=True, help="Chrome version to process")
    
    args = parser.parse_args()
    
    success = process_merged_webgpu(args.version)
    
    if success:
        print(f"\n✅ Successfully processed Chrome {args.version} with WebGPU merge")
    else:
        print(f"\n❌ Failed to process Chrome {args.version}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())