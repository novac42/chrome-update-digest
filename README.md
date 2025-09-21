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
- Python 3.8 or higher
- pip package manager
- Claude Desktop or MCP-compatible client

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/chrome-update-digest.git
cd chrome-update-digest

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### MCP Server Setup

#### For Claude Desktop

Add to your config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Configuration Example (macOS/Linux):**
```json
{
  "mcpServers": {
    "chrome-digest": {
      "command": "/path/to/chrome-update-digest/.venv/bin/python",
      "args": ["/path/to/chrome-update-digest/fast_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/chrome-update-digest"
      }
    }
  }
}
```

**Configuration Example (Windows):**
```json
{
  "mcpServers": {
    "chrome-digest": {
      "command": "C:\\path\\to\\chrome-update-digest\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\chrome-update-digest\\fast_mcp_server.py"],
      "env": {
        "PYTHONPATH": "C:\\path\\to\\chrome-update-digest"
      }
    }
  }
}
```

**Important Notes:**
- Replace `/path/to/chrome-update-digest` with your actual project path
- Ensure the virtual environment is properly created before configuration
- Restart Claude Desktop after modifying the configuration

#### Test the Server

```bash
# Activate virtual environment
source .venv/bin/activate

# Start the MCP server
python fast_mcp_server.py
```

## 📚 Available MCP Tools

### Release Monitoring
- **`check_latest_releases`**: Check for new Chrome releases
- **`crawl_missing_releases`**: Download missing release notes

### Digest Generation
- **`webplatform_digest`**: Generate web platform digest
  - Parameters: `version`, `channel`, `focus_areas`, `language`, `target_area`
  - Focus areas: ai, webgpu, devices, css, security, performance

### Site Publishing
- **`generate_github_pages`**: Refresh `digest_markdown/versions` and area navigation
  - Reuses existing digests when present; re-generates only if content is missing or `force_regenerate` is `true`
  - Parameters: `version`, `channel`, `language`, `force_regenerate`, `skip_clean`, `skip_digest`, `skip_validation`

### Data Processing
- **`split_features_by_heading`**: Split content by heading levels

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

## 🔧 Direct Python Usage

For batch processing or automation, you can also use the Python scripts directly:

```bash
# Process release notes using the clean data pipeline (Recommended)
python3 src/processors/clean_data_pipeline.py --version 139 --with-yaml

# Process beta channel
python3 src/processors/clean_data_pipeline.py --version 139 --channel beta --with-yaml

# Legacy pipeline (deprecated but functional)
python3 src/processors/split_and_process_release_notes.py --version 139

# Monitor releases
python src/processors/monitor_releases.py

# Generate HTML from markdown
python src/convert_md2html.py
```

## 📖 Documentation

- **Technical Overview**: See [docs/tech_docs/technical-overview.md](docs/tech_docs/technical-overview.md) for detailed architecture and pipeline information
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
1. Ensure virtual environment is activated
2. Check all dependencies are installed: `pip install -r requirements.txt`
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
