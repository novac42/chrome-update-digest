"""
Feature Tagging Models and Service
Provides heading-based tagging for Chrome release note features.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
from enum import Enum
from src.utils.link_extractor import ExtractedFeature


class TagPriority(Enum):
    """Priority levels for feature tags."""
    PRIMARY = "primary"      # From direct heading
    SECONDARY = "secondary"  # From parent headings
    CROSS_CUTTING = "cross_cutting"  # From content analysis


@dataclass
class FeatureTag:
    """Represents a tag assigned to a feature."""
    name: str
    priority: TagPriority
    source: str  # 'heading', 'content', 'link'
    confidence: float = 1.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "priority": self.priority.value,
            "source": self.source,
            "confidence": self.confidence
        }


@dataclass
class TaggedFeature:
    """Feature with assigned tags and metadata."""
    feature: ExtractedFeature
    primary_tags: List[FeatureTag] = field(default_factory=list)
    cross_cutting_concerns: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "feature": self.feature.to_dict(),
            "primary_tags": [tag.to_dict() for tag in self.primary_tags],
            "cross_cutting_concerns": self.cross_cutting_concerns
        }
    
    def get_all_tag_names(self) -> Set[str]:
        """Get all unique tag names."""
        tag_names = {tag.name for tag in self.primary_tags}
        tag_names.update(self.cross_cutting_concerns)
        return tag_names


class HeadingBasedTagger:
    """Service for tagging features based on heading hierarchy and content."""
    
    def __init__(self):
        """Initialize the tagger with predefined tag mappings."""
        # Mapping from heading patterns to tag names
        self.heading_to_tag = {
            # Primary categories
            "css and ui": "css",
            "css": "css",
            "ui": "ui",
            "web apis": "webapi",
            "web api": "webapi",
            "javascript": "javascript",
            "js": "javascript",
            "devices": "devices",
            "device": "devices",
            "multimedia": "multimedia",
            "media": "multimedia",
            "performance": "performance",
            "perf": "performance",
            "security": "security",
            "service worker": "serviceworker",
            "serviceworker": "serviceworker",
            "deprecations and removals": "deprecation",
            "deprecation": "deprecation",
            "removal": "deprecation",
            
            # Additional categories
            "webgpu": "webgpu",
            "gpu": "webgpu",
            "storage": "storage",
            "network": "network",
            "privacy": "privacy",
            "accessibility": "accessibility",
            "a11y": "accessibility",
            "pwa": "pwa",
            "progressive web app": "pwa",
        }
        
        # Cross-cutting concern patterns
        self.cross_cutting_patterns = {
            "webgpu": [
                r'\bwebgpu\b', r'\bgpu\b', r'\bwgsl\b', r'\bcompute shader\b',
                r'\bvertex shader\b', r'\bfragment shader\b', r'\bgraphics pipeline\b',
                r'\bcompute pipeline\b', r'\bgpubuffer\b', r'\bgputexture\b',
                r'\bgpudevice\b', r'\bgpuadapter\b', r'\bdawn\b'
            ],
            "ai": [
                r'\bai\b', r'\bmachine learning\b', r'\bml\b', r'\btranslator api\b',
                r'\blanguage detector\b', r'\bsummarizer\b', r'\blanguage model\b',
                r'\bgenai\b', r'\bllm\b', r'\bneural\b'
            ],
            "security": [
                r'\bsecurity\b', r'\bcsp\b', r'\bcors\b', r'\bsamesite\b',
                r'\bintegrity\b', r'\bcrypto\b', r'\bencrypt\b', r'\bauthenticat\b',
                r'\bpermission\b', r'\bsandbox\b'
            ],
            "privacy": [
                r'\bprivacy\b', r'\btracking\b', r'\bcookie\b', r'\bfingerprint\b',
                r'\bthird-party\b', r'\buser-agent\b', r'\bclient hints\b'
            ],
            "experimental": [
                r'\bexperimental\b', r'\borigin trial\b', r'\bbehind flag\b',
                r'\bflag:\b', r'\benable-features\b'
            ],
            "enterprise": [
                r'\benterprise\b', r'\bpolicy\b', r'\bmanaged\b', r'\badmin\b',
                r'\bkiosk\b', r'\bdeployment\b'
            ]
        }
        
        # Compile regex patterns for efficiency
        self.compiled_patterns = {}
        for concern, patterns in self.cross_cutting_patterns.items():
            self.compiled_patterns[concern] = [
                re.compile(pattern, re.IGNORECASE) 
                for pattern in patterns
            ]
    
    def tag_feature(self, feature: ExtractedFeature) -> TaggedFeature:
        """
        Tag a feature based on its heading hierarchy and content.
        
        Args:
            feature: Extracted feature to tag
            
        Returns:
            Tagged feature with primary tags and cross-cutting concerns
        """
        tagged = TaggedFeature(feature=feature)
        
        # Extract primary tags from heading hierarchy
        tagged.primary_tags = self._extract_heading_tags(feature.heading_path)
        
        # Detect cross-cutting concerns from content
        tagged.cross_cutting_concerns = self._detect_cross_cutting_concerns(
            feature.title, 
            feature.content
        )
        
        return tagged
    
    def tag_features(self, features: List[ExtractedFeature]) -> List[TaggedFeature]:
        """
        Tag multiple features.
        
        Args:
            features: List of extracted features
            
        Returns:
            List of tagged features
        """
        return [self.tag_feature(feature) for feature in features]
    
    def _extract_heading_tags(self, heading_path: List[str]) -> List[FeatureTag]:
        """
        Extract tags from heading hierarchy.
        
        Args:
            heading_path: List of headings from root to feature
            
        Returns:
            List of feature tags
        """
        tags = []
        
        # Process each heading in the path
        for i, heading in enumerate(heading_path):
            heading_lower = heading.lower().strip()
            
            # Skip version headings (e.g., "Chrome 138 Release Notes")
            if re.match(r'^chrome \d+', heading_lower):
                continue
            
            # Check against known heading patterns
            for pattern, tag_name in self.heading_to_tag.items():
                if pattern in heading_lower:
                    # Determine priority based on position in hierarchy
                    if i == len(heading_path) - 1:
                        # Direct parent heading
                        priority = TagPriority.PRIMARY
                    elif i == len(heading_path) - 2:
                        # Grandparent heading
                        priority = TagPriority.PRIMARY
                    else:
                        # Higher level heading
                        priority = TagPriority.SECONDARY
                    
                    tag = FeatureTag(
                        name=tag_name,
                        priority=priority,
                        source="heading",
                        confidence=1.0
                    )
                    
                    # Avoid duplicate tags
                    if not any(t.name == tag_name for t in tags):
                        tags.append(tag)
                    break
        
        return tags
    
    def _detect_cross_cutting_concerns(self, title: str, content: str) -> List[str]:
        """
        Detect cross-cutting concerns from feature content.
        
        Args:
            title: Feature title
            content: Feature content
            
        Returns:
            List of detected cross-cutting concern names
        """
        concerns = []
        combined_text = f"{title} {content}"
        
        for concern, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(combined_text):
                    if concern not in concerns:
                        concerns.append(concern)
                    break
        
        return concerns
    
    def generate_tag_summary(self, tagged_features: List[TaggedFeature]) -> Dict:
        """
        Generate summary statistics for tagged features.
        
        Args:
            tagged_features: List of tagged features
            
        Returns:
            Dictionary with tag statistics
        """
        primary_tag_counts = {}
        cross_cutting_counts = {}
        features_by_tag = {}
        
        for tagged in tagged_features:
            # Count primary tags
            for tag in tagged.primary_tags:
                if tag.priority == TagPriority.PRIMARY:
                    tag_name = tag.name
                    primary_tag_counts[tag_name] = primary_tag_counts.get(tag_name, 0) + 1
                    
                    if tag_name not in features_by_tag:
                        features_by_tag[tag_name] = []
                    features_by_tag[tag_name].append(tagged.feature.title)
            
            # Count cross-cutting concerns
            for concern in tagged.cross_cutting_concerns:
                cross_cutting_counts[concern] = cross_cutting_counts.get(concern, 0) + 1
        
        return {
            "total_features": len(tagged_features),
            "primary_tag_distribution": primary_tag_counts,
            "cross_cutting_distribution": cross_cutting_counts,
            "features_by_primary_tag": features_by_tag,
            "untagged_features": sum(
                1 for t in tagged_features 
                if not t.primary_tags
            )
        }
    
    def filter_by_tags(
        self, 
        tagged_features: List[TaggedFeature], 
        include_tags: Optional[List[str]] = None,
        exclude_tags: Optional[List[str]] = None,
        include_cross_cutting: Optional[List[str]] = None
    ) -> List[TaggedFeature]:
        """
        Filter features by tags.
        
        Args:
            tagged_features: List of tagged features
            include_tags: Tags to include (if specified, only these are included)
            exclude_tags: Tags to exclude
            include_cross_cutting: Cross-cutting concerns to include
            
        Returns:
            Filtered list of tagged features
        """
        filtered = []
        
        for tagged in tagged_features:
            # Get all tag names for this feature
            tag_names = {tag.name for tag in tagged.primary_tags}
            
            # Apply include filter
            if include_tags and not any(tag in tag_names for tag in include_tags):
                continue
            
            # Apply exclude filter
            if exclude_tags and any(tag in tag_names for tag in exclude_tags):
                continue
            
            # Apply cross-cutting filter
            if include_cross_cutting:
                if not any(cc in tagged.cross_cutting_concerns 
                          for cc in include_cross_cutting):
                    continue
            
            filtered.append(tagged)
        
        return filtered


if __name__ == "__main__":
    # Example usage
    from pathlib import Path
    from src.utils.link_extractor import LinkExtractor
    
    # Test with a sample file
    test_file = Path("upstream_docs/release_notes/webplatform/chrome-138.md")
    
    if test_file.exists():
        # Extract features
        extractor = LinkExtractor()
        features = extractor.extract_from_file(test_file)
        
        # Tag features
        tagger = HeadingBasedTagger()
        tagged_features = tagger.tag_features(features)
        
        print(f"Tagged {len(tagged_features)} features")
        
        # Generate summary
        summary = tagger.generate_tag_summary(tagged_features)
        print("\nTag Summary:")
        print(f"  Primary tags: {summary['primary_tag_distribution']}")
        print(f"  Cross-cutting: {summary['cross_cutting_distribution']}")
        print(f"  Untagged: {summary['untagged_features']}")
        
        # Show examples
        print("\nExample tagged features:")
        for tagged in tagged_features[:3]:
            print(f"\n  Feature: {tagged.feature.title}")
            print(f"  Primary tags: {[t.name for t in tagged.primary_tags]}")
            print(f"  Cross-cutting: {tagged.cross_cutting_concerns}")