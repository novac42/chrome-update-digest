#!/usr/bin/env python3
"""
Generate GitHub Pages structure with version and area navigation.
Creates a dual navigation system for browsing Chrome release digests.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from datetime import datetime


class GitHubPagesGenerator:
    def __init__(self):
        self.base_path = Path("digest_markdown")
        self.areas_path = self.base_path / "areas"
        self.versions_path = self.base_path / "versions"
        self.upstream_path = Path("upstream_docs/processed_releasenotes/processed_forwebplatform/areas")
        
        # Define focus areas with display names
        self.focus_areas = {
            'css': 'CSS & Styling',
            'javascript': 'JavaScript',
            'graphics-webgpu': 'Graphics & WebGPU',
            'network': 'Network',
            'performance': 'Performance',
            'security-privacy': 'Security & Privacy',
            'webapi': 'Web APIs',
            'multimedia': 'Multimedia',
            'devices': 'Devices',
            'deprecation': 'Deprecations'
        }
        
        # Track available content
        self.area_versions = {}  # area -> list of versions
        self.version_areas = {}  # version -> list of areas
        
    def scan_existing_content(self) -> Tuple[Dict[str, List[int]], Dict[int, List[str]]]:
        """Scan upstream docs to inventory available content."""
        print("Scanning existing content...")
        
        area_versions = {}
        version_areas = {}
        
        if not self.upstream_path.exists():
            print(f"Warning: {self.upstream_path} not found")
            return area_versions, version_areas
            
        # Scan each area directory
        for area_key in self.focus_areas.keys():
            area_path = self.upstream_path / area_key
            if not area_path.exists():
                continue
                
            versions = set()
            
            # Find all Chrome version files
            for file in area_path.glob("chrome-*.md"):
                # Match patterns like chrome-139-stable.md or chrome-139.md
                match = re.search(r'chrome-(\d+)(?:-\w+)?\.md', file.name)
                if match:
                    version = int(match.group(1))
                    versions.add(version)
                    
                    # Add to version_areas mapping
                    if version not in version_areas:
                        version_areas[version] = []
                    if area_key not in version_areas[version]:
                        version_areas[version].append(area_key)
            
            if versions:
                area_versions[area_key] = sorted(versions, reverse=True)
                print(f"  {area_key}: found {len(versions)} versions - {sorted(versions, reverse=True)[:3]}...")
        
        self.area_versions = area_versions
        self.version_areas = version_areas
        
        return area_versions, version_areas
    
    def create_directories(self):
        """Create the directory structure."""
        print("\nCreating directory structure...")
        
        # Create main directories
        self.areas_path.mkdir(parents=True, exist_ok=True)
        self.versions_path.mkdir(parents=True, exist_ok=True)
        
        # Create area subdirectories
        for area_key in self.focus_areas.keys():
            area_dir = self.areas_path / area_key
            area_dir.mkdir(exist_ok=True)
            
        # Create version subdirectories
        for version in self.version_areas.keys():
            version_dir = self.versions_path / f"chrome-{version}"
            version_dir.mkdir(exist_ok=True)
            
        print(f"  Created {len(self.focus_areas)} area directories")
        print(f"  Created {len(self.version_areas)} version directories")
    
    def generate_area_hub_page(self, area_key: str, versions: List[int]):
        """Generate hub page for a specific area."""
        area_name = self.focus_areas[area_key]
        area_dir = self.areas_path / area_key
        
        content = f"""---
layout: default
title: {area_name} - All Versions
---

# {area_name} Updates

Track {area_name.lower()} changes across Chrome versions.

## Available Versions

