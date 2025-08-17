"""
MCP Tool for extracting profile-related features from Chrome Enterprise Release Notes.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ProfileFeatureExtractorTool:
    """MCP tool for extracting profile-related features."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.processed_dir = base_path / "upstream_docs" / "processed_releasenotes" / "processed_forenterprise"
        self.profile_keywords_path = base_path / "prompts" / "profile-keywords.txt"
        
    async def extract_profile_features(self, ctx, version: int, 
                                      output_format: str = "markdown",
                                      keywords_override: Optional[str] = None) -> str:
        """
        Extract profile-related features from enterprise release notes.
        
        Parameters:
        - version: Chrome version number
        - output_format: Output format ("markdown" | "json" | "yaml")
        - keywords_override: Optional custom keywords (comma-separated)
        
        Returns formatted profile features report.
        """
        try:
            # Import the processor here to avoid circular dependencies
            import sys
            sys.path.append(str(self.base_path))
            from src.processors.extract_profile_features import ProfileFeatureExtractor
            
            # Initialize extractor
            extractor = ProfileFeatureExtractor()
            
            # Override keywords if provided
            if keywords_override:
                extractor.keywords = set(k.strip() for k in keywords_override.split(','))
            
            # Find the processed file for this version
            yaml_file = self.processed_dir / f"chrome-{version}-enterprise.yaml"
            if not yaml_file.exists():
                return json.dumps({
                    "error": f"No processed data found for Chrome {version}",
                    "suggestion": "Please run the enterprise processor first"
                })
            
            # Extract features
            features = extractor.extract_from_yaml(str(yaml_file))
            
            if not features:
                return json.dumps({
                    "version": version,
                    "message": "No profile-related features found",
                    "keywords_used": list(extractor.keywords)
                })
            
            # Format output based on requested format
            if output_format == "json":
                return json.dumps({
                    "version": version,
                    "total_features": len(features),
                    "features": [
                        {
                            "title": f.title,
                            "relevance_score": f.relevance_score,
                            "matched_keywords": list(f.matched_keywords),
                            "content": f.content[:500] + "..." if len(f.content) > 500 else f.content
                        }
                        for f in features[:10]  # Limit to top 10 for JSON
                    ]
                }, indent=2)
            
            elif output_format == "yaml":
                import yaml
                return yaml.dump({
                    "version": version,
                    "extraction_date": datetime.now().isoformat(),
                    "total_features": len(features),
                    "features": [
                        {
                            "title": f.title,
                            "relevance_score": f.relevance_score,
                            "matched_keywords": list(f.matched_keywords),
                            "category": f.category,
                            "tags": list(f.tags) if hasattr(f, 'tags') else []
                        }
                        for f in features
                    ]
                }, default_flow_style=False)
            
            else:  # markdown (default)
                report = extractor.generate_report(features, version)
                return report
                
        except Exception as e:
            logger.error(f"Error extracting profile features: {e}")
            return json.dumps({
                "error": str(e),
                "version": version
            })