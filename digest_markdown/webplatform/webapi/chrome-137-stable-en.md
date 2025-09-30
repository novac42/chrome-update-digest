## Area Summary

Chrome 137's Web API updates emphasize privacy, security, and developer diagnostics across the platform. Key changes include stronger resource and storage partitioning, a document-level isolation policy for cross-origin isolation, built-in Ed25519 support in Web Crypto, mitigation of HSTS-based tracking, and richer crash diagnostics for unresponsive pages. These updates advance the web by tightening isolation boundaries, expanding cryptographic capabilities, reducing cross-site tracking vectors, and improving developer ability to diagnose client-side hangs. Together they lower risk for web developers and enhance user privacy and security guarantees.

## Detailed Updates

The following items expand on the themes above and highlight practical implications for Web API consumers and implementers.

### Blob URL Partitioning: Fetching/Navigation

#### What's New
Partitioning of Blob URL access by Storage Key (top-level site, frame origin, and the has-cross-site-ancestor boolean) has been implemented; top-level navigations remain partitioned only by frame origin.

#### Technical Details
Blob URL access is now scoped to Storage Key boundaries to align with Storage Partitioning. This changes how blob URLs are resolved for subresources and frames, enforcing per-site/frame isolation except for top-level navigations which keep origin-only partitioning.

#### Use Cases
- Prevents cross-site leakage via blob URLs in embedded frames.
- Helps developers relying on blob URLs for resource delivery understand cross-origin resolution changes.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40057646 (Tracking bug #40057646)
- https://chromestatus.com/feature/5037311976488960 (ChromeStatus.com entry)

### Call stacks in crash reports from unresponsive web pages

#### What's New
When a page becomes unresponsive due to long-running JavaScript (e.g., infinite loop), Chrome captures and includes the JavaScript call stack in crash/unresponsive reports.

#### Technical Details
The feature records the JS call stack at unresponsive time and includes it in the reporting payload, enabling root-cause analysis for runtime hangs.

#### Use Cases
- Improves developer debugging for performance and liveness issues.
- Aids triage of client-side infinite loops or blocking computations.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=1445539 (Tracking bug #1445539)
- https://chromestatus.com/feature/5045134925406208 (ChromeStatus.com entry)
- https://w3c.github.io/reporting/#crash-report (Spec)

### Document-Isolation-Policy

#### What's New
Document-Isolation-Policy lets a document enable crossOriginIsolation for itself (independent of page COOP/COEP) and is backed by process isolation; non-CORS cross-origin subresources are treated differently under the policy.

#### Technical Details
A document can declare isolation at the document level, triggering process isolation and changing handling of cross-origin non-CORS subresources according to the policy semantics.

#### Use Cases
- Allows pages to opt into cross-origin isolation features without whole-site COOP/COEP deployment.
- Useful for developers needing isolated contexts (e.g., for powerful APIs) while avoiding site-wide header changes.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=333029146 (Tracking bug #333029146)
- https://chromestatus.com/feature/5048940296830976 (ChromeStatus.com entry)
- https://wicg.github.io/document-isolation-policy/ (Spec)

### Ed25519 in web cryptography

#### What's New
Adds support for Curve25519 algorithms in the Web Cryptography API, notably the Ed25519 signature algorithm.

#### Technical Details
Ed25519 key generation, signing, and verification are exposed via the WebCrypto API surface so web apps can use Ed25519 primitives natively.

#### Use Cases
- Modern signature schemes for client-side cryptography and authentication.
- Enables libraries and applications to adopt Ed25519 without polyfills or WASM fallbacks.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=1370697 (Tracking bug #1370697)
- https://chromestatus.com/feature/5056122982457344 (ChromeStatus.com entry)
- https://www.rfc-editor.org/rfc/rfc8032.html (Spec)

### HSTS tracking prevention

#### What's New
Mitigates third-party tracking via the HSTS cache by allowing HSTS upgrades only for top-level navigations and blocking HSTS upgrades for subresource requests.

#### Technical Details
The HSTS upgrade behavior is restricted so subresource requests cannot leverage the HSTS cache for cross-site tracking; top-level navigations still receive HSTS upgrades.

#### Use Cases
- Reduces feasibility of using HSTS state as a cross-site tracking channel.
- Web developers concerned with third-party privacy implications should expect fewer cross-site HSTS-induced redirects for subresources.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40725781 (Tracking bug #40725781)
- https://chromestatus.com/feature/5065878464307200 (ChromeStatus.com entry)

Saved to: digest_markdown/webplatform/Web API/chrome-137-stable-en.md