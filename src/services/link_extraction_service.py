"""
Link Extraction Service
High-level API for extracting and managing links from Chrome release notes.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import hashlib

from src.utils.link_extractor import LinkExtractor, ExtractedFeature
from src.models.feature_tagging import HeadingBasedTagger, TaggedFeature


class LinkExtractionService:
    """High-level service for link extraction and feature tagging."""
    
    def __init__(self, base_path: Path):
        """
        Initialize the service.
        
        Args:
            base_path: Base path of the project
        """
        self.base_path = Path(base_path)
        self.release_notes_dir = self.base_path / "upstream_docs" / "release_notes" / "WebPlatform"
        self.cache_dir = self.base_path / ".cache" / "link_extraction"
        self.output_dir = self.base_path / "upstream_docs" / "processed_releasenotes" / "extracted_links"
        
        # Create directories if they don't exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize extractors
        self.link_extractor = LinkExtractor()
        self.tagger = HeadingBasedTagger()
    
    def extract_version(
        self, 
        version: str, 
        use_cache: bool = True,
        save_output: bool = True
    ) -> List[TaggedFeature]:
        """
        Extract and tag features for a specific Chrome version.
        
        Args:
            version: Chrome version number (e.g., "138")
            use_cache: Whether to use cached results if available
            save_output: Whether to save output to file
            
        Returns:
            List of tagged features
        """
        # Check cache first
        if use_cache:
            cached = self._load_from_cache(version)
            if cached:
                return cached
        
        # Find the release note file
        release_file = self.release_notes_dir / f"chrome-{version}.md"
        if not release_file.exists():
            print(f"Release notes not found for Chrome {version}")
            return []
        
        # Extract features
        features = self.link_extractor.extract_from_file(release_file)
        
        # Tag features
        tagged_features = self.tagger.tag_features(features)
        
        # Save to cache
        if use_cache:
            self._save_to_cache(version, tagged_features)
        
        # Save output if requested
        if save_output:
            self._save_output(version, tagged_features)
        
        return tagged_features
    
    def extract_all_versions(self, use_cache: bool = True) -> Dict[str, List[TaggedFeature]]:
        """
        Extract features from all available Chrome versions.
        
        Args:
            use_cache: Whether to use cached results
            
        Returns:
            Dictionary mapping version to tagged features
        """
        results = {}
        
        # Find all chrome-*.md files
        for release_file in sorted(self.release_notes_dir.glob("chrome-*.md")):
            # Extract version from filename
            version = release_file.stem.split('-')[1]
            
            print(f"Processing Chrome {version}...")
            tagged_features = self.extract_version(version, use_cache=use_cache)
            results[version] = tagged_features
        
        return results
    
    def generate_consolidated_report(self, versions: Optional[List[str]] = None) -> Dict:
        """
        Generate a consolidated report across multiple versions.
        
        Args:
            versions: List of versions to include (None for all)
            
        Returns:
            Consolidated report dictionary
        """
        if versions is None:
            # Get all available versions
            versions = [
                f.stem.split('-')[1] 
                for f in self.release_notes_dir.glob("chrome-*.md")
            ]
        
        all_features = []
        version_summaries = {}
        
        for version in versions:
            tagged_features = self.extract_version(version)
            all_features.extend(tagged_features)
            
            # Generate version summary
            summary = self.tagger.generate_tag_summary(tagged_features)
            version_summaries[version] = {
                "total_features": summary["total_features"],
                "total_links": sum(len(f.feature.links) for f in tagged_features),
                "primary_tags": summary["primary_tag_distribution"],
                "cross_cutting": summary["cross_cutting_distribution"]
            }
        
        # Generate overall statistics
        overall_summary = self.tagger.generate_tag_summary(all_features)
        
        # Link statistics
        total_links = sum(len(f.feature.links) for f in all_features)
        link_types = {}
        for feature in all_features:
            for link in feature.feature.links:
                link_type = link.link_type.value
                link_types[link_type] = link_types.get(link_type, 0) + 1
        
        return {
            "versions_analyzed": versions,
            "overall": {
                "total_features": len(all_features),
                "total_links": total_links,
                "link_type_distribution": link_types,
                "primary_tag_distribution": overall_summary["primary_tag_distribution"],
                "cross_cutting_distribution": overall_summary["cross_cutting_distribution"]
            },
            "by_version": version_summaries,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def validate_links(self, version: str) -> Dict:
        """
        Validate extracted links for a version.
        
        Args:
            version: Chrome version to validate
            
        Returns:
            Validation report
        """
        tagged_features = self.extract_version(version)
        
        validation_results = {
            "version": version,
            "total_features": len(tagged_features),
            "features_with_links": 0,
            "features_without_links": 0,
            "total_links": 0,
            "link_types": {},
            "invalid_links": [],
            "duplicate_links": {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        all_urls = []
        
        for tagged in tagged_features:
            feature = tagged.feature
            
            if feature.links:
                validation_results["features_with_links"] += 1
            else:
                validation_results["features_without_links"] += 1
            
            for link in feature.links:
                validation_results["total_links"] += 1
                
                # Count by type
                link_type = link.link_type.value
                validation_results["link_types"][link_type] = \
                    validation_results["link_types"].get(link_type, 0) + 1
                
                # Check for duplicates
                if link.url in all_urls:
                    if link.url not in validation_results["duplicate_links"]:
                        validation_results["duplicate_links"][link.url] = []
                    validation_results["duplicate_links"][link.url].append(feature.title)
                else:
                    all_urls.append(link.url)
                
                # Basic validation
                if not self.link_extractor._is_valid_url(link.url):
                    validation_results["invalid_links"].append({
                        "feature": feature.title,
                        "url": link.url
                    })
        
        # Calculate percentages
        if validation_results["total_links"] > 0:
            validation_results["summary"] = {
                "valid_link_percentage": 
                    (1 - len(validation_results["invalid_links"]) / validation_results["total_links"]) * 100,
                "duplicate_percentage": 
                    len(validation_results["duplicate_links"]) / validation_results["total_links"] * 100,
                "features_with_links_percentage": 
                    validation_results["features_with_links"] / validation_results["total_features"] * 100
            }
        
        return validation_results
    
    def generate_validation_report(self, version: str) -> Dict:
        """
        Generate a detailed validation report for a version.
        
        Args:
            version: Chrome version
            
        Returns:
            Validation report
        """
        return self.validate_links(version)
    
    def _get_cache_key(self, version: str) -> str:
        """Generate cache key for a version."""
        # Include file modification time in cache key
        release_file = self.release_notes_dir / f"chrome-{version}.md"
        if release_file.exists():
            mtime = release_file.stat().st_mtime
            return f"{version}_{mtime}"
        return version
    
    def _load_from_cache(self, version: str) -> Optional[List[TaggedFeature]]:
        """Load cached results for a version."""
        cache_key = self._get_cache_key(version)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Reconstruct tagged features from JSON
                tagged_features = []
                for item in data:
                    # This is simplified - in production, you'd properly deserialize
                    # For now, return None to skip cache
                    return None
                    
            except Exception as e:
                print(f"Error loading cache for {version}: {e}")
        
        return None
    
    def _save_to_cache(self, version: str, tagged_features: List[TaggedFeature]):
        """Save results to cache."""
        cache_key = self._get_cache_key(version)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            # Convert to JSON-serializable format
            data = [tagged.to_dict() for tagged in tagged_features]
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving cache for {version}: {e}")
    
    def _save_output(self, version: str, tagged_features: List[TaggedFeature]):
        """Save extracted and tagged features to output file."""
        output_file = self.output_dir / f"chrome-{version}-extracted.json"
        
        try:
            # Convert to JSON format with all metadata
            output_data = {
                "version": version,
                "extraction_timestamp": datetime.utcnow().isoformat(),
                "statistics": self.tagger.generate_tag_summary(tagged_features),
                "features": [tagged.to_dict() for tagged in tagged_features]
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"Saved extracted features to {output_file}")
            
        except Exception as e:
            print(f"Error saving output for {version}: {e}")
    
    def export_for_digest(self, version: str, focus_areas: Optional[List[str]] = None) -> Dict:
        """
        Export extracted data in format suitable for digest generation.
        
        Args:
            version: Chrome version
            focus_areas: Optional list of areas to focus on
            
        Returns:
            Dictionary with features organized for digest
        """
        tagged_features = self.extract_version(version)
        
        # Filter by focus areas if specified
        if focus_areas:
            tagged_features = self.tagger.filter_by_tags(
                tagged_features,
                include_tags=focus_areas
            )
        
        # Organize by primary tag
        organized = {}
        for tagged in tagged_features:
            # Get primary tag (or use "other" if none)
            primary_tag = "other"
            for tag in tagged.primary_tags:
                if tag.priority.value == "primary":
                    primary_tag = tag.name
                    break
            
            if primary_tag not in organized:
                organized[primary_tag] = []
            
            # Format feature for digest
            feature_data = {
                "title": tagged.feature.title,
                "content": tagged.feature.content,
                "links": [
                    {
                        "type": link.link_type.value,
                        "url": link.url,
                        "title": link.title
                    }
                    for link in tagged.feature.links
                ],
                "tags": [tag.name for tag in tagged.primary_tags],
                "cross_cutting": tagged.cross_cutting_concerns
            }
            
            organized[primary_tag].append(feature_data)
        
        return {
            "version": version,
            "total_features": len(tagged_features),
            "features_by_category": organized,
            "extraction_method": "deterministic",
            "timestamp": datetime.utcnow().isoformat()
        }


if __name__ == "__main__":
    # Example usage
    service = LinkExtractionService(Path("."))
    
    # Extract for Chrome 138
    version = "138"
    print(f"Extracting features for Chrome {version}...")
    
    tagged_features = service.extract_version(version)
    print(f"Extracted {len(tagged_features)} features")
    
    # Generate validation report
    validation = service.validate_links(version)
    print(f"\nValidation Report:")
    print(f"  Total features: {validation['total_features']}")
    print(f"  Total links: {validation['total_links']}")
    print(f"  Link types: {validation['link_types']}")
    
    if validation.get('summary'):
        print(f"  Valid links: {validation['summary']['valid_link_percentage']:.1f}%")
    
    # Export for digest
    digest_data = service.export_for_digest(version, focus_areas=["webapi", "css"])
    print(f"\nDigest export:")
    print(f"  Categories: {list(digest_data['features_by_category'].keys())}")
    for category, features in digest_data['features_by_category'].items():
        print(f"  {category}: {len(features)} features")