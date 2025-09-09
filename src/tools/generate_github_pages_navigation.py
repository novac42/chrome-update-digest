#!/usr/bin/env python3
"""
Generate GitHub Pages dual navigation system for Chrome Release Digests.
Creates both version-centric and area-centric navigation structures.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import yaml

class GitHubPagesNavigationGenerator:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.source_dir = self.base_path / "upstream_docs/processed_releasenotes/processed_forwebplatform/areas"
        self.digest_dir = self.base_path / "digest_markdown"
        self.versions_dir = self.digest_dir / "versions"
        self.areas_dir = self.digest_dir / "areas"
        
        # Area display names mapping
        self.area_display_names = {
            'css': 'CSS',
            'webapi': 'Web APIs',
            'graphics-webgpu': 'Graphics & WebGPU',
            'security-privacy': 'Security & Privacy',
            'javascript': 'JavaScript',
            'html-dom': 'HTML & DOM',
            'navigation-loading': 'Navigation & Loading',
            'network': 'Network',
            'payment': 'Payment',
            'pwa-service-worker': 'PWA & Service Worker',
            'performance': 'Performance',
            'multimedia': 'Multimedia',
            'devices': 'Devices',
            'identity': 'Identity',
            'browser-changes': 'Browser Changes',
            'deprecations': 'Deprecations',
            'on-device-ai': 'On-Device AI',
            'origin-trials': 'Origin Trials',
            'webassembly': 'WebAssembly',
            'webrtc': 'WebRTC'
        }
        
    def scan_content(self) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
        """Scan source directory to find all versions and areas."""
        version_areas = defaultdict(set)  # version -> set of areas
        area_versions = defaultdict(set)  # area -> set of versions
        
        if not self.source_dir.exists():
            print(f"Source directory {self.source_dir} does not exist")
            return version_areas, area_versions
            
        for area_dir in self.source_dir.iterdir():
            if not area_dir.is_dir():
                continue
                
            area_name = area_dir.name
            
            for md_file in area_dir.glob("chrome-*.md"):
                # Parse version from filename (chrome-139-stable.md)
                match = re.match(r'chrome-(\d+)-(\w+)\.md', md_file.name)
                if match:
                    version = match.group(1)
                    channel = match.group(2)
                    
                    # For now, focus on stable channel
                    if channel == 'stable':
                        version_areas[version].add(area_name)
                        area_versions[area_name].add(version)
                        
        return dict(version_areas), dict(area_versions)
    
    def ensure_directories(self):
        """Create necessary directory structure."""
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        self.areas_dir.mkdir(parents=True, exist_ok=True)
        
    def copy_content_file(self, source_file: Path, dest_file: Path):
        """Copy content file with front matter added."""
        if not source_file.exists():
            return False
            
        # Read original content
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract title from content
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else dest_file.stem
        
        # Add Jekyll front matter
        front_matter = f"""---
layout: default
title: {title}
---

"""
        
        # Write to destination
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(front_matter + content)
            
        return True
    
    def generate_version_pages(self, version_areas: Dict[str, Set[str]]):
        """Generate version-centric navigation pages."""
        versions = sorted(version_areas.keys(), reverse=True)
        
        # Generate main versions index
        index_content = """---
layout: default
title: Chrome Versions
---

# Chrome Release Digests by Version

Browse Chrome release notes organized by version number.

## Available Versions

"""
        
        for version in versions:
            is_latest = version == versions[0]
            latest_badge = " **(Latest Stable)**" if is_latest else ""
            areas_count = len(version_areas[version])
            index_content += f"- [Chrome {version}{latest_badge}](./chrome-{version}/) - {areas_count} areas with updates\n"
            
        with open(self.versions_dir / "index.md", 'w', encoding='utf-8') as f:
            f.write(index_content)
            
        # Generate individual version pages
        for version in versions:
            version_dir = self.versions_dir / f"chrome-{version}"
            version_dir.mkdir(exist_ok=True)
            
            # Version overview page
            is_latest = version == versions[0]
            overview_content = f"""---
layout: default
title: Chrome {version} Release Notes
---

# Chrome {version} Release Notes

[← Back to all versions](../)

## Areas with Updates

