# Chrome Release Notes Focus Areas

This document describes the 23 focus areas used to organize Chrome release notes.

## Overview

Chrome release notes are automatically parsed and categorized into these focus areas based on heading patterns and keywords defined in [config/focus_areas.yaml](../../../../config/focus_areas.yaml).

## Core Web Platform Areas

### css
**CSS styling, layout, and UI features**
- Heading patterns: "CSS", "CSS and UI", "Styling"
- Priority: High
- Examples: CSS Grid, Flexbox, CSS animations, color features

### html-dom
**HTML elements and DOM manipulation**
- Heading patterns: "HTML", "DOM", "HTML and DOM"
- Priority: Medium
- Examples: HTML elements, DOM APIs, element properties

### webapi
**Web APIs and browser interfaces**
- Heading patterns: "Web APIs", "Web API"
- Priority: High
- Special: Can have multiple tags (APIs span many areas)
- Examples: Fetch API, Storage API, Web APIs

### javascript
**JavaScript language features and runtime updates**
- Heading patterns: "JavaScript", "JS"
- Priority: Medium
- Examples: ECMAScript features, runtime improvements

### webassembly
**WebAssembly runtime and tooling updates**
- Heading patterns: "WebAssembly", "Wasm"
- Priority: Medium
- Examples: WebAssembly features, Wasm tooling

## Graphics and Media

### graphics-webgpu
**Graphics rendering and WebGPU features**
- Heading patterns: "WebGPU", "Graphics"
- Priority: High
- Special: Merges content from Chrome Graphics and dedicated WebGPU release notes
- Examples: WebGPU APIs, Canvas2D, rendering features

### multimedia
**Media, audio, and video features**
- Heading patterns: "Multimedia", "audio and video", "WebRTC"
- Priority: Medium
- Examples: Video playback, audio APIs, WebRTC

## Emerging Technologies

### on-device-ai
**On-device AI and LLM features**
- Keywords: "on-device ai", "language model"
- Heading patterns: "On-device AI"
- Priority: High
- Special: Also searches feature content for AI keywords (not just headings)
- Examples: Gemini Nano, Prompt API, AI-powered features

### isolated-web-apps
**Isolated Web Apps (IWAs) and related features**
- Heading patterns: "Isolated Web Apps", "IWAs"
- Priority: Medium
- Examples: IWA installation, permissions, capabilities

### pwa-service-worker
**Progressive Web Apps and service worker features**
- Heading patterns: "PWA", "Service Worker", "Progressive Web Apps"
- Priority: Low
- Examples: Service worker updates, PWA installation, offline capabilities

## Security and Privacy

### security-privacy
**Security and privacy features**
- Heading patterns: "Security", "Privacy", "Privacy and security"
- Priority: High
- Examples: HTTPS, cookies, permissions, encryption

### identity
**Identity, sign-in, and account features**
- Heading patterns: "Identity"
- Priority: Low
- Examples: FedCM, sign-in APIs

## Performance and Lifecycle

### performance
**Performance optimizations and improvements**
- Heading patterns: "Performance"
- Priority: Medium
- Examples: Loading speed, rendering performance, memory optimization

### navigation-loading
**Navigation and resource loading features**
- Heading patterns: "Loading", "Navigation"
- Priority: Low
- Examples: Navigation API, resource loading, prefetch

### network
**Networking and connectivity features**
- Heading patterns: "Network"
- Priority: Low
- Examples: HTTP features, network protocols, fetch

## Device Integration

### devices
**Device APIs and sensor features**
- Heading patterns: "Device", "Devices", "Sensors"
- Priority: Low
- Examples: Geolocation, sensors, device orientation

### payment
**Payment and payment-related features**
- Heading patterns: "Payment", "Payments", "Secure Payment Confirmation"
- Priority: Medium
- Examples: Payment Request API, payment methods

## Developer Experience

### devtools
**Developer Tools and debugging features**
- Heading patterns: "Developer Tools", "DevTools"
- Priority: Medium
- Examples: DevTools panels, debugging features, performance profiling

