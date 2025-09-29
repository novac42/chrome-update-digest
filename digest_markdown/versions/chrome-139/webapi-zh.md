---
layout: default
title: webapi-zh
---

## Area Summary

Chrome 139 的 Web API 更新侧重于提高网页应用的互操作性、平台正确性以及开发者对诊断的控制。主要更改包括跨来源的 web app scope 扩展、按 WHATWG mimesniff spec 更严格的 JSON MIME 类型检测、用于表明符合规范核心特性与限制的 WebGPU 支持标识，以及针对崩溃上报的专用 Crash Reporting API 端点选项。这些更新减少了多来源应用集成摩擦，使基于内容类型的 JS API 行为更可预测，澄清了 GPU 能力信号，并为开发者提供更精确的崩溃遥测路由 —— 全面提升了 Web 的可靠性和开发者使用体验。

## Detailed Updates

The following summarizes each Web API feature in Chrome 139 and the practical implications for developers.

### Web app scope extensions (扩展 web 应用的 scope 到其他来源)

#### What's New
Adds a `scope_extensions` web app manifest field that enables web apps to extend their scope to other origins, allowing sites that control multiple subdomains and top level domains to be presented as a single web app.

#### Technical Details
- Introduces a manifest field (`scope_extensions`) to list additional origins.
- Listed origins must confirm association with the web app (see spec links for association requirements).
- Relevant tags: webapi, service-worker/PWA integration and origin association semantics.

#### Use Cases
- Consolidating multiple domains/subdomains into one installable web app.
- Simplifying navigation, deep links, and back/forward behavior across related origins.

#### References
- https://issues.chromium.org/issues/detail?id=1250011
- https://chromestatus.com/feature/5746537956114432
- https://github.com/WICG/manifest-incubations/pull/113

### Specification-compliant JSON MIME type detection (兼容规范的 JSON MIME 类型检测)

#### What's New
Chrome now recognizes all valid JSON MIME types as defined by the WHATWG mimesniff specification, including any MIME type whose subtype ends with `+json`, in addition to `application/json` and `text/json`.

#### Technical Details
- MIME sniffing behavior for JSON detection updated to match the WHATWG mimesniff rules.
- Affects APIs and features that branch behavior based on JSON content-type detection (fetch, XHR, content sniffers).

#### Use Cases
- Ensures consistent parsing/handling of vendor-specific JSON media types (e.g., `application/ld+json`, `application/vnd.example+json`).
- Reduces accidental misclassification and parsing errors in client code that depends on content-type detection.

#### References
- https://chromestatus.com/feature/5470594816278528
- https://mimesniff.spec.whatwg.org/#json-mime-type

### WebGPU `core-features-and-limits` (指示符合规范的核心特性与限制)

#### What's New
The `core-features-and-limits` feature flag indicates a WebGPU adapter and device support the core features and limits defined by the WebGPU spec.

#### Technical Details
- Signals adapter/device conformance to a baseline set of features and limits.
- Helps feature detection and capability probing in graphics and compute pipelines.
- Relevant tags: webapi, webgpu, graphics-webgpu, performance.

#### Use Cases
- Allowing applications to reliably detect a spec-compliant GPU environment before enabling advanced rendering paths.
- Simplifying feature-gating logic in libraries that target WebGPU.

#### References
- https://issues.chromium.org/issues/418025721
- https://chromestatus.com/feature/4744775089258496
- https://gpuweb.github.io/gpuweb/#core-features-and-limits

### Crash Reporting API: Specify `crash-reporting` to receive only crash reports (仅接收崩溃报告的端点配置)

#### What's New
Developers can specify the endpoint named `crash-reporting` to receive only crash reports; by default, crash reports go to the `default` endpoint which also receives other report types.

#### Technical Details
- Adds a way to register a separate URL for crash report delivery via the well-known endpoint configuration.
- Enables separation of crash telemetry from other reporting categories for finer-grained handling and privacy controls.
- Relevant tags: webapi, security-privacy (telemetry routing and endpoint separation).

#### Use Cases
- Routing crash reports to a dedicated telemetry endpoint for processing without mixing other report types.
- Implementing stricter ingestion and storage policies for crash data.

#### References
- https://issues.chromium.org/issues/414723480
- https://chromestatus.com/feature/5129218731802624
- https://wicg.github.io/crash-reporting/#crash-reports-delivery-priority

已保存文件：digest_markdown/webplatform/Web API/chrome-139-stable-en.md
