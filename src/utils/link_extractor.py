"""
Link Extractor Module
Provides deterministic extraction of links from Chrome release notes markdown files.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict
from pathlib import Path
from enum import Enum


class LinkType(Enum):
    """Enumeration of link types found in release notes."""
    MDN = "mdn"
    CHROMESTATUS = "chromestatus"
    SPEC = "spec"
    TRACKING_BUG = "tracking_bug"
    GITHUB = "github"
    OTHER = "other"


@dataclass
class ExtractedLink:
    """Represents a single extracted link with metadata."""
    url: str
    link_type: LinkType
    title: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "url": self.url,
            "link_type": self.link_type.value,
            "title": self.title
        }


@dataclass
class ExtractedFeature:
    """Represents a feature extracted from release notes with all its metadata."""
    title: str
    content: str
    heading_path: List[str]
    links: List[ExtractedLink] = field(default_factory=list)
    line_number: int = 0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            "title": self.title,
            "content": self.content,
            "heading_path": self.heading_path,
            "links": [link.to_dict() for link in self.links],
            "line_number": self.line_number
        }


class LinkExtractor:
    """Extract links and features from Chrome release notes markdown."""
    
    # Regex patterns for different link types
    REFERENCE_PATTERN = re.compile(
        r'\*\*References:\*\*\s*(.+?)(?=\n\n|\n#|\Z)', 
        re.DOTALL | re.MULTILINE
    )
    
    # Pattern to extract individual links from references
    LINK_PATTERN = re.compile(
        r'\[([^\]]*)\]\(([^)]+)\)'
    )
    
    # Pattern to match heading lines
    HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    
    def __init__(self):
        """Initialize the LinkExtractor."""
        self.link_type_patterns = {
            LinkType.MDN: [
                r'developer\.mozilla\.org',
                r'mdn\.io'
            ],
            LinkType.CHROMESTATUS: [
                r'chromestatus\.com',
                r'chromestatus\.appspot\.com'
            ],
            LinkType.SPEC: [
                r'www\.w3\.org',
                r'w3c\.github\.io',
                r'wicg\.github\.io',
                r'whatwg\.org',
                r'whatpr\.org'
            ],
            LinkType.TRACKING_BUG: [
                r'bugs\.chromium\.org',
                r'crbug\.com'
            ],
            LinkType.GITHUB: [
                r'github\.com',
                r'github\.io'
            ]
        }
    
    def extract_from_file(self, file_path: Path) -> List[ExtractedFeature]:
        """
        Extract features and links from a markdown file.
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            List of extracted features with their links
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.extract_from_content(content)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return []
    
    def extract_from_content(self, content: str) -> List[ExtractedFeature]:
        """
        Extract features and links from markdown content.
        
        Args:
            content: Markdown content as string
            
        Returns:
            List of extracted features with their links
        """
        features = []
        lines = content.split('\n')
        
        # Build heading hierarchy
        heading_stack = []
        current_feature = None
        current_content_lines = []
        
        for i, line in enumerate(lines, 1):
            # Check if this is a heading
            heading_match = self.HEADING_PATTERN.match(line)
            
            if heading_match:
                # Save previous feature if exists
                if current_feature and current_content_lines:
                    current_feature.content = '\n'.join(current_content_lines).strip()
                    # Extract links from the feature content
                    current_feature.links = self._extract_links_from_text(current_feature.content)
                    if current_feature.title and current_feature.content:
                        features.append(current_feature)
                
                # Process heading hierarchy
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()
                
                # Update heading stack
                while len(heading_stack) > 0 and heading_stack[-1][0] >= level:
                    heading_stack.pop()
                heading_stack.append((level, title))
                
                # Create new feature for level 3 headings (###)
                if level == 3:
                    heading_path = [h[1] for h in heading_stack]
                    current_feature = ExtractedFeature(
                        title=title,
                        content="",
                        heading_path=heading_path,
                        line_number=i
                    )
                    current_content_lines = []
                else:
                    current_feature = None
                    current_content_lines = []
            
            elif current_feature is not None:
                # Accumulate content for current feature
                current_content_lines.append(line)
        
        # Don't forget the last feature
        if current_feature and current_content_lines:
            current_feature.content = '\n'.join(current_content_lines).strip()
            current_feature.links = self._extract_links_from_text(current_feature.content)
            if current_feature.title and current_feature.content:
                features.append(current_feature)
        
        return features
    
    def _extract_links_from_text(self, text: str) -> List[ExtractedLink]:
        """
        Extract links from a text block, particularly from References sections.
        
        Args:
            text: Text content that may contain a References section
            
        Returns:
            List of extracted links
        """
        links = []
        
        # Look for References section
        ref_match = self.REFERENCE_PATTERN.search(text)
        if ref_match:
            references_text = ref_match.group(1)
            
            # Extract all markdown links from references
            for link_match in self.LINK_PATTERN.finditer(references_text):
                link_text = link_match.group(1).strip()
                url = link_match.group(2).strip()
                
                if self._is_valid_url(url):
                    link_type = self._categorize_link(url)
                    links.append(ExtractedLink(
                        url=url,
                        link_type=link_type,
                        title=link_text if link_text else None
                    ))
        
        # Also extract any inline links not in References section
        for link_match in self.LINK_PATTERN.finditer(text):
            url = link_match.group(2).strip()
            link_text = link_match.group(1).strip()
            
            # Skip if already found in references
            if not any(link.url == url for link in links):
                if self._is_valid_url(url) and not url.startswith('#'):
                    link_type = self._categorize_link(url)
                    links.append(ExtractedLink(
                        url=url,
                        link_type=link_type,
                        title=link_text if link_text else None
                    ))
        
        return links
    
    def _categorize_link(self, url: str) -> LinkType:
        """
        Categorize a URL into one of the predefined link types.
        
        Args:
            url: URL to categorize
            
        Returns:
            LinkType enum value
        """
        url_lower = url.lower()
        
        for link_type, patterns in self.link_type_patterns.items():
            for pattern in patterns:
                if re.search(pattern, url_lower):
                    return link_type
        
        return LinkType.OTHER
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Check if a string is a valid URL.
        
        Args:
            url: String to validate
            
        Returns:
            True if valid URL, False otherwise
        """
        if not url:
            return False
        
        # Basic URL validation
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        
        return bool(url_pattern.match(url))
    
    def extract_links_summary(self, features: List[ExtractedFeature]) -> Dict:
        """
        Generate a summary of extracted links.
        
        Args:
            features: List of extracted features
            
        Returns:
            Dictionary with summary statistics
        """
        total_features = len(features)
        total_links = sum(len(f.links) for f in features)
        
        link_type_counts = {}
        for feature in features:
            for link in feature.links:
                link_type = link.link_type.value
                link_type_counts[link_type] = link_type_counts.get(link_type, 0) + 1
        
        features_with_links = sum(1 for f in features if f.links)
        
        return {
            "total_features": total_features,
            "total_links": total_links,
            "features_with_links": features_with_links,
            "features_without_links": total_features - features_with_links,
            "link_type_distribution": link_type_counts,
            "average_links_per_feature": total_links / total_features if total_features > 0 else 0
        }


if __name__ == "__main__":
    # Example usage
    from pathlib import Path
    
    # Test with a sample file
    test_file = Path("upstream_docs/release_notes/webplatform/chrome-138.md")
    
    if test_file.exists():
        extractor = LinkExtractor()
        features = extractor.extract_from_file(test_file)
        
        print(f"Extracted {len(features)} features from {test_file.name}")
        
        # Show summary
        summary = extractor.extract_links_summary(features)
        print("\nSummary:")
        print(f"  Total features: {summary['total_features']}")
        print(f"  Total links: {summary['total_links']}")
        print(f"  Features with links: {summary['features_with_links']}")
        print(f"  Link type distribution: {summary['link_type_distribution']}")
        
        # Show first few features as examples
        print("\nFirst 3 features:")
        for feature in features[:3]:
            print(f"\n  Title: {feature.title}")
            print(f"  Path: {' > '.join(feature.heading_path)}")
            print(f"  Links: {len(feature.links)}")
            for link in feature.links:
                print(f"    - [{link.link_type.value}] {link.url[:60]}...")