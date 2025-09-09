---
layout: default
title: webapi
---

## Web APIs

### Blob URL Partitioning: Fetching/Navigation

As a continuation of Storage Partitioning, Chrome has implemented partitioning of Blob URL access by Storage Key (top-level site, frame origin, and the has-cross-site-ancestor boolean), with the exception of top-level navigations which will remain partitioned only by frame origin. This behavior is similar to what's currently implemented by both Firefox and Safari, and aligns Blob URL usage with the partitioning scheme used by other storage APIs as part of Storage Partitioning. In addition, Chrome now enforces noopener on renderer-initiated top-level navigations to Blob URLs where the corresponding site is cross-site to the top-level site performing the navigation. This aligns Chrome with similar behavior in Safari, and the relevant specs have been updated to reflect these changes.

**Note:** This change can be temporarily reverted by setting the `PartitionedBlobURLUsage` policy. The policy will be deprecated when the other storage partitioning related enterprise policies are deprecated.

**References:** [Tracking bug #40057646](https://bugs.chromium.org/p/chromium/issues/detail?id=40057646) | [ChromeStatus.com entry](https://chromestatus.com/feature/5037311976488960)

### Call stacks in crash reports from unresponsive web pages

This feature captures the JavaScript call stack when a web page becomes unresponsive due to JavaScript code running an infinite loop or other very long computation. This helps developers to identify the cause of the unresponsiveness and fix it more easily. The JavaScript call stack is included in the crash reporting API when the reason is unresponsive.

**References:** [Tracking bug #1445539](https://bugs.chromium.org/p/chromium/issues/detail?id=1445539) | [ChromeStatus.com entry](https://chromestatus.com/feature/5045134925406208) | [Spec](https://w3c.github.io/reporting/#crash-report)

### Document-Isolation-Policy

Document-Isolation-Policy lets a document enable crossOriginIsolation for itself, without having to deploy COOP or COEP, and regardless of the crossOriginIsolation status of the page. The policy is backed by process isolation. Additionally, the document non-CORS cross-origin subresources will either be loaded without credentials or will need to have a CORP header.

**References:** [Tracking bug #333029146](https://bugs.chromium.org/p/chromium/issues/detail?id=333029146) | [ChromeStatus.com entry](https://chromestatus.com/feature/5048940296830976) | [Spec](https://wicg.github.io/document-isolation-policy/)

### Ed25519 in web cryptography

This feature adds support for Curve25519 algorithms in the Web Cryptography API, namely the signature algorithm Ed25519.

**References:** [Tracking bug #1370697](https://bugs.chromium.org/p/chromium/issues/detail?id=1370697) | [ChromeStatus.com entry](https://chromestatus.com/feature/5056122982457344) | [Spec](https://www.rfc-editor.org/rfc/rfc8032.html)

### HSTS tracking prevention

Mitigates user tracking by third-parties using the HSTS cache. This feature only allows HSTS upgrades for top-level navigations and blocks HSTS upgrades for sub-resource requests. Doing so makes it infeasible for third-party sites to use the HSTS cache in order to track users across the web.

**References:** [Tracking bug #40725781](https://bugs.chromium.org/p/chromium/issues/detail?id=40725781) | [ChromeStatus.com entry](https://chromestatus.com/feature/5065878464307200)
