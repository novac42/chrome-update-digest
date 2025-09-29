---
layout: default
title: chrome-137-zh
---

## Area Summary

Chrome 137 的 Web API 更新集中在隔离、隐私与开发者诊断：针对 Blob URL 的存储分区、文档级隔离、针对基于 HSTS 的跟踪的保护、扩展的 Web Crypto 支持，以及改进的无响应页面崩溃报告。对开发者影响最大的更改是按存储键对 Blob URL 进行分区以及 Document-Isolation-Policy 的文档级隔离，这些更改会影响资源访问语义和进程隔离的假设。配合 HSTS 跟踪防护和 WebCrypto 中的 Ed25519，这些更新通过收紧安全/隐私保证并扩展密码学能力，同时改善难以调试的挂起问题的可观察性，推动平台前进。这些更改重要的原因在于它们可能需要在代码和部署层面做出调整（存储/URL 处理、隔离预期、密码学使用），并提升 Web 应用的健壮性与隐私属性。

## Detailed Updates

Below are the Web API area changes in Chrome 137 with concise technical context and practical implications for developers.

### Blob URL Partitioning: Fetching/Navigation (Blob URL 存储分区：获取/导航)

#### What's New
Chrome partitions Blob URL access by Storage Key (top-level site, frame origin, and the has-cross-site-ancestor boolean). Top-level navigations remain partitioned only by frame origin.

#### Technical Details
Partitioning uses Storage Key semantics to separate Blob URL access scopes; top-level navigation behavior is an exception and stays partitioned by frame origin.

#### Use Cases
Affects apps that generate or consume blob: URLs across frames/sites — developers should verify Blob URL visibility and sharing across origins/frames under storage partitioning.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40057646 (Tracking bug #40057646)  
- https://chromestatus.com/feature/5037311976488960 (ChromeStatus.com entry)

### Call stacks in crash reports from unresponsive web pages (无响应页面崩溃报告中的调用栈)

#### What's New
When a page becomes unresponsive due to long-running JavaScript (e.g., infinite loops), Chrome captures the JavaScript call stack and includes it in reports to help identify causes.

#### Technical Details
The runtime captures the JS stack at hang detection and attaches it to the crash/unresponsiveness report for diagnostics.

#### Use Cases
Improves debugging for pages that freeze due to heavy JS; developers can use captured stacks to pinpoint and fix long-running computations or infinite loops.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=1445539 (Tracking bug #1445539)  
- https://chromestatus.com/feature/5045134925406208 (ChromeStatus.com entry)  
- https://w3c.github.io/reporting/#crash-report (Spec)

### Document-Isolation-Policy (文档隔离策略)

#### What's New
Document-Isolation-Policy lets a document enable crossOriginIsolation for itself without deploying COOP/COEP and independent of the page’s crossOriginIsolation status. The policy is backed by process isolation.

#### Technical Details
Documents can opt into isolation at the document level; process isolation underpins the policy. The content notes that non-CORS cross-origin subresources will either... (see tracking links for full spec/behavior).

#### Use Cases
Useful for pages or embedded documents that require isolated execution contexts (e.g., to access powerful APIs) without site-wide COOP/COEP deployment; developers embedding cross-origin content should review subresource behavior.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=333029146 (Tracking bug #333029146)  
- https://chromestatus.com/feature/5048940296830976 (ChromeStatus.com entry)  
- https://wicg.github.io/document-isolation-policy/ (Spec)

### Ed25519 in web cryptography (WebCrypto 中的 Ed25519)

#### What's New
Adds support for Curve25519 algorithms in the Web Cryptography API, specifically the Ed25519 signature algorithm.

#### Technical Details
WebCrypto now exposes Ed25519-related primitives per the referenced tracking bug and standards (RFC 8032).

#### Use Cases
Enables web apps to generate and verify Ed25519 signatures natively via WebCrypto, benefiting modern cryptographic workflows and interoperability with systems using Ed25519.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=1370697 (Tracking bug #1370697)  
- https://chromestatus.com/feature/5056122982457344 (ChromeStatus.com entry)  
- https://www.rfc-editor.org/rfc/rfc8032.html (Spec)

### HSTS tracking prevention (基于 HSTS 的跟踪防护)

#### What's New
Mitigates cross-site tracking via the HSTS cache by allowing HSTS upgrades only for top-level navigations and blocking HSTS upgrades for sub-resource requests.

#### Technical Details
Restricts HSTS-induced protocol upgrades in subresource contexts, preventing third parties from leveraging HSTS state to fingerprint or track users.

#### Use Cases
Third-party resources can no longer rely on HSTS cache behavior for tracking; developers of privacy-sensitive third-party services should audit any HSTS-based assumptions.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40725781 (Tracking bug #40725781)  
- https://chromestatus.com/feature/5065878464307200 (ChromeStatus.com entry)

## Area-Specific Expertise Notes

- css: Blob URL partitioning and document isolation can influence cross-origin resource loading and layout embedding scenarios; review resource fetch semantics when styling/embedding cross-origin content.
- webapi: These updates change resource access and isolation APIs and add cryptographic primitives (Ed25519) accessible through WebCrypto.
- graphics-webgpu: Document-level isolation affects capability exposure for powerful APIs; check isolation requirements for GPU or compute-based APIs.
- javascript: Call-stack capture for unresponsive pages improves debugging of long-running JS; developers should leverage this for optimizing event loops and worker use.
- security-privacy: HSTS tracking prevention and Document-Isolation-Policy tighten privacy and process isolation boundaries; update threat models and deployment strategies.
- performance: Blob partitioning and isolation changes can affect cross-origin resource retrieval paths and caching; measure impacts on load performance.
- multimedia: Blob URL visibility changes may affect media blobs shared between frames or origins.
- devices: Document isolation may be a path to enable sensitive device APIs per-document without site-wide headers.
- pwa-service-worker: Storage partitioning semantics can influence service worker-controlled fetches and resource caching strategies.
- webassembly: Isolation and improved cryptography affect secure WASM usage and signing/verification flows.
- 弃用: Review code that assumes global Blob URL reachability or HSTS behaviors; plan migration or testing for partitioned environments.

已保存文件：digest_markdown/webplatform/Web API/chrome-137-stable-en.md
