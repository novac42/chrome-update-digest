#!/usr/bin/env python3
"""
DEPRECATED: This legacy pipeline has been replaced by clean_data_pipeline.py

This file is deprecated and should not be used for new development.
Use src/processors/clean_data_pipeline.py instead, which provides:
- Configuration-driven area mapping via config/focus_areas.yaml
- Smart area classification with fallback to original headings
- Improved WebGPU deduplication logic
- Better support for new focus areas (payment, devtools, etc.)

Legacy description:
Improved pipeline that splits Chrome release notes by heading2 before processing.
This ensures accurate categorization and prevents mixing of different feature areas.
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.yaml_pipeline import YAMLPipeline
from processors.merge_webgpu_graphics import WebGPUGraphicsMerger


class ReleaseNoteSplitter:
    """
    DEPRECATED: Split Chrome release notes by heading2 sections.
    
    Use clean_data_pipeline.py instead for improved area classification.
    """
    
    def __init__(self):
        print("WARNING: split_and_process_release_notes.py is DEPRECATED!")
        print("Please use clean_data_pipeline.py for better area classification and configuration management.")
        print("See CLAUDE.md for migration guidance.")
        self.section_mappings = {
            'css': ['CSS and UI', 'CSS'],
            'webapi': ['Web APIs'],
            'graphics': ['Graphics'],  # Will be replaced with WebGPU merge
            'webgpu': ['WebGPU'],
            'javascript': ['JavaScript'],
            'security': ['Security', 'Privacy and security'],
            'performance': ['Performance'],
            'multimedia': ['Multimedia', 'Images and media'],
            'devices': ['Devices'],
            'html-dom': ['HTML and DOM'],
            'service-worker': ['Service Worker'],
            'webassembly': ['WebAssembly'],
            'identity': ['Identity'],
            'payments': ['Payments'],
            'enterprise': ['Enterprise'],
            'browser': ['Browser changes'],
            'trials': ['Origin trials', 'New origin trials'],
            'deprecations': ['Deprecations and removals']
        }
    
    def split_by_heading2(self, markdown_content: str, version: str = None, channel: str = 'stable', save_files: bool = False) -> Dict[str, str]:
        """
        Split markdown content by heading2 (##) sections and optionally save to files.
        
        Args:
            markdown_content: Full Chrome release notes content
            version: Chrome version number (required if save_files=True)
            channel: Release channel (default: 'stable')
            save_files: Whether to save each section to individual files
            
        Returns:
            Dictionary mapping section names to their content
        """
        lines = markdown_content.split('\n')
        sections = {}
        current_section = 'header'
        current_content = []
        header_content = []
        
        # Create output directory if saving files
        if save_files:
            output_dir = Path(__file__).parent.parent.parent / 'upstream_docs' / 'processed_releasenotes' / 'processed_forwebplatform' / 'split_by_heading'
            output_dir.mkdir(parents=True, exist_ok=True)
        
        for line in lines:
            if line.startswith('## '):
                # Save previous section
                if current_section == 'header':
                    header_content = current_content
                elif current_content:
                    section_name = current_section.strip()
                    content = '\n'.join(current_content)
                    sections[section_name] = content
                    
                    # Save to file if requested
                    if save_files and version:
                        self._save_section_to_file(section_name, content, version, channel, output_dir)
                
                # Start new section
                current_section = line[3:].strip()
                current_content = [line]
            else:
                current_content.append(line)
        
        # Save last section
        if current_section != 'header' and current_content:
            section_name = current_section.strip()
            content = '\n'.join(current_content)
            sections[section_name] = content
            
            # Save to file if requested
            if save_files and version:
                self._save_section_to_file(section_name, content, version, channel, output_dir)
        
        # Store header for reconstruction
        sections['_header'] = '\n'.join(header_content)
        
        return sections
    
    def _save_section_to_file(self, section_name: str, content: str, version: str, channel: str, output_dir: Path):
        """
        Save a section to its own markdown file.
        
        Args:
            section_name: Name of the section (from heading2)
            content: Section content
            version: Chrome version
            channel: Release channel
            output_dir: Directory to save files
        """
        # Normalize section name for filename
        filename_base = section_name.lower().replace(' ', '-').replace('/', '-').replace(':', '')
        filename = f"{filename_base}-chrome-{version}-{channel}.md"
        
        filepath = output_dir / filename
        filepath.write_text(content, encoding='utf-8')
        print(f"    Saved section: {filepath.name}")
    
    def merge_webgpu_section(self, chrome_webgpu_section: Optional[str], 
                           webgpu_release_notes: str, version: str) -> str:
        """
        DEPRECATED: Use merge_webgpu_graphics.py instead.
        This method is kept for backward compatibility but should not be used.
        The new approach splits first, then merges WebGPU with Graphics content.
        
        Args:
            chrome_webgpu_section: WebGPU section from Chrome notes (may be None)
            webgpu_release_notes: Dedicated WebGPU release notes
            version: Chrome version
            
        Returns:
            Merged WebGPU content
        """
        # Extract only actual WebGPU features from dedicated notes
        webgpu_features = self._extract_webgpu_features(webgpu_release_notes)
        
        if not webgpu_features:
            # No additional WebGPU features, return Chrome section as-is
            return chrome_webgpu_section or ""
        
        if not chrome_webgpu_section:
            # No Chrome WebGPU section, create one with WebGPU features
            return f"## WebGPU\n\n{webgpu_features}"
        
        # Merge: add WebGPU features after Chrome's WebGPU content
        lines = chrome_webgpu_section.split('\n')
        merged = []
        
        # Keep Chrome's WebGPU section
        merged.extend(lines)
        
        # Add separator and additional WebGPU features
        merged.append("")
        merged.append("### Additional WebGPU Updates")
        merged.append("")
        merged.extend(webgpu_features.split('\n'))
        
        return '\n'.join(merged)
    
    def _extract_webgpu_features(self, webgpu_content: str) -> str:
        """
        Extract only actual WebGPU feature sections from WebGPU release notes.
        Excludes Origin trials, Deprecations, and other non-WebGPU sections.
        
        Args:
            webgpu_content: Full WebGPU release notes
            
        Returns:
            Only WebGPU-specific features
        """
        lines = webgpu_content.split('\n')
        feature_lines = []
        in_feature = False
        skip_section = False
        
        for line in lines:
            # Skip main title
            if line.startswith('# What\'s New in WebGPU') or line.startswith('# WebGPU'):
                continue
            
            # Check for sections to skip
            if line.startswith('## '):
                section_name = line[3:].strip().lower()
                # Skip these sections as they're not WebGPU-specific
                skip_patterns = [
                    'origin trial', 'deprecation', 'removal', 
                    'what\'s new in webgpu',  # Version history
                    'chrome 1'  # Version references
                ]
                skip_section = any(pattern in section_name for pattern in skip_patterns)
                
                # Dawn updates are WebGPU-specific
                if 'dawn' in section_name:
                    skip_section = False
                    in_feature = True
                elif not skip_section:
                    in_feature = True
                else:
                    in_feature = False
            
            # Add line if we're in a valid feature section
            if in_feature and not skip_section:
                # Demote heading levels for merging
                if line.startswith('## '):
                    feature_lines.append('### ' + line[3:])
                elif line.startswith('### '):
                    feature_lines.append('#### ' + line[4:])
                elif line.startswith('#### '):
                    feature_lines.append('##### ' + line[5:])
                else:
                    feature_lines.append(line)
        
        # Remove trailing empty lines
        while feature_lines and not feature_lines[-1].strip():
            feature_lines.pop()
        
        return '\n'.join(feature_lines)
    
    def reconstruct_with_sections(self, sections: Dict[str, str]) -> str:
        """
        Reconstruct the full markdown from sections.
        
        Args:
            sections: Dictionary of section names to content
            
        Returns:
            Reconstructed markdown content
        """
        lines = []
        
        # Add header if present
        if '_header' in sections:
            lines.append(sections['_header'])
        
        # Add sections in a logical order
        section_order = [
            'CSS and UI', 'CSS',
            'HTML and DOM',
            'JavaScript',
            'Web APIs',
            'Graphics', 'WebGPU',
            'WebAssembly',
            'Multimedia', 'Images and media',
            'Devices',
            'Performance',
            'Security', 'Privacy and security',
            'Service Worker',
            'Identity',
            'Payments',
            'Enterprise',
            'Browser changes',
            'Origin trials', 'New origin trials',
            'Deprecations and removals'
        ]
        
        added_sections = set()
        for section_name in section_order:
            if section_name in sections and section_name not in added_sections:
                lines.append(sections[section_name])
                added_sections.add(section_name)
        
        # Add any remaining sections not in the order
        for section_name, content in sections.items():
            if section_name not in added_sections and not section_name.startswith('_'):
                lines.append(content)
        
        return '\n'.join(lines)


def process_with_split_pipeline(version: str):
    """
    Process Chrome release notes with the improved split pipeline.
    
    Args:
        version: Chrome version to process
    """
    print(f"Processing Chrome {version} with split pipeline...")
    
    # Paths
    chrome_file = Path(f'upstream_docs/release_notes/WebPlatform/chrome-{version}.md')
    webgpu_file = Path(f'upstream_docs/release_notes/WebPlatform/webgpu-{version}.md')
    output_dir = Path('upstream_docs/processed_releasenotes/processed_forwebplatform')
    
    # Read Chrome release notes
    if not chrome_file.exists():
        print(f"  ❌ Chrome release notes not found: {chrome_file}")
        return False
    
    with open(chrome_file, 'r', encoding='utf-8') as f:
        chrome_content = f.read()
    
    # Initialize splitter and pipeline
    splitter = ReleaseNoteSplitter()
    pipeline = YAMLPipeline()
    
    # Step 1: Split Chrome notes by heading2 and save each section
    sections = splitter.split_by_heading2(chrome_content, version=version, channel='stable', save_files=True)
    print(f"  ✓ Split into {len(sections)} sections and saved to processed_forwebplatform/split_by_heading/")
    
    # Step 2: Run WebGPU-Graphics merger AFTER splitting
    # This merges dedicated WebGPU notes with split Graphics/WebGPU sections
    merger = WebGPUGraphicsMerger()
    merge_result = merger.merge(version, 'stable')
    if merge_result['success']:
        print(f"  ✓ Merged WebGPU and Graphics content")
        print(f"    Sources used: {', '.join(merge_result['sources_used'])}")
        print(f"    Features: {merge_result['features_total']} (deduplicated: {merge_result['features_deduplicated']})")
    else:
        print(f"  ⚠️  WebGPU-Graphics merge skipped (no sources found)")
    
    # Step 3: Process with YAML pipeline
    # For graphics-webgpu, use the merged file; for others, use original content
    result = pipeline.process_release_notes(
        markdown_content=chrome_content,  # Original content
        version=version,
        channel='stable',
        save_yaml=True,
        split_by_area=True,
        merge_webgpu=False,  # Don't merge in pipeline, already done by merger
        merged_graphics_webgpu_path=merge_result.get('output_file') if merge_result['success'] else None
    )
    
    print(f"  ✓ Generated YAML files")
    print(f"    Total features: {result['statistics']['total_features']}")
    
    # Check WebGPU area
    webgpu_yaml = output_dir / 'graphics-webgpu' / f'chrome-{version}-stable.yml'
    if webgpu_yaml.exists():
        with open(webgpu_yaml, 'r') as f:
            data = yaml.safe_load(f)
        print(f"    WebGPU features: {len(data.get('features', []))}")
    
    return True


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Process Chrome release notes with split pipeline"
    )
    parser.add_argument(
        "--version", 
        required=True, 
        help="Chrome version to process"
    )
    
    args = parser.parse_args()
    
    success = process_with_split_pipeline(args.version)
    
    if success:
        print(f"\n✅ Successfully processed Chrome {args.version}")
    else:
        print(f"\n❌ Failed to process Chrome {args.version}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())