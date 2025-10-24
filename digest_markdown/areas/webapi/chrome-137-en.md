---
layout: default
title: chrome-137-en
---

## Detailed Updates

Below are focused summaries and developer-facing implications for each Web API change in Chrome 137.

### Blob URL Partitioning: Fetching/Navigation

#### What's New
As part of Storage Partitioning, Chrome partitions Blob URL access by Storage Key (top-level site, frame origin, and the has-cross-site-ancestor boolean). Top-level navigations remain partitioned only by frame origin.

#### Technical Details
Partitioning uses the Storage Key components to scope Blob URL access, reducing cross-site data leakage across frames and sites. Top-level navigation behavior is an explicit exception, remaining frame-origin partitioned.

#### Use Cases
Helps developers building multi-origin apps or embeds avoid accidental Blob-based data exposure across storage partitions and improves alignment with site-isolated storage expectations.

#### References
- Tracking bug #40057646: https://bugs.chromium.org/p/chromium/issues/detail?id=40057646
- ChromeStatus.com entry: https://chromestatus.com/feature/5037311976488960

### Call stacks in crash reports from unresponsive web pages

#### What's New
Chrome captures the JavaScript call stack when a page becomes unresponsive due to long-running or infinite JS execution; the call stack is included in crash/unresponsive reports.

#### Technical Details
The feature collects the runtime JS call stack at the time of unresponsiveness and attaches it to reporting artifacts, aligning with reporting/crash telemetry flows to aid root-cause analysis.

#### Use Cases
Improves debugging of pages that hang from long computations or runaway loops; useful for observability, error triage, and prioritizing fixes for performance- or correctness-related hangs.

#### References
- Tracking bug #1445539: https://bugs.chromium.org/p/chromium/issues/detail?id=1445539
- ChromeStatus.com entry: https://chromestatus.com/feature/5045134925406208
- Spec: https://w3c.github.io/reporting/#crash-report

### Document-Isolation-Policy

#### What's New
Document-Isolation-Policy allows an individual document to enable crossOriginIsolation for itself without deploying COOP/COEP site-wide, backed by process isolation.

#### Technical Details
The policy signals per-document isolation (process isolation) and affects handling of non-CORS cross-origin subresources (behavior described in linked spec/notes). It provides a mechanism to opt a document into stronger isolation independently of the embedding page’s global headers.

#### Use Cases
Enables third-party or embedded documents to opt into cross-origin isolation for features that require it (e.g., certain powerful APIs) without requiring site-wide COOP/COEP deployment.

#### References
- Tracking bug #333029146: https://bugs.chromium.org/p/chromium/issues/detail?id=333029146
- ChromeStatus.com entry: https://chromestatus.com/feature/5048940296830976
- Spec: https://wicg.github.io/document-isolation-policy/

### Ed25519 in web cryptography

#### What's New
Chrome adds support for Curve25519 algorithms in the Web Cryptography API, specifically the Ed25519 signature algorithm.

#### Technical Details
Ed25519 support is exposed via the Web Crypto API (SubtleCrypto) as a native signing/verification primitive, aligning browser crypto capabilities with RFC 8032 for Ed25519 signatures.

#### Use Cases
Allows web applications to perform modern, secure signature operations (e.g., authentication tokens, signed metadata) using Ed25519 without shipping JS/WASM crypto libraries.

#### References
- Tracking bug #1370697: https://bugs.chromium.org/p/chromium/issues/detail?id=1370697
- ChromeStatus.com entry: https://chromestatus.com/feature/5056122982457344
- Spec: https://www.rfc-editor.org/rfc/rfc8032.html

### HSTS tracking prevention

#### What's New
Chrome prevents third-party tracking using the HSTS cache by allowing HSTS upgrades only for top-level navigations and blocking HSTS upgrades for sub-resource requests.

#### Technical Details
HSTS upgrades are restricted based on request context: top-level navigations may be upgraded, while subresource requests are blocked from performing HSTS-driven upgrades, reducing a third party’s ability to fingerprint users via HSTS state.

#### Use Cases
Mitigates tracking techniques that relied on HSTS state to differentiate users across sites; relevant for developers concerned with privacy-preserving defaults and third-party resource loading behavior.

#### References
- Tracking bug #40725781: https://bugs.chromium.org/p/chromium/issues/detail?id=40725781
- ChromeStatus.com entry: https://chromestatus.com/feature/5065878464307200

File target path:
digest_markdown/webplatform/Web API/chrome-137-stable-en.md
