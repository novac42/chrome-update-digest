---
layout: default
title: chrome-140-en
---

## Area Summary

Chrome 140 (stable) introduces two focused updates in the PWA and service worker space: a spec-alignment fix so shared workers inherit controllers for blob-script URLs, and added timing telemetry for the ServiceWorker Static routing API. The SharedWorker fix changes runtime behavior to match the ServiceWorker spec and is gated by an enterprise policy. The timing additions expose routing-related marks in navigation/resource timing, improving observability for developers. Together these changes improve platform consistency and developer ability to measure and reason about service-worker-controlled navigation and routing.

## Detailed Updates

The below entries expand on the summary above and show practical implications for PWA and service-worker development.

### `SharedWorker` script inherits controller for blob script URL

#### What's New
Chrome now aligns with the ServiceWorker specification by allowing shared workers created from blob script URLs to inherit the controller, matching the behavior previously limited to dedicated workers.

#### Technical Details
The change fixes Chrome's prior divergence from the spec where only dedicated workers inherited a controller for blob URLs. An enterprise policy named SharedWorkerBlobURLFixEnabled is mentioned in the release notes to control this behavior rollout.

#### Use Cases
- Ensures consistent controller semantics across dedicated and shared workers for code paths that rely on controller presence (e.g., intercepting fetches or message flows).
- Reduces diffs between browser behavior and the spec, simplifying cross-browser PWA logic and debugging.

#### References
- https://issues.chromium.org/issues/324939068
- https://chromestatus.com/feature/5137897664806912
- https://w3c.github.io/ServiceWorker/#control-and-use-worker-client

### Add `ServiceWorkerStaticRouterTimingInfo`

#### What's New
Chrome adds timing information relevant to the ServiceWorker Static routing API and exposes it through the navigation timing API and resource timing API for developer use.

#### Technical Details
ServiceWorker provides marks to denote routing-related points in time; this feature surfaces two Static routing API–relevant timing values into the platform timing APIs to aid measurement and diagnostics.

#### Use Cases
- Enables precise measurement of routing decisions and their impact on navigation performance.
- Helps developers and performance engineers correlate service-worker routing activity with navigation/resource timing data for optimization and debugging.

#### References
- https://issues.chromium.org/issues/41496865
- https://chromestatus.com/feature/6309742380318720
- https://github.com/w3c/ServiceWorker

File: digest_markdown/webplatform/PWA and service worker/chrome-140-stable-en.md
