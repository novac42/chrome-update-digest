# Common Issues and Troubleshooting

This guide covers common issues when processing Chrome release notes and their solutions.

## Input File Issues

### Issue: Release notes file not found

**Error:**
```
Chrome {version} ({channel}) release notes not found.
Expected location: upstream_docs/release_notes/WebPlatform/
```

**Solutions:**

1. **Check if the version is released yet**
   ```bash
   # Check latest available releases
   uv run chrome-update-digest-cli check-upstream
   ```

2. **Download the release notes manually**
   - Visit: https://developer.chrome.com/release-notes/{version}
   - Save markdown file to: `upstream_docs/release_notes/WebPlatform/chrome-{version}.md`

3. **Try a different channel**
   - Stable channel may not be available yet, try beta:
   ```bash
   uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
     --version {version} --channel beta --verbose
   ```

4. **Use the crawl script to fetch missing releases**
   ```bash
   uv run chrome-update-digest-cli crawl --version {version}
   ```

### Issue: Invalid version format

**Error:**
```
Invalid version format: 'latest'
Version must be a number (e.g., 139, 140)
```

**Solution:**
- Use numeric version numbers only (e.g., 139, 140, 141)
- To find the latest version, use: `uv run chrome-update-digest-cli check-upstream`

## Processing Issues

### Issue: No features extracted for an area

**Behavior:**
- Processing completes but an area has 0 features
- YAML file exists but features list is empty

**Common causes:**

1. **Heading pattern mismatch**
   - Chrome changed the heading format in release notes
   - Solution: Check the actual heading in the release notes and update `config/focus_areas.yaml`

2. **Version doesn't include that area**
   - Not all areas appear in every Chrome version
   - Solution: This is normal; some areas are only present in certain versions

3. **Beta vs Stable differences**
   - Beta releases may have fewer features
   - Solution: Try processing stable channel or wait for stable release

### Issue: WebGPU features missing

**Behavior:**
- WebGPU area has fewer features than expected
- Known WebGPU features not appearing

**Common causes:**

1. **Missing dedicated WebGPU release notes**
   - WebGPU has two sources: Chrome Graphics + dedicated WebGPU file
   - Check for: `upstream_docs/release_notes/WebPlatform/webgpu-{version}.md`
   - Solution: Download from https://developer.chrome.com/docs/web-platform/webgpu-release-notes

2. **Deduplication removing features**
   - WebGPU-specific content takes priority over Chrome Graphics
   - Solution: This is expected behavior; check both source files

### Issue: On-device AI features not found

**Behavior:**
- on-device-ai area empty despite AI features in release notes

**Common causes:**

1. **AI features scattered across sections**
   - AI features may be in Origin Trials, Web APIs, etc.
   - Solution: The pipeline searches content keywords automatically; ensure keywords match in `config/focus_areas.yaml`

2. **New AI terminology**
   - Chrome may use new terms not in keyword list
   - Solution: Update keywords in `config/focus_areas.yaml`:
   ```yaml
   on-device-ai:
     keywords:
       - "on-device ai"
       - "language model"
       - "gemini nano"  # Add new terms
   ```

## Output Issues

### Issue: Output directory not found

**Error:**
```
FileNotFoundError: .../processed_forwebplatform/areas/ does not exist
```

**Solution:**
- The script creates directories automatically
- If you see this error, check filesystem permissions:
  ```bash
  mkdir -p upstream_docs/processed_releasenotes/processed_forwebplatform/areas
  chmod 755 upstream_docs/processed_releasenotes/processed_forwebplatform/areas
  ```

### Issue: YAML file malformed

**Behavior:**
- YAML file exists but can't be parsed
- Error when reading YAML: "invalid YAML syntax"

**Solution:**
1. **Validate YAML syntax**
   ```bash
   python -c "import yaml; yaml.safe_load(open('path/to/file.yml'))"
   ```

2. **Regenerate the file**
   - Delete the malformed YAML file
   - Rerun processing for that version/channel

## Performance Issues

### Issue: Processing is very slow

**Behavior:**
- Full workflow takes >10 minutes
- Individual areas take >30 seconds each

**Common causes:**

1. **Network issues**
   - If using external resources or APIs
   - Solution: Check network connectivity, use local cache

2. **Large release notes**
   - Some versions have 100+ features
   - Solution: Process specific areas instead of all 23:
   ```bash
   --areas css webapi graphics-webgpu  # Only 3 areas
   ```

3. **Debug mode enabled**
   - Verbose logging adds overhead
   - Solution: Remove `--verbose` flag for production runs

### Issue: Out of memory errors

**Behavior:**
- Process crashes with "MemoryError" or system freeze

