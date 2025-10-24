---
layout: default
title: Area Summary
---

# Area Summary

Chrome 135 introduces a diverse set of Web API enhancements focused on interoperability, developer ergonomics, privacy, and performance. Key themes include improved service worker integration, expanded DOM and JavaScript capabilities, and new APIs for asynchronous programming and user interaction. Notable changes such as the addition of `Float16Array`, the Observable API, and updates to navigation and highlight detection empower developers to build more responsive and feature-rich applications. Privacy and security are also strengthened through HSTS tracking prevention and refined CORS redirect handling. Collectively, these updates advance the web platform by aligning with evolving standards, closing compatibility gaps, and enabling new use cases for modern web development.

## Detailed Updates

Below are the detailed updates for Chrome 135 Web API, highlighting technical details and practical benefits for developers.

### Create service worker client and inherit service worker controller for srcdoc iframe

#### What's New
Srcdoc iframes now act as service worker clients and inherit their parent's service worker controller, ensuring consistent interception of resource requests.

#### Technical Details
Previously, srcdoc documents were not covered by service workers, leading to discrepancies in resource handling. This update ensures that resource requests from srcdoc iframes are intercepted by the parent's service worker, aligning behavior with other iframe types.

#### Use Cases
- Enables consistent offline and caching strategies for dynamic iframes.
- Improves debugging and resource timing accuracy for embedded content.

