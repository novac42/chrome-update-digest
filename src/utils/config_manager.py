#!/usr/bin/env python3
"""
Configuration Manager for Chrome Release URL Management

This module provides centralized configuration management for Chrome and WebGPU
release note URLs, ensuring clean separation of concerns and easy maintenance.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages configuration settings, particularly for Chrome release URLs."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize ConfigManager.
        
        Args:
            config_dir: Path to configuration directory. If None, uses default location.
        """
        if config_dir is None:
            # Default to config directory relative to src directory
            self.config_dir = Path(__file__).parent.parent / "config"
        else:
            self.config_dir = Path(config_dir)
        
        self.urls_file = self.config_dir / "urls.json"
        self._urls_cache = None
    
    def load_urls(self) -> Dict[str, Any]:
        """
        Load URL configuration from JSON file.
        
        Returns:
            Dictionary containing URL configuration
            
        Raises:
            FileNotFoundError: If configuration file doesn't exist
            json.JSONDecodeError: If configuration file is invalid JSON
        """
        if self._urls_cache is None:
            if not self.urls_file.exists():
                raise FileNotFoundError(f"URL configuration file not found: {self.urls_file}")
            
            try:
                with open(self.urls_file, 'r', encoding='utf-8') as f:
                    self._urls_cache = json.load(f)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f"Invalid JSON in configuration file: {e}")
        
        return self._urls_cache
    
    
    def get_webplatform_base_url(self) -> str:
        """
        Get Chrome WebPlatform release notes base URL.
        
        Returns:
            Chrome WebPlatform base URL
        """
        urls = self.load_urls()
        return urls["chrome"]["webplatform"]["base_url"]
    
    def get_webplatform_version_url(self, version: int, channel: str = "stable") -> str:
        """
        Get Chrome WebPlatform release notes URL for specific version.
        
        Args:
            version: Chrome version number
            channel: Chrome channel (stable, beta, dev, canary)
            
        Returns:
            Chrome WebPlatform version-specific URL
        """
        urls = self.load_urls()
        
        if channel == "beta":
            # Beta has different URL pattern: /blog/chrome-{version}-beta
            return f"https://developer.chrome.com/blog/chrome-{version}-beta"
        else:
            # Stable uses /release-notes/{version}
            template = urls["chrome"]["webplatform"]["version_url_template"]
            return template.format(version=version)
    
    def get_webgpu_base_url(self) -> str:
        """
        Get WebGPU base URL for news and releases.
        
        Returns:
            WebGPU base URL
        """
        urls = self.load_urls()
        return urls["webgpu"]["base_url"]
    
    def get_webgpu_version_url(self, version: int) -> str:
        """
        Get WebGPU release notes URL for specific version.
        
        Args:
            version: WebGPU version number
            
        Returns:
            WebGPU version-specific URL
        """
        urls = self.load_urls()
        template = urls["webgpu"]["version_url_template"]
        return template.format(version=version)
    
    def reload_config(self):
        """Force reload of configuration from file."""
        self._urls_cache = None
        self.load_urls()
    
    def get_all_urls(self) -> Dict[str, Any]:
        """
        Get all URL configurations.
        
        Returns:
            Complete URL configuration dictionary
        """
        return self.load_urls()


# Global instance for easy access
_config_manager = None

def get_config_manager() -> ConfigManager:
    """
    Get global ConfigManager instance.
    
    Returns:
        ConfigManager singleton instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager




def get_webplatform_base_url() -> str:
    """Convenience function to get webplatform base URL."""
    return get_config_manager().get_webplatform_base_url()


def get_webplatform_version_url(version: int, channel: str = "stable") -> str:
    """Convenience function to get webplatform version URL."""
    return get_config_manager().get_webplatform_version_url(version, channel)


def get_webgpu_base_url() -> str:
    """Convenience function to get WebGPU base URL."""
    return get_config_manager().get_webgpu_base_url()


def get_webgpu_version_url(version: int) -> str:
    """Convenience function to get WebGPU version URL."""
    return get_config_manager().get_webgpu_version_url(version)