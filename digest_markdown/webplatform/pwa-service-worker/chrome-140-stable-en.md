# Chrome 140 Stable - PWA and Service Worker Updates

## Summary

Chrome 140 introduces significant improvements to service worker functionality, focusing on enhanced specification compliance and better developer debugging capabilities. The most notable changes include fixing SharedWorker controller inheritance for blob URLs to align with web standards, and adding comprehensive timing information for the ServiceWorker Static routing API to improve performance monitoring and debugging.

## Feature Details

### `SharedWorker` script inherits controller for blob script URL

**What Changed**:
This update fixes a long-standing discrepancy between Chrome's implementation and the web specification regarding service worker controllers. Previously, while dedicated workers could inherit controllers for blob URLs as specified, shared workers were unable to do so. Chrome 140 corrects this behavior to ensure that SharedWorker scripts now properly inherit controllers when using blob script URLs, bringing Chrome into full compliance with the ServiceWorker specification. This change is controlled by the `SharedWorkerBlobURLFixEnabled` enterprise policy for gradual rollout and potential rollback if needed.

**References**:
- [Tracking bug #324939068](https://issues.chromium.org/issues/324939068)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5137897664806912)
- [Spec](https://w3c.github.io/ServiceWorker/#control-and-use-worker-client)

### Add `ServiceWorkerStaticRouterTimingInfo`

**What Changed**:
Chrome 140 introduces comprehensive timing information for the ServiceWorker Static routing API, exposing detailed performance metrics through both the navigation timing API and resource timing API. This enhancement provides developers with crucial insights into service worker performance by adding two key pieces of Static routing API-relevant timing data. These metrics help developers understand the performance characteristics of their service worker routing decisions, enabling better optimization of offline-first applications and PWAs. The timing information marks specific points in the service worker lifecycle related to static routing, giving developers the data they need to identify bottlenecks and improve user experience.

**References**:
- [Tracking bug #41496865](https://issues.chromium.org/issues/41496865)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6309742380318720)
- [Spec](https://github.com/w3c/ServiceWorker)