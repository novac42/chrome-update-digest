---
layout: default
title: pwa-service-worker
---

## Service worker

### `SharedWorker` script inherits controller for blob script URL

The specification states that workers should inherit controllers for the blob URL. However, existing code allows only dedicated workers to inherit the controller; shared workers don't. This fixes Chrome's behavior to align with the specification. The `SharedWorkerBlobURLFixEnabled` enterprise policy controls this feature.

[Tracking bug #324939068](https://issues.chromium.org/issues/324939068) | [ChromeStatus.com entry](https://chromestatus.com/feature/5137897664806912) | [Spec](https://w3c.github.io/ServiceWorker/#control-and-use-worker-client)

### Add `ServiceWorkerStaticRouterTimingInfo`

This feature adds timing information for the ServiceWorker Static routing API, exposed in the navigation timing API and resource timing API for developer use. ServiceWorker provides timing information to mark certain points in time.

This feature adds two pieces of Static routing API-relevant timing information:

  * `RouterEvaluationStart`: Time to start matching a request with registered router rules.
  * `CacheLookupStart`: Time to start looking up the cache storage if the source is `"cache"`.

Additionally, this feature adds two pieces of router source information: the matched router source and the final router source.

[Tracking bug #41496865](https://issues.chromium.org/issues/41496865) | [ChromeStatus.com entry](https://chromestatus.com/feature/6309742380318720) | [Spec](https://github.com/w3c/ServiceWorker)
