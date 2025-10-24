---
layout: default
title: Area Summary
---

# Area Summary

Chrome 137 (stable) continues the Storage Partitioning effort by introducing partitioning of Blob URL access based on Storage Key. The update isolates Blob URL access using the Storage Key components (top-level site, frame origin, and the has-cross-site-ancestor boolean), with a specific exception for top-level navigations which remain partitioned only by frame origin. This change alters how Blob URLs are resolved and accessed across frames and sites, affecting cross-site resource isolation and developer assumptions about Blob URL visibility. Developers should be aware of potential behavioral differences for fetch/navigation scenarios involving Blob URLs.

## Detailed Updates

The following item explains the Blob URL partitioning change and its implications for navigation and loading.

### Blob URL Partitioning: Fetching/Navigation

#### What's New
Partitioning of Blob URL access by Storage Key (top-level site, frame origin, and the has-cross-site-ancestor boolean) has been implemented, continuing the Storage Partitioning work. Top-level navigations are an exception and remain partitioned only by frame origin.

#### Technical Details
- Blob URL access is now scoped by Storage Key components: top-level site, frame origin, and has-cross-site-ancestor boolean.
- For top-level navigations, partitioning is limited to frame origin only.
- This behavior is presented as a continuation of the broader Storage Partitioning project.

#### Use Cases
- Improves isolation of Blob URL access across different top-level sites and cross-site frames.
- May change runtime visibility and access patterns for Blob URLs used in fetching or navigation contexts.
- Developers should review cross-origin Blob URL usage and tests that assume global Blob URL accessibility.

#### References
- Tracking bug #40057646: https://bugs.chromium.org/p/chromium/issues/detail?id=40057646
- ChromeStatus.com entry: https://chromestatus.com/feature/5037311976488960

Output file: digest_markdown/webplatform/Navigation-Loading/chrome-137-stable-en.md
