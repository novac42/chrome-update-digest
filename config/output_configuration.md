# Chrome Digest Server Configuration
# 定义文件命名模式和容错规则

## File Naming Patterns

### Digest Markdown Files
# Enterprise digests:
# - Primary: digest-chrome-{version}-enterprise-{channel}.md
# - Fallback: digest-chrome-{version}-enterprise.md (for stable)
# - Legacy: chrome-{version}-enterprise.md, {version}-enterprise.md

# WebPlatform digests:
# - Primary: digest-chrome-{version}-webplatform-{channel}.md
# - Fallback: digest-chrome-{version}-webplatform.md (for stable)
# - Legacy: chrome-{version}-webplatform.md, {version}-webplatform.md

### HTML Output Files
# - Format: chrome-{version}-merged-digest-{channel}.html
# - Stable channel: chrome-{version}-merged-digest-stable.html

## Channel Handling
# - Default channel: stable
# - For stable channel: both with and without suffix are generated
# - For other channels (beta, dev, canary): suffix is mandatory
# - Channel fallback: non-stable -> stable when files not found

## Fault Tolerance Features
# 1. Multiple file naming pattern support
# 2. Fuzzy file matching when exact patterns fail
# 3. Automatic channel fallback
# 4. Dual file generation (with/without suffix) for stable
# 5. Comprehensive error messages with available files listing
# 6. Pattern priority ordering for optimal file discovery

## Directory Structure
```
digest_markdown/
├── enterprise/
│   ├── digest-chrome-{version}-enterprise-{channel}.md
│   └── digest-chrome-{version}-enterprise.md
└── webplatform/
    ├── digest-chrome-{version}-webplatform-{channel}.md
    └── digest-chrome-{version}-webplatform.md

digest_html/
├── chrome-{version}-merged-digest-{channel}.html
└── archive/
    └── (older versions)
```

## Usage Examples

### Generate digests with high fault tolerance:
```python
# Enterprise digest
enterprise_tool = EnterpriseDigestTool(base_path)
result = await enterprise_tool.generate_digest_with_sampling(ctx, {
    "version": 138,
    "channel": "stable",  # Will generate both suffixed and non-suffixed files
    "focus_area": "all"
})

# WebPlatform digest  
webplatform_tool = WebplatformDigestTool(base_path)
result = await webplatform_tool.generate_digest_with_sampling(ctx, {
    "version": 138,
    "channel": "stable",  # Will generate both suffixed and non-suffixed files
    "focus_areas": ["ai", "webgpu", "devices"]
})

# Merged HTML (automatically finds appropriate files)
merged_tool = MergedDigestHtmlTool(base_path)
result = await merged_tool.generate_html({
    "version": 138,
    "channel": "beta",  # Will fallback to stable files if beta not found
    "force_regenerate": True
})
```

## Error Handling
- File not found: Lists available files and suggested patterns
- Empty files: Clear error message with file path
- Permission issues: Detailed error with troubleshooting info
- Network timeouts: Retry mechanism with exponential backoff
- Model failures: Fallback to different models and error recovery
