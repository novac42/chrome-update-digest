"""
Enterprise Release Notes Processor Tool
Processes Chrome Enterprise release notes with format auto-detection
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
from fastmcp import Context
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from process_enterprise_release_note import (
    ReleaseNotesProcessorV2,
    ReleaseNotesFormatDetector,
    Feature
)


async def process_enterprise_release(
    ctx: Context, 
    version: str, 
    format_override: Optional[str] = None
) -> Dict:
    """
    Process Chrome Enterprise release notes for a specific version.
    
    Args:
        ctx: FastMCP context
        version: Chrome version number (e.g., "137", "138")
        format_override: Optional format to force ("current" or "history")
    
    Returns:
        Dictionary with processing results
    """
    try:
        # Set up paths
        base_path = Path(__file__).parent.parent.parent
        release_notes_dir = base_path / "upstream_docs" / "release_notes" / "Enterprise"
        processed_dir = base_path / "upstream_docs" / "processed_releasenotes" / "processed_forenterprise"
        
        # Ensure output directory exists
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Find the release file
        input_file = None
        patterns = [
            f"{version}-chrome-enterprise.md",
            f"{version}_chrome_enterprise.md",
            f"*{version}*chrome*enterprise*.md"
        ]
        
        for pattern in patterns:
            matches = list(release_notes_dir.glob(pattern))
            if matches:
                input_file = matches[0]
                break
        
        if not input_file:
            return {
                "success": False,
                "error": f"Could not find release notes for Chrome {version}",
                "version": version
            }
        
        # Create processor and process the file
        processor = ReleaseNotesProcessorV2()
        
        # Apply format override if specified
        if format_override:
            processor.detected_format = format_override
        
        # Process the release notes
        processor.process_release_notes(str(input_file))
        
        # Generate organized output
        organized_content = processor.generate_organized_output()
        
        # Write output file
        output_file = processed_dir / f"{version}-organized_chromechanges-enterprise.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(organized_content)
        
        # Prepare summary
        feature_summary = {
            "total": len(processor.features),
            "by_status": {
                "current": sum(1 for f in processor.features.values() if f.status == "current"),
                "upcoming": sum(1 for f in processor.features.values() if f.status == "upcoming")
            },
            "by_category": {}
        }
        
        # Count features by category
        for feature in processor.features.values():
            for category in feature.categories:
                if category not in feature_summary["by_category"]:
                    feature_summary["by_category"][category] = 0
                feature_summary["by_category"][category] += 1
        
        return {
            "success": True,
            "version": version,
            "detected_format": processor.detected_format,
            "features_processed": feature_summary,
            "input_file": str(input_file.name),
            "output_file": str(output_file.name),
            "output_path": str(output_file)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "version": version
        }


async def list_unprocessed_enterprise_versions(ctx: Context) -> Dict:
    """
    List all unprocessed Chrome Enterprise versions.
    
    Returns:
        Dictionary with unprocessed versions and their status
    """
    try:
        base_path = Path(__file__).parent.parent.parent
        release_notes_dir = base_path / "upstream_docs" / "release_notes" / "Enterprise"
        processed_dir = base_path / "upstream_docs" / "processed_releasenotes" / "processed_forenterprise"
        
        # Find all release note files and extract versions
        release_versions = set()
        for file in release_notes_dir.glob("*.md"):
            match = re.search(r'(\d+)[-_]chrome[-_]enterprise', file.name, re.IGNORECASE)
            if match:
                release_versions.add(int(match.group(1)))
        
        # Find already processed versions
        processed_versions = set()
        for file in processed_dir.glob("*-organized_chromechanges-enterprise.md"):
            match = re.search(r'^(\d+)-organized_chromechanges-enterprise\.md$', file.name)
            if match:
                processed_versions.add(int(match.group(1)))
        
        unprocessed = sorted(release_versions - processed_versions)
        
        return {
            "success": True,
            "all_versions": sorted(release_versions),
            "processed_versions": sorted(processed_versions),
            "unprocessed_versions": unprocessed,
            "total_unprocessed": len(unprocessed)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def analyze_enterprise_features(ctx: Context, version: str) -> Dict:
    """
    Analyze features in a Chrome Enterprise release without processing.
    
    Args:
        ctx: FastMCP context
        version: Chrome version number
    
    Returns:
        Dictionary with feature analysis
    """
    try:
        base_path = Path(__file__).parent.parent.parent
        release_notes_dir = base_path / "upstream_docs" / "release_notes" / "Enterprise"
        
        # Find the release file
        input_file = None
        patterns = [
            f"{version}-chrome-enterprise.md",
            f"{version}_chrome_enterprise.md",
            f"*{version}*chrome*enterprise*.md"
        ]
        
        for pattern in patterns:
            matches = list(release_notes_dir.glob(pattern))
            if matches:
                input_file = matches[0]
                break
        
        if not input_file:
            return {
                "success": False,
                "error": f"Could not find release notes for Chrome {version}",
                "version": version
            }
        
        # Read and detect format
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        detector = ReleaseNotesFormatDetector()
        detected_format = detector.detect_format(content)
        
        # Quick analysis without full processing
        feature_count = len(re.findall(r'^###\s+[^#]', content, re.MULTILINE))
        has_upcoming = bool(re.search(r'\b(upcoming|coming soon)\b', content, re.IGNORECASE))
        
        # Extract section headers
        sections = []
        for match in re.finditer(r'^##\s+([^#\n]+)', content, re.MULTILINE):
            sections.append(match.group(1).strip())
        
        return {
            "success": True,
            "version": version,
            "detected_format": detected_format,
            "file": str(input_file.name),
            "estimated_features": feature_count,
            "has_upcoming_section": has_upcoming,
            "sections": sections
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "version": version
        }