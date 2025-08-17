"""
MCP Tool for processing Chrome Enterprise Release Notes into structured data.
"""

import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class EnterpriseNotesProcessorTool:
    """MCP tool for processing raw enterprise release notes."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.release_notes_dir = base_path / "upstream_docs" / "release_notes" / "Enterprise"
        self.output_dir = base_path / "upstream_docs" / "processed_releasenotes" / "processed_forenterprise"
        
    async def process_enterprise_notes(self, ctx, version: int,
                                      format_override: Optional[str] = None,
                                      generate_organized: bool = True) -> str:
        """
        Process Chrome Enterprise release notes to extract and organize features.
        
        Parameters:
        - version: Chrome version number
        - format_override: Override format detection ("new" | "legacy" | None for auto)
        - generate_organized: Whether to generate organized markdown output
        
        Returns JSON with processing results.
        """
        try:
            # Import the processor here to avoid circular dependencies
            import sys
            sys.path.append(str(self.base_path))
            from src.process_enterprise_release_note import EnterpriseReleaseNotesProcessor
            
            # Initialize processor
            processor = EnterpriseReleaseNotesProcessor(
                upstream_docs_dir=str(self.base_path / "upstream_docs")
            )
            
            # Find the release notes file
            md_file = self.release_notes_dir / f"chrome-{version}-release-notes.md"
            if not md_file.exists():
                # Try alternate naming patterns
                for pattern in [f"chrome{version}*.md", f"*{version}*.md"]:
                    files = list(self.release_notes_dir.glob(pattern))
                    if files:
                        md_file = files[0]
                        break
                else:
                    return json.dumps({
                        "error": f"No release notes found for Chrome {version}",
                        "searched_dir": str(self.release_notes_dir)
                    })
            
            # Process the file
            result = processor.process_single_file(
                md_file, 
                format_override=format_override
            )
            
            if not result:
                return json.dumps({
                    "error": f"Failed to process release notes for Chrome {version}",
                    "file": str(md_file)
                })
            
            # Extract results
            features = result.get('features', [])
            detected_format = result.get('detected_format', 'unknown')
            
            # Generate organized markdown if requested
            organized_path = None
            if generate_organized and features:
                organized_content = processor.generate_organized_markdown(features, version)
                organized_path = self.output_dir / f"chrome-{version}-enterprise-organized.md"
                organized_path.parent.mkdir(parents=True, exist_ok=True)
                with open(organized_path, 'w', encoding='utf-8') as f:
                    f.write(organized_content)
            
            # Generate YAML output
            yaml_path = self.output_dir / f"chrome-{version}-enterprise.yaml"
            yaml_path.parent.mkdir(parents=True, exist_ok=True)
            processor.save_as_yaml(features, yaml_path, version)
            
            return json.dumps({
                "version": version,
                "detected_format": detected_format,
                "total_features": len(features),
                "categories": list(set(f.get('category', 'Uncategorized') for f in features)),
                "output_files": {
                    "yaml": str(yaml_path),
                    "organized_markdown": str(organized_path) if organized_path else None
                },
                "summary": {
                    "by_category": {
                        cat: len([f for f in features if f.get('category') == cat])
                        for cat in set(f.get('category', 'Uncategorized') for f in features)
                    }
                }
            }, indent=2)
            
        except Exception as e:
            logger.error(f"Error processing enterprise notes: {e}")
            return json.dumps({
                "error": str(e),
                "version": version
            })