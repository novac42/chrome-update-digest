"""
Chrome version detection using Chrome Developer Blog RSS feed.
This ensures we only detect versions that have published release notes.
"""

import requests
import feedparser
import re
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class RSSVersionDetector:
    """
    Detect Chrome versions from Chrome Developer Blog RSS feed.
    
    This approach ensures we only detect versions with published release notes,
    avoiding the issue where APIs show a version is released but release notes
    aren't published yet.
    """
    
    def __init__(self):
        """Initialize the RSS detector."""
        # Chrome Developer Blog RSS feed
        self.rss_url = "https://developer.chrome.com/blog/feed.xml"
        
        # Alternative RSS feeds as fallback
        self.fallback_feeds = [
            "https://developer.chrome.com/feeds/blog.xml",
            "https://chromestatus.com/features/feed.xml"
        ]
        
        # Patterns to identify version and channel from blog titles
        self.patterns = {
            'stable': re.compile(r'^New in Chrome (\d+)$', re.IGNORECASE),
            'beta': re.compile(r'^(?:New in Chrome|Chrome) (\d+) beta', re.IGNORECASE),
            'dev': re.compile(r'^(?:New in Chrome|Chrome) (\d+) dev', re.IGNORECASE),
            'canary': re.compile(r'^(?:New in Chrome|Chrome) (\d+) canary', re.IGNORECASE)
        }
    
    def detect_latest_versions(self, days_back: int = 30) -> Dict[str, List[Dict]]:
        """
        Detect Chrome versions from RSS feed.
        
        Args:
            days_back: Number of days to look back in the feed
            
        Returns:
            Dictionary with channels as keys and list of version info as values
            Each version info contains: version, title, link, published_date
        """
        versions = {
            'stable': [],
            'beta': [],
            'dev': [],
            'canary': []
        }
        
        # Try main RSS feed first
        feed_content = self._fetch_rss_feed(self.rss_url)
        
        # Try fallback feeds if main feed fails
        if not feed_content:
            for fallback_url in self.fallback_feeds:
                logger.info(f"Trying fallback feed: {fallback_url}")
                feed_content = self._fetch_rss_feed(fallback_url)
                if feed_content:
                    break
        
        if not feed_content:
            logger.error("Failed to fetch any RSS feed")
            return versions
        
        # Parse the feed
        feed = feedparser.parse(feed_content)
        
        if not feed.entries:
            logger.warning("No entries found in RSS feed")
            return versions
        
        # Check date threshold
        date_threshold = datetime.now() - timedelta(days=days_back)
        
        for entry in feed.entries:
            # Get entry details
            title = entry.get('title', '')
            link = entry.get('link', '')
            
            # Parse published date
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                published = datetime(*entry.updated_parsed[:6])
            
            # Skip old entries
            if published and published < date_threshold:
                continue
            
            # Check each channel pattern
            for channel, pattern in self.patterns.items():
                match = pattern.match(title)
                if match:
                    version = int(match.group(1))
                    version_info = {
                        'version': version,
                        'title': title,
                        'link': link,
                        'published_date': published.isoformat() if published else None,
                        'channel': channel
                    }
                    
                    # Avoid duplicates
                    if not any(v['version'] == version for v in versions[channel]):
                        versions[channel].append(version_info)
                        logger.info(f"Detected Chrome {version} {channel} from RSS: {title}")
                    break
        
        # Sort versions by version number (descending)
        for channel in versions:
            versions[channel].sort(key=lambda x: x['version'], reverse=True)
        
        return versions
    
    def _fetch_rss_feed(self, url: str) -> Optional[str]:
        """
        Fetch RSS feed content.
        
        Args:
            url: RSS feed URL
            
        Returns:
            Feed content as string or None
        """
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Chrome Release Monitor)'
            })
            
            if response.status_code == 200:
                return response.text
            else:
                logger.error(f"Failed to fetch RSS feed: HTTP {response.status_code}")
                
        except requests.RequestException as e:
            logger.error(f"Error fetching RSS feed: {e}")
        
        return None
    
    def get_latest_stable_version(self) -> Optional[int]:
        """
        Get the latest stable Chrome version from RSS.
        
        Returns:
            Latest stable version number or None
        """
        versions = self.detect_latest_versions(days_back=30)
        
        if versions['stable']:
            return versions['stable'][0]['version']
        
        return None
    
    def get_latest_beta_version(self) -> Optional[int]:
        """
        Get the latest beta Chrome version from RSS.
        
        Returns:
            Latest beta version number or None
        """
        versions = self.detect_latest_versions(days_back=30)
        
        if versions['beta']:
            return versions['beta'][0]['version']
        
        return None
    
    def check_version_published(self, version: int, channel: str = 'stable') -> bool:
        """
        Check if a specific version's release notes have been published.
        
        Args:
            version: Chrome version number
            channel: Chrome channel (stable, beta, dev, canary)
            
        Returns:
            True if the version's release notes are published
        """
        versions = self.detect_latest_versions(days_back=60)
        
        channel_versions = versions.get(channel, [])
        return any(v['version'] == version for v in channel_versions)
    
    def get_new_versions(self, known_versions: Dict[str, List[int]]) -> Dict[str, List[int]]:
        """
        Get new versions that aren't in the known versions list.
        
        Args:
            known_versions: Dictionary with channels as keys and lists of known version numbers
            
        Returns:
            Dictionary with channels as keys and lists of new version numbers
        """
        new_versions = {
            'stable': [],
            'beta': [],
            'dev': [],
            'canary': []
        }
        
        # Get current versions from RSS
        current_versions = self.detect_latest_versions(days_back=30)
        
        for channel in new_versions:
            known = set(known_versions.get(channel, []))
            current = [v['version'] for v in current_versions.get(channel, [])]
            
            # Find versions that are in current but not in known
            for version in current:
                if version not in known:
                    new_versions[channel].append(version)
                    logger.info(f"New Chrome {version} {channel} detected")
        
        return new_versions


