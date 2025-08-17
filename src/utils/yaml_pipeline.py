"""
YAML Pipeline for Tagged Features
Provides intermediate YAML format between extraction and digest generation.
"""

import yaml
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict

from src.utils.link_extractor import LinkExtractor, ExtractedFeature
from src.models.feature_tagging import HeadingBasedTagger, TaggedFeature
from src.utils.focus_area_manager import FocusAreaManager


@dataclass
class PipelineStatistics:
    """Statistics about the extraction process."""
    total_features: int = 0
    total_links: int = 0
    primary_tags: Dict[str, int] = None
    cross_cutting: Dict[str, int] = None
    
    def __post_init__(self):
        if self.primary_tags is None:
            self.primary_tags = {}
        if self.cross_cutting is None:
            self.cross_cutting = {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'total_features': self.total_features,
            'total_links': self.total_links,
            'primary_tags': self.primary_tags,
            'cross_cutting': self.cross_cutting
        }


class YAMLPipeline:
    """
    Manages the YAML-based pipeline for feature extraction and tagging.
    
    Pipeline flow:
    1. Extract features from markdown using LinkExtractor
    2. Tag features using HeadingBasedTagger
    3. Save to YAML format
    4. Load from YAML for digest generation
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize the YAML pipeline.
        
        Args:
            output_dir: Directory for YAML output files
        """
        self.base_output_dir = output_dir or Path('upstream_docs/processed_releasenotes/processed_forwebplatform')
        self.base_output_dir.mkdir(parents=True, exist_ok=True)
        # Keep output_dir for backward compatibility, pointing to base dir
        self.output_dir = self.base_output_dir
        
        self.link_extractor = LinkExtractor()
        self.tagger = HeadingBasedTagger()
        self.focus_manager = FocusAreaManager(Path('config/focus_areas.yaml'))
        
        # Define area mappings based on heading2
        self.area_mappings = {
            'css': ['CSS and UI', 'CSS'],
            'webapi': ['Web APIs'],
            'graphics-webgpu': ['WebGPU', 'Graphics', 'Detailed WebGPU Updates', 'Additional WebGPU Updates'],
            'javascript': ['JavaScript'],
            'security': ['Security', 'Privacy and security'],
            'performance': ['Performance'],
            'media': ['Multimedia', 'Images and media'],
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
    
    def process_release_notes(
        self,
        markdown_content: str,
        version: str,
        channel: str = 'stable',
        save_yaml: bool = True,
        split_by_area: bool = False,
        merge_webgpu: bool = True
    ) -> Dict[str, Any]:
        """
        Process release notes through the full pipeline.
        
        Args:
            markdown_content: Raw markdown content
            version: Chrome version number
            channel: Release channel (stable, beta, dev)
            save_yaml: Whether to save YAML output
            split_by_area: Whether to split features into separate YAML files by area
            merge_webgpu: Whether to merge WebGPU release notes if available
            
        Returns:
            Dictionary containing tagged features and metadata
        """
        # Step 0: Merge WebGPU content if available and requested
        if merge_webgpu:
            markdown_content = self._merge_webgpu_content(markdown_content, version)
        
        # Step 1: Extract features with links
        extracted_features = self.link_extractor.extract_from_content(markdown_content)
        
        # Step 2: Tag features
        tagged_features = []
        for feature in extracted_features:
            tagged = self.tagger.tag_feature(feature)
            tagged_features.append(tagged)
        
        # Step 3: Calculate statistics
        stats = self._calculate_statistics(tagged_features)
        
        # Step 4: Build output structure
        features_as_dicts = [self._tagged_feature_to_dict(f) for f in tagged_features]
        output = {
            'version': version,
            'channel': channel,
            'extraction_timestamp': datetime.now().isoformat(),
            'extraction_method': 'deterministic',
            'statistics': stats.to_dict(),
            'features': features_as_dicts
        }
        
        # Step 5: Save to YAML if requested
        if save_yaml:
            if split_by_area:
                # Split features by area and save separate files
                area_features = self.split_features_by_area(features_as_dicts)
                for area, features in area_features.items():
                    area_stats = self._calculate_statistics_from_dicts(features)
                    area_output = {
                        'version': version,
                        'channel': channel,
                        'area': area,
                        'extraction_timestamp': datetime.now().isoformat(),
                        'extraction_method': 'deterministic',
                        'statistics': area_stats.to_dict(),
                        'features': features
                    }
                    yaml_path = self._get_yaml_path(version, channel, area)
                    self.save_to_yaml(area_output, yaml_path)
                
                # Also save a combined file with area information
                output['areas'] = list(area_features.keys())
            else:
                # Save single file with all features
                yaml_path = self._get_yaml_path(version, channel)
                self.save_to_yaml(output, yaml_path)
        
        return output
    
    def filter_by_focus_areas(
        self,
        yaml_data: Dict,
        focus_areas: List[str],
        min_score: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Filter features by focus areas.
        
        Args:
            yaml_data: Loaded YAML data
            focus_areas: List of focus area keys
            min_score: Minimum match score
            
        Returns:
            Filtered YAML data with matched features
        """
        if not focus_areas:
            return yaml_data
        
        # Filter features
        features = yaml_data.get('features', [])
        filtered_features = self.focus_manager.filter_features(
            features, focus_areas, min_score
        )
        
        # Update statistics
        stats = self._calculate_statistics_from_dicts(filtered_features)
        
        # Create filtered output
        filtered_data = yaml_data.copy()
        filtered_data['features'] = filtered_features
        filtered_data['statistics'] = stats.to_dict()
        filtered_data['applied_filters'] = {
            'focus_areas': focus_areas,
            'min_score': min_score or self.focus_manager.matching_config.min_score
        }
        
        return filtered_data
    
    def save_to_yaml(self, data: Dict, file_path: Path) -> None:
        """
        Save data to YAML file.
        
        Args:
            data: Data to save
            file_path: Output file path
        """
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(
                data,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
                width=120
            )
        
        print(f"Saved YAML to {file_path}")
    
    def load_from_yaml(self, file_path: Path) -> Dict[str, Any]:
        """
        Load data from YAML file.
        
        Args:
            file_path: YAML file path
            
        Returns:
            Loaded data dictionary
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def export_to_json(self, yaml_data: Dict, json_path: Path) -> None:
        """
        Export YAML data to JSON format.
        
        Args:
            yaml_data: YAML data dictionary
            json_path: Output JSON file path
        """
        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(yaml_data, f, indent=2, ensure_ascii=False)
        
        print(f"Exported to JSON: {json_path}")
    
    def _tagged_feature_to_dict(self, tagged_feature: TaggedFeature) -> Dict:
        """Convert TaggedFeature to dictionary for YAML."""
        feature_dict = tagged_feature.feature.to_dict()
        
        # Add tagging information
        feature_dict['primary_tags'] = [
            tag.to_dict() for tag in tagged_feature.primary_tags
        ]
        feature_dict['cross_cutting_concerns'] = tagged_feature.cross_cutting_concerns
        
        return feature_dict
    
    def _calculate_statistics(self, tagged_features: List[TaggedFeature]) -> PipelineStatistics:
        """Calculate statistics from tagged features."""
        stats = PipelineStatistics()
        
        stats.total_features = len(tagged_features)
        
        # Count links
        for feature in tagged_features:
            stats.total_links += len(feature.feature.links)
        
        # Count primary tags
        for feature in tagged_features:
            for tag in feature.primary_tags:
                tag_name = tag.name
                stats.primary_tags[tag_name] = stats.primary_tags.get(tag_name, 0) + 1
        
        # Count cross-cutting concerns
        for feature in tagged_features:
            for concern in feature.cross_cutting_concerns:
                stats.cross_cutting[concern] = stats.cross_cutting.get(concern, 0) + 1
        
        return stats
    
    def _calculate_statistics_from_dicts(self, features: List[Dict]) -> PipelineStatistics:
        """Calculate statistics from feature dictionaries."""
        stats = PipelineStatistics()
        
        stats.total_features = len(features)
        
        # Count links and tags
        for feature in features:
            links = feature.get('links', [])
            stats.total_links += len(links)
            
            # Count primary tags
            for tag in feature.get('primary_tags', []):
                tag_name = tag.get('name') if isinstance(tag, dict) else str(tag)
                stats.primary_tags[tag_name] = stats.primary_tags.get(tag_name, 0) + 1
            
            # Count cross-cutting concerns
            for concern in feature.get('cross_cutting_concerns', []):
                stats.cross_cutting[concern] = stats.cross_cutting.get(concern, 0) + 1
        
        return stats
    
    def _get_yaml_path(self, version: str, channel: str = 'stable', area: Optional[str] = None) -> Path:
        """
        Generate YAML file path for a version and optional area.
        
        Structure:
        - With area: processed_forwebplatform/{area}/chrome-{version}-{channel}.yml
        - Without area: processed_forwebplatform/chrome-{version}-{channel}-tagged.yml
        """
        # Ensure channel is set (default to stable if not specified)
        if not channel:
            channel = 'stable'
            
        if area:
            # Area-specific files go in subdirectories
            area_dir = self.base_output_dir / area
            area_dir.mkdir(parents=True, exist_ok=True)
            filename = f"chrome-{version}-{channel}.yml"
            return area_dir / filename
        else:
            # General tagged file stays in root directory
            filename = f"chrome-{version}-{channel}-tagged.yml"
            return self.base_output_dir / filename
    
    def _determine_area(self, feature: Dict) -> str:
        """
        Determine which area a feature belongs to based on its heading path.
        
        Args:
            feature: Feature dictionary with heading_path
            
        Returns:
            Area name (e.g., 'css', 'webapi', 'other')
        """
        heading_path = feature.get('heading_path', [])
        
        # Look for heading2 (usually index 1 or 2 in the path)
        for heading in heading_path:
            # Check each area mapping
            for area, headings in self.area_mappings.items():
                for h in headings:
                    if h.lower() in heading.lower():
                        return area
        
        # Default to 'other' if no match
        return 'other'
    
    def split_features_by_area(self, features: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Split features into separate lists by area.
        
        Args:
            features: List of feature dictionaries
            
        Returns:
            Dictionary mapping area names to feature lists
        """
        area_features = {}
        
        for feature in features:
            area = self._determine_area(feature)
            if area not in area_features:
                area_features[area] = []
            area_features[area].append(feature)
        
        return area_features
    
    def validate_yaml_data(self, yaml_data: Dict) -> List[str]:
        """
        Validate YAML data structure.
        
        Args:
            yaml_data: YAML data to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check required top-level fields
        required_fields = ['version', 'features', 'statistics']
        for field in required_fields:
            if field not in yaml_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate features
        features = yaml_data.get('features', [])
        if not isinstance(features, list):
            errors.append("Features must be a list")
        else:
            for i, feature in enumerate(features):
                if not isinstance(feature, dict):
                    errors.append(f"Feature {i} must be a dictionary")
                    continue
                
                # Check feature fields
                if 'title' not in feature:
                    errors.append(f"Feature {i} missing title")
                if 'links' not in feature:
                    errors.append(f"Feature {i} missing links")
        
        return errors
    
    def merge_yaml_files(self, yaml_files: List[Path], output_path: Path) -> Dict:
        """
        Merge multiple YAML files into one.
        
        Args:
            yaml_files: List of YAML file paths
            output_path: Output file path
            
        Returns:
            Merged data dictionary
        """
        all_features = []
        versions = []
        
        for yaml_file in yaml_files:
            data = self.load_from_yaml(yaml_file)
            all_features.extend(data.get('features', []))
            versions.append(data.get('version', 'unknown'))
        
        # Calculate combined statistics
        stats = self._calculate_statistics_from_dicts(all_features)
        
        # Create merged output
        merged = {
            'versions': versions,
            'extraction_timestamp': datetime.now().isoformat(),
            'extraction_method': 'merged',
            'statistics': stats.to_dict(),
            'features': all_features
        }
        
        # Save merged file
        self.save_to_yaml(merged, output_path)
        
        return merged
    
    def _merge_webgpu_content(self, chrome_content: str, version: str) -> str:
        """
        Merge WebGPU release notes with Chrome content.
        
        Args:
            chrome_content: Chrome release notes content
            version: Chrome version number
            
        Returns:
            Merged content with WebGPU features included
        """
        # Check for WebGPU file in the release notes directory
        webgpu_path = Path(f'upstream_docs/release_notes/WebPlatform/webgpu-{version}.md')
        
        if not webgpu_path.exists():
            # No WebGPU file, return original content
            return chrome_content
        
        print(f"Found WebGPU release notes for version {version}, merging...")
        
        # Read WebGPU content
        with open(webgpu_path, 'r', encoding='utf-8') as f:
            webgpu_content = f.read()
        
        # Parse Chrome content to find WebGPU section
        chrome_lines = chrome_content.split('\n')
        merged_lines = []
        webgpu_section_found = False
        webgpu_section_enhanced = False
        
        i = 0
        while i < len(chrome_lines):
            line = chrome_lines[i]
            
            # Check if this is a WebGPU-related section header
            if (line.startswith('#') and self._is_webgpu_related_line(line) and not webgpu_section_enhanced):
                # Found WebGPU section - enhance it with dedicated WebGPU content
                merged_lines.append(line)  # Keep original header
                merged_lines.append("")
                
                # Add note about enhancement
                merged_lines.append("*This section includes both Chrome WebGPU highlights and detailed WebGPU release notes.*")
                merged_lines.append("")
                
                # Add Chrome WebGPU content first (skip until next header)
                i += 1
                original_header_level = len(line.split()[0]) if line.startswith('#') else 1
                
                while i < len(chrome_lines):
                    current_line = chrome_lines[i]
                    
                    # Stop at next header of same or higher level
                    if current_line.startswith('#'):
                        current_header_level = len(current_line.split()[0])
                        if current_header_level <= original_header_level:
                            break
                    
                    merged_lines.append(current_line)
                    i += 1
                
                # Add dedicated WebGPU content
                merged_lines.append("")
                merged_lines.append("### Detailed WebGPU Updates")
                merged_lines.append("")
                
                # Add WebGPU content (skip title and "What's New in WebGPU" section)
                webgpu_lines = webgpu_content.split('\n')
                skip_title = True
                skip_whats_new = False
                
                for webgpu_line in webgpu_lines:
                    if skip_title and webgpu_line.startswith('# '):
                        skip_title = False
                        continue
                    
                    # Skip "What's New in WebGPU" section which contains version history
                    if webgpu_line.startswith('## What\'s New in WebGPU'):
                        skip_whats_new = True
                        continue
                    
                    # Stop skipping when we hit another H2 section that's not "What's New"
                    if skip_whats_new and webgpu_line.startswith('## ') and 'What\'s New' not in webgpu_line:
                        skip_whats_new = False
                    
                    # Add line only if we're not skipping
                    if not skip_title and not skip_whats_new:
                        merged_lines.append(webgpu_line)
                
                merged_lines.append("")
                webgpu_section_enhanced = True
                webgpu_section_found = True
                continue
            else:
                merged_lines.append(line)
            
            i += 1
        
        # If no WebGPU section was found in Chrome notes, add it as a new section
        if not webgpu_section_found:
            # Find Graphics section or a good insertion point
            insert_index = len(merged_lines)
            
            # Look for Graphics section first, then other suitable locations
            for idx, line in enumerate(merged_lines):
                if line.startswith('## '):
                    line_lower = line.lower()
                    # Insert after Graphics if found
                    if 'graphics' in line_lower:
                        # Find the end of Graphics section
                        temp_idx = idx + 1
                        while temp_idx < len(merged_lines):
                            if merged_lines[temp_idx].startswith('## '):
                                insert_index = temp_idx
                                break
                            temp_idx += 1
                        if insert_index != len(merged_lines):
                            break
                    # Otherwise insert before Security/Deprecations/Removals
                    elif any(keyword in line_lower for keyword in ['security', 'deprecation', 'removal']):
                        insert_index = idx
                        break
            
            # Insert WebGPU section
            webgpu_section = [
                "## WebGPU",
                "",
                "*Complete WebGPU updates for this release.*",
                ""
            ]
            
            # Add WebGPU content (skip title and "What's New in WebGPU" section)
            webgpu_lines = webgpu_content.split('\n')
            skip_title = True
            skip_whats_new = False
            
            for webgpu_line in webgpu_lines:
                if skip_title and webgpu_line.startswith('# '):
                    skip_title = False
                    continue
                
                # Skip "What's New in WebGPU" section which contains version history
                if webgpu_line.startswith('## What\'s New in WebGPU'):
                    skip_whats_new = True
                    continue
                
                # Stop skipping when we hit another H2 section that's not "What's New"
                if skip_whats_new and webgpu_line.startswith('## ') and 'What\'s New' not in webgpu_line:
                    skip_whats_new = False
                
                # Add line only if we're not skipping
                if not skip_title and not skip_whats_new:
                    webgpu_section.append(webgpu_line)
            
            webgpu_section.append("")
            
            # Insert at the determined position
            merged_lines[insert_index:insert_index] = webgpu_section
        
        return '\n'.join(merged_lines)
    
    def _is_webgpu_related_line(self, line: str) -> bool:
        """
        Check if a line is related to WebGPU.
        
        Args:
            line: Line to check
            
        Returns:
            True if the line is WebGPU-related
        """
        webgpu_keywords = [
            'webgpu', 'WebGPU', 'gpu rendering', 'WGSL', 'compute shader', 'vertex shader',
            'fragment shader', 'graphics pipeline', 'compute pipeline', 'GPUBuffer',
            'GPUTexture', 'GPUDevice', 'GPUAdapter', 'Dawn', 'Graphics'
        ]
        
        line_lower = line.lower()
        return any(keyword.lower() in line_lower for keyword in webgpu_keywords)