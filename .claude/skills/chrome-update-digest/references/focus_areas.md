# Chrome Update Digest - Focus Areas Reference

This document describes the 23+ focus areas that the Chrome Update Digest processes.

## Core Web Platform

### CSS
- **Description**: CSS features, properties, selectors, and styling capabilities
- **Heading Patterns**: "CSS", "CSS and UI"
- **Example Features**: Container queries, cascade layers, new color functions

### HTML & DOM
- **Description**: HTML elements, DOM APIs, and document structure
- **Heading Patterns**: "HTML", "DOM"
- **Example Features**: New HTML elements, DOM manipulation APIs

### JavaScript
- **Description**: ECMAScript features, language improvements
- **Heading Patterns**: "JavaScript", "JS", "ECMAScript"
- **Example Features**: New syntax, standard library additions

## Web APIs

### Web APIs
- **Description**: General web platform APIs
- **Heading Patterns**: "Web APIs", "APIs"
- **Example Features**: Fetch, Streams, File System Access, etc.

### PWA & Service Worker
- **Description**: Progressive Web App capabilities and Service Worker features
- **Heading Patterns**: "PWA", "Progressive Web Apps", "Service Workers"
- **Example Features**: Install prompts, offline capabilities, background sync

### WebRTC
- **Description**: Real-time communication APIs
- **Heading Patterns**: "WebRTC", "RTC"
- **Example Features**: Video/audio calling, peer-to-peer data transfer

### WebAssembly
- **Description**: WebAssembly features and tooling
- **Heading Patterns**: "WebAssembly", "Wasm"
- **Example Features**: SIMD, threading, exception handling

## Graphics & Multimedia

### Graphics & WebGPU
- **Description**: Graphics APIs including WebGPU, Canvas, and rendering
- **Heading Patterns**: "Graphics", "WebGPU", "Rendering"
- **Example Features**: WebGPU shaders, compute pipelines, graphics performance
- **Special**: Merges Chrome Graphics section with dedicated WebGPU release notes

### Multimedia
- **Description**: Audio and video APIs
- **Heading Patterns**: "Media", "Audio", "Video"
- **Example Features**: Media capture, codecs, streaming

## Platform & Performance

### Performance
- **Description**: Performance APIs and optimizations
- **Heading Patterns**: "Performance"
- **Example Features**: Performance monitoring, resource timing, optimization hints

### Network
- **Description**: Networking APIs and protocols
- **Heading Patterns**: "Network", "Networking"
- **Example Features**: HTTP/3, connection management, fetch improvements

### Navigation & Loading
- **Description**: Page navigation and resource loading
- **Heading Patterns**: "Navigation", "Loading"
- **Example Features**: Navigation API, prerendering, resource hints

## Device & System

### Devices
- **Description**: Device APIs for hardware access
- **Heading Patterns**: "Devices", "Hardware"
- **Example Features**: USB, Bluetooth, sensors, geolocation

## Security & Privacy

### Security & Privacy
- **Description**: Security features and privacy enhancements
- **Heading Patterns**: "Security", "Privacy"
- **Example Features**: Permissions, HTTPS, secure contexts, privacy sandbox

### Identity
- **Description**: Authentication and identity management
- **Heading Patterns**: "Identity", "Authentication", "FedCM"
- **Example Features**: Federated Credential Management, WebAuthn

### Payment
- **Description**: Web payments and related APIs
- **Heading Patterns**: "Payment" (substring match)
- **Example Features**: Payment Request API, payment handlers

## Emerging Technologies

### On-Device AI
- **Description**: Machine learning and AI capabilities running locally
- **Heading Patterns**: Content-based keyword search
- **Keywords**: "AI", "machine learning", "ML", "neural network", "on-device", "Gemini Nano"
- **Special**: Searches content keywords across all sections, not just headings
- **Example Features**: Prompt API, translation API, summarization

### Origin Trials
- **Description**: Experimental features available for testing
- **Heading Patterns**: "Origin Trials", "Origin Trial"
- **Example Features**: Features in experimental phase requiring opt-in

## Browser & Developer

### Browser Changes
- **Description**: Changes to browser behavior, UI, and capabilities
- **Heading Patterns**: "Browser", "Chrome"
- **Example Features**: UI updates, policy changes, feature flags

### Deprecations
- **Description**: Features being deprecated or removed
- **Heading Patterns**: "Deprecations", "Removals", "Deprecated"
- **Example Features**: Deprecated APIs, removed features, migration paths

### DevTools
- **Description**: Chrome DevTools improvements
- **Heading Patterns**: "DevTools", "Developer Tools" (substring match)
- **Example Features**: New panels, debugging capabilities, performance tools

## Other

### Other
- **Description**: Features that don't fit into predefined categories
- **Usage**: Catchall for unclassified content

---

## Area Classification Logic

### Heading-Based Classification
Most areas are classified by matching section headings in the release notes:
- Exact match: `"CSS" heading → css area`
- Partial match: `"CSS and UI" heading → css area`
- Case-insensitive matching

### Content-Based Classification
Some areas (like on-device-ai) search content keywords:
- Keywords defined in `config/focus_areas.yaml`
- Searches feature title and content body
- Used when `search_content_keywords: true`

### Multi-Source Classification
Graphics-WebGPU area merges content from:
1. Chrome release notes (Graphics/WebGPU sections)
2. Dedicated WebGPU release notes (`webgpu-{version}.md`)
3. Deduplication applied to avoid duplicate features

### Cross-Cutting Concerns
Features can appear in multiple areas:
- AI features: both `origin-trials` and `on-device-ai`
- Security features: both primary area and `security-privacy`
- Tagged for discoverability across areas

---

## Configuration

All area definitions live in `.claude/skills/chrome-update-digest/config/focus_areas.yaml`.

Each area includes:
- `heading_patterns`: List of heading text to match
- `keywords`: Content keywords (if `search_content_keywords: true`)
- `description`: Human-readable description
- `search_content_keywords`: Whether to search content (default: false)

## Output Structure

For each area and version, the pipeline generates:
```
upstream_docs/processed_releasenotes/processed_forwebplatform/areas/{area}/
├── chrome-{version}-{channel}.md      # Human-readable extracted content
└── chrome-{version}-{channel}.yml     # Structured data with links and metadata
```

Example:
```
areas/css/
├── chrome-143-stable.md
└── chrome-143-stable.yml
```

The YAML file includes:
- Feature titles and content
- Extracted links (spec links, demo links, doc links)
- Tags and cross-cutting concerns
- Heading hierarchy preservation
- Statistics (feature count, link count)

---

*This reference describes the focus area system as of January 2025. Areas may be added or modified over time to reflect Chrome's evolving platform.*
