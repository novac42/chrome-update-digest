#!/usr/bin/env python3
"""
Merge WebGPU and Graphics content from three potential sources.
This script runs AFTER splitting by heading2 to ensure proper categorization.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
import argparse


@dataclass
class Feature:
    """Represents a feature from release notes."""
    title: str
    content: str
    issue_ids: Set[str]
    source: str
    priority: int  # 1=dedicated, 2=heading2, 3=rendering


class WebGPUGraphicsMerger:
    """Merge WebGPU and Graphics content from multiple sources."""
    
    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize the merger.
        
        Args:
            base_path: Base directory path (defaults to current directory)
        """
        self.base_path = base_path or Path.cwd()
        
        # Define paths
        # Try multiple possible locations for WebGPU notes
        self.dedicated_dirs = [
            self.base_path / "upstream_docs" / "release_notes" / "webgpu",
            self.base_path / "upstream_docs" / "release_notes" / "WebPlatform"  # Current location
        ]
        # Try multiple possible locations for split files
        self.split_dirs = [
            self.base_path / "upstream_docs" / "processed_releasenotes" / "processed_forwebplatform" / "split_by_area",
            self.base_path / "upstream_docs" / "processed_releasenotes" / "processed_forwebplatform" / "split_by_heading"  # Current location
        ]
        self.output_dir = self.base_path / "upstream_docs" / "processed_releasenotes" / "processed_forwebplatform" / "merged" / "graphics-webgpu"
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Version ranges for WebGPU heading2
        self.webgpu_heading2_versions = range(136, 138)  # 136-137
    
    def get_available_sources(self, version: str, channel: str) -> Dict[str, Optional[Path]]:
        """
        Get available source files for a given version.
        
        Args:
            version: Chrome version number
            channel: Release channel (stable, beta, etc.)
            
        Returns:
            Dictionary of source type to file path (None if not found)
        """
        sources = {}
        
        # 1. Check dedicated WebGPU release notes (try multiple locations)
        webgpu_file = None
        for dedicated_dir in self.dedicated_dirs:
            # Try different naming patterns
            patterns = [
                f"chrome-{version}-{channel}.md",
                f"webgpu-{version}.md",  # Current pattern in WebPlatform folder
                f"webgpu-{version}-{channel}.md"
            ]
            for pattern in patterns:
                candidate = dedicated_dir / pattern
                if candidate.exists():
                    webgpu_file = candidate
                    break
            if webgpu_file:
                break
        sources['dedicated_webgpu'] = webgpu_file
        
        # 2. Check WebGPU heading2 split (only for specific versions)
        webgpu_h2_file = None
        if int(version) in self.webgpu_heading2_versions:
            for split_dir in self.split_dirs:
                candidate = split_dir / "webgpu" / f"chrome-{version}-{channel}.md"
                if candidate.exists():
                    webgpu_h2_file = candidate
                    break
                # Try without subdirectory
                candidate = split_dir / f"webgpu-chrome-{version}-{channel}.md"
                if candidate.exists():
                    webgpu_h2_file = candidate
                    break
        sources['webgpu_heading2'] = webgpu_h2_file
        
        # 3. Check Rendering/Graphics split
        rendering_file = None
        for split_dir in self.split_dirs:
            # Try various patterns
            patterns = [
                split_dir / "rendering" / f"chrome-{version}-{channel}.md",
                split_dir / "graphics" / f"chrome-{version}-{channel}.md",
                split_dir / f"rendering-chrome-{version}-{channel}.md",
                split_dir / f"graphics-chrome-{version}-{channel}.md"
            ]
            for candidate in patterns:
                if candidate.exists():
                    rendering_file = candidate
                    break
            if rendering_file:
                break
        sources['rendering_graphics'] = rendering_file
        
        return sources
    
    def extract_issue_ids(self, content: str) -> Set[str]:
        """
        Extract issue IDs from content.
        
        Args:
            content: Markdown content
            
        Returns:
            Set of issue IDs found
        """
        issue_ids = set()
        
        # Match various issue patterns
        patterns = [
            r'\[Issue (\d+)\]',
            r'crbug\.com/(\d+)',
            r'bugs\.chromium\.org/p/chromium/issues/detail\?id=(\d+)',
            r'chromium:(\d+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            issue_ids.update(matches)
        
        return issue_ids
    
    def extract_webgpu_content(self, content: str, source: str) -> str:
        """
        Extract relevant WebGPU content, excluding history sections.
        
        Args:
            content: Raw markdown content
            source: Source identifier
            
        Returns:
            Cleaned content
        """
        if source == 'dedicated_webgpu':
            # Find and remove the "What's New in WebGPU" history section
            history_pattern = r'^##\s+What\'s New in WebGPU.*$'
            match = re.search(history_pattern, content, re.MULTILINE | re.IGNORECASE)
            if match:
                # Keep only content before the history section
                content = content[:match.start()].strip()
            
            # Remove metadata headers and navigation
            lines = content.split('\n')
            cleaned_lines = []
            skip_until_h2 = True
            
            for line in lines:
                # Skip everything until we find the first H2 (##)
                if skip_until_h2:
                    if line.startswith('## ') and not 'What\'s New in WebGPU' in line:
                        skip_until_h2 = False
                        cleaned_lines.append(line)
                    continue
                
                # Skip navigation links and metadata
                if line.strip().startswith('* [') or line.strip().startswith('Published:') or line.strip().startswith('Stay organized'):
                    continue
                if line.strip() in ['![François Beaufort](https://web.dev/images/authors/beaufortfrancois.jpg)', 
                                   'François Beaufort', '[ GitHub ](https://github.com/beaufortfrancois)']:
                    continue
                    
                cleaned_lines.append(line)
            
            content = '\n'.join(cleaned_lines).strip()
        
        return content
    
    def parse_features(self, content: str, source: str, priority: int) -> List[Feature]:
        """
        Parse features from markdown content.
        For dedicated WebGPU, returns the entire content as a single feature.
        For other sources, parses by H3 headers.
        
        Args:
            content: Markdown content
            source: Source identifier
            priority: Source priority (1=highest)
            
        Returns:
            List of parsed features
        """
        # Clean the content first
        content = self.extract_webgpu_content(content, source)
        
        if source == 'dedicated_webgpu' and content:
            # Return the entire content as a single feature for dedicated WebGPU
            # This preserves all the detailed content with proper formatting
            return [Feature(
                title="WebGPU Updates",
                content=content,
                issue_ids=self.extract_issue_ids(content),
                source=source,
                priority=priority
            )]
        
        # For other sources, parse by H3 headers
        features = []
        sections = re.split(r'^###\s+(.+)$', content, flags=re.MULTILINE)
        
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                title = sections[i].strip()
                feature_content = sections[i + 1].strip()
                
                features.append(Feature(
                    title=title,
                    content=feature_content,
                    issue_ids=self.extract_issue_ids(feature_content),
                    source=source,
                    priority=priority
                ))
        
        return features
    
    def deduplicate_features(self, all_features: List[Feature]) -> Tuple[List[Feature], int]:
        """
        Deduplicate features based on title and issue IDs.
        
        Args:
            all_features: List of all features from all sources
            
        Returns:
            Tuple of (deduplicated features, number of duplicates removed)
        """
        seen_issues = {}  # issue_id -> Feature
        seen_titles = {}  # normalized_title -> Feature
        unique_features = []
        duplicates_removed = 0
        
        # Sort by priority (lower number = higher priority)
        all_features.sort(key=lambda f: f.priority)
        
        for feature in all_features:
            is_duplicate = False
            
            # Check for duplicate by issue ID
            for issue_id in feature.issue_ids:
                if issue_id in seen_issues:
                    # Found duplicate - keep the one with higher priority (lower number)
                    existing = seen_issues[issue_id]
                    if feature.priority < existing.priority:
                        # Replace with higher priority version
                        unique_features.remove(existing)
                        unique_features.append(feature)
                        seen_issues[issue_id] = feature
                        # Update title mapping
                        normalized_title = self.normalize_title(feature.title)
                        seen_titles[normalized_title] = feature
                    duplicates_removed += 1
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                # Check for duplicate by title (fuzzy match)
                normalized_title = self.normalize_title(feature.title)
                if normalized_title in seen_titles:
                    # Found duplicate - keep the one with more content
                    existing = seen_titles[normalized_title]
                    if len(feature.content) > len(existing.content):
                        unique_features.remove(existing)
                        unique_features.append(feature)
                        seen_titles[normalized_title] = feature
                        # Update issue mapping
                        for issue_id in feature.issue_ids:
                            seen_issues[issue_id] = feature
                    duplicates_removed += 1
                    is_duplicate = True
            
            if not is_duplicate:
                # New unique feature
                unique_features.append(feature)
                normalized_title = self.normalize_title(feature.title)
                seen_titles[normalized_title] = feature
                for issue_id in feature.issue_ids:
                    seen_issues[issue_id] = feature
        
        return unique_features, duplicates_removed
    
    def normalize_title(self, title: str) -> str:
        """
        Normalize title for fuzzy matching.
        
        Args:
            title: Feature title
            
        Returns:
            Normalized title
        """
        # Remove special characters and normalize whitespace
        normalized = re.sub(r'[^\w\s]', '', title.lower())
        normalized = ' '.join(normalized.split())
        return normalized
    
    def generate_merged_content(self, features: List[Feature], version: str, channel: str,
                              sources_used: List[str]) -> str:
        """
        Generate merged markdown content.
        
        Args:
            features: List of features
            version: Chrome version
            channel: Release channel
            sources_used: List of sources that were used
            
        Returns:
            Merged markdown content
        """
        lines = []
        
        # Header
        lines.append(f"# Graphics and WebGPU - Chrome {version} {channel.title()}")
        lines.append("")
        
        if not features:
            lines.append("*No WebGPU or Graphics content available for this version.*")
            return '\n'.join(lines)
        
        # Group features by source
        rendering_features = [f for f in features if f.source == 'rendering_graphics']
        dedicated_features = [f for f in features if f.source == 'dedicated_webgpu']
        heading2_features = [f for f in features if f.source == 'webgpu_heading2']
        
        # Add Rendering and Graphics section
        if rendering_features:
            lines.append("## Rendering and Graphics")
            lines.append("")
            for feature in rendering_features:
                lines.append(f"### {feature.title}")
                lines.append(feature.content)
                lines.append("")
        
        # Add WebGPU Features section
        if dedicated_features or heading2_features:
            lines.append("## WebGPU Features")
            lines.append("")
            
            # For dedicated features, just add the content directly
            # since it's already complete with H2 sections
            if dedicated_features:
                for feature in dedicated_features:
                    # The content already has proper formatting
                    lines.append(feature.content)
                    lines.append("")
            
            if heading2_features:
                lines.append("### From Chrome Release Notes")
                lines.append("")
                for feature in heading2_features:
                    lines.append(f"#### {feature.title}")
                    lines.append(feature.content)
                    lines.append("")
        
        # Add metadata footer
        lines.append("---")
        lines.append(f"*Generated from {len(sources_used)} source(s): {', '.join(sources_used)}*")
        
        return '\n'.join(lines)
    
    def merge(self, version: str, channel: str = "stable") -> Dict:
        """
        Merge WebGPU and Graphics content for a specific version.
        
        Args:
            version: Chrome version number
            channel: Release channel
            
        Returns:
            Dictionary with merge results
        """
        print(f"\nMerging WebGPU and Graphics content for Chrome {version} {channel}...")
        
        # Get available sources
        sources = self.get_available_sources(version, channel)
        available_sources = {k: v for k, v in sources.items() if v is not None}
        
        if not available_sources:
            print(f"No sources found for Chrome {version} {channel}")
            # Create placeholder file
            output_file = self.output_dir / f"chrome-{version}-{channel}.md"
            placeholder_content = f"""# Graphics and WebGPU - Chrome {version} {channel.title()}

*No WebGPU or Graphics content available for this version.*
"""
            output_file.write_text(placeholder_content)
            return {
                'success': True,
                'sources_used': [],
                'features_total': 0,
                'features_deduplicated': 0,
                'output_file': str(output_file)
            }
        
        print(f"Found {len(available_sources)} source(s): {', '.join(available_sources.keys())}")
        
        # Load and parse features from each source
        all_features = []
        
        # Priority 1: Dedicated WebGPU
        if 'dedicated_webgpu' in available_sources:
            content = available_sources['dedicated_webgpu'].read_text()
            features = self.parse_features(content, 'dedicated_webgpu', priority=1)
            all_features.extend(features)
            print(f"  - Loaded {len(features)} features from dedicated WebGPU notes")
        
        # Priority 2: WebGPU heading2
        if 'webgpu_heading2' in available_sources:
            content = available_sources['webgpu_heading2'].read_text()
            features = self.parse_features(content, 'webgpu_heading2', priority=2)
            all_features.extend(features)
            print(f"  - Loaded {len(features)} features from WebGPU heading2 split")
        
        # Priority 3: Rendering/Graphics
        if 'rendering_graphics' in available_sources:
            content = available_sources['rendering_graphics'].read_text()
            features = self.parse_features(content, 'rendering_graphics', priority=3)
            all_features.extend(features)
            print(f"  - Loaded {len(features)} features from Rendering/Graphics split")
        
        # No deduplication here - will be handled in YAML generation
        unique_features = all_features
        duplicates_removed = 0
        print(f"Total features: {len(unique_features)}")
        
        # Generate merged content
        merged_content = self.generate_merged_content(
            unique_features, version, channel, list(available_sources.keys())
        )
        
        # Write output
        output_file = self.output_dir / f"chrome-{version}-{channel}.md"
        output_file.write_text(merged_content)
        print(f"Wrote merged content to {output_file}")
        
        return {
            'success': True,
            'sources_used': list(available_sources.keys()),
            'features_total': len(unique_features),
            'features_deduplicated': duplicates_removed,
            'output_file': str(output_file)
        }


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Merge WebGPU and Graphics content from multiple sources'
    )
    parser.add_argument('--version', help='Chrome version number (required unless --batch)')
    parser.add_argument('--channel', default='stable', help='Release channel (default: stable)')
    parser.add_argument('--batch', action='store_true', help='Process multiple versions (124-139)')
    
    args = parser.parse_args()
    
    if not args.batch and not args.version:
        parser.error("--version is required unless --batch is specified")
    
    merger = WebGPUGraphicsMerger()
    
    if args.batch:
        # Process multiple versions
        versions = range(124, 140)
        results = []
        for version in versions:
            result = merger.merge(str(version), args.channel)
            results.append(result)
        
        # Summary
        print("\n" + "="*60)
        print("Batch Processing Summary")
        print("="*60)
        successful = sum(1 for r in results if r['success'])
        total_features = sum(r['features_total'] for r in results)
        total_dedup = sum(r['features_deduplicated'] for r in results)
        print(f"Processed {successful}/{len(versions)} versions successfully")
        print(f"Total features: {total_features}")
        print(f"Total deduplicated: {total_dedup}")
    else:
        # Process single version
        result = merger.merge(args.version, args.channel)
        if result['success']:
            print(f"\n✅ Successfully merged Chrome {args.version} {args.channel}")
            print(f"   Sources used: {', '.join(result['sources_used'])}")
            print(f"   Features: {result['features_total']} (deduplicated: {result['features_deduplicated']})")
        else:
            print(f"\n❌ Failed to merge Chrome {args.version} {args.channel}")
            sys.exit(1)


if __name__ == '__main__':
    main()