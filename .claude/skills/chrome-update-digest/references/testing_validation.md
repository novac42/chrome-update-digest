# Testing & Validation

Post-processing validation checklist and testing procedures.

## Quick Validation Checklist

After running the skill, verify:

- [ ] Extraction successful (~23 YAML files)
- [ ] Digests generated (~46 markdown files)
- [ ] Navigation updated (version appears in indexes)
- [ ] Content non-empty (no empty files)
- [ ] Structure valid (headings present)

## Detailed Validation Steps

### 1. Check Extraction Success

**Verify YAML files created**:
```bash
# Should show ~23 YAML files
ls upstream_docs/processed_releasenotes/processed_forwebplatform/areas/*/chrome-143-stable.yml | wc -l
```

**Expected output**: `23` (or close, depending on release content)

**Check specific areas**:
```bash
# List all extracted areas
ls -1 upstream_docs/processed_releasenotes/processed_forwebplatform/areas/
```

**Expected areas** (partial list):
- css
- webapi
- graphics-webgpu
- javascript
- security-privacy
- performance
- on-device-ai
- origin-trials
- deprecations

### 2. Verify Digests Generated

**Count digest files**:
```bash
# Should show ~46 files (23 en + 23 zh)
ls digest_markdown/webplatform/*/chrome-143-stable-*.md | wc -l
```

**Expected output**: `46` (23 areas × 2 languages)

**Check bilingual output**:
```bash
# English digests
ls digest_markdown/webplatform/*/chrome-143-stable-en.md | wc -l

# Chinese digests
ls digest_markdown/webplatform/*/chrome-143-stable-zh.md | wc -l
```

Both should show `23`.

### 3. Confirm Navigation Updated

**Check version-centric navigation**:
```bash
# Should find the new version
grep -r "Chrome 143" digest_markdown/versions/
```

**Expected**: Multiple matches in version index files

**Check area-centric navigation**:
```bash
# Should find version in area indexes
grep -r "Chrome 143" digest_markdown/areas/
```

**Expected**: Each area index should mention Chrome 143

### 4. Quick Content Check

**Find empty files** (should be none):
```bash
find digest_markdown/webplatform/ -name "chrome-143-stable-*.md" -type f -empty
```

**Expected output**: _(no output means no empty files)_

**Check file sizes** (should be reasonable):
```bash
# List files with sizes
ls -lh digest_markdown/webplatform/css/chrome-143-stable-*.md
```

**Expected**: Files should be several KB to several hundred KB

### 5. Validate Structure

#### English Digests

Required sections:
- **Area Summary** (3-5 sentences overview)
- **Detailed Updates** (feature-by-feature breakdown)

**Verify headings**:
```bash
# Check for required headings
grep "## Area Summary" digest_markdown/webplatform/css/chrome-143-stable-en.md
grep "## Detailed Updates" digest_markdown/webplatform/css/chrome-143-stable-en.md
grep "### " digest_markdown/webplatform/css/chrome-143-stable-en.md | head -5
```

**Expected**: All headings present, features use H3 (`###`)

#### Chinese Digests

Same structure as English:
- Area Summary (区域概述)
- Detailed Updates (详细更新)
- Proper Chinese translation

**Verify Chinese content**:
```bash
# Should contain Chinese characters
file digest_markdown/webplatform/css/chrome-143-stable-zh.md
```

**Expected**: "UTF-8 Unicode text"

### 6. Link Format Validation

**Check for bare URLs** (should be none):
```bash
# Find bare http/https URLs (not in markdown links)
grep -E 'http[s]?://[^\)]+ ' digest_markdown/webplatform/css/chrome-143-stable-en.md
```

**Expected**: _(no output or only URLs inside markdown links)_

**Verify markdown link format**:
```bash
# Should find markdown-formatted links
grep -E '\[.+\]\(http' digest_markdown/webplatform/css/chrome-143-stable-en.md | head -3
```

**Expected**: Multiple matches like `[ChromeStatus](https://chromestatus.com/...)`

## Sample Content Validation

### English Digest Sample

Pick a random area and verify content quality:

```bash
head -50 digest_markdown/webplatform/css/chrome-143-stable-en.md
```

**Check for**:
- Title mentions area and version
- Area Summary is coherent
- Features have clear descriptions
- Links are properly formatted
- No template variables (`[AREA]`, `[version]`, etc.)

### Chinese Digest Sample

```bash
head -50 digest_markdown/webplatform/css/chrome-143-stable-zh.md
```

**Check for**:
- Chinese translation present
- Technical terms handled correctly
- Links preserved from English version
- No mixed language (except technical terms)

## Automated Validation Script

For convenience, run all checks:

```bash
# Create quick validation script
cat > /tmp/validate_chrome_143.sh << 'EOF'
#!/bin/bash
VERSION=143
CHANNEL=stable

echo "=== Validation Report for Chrome $VERSION ($CHANNEL) ==="

echo -e "\n1. YAML Extraction:"
yaml_count=$(ls upstream_docs/processed_releasenotes/processed_forwebplatform/areas/*/chrome-${VERSION}-${CHANNEL}.yml 2>/dev/null | wc -l)
echo "   Found: $yaml_count YAML files (expected ~23)"

echo -e "\n2. Digest Generation:"
md_count=$(ls digest_markdown/webplatform/*/chrome-${VERSION}-${CHANNEL}-*.md 2>/dev/null | wc -l)
echo "   Found: $md_count markdown files (expected ~46)"

echo -e "\n3. Empty Files:"
empty=$(find digest_markdown/webplatform/ -name "chrome-${VERSION}-${CHANNEL}-*.md" -type f -empty 2>/dev/null)
if [ -z "$empty" ]; then
  echo "   ✓ No empty files"
else
  echo "   ✗ Found empty files:"
  echo "$empty"
fi

echo -e "\n4. Navigation Update:"
nav_version=$(grep -r "Chrome $VERSION" digest_markdown/versions/ 2>/dev/null | wc -l)
echo "   Found in navigation: $nav_version references"

echo -e "\n=== Validation Complete ==="
EOF

chmod +x /tmp/validate_chrome_143.sh
/tmp/validate_chrome_143.sh
```

## Regression Testing

When making skill changes, test with a known-good version:

1. **Backup existing outputs** for a processed version
2. **Rerun processing** with changes
3. **Compare outputs** with diff tools
4. **Verify no regressions** in content quality

## Performance Benchmarks

Typical processing times (reference only):

- **Extraction**: 1-2 minutes
- **Single area digest**: 30-60 seconds
- **All areas (parallel)**: 2-5 minutes
- **Total (end-to-end)**: 5-10 minutes

Significant deviations may indicate issues.

## Quality Assurance Checklist

Before considering processing complete:

- [ ] All areas extracted from release notes
- [ ] All digests generated (English + Chinese)
- [ ] Navigation updated with new version
- [ ] No empty or corrupted files
- [ ] Links properly formatted
- [ ] Chinese translations present
- [ ] No template variables left in output
- [ ] File sizes reasonable (not truncated)
- [ ] Headings structure correct
- [ ] Content semantically accurate

## Reporting Issues

When validation fails:

1. Note which specific check failed
2. Collect error messages and logs
3. Check [error_handling.md](error_handling.md) for solutions
4. Document steps to reproduce
5. Report with full context if bug is suspected
