#!/usr/bin/env python3
"""
Validate the generated GitHub Pages navigation structure.
Checks for broken links, missing files, and structural integrity.
"""

import os
import re
from pathlib import Path
from typing import List, Set, Tuple

class GitHubPagesValidator:
    def __init__(self, digest_dir: str = "digest_markdown"):
        self.digest_dir = Path(digest_dir)
        self.errors = []
        self.warnings = []
        
    def extract_links(self, file_path: Path) -> List[str]:
        """Extract all markdown links from a file."""
        links = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Match markdown links [text](url)
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(pattern, content)
        
        for text, url in matches:
            # Skip external links and absolute paths (Chrome docs references)
            if (url.startswith('http://') or url.startswith('https://') or 
                url.startswith('/static/') or url.startswith('/docs/') or 
                url.startswith('/blog/') or url.startswith('/origintrials')):
                continue
            links.append(url)
            
        return links
    
    def resolve_link(self, from_file: Path, link: str) -> Path:
        """Resolve a relative link to an absolute path."""
        if link.startswith('/'):
            # Absolute link from digest_markdown root
            return self.digest_dir / link.lstrip('/')
        else:
            # Relative link from current file
            return (from_file.parent / link).resolve()
    
    def validate_file_links(self, file_path: Path) -> Tuple[int, int]:
        """Validate all links in a markdown file."""
        valid = 0
        broken = 0
        
        links = self.extract_links(file_path)
        relative_path = file_path.relative_to(self.digest_dir)
        
        for link in links:
            # Clean up link (remove anchors)
            clean_link = link.split('#')[0] if '#' in link else link
            
            if not clean_link:  # Anchor-only link
                continue
                
            resolved = self.resolve_link(file_path, clean_link)
            
            # Check if it's a directory link
            if clean_link.endswith('/'):
                # Should resolve to index.md
                index_file = resolved / 'index.md'
                if index_file.exists():
                    valid += 1
                else:
                    broken += 1
                    self.errors.append(f"{relative_path}: Broken link to {link} (no index.md)")
            else:
                # Add .md extension if missing and not .html
                if not resolved.suffix:
                    resolved = resolved.with_suffix('.md')
                elif resolved.suffix == '.html':
                    # Convert .html to .md for checking
                    resolved = resolved.with_suffix('.md')
                    
                if resolved.exists():
                    valid += 1
                else:
                    broken += 1
                    self.errors.append(f"{relative_path}: Broken link to {link}")
                    
        return valid, broken
    
    def validate_structure(self):
        """Validate the overall directory structure."""
        required_dirs = [
            self.digest_dir / 'versions',
            self.digest_dir / 'areas'
        ]
        
        required_files = [
            self.digest_dir / 'index.md',
            self.digest_dir / 'versions' / 'index.md',
            self.digest_dir / 'areas' / 'index.md',
            self.digest_dir / '_config.yml'
        ]
        
        for dir_path in required_dirs:
            if not dir_path.exists():
                self.errors.append(f"Missing required directory: {dir_path}")
                
        for file_path in required_files:
            if not file_path.exists():
                self.errors.append(f"Missing required file: {file_path}")
                
    def validate_front_matter(self, file_path: Path) -> bool:
        """Check if a markdown file has Jekyll front matter."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for Jekyll front matter
        if not content.startswith('---\n'):
            relative_path = file_path.relative_to(self.digest_dir)
            self.warnings.append(f"{relative_path}: Missing Jekyll front matter")
            return False
            
        return True
    
    def run(self) -> bool:
        """Run all validation checks."""
        print("Validating GitHub Pages structure...")
        
        # Check structure
        print("\n1. Checking directory structure...")
        self.validate_structure()
        
        # Check all markdown files
        print("\n2. Validating markdown files...")
        md_files = list(self.digest_dir.rglob('*.md'))
        
        total_valid_links = 0
        total_broken_links = 0
        files_with_front_matter = 0
        
        for md_file in md_files:
            # Skip old webplatform directory if it exists
            if 'webplatform' in str(md_file):
                continue
                
            # Check front matter
            if self.validate_front_matter(md_file):
                files_with_front_matter += 1
                
            # Check links
            valid, broken = self.validate_file_links(md_file)
            total_valid_links += valid
            total_broken_links += broken
            
        print(f"  - Files checked: {len(md_files)}")
        print(f"  - Files with front matter: {files_with_front_matter}/{len(md_files)}")
        print(f"  - Valid links: {total_valid_links}")
        print(f"  - Broken links: {total_broken_links}")
        
        # Check version coverage
        print("\n3. Checking version coverage...")
        versions_dir = self.digest_dir / 'versions'
        if versions_dir.exists():
            versions = [d.name for d in versions_dir.iterdir() if d.is_dir()]
            print(f"  - Versions found: {', '.join(sorted(versions))}")
            
        # Check area coverage
        print("\n4. Checking area coverage...")
        areas_dir = self.digest_dir / 'areas'
        if areas_dir.exists():
            areas = [d.name for d in areas_dir.iterdir() if d.is_dir()]
            print(f"  - Areas found: {len(areas)} areas")
            
        # Report results
        print("\n" + "="*50)
        
        if self.errors:
            print(f"\n❌ Validation failed with {len(self.errors)} errors:")
            for error in self.errors[:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more errors")
            return False
        else:
            print("\n✅ Validation passed!")
            
        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} warnings:")
            for warning in self.warnings[:5]:  # Show first 5 warnings
                print(f"  - {warning}")
            if len(self.warnings) > 5:
                print(f"  ... and {len(self.warnings) - 5} more warnings")
                
        return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate GitHub Pages navigation structure')
    parser.add_argument('--digest-dir', default='digest_markdown', help='Path to digest_markdown directory')
    
    args = parser.parse_args()
    
    validator = GitHubPagesValidator(args.digest_dir)
    success = validator.run()
    
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())