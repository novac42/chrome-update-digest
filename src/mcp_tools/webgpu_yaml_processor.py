"""
MCP Tool for processing merged WebGPU markdown files to generate YAML.
"""

import json
import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


class WebGPUYAMLProcessorTool:
    """MCP tool for processing merged WebGPU content into structured YAML."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.processed_dir = base_path / "upstream_docs" / "processed_releasenotes" / "processed_forwebplatform"
        
    async def process_webgpu_yaml(self, ctx, version: str,
                                 merge_first: bool = True,
                                 target_areas: Optional[List[str]] = None) -> str:
        """
        Process merged WebGPU markdown to generate structured YAML files.
        
        Parameters:
        - version: Chrome version number
        - merge_first: Whether to merge WebGPU content first (default: True)
        - target_areas: Optional list of specific areas to generate (None for all)
        
        Returns JSON with processing results.
        """
        try:
            # Import dependencies
            import sys
            sys.path.append(str(self.base_path))
            from src.utils.yaml_pipeline import YAMLPipeline
            from src.merge_webgpu_release_notes_v2 import merge_webgpu_notes
            
            # Step 1: Merge WebGPU if requested
            if merge_first:
                logger.info(f"Merging WebGPU content for Chrome {version}")
                merged_content = merge_webgpu_notes(version)
                
                if not merged_content:
                    return json.dumps({
                        "error": f"Failed to merge WebGPU for version {version}",
                        "suggestion": "Check if WebGPU release notes exist for this version"
                    })
                
                # Save merged markdown
                merged_path = self.processed_dir / f"{version}-merged-webgpu.md"
                merged_path.parent.mkdir(parents=True, exist_ok=True)
                with open(merged_path, 'w', encoding='utf-8') as f:
                    f.write(merged_content)
                logger.info(f"Saved merged markdown: {merged_path}")
            else:
                # Load existing merged content
                merged_path = self.processed_dir / f"{version}-merged-webgpu.md"
                if not merged_path.exists():
                    return json.dumps({
                        "error": f"No merged WebGPU content found for version {version}",
                        "suggestion": "Set merge_first=true or run WebGPU merger first"
                    })
                with open(merged_path, 'r', encoding='utf-8') as f:
                    merged_content = f.read()
            
            # Step 2: Process to YAML
            pipeline = YAMLPipeline()
            
            # Process WITHOUT the merge_webgpu flag since we already merged
            result = pipeline.process_release_notes(
                markdown_content=merged_content,
                version=version,
                channel="stable",
                save_yaml=True,
                split_by_area=True,
                merge_webgpu=False  # Important: already merged
            )
            
            if not result:
                return json.dumps({
                    "error": f"Failed to process merged content to YAML",
                    "version": version
                })
            
            # Filter areas if specified
            area_files = result.get('area_files', {})
            if target_areas:
                area_files = {k: v for k, v in area_files.items() 
                            if k in target_areas}
            
            return json.dumps({
                "version": version,
                "success": True,
                "total_features": result.get('statistics', {}).get('total_features', 0),
                "total_links": result.get('statistics', {}).get('total_links', 0),
                "areas_generated": list(area_files.keys()),
                "output_files": {
                    "main_yaml": str(result.get('yaml_file', '')),
                    "merged_markdown": str(merged_path),
                    "area_yamls": {
                        area: str(path) for area, path in area_files.items()
                    }
                },
                "statistics": result.get('statistics', {})
            }, indent=2)
            
        except Exception as e:
            logger.error(f"Error processing WebGPU YAML: {e}")
            return json.dumps({
                "error": str(e),
                "version": version
            })