"""
        
        # Add version links
        for version in versions:
            content += f"### [Chrome {version}](./chrome-{version})\n"
            
            # Check what files exist for this version
            source_path = self.upstream_path / area_key / f"chrome-{version}-stable.md"
            if not source_path.exists():
                source_path = self.upstream_path / area_key / f"chrome-{version}.md"
            
            if source_path.exists():
                # Get preview (first few lines of content)
                preview_lines = source_path.read_text(encoding='utf-8').split('\n')[:5]
                preview = ' '.join(line for line in preview_lines if line and not line.startswith('#'))[:150]
                if preview:
                    content += f"*{preview}...*\n"
            
            content += "\n"
        
        # Add navigation
        content += f"""---

## Navigation
- [← Back to All Areas](../)
- [Home](/)
- [Browse by Version](/versions/)

*Last updated: {datetime.now().strftime('%Y-%m-%d')}*
"""
        
        # Write the hub page
        index_file = area_dir / "index.md"
        index_file.write_text(content)
        
        # Generate individual version pages for this area
        for version in versions:
            self.generate_area_version_page(area_key, version)
    
    def generate_area_version_page(self, area_key: str, version: int):
        """Generate area-specific page for a version."""
        area_name = self.focus_areas[area_key]
        area_dir = self.areas_path / area_key
        
        # Find source file
        source_path = self.upstream_path / area_key / f"chrome-{version}-stable.md"
        if not source_path.exists():
            source_path = self.upstream_path / area_key / f"chrome-{version}.md"
        
        if not source_path.exists():
            return
        
        # Read source content
        source_content = source_path.read_text(encoding='utf-8')
        
        # Generate page with proper front matter
        content = f"""---
layout: default
title: Chrome {version} - {area_name}
---

# Chrome {version} - {area_name}

[← Back to {area_name}](./) | [View Full Chrome {version} Release](/versions/chrome-{version}/)

{source_content}

---

## Navigation
- [← Previous Version](./chrome-{version-1}) | [Next Version →](./chrome-{version+1})
- [All {area_name} Updates](./)
- [All Chrome {version} Updates](/versions/chrome-{version}/)
"""
        
        # Write the page
        page_file = area_dir / f"chrome-{version}.md"
        page_file.write_text(content)
    
    def generate_version_overview_page(self, version: int, areas: List[str]):
        """Generate overview page for a specific version."""
        version_dir = self.versions_path / f"chrome-{version}"
        
        content = f"""---
layout: default
title: Chrome {version} Release Notes
---

# Chrome {version} Release Notes

## What's New in Chrome {version}

This release includes updates across the following areas:

"""
        
        # Add area links with counts
        for area_key in areas:
            area_name = self.focus_areas.get(area_key, area_key.title())
            content += f"### [{area_name}](./{area_key})\n"
            
            # Get feature count if possible
            source_path = self.upstream_path / area_key / f"chrome-{version}-stable.md"
            if not source_path.exists():
                source_path = self.upstream_path / area_key / f"chrome-{version}.md"
            
            if source_path.exists():
                source_text = source_path.read_text(encoding='utf-8')
                feature_count = len(re.findall(r'^###\s+', source_text, re.MULTILINE))
                if feature_count > 0:
                    content += f"*{feature_count} features/changes*\n"
            
            content += "\n"
        
        # Add navigation
        content += f"""---

## Navigation
- [← Chrome {version-1}](../chrome-{version-1}/) | [Chrome {version+1} →](../chrome-{version+1}/)
- [All Versions](../)
- [Browse by Feature Area](/areas/)
- [Home](/)

*Chrome {version} was released in {self.estimate_release_date(version)}*
"""
        
        # Write overview page
        index_file = version_dir / "index.md"
        index_file.write_text(content)
        
        # Generate area-specific pages for this version
        for area_key in areas:
            self.generate_version_area_page(version, area_key)
    
    def generate_version_area_page(self, version: int, area_key: str):
        """Generate version-specific page for an area."""
        area_name = self.focus_areas.get(area_key, area_key.title())
        version_dir = self.versions_path / f"chrome-{version}"
        
        # Find source file
        source_path = self.upstream_path / area_key / f"chrome-{version}-stable.md"
        if not source_path.exists():
            source_path = self.upstream_path / area_key / f"chrome-{version}.md"
        
        if not source_path.exists():
            return
        
        # Read source content
        source_content = source_path.read_text(encoding='utf-8')
        
        # Generate page
        content = f"""---