#### References
- [Tracking bug #41411856](https://issues.chromium.org/issues/41411856)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5128675425779712)
- [Spec](https://github.com/w3c/ServiceWorker/issues/765)

---

### Element reflection

#### What's New
ARIA relationship attributes are now reflected as element references in IDL, rather than as DOMStrings.

#### Technical Details
Implements the ARIAMixin interface, exposing attributes as `Element` or `FrozenArray<Element>`, improving type safety and developer experience.

#### Use Cases
- Simplifies ARIA attribute manipulation in JavaScript.
- Enhances accessibility tooling and dynamic ARIA updates.

#### References
- [ARIAMixin](https://w3c.github.io/aria/#ARIAMixin)
- [Tracking bug #981423](https://issues.chromium.org/issues/981423)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6244885579431936)
- [Spec](https://html.spec.whatwg.org/multipage/common-dom-interfaces.html#reflecting-content-attributes-in-idl-attributes:element)

---

### Fenced frames: Automatic beacon cross-origin data support

#### What's New
Fenced frames loaded via certain APIs can now automatically send reporting beacons with cross-origin data.

#### Technical Details
Supports automatic beacon reporting for cross-origin documents in fenced frames, expanding beyond top-level navigation beacons.

#### Use Cases
- Enables privacy-preserving ad measurement and reporting.
- Supports advanced analytics in privacy-centric environments.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5121048142675968)
- [Spec](https://github.com/WICG/fenced-frame/pull/203)

---

### `Float16Array`

#### What's New
Introduces the `Float16Array` typed array, supporting 16-bit floating point numbers.

#### Technical Details
Values are rounded to IEEE fp16 when written. This addition aligns with the latest ECMAScript proposals and improves compatibility with graphics and ML workloads.

#### Use Cases
- Efficient storage and computation for graphics, ML, and scientific data.
- Reduces memory usage for large numeric datasets.

#### References
- [Tracking bug #42203953](https://issues.chromium.org/issues/42203953)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5164400693215232)
- [Spec](https://tc39.es/proposal-float16array)

---

### HSTS tracking prevention

#### What's New
Prevents third-party tracking via the HSTS cache by restricting HSTS upgrades to top-level navigations only.

#### Technical Details
Blocks HSTS upgrades for sub-resource requests, mitigating cross-site tracking vectors.

#### Use Cases
- Enhances user privacy by reducing fingerprinting and tracking risks.
- Aligns with modern web security best practices.

#### References
- [Tracking bug #40725781](https://issues.chromium.org/issues/40725781)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5072685886078976)

---

### NavigateEvent sourceElement

#### What's New
Adds a `sourceElement` property to `NavigateEvent`, exposing the element that initiated navigation.

#### Technical Details
When navigation is triggered by an element (e.g., link or form), `sourceElement` references the initiating DOM element.

#### Use Cases
- Enables advanced navigation analytics and custom routing logic.
- Facilitates debugging and event tracing in SPAs.

#### References
- [Tracking bug #40281924](https://issues.chromium.org/issues/40281924)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5134353390895104)
- [Spec](https://html.spec.whatwg.org/multipage/nav-history-apis.html#dom-navigateevent-sourceelement)

---

### NotRestoredReasons API reason name change

#### What's New
Standardizes reason texts in the NotRestoredReasons API to match the latest specification.

#### Technical Details
Updates reason names for why pages are not restored from the back/forward cache, improving consistency with the HTML spec.

#### Use Cases
- Simplifies monitoring and debugging of navigation and caching issues.
- Ensures compatibility with cross-browser diagnostics.

#### References
- [Tracking bug #331754704](https://issues.chromium.org/issues/331754704)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6444139556896768)
- [Spec](https://github.com/whatwg/html/pull/10154)

---

### Observable API

#### What's New
Introduces the Observable API for handling asynchronous streams of events.

#### Technical Details
Provides a native Observable interface, enabling ergonomic handling of multiple asynchronous events, similar to Promises but for streams.

#### Use Cases
- Reactive programming patterns in web apps.
- Simplifies event-driven architectures and data streams.

#### References
- [Tracking bug #1485981](https://issues.chromium.org/issues/1485981)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5154593776599040)
- [Spec](https://wicg.github.io/observable)

---

### Remove clamping of `setInterval(...)` to >= 1ms

#### What's New
Removes the minimum 1ms delay clamp for `setInterval`, allowing zero-delay intervals.

#### Technical Details
`setInterval(..., 0)` now results in a 0ms delay, except for nested calls which still clamp to 4ms.

#### Use Cases
- Enables finer-grained timing for high-performance applications.
- Useful for animation loops and real-time updates.

#### References
- [Tracking bug #41380458](https://issues.chromium.org/issues/41380458)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5072451480059904)

---

### Service Worker client URL ignore `history.pushState()` changes

#### What's New
The `Client.url` property for service workers now ignores URL changes made via `history.pushState()`.

#### Technical Details
`Client.url` reflects the creation URL of the document, not subsequent history API changes, aligning with the service worker specification.

#### Use Cases
- Ensures consistent service worker behavior for SPAs.
- Prevents confusion in client identification and caching logic.

#### References
- [Tracking bug #41337436](https://issues.chromium.org/issues/41337436)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4996996949344256)
- [Spec](https://www.w3.org/TR/service-workers/#client-url)

---

### Support `rel` and `relList` attributes for `SVGAElement`

#### What's New
Adds `rel` and `relList` attributes to SVG `<a>` elements, mirroring HTML anchor behavior.

#### Technical Details
Implements SVG 2.0 features for link relationships, enhancing security and privacy controls.

#### Use Cases
- Consistent link management across HTML and SVG.
- Enables advanced SVG navigation and security policies.

#### References
- [Tracking bug #40589293](https://issues.chromium.org/issues/40589293)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5066982694846464)
- [Spec](https://svgwg.org/svg2-draft/linking.html#__svg__SVGAElement__rel)

---

### Timestamps for RTC Encoded Frames

#### What's New
Exposes capture and receive timestamps for WebRTC encoded frames.

#### Technical Details
Provides metadata for frames transmitted via RTCPeerConnection, including when frames were captured and received.

#### Use Cases
- Enables precise media synchronization and diagnostics.
- Supports advanced analytics for real-time communications.

#### References
- [Tracking bug #391114797](https://issues.chromium.org/issues/391114797)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6294486420029440)
- [Spec](https://w3c.github.io/webrtc-encoded-transform/#dom-rtcencodedaudioframemetadata-receivetime)

---

### Update HTTP request headers, body, and referrer policy on CORS redirect

#### What's New
Aligns CORS redirect behavior with the Fetch spec by updating headers, body, and referrer policy as needed.

#### Technical Details
Removes request-body-headers and body if the HTTP method changes on redirect, and updates the referrer policy for compatibility with other browsers.

#### Use Cases
- Improves cross-browser compatibility for CORS requests.
- Reduces subtle bugs in complex fetch scenarios.

#### References
- [Tracking bug #40686262](https://issues.chromium.org/issues/40686262)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5129859522887680)
- [Spec](https://fetch.spec.whatwg.org/#http-redirect-fetch)

---

### fetchLater API

#### What's New
Introduces `fetchLater()`, allowing developers to schedule deferred fetch requests.

#### Technical Details
Deferred requests are queued and executed when the document is destroyed or after a specified time, with privacy considerations.

#### Use Cases
- Enables background data prefetching and deferred analytics.
- Improves performance and privacy for resource loading.

#### References
- [Tracking bug #1465781](https://issues.chromium.org/issues/1465781)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4654499737632768)
- [Spec](https://whatpr.org/fetch/1647/07662d3...139351f.html)

---

### highlightsFromPoint API

#### What's New
Adds the `highlightsFromPoint` API to detect custom highlights at a specific document point.

#### Technical Details
Enables querying of highlight overlays, including those in shadow DOM, for precise user interaction.

#### Use Cases
- Supports advanced text selection, annotation, and accessibility features.
- Useful for editors, readers, and collaborative tools.

#### References
- [Tracking bug #365046212](https://issues.chromium.org/issues/365046212)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4552801607483392)
- [Spec](https://drafts.csswg.org/css-highlight-api-1/#interactions)
