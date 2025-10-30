# Chrome Digest Server

A comprehensive MCP (Model Context Protocol) server for accessing and analyzing Chrome release notes, generating AI-powered digests, and extracting feature information for web platform updates.

## 🎯 What You Can Get

This MCP server provides access to:

### 📊 Processed Chrome Release Data
- **Web Platform Updates**: CSS, JavaScript, Web APIs, performance improvements, etc.
- **WebGPU Features**: Graphics and compute capabilities

### 📝 AI-Generated Digests
- **Web Platform Digests**: Targeted at web developers and platform engineers
- **Bilingual Support**: English and Chinese digest generation
- **Focus Area Filtering**: Get updates for specific areas (AI, Security, Performance, etc.)

### 🔍 Feature Analysis
- **Area-based Classification**: Features organized by functional areas
- **Link Extraction**: 100% accurate link discovery from release notes
- **Version Comparison**: Track changes across Chrome versions

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) (install via `pip install uv` or your platform package manager)
- Claude Desktop or another MCP-compatible client

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/chrome-update-digest.git
cd chrome-update-digest

# Install dependencies and create a uv-managed environment
uv sync
```

### MCP Server Setup

### Sampling Requirements

This MCP server calls the connected MCP client's LLM using sampling to build its digests. Use an MCP client that supports sampling workflows—we recommend VS Code or VS Code Insiders because they expose the full sampling controls needed by the server.

When VS Code first loads the `chrome-digest` MCP server, it prompts to allow the tool to use the VS Code model. Click **Allow** so the server can make sampling calls through the client.

In VS Code, open `List Servers -> Configure Model Access (Sampling)` for `chrome-digest` and allow the client to pick an appropriate sampling-capable option. The server now defaults to **legacy-safe sampling**, which lets the client decide which model to use. This avoids payload compatibility issues we hit with stricter schemas late in 2024.

Sampling feature flags:
- `USE_LEGACY_SAMPLING` (default `true`): When `true`, the server sends your raw prompt to the client and does **not** specify a model. Set to `false` only after validating that your MCP client accepts `SamplingMessage` payloads and respects model preferences.
- `WEBPLATFORM_MODEL_PREFERENCES`: JSON or shorthand passed through *only when* `USE_LEGACY_SAMPLING=false` (e.g. `{ "model": "gpt-5-mini" }` or `gpt-5-mini`).
- `WEBPLATFORM_MODEL`: Shorthand model string used when preferences JSON is not provided (`USE_LEGACY_SAMPLING=false` required).
- `WEBPLATFORM_DEFAULT_MODEL`: Fallback when neither of the above is set (`USE_LEGACY_SAMPLING=false` required). Defaults to `gpt-5-mini`.
- `WEBPLATFORM_SAMPLING_TIMEOUT`: Per-attempt timeout in seconds (default 120).

#### Configure Your MCP Client

Connect the server through your preferred MCP client (VS Code, Cursor, Claude Desktop, etc.):

**Configuration Example (macOS/Linux using uv project runner):**
```json
{
  "mcpServers": {
    "chrome-digest": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "/path/to/chrome-update-digest",
        "chrome-update-digest-mcp",
        "--base-path",
        "/path/to/chrome-update-digest"
      ]
    }
  }
}
```

**Configuration Example (Windows PowerShell):**
```json
{
  "mcpServers": {
    "chrome-digest": {
      "command": "uv.exe",
      "args": [
        "run",
        "--project",
        "C:\\path\\to\\chrome-update-digest",
        "chrome-update-digest-mcp",
        "--base-path",
        "C:\\path\\to\\chrome-update-digest"
      ]
    }
  }
}
```

**Important Notes:**
- Replace `/path/to/chrome-update-digest` with your actual project path
- Run `uv sync` at least once so dependencies are available to the runner
- Restart your MCP client after modifying its configuration

#### Test the Server

```bash
# Run the packaged MCP server (uses base path for prompts/config/data)
uv run chrome-update-digest-mcp --base-path .
```

### Command Line Utilities

The bundled CLI wraps the existing processor scripts so you can run them through uv:

```bash
# Clean data pipeline (arguments forwarded to clean_data_pipeline.py)
uv run chrome-update-digest-cli process -- --version 140 --channel stable --with-yaml

