---
layout: default
title: chrome-137-en
---

## Area Summary

Chrome 137 (stable) focuses on strengthening web platform isolation, privacy, and cryptography while improving developer diagnostics. Key themes are finer-grained storage and resource partitioning (Blob URL partitioning, HSTS tracking prevention, Document-Isolation-Policy), stronger crypto primitives (Ed25519 in Web Crypto), and improved debugging data (call stacks for unresponsive pages). These updates advance security and privacy guarantees, make cross-origin resource handling more explicit, and give developers clearer signals to fix performance and correctness issues. For Web API teams, the changes shift integration and migration considerations toward per-document isolation and expanded cryptographic capabilities.

## Detailed Updates

The following entries expand on the high-level themes above and summarize what developers need to know.

### Blob URL Partitioning: Fetching/Navigation

#### What's New
Chrome partitions Blob URL access by Storage Key (top-level site, frame origin, and the has-cross-site-ancestor boolean), except top-level navigations remain partitioned only by frame origin.

#### Technical Details
Partitioning ties Blob URL access checking to the Storage Key, reducing cross-site leakage via blob URLs. Top-level navigation behavior is an exception and remains partitioned by frame origin.

#### Use Cases
- Prevents cross-site tracking or data leaks via blob: URLs between frames with different storage keys.
- Relevant for apps that generate and share blob URLs across origins or frames.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40057646 — Tracking bug #40057646
- https://chromestatus.com/feature/5037311976488960 — ChromeStatus.com entry

### Call stacks in crash reports from unresponsive web pages

#### What's New
When a page becomes unresponsive due to long-running JavaScript (e.g., infinite loops), Chrome captures the JavaScript call stack and includes it in crash/reporting data to help developers identify the cause.

#### Technical Details
The feature captures the JS call stack at the time of unresponsiveness and attaches it to the reporting/crash data used for diagnostics and developer feedback.

#### Use Cases
- Helps developers locate and fix hot loops or long-running synchronous computations causing UI hangs.
- Improves triage for unresponsive-page crashes via richer diagnostic payloads.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=1445539 — Tracking bug #1445539
- https://chromestatus.com/feature/5045134925406208 — ChromeStatus.com entry
- https://w3c.github.io/reporting/#crash-report — Spec

### Document-Isolation-Policy

#### What's New
Document-Isolation-Policy lets a document enable crossOriginIsolation for itself without deploying COOP/COEP and independent of the page's crossOriginIsolation status; the policy is backed by process isolation.

#### Technical Details
The policy enables per-document cross-origin isolation and uses process isolation to enforce it. The YAML summary notes additional effects on non-CORS cross-origin subresources.

#### Use Cases
- Sites or embedded documents that require cross-origin-isolated features (e.g., certain performance APIs or SharedArrayBuffer) can opt in per document.
- Useful for iframes or embedded widgets that need stronger isolation without page-level COOP/COEP changes.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=333029146 — Tracking bug #333029146
- https://chromestatus.com/feature/5048940296830976 — ChromeStatus.com entry
- https://wicg.github.io/document-isolation-policy/ — Spec

### Ed25519 in web cryptography

#### What's New
Adds support for Curve25519 algorithms in the Web Cryptography API, specifically the Ed25519 signature algorithm.

#### Technical Details
Ed25519 support integrates Curve25519-based signature operations into the Web Crypto API surface, enabling native generation, signing, and verification using this modern signature scheme.

#### Use Cases
- Web apps requiring modern, high-performance signature algorithms for authentication, secure messaging, or cryptographic protocols.
- Simplifies using Ed25519 from web contexts without relying on external libraries or WASM bindings.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=1370697 — Tracking bug #1370697
- https://chromestatus.com/feature/5056122982457344 — ChromeStatus.com entry
- https://www.rfc-editor.org/rfc/rfc8032.html — Spec

### HSTS tracking prevention

#### What's New
Mitigates third-party tracking via the HSTS cache by allowing HSTS upgrades only for top-level navigations and blocking HSTS upgrades for sub-resource requests.

#### Technical Details
The feature restricts HSTS-driven upgrades in subresource contexts, making it infeasible for third parties to leverage the HSTS cache to create cross-site identifiers.

#### Use Cases
- Prevents HSTS-based cross-site tracking vectors used by third-party domains.
- Affects integrations that relied on subresource HSTS upgrades; developers should ensure resources remain accessible over HTTPS or handle degraded behaviour.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40725781 — Tracking bug #40725781
- https://chromestatus.com/feature/5065878464307200 — ChromeStatus.com entry

Saved file: digest_markdown/webplatform/Web API/chrome-137-stable-en.md
