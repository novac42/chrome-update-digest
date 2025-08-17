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
    
    def extract_webgpu_features(self, webgpu_content: str) -> List[str]:
        """
        Extract only the actual WebGPU feature sections from the WebGPU release notes.
        
        Returns:
            List of feature sections as strings
        """
        lines = webgpu_content.split('\n')
        features = []
        current_feature = []
        in_feature = False
        skip_sections = ['What\'s New in WebGPU', 'WebGPU 139 Release Notes', 'WebGPU 138 Release Notes', 'WebGPU 137 Release Notes']
        
        for line in lines:
            # Check if this is a H2 header
            if line.startswith('## '):
                # Check if we should skip this section
                if any(skip in line for skip in skip_sections):
                    in_feature = False
                    current_feature = []
                    continue
                
                # Save previous feature if exists
                if current_feature and in_feature:
                    features.append('\n'.join(current_feature))
                
                # Start new feature
                current_feature = ['### ' + line[3:]]  # Convert H2 to H3
                in_feature = True
            
            # Check for H3 headers (demote to H4)
            elif line.startswith('### ') and in_feature:
                current_feature.append('#### ' + line[4:])
            
            # Add content if we're in a feature section
            elif in_feature:
                current_feature.append(line)
        
        # Don't forget the last feature
        if current_feature and in_feature:
            features.append('\n'.join(current_feature))
        
        # Filter out empty or whitespace-only features
        features = [f.strip() for f in features if f.strip()]
        
        return features
    
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
        
        # Extract WebGPU features
        webgpu_features = self.extract_webgpu_features(webgpu_content)
        
        if not webgpu_features:
            print(f"  No WebGPU features found to merge")
            return chrome_content
        
        print(f"  Found {len(webgpu_features)} WebGPU features to merge")
        
        # Find where to insert WebGPU content
        chrome_lines = chrome_content.split('\n')
        merged_lines = []
        webgpu_inserted = False
        
        i = 0
        while i < len(chrome_lines):
            line = chrome_lines[i]
            
            # Look for Graphics section or WebGPU mentions
            if line.startswith('## Graphics') or (line.startswith('### ') and 'WebGPU' in line):
                # Add the Graphics header
                merged_lines.append(line)
                merged_lines.append("")
                
                # Skip to next line
                i += 1
                
                # Collect existing Graphics content until next H2
                while i < len(chrome_lines) and not chrome_lines[i].startswith('## '):
                    merged_lines.append(chrome_lines[i])
                    i += 1
                
                # Now add the WebGPU features
                if not webgpu_inserted:
                    merged_lines.append("")
                    merged_lines.append("### Additional WebGPU Updates")
                    merged_lines.append("")
                    merged_lines.append("*The following WebGPU features and updates are included in this release:*")
                    merged_lines.append("")
                    
                    for feature in webgpu_features:
                        merged_lines.append(feature)
                        merged_lines.append("")
                    
                    webgpu_inserted = True
                
                # Don't increment i since we're at the next section
                continue
            else:
                merged_lines.append(line)
                i += 1
        
        # If no Graphics section was found, add WebGPU as its own section
        if not webgpu_inserted:
            # Find a good insertion point
            insert_index = len(merged_lines)
            
            for idx, line in enumerate(merged_lines):
                if line.startswith('## ') and any(keyword in line.lower() for keyword in ['deprecation', 'removal', 'origin trial']):
                    insert_index = idx
                    break
            
            # Insert WebGPU section
            webgpu_section = [
                "## WebGPU",
                "",
                "*WebGPU updates for this release:*",
                ""
            ]
            
            for feature in webgpu_features:
                webgpu_section.append(feature)
                webgpu_section.append("")
            
            merged_lines[insert_index:insert_index] = webgpu_section
        
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


def extract_webgpu_features(webgpu_content: str) -> List[str]:
    """
    Extract only the actual WebGPU feature sections from the WebGPU release notes.
    Standalone function version for import.
    
    Returns:
        List of feature sections as strings
    """
    lines = webgpu_content.split('\n')
    features = []
    current_feature = []
    in_feature = False
    skip_sections = ['What\'s New in WebGPU', 'WebGPU 139 Release Notes', 'WebGPU 138 Release Notes', 'WebGPU 137 Release Notes']
    
    for line in lines:
        # Check if this is a H2 header
        if line.startswith('## '):
            # Check if we should skip this section
            if any(skip in line for skip in skip_sections):
                in_feature = False
                current_feature = []
                continue
            
            # Save previous feature if exists
            if current_feature and in_feature:
                features.append('\n'.join(current_feature))
            
            # Start new feature
            current_feature = ['### ' + line[3:]]  # Convert H2 to H3
            in_feature = True
        
        # Check for H3 headers (demote to H4)
        elif line.startswith('### ') and in_feature:
            current_feature.append('#### ' + line[4:])
        
        # Add content if we're in a feature section
        elif in_feature:
            current_feature.append(line)
    
    # Don't forget the last feature
    if current_feature and in_feature:
        features.append('\n'.join(current_feature))
    
    # Filter out empty or whitespace-only features
    features = [f.strip() for f in features if f.strip()]
    
    return features


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