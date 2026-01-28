# Error Handling Reference

Comprehensive error scenarios and troubleshooting guide.

## Error Reference Table

| Error | Cause | Solution |
|-------|-------|----------|
| "Chrome release notes not found" | Version not released yet or not downloaded | Use `--check-latest` to verify version exists |
| "No areas found" | Clean pipeline hasn't run yet | Run without `--list-areas` first to extract areas |
| "WebGPU download failed" | Network issue or version doesn't have WebGPU notes | OK to continue - WebGPU is optional |
| "Agent timeout" | LLM rate limit or large content | Retry failed areas individually |
| "Invalid version format" | Version not a number | Use format: `143`, `144` (digits only) |
| "YAML file not found" | Area extraction failed | Check clean pipeline output for errors |
| "Permission denied" | File system permissions issue | Check write permissions on output directories |
| "Module not found" | Missing dependencies | Run `uv sync` to install dependencies |

## Common Scenarios

### Missing WebGPU Release Notes

**Scenario**: WebGPU download fails or file doesn't exist

**Impact**: Minimal - WebGPU is optional

**Action**:
- Processing continues normally
- `graphics-webgpu` area will only contain Chrome Graphics content
- Normal for older versions (< Chrome 113)

### Partial Agent Failures

**Scenario**: Some digest generation agents timeout or fail

**Impact**: Incomplete digests for some areas

**Action**:
1. Note which areas failed
2. Continue processing remaining areas
3. Retry failed areas individually after completion
4. Or rerun entire process after investigating cause

### Rate Limits

**Scenario**: LLM API rate limits hit during parallel processing

**Impact**: Multiple agent failures simultaneously

**Action**:
- Process areas in smaller batches (e.g., 5 at a time)
- Add delays between batches
- Use `--list-areas` to target specific areas for retry

### Network Issues During Download

**Scenario**: Release notes download fails due to network

**Impact**: Cannot proceed without Chrome release notes

**Action**:
1. Check network connectivity
2. Verify Chrome version is released: `--check-latest`
3. Manual download option: Place files in `upstream_docs/release_notes/WebPlatform/`
4. Retry after network is restored

### Empty or Corrupted YAML

**Scenario**: Clean pipeline produces empty or invalid YAML

**Impact**: Agent cannot generate digest for that area

**Action**:
1. Check source release notes are valid
2. Review clean pipeline output for warnings
3. Report issue if reproducible

### Disk Space Issues

**Scenario**: Not enough disk space for outputs

**Impact**: Write failures during digest generation

**Action**:
1. Check available disk space
2. Clean up old processed versions if needed
3. Ensure ~100MB free space for typical processing

## Debugging Tips

### Enable Verbose Mode

```bash
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
  --version 143 \
  --verbose
```

### Check Intermediate Outputs

1. **Release notes downloaded**:
   ```bash
   ls upstream_docs/release_notes/WebPlatform/chrome-143*.md
   ls upstream_docs/release_notes/WebPlatform/webgpu-143.md
   ```

2. **Areas extracted**:
   ```bash
   ls upstream_docs/processed_releasenotes/processed_forwebplatform/areas/*/chrome-143-stable.yml
   ```

3. **Digests generated**:
   ```bash
   ls digest_markdown/webplatform/*/chrome-143-stable-*.md
   ```

### Read Agent Logs

When agents fail, check the agent output for specific error messages:
- YAML parsing errors
- Prompt template issues
- Content length limits
- API errors

## Recovery Strategies

### Full Reprocess

```bash
# Clean and reprocess from scratch
rm -rf upstream_docs/processed_releasenotes/processed_forwebplatform/areas/*/chrome-143-stable.*
rm -rf digest_markdown/webplatform/*/chrome-143-stable-*.md

# Rerun
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py --version 143
```

### Selective Retry

```bash
# Regenerate specific area digests
# Agent 1: css English
# Agent 2: css Chinese
# etc.
```

### Manual Intervention

For persistent issues:
1. Examine the YAML file content
2. Check prompt template syntax
3. Test with a single area first
4. Report bug if reproducible

## Prevention Best Practices

1. **Always use `--check-latest`** before processing new versions
2. **Monitor disk space** before large batch processing
3. **Test with beta first** before processing stable versions
4. **Process during off-peak hours** to avoid rate limits
5. **Keep dependencies updated**: `uv sync` regularly

## Getting Help

If errors persist:
1. Check [common_issues.md](common_issues.md)
2. Review [implementation_guide.md](implementation_guide.md)
3. Examine script output and logs
4. Report reproducible bugs with full error messages
