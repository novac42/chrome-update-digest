"""
Core release monitoring functionality shared between scripts and MCP tools.
"""

import json
import logging
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple

import requests
from bs4 import BeautifulSoup
import html2text

# Cross-platform file locking support
try:
    import fcntl  # type: ignore
except ImportError:  # Windows
    fcntl = None  # type: ignore
    import msvcrt  # type: ignore


def _lock_file(f):
    """Acquire an exclusive lock on the file handle cross-platform."""
    if fcntl is not None:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    else:
        # On Windows, lock 1 byte from the start of the file
        try:
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
        except Exception:
            # Best-effort: if locking fails, proceed without strict locking
            pass


def _unlock_file(f):
    """Release a previously acquired lock cross-platform."""
    if fcntl is not None:
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    else:
        try:
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except Exception:
            pass

from utils.config_manager import (
    get_webplatform_base_url, 
    get_webplatform_version_url,
    get_webgpu_base_url,
    get_webgpu_version_url
)

logger = logging.getLogger(__name__)


class ReleaseMonitorCore:
    """Core functionality for monitoring Chrome and WebGPU releases."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.monitoring_dir = base_path / ".monitoring"
        self.versions_file = self.monitoring_dir / "versions.json"
        self.release_notes_dir = base_path / "upstream_docs" / "release_notes" / "WebPlatform"
        
        # Ensure directories exist
        self.monitoring_dir.mkdir(exist_ok=True)
        (self.monitoring_dir / "logs").mkdir(exist_ok=True)
        
    def scan_existing_versions(self, channel: str = "stable") -> Dict[str, Set[int]]:
        """Scan existing release note files to extract version numbers.
        
        Args:
            channel: Release channel for webplatform ("stable", "beta", "dev", "canary")
        """
        versions = {"webplatform": set(), "webgpu": set()}
        
        # Scan WebPlatform release notes
        webplatform_dir = self.release_notes_dir / "webplatform"
        if webplatform_dir.exists():
            # Chrome versions - handle stable vs channel-specific
            if channel == "stable":
                # For stable, look for chrome-XXX.md (without channel suffix)
                for file in webplatform_dir.glob("chrome-*.md"):
                    # Exclude files with channel suffixes (beta, dev, canary)
                    if re.search(r'-(?:beta|dev|canary)\.md$', file.name):
                        continue
                    match = re.search(r'chrome-(\d+)\.md$', file.name)
                    if match:
                        versions["webplatform"].add(int(match.group(1)))
            else:
                # For non-stable channels, look for chrome-XXX-channel.md
                for file in webplatform_dir.glob(f"chrome-*-{channel}.md"):
                    match = re.search(rf'chrome-(\d+)-{channel}\.md$', file.name)
                    if match:
                        versions["webplatform"].add(int(match.group(1)))
            
            # WebGPU versions - always without channel suffix (WebGPU doesn't have channels)
            for file in webplatform_dir.glob("webgpu-*.md"):
                match = re.search(r'webgpu-(\d+)\.md$', file.name)
                if match:
                    versions["webgpu"].add(int(match.group(1)))
        
        return versions
    
    def detect_missing_stable_versions(self) -> List[int]:
        """Detect Chrome stable versions that are missing when beta versions exist.
        
        Returns:
            List of Chrome version numbers that have beta but no stable release notes.
        """
        missing_stable = []
        
        webplatform_dir = self.release_notes_dir / "webplatform"
        if not webplatform_dir.exists():
            return missing_stable
        
        # Find all beta versions
        beta_versions = set()
        for file in webplatform_dir.glob("chrome-*-beta.md"):
            match = re.search(r'chrome-(\d+)-beta\.md$', file.name)
            if match:
                beta_versions.add(int(match.group(1)))
        
        # Find all stable versions (no channel suffix)
        stable_versions = set()
        for file in webplatform_dir.glob("chrome-*.md"):
            # Exclude files with channel suffixes
            if re.search(r'-(?:beta|dev|canary)\.md$', file.name):
                continue
            match = re.search(r'chrome-(\d+)\.md$', file.name)
            if match:
                stable_versions.add(int(match.group(1)))
        
        # Find versions that have beta but no stable
        for version in beta_versions:
            if version not in stable_versions:
                missing_stable.append(version)
        
        return sorted(missing_stable)
    
    def detect_latest_webplatform_version(self) -> Optional[int]:
        """Detect the latest available Chrome version from the web.
        
        Since the main release notes page doesn't list versions directly,
        we probe for the latest version by checking if version pages exist.
        """
        try:
            # Start from a known recent version and probe upwards
            # We can get a hint from existing local versions
            existing = self.scan_existing_versions("stable")
            chrome_versions = [v for v in existing["webplatform"] if v >= 100]
            
            # Start from the highest local version, or 135 as fallback
            start_version = max(chrome_versions) if chrome_versions else 135
            
            # Probe upwards to find the latest available version
            latest_found = None
            for version in range(start_version, start_version + 10):
                url = get_webplatform_version_url(version)
                try:
                    response = requests.head(url, timeout=5, allow_redirects=True)
                    if response.status_code == 200:
                        latest_found = version
                        logger.debug(f"Chrome {version} exists")
                    else:
                        logger.debug(f"Chrome {version} not found (status {response.status_code})")
                        # If we found at least one version and this one doesn't exist, we're done
                        if latest_found and latest_found >= start_version:
                            break
                except requests.RequestException:
                    # If we found versions and hit an error, return what we have
                    if latest_found:
                        break
                    continue
            
            if latest_found:
                logger.info(f"Detected latest Chrome version: {latest_found}")
                return latest_found
            
            # Fallback: Try to get version from the blog page
            logger.info("Probing failed, trying blog page as fallback")
            blog_url = "https://developer.chrome.com/blog"
            response = requests.get(blog_url, timeout=10)
            if response.status_code == 200:
                # Look for "New in Chrome XXX" which indicates stable releases
                matches = re.findall(r'New in Chrome\s+(\d{3})', response.text, re.IGNORECASE)
                if matches:
                    versions = [int(m) for m in matches if 100 <= int(m) <= 200]
                    if versions:
                        return max(versions)
                        
        except Exception as e:
            logger.error(f"Error detecting latest Chrome version: {e}")
        
        return None
    
    def detect_latest_webgpu_version(self) -> Optional[int]:
        """Detect the latest available WebGPU version from the web."""
        try:
            url = get_webgpu_base_url()
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            versions = []
            
            # Look for "New in WebGPU XX" patterns
            webgpu_pattern = re.compile(r'(?:New\s+in\s+)?WebGPU\s+(\d+)', re.IGNORECASE)
            for text in soup.stripped_strings:
                matches = webgpu_pattern.findall(text)
                for match in matches:
                    ver = int(match)
                    if ver >= 100:  # Filter reasonable version numbers
                        versions.append(ver)
            
            # Also check for blog posts
            blog_pattern = re.compile(r'new-in-webgpu-(\d+)')
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                matches = blog_pattern.findall(href)
                for match in matches:
                    versions.append(int(match))
            
            if versions:
                return max(versions)  # Return the highest version number
                
        except Exception as e:
            logger.error(f"Error detecting latest WebGPU version: {e}")
        
        return None
    
    
    def download_chrome_release(self, version: int, channel: str = "stable") -> Dict[str, any]:
        """Download Chrome release notes.
        
        Args:
            version: Chrome version number
            channel: Release channel ("stable", "beta", "dev", "canary")
        """
        try:
            # Pass channel to get correct URL
            url = get_webplatform_version_url(version, channel)
            logger.info(f"Downloading Chrome {version} {channel} from: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            if not main_content:
                return {
                    "success": False,
                    "error": f"Could not find main content for Chrome {version}"
                }
            
            # Convert to markdown
            h = html2text.HTML2Text()
            h.body_width = 0
            h.ignore_links = False
            h.ignore_images = False
            h.unicode_snob = True
            
            markdown_content = h.handle(str(main_content))
            
            # Clean up
            markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
            
            # Include channel suffix in filename for non-stable channels
            if channel == "stable":
                output_file = self.release_notes_dir / "webplatform" / f"chrome-{version}.md"
            else:
                output_file = self.release_notes_dir / "webplatform" / f"chrome-{version}-{channel}.md"
                
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Chrome {version} Release Notes ({channel.capitalize()})\n\n")
                f.write(f"Source: {url}\n\n")
                f.write(markdown_content)
            
            return {
                "success": True,
                "file_path": str(output_file),
                "url": url
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error downloading Chrome release {version}: {str(e)}"
            }
    
    def download_webgpu_release(self, version: int) -> Dict[str, any]:
        """Download WebGPU release notes.
        
        Args:
            version: WebGPU version number
        
        Note: WebGPU doesn't have release channels, always downloads as stable.
        """
        try:
            url = get_webgpu_version_url(version)
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            if not main_content:
                return {
                    "success": False,
                    "error": f"Could not find main content for WebGPU {version}"
                }
            
            # Convert to markdown
            h = html2text.HTML2Text()
            h.body_width = 0
            h.ignore_links = False
            h.ignore_images = False
            h.unicode_snob = True
            
            markdown_content = h.handle(str(main_content))
            
            # Clean up
            markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
            
            # WebGPU files never have channel suffix
            output_file = self.release_notes_dir / "webplatform" / f"webgpu-{version}.md"
                
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# WebGPU {version} Release Notes\n\n")
                f.write(f"Source: {url}\n\n")
                f.write(markdown_content)
            
            return {
                "success": True,
                "file_path": str(output_file),
                "url": url
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error downloading WebGPU release {version}: {str(e)}"
            }
    
    
    def update_version_tracking(self, release_type: str, version: int):
        """Update the version tracking JSON file with file locking for concurrent access protection."""
        versions = {}
        max_retries = 3
        retry_delay = 0.1  # 100ms
        
        # Ensure the file exists
        if not self.versions_file.exists():
            self.versions_file.parent.mkdir(parents=True, exist_ok=True)
            self.versions_file.write_text("{}")
        
        for attempt in range(max_retries):
            try:
                # Use file locking to prevent concurrent access issues
                with open(self.versions_file, 'r+') as f:
                    # Acquire exclusive lock (will block until lock is available)
                    _lock_file(f)
                    try:
                        # Read current content
                        f.seek(0)
                        content = f.read()
                        if content:
                            try:
                                versions = json.loads(content)
                            except json.JSONDecodeError:
                                logger.warning("Invalid JSON in version tracking file, resetting")
                                versions = {}
                        
                        # Initialize structure if needed
                        if "chrome" not in versions:
                            versions["chrome"] = []
                        if "webgpu" not in versions:
                            versions["webgpu"] = []
                        
                        # Add version if not already tracked
                        if release_type == "chrome" and version not in versions["chrome"]:
                            versions["chrome"].append(version)
                        elif release_type == "webgpu" and version not in versions["webgpu"]:
                            versions["webgpu"].append(version)
                        
                        # Update timestamp
                        versions["last_check"] = datetime.now(timezone.utc).isoformat()
                        
                        # Write updated content
                        f.seek(0)
                        f.truncate()
                        json.dump(versions, f, indent=2)
                        
                    finally:
                        # Release lock
                        _unlock_file(f)
                
                # Successfully updated
                return
                
            except IOError as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Error accessing version tracking file (attempt {attempt + 1}/{max_retries}): {e}")
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                else:
                    logger.error(f"Failed to update version tracking after {max_retries} attempts: {e}")