layout: default
title: Chrome {version} - {area_name}
---

# Chrome {version} - {area_name}

[← Back to Chrome {version}](./) | [View All {area_name} Updates](/areas/{area_key}/)

{source_content}

---

## Navigation
- [Chrome {version} Overview](./)
- [All {area_name} Updates](/areas/{area_key}/)
- [Browse Other Areas](./)
"""
        
        # Write the page
        page_file = version_dir / f"{area_key}.md"
        page_file.write_text(content)
    
    def generate_areas_index(self):
        """Generate main areas index page."""
        content = """---
layout: default
title: Browse by Feature Area
---

# Browse Chrome Updates by Feature Area

Select a feature area to track changes across all Chrome versions.

## Feature Areas

"""
        
        # Add area cards
        for area_key, area_name in self.focus_areas.items():
            if area_key in self.area_versions:
                versions = self.area_versions[area_key]
                version_count = len(versions)
                latest = versions[0] if versions else "N/A"
                
                content += f"### [{area_name}](./{area_key}/)\n"
                content += f"Track {area_name.lower()} evolution across Chrome releases.\n\n"
                content += f"- **Versions available:** {version_count}\n"
                content += f"- **Latest:** Chrome {latest}\n"
                content += f"- **Range:** Chrome {min(versions)} - {max(versions)}\n\n"
        
        # Add navigation
        content += """---

## Navigation
- [Browse by Version](/versions/)
- [Home](/)

*Explore how Chrome features evolve over time by selecting an area above.*
"""
        
        # Write index
        index_file = self.areas_path / "index.md"
        index_file.write_text(content)
        print(f"Created areas index: {index_file}")
    
    def generate_versions_index(self):
        """Generate main versions index page."""
        content = """---
layout: default
title: Browse by Chrome Version
---

# Browse by Chrome Version

Select a Chrome version to see all updates in that release.

## Available Versions

"""
        
        # Sort versions in reverse order
        sorted_versions = sorted(self.version_areas.keys(), reverse=True)
        
        # Mark latest stable
        if sorted_versions:
            latest = sorted_versions[0]
            content += f"### [Chrome {latest} (Latest)](./{f'chrome-{latest}'}/) ⭐\n"
            area_count = len(self.version_areas.get(latest, []))
            content += f"*{area_count} areas updated*\n\n"
            
            # Add other versions
            for version in sorted_versions[1:]:
                content += f"### [Chrome {version}](./{f'chrome-{version}'}/)\n"
                area_count = len(self.version_areas.get(version, []))
                content += f"*{area_count} areas updated*\n\n"
        
        # Add navigation
        content += """---

## Navigation
- [Browse by Feature Area](/areas/)
- [Home](/)

*Select a version to explore what's new in that Chrome release.*
"""
        
        # Write index
        index_file = self.versions_path / "index.md"
        index_file.write_text(content)
        print(f"Created versions index: {index_file}")
    
    def update_main_index(self):
        """Update the main index.md with dual navigation."""
        latest_version = max(self.version_areas.keys()) if self.version_areas else 139
        
        content = f"""---
layout: home
title: Chrome Release Digests
---

# Chrome Release Digests

Welcome to the Chrome Release Notes Digest collection. Choose how you'd like to explore Chrome updates:

## 🔍 Browse by Version
View all changes in a specific Chrome release:

- [**Chrome {latest_version}** (Latest Stable)](/versions/chrome-{latest_version}/) ⭐
- [Chrome {latest_version-1}](/versions/chrome-{latest_version-1}/)
- [Chrome {latest_version-2}](/versions/chrome-{latest_version-2}/)
- [View All Versions →](/versions/)

