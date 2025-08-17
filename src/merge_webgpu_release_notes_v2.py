#!/usr/bin/env python3
"""
Improved WebGPU merge script that only extracts actual WebGPU features.
"""

import os
import re
import argparse
from pathlib import Path
from typing import List, Optional


class WebGPUMergerV2:
    """Improved merger that only extracts WebGPU feature sections."""
    
    def __init__(self, upstream_docs_dir: str):
        self.upstream_docs_dir = Path(upstream_docs_dir)
        self.release_notes_dir = self.upstream_docs_dir / "release_notes" / "WebPlatform"
        self.output_dir = self.upstream_docs_dir / "processed_releasenotes" / "processed_forwebplatform"
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def clean_and_process_webgpu_content(self, webgpu_content: str) -> str:
        """
        Clean WebGPU content by removing header and footer sections,
        then adjust heading levels.
        
        Returns:
            Cleaned and processed WebGPU content as string
        """
        lines = webgpu_content.split('\n')
        cleaned_lines = []
        in_content = False
        skip_next_empty = False
        
        for i, line in enumerate(lines):
            # Skip the main title line - handles both patterns:
            # "# What's New in WebGPU" and "# WebGPU XXX Release Notes"
            if line.startswith('# What\'s New in WebGPU') or (line.startswith('# WebGPU') and 'Release Notes' in line):
                in_content = True
                skip_next_empty = True  # Skip the empty line after title
                continue
            
            # Skip one empty line after the title
            if skip_next_empty and not line.strip():
                skip_next_empty = False
                continue
            
            # Skip source and navigation lines
            if in_content and (line.startswith('Source:') or '* [' in line and 'Chrome for Developers' in line):
                continue
            
            # Stop capturing when we hit the version history section (at the end of some files)
            # This section lists previous Chrome versions
            if line.strip() == '## What\'s New in WebGPU' or 'Chrome 1' in line and '##' in line:
                break
            
            # Add lines if we're in the content section
            if in_content:
                cleaned_lines.append(line)
        
        # Now process the cleaned content to adjust heading levels
        processed_lines = []
        
        for line in cleaned_lines:
            # Skip empty lines at the beginning
            if not processed_lines and not line.strip():
                continue
                
            # Demote all headings by one level
            if line.startswith('## '):
                processed_lines.append('### ' + line[3:])
            elif line.startswith('### '):
                processed_lines.append('#### ' + line[4:])
            elif line.startswith('#### '):
                processed_lines.append('##### ' + line[5:])
            elif line.startswith('##### '):
                processed_lines.append('###### ' + line[6:])
            else:
                processed_lines.append(line)
        
        # Remove trailing empty lines
        while processed_lines and not processed_lines[-1].strip():
            processed_lines.pop()
        
        return '\n'.join(processed_lines)
    
    def merge_release_notes(self, version: str) -> Optional[str]:
        """
        Merge Chrome and WebGPU release notes for a specific version.
        
        Args:
            version: Version number (e.g., "139")
            
        Returns:
            Merged content as string, or None if failed
        """
        chrome_file = self.release_notes_dir / f"chrome-{version}.md"
        webgpu_file = self.release_notes_dir / f"webgpu-{version}.md"
        
        print(f"Processing version {version}...")
        print(f"  Chrome file: {chrome_file}")
        print(f"  WebGPU file: {webgpu_file}")
        
        # Read Chrome content
        try:
            with open(chrome_file, 'r', encoding='utf-8') as f:
                chrome_content = f.read()
        except Exception as e:
            print(f"  Error reading Chrome file: {e}")
            return None
        
        # Check if WebGPU file exists
        if not webgpu_file.exists():
            print(f"  No WebGPU file found, returning Chrome content as-is")
            return chrome_content
        
        # Read WebGPU content
        try:
            with open(webgpu_file, 'r', encoding='utf-8') as f:
                webgpu_content = f.read()
        except Exception as e:
            print(f"  Error reading WebGPU file: {e}")
            return chrome_content
        
        # Clean and process WebGPU content
        processed_webgpu = self.clean_and_process_webgpu_content(webgpu_content)
        
        if not processed_webgpu.strip():
            print(f"  No WebGPU content found after cleaning")
            return chrome_content
        
        print(f"  WebGPU content processed successfully")
        
        # Find where to insert WebGPU content
        chrome_lines = chrome_content.split('\n')
        merged_lines = []
        webgpu_inserted = False
        
        i = 0
        while i < len(chrome_lines):
            line = chrome_lines[i]
            
            # Look for a good insertion point - before Origin trials or Deprecations
            if not webgpu_inserted and line.startswith('## ') and any(keyword in line.lower() for keyword in ['origin trial', 'deprecation', 'removal']):
                # Insert WebGPU section before this section
                merged_lines.append("## WebGPU")
                merged_lines.append("")
                merged_lines.extend(processed_webgpu.split('\n'))
                merged_lines.append("")
                webgpu_inserted = True
            
            merged_lines.append(line)
            i += 1
        
        # If no suitable insertion point was found, add at the end
        if not webgpu_inserted:
            merged_lines.append("")
            merged_lines.append("## WebGPU")
            merged_lines.append("")
            merged_lines.extend(processed_webgpu.split('\n'))
            merged_lines.append("")
        
        return '\n'.join(merged_lines)
    
    def save_merged_content(self, version: str, content: str) -> bool:
        """Save merged content to output directory."""
        output_file = self.output_dir / f"{version}-merged-webgpu.md"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Saved to: {output_file}")
            return True
        except Exception as e:
            print(f"  Error saving to {output_file}: {e}")
            return False


