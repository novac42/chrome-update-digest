# Chrome Update Digest - Common Issues & Troubleshooting

This guide covers common issues you might encounter when using the Chrome Update Digest skill.

## Installation Issues

### "uv command not found"
**Problem**: The `uv` package manager is not installed.

**Solutions**:
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart your shell or source the profile
source ~/.bashrc  # or ~/.zshrc
```

### "chrome-update-digest-cli: command not found"
**Problem**: The CLI tool is not installed in the project.

**Solutions**:
```bash
# Navigate to project root
cd /path/to/chrome-update-digest

# Sync dependencies
uv sync

# Verify installation
uv run chrome-update-digest-cli --help
```

### "ModuleNotFoundError: No module named 'chrome_update_digest'"
**Problem**: Python package not installed or wrong environment.

**Solutions**:
```bash
# Ensure you're in project root
cd /path/to/chrome-update-digest

# Install in development mode
uv pip install -e .

# Or use uv sync
uv sync
```

## Input File Issues

### "Release notes not found"
**Problem**: Raw release notes file doesn't exist for the specified version.

**Diagnosis**:
```bash
# Check if file exists
ls upstream_docs/release_notes/WebPlatform/chrome-{version}.md
```

**Solutions**:
1. **Download release notes manually**:
   - Visit https://developer.chrome.com/release-notes/{version}
   - Save as `upstream_docs/release_notes/WebPlatform/chrome-{version}.md`

2. **Check version number**:
   - Verify the version is released
   - Latest stable is usually 2-3 versions ahead of current

3. **Try beta channel**:
   ```
   Process Chrome {version} beta
   ```

4. **Check file naming**:
   - File might be named `chrome-{version}-stable.md`
   - Skill handles both naming patterns

### "WebGPU file not found" (Warning, not error)
**Problem**: Optional WebGPU-specific release notes missing.

**Note**: This is usually fine - WebGPU content may be in main release notes.

**Solution** (optional):
```bash
# Download WebGPU release notes if available
# Save as upstream_docs/release_notes/WebPlatform/webgpu-{version}.md
```

## Processing Issues

### "Clean pipeline failed"
**Problem**: The data extraction pipeline encountered an error.

**Diagnosis**:
```bash
# Run with verbose output
python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
  --version {version} --verbose
```

**Common causes**:
1. **Malformed markdown**: Release notes have unexpected structure
   - Solution: Check the raw markdown file for syntax issues

2. **Missing dependencies**: Required packages not installed
   - Solution: Run `uv sync` to install all dependencies

3. **Permission errors**: Can't write to output directories
   - Solution: Check directory permissions
   ```bash
   chmod -R u+w upstream_docs/processed_releasenotes/
   ```

### "Navigation generation failed"
**Problem**: GitHub Pages navigation could not be generated.

**Diagnosis**:
```bash
# Check if processed files exist
ls -R upstream_docs/processed_releasenotes/processed_forwebplatform/areas/
```

**Solutions**:
1. **Processed files missing**: Run clean pipeline first
2. **Output directory doesn't exist**: Create it
   ```bash
   mkdir -p digest_markdown/{areas,versions}
   ```
3. **Permission errors**: Fix permissions
   ```bash
   chmod -R u+w digest_markdown/
   ```

## Path Resolution Issues

### "Project root not found"
**Problem**: Skill can't locate the chrome-update-digest project root.

**Diagnosis**:
- Check if you're in the project directory
- Check if `upstream_docs/` and `digest_markdown/` exist

**Solutions**:
1. **Run from project root**:
   ```bash
   cd /path/to/chrome-update-digest
   # Then invoke skill
   ```

2. **Set environment variable**:
   ```bash
   export CHROME_UPDATE_DIGEST_BASE_PATH=/path/to/chrome-update-digest
   ```

3. **Check marker directories exist**:
   ```bash
   ls -ld upstream_docs/ digest_markdown/
   ```

## Output Issues

### "No files generated"
**Problem**: Processing completes but no output files found.

**Diagnosis**:
```bash
# Check expected output locations
ls upstream_docs/processed_releasenotes/processed_forwebplatform/areas/*/chrome-{version}-*.md
ls digest_markdown/areas/*/chrome-{version}.md
```

**Solutions**:
1. Check for errors in the processing output
2. Verify input files were processed correctly
3. Check disk space: `df -h`

### "Old files not updated"
**Problem**: Changes not reflected in output files.

**Solution**: The pipeline regenerates files, so they should update. If not:
```bash
# Remove old files and regenerate
rm -rf upstream_docs/processed_releasenotes/processed_forwebplatform/areas/*/chrome-{version}-*
rm -rf digest_markdown/areas/*/chrome-{version}.md
rm -rf digest_markdown/versions/chrome-{version}/

