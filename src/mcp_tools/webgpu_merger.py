"""
MCP Tool for merging WebGPU release notes with Chrome release notes.
"""

import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class WebGPUMergerTool:
    """MCP tool for merging WebGPU content into Chrome release notes."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.release_notes_dir = base_path / "upstream_docs" / "release_notes"
        self.output_dir = base_path / "upstream_docs" / "processed_releasenotes" / "processed_forwebplatform"
        
    async def merge_webgpu_notes(self, ctx, version: str,
                                save_output: bool = True,
                                include_metadata: bool = False) -> str:
        """
        Merge WebGPU release notes into Chrome release notes.
        
        Parameters:
        - version: Chrome version number
        - save_output: Whether to save the merged output to file (default: True)
        - include_metadata: Whether to include WebGPU metadata sections (default: False)
        
        Returns the merged markdown content or error message.
        """
        try:
            # Import the merger
            import sys
            sys.path.append(str(self.base_path))
            from src.merge_webgpu_release_notes_v2 import WebGPUMergerV2
            
            # Initialize merger
            merger = WebGPUMergerV2(
                upstream_docs_dir=str(self.base_path / "upstream_docs")
            )
            
            # Check if Chrome release notes exist
            chrome_path = self.release_notes_dir / "WebPlatform" / f"chrome-{version}-release-notes-webplatform.md"
            if not chrome_path.exists():
                # Try alternate patterns
                chrome_patterns = [
                    f"chrome-{version}*.md",
                    f"*{version}*.md"
                ]
                for pattern in chrome_patterns:
                    files = list((self.release_notes_dir / "WebPlatform").glob(pattern))
                    if files:
                        chrome_path = files[0]
                        break
                else:
                    return json.dumps({
                        "error": f"Chrome release notes not found for version {version}",
                        "searched_dir": str(self.release_notes_dir / "WebPlatform")
                    })
            
            # Check if WebGPU release notes exist
            webgpu_path = self.release_notes_dir / "WebGPU" / f"webgpu-release-notes-{version}.md"
            if not webgpu_path.exists():
                # Try alternate patterns
                webgpu_patterns = [
                    f"webgpu*{version}*.md",
                    f"*{version}*.md"
                ]
                for pattern in webgpu_patterns:
                    files = list((self.release_notes_dir / "WebGPU").glob(pattern))
                    if files:
                        webgpu_path = files[0]
                        break
                else:
                    logger.warning(f"WebGPU release notes not found for version {version}")
                    # Return original Chrome content
                    with open(chrome_path, 'r', encoding='utf-8') as f:
                        return json.dumps({
                            "version": version,
                            "warning": "No WebGPU content to merge",
                            "content": f.read(),
                            "chrome_file": str(chrome_path)
                        })
            
            # Read files
            with open(chrome_path, 'r', encoding='utf-8') as f:
                chrome_content = f.read()
            
            with open(webgpu_path, 'r', encoding='utf-8') as f:
                webgpu_content = f.read()
            
            # Extract WebGPU features
            features = merger.extract_webgpu_features(webgpu_content)
            
            if not features:
                return json.dumps({
                    "version": version,
                    "warning": "No WebGPU features found to merge",
                    "content": chrome_content,
                    "chrome_file": str(chrome_path),
                    "webgpu_file": str(webgpu_path)
                })
            
            # Merge content
            merged_content = merger.merge_with_chrome(chrome_content, features)
            
            # Save if requested
            output_path = None
            if save_output:
                output_path = self.output_dir / f"{version}-merged-webgpu.md"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(merged_content)
                logger.info(f"Saved merged content to {output_path}")
            
            # Calculate statistics
            webgpu_features_count = len(features)
            total_lines = len(merged_content.split('\n'))
            
            return json.dumps({
                "version": version,
                "success": True,
                "webgpu_features_merged": webgpu_features_count,
                "total_lines": total_lines,
                "files": {
                    "chrome_source": str(chrome_path),
                    "webgpu_source": str(webgpu_path),
                    "output": str(output_path) if output_path else None
                },
                "content_preview": merged_content[:1000] + "..." if len(merged_content) > 1000 else merged_content
            }, indent=2)
            
        except Exception as e:
            logger.error(f"Error merging WebGPU notes: {e}")
            return json.dumps({
                "error": str(e),
                "version": version
            })