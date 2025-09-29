## Area Summary

Chrome 137 的 Web API 更新侧重于隐私、安全和平台级健壮性：存储与资源分区、HSTS 跟踪缓解，以及文档级隔离。通过在页面无响应时捕获 JavaScript 调用栈并扩展对 Ed25519 的加密支持，开发者获得了改进的工具和诊断能力。这些更改通过减少跨站点跟踪向量、在不全面部署 COOP/COEP 的情况下更安全地使用强大 API，以及使调试和现代加密使用更为可行，推动了 Web 的发展。对于维护 Web 应用的团队而言，此版本强调了对隐私、可观测性和密码学现代化的优先级。

## Detailed Updates

The following items expand on the summary above with concise technical and developer-focused details.

### Blob URL Partitioning: Fetching/Navigation

#### What's New
Partitioning of Blob URL access by Storage Key (top-level site, frame origin, and has-cross-site-ancestor boolean) has been implemented as part of Storage Partitioning; top-level navigations remain partitioned only by frame origin.

#### Technical Details
Partitioning isolates Blob URL access to a storage key boundary, tying Blob access checks to site/frame origin context and cross-site ancestry. Top-level navigations are treated as an exception and continue to use frame-origin partitioning.

#### Use Cases
Prevents cross-site Blob URL leakage and reduces cross-origin data exposure for embedded resources and frames, helping developers relying on Blobs for in-page data to align with 隐私边界。

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40057646 (Tracking bug #40057646)  
- https://chromestatus.com/feature/5037311976488960 (ChromeStatus.com entry)

### Call stacks in crash reports from unresponsive web pages

#### What's New
Chrome now captures the JavaScript call stack when a page becomes unresponsive due to long-running JS (e.g., infinite loops), and includes it in crash/unresponsive reports.

#### Technical Details
The feature records the JS call stack at the point of unresponsiveness and attaches that information to the relevant reporting payload, aligning with reporting API practices.

#### Use Cases
Improves debugging of hangs and long tasks by surfacing the offending call stack to developers and site operators, reducing time-to-fix for performance and correctness issues.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=1445539 (Tracking bug #1445539)  
- https://chromestatus.com/feature/5045134925406208 (ChromeStatus.com entry)  
- https://w3c.github.io/reporting/#crash-report (Spec)

### Document-Isolation-Policy

#### What's New
Document-Isolation-Policy allows a document to enable crossOriginIsolation for itself without deploying COOP/COEP across the page and irrespective of the page’s crossOriginIsolation status; it is backed by process isolation.

#### Technical Details
The policy changes how a document can opt into cross-origin isolation at document level; non-CORS cross-origin subresources will be handled according to the policy and process isolation semantics.

#### Use Cases
Enables localized use of crossOriginIsolation for pages or embedded documents that need isolated execution (e.g., for SharedArrayBuffer or other features), without site-wide COOP/COEP rollout.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=333029146 (Tracking bug #333029146)  
- https://chromestatus.com/feature/5048940296830976 (ChromeStatus.com entry)  
- https://wicg.github.io/document-isolation-policy/ (Spec)

### Ed25519 in web cryptography

#### What's New
Adds support for Curve25519 algorithms in the Web Cryptography API, specifically the Ed25519 signature algorithm.

#### Technical Details
Ed25519 is exposed via Web Crypto interfaces to enable modern signature primitives based on RFC 8032 (Ed25519). Implementation tracking and standardization references are provided.

#### Use Cases
Allows web apps to perform modern, fast, and compact digital signatures in-browser for authentication, signing messages, and interoperability with systems using Ed25519.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=1370697 (Tracking bug #1370697)  
- https://chromestatus.com/feature/5056122982457344 (ChromeStatus.com entry)  
- https://www.rfc-editor.org/rfc/rfc8032.html (Spec)

### HSTS tracking prevention

#### What's New
Mitigates tracking via the HSTS cache by allowing HSTS upgrades only for top-level navigations and blocking HSTS upgrades for subresource requests.

#### Technical Details
The change restricts HSTS-induced protocol upgrades (HTTP→HTTPS) to top-level navigations; subresource requests will not be upgraded via the HSTS cache, reducing the HSTS cache's utility for cross-site tracking.

#### Use Cases
Prevents third-party sites from using HSTS cache state as a tracking signal for identifying users across sites, protecting user privacy and making resource-loading behavior less fingerprintable.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40725781 (Tracking bug #40725781)  
- https://chromestatus.com/feature/5065878464307200 (ChromeStatus.com entry)

已保存到: digest_markdown/webplatform/Web API/chrome-137-stable-en.md