def detect_chrome_from_rss() -> Dict[str, List[Dict]]:
    """
    Convenience function to detect Chrome versions from RSS.
    
    Returns:
        Dictionary with detected versions by channel
    """
    detector = RSSVersionDetector()
    return detector.detect_latest_versions()


def get_latest_stable_from_rss() -> Optional[int]:
    """
    Convenience function to get latest stable version from RSS.
    
    Returns:
        Latest stable version number or None
    """
    detector = RSSVersionDetector()
    return detector.get_latest_stable_version()


if __name__ == "__main__":
    # Test the RSS detector
    logging.basicConfig(level=logging.INFO)
    
    print("Chrome RSS Version Detection Test")
    print("=" * 50)
    
    detector = RSSVersionDetector()
    
    # Detect versions from last 30 days
    versions = detector.detect_latest_versions(days_back=30)
    
    print("\nDetected Chrome Versions from RSS:")
    for channel, version_list in versions.items():
        if version_list:
            print(f"\n{channel.upper()} Channel:")
            for v in version_list[:3]:  # Show top 3
                print(f"  Chrome {v['version']}: {v['title']}")
                if v['published_date']:
                    print(f"    Published: {v['published_date'][:10]}")
    
    # Get latest stable
    latest_stable = detector.get_latest_stable_version()
    if latest_stable:
        print(f"\nLatest stable version: Chrome {latest_stable}")
        
        # Check if it's published
        is_published = detector.check_version_published(latest_stable, 'stable')
        print(f"Release notes published: {is_published}")
    
    # Test new version detection
    print("\nTesting new version detection:")
    known = {'stable': [137, 138], 'beta': [138, 139]}
    new = detector.get_new_versions(known)
    
    for channel, versions in new.items():
        if versions:
            print(f"  New {channel} versions: {versions}")