"""
            
            for area in sorted(version_areas[version]):
                display_name = self.area_display_names.get(area, area.replace('-', ' ').title())
                overview_content += f"- [{display_name}](./{area}.html)\n"
                
                # Copy area content to version directory
                source_file = self.source_dir / area / f"chrome-{version}-stable.md"
                dest_file = version_dir / f"{area}.md"
                self.copy_content_file(source_file, dest_file)
                
            # Add navigation links
            overview_content += "\n## Navigation\n\n"
            
            # Previous/Next version navigation
            version_idx = versions.index(version)
            if version_idx > 0:
                newer_version = versions[version_idx - 1]
                overview_content += f"- [← Chrome {newer_version} (Newer)](../chrome-{newer_version}/)\n"
            if version_idx < len(versions) - 1:
                older_version = versions[version_idx + 1]
                overview_content += f"- [Chrome {older_version} (Older) →](../chrome-{older_version}/)\n"
                
            overview_content += "- [View all versions](../)\n"
            overview_content += "- [Browse by feature area](../../areas/)\n"
            
            with open(version_dir / "index.md", 'w', encoding='utf-8') as f:
                f.write(overview_content)
                
    def generate_area_pages(self, area_versions: Dict[str, Set[str]]):
        """Generate area-centric navigation pages."""
        areas = sorted(area_versions.keys())
        
        # Generate main areas index
        index_content = """---
layout: default
title: Feature Areas
---

# Chrome Release Digests by Feature Area

Browse Chrome release notes organized by feature area to track evolution over time.

## Available Feature Areas

"""
        
        for area in areas:
            display_name = self.area_display_names.get(area, area.replace('-', ' ').title())
            versions_count = len(area_versions[area])
            index_content += f"- [{display_name}](./{area}/) - Updates in {versions_count} versions\n"
            
        with open(self.areas_dir / "index.md", 'w', encoding='utf-8') as f:
            f.write(index_content)
            
        # Generate individual area pages
        for area in areas:
            area_dir = self.areas_dir / area
            area_dir.mkdir(exist_ok=True)
            
            display_name = self.area_display_names.get(area, area.replace('-', ' ').title())
            versions = sorted(area_versions[area], reverse=True)
            
            # Area hub page
            hub_content = f"""---
layout: default
title: {display_name} Updates
---

# {display_name} Updates

[← Back to all areas](../)

## Version History

Track the evolution of {display_name} features across Chrome releases.

### Available Versions

"""
            
            for version in versions:
                is_latest = version == versions[0]
                latest_badge = " **(Latest)**" if is_latest else ""
                hub_content += f"- [Chrome {version}{latest_badge}](./chrome-{version}.html)\n"
                
                # Copy version content to area directory
                source_file = self.source_dir / area / f"chrome-{version}-stable.md"
                dest_file = area_dir / f"chrome-{version}.md"
                self.copy_content_file(source_file, dest_file)
                
            # Add navigation
            hub_content += "\n## Navigation\n\n"
            hub_content += "- [View all feature areas](../)\n"
            hub_content += "- [Browse by Chrome version](../../versions/)\n"
            
            with open(area_dir / "index.md", 'w', encoding='utf-8') as f:
                f.write(hub_content)
                
    def update_main_index(self, version_areas: Dict[str, Set[str]], area_versions: Dict[str, Set[str]]):
        """Update the main index.md with dual navigation."""
        versions = sorted(version_areas.keys(), reverse=True)
        areas = sorted(area_versions.keys())
        
        # Get top areas by update frequency
        top_areas = sorted(areas, key=lambda a: len(area_versions[a]), reverse=True)[:5]
        
        index_content = """---
layout: default
title: Chrome Release Digests
---

# Chrome Release Digests

Comprehensive release notes for Chrome web platform features, organized for easy navigation.

## Browse by Version

Explore what's new in each Chrome release:

"""
        
        # Show latest 3 versions
        for version in versions[:3]:
            is_latest = version == versions[0]
            latest_badge = " **(Latest Stable)**" if is_latest else ""
            areas_count = len(version_areas[version])
            index_content += f"- [Chrome {version}{latest_badge}](./versions/chrome-{version}/) - {areas_count} areas with updates\n"
            
        index_content += f"- [View all {len(versions)} versions →](./versions/)\n"
        
        index_content += """

## Browse by Feature Area

Track the evolution of specific features across Chrome versions:

