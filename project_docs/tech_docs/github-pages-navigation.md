# GitHub Pages Navigation System

## Overview

The Chrome Release Digests site now features a dual navigation system that allows users to browse content in two ways:
1. **By Version** - See all changes in a specific Chrome release
2. **By Feature Area** - Track how a feature area evolves over time

All navigation is emitted in both English and Chinese. Both languages now share the same directory tree; English pages own the index files (`index.md`), while bilingual runs add Chinese leaf companions with a `-zh` suffix alongside the English `-en` files.

## Directory Structure

```
digest_markdown/
├── _config.yml                  # Jekyll configuration
├── _layouts/                    # Shared page layouts
├── assets/                      # Shared assets (CSS, JS, images)
├── index.md                     # English landing page
├── versions/                    # Version-centric navigation
│   ├── index.md                # Version selector (en)
│   └── chrome-136/
│       ├── index.md            # Chrome 136 overview (en)
│       ├── css-en.md           # CSS changes in Chrome 136 (en)
│       └── css-zh.md           # CSS changes in Chrome 136 (zh leaf)
├── areas/                       # Area-centric navigation
│   ├── index.md                # Feature-area hub (en)
│   └── css/
│       ├── index.md            # CSS hub (en)
│       ├── chrome-136-en.md    # CSS in Chrome 136 (en)
│       └── chrome-136-zh.md    # CSS in Chrome 136 (zh leaf)
└── webplatform/                 # Staging digests copied from the pipeline
    ├── css/
    │   ├── chrome-136-stable-en.md
    │   └── chrome-136-stable-zh.md
    └── [other areas]/
```

## Usage

### Generating/Updating Navigation

Run the generation script to create or update the navigation structure:

```bash
# Activate virtual environment
source .venv/bin/activate

# Generate navigation
python3 src/tools/generate_github_pages_navigation.py

# Bilingual run (emits -en/-zh leaf pages inside shared directories)
python3 src/tools/generate_github_pages_navigation.py --language bilingual

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

The navigation generator copies pre-processed digests staged in:
```
digest_markdown/webplatform/
├── [area]/
│   ├── chrome-[version]-stable-en.md   # English digest
│   └── chrome-[version]-stable-zh.md   # Chinese digest (when available)
```

That staging directory is produced by the clean data pipeline (see `src/chrome_update_digest/processors/clean_data_pipeline.py`) using the focus-area metadata in `config/focus_areas.yaml`. The pipeline itself reads the upstream inputs in `upstream_docs/processed_releasenotes/processed_forwebplatform/` and normalises them before the navigation generator runs.

*Implementation note:* the validator in `src/tools/validate_github_pages.py` deliberately skips the `webplatform/` staging tree because those files serve as source material rather than published pages.

## Language Structure

Running the generator with `--language bilingual` now produces a single navigation tree. Version and area directories contain companion files such as `css-en.md` and `css-zh.md`, with English index pages (`index.md`) remaining the sole hubs. Chinese visitors land directly on the `*-zh.md` leaf pages, which sit alongside the English leaves inside every version and area folder.

## Supported Versions

The generator derives the available versions by scanning `digest_markdown/webplatform/*/chrome-*-stable-*.md`. Any version present in the staging tree appears automatically in the published navigation. In the current repository snapshot, only Chrome 136 digests are present, so the rendered site exposes Chrome 136 for both languages.

## Supported Areas

Areas are driven by the entries in `config/focus_areas.yaml`. When that configuration changes, the next pipeline run updates the staging digests and the navigation generator picks up the new set automatically. Recent additions such as `isolated-web-apps`, `enterprise`, and `devtools` therefore appear without code changes.

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
1. Confirm the staged files exist in `digest_markdown/webplatform/[area]/chrome-[version]-stable-*.md`
2. If they are absent, run the clean data pipeline to rebuild `digest_markdown/webplatform`
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