def clean_and_process_webgpu_content_standalone(webgpu_content: str) -> str:
    """
    Clean WebGPU content by removing header and footer sections,
    then adjust heading levels.
    Standalone function version for import.
    
    Returns:
        Cleaned and processed WebGPU content as string
    """
    lines = webgpu_content.split('\n')
    cleaned_lines = []
    in_content = False
    
    for i, line in enumerate(lines):
        # Start capturing after we see "Published:"
        if 'Published:' in line and not in_content:
            in_content = True
            continue
        
        # Stop capturing when we hit the version history section
        if line.strip() == '## What\'s New in WebGPU':
            break
        
        # Add lines if we're in the content section
        if in_content:
            cleaned_lines.append(line)
    
    # Now process the cleaned content to adjust heading levels
    processed_lines = []
    
    for line in cleaned_lines:
        # Skip empty lines at the beginning
        if not processed_lines and not line.strip():
            continue
            
        # Demote all headings by one level
        if line.startswith('## '):
            processed_lines.append('### ' + line[3:])
        elif line.startswith('### '):
            processed_lines.append('#### ' + line[4:])
        elif line.startswith('#### '):
            processed_lines.append('##### ' + line[5:])
        elif line.startswith('##### '):
            processed_lines.append('###### ' + line[6:])
        else:
            processed_lines.append(line)
    
    # Remove trailing empty lines
    while processed_lines and not processed_lines[-1].strip():
        processed_lines.pop()
    
    return '\n'.join(processed_lines)


def merge_webgpu_notes(version: str) -> Optional[str]:
    """
    Merge Chrome and WebGPU release notes for a specific version.
    Standalone function version for import.
    
    Args:
        version: Version number (e.g., "139")
        
    Returns:
        Merged content as string, or None if failed
    """
    merger = WebGPUMergerV2('upstream_docs')
    return merger.merge_release_notes(version)


# Backward compatibility alias
def extract_webgpu_features(webgpu_content: str) -> List[str]:
    """
    Legacy function - now returns processed content as a single-item list.
    For backward compatibility only.
    """
    processed = clean_and_process_webgpu_content_standalone(webgpu_content)
    if processed:
        return [processed]
    return []


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Merge WebGPU release notes with Chrome release notes (improved version)")
    parser.add_argument("--upstream-docs", 
                       default="upstream_docs",
                       help="Path to upstream_docs directory")
    parser.add_argument("--version", 
                       required=True,
                       help="Chrome version to process")
    
    args = parser.parse_args()
    
    merger = WebGPUMergerV2(args.upstream_docs)
    
    # Process the version
    merged_content = merger.merge_release_notes(args.version)
    
    if merged_content:
        success = merger.save_merged_content(args.version, merged_content)
        if success:
            print(f"Successfully merged WebGPU for Chrome {args.version}")
            return 0
        else:
            print(f"Failed to save merged content for Chrome {args.version}")
            return 1
    else:
        print(f"Failed to merge WebGPU for Chrome {args.version}")
        return 1


if __name__ == "__main__":
    exit(main())