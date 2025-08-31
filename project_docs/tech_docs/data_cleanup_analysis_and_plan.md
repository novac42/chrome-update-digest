# Data Cleanup Analysis and Improvement Plan

## Current Implementation Review

### Problems Identified

1. **Header Level Dependency**
   - Current implementation relies on exact header patterns (`##` for h2, `###` for h3)
   - Needs to handle potential structure changes in release notes
   - Section names might change over time

2. **WebGPU Processing Complexity**
   - WebGPU notes contain invalid historical sections that need removal:
     - Everything after `## What's New in WebGPU` (version history)
     - All `### Chrome {version}` sections (duplicated changelog)
   - Need to filter metadata like author info, navigation links
   - Must preserve only actual feature content (h2, h3, h4, h5 sections)

3. **Structure Validation Needed**
   - No validation that release note structure hasn't changed
   - Should verify known areas exist ('CSS', 'Web APIs', etc.)
   - Alert if structure deviates from expected format

## Proposed Solution: Clean Data Pipeline

### Core Principles (Data Engineering Best Practices)

1. **Structure-Based Extraction**
   - `##` (h2) = Area (e.g., CSS, Web APIs, Graphics)
   - `###` (h3) = Feature name
   - `####`/`#####` (h4/h5) = Feature details (belong to parent h3)
   - Hierarchical relationship preserved

2. **Validation First**
   - Check for expected h2 sections before processing
   - Known areas: 'CSS', 'Web API', 'Origin trials', 'Deprecations'
   - Alert if structure changes (missing expected sections)

3. **WebGPU Data Cleaning**
   ```
   Step 1: Remove invalid sections
   - Remove everything from "## What's New in WebGPU" to end
   - This removes all ### Chrome {version} history
   
   Step 2: Filter metadata
   - Remove headers with: 'Release Notes', 'Key Updates', 'What's New'
   - Remove author info, navigation links, published dates
   
   Step 3: Extract valid content
   - Keep all h2/h3/h4/h5 that remain
   - These are the actual WebGPU features
   ```

4. **Graphics-WebGPU Area Creation**
   - Merge cleaned WebGPU content with Graphics section from Chrome notes
   - Output as single 'graphics-webgpu' area file

## Implementation Architecture

```python
class CleanDataPipeline:
    def __init__(self):
        self.expected_areas = [
            'CSS', 'Web APIs', 'Graphics', 'WebGPU', 
            'JavaScript', 'Security', 'Performance',
            'Origin trials', 'Deprecations'
        ]
    
    def validate_structure(self, content):
        """Validate h2 sections match expected areas"""
        h2_sections = extract_h2_titles(content)
        missing = set(self.expected_areas) - set(h2_sections)
        if missing:
            warn(f"Structure changed! Missing: {missing}")
        return len(missing) == 0
    
    def clean_webgpu(self, content):
        """Remove invalid WebGPU sections"""
        # Step 1: Remove version history
        content = remove_from_pattern(content, r'^## What\'s New in WebGPU', end_of_file)
        
        # Step 2: Remove metadata
        content = remove_lines_with(['Published:', 'François Beaufort', 'GitHub'])
        
        # Step 3: Filter invalid headers
        content = remove_headers_containing(['Release Notes', 'Key Updates'])
        
        return content
    
    def extract_by_area(self, content):
        """Extract content by h2 areas"""
        areas = {}
        for h2_section in parse_h2_sections(content):
            area_name = normalize_area_name(h2_section.title)
            areas[area_name] = {
                'features': extract_h3_features(h2_section),
                'raw_content': h2_section.content
            }
        return areas
```

## Data Flow

```
1. Input Files:
   - chrome-139.md (main release notes)
   - webgpu-139.md (WebGPU specific)

2. Validation:
   - Check chrome-139.md has expected h2 sections
   - Alert if structure changed

3. Chrome Processing:
   - Split by h2 → areas
   - Each h3 → feature within area
   - h4/h5 → feature details

4. WebGPU Cleaning:
   - Remove "What's New in WebGPU" to EOF
   - Remove metadata and navigation
   - Keep only feature content

5. Merge Graphics-WebGPU:
   - Chrome Graphics section + Cleaned WebGPU content
   - Output as single area file

6. Output Structure:
   areas/
   ├── css/chrome-139.md
   ├── web-apis/chrome-139.md
   ├── graphics-webgpu/chrome-139.md  # Merged
   └── [other-areas]/chrome-139.md
```

## Key Insights from Data Analysis

### Chrome Release Notes Structure
- Consistent h2 sections: CSS, Web APIs, Graphics, JavaScript, etc.
- Each h2 = Area, h3 = Feature, h4/h5 = Feature details
- Structure has been stable across versions 124-139

### WebGPU Notes Issues
1. **Invalid Content at End** (Lines 110-336 in webgpu-139.md):
   - `## What's New in WebGPU` starts version history
   - All `### Chrome {version}` sections are duplicates
   - Must remove everything from this point onward

2. **Metadata to Filter**:
   - Author info (François Beaufort, GitHub links)
   - Navigation links
   - "Stay organized with collections"
   - Published dates

3. **Valid Content Pattern**:
   - h2 sections = Major features (e.g., "3D texture support")
   - h3 sections = Sub-features or code examples
   - h4/h5 = Additional details

## Benefits of Clean Pipeline

1. **Simplicity**: Direct h2→Area, h3→Feature mapping
2. **Validation**: Early detection of structure changes
3. **Data Quality**: Clean WebGPU data without duplicates
4. **Maintainability**: Clear rules, no complex AI classification
5. **Performance**: Fast, deterministic processing

## Next Steps

1. Implement validation function for structure checking
2. Create WebGPU cleaning function with regex patterns
3. Build simple h2-based area extractor
4. Test with versions 124-139
5. Compare output with current pipeline