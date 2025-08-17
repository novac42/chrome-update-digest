"""
Focus Area Manager for Chrome Release Notes.
Implements heading-first matching with Web API exception.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
import re


class FocusAreaManager:
    """
    Manages focus areas for filtering and categorizing Chrome release notes.
    
    Key features:
    - Heading-first matching priority
    - Web API exception for multiple tags
    - Case-insensitive matching
    - Simplified keyword approach
    """
    
    def __init__(self, config_path: Path):
        """Initialize with configuration file."""
        self.config_path = config_path
        self.config = self._load_config()
        self.focus_areas = self.config.get('focus_areas', {})
        self.metadata = self.config.get('metadata', {})
    
    def _load_config(self) -> Dict:
        """Load focus areas configuration from YAML."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def tag_feature(self, feature: Dict) -> List[str]:
        """
        Tag a feature based on heading-first priority and keywords.
        
        Args:
            feature: Feature dict with 'title', 'content', and optionally 'heading'
            
        Returns:
            List of area tags for the feature
        """
        tags = []
        
        # Extract heading if present
        heading = feature.get('heading', '').strip()
        title = feature.get('title', '').strip()
        content = feature.get('content', '').strip()
        
        # Step 1: Check heading match (highest priority)
        if heading:
            heading_tags = self._match_by_heading(heading)
            if heading_tags:
                tags.extend(heading_tags)
                
                # If heading matched and it's not Web API, we're done
                # (unless Web API is in the tags, then continue to find more)
                if 'webapi' not in tags:
                    return tags if tags else ['others']
        
        # Step 2: Check title and content for keywords
        # This happens if:
        # - No heading match found
        # - Or Web API was matched (can have multiple tags)
        combined_text = f"{title} {content}".lower()
        
        for area_key, area_config in self.focus_areas.items():
            if area_key == 'others':
                continue  # Others is only used as fallback
                
            # Skip if already tagged (unless it's webapi or this is webapi)
            if tags and area_key not in tags and area_key != 'webapi' and 'webapi' not in tags:
                continue
            
            # Check keywords
            keywords = area_config.get('keywords', [])
            for keyword in keywords:
                if self._keyword_matches(keyword.lower(), combined_text):
                    if area_key not in tags:
                        tags.append(area_key)
                    break
        
        # Step 3: If no tags found, use 'others'
        if not tags:
            tags = ['others']
        
        return tags
    
    def _match_by_heading(self, heading: str) -> List[str]:
        """
        Match heading against configured patterns.
        
        Args:
            heading: The heading text to match
            
        Returns:
            List of matching area tags
        """
        tags = []
        heading_lower = heading.lower()
        
        for area_key, area_config in self.focus_areas.items():
            heading_patterns = area_config.get('heading_patterns', [])
            
            for pattern in heading_patterns:
                if pattern.lower() in heading_lower or heading_lower in pattern.lower():
                    tags.append(area_key)
                    
                    # If not Web API and not others, stop after first match
                    if area_key != 'webapi' and area_key != 'others':
                        return tags
                    break  # Break inner loop but continue checking other areas for webapi
        
        return tags
    
    def _keyword_matches(self, keyword: str, text: str) -> bool:
        """
        Check if keyword matches in text (case-insensitive).
        
        Args:
            keyword: Keyword to search for
            text: Text to search in
            
        Returns:
            True if keyword is found
        """
        # Use word boundary matching for better accuracy
        # This prevents "api" from matching "rapid" or "capitalize"
        pattern = r'\b' + re.escape(keyword) + r'\b'
        return bool(re.search(pattern, text, re.IGNORECASE))
    
    def filter_features(
        self, features: List[Dict], focus_areas: List[str]) -> List[Dict]:
        """
        Filter features by specified focus areas.
        
        Args:
            features: List of feature dictionaries
            focus_areas: List of focus area names to filter by
            
        Returns:
            Filtered list of features
        """
        if not focus_areas:
            return features
        
        # Normalize focus area names
        focus_area_keys = []
        for area in focus_areas:
            area_lower = area.lower().replace(' ', '-').replace('_', '-')
            
            # Map common variations
            if area_lower in ['ai', 'on-device-ai', 'ondeviceai']:
                focus_area_keys.append('on-device-ai')
            elif area_lower in ['webgpu', 'gpu', 'graphics']:
                focus_area_keys.append('graphics-webgpu')
            elif area_lower in ['security', 'privacy']:
                focus_area_keys.append('security-privacy')
            elif area_lower in ['api', 'webapi', 'web-api']:
                focus_area_keys.append('webapi')
            elif area_lower in ['css', 'styling']:
                focus_area_keys.append('css')
            elif area_lower in ['html', 'dom']:
                focus_area_keys.append('html-dom')
            elif area_lower in ['media', 'multimedia', 'audio', 'video']:
                focus_area_keys.append('multimedia')
            elif area_lower in ['pwa', 'service-worker', 'serviceworker']:
                focus_area_keys.append('pwa-service-worker')
            elif area_lower in ['loading', 'navigation']:
                focus_area_keys.append('navigation-loading')
            elif area_lower in ['trials', 'origin-trials']:
                focus_area_keys.append('origin-trials')
            elif area_lower in ['deprecations', 'deprecated']:
                focus_area_keys.append('deprecations')
            elif area_lower in ['performance', 'optimization']:
                focus_area_keys.append('performance')
            elif area_lower in ['device', 'devices', 'sensor']:
                focus_area_keys.append('devices')
            else:
                # Check if it matches any configured area key
                for key in self.focus_areas.keys():
                    if area_lower == key.lower().replace('_', '-'):
                        focus_area_keys.append(key)
                        break
        
        if not focus_area_keys:
            return features
        
        # Filter features that have at least one matching tag
        filtered = []
        for feature in features:
            feature_tags = feature.get('primary_tags', [])
            
            # Extract tag names if tags are dicts
            tag_names = []
            for tag in feature_tags:
                if isinstance(tag, dict):
                    tag_names.append(tag.get('name', '').lower())
                else:
                    tag_names.append(str(tag).lower())
            
            # Check if any feature tag matches our focus areas
            for focus_key in focus_area_keys:
                if focus_key in tag_names:
                    filtered.append(feature)
                    break
        
        return filtered
    
    def get_area_info(self, area_key: str) -> Optional[Dict]:
        """
        Get information about a specific focus area.
        
        Args:
            area_key: The area key to look up
            
        Returns:
            Area configuration dict or None
        """
        return self.focus_areas.get(area_key)
    
    def list_areas(self) -> List[str]:
        """
        List all configured focus areas.
        
        Returns:
            List of area keys
        """
        return list(self.focus_areas.keys())
    
    def get_area_display_name(self, area_key: str) -> str:
        """
        Get the display name for an area.
        
        Args:
            area_key: The area key
            
        Returns:
            Display name or the key itself if not found
        """
        area = self.focus_areas.get(area_key, {})
        return area.get('name', area_key)
    
    def split_features_by_area(self, features: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Split features into separate lists by area.
        
        Args:
            features: List of tagged features
            
        Returns:
            Dict mapping area keys to lists of features
        """
        area_features = {}
        
        for feature in features:
            tags = feature.get('primary_tags', [])
            
            # If no tags, put in others
            if not tags:
                if 'others' not in area_features:
                    area_features['others'] = []
                area_features['others'].append(feature)
                continue
            
            # Add to each tagged area
            for tag in tags:
                tag_name = tag.get('name') if isinstance(tag, dict) else str(tag)
                
                if tag_name not in area_features:
                    area_features[tag_name] = []
                area_features[tag_name].append(feature)
        
        return area_features