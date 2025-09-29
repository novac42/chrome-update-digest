---
layout: default
title: chrome-139-en
---

## Detailed Updates

The following Network-specific items from Chrome 139 are summarized with practical implications for developers and operations teams.

### Reduce fingerprinting in Accept-Language header information

#### What's New
Reduces the amount of information the `Accept-Language` header value string exposes in HTTP requests and in `navigator.languages`. Instead of sending a full list of the user's preferred languages on every HTTP request using the `Accept-Language` header, Chrome only sends the user's most preferred la...

#### Technical Details
The change truncates the language signal sent from the browser to servers and to the `navigator.languages` API surface, limiting the data available for cross-site fingerprinting and server-side inference.

#### Use Cases
- Privacy-sensitive web apps and analytics should expect less granular per-request language data.
- Server-side content negotiation relying on full language lists must adapt to receiving only the top-preferred language.

#### References
- Tracking bug #1306905 — https://issues.chromium.org/issues/1306905
- ChromeStatus.com entry — https://chromestatus.com/feature/5188040623390720

### Randomize TCP port allocation on Windows

#### What's New
Enables TCP port randomization on versions of Windows (2020 or later) where port re-use issues are not expected to occur too rapidly, addressing allocation predictability and reuse-related failures.

#### Technical Details
The launch randomizes ephemeral TCP port selection to reduce collisions and the likelihood of rejections caused by rapid port re-use. The rollout targets Windows releases where the risk of problematic fast re-use (a manifestation of the Birthday problem) is low.

#### Use Cases
- Servers and clients should see fewer transient connection failures due to port re-use collisions on supported Windows versions.
- Network debugging and NAT/firewall rules should account for increased ephemeral port entropy.

#### References
- Tracking bug #40744069 — https://issues.chromium.org/issues/40744069
- ChromeStatus.com entry — https://chromestatus.com/feature/5106900286570496

Area-Specific Expertise (Network implications)

- css: No direct impact in this release; style/layout behaviors unaffected by these Network changes.
- webapi: `navigator.languages` exposure is reduced; web apps reading this API will receive less data.
- graphics-webgpu: Not applicable to these Network items.
- javascript: Client-side scripts that inspect `navigator.languages` should handle reduced language lists.
- security-privacy: Primary beneficiary—reduces fingerprinting surface and increases transport-layer unpredictability.
- performance: TCP port randomization can improve connection reliability but may affect diagnostics that assume deterministic ports.
- multimedia: Media streaming stacks should be resilient to ephemeral port behavior; no codec changes.
- devices: No direct device-API implications.
- pwa-service-worker: Service workers should continue to function; accept-language changes may affect localized fetch responses.
- webassembly: No direct impact.
- deprecations: No deprecations announced for Network in this data.

Save path

```text
digest_markdown/webplatform/Network/chrome-139-stable-en.md