### browser-changes
**Platform-level browser behavior updates**
- Heading patterns: "Browser changes"
- Priority: Medium
- Examples: Browser UI changes, behavior updates

## Enterprise and Beta

### enterprise
**Enterprise policies and admin features**
- Heading patterns: "Enterprise"
- Priority: Low
- Examples: Group policies, admin controls, enterprise features

### origin-trials
**Experimental features in origin trials**
- Heading patterns: "Origin trials"
- Priority: Medium
- Examples: New APIs in trial phase, experimental features

### deprecations
**Deprecated and removed features**
- Heading patterns: "Deprecations", "Deprecations and removals", "Removals"
- Priority: Medium
- Examples: Deprecated APIs, removed features, breaking changes

## Area Priority Levels

Areas are assigned priority levels to guide digest generation:

- **Priority 1 (High)**: Core web platform features most relevant to developers
  - css, webapi, graphics-webgpu, on-device-ai, security-privacy

- **Priority 2 (Medium)**: Important but more specialized features
  - html-dom, javascript, webassembly, multimedia, performance, etc.

- **Priority 3 (Low)**: Specialized or less frequently updated areas
  - devices, pwa-service-worker, navigation-loading, network, identity, enterprise

## Extraction Strategy

### Standard Areas
Most areas use **heading-only matching**:
1. Parse h2 headings in release notes
2. Match against heading_patterns (case-insensitive)
3. Extract all content under matching headings

### Special Cases

**on-device-ai**:
- Also searches feature **content** for keywords ("on-device ai", "language model")
- Identifies AI features scattered across other sections

**graphics-webgpu**:
- Merges content from two sources:
  1. Chrome release notes "Graphics" section
  2. Dedicated WebGPU release notes (webgpu-{version}.md)
- Deduplicates features with WebGPU-specific content taking priority

**webapi**:
- Can have multiple tags (one feature may belong to multiple areas)
- Broad catch-all for Web APIs

## Common Patterns

### Heading Variations
Many areas support multiple heading patterns to handle variations:
- "CSS" vs "CSS and UI"
- "Web APIs" vs "Web API" (singular/plural)
- "Deprecations" vs "Deprecations and removals"

### Channel Differences
- **Stable**: Final release, comprehensive feature list
- **Beta**: Earlier release, may have fewer features or different focus

### Version Consistency
- Not all areas appear in every version
- Some areas (like "on-device-ai") are relatively new
- Core areas (CSS, Web APIs, Security) appear in most versions

## Using Areas in Processing

### Process all areas:
```bash
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
  --version 139 --verbose
```

### Process specific areas:
```bash
uv run python .claude/skills/chrome-update-digest/scripts/process_chrome.py \
  --version 139 --areas css webapi graphics-webgpu --verbose
```

### Common subsets:
```bash
# Core web platform (5 areas)
--areas css webapi html-dom javascript graphics-webgpu

# AI and emerging tech (3 areas)
--areas on-device-ai isolated-web-apps pwa-service-worker

# Security and privacy (2 areas)
--areas security-privacy identity

# Developer experience (2 areas)
--areas devtools browser-changes
```

## Output Structure

Each area produces two files:
- **YAML**: Structured data (`chrome-{version}-{channel}.yml`)
- **Markdown**: Human-readable content (`chrome-{version}-{channel}.md`)

Output location:
```
upstream_docs/processed_releasenotes/processed_forwebplatform/areas/
├── css/
│   ├── chrome-139-stable.yml
│   └── chrome-139-stable.md
├── webapi/
│   ├── chrome-139-stable.yml
│   └── chrome-139-stable.md
└── ... (21 more areas)
```

## References

- Full configuration: [config/focus_areas.yaml](../../../../config/focus_areas.yaml)
- Processing pipeline: [src/chrome_update_digest/processors/clean_data_pipeline.py](../../../../src/chrome_update_digest/processors/clean_data_pipeline.py)
- Area extractors: [src/chrome_update_digest/processors/area_extractors.py](../../../../src/chrome_update_digest/processors/area_extractors.py)
