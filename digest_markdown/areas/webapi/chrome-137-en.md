---
layout: default
title: chrome-137-en
---

## Area Summary

Chrome 137’s Web API updates focus on isolation, privacy, and developer diagnostics: storage partitioning for Blob URLs, document-level isolation, protections against HSTS-based tracking, expanded Web Crypto support, and improved crash reporting for unresponsive pages. The most impactful changes for developers are storage-keyed Blob URL partitioning and document-level isolation (Document-Isolation-Policy), which affect resource access semantics and process isolation assumptions. Together with HSTS tracking prevention and Ed25519 in WebCrypto, these updates advance the platform by tightening security/privacy guarantees and broadening cryptographic capabilities while improving observability for hard-to-debug hangs. These changes matter because they can require code- and deployment-level adjustments (storage/URL handling, isolation expectations, cryptography usage) and they improve the robustness and privacy properties of web apps.

## Detailed Updates

Below are the Web API area changes in Chrome 137 with concise technical context and practical implications for developers.

### Blob URL Partitioning: Fetching/Navigation

#### What's New
Chrome partitions Blob URL access by Storage Key (top-level site, frame origin, and the has-cross-site-ancestor boolean). Top-level navigations remain partitioned only by frame origin.

#### Technical Details
Partitioning uses Storage Key semantics to separate Blob URL access scopes; top-level navigation behavior is an exception and stays partitioned by frame origin.

#### Use Cases
Affects apps that generate or consume blob: URLs across frames/sites — developers should verify Blob URL visibility and sharing across origins/frames under storage partitioning.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40057646 (Tracking bug #40057646)  
- https://chromestatus.com/feature/5037311976488960 (ChromeStatus.com entry)

### Call stacks in crash reports from unresponsive web pages

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

### Document-Isolation-Policy

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

### Ed25519 in web cryptography

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

### HSTS tracking prevention

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
- deprecations: Review code that assumes global Blob URL reachability or HSTS behaviors; plan migration or testing for partitioned environments.

Saved file:
digest_markdown/webplatform/Web API/chrome-137-stable-en.md
