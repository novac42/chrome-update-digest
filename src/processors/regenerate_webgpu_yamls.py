#!/usr/bin/env python3
"""
Script to regenerate WebGPU YAML files with merged content for all available versions.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.yaml_pipeline import YAMLPipeline


def regenerate_webgpu_yamls():
    """Regenerate WebGPU YAML files for all versions with WebGPU release notes."""
    
    print("=" * 50)
    print("Regenerating WebGPU YAML Files")
    print("=" * 50)
    
    pipeline = YAMLPipeline()
    release_notes_dir = Path('upstream_docs/release_notes/WebPlatform')
    
    # Find all Chrome versions with WebGPU notes
    webgpu_files = list(release_notes_dir.glob('webgpu-*.md'))
    versions_to_process = []
    
    for webgpu_file in webgpu_files:
        version = webgpu_file.stem.split('-')[1]
        if version.isdigit():
            chrome_file = release_notes_dir / f'chrome-{version}.md'
            if chrome_file.exists():
                versions_to_process.append(version)
    
    versions_to_process.sort(key=int, reverse=True)
    
    print(f"Found {len(versions_to_process)} versions with WebGPU notes")
    print(f"Versions: {', '.join(versions_to_process)}")
    print()
    
    success_count = 0
    failure_count = 0
    
    for version in versions_to_process:
        print(f"Processing Chrome {version}...")
        
        chrome_path = release_notes_dir / f'chrome-{version}.md'
        
        try:
            # Read Chrome content
            with open(chrome_path, 'r', encoding='utf-8') as f:
                chrome_content = f.read()
            
            # Process with merge enabled
            result = pipeline.process_release_notes(
                markdown_content=chrome_content,
                version=version,
                channel="stable",
                save_yaml=True,
                split_by_area=True,
                merge_webgpu=True  # Enable WebGPU merge
            )
            
            # Check if WebGPU YAML was generated
            webgpu_yaml_path = Path(f'upstream_docs/processed_releasenotes/processed_forwebplatform/webgpu/chrome-{version}-stable.yml')
            
            if webgpu_yaml_path.exists():
                import yaml
                with open(webgpu_yaml_path, 'r', encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f)
                feature_count = len(yaml_data.get('features', []))
                print(f"  ✓ Generated WebGPU YAML with {feature_count} features")
                success_count += 1
            else:
                # Check if there were any WebGPU features
                webgpu_features = 0
                for feature in result.get('features', []):
                    area = pipeline._determine_area(feature)
                    if area == 'webgpu':
                        webgpu_features += 1
                
                if webgpu_features > 0:
                    print(f"  ⚠️  Expected WebGPU YAML but not generated ({webgpu_features} features found)")
                    failure_count += 1
                else:
                    print(f"  - No WebGPU features found (skipped)")
        
        except Exception as e:
            print(f"  ❌ Error: {e}")
            failure_count += 1
        
        print()
    
    print("=" * 50)
    print("Summary")
    print("=" * 50)
    print(f"Successfully processed: {success_count}/{len(versions_to_process)} versions")
    
    if failure_count > 0:
        print(f"Failed: {failure_count} versions")
        return False
    
    return True


if __name__ == "__main__":
    success = regenerate_webgpu_yamls()
    
    if success:
        print("\n✅ All WebGPU YAML files regenerated successfully!")
        sys.exit(0)
    else:
        print("\n⚠️  Some versions had issues, please review")
        sys.exit(1)