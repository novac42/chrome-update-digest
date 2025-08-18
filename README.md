# Chrome Digest Server

A comprehensive MCP (Model Context Protocol) server for accessing and analyzing Chrome release notes, generating AI-powered digests, and extracting feature information across enterprise and web platform updates.

## 🎯 What You Can Get

This MCP server provides access to:

### 📊 Processed Chrome Release Data
- **Enterprise Release Notes**: Security policies, admin features, management capabilities
- **Web Platform Updates**: CSS, JavaScript, Web APIs, performance improvements  
- **WebGPU Features**: Graphics and compute capabilities
- **Profile Features**: User profile and sync-related updates

### 📝 AI-Generated Digests
- **Enterprise Digests**: Focused on IT administrators and enterprise deployments
- **Web Platform Digests**: Targeted at web developers and platform engineers
- **Bilingual Support**: English and Chinese digest generation
- **Focus Area Filtering**: Get updates for specific areas (AI, Security, Performance, etc.)

### 🔍 Feature Analysis
- **Profile Feature Extraction**: Identify profile-related features across releases
- **Area-based Classification**: Features organized by functional areas
- **Link Extraction**: 100% accurate link discovery from release notes
- **Version Comparison**: Track changes across Chrome versions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
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

```json
{
  "mcpServers": {
    "chrome-digest": {
      "command": "/path/to/chrome-update-digest/.venv/bin/python",
      "args": ["/path/to/chrome-update-digest/fast_mcp_server.py"]
    }
  }
}
```

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
- **`enterprise_digest`**: Generate enterprise-focused digest
  - Parameters: `version`, `channel`, `focus_area`, `custom_instruction`
  - Focus areas: productivity, security, management, all

- **`webplatform_digest`**: Generate web platform digest
  - Parameters: `version`, `channel`, `focus_areas`, `language`, `target_area`
  - Focus areas: ai, webgpu, devices, css, security, performance

- **`merged_digest_html`**: Create combined HTML output
  - Parameters: `version`, `channel`, `force_regenerate`

### Data Processing
- **`process_enterprise_notes`**: Process raw enterprise release notes
- **`extract_profile_features`**: Extract profile-related features
- **`merge_webgpu_notes`**: Merge WebGPU with Chrome release notes
- **`process_webgpu_yaml`**: Generate structured YAML from merged content
- **`split_features_by_heading`**: Split content by heading levels

## 💡 Usage Examples

### Generate an Enterprise Digest
```json
{
  "tool": "enterprise_digest",
  "parameters": {
    "version": 138,
    "focus_area": "security"
  }
}
```

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

### Extract Profile Features
```json
{
  "tool": "extract_profile_features",
  "parameters": {
    "version": 138,
    "output_format": "markdown"
  }
}
```

### Check for Latest Releases
```json
{
  "tool": "check_latest_releases",
  "parameters": {
    "release_type": "both",
    "channel": "stable"
  }
}
```

## 📁 Data Organization

```
chrome-update-digest/
├── upstream_docs/           # Source data
│   ├── release_notes/      # Raw release notes
│   └── processed_releasenotes/  # Processed data
├── digest_markdown/        # Generated digests (MD)
├── digest_html/           # Generated digests (HTML)
├── feature_details/       # Feature-specific data
└── prompts/              # AI prompt templates
```

## 🔧 Direct Python Usage

For batch processing or automation, you can also use the Python scripts directly:

```bash
# Process enterprise release notes
python src/process_enterprise_release_note.py

# Process release notes with WebGPU merge (integrated pipeline)
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
- **Enterprise & Developer**: Separate tracks for different audiences
- **Fault Tolerant**: Smart file discovery and fallback mechanisms
- **Fast Processing**: Efficient YAML pipeline for quick analysis

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Chrome Platform Team for comprehensive release notes
- FastMCP framework for excellent MCP server implementation
- The open-source community for continuous improvements

---

**Get Chrome updates that matter to you, powered by AI 🚀**

For technical details and architecture information, please refer to the [Technical Overview](docs/tech_docs/technical-overview.md).