## Web APIs

### Create service worker client and inherit service worker controller for srcdoc iframe

Srcdoc context documents are currently not service worker clients and not covered by their parent's service worker. That results in some discrepancies (for example, Resource Timing reports the URLs that these document load, but service worker doesn't intercept them). This change aims to fix the discrepancies by creating service worker clients for srcdoc iframes and make them inherit parent's service worker controller.

[Tracking bug #41411856](https://issues.chromium.org/issues/41411856) | [ChromeStatus.com entry](https://chromestatus.com/feature/5128675425779712) | [Spec](https://github.com/w3c/ServiceWorker/issues/765)

### Element reflection

This feature allows for ARIA relationship attributes to be reflected in IDL as element references rather than DOMStrings.

This implements the IDL attributes in the [ARIAMixin](https://w3c.github.io/aria/#ARIAMixin) interface with a type of Element or `FrozenArray<Element>`, with the exception of `ariaOwnsElements`.

[Tracking bug #981423](https://issues.chromium.org/issues/981423) | [ChromeStatus.com entry](https://chromestatus.com/feature/6244885579431936) | [Spec](https://html.spec.whatwg.org/multipage/common-dom-interfaces.html#reflecting-content-attributes-in-idl-attributes:element)

### Fenced frames: Automatic beacon cross-origin data support

Fenced frames or URN iframes, if loaded through an API like Protected Audience or Shared Storage, can send out reporting beacons automatically if some event occurs (currently only top-level navigation beacons are supported). This feature was previously updated to allow cross-origin documents loaded in the root fenced frame's tree to send automatic beacons if opted in, but still kept the restriction that only frames that are same-origin to the origin loaded by the API could set the data that would be sent as part of the beacon. This feature expands that functionality to allow the cross-origin document to set the data that will be used in the automatic beacon.

To allow this while still preserving privacy, both the fenced frame root document and the cross-origin subframe document must explicitly opt in. This is the same opt in shape as other cross-origin FFAR features. Specifically, the root frame must opt in using the `Allow-Fenced-Frame-Automatic-Beacons` header, and the cross-origin subframe setting the data must opt in with the `crossOriginExposed` parameter in the call to `setReportEvent()`.

[ChromeStatus.com entry](https://chromestatus.com/feature/5121048142675968) | [Spec](https://github.com/WICG/fenced-frame/pull/203)

### `Float16Array`

Adds the `Float16Array` typed array. Number values are rounded to IEEE fp16 when writing into `Float16Array` instances.

[Tracking bug #42203953](https://issues.chromium.org/issues/42203953) | [ChromeStatus.com entry](https://chromestatus.com/feature/5164400693215232) | [Spec](https://tc39.es/proposal-float16array)

### HSTS tracking prevention

Mitigates user tracking by third-parties using the HSTS cache.

This feature only allows HSTS upgrades for top-level navigations and blocks HSTS upgrades for sub-resource requests. Doing so makes it infeasible for third-party sites to use the HSTS cache in order to track users across the web.

[Tracking bug #40725781](https://issues.chromium.org/issues/40725781) | [ChromeStatus.com entry](https://chromestatus.com/feature/5072685886078976)

### NavigateEvent sourceElement

When a navigation is initiated by an Element (for example, with a link click or a form submission), the `sourceElement` property on the `NavigateEvent` will be the initiating element.

[Tracking bug #40281924](https://issues.chromium.org/issues/40281924) | [ChromeStatus.com entry](https://chromestatus.com/feature/5134353390895104) | [Spec](https://html.spec.whatwg.org/multipage/nav-history-apis.html#dom-navigateevent-sourceelement)

### NotRestoredReasons API reason name change

The NotRestoredReasons API is changing some of the reason texts to align to the standardized names. If you are monitoring these reasons you may notice a change in reason texts.

[Tracking bug #331754704](https://issues.chromium.org/issues/331754704) | [ChromeStatus.com entry](https://chromestatus.com/feature/6444139556896768) | [Spec](https://github.com/whatwg/html/pull/10154)

### Observable API

Observables are a popular reactive-programming paradigm to handle an asynchronous stream of push-based events. They can be thought of as Promises but for multiple events, and aim to do what Promises did for callbacks and nesting. That is, they allow ergonomic event handling by providing an Observable object that represents the asynchronous flow of events.

You can subscribe to the object to receive events as they come in, and call any of its operators or combinators to declaratively describe the flow of transformations through which events go. This is in contrast with the imperative version, which often requires complicated nesting with things like `addEventListener()`.

[Tracking bug #1485981](https://issues.chromium.org/issues/1485981) | [ChromeStatus.com entry](https://chromestatus.com/feature/5154593776599040) | [Spec](https://wicg.github.io/observable)

### Remove clamping of `setInterval(...)` to >= 1ms

Prior to Chrome 135, `setInterval` with a value less than 1 is clamped to 1. From Chrome 135 this restriction is removed.

  * **Before** : `setInterval(..., 0)` = `1ms` delay.
  * **After** : `setInterval(..., 0)` = `0ms` delay.

**Note:** This has no effect on the 4ms clamping for nested calls to timeouts.

[Tracking bug #41380458](https://issues.chromium.org/issues/41380458) | [ChromeStatus.com entry](https://chromestatus.com/feature/5072451480059904)

### Service Worker client URL ignore `history.pushState()` changes

Modify the service worker `Client.url` property to ignore document URL changes with `history.pushState()` and other similar history APIs. The `Client.url` property is intended to be the creation URL of the HTML document which ignores such changes.

[Tracking bug #41337436](https://issues.chromium.org/issues/41337436) | [ChromeStatus.com entry](https://chromestatus.com/feature/4996996949344256) | [Spec](https://www.w3.org/TR/service-workers/#client-url)

### Support `rel` and `relList` attributes for `SVGAElement`

The SVGAElement interface in SVG 2.0 allows manipulation of `<a>` elements similar to HTML anchor elements. Supporting the `rel` and `relList` attributes enhances security and privacy for developers.

This alignment with HTML anchor elements ensures consistency and ease of use across web technologies.

[Tracking bug #40589293](https://issues.chromium.org/issues/40589293) | [ChromeStatus.com entry](https://chromestatus.com/feature/5066982694846464) | [Spec](https://svgwg.org/svg2-draft/linking.html#__svg__SVGAElement__rel)

### Timestamps for RTC Encoded Frames

This feature consists in exposing to the Web some timestamps that are present in WebRTC encoded frames transmitted using RTCPeerConnection. The timestamps in question are:

  * **Capture timestamp** : The timestamp when a frame was originally captured.
  * **Receive timestamp** : The timestamp when a frame was received.

[Tracking bug #391114797](https://issues.chromium.org/issues/391114797) | [ChromeStatus.com entry](https://chromestatus.com/feature/6294486420029440) | [Spec](https://w3c.github.io/webrtc-encoded-transform/#dom-rtcencodedaudioframemetadata-receivetime)

### Update HTTP request headers, body, and referrer policy on CORS redirect

Update the HTTP request on CORS redirect by removing the request-body-headers and body if the method has changed, and updating the referrer policy. These request updates align with the Fetch spec and match the behavior implemented by Firefox and Safari to improve compatibility.

[Tracking bug #40686262](https://issues.chromium.org/issues/40686262) | [ChromeStatus.com entry](https://chromestatus.com/feature/5129859522887680) | [Spec](https://fetch.spec.whatwg.org/#http-redirect-fetch)

### fetchLater API

`fetchLater()` is a JavaScript API to request a deferred fetch. Once called in a document, a deferred request is queued by the browser in the PENDING state, and will be invoked by the earliest of the following conditions:

  * The document is destroyed.
  * After a user-specified time. For privacy reason, all pending requests will be flushed upon document entering bfcache no matter how much time is left.
  * Browser decides it's time to send it.

The API returns a FetchLaterResult that contains a boolean field "activated" that may be updated to tell whether the deferred request has been sent out or not. On successful sending, the whole response will be ignored by browser, including body and headers. Nothing at all should be processed or updated, as the page may have already be gone.

Note that from the point of view of the API user, the exact send time is unknown.

[Tracking bug #1465781](https://issues.chromium.org/issues/1465781) | [ChromeStatus.com entry](https://chromestatus.com/feature/4654499737632768) | [Spec](https://whatpr.org/fetch/1647/07662d3...139351f.html)

### highlightsFromPoint API

The highlightsFromPoint API lets developers interact with custom highlights by detecting which highlights exist at a specific point within a document. This interactivity is valuable for complex web features where multiple highlights may overlap or exist within shadow DOM. By providing precise point-based highlight detection, the API empowers developers to manage dynamic interactions with custom highlights more effectively, such as responding to user clicks or hover events on highlighted regions to trigger custom tooltips, context menus, or other interactive features.

[Tracking bug #365046212](https://issues.chromium.org/issues/365046212) | [ChromeStatus.com entry](https://chromestatus.com/feature/4552801607483392) | [Spec](https://drafts.csswg.org/css-highlight-api-1/#interactions)
