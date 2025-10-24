"""
MCP Tool for monitoring and crawling Chrome release notes.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from chrome_update_digest.utils.release_monitor_core import ReleaseMonitorCore

logger = logging.getLogger(__name__)


class ReleaseMonitorTool:
    """MCP tool for checking and crawling release notes."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.core = ReleaseMonitorCore(base_path)
        
    async def check_latest_releases(self, ctx, arguments: dict) -> str:
        """
        Check for latest available release versions and compare with local files.
        
        Parameters:
        - release_type: "webplatform" (default: "webplatform")
        - channel: "stable" | "beta" | "dev" | "canary" (default: "stable")
        
        Returns JSON with latest versions and missing releases.
        """
        # Input validation
        SUPPORTED_RELEASE_TYPES = ["webplatform"]
        SUPPORTED_CHANNELS = ["stable", "beta", "dev", "canary"]
        
        release_type = arguments.get("release_type", "webplatform")
        channel = arguments.get("channel", "stable")
        
        # Validate release_type
        if release_type not in SUPPORTED_RELEASE_TYPES:
            return json.dumps({
                "status": "error",
                "error": f"Unsupported release_type: {release_type}. Must be one of: {', '.join(SUPPORTED_RELEASE_TYPES)}"
            })
        
        # Validate channel
        if channel not in SUPPORTED_CHANNELS:
            return json.dumps({
                "status": "error", 
                "error": f"Unsupported channel: {channel}. Must be one of: {', '.join(SUPPORTED_CHANNELS)}"
            })
        
        try:
            # Scan existing local versions with channel
            existing_versions = self.core.scan_existing_versions(channel)
            
            results = {
                "webplatform": {},
                "channel": channel,
                "status": "success"
            }
            
            # Check WebPlatform releases
            if release_type == "webplatform":
                # Check Chrome
                latest_chrome = self.core.detect_latest_webplatform_version()
                if latest_chrome:
                    local_chrome_versions = [v for v in existing_versions["webplatform"] 
                                           if v >= 100]  # Filter to Chrome versions
                    results["webplatform"]["chrome"] = {
                        "latest_available": latest_chrome,
                        "latest_local": max(local_chrome_versions) if local_chrome_versions else None,
                        "is_missing": latest_chrome not in existing_versions["webplatform"]
                    }
                
                # Check for missing stable versions when beta exists
                if channel == "stable":
                    missing_stable = self.core.detect_missing_stable_versions()
                    if missing_stable:
                        results["webplatform"]["missing_stable_with_beta"] = missing_stable
                
                # Check WebGPU
                latest_webgpu = self.core.detect_latest_webgpu_version()
                if latest_webgpu:
                    # WebGPU versions are stored separately
                    webgpu_versions = existing_versions.get("webgpu", set())
                    results["webplatform"]["webgpu"] = {
                        "latest_available": latest_webgpu,
                        "latest_local": latest_webgpu if latest_webgpu in webgpu_versions else None,
                        "is_missing": latest_webgpu not in webgpu_versions
                    }
            
            
            # Add summary
            missing_releases = []
            if results["webplatform"].get("chrome", {}).get("is_missing"):
                missing_releases.append(f"Chrome {results['webplatform']['chrome']['latest_available']}")
            # Add missing stable versions where beta exists
            missing_stable = results["webplatform"].get("missing_stable_with_beta", [])
            for version in missing_stable:
                missing_releases.append(f"Chrome {version} (stable - beta exists)")
            if results["webplatform"].get("webgpu", {}).get("is_missing"):
                missing_releases.append(f"WebGPU {results['webplatform']['webgpu']['latest_available']}")
            
            results["summary"] = {
                "missing_releases": missing_releases,
                "recommendation": "Use crawl_missing_releases to download missing releases" if missing_releases else "All releases are up to date"
            }
            
            return json.dumps(results, indent=2)
            
        except Exception as e:
            logger.error(f"Error checking releases: {e}")
            return json.dumps({
                "status": "error",
                "error": str(e)
            }, indent=2)
    
    async def crawl_missing_releases(self, ctx, arguments: dict) -> str:
        """
        Crawl missing release notes after user confirmation.
        
        Parameters:
        - release_type: "webplatform" (default: "webplatform")
        - channel: "stable" | "beta" | "dev" | "canary" (default: "stable")
        - confirmed: boolean - Must be true to proceed with crawling
        - force_redownload: boolean (default: false) - Download even if file exists
        
        Returns JSON with download results.
        """
        # Input validation
        SUPPORTED_RELEASE_TYPES = ["webplatform"]
        SUPPORTED_CHANNELS = ["stable", "beta", "dev", "canary"]
        
        release_type = arguments.get("release_type", "webplatform")
        channel = arguments.get("channel", "stable")
        confirmed = arguments.get("confirmed", False)
        force_redownload = arguments.get("force_redownload", False)
        
        # Validate release_type
        if release_type not in SUPPORTED_RELEASE_TYPES:
            return json.dumps({
                "status": "error",
                "error": f"Unsupported release_type: {release_type}. Must be one of: {', '.join(SUPPORTED_RELEASE_TYPES)}"
            }, indent=2)
        
        # Validate channel
        if channel not in SUPPORTED_CHANNELS:
            return json.dumps({
                "status": "error",
                "error": f"Unsupported channel: {channel}. Must be one of: {', '.join(SUPPORTED_CHANNELS)}"
            }, indent=2)
        
        if not confirmed:
            return json.dumps({
                "status": "error",
                "error": "User confirmation required. Please set 'confirmed: true' to proceed with crawling."
            }, indent=2)
        
        try:
            # First check what's missing with the specified channel
            check_result = await self.check_latest_releases(ctx, {"release_type": release_type, "channel": channel})
            check_data = json.loads(check_result)
            
            if check_data.get("status") == "error":
                return check_result
            
            results = {
                "downloaded": [],
                "errors": [],
                "status": "success"
            }
            
            # Download WebPlatform releases
            if release_type == "webplatform":
                # Chrome
                chrome_info = check_data.get("webplatform", {}).get("chrome", {})
                if chrome_info.get("is_missing") or force_redownload:
                    version = chrome_info.get("latest_available")
                    if version:
                        download_result = self.core.download_chrome_release(version, channel)
                        if download_result["success"]:
                            file_path = download_result.get("file_path") or download_result.get("file")
                            description = f"Chrome {version} ({channel})"
                            if file_path:
                                description += f" -> {file_path}"
                            results["downloaded"].append(description)
                            self.core.update_version_tracking("chrome", version)
                        else:
                            results["errors"].append(download_result["error"])
                
                # WebGPU (no channel parameter - WebGPU doesn't have channels)
                webgpu_info = check_data.get("webplatform", {}).get("webgpu", {})
                if webgpu_info.get("is_missing") or force_redownload:
                    version = webgpu_info.get("latest_available")
                    if version:
                        download_result = self.core.download_webgpu_release(version)
                        if download_result["success"]:
                            file_path = download_result.get("file_path") or download_result.get("file")
                            description = f"WebGPU {version}"
                            if file_path:
                                description += f" -> {file_path}"
                            results["downloaded"].append(description)
                            self.core.update_version_tracking("webgpu", version)
                        else:
                            results["errors"].append(download_result["error"])
                
                # Download missing stable versions when beta exists
                if channel == "stable":
                    missing_stable = check_data.get("webplatform", {}).get("missing_stable_with_beta", [])
                    for version in missing_stable:
                        download_result = self.core.download_chrome_release(version, "stable")
                        if download_result["success"]:
                            file_path = download_result.get("file_path") or download_result.get("file")
                            description = f"Chrome {version} (stable)"
                            if file_path:
                                description += f" -> {file_path}"
                            results["downloaded"].append(description)
                            self.core.update_version_tracking("chrome", version)
                        else:
                            results["errors"].append(download_result["error"])
            
            
            # Set status based on results
            if results["errors"] and not results["downloaded"]:
                results["status"] = "failed"
            elif results["errors"]:
                results["status"] = "partial"
            
            return json.dumps(results, indent=2)
            
        except Exception as e:
            logger.error(f"Error crawling releases: {e}")
            return json.dumps({
                "status": "error",
                "error": str(e)
            }, indent=2)
