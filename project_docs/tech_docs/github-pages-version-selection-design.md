# GitHub Pages Version Selection Design

## Overview
This document outlines the design for implementing version selection functionality on the GitHub Pages deployment of Chrome Release Digests.

## Current State

### Existing Structure
```
digest_markdown/
├── index.md                    # Static home page
├── webplatform/
│   ├── css/
│   │   ├── chrome-139-stable-en.md
│   │   └── chrome-139-stable-zh.md
│   └── [other areas]/
└── enterprise/
```

### Limitations
- Single version display (Chrome 139 only)
- No navigation between versions
- No historical comparison capability
- Static links hardcoded in index.md

## Proposed Solution: Dual Navigation System

### 1. Version-Centric Navigation
Users can browse by Chrome version to see all changes in a specific release.

```
digest_markdown/
├── versions/
│   ├── index.md               # Version selector page
│   ├── chrome-139/
│   │   ├── index.md          # Chrome 139 overview
│   │   ├── css.md            # CSS changes in 139
│   │   ├── webapi.md         # WebAPI changes in 139
│   │   └── [other areas].md
│   ├── chrome-138/
│   │   └── [same structure]
│   └── chrome-137/
│       └── [same structure]
```

### 2. Area-Centric Navigation
Users can browse by feature area to track evolution across versions.

```
digest_markdown/
├── areas/
│   ├── index.md               # Area selector page
│   ├── css/
│   │   ├── index.md          # CSS hub with version list
│   │   ├── chrome-139.md     # CSS in Chrome 139
│   │   ├── chrome-138.md     # CSS in Chrome 138
│   │   └── chrome-137.md     # CSS in Chrome 137
│   └── [other areas]/
│       └── [same structure]
```

## Implementation Strategy

### Phase 1: Data Organization
1. **Inventory Existing Content**
   - Scan `upstream_docs/processed_releasenotes/processed_forwebplatform/areas/`
   - Identify available versions per area
   - Map language variants (en/zh)

2. **Content Aggregation**
   - Group by version (136-139)
   - Group by area (css, webapi, etc.)
   - Track coverage gaps

### Phase 2: Static Page Generation

#### Version Pages
Each version gets:
- Overview page listing all areas
- Individual area pages
- Navigation to prev/next version
- Language toggle (en/zh)

#### Area Pages  
Each area gets:
- Hub page with version timeline
- Individual version pages
- Comparison features (future)
- RSS feed (future)

### Phase 3: Navigation Enhancement

#### Main Index Update
```markdown
# Chrome Release Digests

## Browse by Version
- [Chrome 139 (Latest Stable)](/versions/chrome-139/)
- [Chrome 138](/versions/chrome-138/)
- [View All Versions →](/versions/)

## Browse by Feature Area
- [CSS Updates](/areas/css/)
- [JavaScript Updates](/areas/javascript/)
- [View All Areas →](/areas/)
```

#### Breadcrumb Navigation
Every page includes:
```
Home > Versions > Chrome 139 > CSS
Home > Areas > CSS > Chrome 139
```

## Technical Considerations

### 1. Jekyll Compatibility
- Use Jekyll collections for versions/areas
- Leverage front matter for metadata
- Create custom layouts for navigation

### 2. File Naming Convention
```
# Version-based
versions/chrome-{version}/{area}.md

# Area-based  
areas/{area}/chrome-{version}.md
```

### 3. Automated Generation
- Script to reorganize existing content
- Generate index pages dynamically
- Update on new version release

### 4. SEO & Discovery
- Consistent URL structure
- Sitemap generation
- Meta descriptions per page

## Benefits

1. **User Experience**
   - Multiple navigation paths
   - Easy version comparison
   - Historical tracking

2. **Maintainability**
   - Clear file organization
   - Automated generation
   - Scalable structure

3. **GitHub Pages Native**
   - No JavaScript required
   - Works with Jekyll
   - Fast static pages

## Migration Plan

### Step 1: Prepare Structure
- Create directories
- Set up Jekyll config
- Design templates

### Step 2: Generate Content
- Run migration script
- Generate index pages
- Create navigation

### Step 3: Deploy & Test
- Test locally with Jekyll
- Deploy to GitHub Pages
- Verify all links work

### Step 4: Automation
- Integrate with release pipeline
- Auto-generate new version pages
- Update navigation automatically

## Future Enhancements

1. **Version Comparison**
   - Side-by-side view
   - Diff highlighting
   - Change summary

2. **Search Functionality**
   - Client-side search
   - Filter by keywords
   - Advanced queries

3. **Subscription Features**
   - RSS feeds per area
   - Email notifications
   - Change alerts

4. **Interactive Features**
   - Version timeline
   - Feature adoption charts
   - Browser compatibility matrix

## Example User Flows

### Flow 1: "What's new in Chrome 139?"
1. Home → Versions → Chrome 139
2. See all areas with changes
3. Click specific area for details

### Flow 2: "How has CSS evolved?"
1. Home → Areas → CSS
2. See timeline of CSS changes
3. Click version for specific details

### Flow 3: "Compare Chrome 138 vs 139"
1. Navigate to Chrome 139
2. Click "Compare with previous"
3. See highlighted differences

## Success Metrics

- Page load time < 1s
- 3 clicks max to any content
- Support 20+ versions
- Zero JavaScript dependency
- Mobile-responsive design

## Conclusion

This design provides a scalable, maintainable solution for version selection on GitHub Pages while working within Jekyll's constraints. The dual navigation system serves both users who think in terms of versions and those who track specific feature areas.