# Rerun processing
python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
  --version {version} --verbose
```

## GitHub Pages Issues

### "GitHub Pages not updating"
**Problem**: Site not reflecting new content after commit.

**Diagnosis**:
```bash
# Check if changes were committed
git status

# Check GitHub Actions
# Visit https://github.com/{user}/{repo}/actions
```

**Solutions**:
1. **Commit and push changes**:
   ```bash
   git add digest_markdown/
   git commit -m "Update Chrome {version} digest"
   git push origin main
   ```

2. **Check GitHub Actions workflow**:
   - Visit repo → Actions tab
   - Look for failed builds
   - Check workflow logs

3. **Verify workflow file**:
   ```bash
   cat .github/workflows/pages.yml
   ```

4. **Check Pages settings**:
   - Repo → Settings → Pages
   - Ensure Source is "GitHub Actions"

### "Jekyll build failed"
**Problem**: Jekyll can't build the site.

**Common causes**:
1. **Invalid front matter**: Check markdown files have proper YAML front matter
2. **Invalid markdown**: Syntax errors in generated files
3. **Missing _config.yml**: Navigation generator should create this

**Solution**:
```bash
# Regenerate navigation (creates _config.yml)
python src/chrome_update_digest/tools/generate_github_pages_navigation.py
```

## Permission Issues

### "Permission denied" when running script
**Problem**: Script is not executable.

**Solution**:
```bash
chmod +x .claude/skills/chrome-update-digest/scripts/process_chrome.py
```

### "Permission denied" writing files
**Problem**: Can't write to output directories.

**Solution**:
```bash
# Fix permissions
chmod -R u+w upstream_docs/processed_releasenotes/
chmod -R u+w digest_markdown/
```

## Performance Issues

### "Processing takes too long"
**Problem**: Pipeline runs very slowly.

**Factors**:
- Number of features in release (Chrome releases vary in size)
- System resources
- Network latency (if downloading resources)

**Solutions**:
1. **Use faster storage**: SSD recommended
2. **Close other applications**: Free up RAM
3. **Check system load**: `top` or `htop`

Note: Normal processing time is 30-60 seconds for extraction + navigation.

## Debugging Tips

### Enable verbose output
```bash
python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
  --version {version} --verbose
```

### Check Python environment
```bash
# Which Python is being used?
uv run python --version

# Which packages are installed?
uv pip list | grep chrome-update-digest
```

### Inspect intermediate files
```bash
# Check YAML files were generated
cat upstream_docs/processed_releasenotes/processed_forwebplatform/areas/css/chrome-{version}-stable.yml

# Check markdown files have content
wc -l upstream_docs/processed_releasenotes/processed_forwebplatform/areas/*/chrome-{version}-*.md
```

### Test components separately

**Test clean pipeline**:
```bash
uv run chrome-update-digest-cli process -- --version {version} --with-yaml
```

**Test navigation generator**:
```bash
uv run python src/chrome_update_digest/tools/generate_github_pages_navigation.py
```

## Getting Help

If none of these solutions work:

1. **Check project documentation**: `CLAUDE.md` and `README.md` in project root
2. **Review logs**: Look for error messages in output
3. **Check GitHub issues**: https://github.com/{user}/{repo}/issues
4. **Verify environment**: Ensure all prerequisites are met

## Reporting Issues

When reporting issues, include:
- Chrome version being processed
- Full error message
- Output of `uv run chrome-update-digest-cli --version`
- Operating system and Python version
- Steps to reproduce

---

*Last updated: January 2025*
