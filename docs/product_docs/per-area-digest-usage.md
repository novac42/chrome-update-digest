# Per-Area Digest Generation Usage Guide

## Overview

The enhanced WebPlatform digest tool generates separate digests for each focus area by default, with automatic English-to-Chinese translation capabilities.

## Usage

### Default Behavior (Per-Area Generation)

By default, the tool generates separate digests for each area:

```python
from src.mcp_tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool

tool = EnhancedWebplatformDigestTool()
result = await tool.run(
    ctx=ctx,
    version="139",
    channel="stable",
    language="en"  # split_by_area=True by default
)
```

### Single Combined Digest

To generate a single digest covering all areas (old behavior):

```python
result = await tool.run(
    ctx=ctx,
    version="139",
    channel="stable",
    split_by_area=False,  # Explicitly disable per-area splitting
    language="en"
)
```

### Bilingual Generation (Default)

Generate both English and Chinese versions for all areas:

```python
result = await tool.run(
    ctx=ctx,
    version="139",
    channel="stable",
    language="bilingual"  # or None for bilingual by default
    # split_by_area=True by default
)
```

### Command Line Usage

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the test script
python test_per_area_run.py
```

## Output Structure

### Directory Organization

```
digest_markdown/
└── webplatform/
    ├── css/
    │   ├── chrome-139-stable-en.md
    │   └── chrome-139-stable-zh.md
    ├── webapi/
    │   ├── chrome-139-stable-en.md
    │   └── chrome-139-stable-zh.md
    ├── graphics-webgpu/
    │   ├── chrome-139-stable-en.md
    │   └── chrome-139-stable-zh.md
    └── ...
```

### Result JSON Structure

```json
{
  "success": true,
  "mode": "per_area",
  "version": "139",
  "channel": "stable",
  "language": "bilingual",
  "languages": ["en", "zh"],
  "areas": ["css", "webapi", "graphics-webgpu", ...],
  "outputs": {
    "css": {
      "en": "/path/to/css/chrome-139-stable-en.md",
      "zh": "/path/to/css/chrome-139-stable-zh.md"
    },
    ...
  },
  "translation_status": {
    "css": "ok",
    "webapi": "retry_success",
    "graphics-webgpu": "fallback"
  },
  "errors": {}
}
```

## Focus Areas

The following areas are automatically processed:

- **css**: CSS & Styling features
- **webapi**: Web APIs and DOM interfaces
- **graphics-webgpu**: Graphics and WebGPU features
- **javascript**: JavaScript language features
- **multimedia**: Media, audio, and video features
- **performance**: Performance optimizations
- **security-privacy**: Security and privacy features
- **pwa-service-worker**: PWA and Service Worker features
- **devices**: Device APIs and sensors
- **deprecations**: Deprecated features
- **others**: Untagged features

## Area Normalization

The system automatically normalizes area names:

- `webgpu`, `gpu`, `graphics` → `graphics-webgpu`
- `security`, `privacy` → `security-privacy`
- `pwa`, `service-worker` → `pwa-service-worker`
- `api`, `web-api` → `webapi`

## Translation Pipeline

1. **English Generation**: Each area digest is first generated in English (canonical version)
2. **Validation**: English digest is validated to ensure all features are included
3. **Translation**: English digest is translated to Chinese using specialized prompt
4. **Structure Validation**: Translation is validated to ensure:
   - Same heading hierarchy
   - Preserved links
   - No added/removed features
5. **Retry**: Failed validations trigger one retry with corrective context
6. **Fallback**: If retry fails, a fallback message is generated

## Fallback Handling

### Empty Area Fallback
When an area has no features:
```markdown
# Chrome 139 CSS & Styling Digest

> No new features in the CSS & Styling area for this release.
```

### Generation Failure Fallback
When LLM generation fails validation:
```markdown
# Chrome 139 CSS & Styling Digest (Fallback)
> LLM generation failed: [reason]. Below is the raw feature list.

## Features
### Feature Title
Links:
- [Link Title](url)
```

### Translation Failure Fallback
When translation fails:
```markdown
# Chrome 139 CSS & Styling 摘要（中文翻译失败）

> 自动翻译失败。请参考英文版：[path]

## Translation Failed
The automatic translation to Chinese failed...
```

## Quality Controls

### Feature Validation
- Checks that ≥70% of expected features appear in digest
- Validates that links are from the original YAML data
- Allows maximum 2 extra links (for related resources)

### Translation Validation
- Ensures heading count and hierarchy match
- Verifies all links are preserved
- Checks no features added or removed
- Validates terminology consistency

### Content Truncation
- Feature descriptions truncated to 300 characters
- Prevents token limit issues with large areas
- Preserves essential information

## Performance Considerations

- **Sequential Processing**: Areas processed one at a time (no concurrency yet)
- **Caching**: YAML data cached to avoid reprocessing
- **Retry Limits**: Maximum 1 retry per generation/translation
- **Timeout**: 60 seconds per LLM call

## Testing

Run the test suite:
```bash
pytest tests/test_webplatform_per_area_generation.py -v
```

Key test coverage:
- Area normalization
- Feature truncation
- Digest validation
- Translation validation
- Fallback generation
- Empty area handling

## Future Enhancements

1. **Parallel Processing**: Generate multiple areas concurrently
2. **Incremental Updates**: Only regenerate changed areas
3. **Custom Area Groups**: Support user-defined area combinations
4. **Statistics Dashboard**: Aggregate metrics across areas
5. **Quality Metrics**: Track validation success rates