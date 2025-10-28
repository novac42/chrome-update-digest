---
layout: default
title: Area Summary
---

# Area Summary

Chrome 138 introduces ServiceWorker support for speculation-rules prefetch, allowing prefetches to targets that are controlled by a Service Worker. The most impactful change for developers is that prefetches are no longer cancelled when a controlling Service Worker is detected, improving cache priming and navigation responsiveness for SW-controlled sites. This change advances the web platform by aligning navigation speculation with ServiceWorker control, enabling more reliable offline-first and performance optimizations. These updates matter because they reduce wasted work and improve the effectiveness of prefetch strategies for PWAs.

## Detailed Updates

The brief summary above frames the single change in this release; details and developer implications follow.

### ServiceWorker support for Speculation Rules Prefetch

#### What's New
Enables speculation-rules prefetches to URLs that are controlled by a Service Worker instead of cancelling those prefetches when a controlling Service Worker is detected.

#### Technical Details
ServiceWorker-controlled prefetches are now allowed by the integration between the Nav Speculation rules and ServiceWorker control. Previously, the browser cancelled a speculation prefetch if it detected a controlling ServiceWorker, preventing the prefetch from populating the ServiceWorker-controlled fetch path. With this change, the prefetch can proceed and be served/handled by the ServiceWorker as applicable.

#### Use Cases
- PWAs that use ServiceWorkers for offline caching can prime the SW cache via speculation rules before navigation, improving perceived load times.
- Sites using navigation speculation to prefetch likely navigations will see reduced wasted work and better cache hit rates when ServiceWorkers are present.
- Developers can rely on speculation-rules as part of an end-to-end performance strategy that includes SW routing and caching.

#### References
- [Tracking bug #40947546](https://bugs.chromium.org/p/chromium/issues/detail?id=40947546)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5121066433150976)
- [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-sw-integration)

# Area-Specific Expertise (PWA and service worker focus)

- css: Prefetch and SW interactions can improve initial render speed by ensuring critical CSS is served from SW cache.
- webapi: This change affects fetch flows and the fetch event lifecycle when speculation prefetches target SW-controlled scopes.
- graphics-webgpu: Reduced navigation latency can improve time-to-first-frame for GPU-heavy pages by earlier resource availability.
- javascript: ServiceWorker script lifecycle and fetch handlers should account for prefetch-originated requests and idempotent handling.
- security-privacy: Developers must ensure prefetch handling respects CORS, credentials, and privacy constraints consistent with SW fetch semantics.
- performance: Enables more effective cache priming strategies, reducing navigation stall and improving perceived performance.
- multimedia: Prefetching media assets via SW-controlled scopes can smooth playback startup for PWAs.
- devices: Faster navigations aid device API initialization when PWAs prefetch resources needed for hardware access.
- pwa-service-worker: Directly improves offline-first and background resource priming strategies by allowing SW to serve speculation prefetches.
- webassembly: WASM modules can be prefetched into SW cache to accelerate startup for heavy compute pages.
- deprecations: No deprecations in this change; evaluate existing prefetch strategies to leverage SW integration where applicable.
