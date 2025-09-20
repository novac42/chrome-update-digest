#!/usr/bin/env python3
"""
Chrome & WebGPU Release Monitor

Main orchestrator for monitoring Chrome and WebGPU releases.
Reuses existing crawl infrastructure to detect new releases and download content.
"""

import json
import os
import sys
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from bs4 import BeautifulSoup
import html2text
from utils.config_manager import (
    get_webplatform_base_url, 
    get_webplatform_version_url,
    get_webgpu_base_url,
    get_webgpu_version_url
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('.monitoring/logs/monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ReleaseMonitor:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.monitoring_dir = self.base_dir / ".monitoring"
        self.versions_file = self.monitoring_dir / "versions.json"
        self.release_notes_dir = self.base_dir / "upstream_docs" / "release_notes" / "WebPlatform"
        
        # Ensure directories exist
        self.monitoring_dir.mkdir(exist_ok=True)
        (self.monitoring_dir / "logs").mkdir(exist_ok=True)
        
        # Load existing versions
        self.versions = self.load_versions()
        
    def load_versions(self) -> Dict:
        """Load version tracking data from JSON file."""
        if self.versions_file.exists():
            try:
                with open(self.versions_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error loading versions: {e}")
        
        # Default structure if file doesn't exist
        return {
            "chrome": [],
            "webgpu": [],
            "last_check": None
        }
    
    def save_versions(self):
        """Save version tracking data to JSON file."""
        from datetime import timezone
        self.versions["last_check"] = datetime.now(timezone.utc).isoformat()
        
        try:
            with open(self.versions_file, 'w') as f:
                json.dump(self.versions, f, indent=2)
            logger.info("Versions saved successfully")
        except IOError as e:
            logger.error(f"Error saving versions: {e}")
    
    def scan_existing_versions(self) -> Dict[str, Set[int]]:
        """Scan existing release note files to extract version numbers."""
        versions = {"chrome": set(), "webgpu": set()}
        
        search_dirs = [self.release_notes_dir]
        nested_dir = self.release_notes_dir / "webplatform"
        if nested_dir.exists():
            search_dirs.append(nested_dir)

        for directory in search_dirs:
            if not directory.exists():
                continue

            for file in directory.glob("chrome-*.md"):
                match = re.search(r'chrome-(\d+)', file.stem)
                if match:
                    versions["chrome"].add(int(match.group(1)))

            for file in directory.glob("webgpu-*.md"):
                match = re.search(r'webgpu-(\d+)', file.stem)
                if match:
                    versions["webgpu"].add(int(match.group(1)))
        
        logger.info(f"Found existing versions - Chrome: {sorted(versions['chrome'])}, WebGPU: {sorted(versions['webgpu'])}")
        return versions
    
    def detect_new_chrome_versions(self, existing_versions: Set[int]) -> List[int]:
        """Detect new Chrome versions using web scraping."""
        try:
            logger.info("Detecting Chrome versions...")
            available_versions = self._detect_chrome_versions_from_web()
            new_versions = [v for v in available_versions if v not in existing_versions]
            logger.info(f"New Chrome versions detected: {new_versions}")
            return new_versions
        except Exception as e:
            logger.error(f"Error detecting Chrome versions: {e}")
            return []
        
    
    def detect_new_webgpu_versions(self, existing_versions: Set[int]) -> List[int]:
        """Detect new WebGPU versions using web scraping."""
        try:
            logger.info("Detecting WebGPU versions...")
            available_versions = self._detect_webgpu_versions_from_web()
            new_versions = [v for v in available_versions if v not in existing_versions]
            logger.info(f"New WebGPU versions detected: {new_versions}")
            return new_versions
        except Exception as e:
            logger.error(f"Error detecting WebGPU versions: {e}")
            return []
    
    def _detect_chrome_versions_from_web(self) -> List[int]:
        """Detect available Chrome versions from RSS feed."""
        try:
            # Import RSS detector
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from src.utils.rss_version_detector import RSSVersionDetector
            
            detector = RSSVersionDetector()
            
            # Get versions from RSS (only stable and beta are relevant for release notes)
            versions_by_channel = detector.detect_latest_versions(days_back=60)
            
            all_versions = []
            
            # Collect stable versions (these are the main release notes)
            for version_info in versions_by_channel.get('stable', []):
                all_versions.append(version_info['version'])
                logger.info(f"RSS: Chrome {version_info['version']} stable - {version_info['title']}")
            
            # Also include beta versions
            for version_info in versions_by_channel.get('beta', []):
                all_versions.append(version_info['version'])
                logger.info(f"RSS: Chrome {version_info['version']} beta - {version_info['title']}")
            
            return sorted(list(set(all_versions)), reverse=True)  # Remove duplicates and sort descending
            
        except Exception as e:
            logger.error(f"Error detecting Chrome versions from RSS: {e}")
            
            # Fallback to old method if RSS fails
            logger.info("Falling back to web scraping method...")
            return self._detect_chrome_versions_from_web_fallback()
        
    def _detect_chrome_versions_from_web_fallback(self) -> List[int]:
        """Fallback method using web scraping."""
        try:
            url = get_webplatform_base_url()
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                versions = []
                
                # Look for version numbers in links and content
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    match = re.search(r'/release-notes/(\d+)/', href)
                    if match:
                        versions.append(int(match.group(1)))
                
                return sorted(list(set(versions)))
            
        except Exception as e:
            logger.error(f"Error in fallback web scraping: {e}")
        
        return []
    
    def _detect_webgpu_versions_from_web(self) -> List[int]:
        """Detect available WebGPU versions from web."""
        try:
            url = get_webgpu_base_url()
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                versions = []
                
                # Look for "New in WebGPU XX" patterns
                webgpu_pattern = re.compile(r'(?:New\s+in\s+)?WebGPU\s+(\d+)', re.IGNORECASE)
                for text in soup.stripped_strings:
                    matches = webgpu_pattern.findall(text)
                    for match in matches:
                        if int(match) >= 100:  # Filter reasonable version numbers
                            versions.append(int(match))
                
                # Also check for blog posts
                blog_pattern = re.compile(r'new-in-webgpu-(\d+)')
                for link in soup.find_all('a', href=True):
                    href = link.get('href', '')
                    matches = blog_pattern.findall(href)
                    for match in matches:
                        versions.append(int(match))
                
                return sorted(list(set(versions)))  # Remove duplicates and sort
            
        except Exception as e:
            logger.error(f"Error fetching WebGPU versions: {e}")
        
        return []
    
    def download_chrome_release(self, version: int, channel: str = None) -> bool:
        """Download Chrome release notes from web.
        
        Args:
            version: Chrome version number
            channel: Optional channel override. If None, will auto-detect from RSS
        """
        # Auto-detect channel if not provided
        if channel is None:
            # Check RSS to determine if this is stable or beta
            from src.utils.rss_version_detector import RSSVersionDetector
            detector = RSSVersionDetector()
            versions_info = detector.detect_latest_versions(days_back=60)
            
            # Check if this version is in stable or beta
            for stable_info in versions_info.get('stable', []):
                if stable_info['version'] == version:
                    channel = 'stable'
                    break
            
            if channel is None:
                for beta_info in versions_info.get('beta', []):
                    if beta_info['version'] == version:
                        channel = 'beta'
                        break
            
            # Default to stable if still not found
            if channel is None:
                channel = 'stable'
        
        logger.info(f"Downloading Chrome {version} {channel} release notes")
        
        try:
            url = get_webplatform_version_url(version, channel)
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find main content
                main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
                if not main_content:
                    logger.warning(f"Could not find main content for Chrome {version}")
                    return False
                
                # Convert to markdown
                h = html2text.HTML2Text()
                h.body_width = 0
                h.ignore_links = False
                h.ignore_images = False
                h.unicode_snob = True
                
                markdown_content = h.handle(str(main_content))
                
                # Clean up
                markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
                
                # Include channel in filename for non-stable versions
                if channel == 'beta':
                    output_file = self.release_notes_dir / f"chrome-{version}-beta.md"
                    title = f"# Chrome {version} Release Notes (Beta)\n\n"
                else:
                    output_file = self.release_notes_dir / f"chrome-{version}.md"
                    title = f"# Chrome {version} Release Notes\n\n"
                    
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(title)
                    f.write(f"Source: {url}\n\n")
                    f.write(markdown_content)
                
                logger.info(f"Chrome release notes saved: {output_file}")
                return True
            else:
                logger.error(f"Failed to fetch Chrome {version}: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error downloading Chrome release {version}: {e}")
            return False
    
    def download_webgpu_release(self, version: int) -> bool:
        """Download WebGPU release notes from web."""
        logger.info(f"Downloading WebGPU release notes for version {version}")
        
        try:
            url = get_webgpu_version_url(version)
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find main content
                main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
                if not main_content:
                    logger.warning(f"Could not find main content for WebGPU {version}")
                    return False
                
                # Convert to markdown
                h = html2text.HTML2Text()
                h.body_width = 0
                h.ignore_links = False
                h.ignore_images = False
                h.unicode_snob = True
                
                markdown_content = h.handle(str(main_content))
                
                # Clean up
                markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
                
                output_file = self.release_notes_dir / f"webgpu-{version}.md"
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"# WebGPU {version} Release Notes\n\n")
                    f.write(f"Source: {url}\n\n")
                    f.write(markdown_content)
                
                logger.info(f"WebGPU release notes saved: {output_file}")
                return True
            else:
                logger.error(f"Failed to fetch WebGPU {version}: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error downloading WebGPU release {version}: {e}")
            return False
    
    def run_monitoring(self):
        """Main monitoring loop."""
        logger.info("Starting release monitoring...")
        
        # Scan existing versions
        existing = self.scan_existing_versions()
        
        # Detect new versions
        new_chrome = self.detect_new_chrome_versions(set(existing["chrome"]))
        new_webgpu = self.detect_new_webgpu_versions(set(existing["webgpu"]))
        
        # Download new content
        downloaded_chrome = []
        downloaded_webgpu = []
        
        for version in new_chrome:
            if self.download_chrome_release(version):
                downloaded_chrome.append(version)
                self.versions["chrome"].append(version)
        
        for version in new_webgpu:
            if self.download_webgpu_release(version):
                downloaded_webgpu.append(version)
                self.versions["webgpu"].append(version)
        
        # Save updated versions
        if downloaded_chrome or downloaded_webgpu:
            self.save_versions()
            logger.info(f"Monitoring complete. Downloaded: Chrome {downloaded_chrome}, WebGPU {downloaded_webgpu}")
        else:
            logger.info("No new releases detected")
        
        return {
            "chrome": downloaded_chrome,
            "webgpu": downloaded_webgpu
        }

def main():
    """Main entry point."""
    monitor = ReleaseMonitor()
    results = monitor.run_monitoring()
    
    # Exit with appropriate code
    if results["chrome"] or results["webgpu"]:
        print(f"New releases detected: Chrome={results['chrome']}, WebGPU={results['webgpu']}")
        sys.exit(1)  # Exit with 1 to indicate new content for CI
    else:
        print("No new releases")
        sys.exit(0)

if __name__ == "__main__":
    main()