# Monitor upstream releases (forwards to monitor_releases.py)
uv run chrome-update-digest-cli monitor
```

## 📚 Available MCP Tools

### Digest Orchestration
- `webplatform_digest`: Run the full pipeline (sampling) and return structured results.
- `digest_prepare_yaml`: Pre-stage structured YAML without writing outputs.
- `digest_generate_area`: Generate a single area within a prepared run (sampling).
- `digest_translate_area`: Translate an area to the run's target language (sampling).
- `digest_write_outputs`: Persist artefacts for a specific run to disk.
- `digest_validate_links`: Verify outbound links for a release digest.
- `digest_available_prompts`: List prompt templates bundled with the server.
- `digest_register_release_resources`: Register processed release notes as FastMCP resources.

### Run Insight & Maintenance
- `get_webplatform_progress`: Quick snapshot of active digest work.
- `digest_summarize_progress`: Historical and in-flight run status.
- `progress_watch`: Streaming-friendly progress watcher for long jobs.
- `digest_list_outputs`: Enumerate outputs associated with a run ID.
- `digest_describe_run_config`: Inspect stored parameters for a run.
- `digest_inspect_cache`: Check cached artefacts, optionally per area.
- `digest_reset_run_state`: Reset metadata and optionally clear cache.
- `telemetry_report_metrics`: Return telemetry gathered during runs.

### Release Monitoring
- `check_latest_releases`: Check upstream channels for the newest versions.
- `crawl_missing_releases`: Crawl and backfill missing release metadata.

### Data Preparation (no sampling)
- `clean_data_pipeline_run`: Produce processed markdown/YAML release notes entirely offline.
- `clean_data_pipeline_check`: Confirm whether processed files already exist.
- `split_features_by_heading`: Split arbitrary content by heading depth for downstream tooling.

### Site Publishing
- `generate_github_pages`: Refresh `digest_markdown/versions` and area navigation, reusing cached digest data where possible.

## 💡 Usage Examples

### Generate a Web Platform Digest with AI Focus
```json
{
  "tool": "webplatform_digest",
  "parameters": {
    "version": 138,
    "focus_areas": ["ai", "webgpu"],
    "language": "bilingual"
  }
}
```

### Check for Latest Releases
```json
{
  "tool": "check_latest_releases",
  "parameters": {
    "release_type": "webplatform",
    "channel": "stable"
  }
}
```

### Materialize Processed Release Notes Without Sampling
```json
{
  "tool": "clean_data_pipeline_run",
  "parameters": {
    "version": "140",
    "channel": "stable",
    "with_yaml": true
  }
}
```

## 📁 Data Organization

```
chrome-update-digest/
├── upstream_docs/                      # Source data
│   ├── release_notes/                  # Raw release notes
│   │   └── WebPlatform/               # Web platform & WebGPU notes
│   └── processed_releasenotes/         # Processed data
│       └── processed_forwebplatform/
│           └── areas/                  # Area-specific processed data
│               ├── css/                # CSS features (MD + YAML)
│               ├── webapi/             # Web API features
│               ├── graphics-webgpu/    # WebGPU features
│               ├── on-device-ai/       # AI features
│               └── security/           # Security updates
├── digest_markdown/                    # Generated digests (MD)
├── digest_html/                       # Generated digests (HTML)
├── config/                            # Configuration files
│   └── focus_areas.yaml              # Area definitions
└── prompts/                          # AI prompt templates
```

## 🔧 CLI & Module Usage

For automation and scripting you can keep everything inside the uv-managed environment:

```bash
# Clean data pipeline (recommended)
uv run chrome-update-digest-cli process -- --version 139 --with-yaml

# Process beta channel
uv run chrome-update-digest-cli process -- --version 139 --channel beta --with-yaml

# Legacy pipeline (still available, but deprecated)
uv run python -m chrome_update_digest.processors.split_and_process_release_notes --version 139

# Monitor releases from the command line
uv run chrome-update-digest-cli monitor

# Preview GitHub Pages output locally (requires Ruby/Jekyll)
bundle exec jekyll serve --source digest_markdown --destination _site
```

## 📖 Documentation

- **Technical Overview**: See [project_docs/tech_docs/technical-overview.md](project_docs/tech_docs/technical-overview.md) for detailed architecture and pipeline information
- **Development Guide**: Check [CLAUDE.md](CLAUDE.md) for development instructions
- **API Reference**: MCP tools are self-documenting through the protocol

## 🛟 Support

### Common Questions

**Q: How often is the data updated?**
A: Use `check_latest_releases` to check for new releases. Chrome typically releases monthly.

**Q: Can I customize the digest format?**
A: Yes, use the `custom_instruction` parameter in digest tools to add specific requirements.

**Q: What Chrome versions are supported?**
A: Generally Chrome 100+ with better support for recent versions (130+).

**Q: Can I get digests in other languages?**
A: Currently supports English, Chinese, and bilingual. More languages can be added via prompt templates.

**Q: What's the difference between stable and beta channels?**
A: Beta releases come earlier (e.g., June) with preview features, while stable releases come later (e.g., August) with finalized features. Beta may have fewer features or different focus areas.

**Q: How are WebGPU features handled?**
A: WebGPU features are extracted from both Chrome Graphics sections and dedicated WebGPU release notes, then deduplicated with WebGPU-specific content taking priority.

### Troubleshooting

If the MCP server doesn't start:
1. Ensure dependencies are synced: `uv sync`
2. Confirm the launch command uses `uv run chrome-update-digest-mcp --base-path <workspace>`
3. Verify the path in your MCP client configuration

If tools aren't working:
1. Check that source data exists in `upstream_docs/`
2. Run `check_latest_releases` to download missing data
3. Review server logs for specific errors

## 🌟 Features

- **100% Link Accuracy**: Deterministic link extraction without AI hallucination
- **Bilingual Support**: Native English and Chinese digest generation
- **Focus Area Filtering**: Get only the updates relevant to your needs
- **Developer Focus**: Focused on web developers and platform engineers
- **Multi-Channel Support**: Process stable, beta, and other release channels
- **WebGPU Deduplication**: Smart merging of WebGPU features from multiple sources
- **Dynamic Hierarchy Detection**: Handles inconsistent heading structures across versions
- **Fault Tolerant**: Smart file discovery and fallback mechanisms
- **Fast Processing**: Efficient YAML pipeline for quick analysis
- **Area-Based Classification**: Automatic feature categorization into functional areas

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Chrome Platform Team for comprehensive release notes
- FastMCP framework for excellent MCP server implementation
- The open-source community for continuous improvements

---

**Get Chrome updates that matter to you, powered by AI 🚀**

For technical details and architecture information, please refer to the [Technical Overview](docs/tech_docs/technical-overview.md).
