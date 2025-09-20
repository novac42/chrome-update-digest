"""
Area extractors for Chrome release notes processing.
Implements Strategy pattern for different extraction methods.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from pathlib import Path
import re
import yaml


@dataclass
class Section:
    """Represents a document section."""
    title: str
    level: int  # 2=h2, 3=h3, etc.
    content: str  # Full content including the header
    start_line: int
    end_line: int
    features: List['Section'] = field(default_factory=list)  # h3 features under h2


class BaseAreaExtractor(ABC):
    """
    Abstract base class for area extractors.
    Provides common functionality for all extraction strategies.
    """

    def __init__(self, focus_areas_config: Dict):
        """
        Initialize with focus areas configuration.

        Args:
            focus_areas_config: Configuration dictionary from focus_areas.yaml
        """
        self.focus_areas_config = focus_areas_config
        self.area_config = {}

    def set_area_config(self, area_key: str, area_config: Dict):
        """
        Set configuration for a specific area.

        Args:
            area_key: The area identifier
            area_config: Configuration for this specific area
        """
        self.area_key = area_key
        self.area_config = area_config

    @abstractmethod
    def extract(self, sections: List[Section], content: str) -> Dict[str, str]:
        """
        Extract area content from sections.

        Args:
            sections: Parsed sections from the release notes
            content: Raw content for additional processing

        Returns:
            Dictionary mapping area keys to extracted content
        """
        pass

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

        # Simple word overlap
        words1 = set(t1.split())
        words2 = set(t2.split())
        if not words1 or not words2:
            return 0.0

        overlap = len(words1 & words2)
        total = len(words1 | words2)

        return overlap / total if total > 0 else 0.0


class StandardAreaExtractor(BaseAreaExtractor):
    """
    Extracts areas based on heading patterns.
    Used for areas like CSS, Web APIs, etc.
    """

    def extract(self, sections: List[Section], content: str) -> Dict[str, str]:
        """
        Extract content for areas that match heading patterns.

        Args:
            sections: Parsed sections from the release notes
            content: Raw content (not used in this extractor)

        Returns:
            Dictionary with area key and its content
        """
        areas = {}
        heading_patterns = self.area_config.get('heading_patterns', [])

        for section in sections:
            # Skip meta sections
            if any(skip in section.title.lower() for skip in ['what\'s new', 'chrome 1']):
                continue

            # Check if section matches any heading pattern
            section_lower = section.title.lower().strip()
            for pattern in heading_patterns:
                if pattern.lower() == section_lower:
                    # Found matching section
                    if self.area_key in areas:
                        areas[self.area_key] = areas[self.area_key] + '\n\n' + section.content
                    else:
                        areas[self.area_key] = section.content
                    break

        return areas


class PartialMatchAreaExtractor(BaseAreaExtractor):
    """
    Extracts areas based on partial heading matches.
    Used for areas like Payment and DevTools.
    """

    def extract(self, sections: List[Section], content: str) -> Dict[str, str]:
        """
        Extract content for areas that partially match headings.

        Args:
            sections: Parsed sections from the release notes
            content: Raw content (not used in this extractor)

        Returns:
            Dictionary with area key and its content
        """
        areas = {}
        keywords = self.area_config.get('keywords', [])

        for section in sections:
            # Skip meta sections
            if any(skip in section.title.lower() for skip in ['what\'s new', 'chrome 1']):
                continue

            section_lower = section.title.lower().strip()

            # Check for partial matches
            for keyword in keywords:
                if keyword.lower() in section_lower:
                    # Found matching section
                    if self.area_key in areas:
                        areas[self.area_key] = areas[self.area_key] + '\n\n' + section.content
                    else:
                        areas[self.area_key] = section.content
                    break

        return areas


class KeywordAreaExtractor(BaseAreaExtractor):
    """
    Extracts individual features based on content keywords.
    Used for areas like on-device-ai that need feature-level filtering.
    """

    def extract(self, sections: List[Section], content: str) -> Dict[str, str]:
        """
        Extract individual features that match content keywords.

        Args:
            sections: Parsed sections from the release notes
            content: Raw content (not used in this extractor)

        Returns:
            Dictionary with area key and matching features
        """
        areas = {}
        keywords = self.area_config.get('keywords', [])

        # Check each section and its features
        for section in sections:
            # Skip meta sections
            if any(skip in section.title.lower() for skip in ['what\'s new', 'chrome 1']):
                continue

            # Check each feature in the section
            for feature in section.features:
                feature_content_lower = feature.content.lower()

                # Check if feature contains any keywords
                for keyword in keywords:
                    if keyword.lower() in feature_content_lower:
                        # Add this specific feature
                        if self.area_key in areas:
                            areas[self.area_key] = areas[self.area_key] + '\n\n' + feature.content
                        else:
                            areas[self.area_key] = feature.content
                        break  # Found match, no need to check other keywords

        return areas


class WebGPUAreaExtractor(BaseAreaExtractor):
    """
    Special extractor for WebGPU that handles multi-source extraction and deduplication.
    Merges content from Graphics section and dedicated WebGPU release notes.
    """

    def __init__(self, focus_areas_config: Dict):
        """
        Initialize WebGPU extractor with additional functionality for multi-source handling.

        Args:
            focus_areas_config: Configuration dictionary from focus_areas.yaml
        """
        super().__init__(focus_areas_config)
        self.webgpu_content = None
        self.webgpu_sections = []

    def set_webgpu_content(self, content: str, sections: List[Section]):
        """
        Set dedicated WebGPU release note content.

        Args:
            content: Raw WebGPU release note content
            sections: Parsed sections from WebGPU release notes
        """
        self.webgpu_content = content
        self.webgpu_sections = sections

    def extract(self, sections: List[Section], content: str) -> Dict[str, str]:
        """
        Extract WebGPU content from both Chrome Graphics and dedicated WebGPU notes.

        Args:
            sections: Parsed sections from Chrome release notes
            content: Raw Chrome release note content

        Returns:
            Dictionary with merged and deduplicated WebGPU content
        """
        areas = {}

        # First extract from Chrome Graphics section
        graphics_features = self._extract_graphics_webgpu(sections)

        # Then extract from dedicated WebGPU notes if available
        webgpu_features = self._extract_dedicated_webgpu()

        # Merge and deduplicate
        merged_content = self._merge_and_deduplicate(graphics_features, webgpu_features)

        if merged_content:
            areas[self.area_key] = merged_content

        return areas

    def _extract_graphics_webgpu(self, sections: List[Section]) -> List[Dict]:
        """Extract WebGPU features from Graphics section."""
        features = []

        for section in sections:
            # Look for Graphics section
            if 'graphics' in section.title.lower():
                # Extract WebGPU-related features
                for feature in section.features:
                    if 'webgpu' in feature.title.lower() or 'gpu' in feature.content.lower():
                        features.append({
                            'title': feature.title,
                            'content': feature.content,
                            'source': 'graphics'
                        })

        return features

    def _extract_dedicated_webgpu(self) -> List[Dict]:
        """Extract features from dedicated WebGPU release notes."""
        features = []

        if not self.webgpu_sections:
            return features

        for section in self.webgpu_sections:
            # Skip meta sections
            if section.level == 1 or 'what\'s new' in section.title.lower():
                continue

            # WebGPU notes may have features at h2 level
            if section.level == 2:
                features.append({
                    'title': section.title,
                    'content': section.content,
                    'source': 'webgpu'
                })

            # Also check for h3 features
            for feature in section.features:
                features.append({
                    'title': feature.title,
                    'content': feature.content,
                    'source': 'webgpu'
                })

        return features

    def _merge_and_deduplicate(self, graphics_features: List[Dict], webgpu_features: List[Dict]) -> str:
        """
        Merge and deduplicate features, prioritizing WebGPU-specific content.

        Args:
            graphics_features: Features from Graphics section
            webgpu_features: Features from dedicated WebGPU notes

        Returns:
            Merged content string
        """
        # Create a mapping of normalized titles to features
        feature_map = {}

        # Add graphics features first
        for feature in graphics_features:
            norm_title = self.normalize_title(feature['title'])
            feature_map[norm_title] = feature

        # Add/override with WebGPU features (they have priority)
        for feature in webgpu_features:
            norm_title = self.normalize_title(feature['title'])

            # Check for similar existing features
            found_similar = False
            for existing_title in list(feature_map.keys()):
                similarity = self.calculate_similarity(feature['title'], existing_title)
                if similarity > 0.7:  # High similarity threshold
                    # Replace with WebGPU version (priority)
                    del feature_map[existing_title]
                    feature_map[norm_title] = feature
                    found_similar = True
                    break

            if not found_similar:
                feature_map[norm_title] = feature

        # Combine all unique features
        content_parts = []
        for feature in feature_map.values():
            content_parts.append(feature['content'])

        return '\n\n'.join(content_parts)


class AreaExtractorFactory:
    """
    Factory class to create appropriate extractors based on area configuration.
    """

    def __init__(self, focus_areas_config: Dict):
        """
        Initialize factory with focus areas configuration.

        Args:
            focus_areas_config: Configuration dictionary from focus_areas.yaml
        """
        self.focus_areas_config = focus_areas_config

    def create_extractor(self, area_key: str, area_config: Dict) -> BaseAreaExtractor:
        """
        Create appropriate extractor for the given area.

        Args:
            area_key: The area identifier
            area_config: Configuration for this area

        Returns:
            Appropriate area extractor instance
        """
        # Special case for WebGPU
        if area_key == 'graphics-webgpu':
            extractor = WebGPUAreaExtractor(self.focus_areas_config)
        # Areas with content keyword search
        elif area_config.get('search_content_keywords', False):
            extractor = KeywordAreaExtractor(self.focus_areas_config)
        # Areas with partial matching (payment, devtools)
        elif area_key in ['payment', 'devtools']:
            extractor = PartialMatchAreaExtractor(self.focus_areas_config)
        # Standard heading-based extraction
        else:
            extractor = StandardAreaExtractor(self.focus_areas_config)

        extractor.set_area_config(area_key, area_config)
        return extractor

    def get_all_extractors(self) -> Dict[str, BaseAreaExtractor]:
        """
        Create extractors for all configured areas.

        Returns:
            Dictionary mapping area keys to their extractors
        """
        extractors = {}

        for area_key, area_config in self.focus_areas_config.get('focus_areas', {}).items():
            extractors[area_key] = self.create_extractor(area_key, area_config)

        return extractors