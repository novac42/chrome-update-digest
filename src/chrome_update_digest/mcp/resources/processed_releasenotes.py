"""
Processed Release Notes Resource Handler
Provides MCP resource access to processed Chrome release notes
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime


class ProcessedReleaseNotesResource:
    """Resource handler for processed release notes"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.processed_path = base_path / "upstream_docs" / "processed_releasenotes"
        self.feature_details_path = base_path / "feature_details"
        
        # Define resource categories
        self.categories = {
            "features": "Chrome feature updates",
            "processed_forwebplatform": "Web platform and developer updates",
            "processed_given_feature": "Feature-specific reports"
        }
        
        # Tag mappings for auto-tagging
        self.tag_mappings = {
            "security": ["security", "safe", "protect", "2sv", "authentication"],
            "webplatform": ["webplatform", "web", "api", "css", "javascript"],
            "ai": ["ai", "ml", "machine-learning", "artificial"],
            "webgpu": ["webgpu", "gpu", "graphics"],
            "profile": ["profile", "user", "sync"],
            "performance": ["performance", "speed", "optimization", "faster"],
            "devices": ["device", "hardware", "sensor", "usb", "bluetooth"]
        }
    
    def list_resources(self) -> List[Dict[str, Any]]:
        """List all available processed release note resources"""
        resources = []
        
        # Define paths to check - features and processed_given_feature will be in feature_details
        paths_to_check = []
        
        # Add old processed_releasenotes path for webplatform docs
        if self.processed_path.exists():
            # Only check non-feature subdirectories in the old location
            for item in self.processed_path.iterdir():
                if item.is_dir() and item.name not in ["features", "processed_given_feature", "processed_forenterprise"]:
                    paths_to_check.append((self.processed_path, item.name))
        
        # Add feature_details path for features and processed_given_feature
        if self.feature_details_path.exists():
            for subdir in ["features", "processed_given_feature"]:
                feature_subdir = self.feature_details_path / subdir
                if feature_subdir.exists():
                    paths_to_check.append((self.feature_details_path, subdir))
        
        # Also check if features/processed_given_feature still exist in old location (during migration)
        for subdir in ["features", "processed_given_feature"]:
            old_path = self.processed_path / subdir
            if old_path.exists():
                paths_to_check.append((self.processed_path, subdir))
        
        # Process each path
        for base_path, subdir in paths_to_check:
            search_path = base_path / subdir if subdir else base_path
            
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file.endswith('.md'):
                        file_path = Path(root) / file
                        
                        # Calculate relative path based on which base we're using
                        if base_path == self.feature_details_path:
                            # For feature_details, include the subdirectory in the relative path
                            relative_path = file_path.relative_to(base_path)
                        else:
                            # For processed_releasenotes, use the standard relative path
                            relative_path = file_path.relative_to(self.processed_path)
                        
                        # Create resource URI - always use processed_releasenotes for backward compatibility
                        uri = f"upstream://processed_releasenotes/{relative_path.as_posix()}"
                        
                        # Extract metadata from path and filename
                        metadata = self._extract_metadata(relative_path, file)
                        
                        # Generate tags based on path and content
                        tags = self._generate_tags(relative_path, file, metadata)
                        
                        # Generate description based on metadata
                        description = self._generate_description(metadata, file)
                        
                        # Get file stats
                        file_stats = file_path.stat()
                        
                        resources.append({
                            "uri": uri,
                            "name": file,
                            "description": description,
                            "mimeType": "text/markdown",
                            "_meta": {
                                "_fastmcp": {
                                    "tags": tags,
                                    "created_at": datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                                    "modified_at": datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                                    "size": file_stats.st_size,
                                    "category": metadata.get("category"),
                                    "version": metadata.get("version"),
                                    "subcategory": metadata.get("subcategory")
                                }
                            }
                        })
        
        # Remove duplicates (in case both old and new paths exist during migration)
        seen_uris = set()
        unique_resources = []
        for resource in resources:
            if resource["uri"] not in seen_uris:
                seen_uris.add(resource["uri"])
                unique_resources.append(resource)
        
        return sorted(unique_resources, key=lambda r: r["uri"])
    
    def read_resource(self, uri: str) -> str:
        """Read content of a specific resource"""
        # Parse URI to get file path
        if not uri.startswith("upstream://processed_releasenotes/"):
            raise ValueError(f"Invalid resource URI: {uri}")
        
        relative_path = uri.replace("upstream://processed_releasenotes/", "")
        
        # Check if this is a features or processed_given_feature path
        path_parts = Path(relative_path).parts
        file_path = None
        
        if path_parts and path_parts[0] in ["features", "processed_given_feature"]:
            # Try new location first
            new_path = self.feature_details_path / relative_path
            if new_path.exists():
                file_path = new_path
            else:
                # Fall back to old location
                file_path = self.processed_path / relative_path
        else:
            # Other categories remain in processed_releasenotes
            file_path = self.processed_path / relative_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"Resource not found: {uri}")
        
        if not file_path.is_file():
            raise ValueError(f"Resource is not a file: {uri}")
        
        # Security check: ensure file is within allowed directories
        try:
            resolved_path = file_path.resolve()
            # Check if file is in either processed_releasenotes or feature_details
            is_in_processed = False
            is_in_features = False
            
            try:
                resolved_path.relative_to(self.processed_path.resolve())
                is_in_processed = True
            except ValueError:
                pass
            
            try:
                resolved_path.relative_to(self.feature_details_path.resolve())
                is_in_features = True
            except ValueError:
                pass
            
            if not (is_in_processed or is_in_features):
                raise ValueError(f"Access denied to resource outside allowed directories: {uri}")
        except Exception as e:
            if "Access denied" in str(e):
                raise
            raise ValueError(f"Security check failed for resource: {uri}")
        
        # Read and return file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Failed to read resource {uri}: {e}")
    
    def _extract_metadata(self, relative_path: Path, filename: str) -> Dict[str, Optional[str]]:
        """Extract metadata from file path and name"""
        metadata = {
            "category": None,
            "version": None,
            "feature_type": None,
            "subcategory": None
        }
        
        parts = relative_path.parts
        
        # Extract category
        if parts and parts[0] in self.categories:
            metadata["category"] = parts[0]
        
        # Extract version from filename or path
        version_match = re.search(r'(?:profile-)?(\d+)', str(relative_path))
        if version_match:
            metadata["version"] = version_match.group(1)
        
        # Extract feature type for features category
        if metadata["category"] == "features" and len(parts) > 1:
            # e.g., features/profile-137/feature-name.md
            metadata["feature_type"] = parts[1].replace(f"profile-{metadata['version']}", "").strip("-") or "profile"
        
        # Extract subcategory from filename patterns
        if "webplatform" in filename.lower() or "webgpu" in filename.lower():
            metadata["subcategory"] = "webplatform"
        elif "profile" in filename.lower():
            metadata["subcategory"] = "profile"
        
        return metadata
    
    def _generate_description(self, metadata: Dict[str, Optional[str]], filename: str) -> str:
        """Generate a descriptive string based on metadata"""
        parts = []
        
        if metadata["version"]:
            parts.append(f"Chrome {metadata['version']}")
        
        if metadata["category"] in self.categories:
            if metadata["category"] == "features":
                if metadata["subcategory"]:
                    parts.append(f"{metadata['subcategory'].title()} feature")
                else:
                    parts.append("Feature update")
            else:
                parts.append(self.categories[metadata["category"]])
        
        # Clean up filename for display
        clean_name = filename.replace(".md", "").replace("-", " ").title()
        
        if parts:
            return f"{' - '.join(parts)}: {clean_name}"
        else:
            return f"Chrome release notes: {clean_name}"
    
    def _generate_tags(self, relative_path: Path, filename: str, metadata: Dict[str, Optional[str]]) -> List[str]:
        """Generate tags based on file path, name and metadata"""
        tags = []
        
        # Add version tag
        if metadata.get("version"):
            tags.append(f"chrome-{metadata['version']}")
        
        # Add category tags
        if metadata.get("category"):
            tags.append(metadata["category"])
        
        # Add subcategory tags
        if metadata.get("subcategory"):
            tags.append(metadata["subcategory"])
        
        # Auto-detect tags from filename and path
        path_str = str(relative_path).lower()
        filename_lower = filename.lower()
        
        for tag_key, keywords in self.tag_mappings.items():
            for keyword in keywords:
                if keyword in path_str or keyword in filename_lower:
                    if tag_key not in tags:
                        tags.append(tag_key)
                    break
        
        # Add special tags for specific patterns
        if "profile-" in path_str:
            tags.append("profile")
        if "webgpu" in filename_lower:
            tags.append("webgpu")
        if "-organized_chromechanges-" in filename_lower:
            tags.append("organized")
        if "given_feature" in path_str:
            tags.append("feature-specific")
        
        return sorted(list(set(tags)))  # Remove duplicates and sort