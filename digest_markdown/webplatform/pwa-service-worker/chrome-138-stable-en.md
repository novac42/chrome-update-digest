### 1. Area Summary

Chrome 138 (stable) adds support for ServiceWorker-controlled prefetches driven by the Speculation Rules API. The most impactful change for developers is that speculation-rules prefetches can now be routed through a controlling Service Worker instead of being cancelled when a Service Worker is present. This aligns browser behavior with the nav-speculation integration spec and enables more consistent caching and offline handling for prefetched navigation targets. These updates matter because they reduce surprising differences between prefetch and normal navigation for PWAs and improve predictability of Service Worker control.

## Detailed Updates

Below are the details connecting the summary to the single listed change in this release.

### ServiceWorker support for Speculation Rules Prefetch

#### What's New
Enables ServiceWorker-controlled prefetches: speculation-rules prefetches to URLs that are controlled by a Service Worker are no longer cancelled upon detecting the controlling Service Worker.

#### Technical Details
Per the linked specification, prefetches initiated via the Speculation Rules API can integrate with Service Worker control so that fetches follow the same Service Worker handling model as normal navigations. See the spec and tracking bug for implementation notes and status.

#### Use Cases
- PWAs: Prefetched navigations can be served by a Service Worker, improving cache utilization and consistency between prefetch and subsequent navigation.
- Offline-first flows: Prefetches can prime the Service Worker cache for future navigations.
- Performance testing: Reduces variance between prefetched responses and responses served during normal navigation, simplifying performance tuning.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40947546
- https://chromestatus.com/feature/5121066433150976
- https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-sw-integration

File saved to:
```text
digest_markdown/webplatform/PWA and service worker/chrome-138-stable-en.md
```