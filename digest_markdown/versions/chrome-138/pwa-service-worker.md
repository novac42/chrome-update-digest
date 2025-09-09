---
layout: default
title: pwa-service-worker
---

## Service Worker

### ServiceWorker support for Speculation Rules Prefetch

This feature enables ServiceWorker-controlled prefetches, that is a speculation rules prefetch to URLs controlled by a Service Worker. Previously, the prefetch is cancelled upon detecting a controlling Service Worker, thus subsequent navigation to the prefetch target is served by the non-prefetch path. This feature will enable the prefetch request to go through the Service Worker's fetch handler and the response with the Service Worker interception is cached in the prefetch cache, resulting in a subsequent navigation being served by the prefetch cache. Use the enterprise policy `PrefetchWithServiceWorkerEnabled` to control this feature.

**References:** [Tracking bug #40947546](https://bugs.chromium.org/p/chromium/issues/detail?id=40947546) | [ChromeStatus.com entry](https://chromestatus.com/feature/5121066433150976) | [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-sw-integration)