**Solution:**
1. **Process areas in smaller batches**
   ```bash
   # Process 5 areas at a time
   --areas css webapi html-dom javascript graphics-webgpu
   # Then process next 5
   --areas on-device-ai security-privacy origin-trials deprecations multimedia
   ```

2. **Increase system resources**
   - Close other applications
   - Increase swap space (Linux/macOS)

## Validation Issues

### Issue: Links in output are broken

**Behavior:**
- Generated markdown contains broken links
- Links return 404 errors

**Common causes:**

1. **Chrome documentation URLs changed**
   - Chrome.com restructured documentation
   - Solution: Validate links after generation:
   ```bash
   uv run chrome-update-digest-cli validate-links --version {version}
   ```

2. **Relative vs absolute links**
   - Links may be relative in source but need to be absolute
   - Solution: Check link extraction logic in pipeline

## Environment Issues

### Issue: Import errors

**Error:**
```
ModuleNotFoundError: No module named 'chrome_update_digest'
```

**Solution:**
1. **Ensure dependencies are installed**
   ```bash
   uv sync
   ```

2. **Use uv run to execute scripts**
   ```bash
   # Correct
   uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py

   # Incorrect (missing uv run)
   python .claude/skills/chrome-update-digest/scripts/process_chrome.py
   ```

3. **Check PYTHONPATH** (if not using uv run)
   ```bash
   export PYTHONPATH=/path/to/chrome-update-digest:$PYTHONPATH
   python .claude/skills/chrome-update-digest/scripts/process_chrome.py
   ```

### Issue: Wrong Python version

**Error:**
```
SyntaxError: invalid syntax (type hints, match statements, etc.)
```

**Solution:**
- Requires Python 3.10+
- Check version:
  ```bash
  uv run python --version
  ```
- If version is too old, update Python or use uv's managed Python

### Issue: CHROME_UPDATE_DIGEST_BASE_PATH not set

**Behavior:**
- Script can't find config files or release notes
- FileNotFoundError for config/focus_areas.yaml

**Solution:**
- The script auto-detects base path, but you can override:
  ```bash
  export CHROME_UPDATE_DIGEST_BASE_PATH=/path/to/chrome-update-digest
  ```
- Or use --base-path flag:
  ```bash
  --base-path /path/to/chrome-update-digest
  ```

## Channel-Specific Issues

### Issue: Beta channel has different structure

**Behavior:**
- Beta processing fails or produces unexpected results
- Features missing or misclassified

**Common causes:**

1. **Beta uses different headings**
   - Beta may have preliminary headings
   - Solution: Check actual beta release notes structure

2. **Beta has fewer features**
   - This is expected; beta is an earlier snapshot
   - Solution: No action needed; wait for stable release for complete features

3. **Beta filename different**
   - Looking for `chrome-139-beta.md` but file is `chrome-139.md`
   - Solution: Script handles this automatically with fallback logic

## Debugging Tips

### Enable verbose output
```bash
--verbose
```
Shows detailed progress, helpful for identifying where processing fails.

### Check intermediate outputs
```bash
# Inspect YAML files generated by clean pipeline
ls -la upstream_docs/processed_releasenotes/processed_forwebplatform/areas/css/

# View YAML content
cat upstream_docs/processed_releasenotes/processed_forwebplatform/areas/css/chrome-139-stable.yml
```

### Test with a single area
```bash
# Faster testing with just one area
--areas css --verbose
```

### Compare stable vs beta
```bash
# Process both channels
--version 139 --channel stable --verbose
--version 139 --channel beta --verbose

# Compare outputs
diff upstream_docs/processed_releasenotes/processed_forwebplatform/areas/css/chrome-139-stable.md \
     upstream_docs/processed_releasenotes/processed_forwebplatform/areas/css/chrome-139-beta.md
```

## Getting Help

If you encounter an issue not covered here:

1. **Check the logs** with `--verbose` flag
2. **Inspect intermediate files** (YAML, markdown)
3. **Verify input files** exist and are well-formed
4. **Check focus_areas.yaml** configuration matches release notes structure
5. **Review recent commits** in case of regressions

## Common Workflows

### Full processing (production)
```bash
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
  --version 139 \
  --channel stable \
  --language bilingual \
  --verbose
```

### Quick test (single area)
```bash
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
  --version 139 \
  --areas css \
  --language en \
  --verbose
```

### Beta preview
```bash
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
  --version 139 \
  --channel beta \
  --language en \
  --verbose
```

### Core areas only
```bash
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
  --version 139 \
  --areas css webapi html-dom javascript graphics-webgpu \
  --verbose
```