"""
        
        # Show top 5 areas
        for area in top_areas:
            display_name = self.area_display_names.get(area, area.replace('-', ' ').title())
            versions_count = len(area_versions[area])
            index_content += f"- [{display_name}](./areas/{area}/) - Updates in {versions_count} versions\n"
            
        index_content += f"- [View all {len(areas)} feature areas →](./areas/)\n"
        
        index_content += """

## Quick Links

- **Latest Release**: [Chrome """ + versions[0] + """](./versions/chrome-""" + versions[0] + """/)
- **Most Active Areas**: CSS, Web APIs, Graphics & WebGPU
- **Version Comparison**: Compare changes between releases
- **Search**: Use browser search (Ctrl+F) on any page

## About

This site provides structured, searchable release notes for Chrome's web platform features. Content is automatically generated from official Chrome release notes and organized for developer convenience.

### Navigation Tips

- **By Version**: See all changes in a specific Chrome release
- **By Area**: Track how a feature area evolves over time
- **Breadcrumbs**: Use navigation links on each page to explore related content

### Update Frequency

New Chrome stable releases are typically published every 4 weeks. This site is updated shortly after each stable release.

---

*Generated from [Chrome Release Notes](https://developer.chrome.com/release-notes/)*
"""
        
        with open(self.digest_dir / "index.md", 'w', encoding='utf-8') as f:
            f.write(index_content)
            
    def generate_jekyll_config(self):
        """Update Jekyll configuration for GitHub Pages."""
        config = {
            'title': 'Chrome Release Digests',
            'description': 'Comprehensive Chrome web platform release notes with version selection',
            'theme': 'minima',
            'plugins': ['jekyll-feed', 'jekyll-sitemap'],
            'defaults': [
                {
                    'scope': {
                        'path': '',
                        'type': 'pages'
                    },
                    'values': {
                        'layout': 'default'
                    }
                }
            ]
        }
        
        config_path = self.digest_dir / "_config.yml"
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False)
            
    def clean_old_structure(self):
        """Clean up old webplatform directory if it exists."""
        old_dir = self.digest_dir / "webplatform"
        if old_dir.exists():
            print(f"Removing old webplatform directory: {old_dir}")
            shutil.rmtree(old_dir)
            
    def run(self):
        """Execute the complete migration."""
        print("Starting GitHub Pages navigation generation...")
        
        # Scan content
        print("Scanning source content...")
        version_areas, area_versions = self.scan_content()
        
        if not version_areas:
            print("No content found to process")
            return
            
        print(f"Found {len(version_areas)} versions and {len(area_versions)} areas")
        
        # Ensure directories
        print("Creating directory structure...")
        self.ensure_directories()
        
        # Generate pages
        print("Generating version-centric pages...")
        self.generate_version_pages(version_areas)
        
        print("Generating area-centric pages...")
        self.generate_area_pages(area_versions)
        
        print("Updating main index...")
        self.update_main_index(version_areas, area_versions)
        
        print("Updating Jekyll configuration...")
        self.generate_jekyll_config()
        
        print("Cleaning old structure...")
        self.clean_old_structure()
        
        print("\nGeneration complete!")
        print(f"- Versions: {', '.join(sorted(version_areas.keys(), reverse=True))}")
        print(f"- Areas: {len(area_versions)} total")
        print(f"- Output: {self.digest_dir}")
        
        return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate GitHub Pages navigation for Chrome Release Digests')
    parser.add_argument('--base-path', default='.', help='Base path of the project')
    parser.add_argument('--clean', action='store_true', help='Clean existing structure before generating')
    
    args = parser.parse_args()
    
    generator = GitHubPagesNavigationGenerator(args.base_path)
    
    if args.clean:
        print("Cleaning existing structure...")
        if generator.versions_dir.exists():
            shutil.rmtree(generator.versions_dir)
        if generator.areas_dir.exists():
            shutil.rmtree(generator.areas_dir)
            
    success = generator.run()
    
    if success:
        print("\n✅ Successfully generated GitHub Pages navigation structure")
        print("\nTo preview locally:")
        print("  cd digest_markdown")
        print("  jekyll serve")
        print("\nThen visit http://localhost:4000")
    else:
        print("\n❌ Generation failed")
        return 1
        
    return 0


if __name__ == '__main__':
    exit(main())