## 📚 Browse by Feature Area
Track how specific features evolve across Chrome versions:

### Core Web Platform
- [**CSS & Styling**](/areas/css/) - Layout, animations, and visual updates
- [**JavaScript**](/areas/javascript/) - JS engine improvements and features
- [**Web APIs**](/areas/webapi/) - New and updated browser APIs

### Performance & Graphics
- [**Performance**](/areas/performance/) - Speed and optimization updates
- [**Graphics & WebGPU**](/areas/graphics-webgpu/) - GPU and rendering features

### Security & Network
- [**Security & Privacy**](/areas/security-privacy/) - Security enhancements
- [**Network**](/areas/network/) - Protocol and connectivity updates

### Media & Devices
- [**Multimedia**](/areas/multimedia/) - Audio, video, and media features
- [**Devices**](/areas/devices/) - Hardware and device integration

### Maintenance
- [**Deprecations**](/areas/deprecation/) - Removed and deprecated features

[View All Areas →](/areas/)

## 📊 Quick Stats

- **Latest Stable:** Chrome {latest_version}
- **Total Versions Tracked:** {len(self.version_areas)}
- **Feature Areas:** {len(self.focus_areas)}

---

## About

This site provides structured, digestible summaries of Chrome release notes, organized for easy navigation and discovery. Whether you're tracking a specific feature's evolution or exploring what's new in the latest release, we've got you covered.

---

*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC*
"""
        
        # Write updated index
        index_file = self.base_path / "index.md"
        index_file.write_text(content)
        print(f"Updated main index: {index_file}")
    
    def estimate_release_date(self, version: int) -> str:
        """Estimate release date based on Chrome's ~4 week release cycle."""
        # Chrome 139 was released around November 2024
        base_version = 139
        base_year = 2024
        base_month = 11
        
        version_diff = version - base_version
        # Roughly 13 releases per year (every 4 weeks)
        month_diff = version_diff * 4 / 4.33  # weeks to months
        
        total_months = base_month + month_diff
        year = base_year + int(total_months // 12)
        month = int(total_months % 12)
        if month <= 0:
            month = 12 + month
            year -= 1
        
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        
        return f"{months[month-1]} {year}"
    
    def generate_all(self):
        """Generate the complete GitHub Pages structure."""
        print("=" * 60)
        print("GitHub Pages Structure Generator")
        print("=" * 60)
        
        # Step 1: Scan existing content
        self.scan_existing_content()
        
        if not self.area_versions:
            print("\n⚠️ No content found in upstream_docs. Please run digest generation first.")
            return
        
        print(f"\nFound content for {len(self.version_areas)} versions across {len(self.area_versions)} areas")
        
        # Step 2: Create directory structure
        self.create_directories()
        
        # Step 3: Generate area pages
        print("\nGenerating area hub pages...")
        for area_key, versions in self.area_versions.items():
            self.generate_area_hub_page(area_key, versions)
            print(f"  ✓ {area_key}: {len(versions)} versions")
        
        # Step 4: Generate version pages
        print("\nGenerating version overview pages...")
        for version, areas in self.version_areas.items():
            self.generate_version_overview_page(version, areas)
            print(f"  ✓ Chrome {version}: {len(areas)} areas")
        
        # Step 5: Generate index pages
        print("\nGenerating index pages...")
        self.generate_areas_index()
        self.generate_versions_index()
        self.update_main_index()
        
        print("\n" + "=" * 60)
        print("✅ GitHub Pages structure generation complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Review generated pages in digest_markdown/")
        print("2. Test locally: cd digest_markdown && bundle exec jekyll serve")
        print("3. Commit and push to trigger GitHub Pages deployment")
        print("4. Access at: https://[username].github.io/chrome-update-digest/")


def main():
    generator = GitHubPagesGenerator()
    generator.generate_all()


if __name__ == "__main__":
    main()