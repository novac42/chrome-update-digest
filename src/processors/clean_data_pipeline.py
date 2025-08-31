#!/usr/bin/env python3
"""
Clean data pipeline for WebPlatform release notes.
Simple, robust, and structure-based extraction.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
import yaml
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class Section:
    """Represents a document section."""
    title: str
    level: int  # 2=h2, 3=h3, etc.
    content: str  # Full content including the header
    start_line: int
    end_line: int
    features: List['Section'] = field(default_factory=list)  # h3 features under h2


class CleanDataPipeline:
    """
    Clean, structure-based data extraction pipeline.
    """
    
    def __init__(self, focus_areas_config_path: Optional[Path] = None):
        """Initialize with expected areas for validation."""
        # Load focus areas configuration
        if not focus_areas_config_path:
            focus_areas_config_path = Path(__file__).parent.parent.parent / 'config' / 'focus_areas.yaml'
        
        self.focus_areas_config = self._load_focus_areas_config(focus_areas_config_path)
        
        # Core areas that should exist in Chrome release notes (for validation)
        self.expected_areas = {
            'CSS', 'Web APIs', 'Graphics', 'JavaScript', 
            'Security', 'Performance', 'Origin trials', 
            'Deprecations and removals'
        }
    
    def _load_focus_areas_config(self, config_path: Path) -> Dict:
        """Load focus areas configuration from YAML file."""
        if not config_path.exists():
            print(f"Warning: Focus areas config not found at {config_path}")
            return {'focus_areas': {}}
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def _map_area_name(self, heading_title: str) -> str:
        """
        Map a heading title to the corresponding focus area key.
        Uses focus_areas.yaml configuration with fallback to original heading.
        
        Args:
            heading_title: The h2 heading title from release notes
            
        Returns:
            Focus area key or original heading if no match found
        """
        heading_lower = heading_title.lower().strip()
        
        # Try exact heading pattern matches first (strict matching)
        for area_key, area_config in self.focus_areas_config.get('focus_areas', {}).items():
            heading_patterns = area_config.get('heading_patterns', [])
            for pattern in heading_patterns:
                if pattern.lower() == heading_lower:
                    return area_key
        
        # Try partial matches for specific areas (Payment, Developer Tools)
        # Payment: if heading contains "payment"
        if 'payment' in heading_lower:
            return 'payment'
        
        # DevTools: if heading contains "developer tools"
        if 'developer tools' in heading_lower:
            return 'devtools'
        
        # Try exact keyword matches only (no partial matching to avoid confusion)
        for area_key, area_config in self.focus_areas_config.get('focus_areas', {}).items():
            keywords = area_config.get('keywords', [])
            for keyword in keywords:
                if keyword.lower() == heading_lower:
                    return area_key
        
        # Final fallback: check if the heading contains device/devices
        if 'device' in heading_lower:
            return 'devices'
        
        # Use original heading title as area name if no focus area matches
        return heading_title.lower().replace(' ', '-').replace('&', 'and')
    
    def validate_structure(self, content: str) -> Tuple[bool, List[str]]:
        """
        Validate that the release notes have expected structure.
        
        Returns:
            Tuple of (is_valid, list_of_warnings)
        """
        warnings = []
        h2_sections = self.extract_h2_titles(content)
        
        # Check if any expected areas are found
        found_areas = set()
        for h2 in h2_sections:
            for expected in self.expected_areas:
                if expected.lower() in h2.lower():
                    found_areas.add(expected)
        
        missing = self.expected_areas - found_areas
        
        if len(missing) > len(self.expected_areas) * 0.5:  # More than 50% missing
            warnings.append(f"WARNING: Structure may have changed! Missing areas: {missing}")
            return False, warnings
        elif missing:
            warnings.append(f"INFO: Some areas not found (may be normal): {missing}")
        
        return True, warnings
    
    def extract_h2_titles(self, content: str) -> List[str]:
        """Extract all h2 titles from content."""
        pattern = r'^##\s+(.+)$'
        return re.findall(pattern, content, re.MULTILINE)
    
    def clean_webgpu_content(self, content: str) -> str:
        """
        Clean WebGPU release notes by removing invalid sections.
        Compatible with versions 136-139 with different structures.
        
        Cleaning rules:
        1. Remove version history (from "## What's New in WebGPU" to end) - for 136, 139 etc
        2. Remove metadata (author, dates, navigation) - for 136, 139 etc  
        3. Keep ALL actual feature content and heading structure
        4. For clean versions like 137, 138: minimal cleaning
        """
        lines = content.split('\n')
        cleaned_lines = []
        skip_remaining = False
        
        for i, line in enumerate(lines):
            # Check for version history section start (not the main title)
            # This removes "## What's New in WebGPU" history sections (not "# What's New in WebGPU" titles)
            if re.match(r'^##\s+What\'s New in WebGPU\s*$', line, re.IGNORECASE) and i > 10:
                # Only remove if it's not near the beginning (not the main title)
                skip_remaining = True
                break
            
            # Skip metadata lines (common in 136, 139 but not in 137, 138)
            if any(skip in line for skip in [
                'François Beaufort', 
                '[ GitHub ]',
                'Published:',
                'Stay organized with collections',
                'Chrome for Developers',
                '![François Beaufort]',
                'Last updated',
                'Source: https://developer.chrome.com'
            ]):
                continue
            
            # Skip navigation markers at the beginning
            if line.strip().startswith('* [') and 'https://' in line and i < 20:
                continue
            
            # Skip collection organization prompts
            if 'Stay organized with collections' in line:
                continue
                
            # Add valid lines
            if not skip_remaining:
                cleaned_lines.append(line)
        
        # Join and clean up
        cleaned = '\n'.join(cleaned_lines)
        
        # IMPORTANT: Don't remove valid content headers, only remove if they're clearly metadata
        # Keep "## Key Updates" and other structural headers
        
        # Clean up excessive blank lines
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        return cleaned.strip()
    
    def parse_sections(self, content: str) -> List[Section]:
        """
        Parse content into hierarchical sections.
        """
        lines = content.split('\n')
        sections = []
        current_h2 = None
        current_h3 = None
        
        for i, line in enumerate(lines):
            # Check for h2
            h2_match = re.match(r'^##\s+(.+)$', line)
            if h2_match:
                # Save previous h2 if exists
                if current_h2:
                    current_h2.end_line = i - 1
                    current_h2.content = '\n'.join(lines[current_h2.start_line:current_h2.end_line + 1])
                    sections.append(current_h2)
                
                # Create new h2 section
                current_h2 = Section(
                    title=h2_match.group(1).strip(),
                    level=2,
                    content='',
                    start_line=i,
                    end_line=i
                )
                current_h3 = None
                continue
            
            # Check for h3
            h3_match = re.match(r'^###\s+(.+)$', line)
            if h3_match and current_h2:
                # Save previous h3 if exists
                if current_h3:
                    current_h3.end_line = i - 1
                    current_h3.content = '\n'.join(lines[current_h3.start_line:current_h3.end_line + 1])
                
                # Create new h3 feature
                current_h3 = Section(
                    title=h3_match.group(1).strip(),
                    level=3,
                    content='',
                    start_line=i,
                    end_line=i
                )
                current_h2.features.append(current_h3)
        
        # Close last sections
        if current_h3:
            current_h3.end_line = len(lines) - 1
            current_h3.content = '\n'.join(lines[current_h3.start_line:current_h3.end_line + 1])
        
        if current_h2:
            current_h2.end_line = len(lines) - 1
            current_h2.content = '\n'.join(lines[current_h2.start_line:current_h2.end_line + 1])
            sections.append(current_h2)
        
        return sections
    
    def extract_areas(self, content: str) -> Dict[str, str]:
        """
        Extract content by area based on h2 sections using focus_areas.yaml mapping.
        Supports content keyword search for areas like on-device-ai at feature level.
        
        Returns:
            Dictionary mapping focus area keys to content.
        """
        sections = self.parse_sections(content)
        areas = {}
        
        for section in sections:
            # Skip meta sections
            if any(skip in section.title.lower() for skip in ['what\'s new', 'chrome 1']):
                continue
            
            # Map to focus area using configuration
            area_key = self._map_area_name(section.title)
            
            # Combine content if area already exists (multiple headings map to same area)
            if area_key in areas:
                areas[area_key] += '\n\n' + section.content
            else:
                areas[area_key] = section.content
            
            # Check for additional areas that search content keywords at FEATURE level
            self._extract_keyword_features(section, area_key, areas)
        
        return areas
    
    def _extract_keyword_features(self, section, area_key, areas):
        """
        Extract individual features that match content keywords for specific areas.
        This is used for areas like on-device-ai that should only include specific features
        from sections like origin-trials, not the entire section.
        """
        # Only process areas that have search_content_keywords enabled
        for area_key_check, area_config in self.focus_areas_config.get('focus_areas', {}).items():
            if area_config.get('search_content_keywords', False):
                keywords = area_config.get('keywords', [])
                
                # Check each h3 feature in this section
                for feature in section.features:
                    # Check if this feature content contains any of the keywords
                    feature_content_lower = feature.content.lower()
                    for keyword in keywords:
                        if keyword.lower() in feature_content_lower:
                            # Add this specific feature to the keyword area
                            if area_key_check not in areas:
                                areas[area_key_check] = feature.content
                            else:
                                areas[area_key_check] += '\n\n' + feature.content
                            break  # Found match, no need to check other keywords for this feature
    
    def _find_content_keyword_areas(self, content: str) -> List[str]:
        """
        Find areas that should include this content based on keyword search.
        Used for areas with search_content_keywords: true.
        """
        content_lower = content.lower()
        matching_areas = []
        
        for area_key, area_config in self.focus_areas_config.get('focus_areas', {}).items():
            # Only check areas with search_content_keywords enabled
            if area_config.get('search_content_keywords', False):
                keywords = area_config.get('keywords', [])
                for keyword in keywords:
                    if keyword.lower() in content_lower:
                        matching_areas.append(area_key)
                        break  # Found match, no need to check other keywords for this area
        
        return matching_areas
    
    def extract_issue_ids(self, content: str) -> set:
        """Extract issue IDs and tracking links from content."""
        issue_ids = set()
        
        # Various patterns for issue IDs
        patterns = [
            r'tracking bug #(\d+)',
            r'issue (\d+)',
            r'issues\.chromium\.org/issues/(\d+)',
            r'crbug\.com/(\d+)',
            r'chromestatus\.com/feature/(\d+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            issue_ids.update(matches)
        
        return issue_ids
    
    def normalize_title(self, title: str) -> str:
        """Normalize title for comparison."""
        # Remove common prefixes
        title = re.sub(r'^WebGPU:\s*', '', title, flags=re.IGNORECASE)
        # Convert to lowercase and remove special chars
        title = re.sub(r'[^\w\s]', '', title.lower())
        # Normalize whitespace
        title = ' '.join(title.split())
        return title
    
    def calculate_similarity(self, title1: str, title2: str) -> float:
        """Calculate similarity between two titles."""
        t1 = self.normalize_title(title1)
        t2 = self.normalize_title(title2)
        
        # Exact match
        if t1 == t2:
            return 1.0
        
        # Check if one contains the other
        if t1 in t2 or t2 in t1:
            return 0.8
        
        # Word overlap
        words1 = set(t1.split())
        words2 = set(t2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    def deduplicate_features(self, chrome_features: List[Section], 
                           webgpu_features: List[Section]) -> List[Section]:
        """
        Deduplicate features with WebGPU taking priority.
        
        Returns:
            List of deduplicated features with WebGPU features prioritized.
        """
        unique_features = []
        webgpu_titles_used = set()
        
        # First pass: Add all WebGPU features (they have priority)
        for webgpu_feature in webgpu_features:
            # Skip meta sections
            if any(skip in webgpu_feature.title.lower() 
                   for skip in ['dawn updates', 'what\'s new']):
                if 'dawn' in webgpu_feature.title.lower():
                    unique_features.append(webgpu_feature)
                continue
            
            unique_features.append(webgpu_feature)
            webgpu_titles_used.add(self.normalize_title(webgpu_feature.title))
        
        # Second pass: Add Chrome features that don't duplicate WebGPU
        for chrome_feature in chrome_features:
            chrome_normalized = self.normalize_title(chrome_feature.title)
            
            # Check for duplicates
            is_duplicate = False
            
            # Check title similarity
            for webgpu_normalized in webgpu_titles_used:
                similarity = self.calculate_similarity(chrome_feature.title, webgpu_normalized)
                if similarity > 0.7:  # 70% similarity threshold
                    is_duplicate = True
                    break
            
            # Check issue ID overlap
            if not is_duplicate:
                chrome_issues = self.extract_issue_ids(chrome_feature.content)
                for webgpu_feature in webgpu_features:
                    webgpu_issues = self.extract_issue_ids(webgpu_feature.content)
                    if chrome_issues & webgpu_issues:  # Any common issue IDs
                        is_duplicate = True
                        break
            
            # Add if not duplicate
            if not is_duplicate:
                unique_features.append(chrome_feature)
        
        return unique_features
    
    def merge_graphics_webgpu(self, chrome_graphics: Optional[str], 
                             webgpu_content: str, version: str) -> str:
        """
        Merge Graphics section from Chrome with cleaned WebGPU content.
        Includes deduplication with WebGPU taking priority.
        
        Args:
            chrome_graphics: Graphics section from Chrome release notes
            webgpu_content: Cleaned WebGPU release notes
            version: Chrome version number
            
        Returns:
            Merged and deduplicated content for graphics-webgpu area.
        """
        # Parse features from both sources
        chrome_features = []
        if chrome_graphics:
            chrome_sections = self.parse_sections(chrome_graphics)
            for section in chrome_sections:
                chrome_features.extend(section.features)
        
        webgpu_features = []
        if webgpu_content:
            webgpu_sections = self.parse_sections(webgpu_content)
            # Extract h3 features from WebGPU h2 sections
            for section in webgpu_sections:
                webgpu_features.extend(section.features)
        
        # Deduplicate features
        unique_features = self.deduplicate_features(chrome_features, webgpu_features)
        
        # Build merged content
        merged = [f"# Graphics and WebGPU - Chrome {version}\n"]
        
        # Separate Chrome and WebGPU features
        chrome_unique = [f for f in unique_features if f in chrome_features]
        webgpu_unique = [f for f in unique_features if f in webgpu_features]
        
        # Add Chrome Graphics features (non-duplicates)
        if chrome_unique:
            merged.append("## Graphics (from Chrome Release Notes)\n")
            for feature in chrome_unique:
                merged.append(f"### {feature.title}")
                # Get content without the header
                content_lines = feature.content.split('\n')[1:]
                merged.append('\n'.join(content_lines))
                merged.append("")
        
        # Add WebGPU features
        if webgpu_unique:
            merged.append("## WebGPU Features\n")
            for feature in webgpu_unique:
                merged.append(f"### {feature.title}")
                # Get content without the header  
                content_lines = feature.content.split('\n')[1:]
                merged.append('\n'.join(content_lines))
                merged.append("")
        
        # Add stats comment
        total_before = len(chrome_features) + len(webgpu_features)
        total_after = len(unique_features)
        merged.append(f"<!-- Deduplication: {total_before} → {total_after} features -->")
        
        return '\n'.join(merged)
    
    def process_version(self, version: str, output_dir: Optional[Path] = None) -> Dict[str, Path]:
        """
        Process a specific Chrome version with validation and cleaning.
        
        Returns:
            Dictionary mapping area names to output file paths.
        """
        return self.process_version_markdown_only(version, output_dir)
    
    def process_version_with_yaml(self, version: str, 
                                 markdown_output_dir: Optional[Path] = None,
                                 yaml_output_dir: Optional[Path] = None) -> Dict[str, Dict[str, Path]]:
        """
        Complete processing with both markdown and YAML output.
        
        Returns:
            Dictionary with 'markdown' and 'yaml' keys mapping to file paths.
        """
        # Default directories
        if not markdown_output_dir:
            markdown_output_dir = Path('upstream_docs/processed_releasenotes/processed_forwebplatform/areas')
        if not yaml_output_dir:
            yaml_output_dir = Path('upstream_docs/processed_releasenotes/processed_forwebplatform/processed_yaml')
        
        # Ensure directories exist
        markdown_output_dir.mkdir(parents=True, exist_ok=True)
        yaml_output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"Processing Chrome {version} with YAML output")
        print(f"{'='*60}")
        
        # Step 1: Generate markdown files
        print("  Step 1: Generating markdown files...")
        markdown_files = self.process_version(version, markdown_output_dir)
        print(f"  ✓ Generated {len(markdown_files)} markdown files")
        
        # Step 2: Convert to YAML
        print("\n  Step 2: Converting to YAML...")
        from utils.yaml_pipeline import YAMLPipeline
        
        yaml_pipeline = YAMLPipeline()
        yaml_files = {}
        
        for area, markdown_file in markdown_files.items():
            try:
                # Read markdown content
                markdown_content = markdown_file.read_text(encoding='utf-8')
                
                # Create area output directory
                area_yaml_dir = yaml_output_dir / area
                area_yaml_dir.mkdir(exist_ok=True)
                
                # Process with YAML pipeline  
                result = yaml_pipeline.process_release_notes(
                    markdown_content=markdown_content,
                    version=version,
                    channel='stable',
                    save_yaml=True,
                    split_by_area=False,  # We're already area-specific
                    merge_webgpu=False    # Already merged in our pipeline
                )
                
                # Check if we have features 
                features = result.get('features', [])
                if features:
                    # Save YAML manually since we need custom path
                    yaml_file = area_yaml_dir / f'chrome-{version}-stable.yml'
                    
                    yaml_data = {
                        'version': version,
                        'channel': 'stable', 
                        'area': area,
                        'features': features,
                        'statistics': result.get('statistics', {}),
                        'generated_at': datetime.now().isoformat()
                    }
                    
                    with open(yaml_file, 'w', encoding='utf-8') as f:
                        yaml.safe_dump(yaml_data, f, default_flow_style=False, allow_unicode=True)
                    
                    yaml_files[area] = yaml_file
                    features_count = len(features)
                    print(f"    ✓ {area:20s}: {features_count:2d} features → YAML")
                else:
                    print(f"    ❌ {area:20s}: YAML conversion failed - no features extracted")
                    
            except Exception as e:
                print(f"    ❌ {area:20s}: Error - {e}")
        
        return {
            'markdown': markdown_files,
            'yaml': yaml_files
        }

    def process_version_markdown_only(self, version: str, output_dir: Optional[Path] = None) -> Dict[str, Path]:
        """
        Process version and return markdown files only (refactored from original method).
        """
        if not output_dir:
            output_dir = Path('upstream_docs/processed_releasenotes/processed_forwebplatform/areas')
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Input files
        chrome_file = Path(f'upstream_docs/release_notes/WebPlatform/chrome-{version}.md')
        webgpu_file = Path(f'upstream_docs/release_notes/WebPlatform/webgpu-{version}.md')
        
        if not chrome_file.exists():
            raise FileNotFoundError(f"Chrome release notes not found: {chrome_file}")
        
        print(f"\n{'='*60}")
        print(f"Processing Chrome {version}")
        print(f"{'='*60}")
        
        # Read Chrome content
        chrome_content = chrome_file.read_text(encoding='utf-8')
        
        # Validate structure
        is_valid, warnings = self.validate_structure(chrome_content)
        for warning in warnings:
            print(f"  {warning}")
        
        if not is_valid:
            print("  ⚠️  Structure validation failed, but continuing...")
        
        # Extract areas from Chrome
        print("\n  Extracting areas from Chrome release notes...")
        areas = self.extract_areas(chrome_content)
        print(f"  ✓ Found {len(areas)} areas")
        
        # Process WebGPU if exists
        if webgpu_file.exists():
            print("\n  Processing WebGPU release notes...")
            webgpu_raw = webgpu_file.read_text(encoding='utf-8')
            
            # Clean WebGPU content
            webgpu_cleaned = self.clean_webgpu_content(webgpu_raw)
            
            # Calculate cleaning stats
            original_lines = len(webgpu_raw.split('\n'))
            cleaned_lines = len(webgpu_cleaned.split('\n'))
            print(f"  ✓ Cleaned WebGPU: {original_lines} → {cleaned_lines} lines "
                  f"(removed {original_lines - cleaned_lines} lines)")
            
            # Merge with Graphics-WebGPU area
            chrome_graphics = areas.get('graphics-webgpu', '')
            merged_content = self.merge_graphics_webgpu(chrome_graphics, webgpu_cleaned, version)
            areas['graphics-webgpu'] = merged_content
        
        # Write output files
        print("\n  Writing area files...")
        output_files = {}
        
        for area, content in areas.items():
            if not content.strip():
                continue
            
            # Create area directory
            area_dir = output_dir / area
            area_dir.mkdir(exist_ok=True)
            
            # Write file
            output_file = area_dir / f'chrome-{version}-stable.md'
            output_file.write_text(content, encoding='utf-8')
            output_files[area] = output_file
            
            # Stats
            lines = len(content.split('\n'))
            features = len(re.findall(r'^###\s+', content, re.MULTILINE))
            print(f"    ✓ {area:20s}: {lines:4d} lines, {features:2d} features")
        
        return output_files


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Clean data pipeline for WebPlatform release notes"
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Chrome version to process"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory for area files"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate structure without processing"
    )
    parser.add_argument(
        "--with-yaml",
        action="store_true",
        help="Also generate YAML output files"
    )
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = CleanDataPipeline()
    
    if args.validate_only:
        # Just validate
        chrome_file = Path(f'upstream_docs/release_notes/WebPlatform/chrome-{args.version}.md')
        if not chrome_file.exists():
            print(f"❌ File not found: {chrome_file}")
            return 1
        
        content = chrome_file.read_text(encoding='utf-8')
        is_valid, warnings = pipeline.validate_structure(content)
        
        print(f"Chrome {args.version} Structure Validation:")
        for warning in warnings:
            print(f"  {warning}")
        
        if is_valid:
            print("✅ Structure is valid")
            return 0
        else:
            print("❌ Structure validation failed")
            return 1
    
    try:
        if args.with_yaml:
            # Full processing with YAML
            result = pipeline.process_version_with_yaml(args.version)
            markdown_files = result['markdown']
            yaml_files = result['yaml']
            
            print(f"\n{'='*60}")
            print(f"✅ Successfully processed Chrome {args.version}")
            print(f"   Generated {len(markdown_files)} markdown files")
            print(f"   Generated {len(yaml_files)} YAML files")
            print(f"{'='*60}")
        else:
            # Markdown only
            output_files = pipeline.process_version(args.version, args.output_dir)
            
            print(f"\n{'='*60}")
            print(f"✅ Successfully processed Chrome {args.version}")
            print(f"   Generated {len(output_files)} area files")
            print(f"{'='*60}")
        
    except Exception as e:
        print(f"\n❌ Error processing Chrome {args.version}: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())