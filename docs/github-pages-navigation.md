# GitHub Pages Navigation System

## Overview

The Chrome Release Digests site now features a dual navigation system that allows users to browse content in two ways:
1. **By Version** - See all changes in a specific Chrome release
2. **By Feature Area** - Track how a feature area evolves over time

## Directory Structure

```
digest_markdown/
├── index.md                    # Main landing page with dual navigation
├── _config.yml                 # Jekyll configuration
├── versions/                   # Version-centric navigation
│   ├── index.md               # Version selector page
│   ├── chrome-139/
│   │   ├── index.md          # Chrome 139 overview
│   │   ├── css.md            # CSS changes in 139
│   │   ├── webapi.md         # WebAPI changes in 139
│   │   └── [other areas].md
│   └── chrome-[version]/      # Other versions
└── areas/                      # Area-centric navigation
    ├── index.md               # Area selector page
    ├── css/
    │   ├── index.md          # CSS hub with version list
    │   ├── chrome-139.md     # CSS in Chrome 139
    │   └── chrome-[version].md
    └── [other areas]/         # Other feature areas
```

## Usage

### Generating/Updating Navigation

Run the generation script to create or update the navigation structure:

```bash
# Activate virtual environment
source .venv/bin/activate

# Generate navigation
python3 src/tools/generate_github_pages_navigation.py

# Clean and regenerate (removes existing structure first)
python3 src/tools/generate_github_pages_navigation.py --clean
```

### Validating Structure

Check for broken links and structural issues:

```bash
python3 src/tools/validate_github_pages.py
```

### Local Preview

Test the site locally with Jekyll:

```bash
cd digest_markdown
bundle install  # First time only
bundle exec jekyll serve
# Visit http://localhost:4000
```

## Features

### Version-Centric Navigation
- Browse all changes in a specific Chrome release
- Navigate between versions (previous/next)
- See which feature areas had updates
- Latest version clearly marked

### Area-Centric Navigation
- Track evolution of specific features
- View changes across multiple versions
- Compare implementations over time
- See version history for each area

### Cross-Navigation
- Easy switching between navigation modes
- Breadcrumb navigation on all pages
- Consistent navigation links
- Mobile-responsive design

## Automation

### Integration with Release Pipeline

The navigation generation can be integrated into the release processing pipeline:

```python
# In your release processing script
from src.tools.generate_github_pages_navigation import GitHubPagesNavigationGenerator

# After processing release notes
generator = GitHubPagesNavigationGenerator()
generator.run()
```

### Continuous Updates

When new Chrome versions are processed:
1. Run the clean data pipeline for the new version
2. Execute the navigation generation script
3. Validate the structure
4. Commit and push to GitHub

## Content Sources

The navigation system pulls content from:
```
upstream_docs/processed_releasenotes/processed_forwebplatform/areas/
├── [area]/
│   ├── chrome-[version]-stable.md   # Stable channel content
│   ├── chrome-[version]-stable.yml  # Structured data
│   └── chrome-[version]-beta.md     # Beta channel content (if available)
```

## Supported Versions

Currently includes:
- Chrome 139 (Latest Stable)
- Chrome 138
- Chrome 137
- Chrome 136

## Supported Areas

20 feature areas including:
- CSS
- Web APIs
- Graphics & WebGPU
- Security & Privacy
- JavaScript
- HTML & DOM
- Navigation & Loading
- Network
- Payment
- PWA & Service Worker
- Performance
- Multimedia
- Devices
- Identity
- Browser Changes
- Deprecations
- On-Device AI
- Origin Trials
- WebAssembly
- WebRTC

## Benefits

1. **User Experience**
   - Multiple navigation paths for different use cases
   - Easy version comparison
   - Historical tracking of features
   - Quick access to latest updates

2. **Maintainability**
   - Automated generation from processed release notes
   - Clear file organization
   - Scalable structure for future versions
   - Single source of truth

3. **GitHub Pages Native**
   - No JavaScript required
   - Works with Jekyll out of the box
   - Fast static pages
   - SEO-friendly URLs

## Future Enhancements

Planned improvements include:
- Version comparison views
- RSS feeds per area
- Search functionality
- Feature adoption timeline
- Browser compatibility matrix

## Troubleshooting

### Missing Content
If some versions or areas are missing:
1. Check that source files exist in `upstream_docs/processed_releasenotes/`
2. Run the clean data pipeline for missing versions
3. Regenerate navigation with `--clean` flag

### Broken Links
Run the validator to identify and fix broken links:
```bash
python3 src/tools/validate_github_pages.py
```

### Jekyll Build Errors
Ensure Jekyll dependencies are installed:
```bash
cd digest_markdown
bundle install
bundle exec jekyll build --verbose
```