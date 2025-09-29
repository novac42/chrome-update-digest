# Chrome Update Analyzer - PWA and Service Worker (Chrome 140)

## Area Summary

Chrome 140 brings targeted improvements to service worker functionality that enhance both specification compliance and developer observability. The release focuses on fixing long-standing behavioral inconsistencies between shared and dedicated workers while adding crucial timing instrumentation for the ServiceWorker Static routing API. These updates strengthen the foundation for Progressive Web Apps by ensuring more predictable service worker behavior and providing developers with better performance monitoring capabilities for routing decisions.

## Detailed Updates

Building on the core service worker improvements, Chrome 140 introduces both compliance fixes and new developer tools that will enhance PWA development workflows.

### `SharedWorker` script inherits controller for blob script URL

#### What's New
Chrome now properly implements the specification requirement for shared workers to inherit service worker controllers when using blob URLs, bringing behavior in line with dedicated workers.

#### Technical Details
Previously, Chrome allowed only dedicated workers to inherit the service worker controller for blob URLs, while shared workers did not inherit this controller despite the specification requiring it. This fix ensures consistent behavior across worker types. The `SharedWorkerBlobURLFixEnabled` enterprise policy provides control over this change for enterprise environments that may need to manage the transition.

#### Use Cases
This fix ensures more predictable PWA behavior when using shared workers with blob scripts, particularly important for applications that rely on service worker interception for caching or routing. Developers can now expect consistent service worker control regardless of whether they use dedicated or shared workers with blob URLs.

#### References
- [Tracking bug #324939068](https://issues.chromium.org/issues/324939068)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5137897664806912)
- [Spec](https://w3c.github.io/ServiceWorker/#control-and-use-worker-client)

### Add `ServiceWorkerStaticRouterTimingInfo`

#### What's New
Chrome now exposes timing information for the ServiceWorker Static routing API through the Navigation Timing API and Resource Timing API, giving developers visibility into routing performance.

#### Technical Details
This feature adds two key timing measurements for the Static routing API: timing marks for when routing decisions are made and performance metrics that help developers understand the impact of static routing on their application's performance. The timing information integrates with existing web performance APIs, making it accessible through standard performance measurement tools.

#### Use Cases
Developers can now monitor and optimize their ServiceWorker static routing configurations by analyzing timing data. This is particularly valuable for PWAs with complex routing logic, allowing teams to identify performance bottlenecks in their service worker routing decisions and optimize accordingly. The timing data helps quantify the performance benefits of static routing compared to traditional service worker interception.

#### References
- [Tracking bug #41496865](https://issues.chromium.org/issues/41496865)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6309742380318720)
- [Spec](https://github.com/w3c/ServiceWorker)