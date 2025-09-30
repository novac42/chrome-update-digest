## Area Summary

Chrome 140 for PWA and service worker focuses on spec alignment and improved observability. One change fixes SharedWorker behavior so blob-script shared workers inherit controllers per the ServiceWorker spec, closing a behavioral gap. The other exposes static routing timing points via navigation and resource timing APIs, improving developers' ability to measure service worker routing latency. Together these updates improve correctness and give developers better diagnostic data to optimize offline and routing performance.

## Detailed Updates

The items below expand on the summary and highlight developer-facing implications.

### `SharedWorker` script inherits controller for blob script URL

#### What's New
Shared workers created from blob script URLs now inherit the service worker controller as specified by the ServiceWorker spec, matching the behavior previously limited to dedicated workers.

#### Technical Details
Chrome's previous implementation limited controller inheritance to dedicated workers; this change aligns shared worker blob URL handling with the spec's control-and-use-worker-client rules. An enterprise policy `SharedWorkerBlobURLFixEnabled` is mentioned in the tracking notes for administrative control.

#### Use Cases
- PWAs that spawn shared workers from blob URLs will now see the same controlled-context semantics as dedicated workers, enabling consistent fetch interception and client-controlled behavior.
- Improves predictability for apps relying on service worker-controlled network behavior in multi-page or multi-context architectures.

#### References
- https://issues.chromium.org/issues/324939068
- https://chromestatus.com/feature/5137897664806912
- https://w3c.github.io/ServiceWorker/#control-and-use-worker-client

### Add `ServiceWorkerStaticRouterTimingInfo`

#### What's New
Adds timing marks for ServiceWorker static routing to the navigation timing and resource timing APIs, providing explicit timestamps for key routing events.

#### Technical Details
The change exposes two static routing API-relevant timing points through the standard timing APIs, allowing the browser to report when service worker static routing decisions occur relative to navigation and resource load lifecycles. This integrates service worker routing telemetry into existing web performance interfaces.

#### Use Cases
- Measure and profile the latency introduced by service worker static routing for navigations and resource loads.
- Correlate routing timings with rendering and network events to prioritize optimizations and detect regressions in PWA startup and resource fetch paths.
- Use timing data in performance monitoring and synthetic tests to validate routing improvements across releases.

#### References
- https://issues.chromium.org/issues/41496865
- https://chromestatus.com/feature/6309742380318720
- https://github.com/w3c/ServiceWorker

File saved to: digest_markdown/webplatform/PWA and service worker/chrome-140-stable-en.md