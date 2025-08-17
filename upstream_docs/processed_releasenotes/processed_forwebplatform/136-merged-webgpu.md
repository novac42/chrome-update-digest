# Chrome 136 Release Notes

**Stable release date:** April 29th, 2025

Unless otherwise noted, the following changes apply to Chrome 136 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. Want just the highlights? Check out [New in Chrome 136](https://developer.chrome.com/blog/new-in-chrome-136).

## HTML and DOM

### Language support for CanvasTextDrawingStyles

The `<canvas>` DOM element, like all DOM elements, accepts a `lang` attribute that is used to define language specific treatment for font selection (when fonts have locale specific glyphs). Browsers respect this attribute. However, when an `OffscreenCanvas` is created there is no way to set locale information, possibly resulting in a state where an offscreen canvas produces rendered results that differ from the canvas in which its output is used. This feature adds a `lang` IDL attribute to `CanvasTextDrawingStyles` to give developers direct control over the language for the text drawing and metrics.

**References:** [Tracking bug #385006131](https://bugs.chromium.org/p/chromium/issues/detail?id=385006131) | [ChromeStatus.com entry](https://chromestatus.com/feature/5101829618114560) | [Spec](https://html.spec.whatwg.org/multipage/canvas.html#canvastextdrawingstyles)

## CSS and UI

### The dynamic-range-limit property

Enables a page to limit the maximum brightness of HDR content.

**References:** [Tracking bug #1470298](https://bugs.chromium.org/p/chromium/issues/detail?id=1470298) | [ChromeStatus.com entry](https://chromestatus.com/feature/5023877486493696) | [Spec](https://www.w3.org/TR/css-color-hdr/#dynamic-range-limit)

### Partition :visited links history

To eliminate user browsing history leaks, anchor elements are styled as `:visited` only if they have been clicked from this top-level site and frame origin before. There is an exception for "self-links", where links to a site's own pages can be styled as `:visited` even if they have not been clicked on in this exact top-level site and frame origin before. This exemption is only enabled in top-level frames or subframes which are same-origin with the top-level frame. The privacy benefits are still achieved because sites already know which of its subpages a user has visited, so no new information is exposed. This was a community-requested exception which improves user experience.

**References:** [Tracking bug #1448609](https://bugs.chromium.org/p/chromium/issues/detail?id=1448609) | [ChromeStatus.com entry](https://chromestatus.com/feature/5029851625472000) | [Spec](https://www.w3.org/TR/css-pseudo-4/#visited-pseudo)

### Unprefixed print-color-adjust

The `print-color-adjust` property lets you adjust colors in printed web pages. This is the same as Chrome's already-supported `-webkit-print-color-adjust`, but with a standardized name. The `-webkit-` prefixed version is not removed.

**References:** [MDN Docs](https://developer.mozilla.org/docs/Web/CSS/print-color-adjust) | [Tracking bug #376381169](https://bugs.chromium.org/p/chromium/issues/detail?id=376381169) | [ChromeStatus.com entry](https://chromestatus.com/feature/5090690412953600) | [Spec](https://www.w3.org/TR/css-color-adjust-1/#print-color-adjust)

### Rename string attr() type to raw-string

The CSS Working Group has resolved to replace `string` `attr()` type with `raw-string`. Therefore from Chrome 136 `attr(data-foo string)` becomes `attr(data-foo raw-string)`.

**References:** [Tracking bug #400981738](https://bugs.chromium.org/p/chromium/issues/detail?id=400981738) | [ChromeStatus.com entry](https://chromestatus.com/feature/5110654344216576) | [Spec](https://www.w3.org/TR/css-values-5/#attr-notation)

### Type-agnostic var() fallback

The fallback part of a `var()` function does not validate against the type of the custom property being referenced.

**References:** [Tracking bug #372475301](https://bugs.chromium.org/p/chromium/issues/detail?id=372475301) | [ChromeStatus.com entry](https://chromestatus.com/feature/5049845796618240)

## Web APIs

### Dispatch click events to captured pointer

If a pointer is captured while the `pointerup` event is being dispatched, the click event is now dispatched to the captured target instead of the nearest common ancestor of `pointerdown` and `pointerup` events as per the UI Event spec. For uncaptured pointers, the click target remains unchanged.

**References:** [Tracking bug #40851596](https://bugs.chromium.org/p/chromium/issues/detail?id=40851596) | [ChromeStatus.com entry](https://chromestatus.com/feature/5045063816396800) | [Spec](https://w3c.github.io/uievents/#event-type-click)

### Explicit compile hints with magic comments

Allows attaching of information about which functions should be eager parsed and compiled in JavaScript files. The information is encoded as magic comments.

**References:** [Tracking bug #13917](https://bugs.chromium.org/p/chromium/issues/detail?id=13917) | [ChromeStatus.com entry](https://chromestatus.com/feature/5047772830048256) | [Spec](https://github.com/v8/v8/wiki/Design-Elements#compile-hints)

### Incorporate navigation initiator into the HTTP cache partition key

Chrome's HTTP cache keying scheme is updated to include an `is-cross-site-main-frame-navigation` boolean to mitigate cross-site leak attacks involving top-level navigation. Specifically, this will prevent cross-site attacks in which an attacker can initiate a top-level navigation to a given page and then navigate to a resource known to be loaded by the page in order to infer sensitive information using load timing. This change also improves privacy by preventing a malicious site from using navigations to infer whether a user has visited a given site previously.

**References:** [Tracking bug #398784714](https://bugs.chromium.org/p/chromium/issues/detail?id=398784714) | [ChromeStatus.com entry](https://chromestatus.com/feature/5108419906535424) | [Spec](https://httpwg.org/specs/rfc9110.html#caching)

### Protected audience: text conversion helpers

Protected Audience bidding and scoring scripts that interface with WebAssembly need to efficiently convert string-typed data to (and from) byte arrays (for example, to pass strings into and out of WebAssembly with the "memory" ArrayBuffer). This provides two standalone functions, `protectedAudience.encodeUtf8`, and `protectedAudience.decodeUtf8` to perform these tasks about an order of magnitude more efficiently than doing it in JavaScript.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5099738574602240)

### RegExp.escape

`RegExp.escape` is a static method that takes a string and returns an escaped version that may be used as a pattern inside a regular expression.

**Example:**

```javascript
const str = prompt("Please enter a string");
const escaped = RegExp.escape(str);
const re = new RegExp(escaped, 'g');
// handles reg exp special tokens with the replacement.
console.log(ourLongText.replace(re));
```

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5074350768316416) | [Spec](https://tc39.es/proposal-regex-escaping/)

### Speculation rules: tag field

This enables developers to add `tag` field to speculation rules. This optional field can be used to track the source of speculation rules. For example, to treat them differently at an intermediary server. Any tags associated with a speculation will be sent with the `Sec-Speculation-Tags` header.

**References:** [Tracking bug #381687257](https://bugs.chromium.org/p/chromium/issues/detail?id=381687257) | [ChromeStatus.com entry](https://chromestatus.com/feature/5100969695576064) | [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-tag)

### Update ProgressEvent to use double type for loaded and total

The `ProgressEvent` has attributes `loaded` and `total` indicating the progress, and their type is `unsigned long long` now. With this feature, the type for these two attributes is changed to `double` instead, which gives the developer more control over the value. For example, the developers can now create a `ProgressEvent` with the total of 1 and the loaded increasing from 0 to 1 gradually. This is aligned with the default behavior of the `<progress>` HTML element if the max attribute is omitted.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5084700244254720) | [Spec](https://xhr.spec.whatwg.org/#interface-progressevent)

## Privacy and security

### Permissions Policy reports for iframes

Introduces a new violation type called "Potential Permissions Policy violation", which will only look at Permissions Policy (including report-only policy) and the allow attribute set in iframes to detect the conflict between Permissions Policy enforced versus permissions propagated to iframes.

**References:** [Tracking bug #40941424](https://bugs.chromium.org/p/chromium/issues/detail?id=40941424) | [ChromeStatus.com entry](https://chromestatus.com/feature/5061997434142720) | [Spec](https://w3c.github.io/webappsec-permissions-policy/#reporting)

### Reduce fingerprinting in Accept-Language header information

Reduces the amount of information the Accept-Language header value string exposes in HTTP requests and in `navigator.languages`. Instead of sending a full list of the user's preferred languages on every HTTP request, Chrome now sends the user's most preferred language in the Accept-Language header.

**References:** [Tracking bug #1306905](https://bugs.chromium.org/p/chromium/issues/detail?id=1306905) | [ChromeStatus.com entry](https://chromestatus.com/feature/5042348942655488)

## Identity

### FedCM updates

Allows FedCM to show multiple identity providers in the same dialog, by having all providers in the same `get()` call. This provides developers with a convenient way to present all supported identity providers to users. Chrome 136 also removes support for add another account in FedCM passive mode. This feature allows showing a use another account button alongside other IdP accounts in the chooser. The feature is currently unused, and UX conversations have led us to believe that supporting this leads to a more complicated flow without much benefit. This feature will still work in FedCM active mode.

**References:** [Tracking bug #1348262](https://bugs.chromium.org/p/chromium/issues/detail?id=1348262) | [ChromeStatus.com entry](https://chromestatus.com/feature/5049732142194688) | [Spec](https://fedidcg.github.io/FedCM/)

### Web authentication conditional create (passkey upgrades)

WebAuthn conditional create requests let websites upgrade existing password credentials to a passkey.

**References:** [Tracking bug #377758786](https://bugs.chromium.org/p/chromium/issues/detail?id=377758786) | [ChromeStatus.com entry](https://chromestatus.com/feature/5097871013068800) | [Spec](https://w3c.github.io/webauthn/#enum-credentialmediationrequirement)

## Images and media

### AudioContext Interrupted State

Adds an "interrupted" state to `AudioContextState`. This new state lets the User Agent pause playback during exclusive audio access (VoIP) or when a laptop lid is closed.

**References:** [Tracking bug #374805121](https://bugs.chromium.org/p/chromium/issues/detail?id=374805121) | [ChromeStatus.com entry](https://chromestatus.com/feature/5087843301908480) | [Spec](https://webaudio.github.io/web-audio-api/#AudioContextState)

### Captured surface control

A Web API that lets web applications:
- Forward wheel events to a captured tab.
- Read and change the zoom level of a captured tab.

**References:** [Tracking bug #1466247](https://bugs.chromium.org/p/chromium/issues/detail?id=1466247) | [ChromeStatus.com entry](https://chromestatus.com/feature/5064816815276032) | [Spec](https://wicg.github.io/captured-surface-control/)

### CapturedSurfaceResolution

Expose pixel ratio of the captured surface while screensharing. This feature helps applications to conserve their system resources or adapt the quality over bandwidth trade-off according to the physical and logical resolutions of the captured surface.

**References:** [Tracking bug #383946052](https://bugs.chromium.org/p/chromium/issues/detail?id=383946052) | [ChromeStatus.com entry](https://chromestatus.com/feature/5100866324422656) | [Spec](https://w3c.github.io/mediacapture-screen-share-extensions/#capturedsurfaceresolution)

### H265 (HEVC) codec support in WebRTC

After this change, HEVC will join VP8, H.264, VP9, and AV1 as supported codecs in WebRTC. Support will be queryable using the MediaCapabilities API.

**References:** [Tracking bug #391903235](https://bugs.chromium.org/p/chromium/issues/detail?id=391903235) | [ChromeStatus.com entry](https://chromestatus.com/feature/5104835309936640) | [Spec](https://www.w3.org/TR/webrtc/#dom-rtcrtpcodeccapability)

### H26x Codec support updates for MediaRecorder

Chromium's MediaRecorder API now supports HEVC encoding, introducing the `hvc1.*` codec string, and adds new codecs (`hev1.*` and `avc3.*`) supporting variable resolution video in MP4. Support for HEVC platform encoding was added in WebCodecs in Chromium M130. As a follow-up, support has been added to the MediaRecorder API in Chromium. The API now supports both MP4 and Matroska muxer types with different HEVC and H.264 mime type specifications. HEVC encoding is only supported if the user's device and operating system provide the necessary capabilities.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5103892473503744)

### Use DOMPointInit for getCharNumAtPosition, isPointInFill, isPointInStroke

This change brings Chromium code in line with the latest W3C specification for `SVGGeometryElement` and `SVGPathElement` in terms of use of `DOMPointInit` over `SVGPoint` for `getCharNumAtPosition`, `isPointInFill`, `isPointInStroke`.

**References:** [Tracking bug #40572887](https://bugs.chromium.org/p/chromium/issues/detail?id=40572887) | [ChromeStatus.com entry](https://chromestatus.com/feature/5084627093929984) | [Spec](https://www.w3.org/TR/SVG2/types.html#InterfaceDOMPointInit)

## WebGPU

### GPUAdapterInfo isFallbackAdapter attribute

The `GPUAdapterInfo` `isFallbackAdapter` boolean attribute indicates if an adapter has significant performance limitations in return for wider compatibility, more predictable behavior, or improved privacy. Note that a fallback adapter may not be present on all systems.

**References:** [Tracking bug #403172841](https://bugs.chromium.org/p/chromium/issues/detail?id=403172841) | [ChromeStatus.com entry](https://chromestatus.com/feature/5113344043884544) | [Spec](https://gpuweb.github.io/gpuweb/#gpuadapterinfo)

## Browser changes

### Fluent scrollbars

This feature modernizes the Chromium scrollbars (both overlay and non-overlay) on Windows and Linux to fit the Windows 11 Fluent design language. Non-overlay Fluent scrollbars will be enabled by default in Linux and Windows. This change applies to Linux as well because Chromium's Linux scrollbar design has historically been aligned with what ships on Windows. How to expose enabling overlay Fluent scrollbars is still being decided.

**References:** [Tracking bug #1292117](https://bugs.chromium.org/p/chromium/issues/detail?id=1292117) | [ChromeStatus.com entry](https://chromestatus.com/feature/5023688844812288)

## WebGPU

### GPUAdapterInfo isFallbackAdapter attribute

The GPUAdapterInfo `isFallbackAdapter` boolean attribute indicates whether a GPUAdapter has significant performance limitations in exchange for wider compatibility, more predictable behavior, or improved privacy. This addition was necessary because libraries that take user-provided GPUDevice objects couldn't access this information through the `adapterInfo` attribute on GPUDevice. See the following example and [issue 403172841](https://issues.chromium.org/issues/403172841).
    
    
    const adapter = await navigator.gpu.requestAdapter();
    
    if (adapter?.info.isFallbackAdapter) {
      // The returned adapter is a software-backed fallback adapter, which
      // may have significantly lower performance and fewer features.
    }
    

Since Chrome has not yet shipped support for fallback adapters, `isFallbackAdapter` is at the moment always false on users' devices. We're investigating whether the GPUAdapter `isFallbackAdapter` attribute can be deprecated and removed. See [intent to ship](https://groups.google.com/a/chromium.org/g/blink-dev/c/VUkzIOWd2n0).

### Shader compilation time improvements on D3D12

The Chrome team keeps improving Tint, the WebGPU shader language compiler, by adding an intermediate representation (IR) for devices that support WebGPU with the D3D12 backend. This IR, positioned between Tint's abstract syntax tree (AST) and the HLSL backend writer, will make the compiler more efficient and maintainable, ultimately benefiting both developers and users. Initial tests show that the new version of Tint is up to 10 times faster when translating Unity's WGSL shaders to HLSL.

![A flowchart shows the process of converting WGSL shader code into low-level GPU instructions.](/static/blog/new-in-webgpu-136/image/render-pipeline-creation-in-windows.jpg) Render pipeline creation in Windows.

These improvements—already accessible on Android, ChromeOS, and macOS—are being progressively expanded to Windows devices that support WebGPU with the D3D12 backend. See [issue 42251045](https://issues.chromium.org/issues/42251045).

### Save and copy canvas images

Chrome users can now right-click on a WebGPU canvas and access context menu options **Save Image As…** or **Copy Image**. See [issue 40902474](https://issues.chromium.org/issues/40902474).

![The ](/static/blog/new-in-webgpu-136/image/save-image-as.jpg) User selected "Save Image As…" context menu.

### Lift compatibility mode restrictions

The experimental `"core-features-and-limits"` feature when available on a GPUDevice, lifts all compatibility mode restrictions (features and limits) when the `chrome://flags/#enable-unsafe-webgpu` flag is enabled. See [issue 395855517](https://issues.chromium.org/issues/395855517).

Requesting a GPUAdapter with the `featureLevel: "compatibility"` option hints the browser to select the experimental [WebGPU compatibility mode](https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md). If successful, the resulting adapter is "compatibility-defaulting". Otherwise, it is "core-defaulting", which is the same as using the `featureLevel: "core"` option. Moreover, calling `requestDevice()` without `requiredFeatures` and `requiredLimits` request a GPUDevice with the GPUAdapter's default capabilities.

Core-defaulting adapters always support the `"core-features-and-limits"` feature and it is automatically enabled on GPUDevices created from them. For compatibility-defaulting adapters, the `"core-features-and-limits"` feature may be supported and can be requested on GPUDevices created from them. Both types of adapters may also support features like `"float32-blendable"`, which is optional in both core and compatibility modes.

The following example is for an application that requires `"float32-blendable"` and supports using core features if available, but uses only compatibility features if core features are not available.
    
    
    const adapter = await navigator.gpu.requestAdapter({ featureLevel: "compatibility" });
    
    if (!adapter || !adapter.features.has("float32-blendable")) {
      throw new Error("32-bit float textures blending support is not available");
    }
    
    const requiredFeatures = [];
    if (adapter.features.has("core-features-and-limits")) {
      requiredFeatures.push("core-features-and-limits");
    }
    
    const device = await adapter.requestDevice({ requiredFeatures });
    
    if (!device.features.has("core-features-and-limits")) {
      // Compatibility mode restrictions validation rules will apply.
    }
    

The experimental GPUAdapter `featureLevel`and `isCompatibilityMode` attributes have been removed in favor of the `"core-features-and-limits"` feature. See [issue 395855516](https://issues.chromium.org/issues/395855516).

### Dawn updates

The [callback status](https://webgpu-native.github.io/webgpu-headers/Asynchronous-Operations.html#CallbackStatuses) enum `InstanceDropped` has been renamed to `CallbackCancelled` to clarify that the callback was cancelled, but background processing associated with the event, such as pipeline compilation, might still be running. The new name is more generally-applicable, in case another cancellation mechanism is added later. See [issue 520](https://github.com/webgpu-native/webgpu-headers/issues/520).

The `wgpu::PopErrorScopeStatus::EmptyStack` enum that indicates that the error scope stack couldn't be popped has been renamed to `wgpu::PopErrorScopeStatus::Error` (which is also more generally-applicable). The callback now also includes a corresponding error explanation message to help debugging. See [issue 369](https://github.com/webgpu-native/webgpu-headers/issues/369).

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7049..chromium/7103?n=1000).

## Origin trials

### Audio Output Devices API: setDefaultSinkId()

This feature adds `setDefaultSinkId()` to `MediaDevices`, which enables the top-level frame to change the default audio output device used by its subframes.

**References:** [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [ChromeStatus.com entry](https://chromestatus.com/feature/5066644096548864) | [Spec](https://webaudio.github.io/web-audio-api/#dom-mediadevices-setdefaultsinkid)

### Enable web applications to understand bimodal performance timings

Web applications may suffer from bimodal distribution in page load performance, due to factors outside of the web application's control. For example:
- When a user agent first launches (a "cold start" scenario), it must perform many expensive initialization tasks that compete for resources on the system.
- Browser extensions can affect the performance of a website. For instance, some extensions run additional code on every page you visit, which can increase CPU usage and result in slower response times.
- When a machine is busy performing intensive tasks, it can lead to slower loading of web pages.

A new `confidence` field on the `PerformanceNavigationTiming` object will enable developers to discern if the navigation timings are representative for their web application.

**References:** [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #1413848](https://bugs.chromium.org/p/chromium/issues/detail?id=1413848) | [ChromeStatus.com entry](https://chromestatus.com/feature/5037395062800384) | [Spec](https://w3c.github.io/navigation-timing/)

### Update of Canvas text rendering implementation

This is not a web-exposed change. The implementation of `CanvasRenderingContext2D` `measureText()`, `fillText()`, and `strokeText()` has a drastic change. This might affect performance, so we'd like to run an origin trial so canvas-heavy applications can try out the new implementation.

**References:** [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #389726691](https://bugs.chromium.org/p/chromium/issues/detail?id=389726691) | [ChromeStatus.com entry](https://chromestatus.com/feature/5104000067985408)

## Deprecations and removals

### Remove HTMLFencedFrameElement.canLoadOpaqueURL()

The `HTMLFencedFrameElement` method `canLoadOpaqueURL()` was replaced with `navigator.canLoadAdAuctionFencedFrame()` in 2023, and calling it has resulted in a deprecation console warning ever since pointing to the new API. The method is removed from Chrome 136.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5083847901667328)

---

*Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.*

*Last updated 2025-04-29 UTC.*
