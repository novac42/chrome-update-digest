#!/usr/bin/env python3
"""
Validation script to compare deterministic extraction with current LLM output.
Helps validate the accuracy of the new extraction pipeline.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
import argparse
from datetime import datetime

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.yaml_pipeline import YAMLPipeline
from src.utils.link_extractor import LinkExtractor
from src.models.feature_tagging import HeadingBasedTagger


class ExtractionValidator:
    """Validates the extraction pipeline against existing outputs."""
    
    def __init__(self):
        self.yaml_pipeline = YAMLPipeline()
        self.link_extractor = LinkExtractor()
        self.tagger = HeadingBasedTagger()
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'files_processed': 0,
            'total_features': 0,
            'total_links': 0,
            'link_accuracy': {},
            'tag_coverage': {},
            'errors': []
        }
    
    def validate_file(self, markdown_path: Path) -> Dict:
        """
        Validate extraction for a single file.
        
        Args:
            markdown_path: Path to markdown release notes
            
        Returns:
            Validation results for this file
        """
        print(f"\nValidating: {markdown_path.name}")
        
        try:
            # Read markdown content
            with open(markdown_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract features
            features = self.link_extractor.extract_from_content(content)
            
            # Tag features
            tagged_features = []
            for feature in features:
                tagged = self.tagger.tag_feature(feature)
                tagged_features.append(tagged)
            
            # Collect statistics
            file_stats = {
                'file': markdown_path.name,
                'features_count': len(features),
                'links_count': sum(len(f.links) for f in features),
                'link_types': {},
                'tags': {},
                'validation_issues': []
            }
            
            # Analyze links
            for feature in features:
                for link in feature.links:
                    link_type = link.link_type
                    file_stats['link_types'][link_type] = file_stats['link_types'].get(link_type, 0) + 1
                    
                    # Validate URL format
                    if not link.url.startswith(('http://', 'https://')):
                        file_stats['validation_issues'].append({
                            'type': 'invalid_url_scheme',
                            'feature': feature.title,
                            'url': link.url
                        })
            
            # Analyze tags
            for tagged in tagged_features:
                for tag in tagged.primary_tags:
                    tag_name = tag.name
                    file_stats['tags'][tag_name] = file_stats['tags'].get(tag_name, 0) + 1
            
            # Check for features without tags
            untagged_count = sum(1 for t in tagged_features if not t.primary_tags)
            if untagged_count > 0:
                file_stats['validation_issues'].append({
                    'type': 'untagged_features',
                    'count': untagged_count
                })
            
            # Check for features without links
            linkless_count = sum(1 for f in features if not f.links)
            if linkless_count > 0:
                file_stats['validation_issues'].append({
                    'type': 'features_without_links',
                    'count': linkless_count
                })
            
            print(f"  - Features: {file_stats['features_count']}")
            print(f"  - Links: {file_stats['links_count']}")
            print(f"  - Link types: {file_stats['link_types']}")
            print(f"  - Tags: {file_stats['tags']}")
            
            if file_stats['validation_issues']:
                print(f"  - Issues: {len(file_stats['validation_issues'])}")
                for issue in file_stats['validation_issues']:
                    print(f"    - {issue['type']}: {issue.get('count', issue.get('url', ''))}")
            
            return file_stats
            
        except Exception as e:
            error_msg = f"Error processing {markdown_path.name}: {str(e)}"
            print(f"  ERROR: {error_msg}")
            self.results['errors'].append(error_msg)
            return None
    
    def validate_directory(self, directory: Path) -> None:
        """
        Validate all markdown files in a directory.
        
        Args:
            directory: Directory containing markdown files
        """
        markdown_files = list(directory.glob("*.md"))
        
        if not markdown_files:
            print(f"No markdown files found in {directory}")
            return
        
        print(f"Found {len(markdown_files)} markdown files to validate")
        
        all_link_types = {}
        all_tags = {}
        
        for md_file in markdown_files:
            stats = self.validate_file(md_file)
            
            if stats:
                self.results['files_processed'] += 1
                self.results['total_features'] += stats['features_count']
                self.results['total_links'] += stats['links_count']
                
                # Aggregate link types
                for link_type, count in stats['link_types'].items():
                    all_link_types[link_type] = all_link_types.get(link_type, 0) + count
                
                # Aggregate tags
                for tag, count in stats['tags'].items():
                    all_tags[tag] = all_tags.get(tag, 0) + count
        
        self.results['link_accuracy']['by_type'] = all_link_types
        self.results['tag_coverage']['by_tag'] = all_tags
    
    def generate_report(self, output_path: Path = None) -> None:
        """
        Generate validation report.
        
        Args:
            output_path: Optional path to save report
        """
        print("\n" + "="*60)
        print("VALIDATION REPORT")
        print("="*60)
        
        print(f"\nFiles Processed: {self.results['files_processed']}")
        print(f"Total Features: {self.results['total_features']}")
        print(f"Total Links: {self.results['total_links']}")
        
        if self.results['files_processed'] > 0:
            avg_features = self.results['total_features'] / self.results['files_processed']
            avg_links = self.results['total_links'] / self.results['files_processed']
            print(f"Average Features per File: {avg_features:.1f}")
            print(f"Average Links per File: {avg_links:.1f}")
        
        print("\nLink Distribution by Type:")
        for link_type, count in sorted(self.results['link_accuracy']['by_type'].items()):
            percentage = (count / self.results['total_links'] * 100) if self.results['total_links'] > 0 else 0
            print(f"  - {link_type}: {count} ({percentage:.1f}%)")
        
        print("\nTag Distribution:")
        for tag, count in sorted(self.results['tag_coverage']['by_tag'].items(), 
                                key=lambda x: x[1], reverse=True)[:10]:
            print(f"  - {tag}: {count}")
        
        if self.results['errors']:
            print(f"\nErrors Encountered: {len(self.results['errors'])}")
            for error in self.results['errors'][:5]:
                print(f"  - {error}")
        
        # Save report if requested
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2)
            print(f"\nReport saved to: {output_path}")
    
    def compare_with_existing(self, existing_digest_path: Path, new_yaml_path: Path) -> Dict:
        """
        Compare extracted links with existing digest.
        
        Args:
            existing_digest_path: Path to existing digest
            new_yaml_path: Path to new YAML extraction
            
        Returns:
            Comparison results
        """
        comparison = {
            'existing_file': existing_digest_path.name,
            'new_file': new_yaml_path.name,
            'link_comparison': {},
            'differences': []
        }
        
        # Load existing digest
        with open(existing_digest_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # Extract URLs from existing digest (simple regex)
        import re
        existing_urls = set(re.findall(r'https?://[^\s\)]+', existing_content))
        
        # Load new YAML
        yaml_data = self.yaml_pipeline.load_from_yaml(new_yaml_path)
        
        # Extract URLs from YAML
        new_urls = set()
        for feature in yaml_data.get('features', []):
            for link in feature.get('links', []):
                if isinstance(link, dict):
                    new_urls.add(link.get('url', ''))
        
        # Compare
        comparison['link_comparison'] = {
            'existing_count': len(existing_urls),
            'new_count': len(new_urls),
            'common': len(existing_urls & new_urls),
            'only_in_existing': len(existing_urls - new_urls),
            'only_in_new': len(new_urls - existing_urls)
        }
        
        # Calculate accuracy
        if existing_urls:
            accuracy = (len(existing_urls & new_urls) / len(existing_urls)) * 100
            comparison['link_comparison']['accuracy'] = f"{accuracy:.1f}%"
        
        print(f"\nComparison Results:")
        print(f"  Existing digest URLs: {len(existing_urls)}")
        print(f"  New extraction URLs: {len(new_urls)}")
        print(f"  Common URLs: {len(existing_urls & new_urls)}")
        print(f"  Only in existing: {len(existing_urls - new_urls)}")
        print(f"  Only in new: {len(new_urls - existing_urls)}")
        
        if existing_urls:
            print(f"  Accuracy: {accuracy:.1f}%")
        
        return comparison


def main():
    """Main entry point for validation script."""
    parser = argparse.ArgumentParser(description='Validate link extraction pipeline')
    parser.add_argument(
        '--input-dir',
        type=Path,
        default=Path('upstream_docs/release_notes/webplatform'),
        help='Directory containing markdown files to validate'
    )
    parser.add_argument(
        '--output-report',
        type=Path,
        help='Path to save validation report (JSON)'
    )
    parser.add_argument(
        '--compare-existing',
        type=Path,
        help='Path to existing digest for comparison'
    )
    parser.add_argument(
        '--compare-yaml',
        type=Path,
        help='Path to new YAML extraction for comparison'
    )
    
    args = parser.parse_args()
    
    validator = ExtractionValidator()
    
    # Run validation
    if args.compare_existing and args.compare_yaml:
        # Compare mode
        validator.compare_with_existing(args.compare_existing, args.compare_yaml)
    else:
        # Validation mode
        validator.validate_directory(args.input_dir)
        validator.generate_report(args.output_report)


if __name__ == '__main__':
    main()