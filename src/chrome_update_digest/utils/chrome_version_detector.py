"""
Robust Chrome version detection using official APIs.
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class ChromeVersionDetector:
    """
    Robust Chrome version detection using multiple official sources.
    """
    
    def __init__(self):
        """Initialize the detector with API endpoints."""
        self.apis = {
            'version_history': {
                'url': 'https://versionhistory.googleapis.com/v1/chrome/platforms/{platform}/channels/{channel}/versions',
                'description': 'Google Chrome Version History API (most reliable)'
            },
            'omaha_proxy': {
                'url': 'https://omahaproxy.appspot.com/all.json',
                'description': 'OmahaProxy - Official Chrome version tracker'
            },
            'chromium_dash': {
                'url': 'https://chromiumdash.appspot.com/fetch_releases?channel={channel}&platform={platform}&num=10',
                'description': 'Chromium Dashboard API'
            }
        }
    
    def get_latest_stable_version(self) -> Optional[int]:
        """
        Get the latest stable Chrome version number.
        
        Returns:
            Latest Chrome major version number (e.g., 139) or None if detection fails
        """
        # Try each method in order of reliability
        version = self._get_version_from_history_api()
        if version:
            return version
            
        version = self._get_version_from_omaha()
        if version:
            return version
            
        version = self._get_version_from_chromium_dash()
        if version:
            return version
            
        logger.error("Failed to detect Chrome version from all sources")
        return None
    
    def _get_version_from_history_api(self) -> Optional[int]:
        """Get version from Google Chrome Version History API."""
        try:
            # Try multiple platforms to ensure we get a result
            platforms = ['win', 'mac', 'linux']
            
            for platform in platforms:
                url = self.apis['version_history']['url'].format(
                    platform=platform,
                    channel='stable'
                )
                
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'versions' in data and data['versions']:
                        latest = data['versions'][0]
                        version_str = latest.get('version', '')
                        if version_str:
                            # Extract major version number
                            major_version = int(version_str.split('.')[0])
                            logger.info(f"Chrome Version History API: Chrome {major_version} stable ({version_str})")
                            return major_version
                            
        except Exception as e:
            logger.error(f"Error fetching from Version History API: {e}")
        
        return None
    
    def _get_version_from_omaha(self) -> Optional[int]:
        """Get version from OmahaProxy API."""
        try:
            url = self.apis['omaha_proxy']['url']
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Look for Windows stable version (most commonly referenced)
                for os_data in data:
                    if os_data.get('os') in ['win', 'win64']:
                        for version in os_data.get('versions', []):
                            if version.get('channel') == 'stable':
                                version_str = version.get('current_version', '')
                                if version_str:
                                    major_version = int(version_str.split('.')[0])
                                    logger.info(f"OmahaProxy API: Chrome {major_version} stable ({version_str})")
                                    return major_version
                                    
        except Exception as e:
            logger.error(f"Error fetching from OmahaProxy: {e}")
        
        return None
    
    def _get_version_from_chromium_dash(self) -> Optional[int]:
        """Get version from Chromium Dashboard API."""
        try:
            url = self.apis['chromium_dash']['url'].format(
                channel='Stable',
                platform='Windows'
            )
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list) and len(data) > 0:
                    latest = data[0]
                    version_str = latest.get('version', '')
                    if version_str:
                        major_version = int(version_str.split('.')[0])
                        logger.info(f"Chromium Dashboard: Chrome {major_version} stable")
                        return major_version
                        
        except Exception as e:
            logger.error(f"Error fetching from Chromium Dashboard: {e}")
        
        return None
    
    def get_all_channels_info(self) -> Dict[str, Optional[int]]:
        """
        Get version information for all Chrome channels.
        
        Returns:
            Dictionary with channel names as keys and major version numbers as values
        """
        channels_info = {}
        
        try:
            url = self.apis['omaha_proxy']['url']
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Get Windows versions (most commonly referenced)
                for os_data in data:
                    if os_data.get('os') == 'win64':
                        for version in os_data.get('versions', []):
                            channel = version.get('channel', '').lower()
                            version_str = version.get('current_version', '')
                            if channel and version_str:
                                major_version = int(version_str.split('.')[0])
                                channels_info[channel] = major_version
                        break
                        
        except Exception as e:
            logger.error(f"Error fetching channel info: {e}")
        
        return channels_info
    
    def get_version_release_date(self, version: int) -> Optional[str]:
        """
        Get the release date for a specific Chrome version.
        
        Args:
            version: Major version number
            
        Returns:
            Release date string or None
        """
        try:
            # Check version history API
            url = f'https://versionhistory.googleapis.com/v1/chrome/platforms/win/channels/stable/versions'
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for ver in data.get('versions', []):
                    version_str = ver.get('version', '')
                    if version_str.startswith(f'{version}.'):
                        # The API doesn't directly provide dates, but we can infer from version order
                        return "Recently released"
                        
        except Exception as e:
            logger.error(f"Error fetching release date: {e}")
        
        return None


def detect_latest_chrome_version() -> Optional[int]:
    """
    Convenience function to detect the latest Chrome stable version.
    
    Returns:
        Latest Chrome major version number or None
    """
    detector = ChromeVersionDetector()
    return detector.get_latest_stable_version()


def get_all_chrome_channels() -> Dict[str, Optional[int]]:
    """
    Convenience function to get all Chrome channel versions.
    
    Returns:
        Dictionary with channel versions
    """
    detector = ChromeVersionDetector()
    return detector.get_all_channels_info()


if __name__ == "__main__":
    # Test the detector
    logging.basicConfig(level=logging.INFO)
    
    print("Chrome Version Detection Test")
    print("=" * 50)
    
    detector = ChromeVersionDetector()
    
    # Get latest stable
    latest = detector.get_latest_stable_version()
    print(f"\nLatest stable version: Chrome {latest}")
    
    # Get all channels
    channels = detector.get_all_channels_info()
    print("\nAll channels:")
    for channel, version in channels.items():
        print(f"  {channel}: Chrome {version}")