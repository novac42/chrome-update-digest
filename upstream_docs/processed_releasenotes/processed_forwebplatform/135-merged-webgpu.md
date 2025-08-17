# Chrome 135 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/135

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Docs ](https://developer.chrome.com/docs)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 135

Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** April 1st, 2025

Unless otherwise noted, the following changes apply to Chrome 135 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 135](/blog/new-in-chrome-135). 

## HTML and DOM

### Invoker Commands; the command and commandfor attributes

The `command` and `commandfor` attributes on `<button>` elements let you assign behaviour to buttons in a more accessible and declarative way.

[Tracking bug #1490919](https://issues.chromium.org/issues/1490919) | [ChromeStatus.com entry](https://chromestatus.com/feature/5142517058371584) | [Spec](https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-commandfor)

### Link `rel=facilitated-payment` to support push payments

Adds support for `<link rel="facilitated-payment" href="...">` as a hint that the browser should notify registered payment clients about a pending push payment.

[Tracking bug #1477049](https://issues.chromium.org/issues/1477049) | [ChromeStatus.com entry](https://chromestatus.com/feature/5198846820352000)

## CSS

### `::column` pseudo-element for carousels

A `::column` pseudo-element, which allows applying a limited set of styles to the generated fragments. Specifically, this would be limited to styles which do not affect the layout, and thus can be applied post-layout.

[ChromeStatus.com entry](https://chromestatus.com/feature/5192332683771904)

### `::scroll-button()` pseudo-elements

Allows the creation of interactive scroll buttons as pseudo-elements, for example:
    
    
    .scroller {
      overflow: auto;
    }
    
    .scroller::scroll-button(inline-start) {
      content: "<";
    }
    
    .scroller::scroll-button(inline-end) {
      content: ">";
    }
    

These should be focusable, behaving as a button (including their UA styles). When activated, a scroll should be performed in the direction by some amount. When it is not possible to scroll in that direction, they should be disabled (and styled with `:disabled`), otherwise they are enabled (and styled with `:enabled`).

The selector lets you define buttons in four logical directions: `block-start`, `block-end`, `inline-start`, `inline-end`; as well as four physical directions: `up`, `down`, `left`, `right`.

[Tracking bug #370067113](https://issues.chromium.org/issues/370067113) | [ChromeStatus.com entry](https://chromestatus.com/feature/5093129273999360) | [Spec](https://drafts.csswg.org/css-overflow-5/#scroll-buttons)

### `::scroll-marker` and `::scroll-marker-group`

Adds the `::scroll-marker` and `::scroll-marker-group` pseudo-elements for scrolling containers. They let you create a set of focusable markers for all of the associated items within the scrolling container.

[Tracking bug #332396355](https://issues.chromium.org/issues/332396355) | [ChromeStatus.com entry](https://chromestatus.com/feature/5160035463462912) | [Spec](https://drafts.csswg.org/css-overflow-5/#scroll-markers)

### CSS Inertness—the `interactivity` property

The `interactivity` property specifies whether an element and its flat tree descendants (including text runs) are inert or not.

Making an element inert affects whether it can be focused, edited, selected, and searchable by find-in-page. It also affects whether it is visible in the accessibility tree.

[ChromeStatus.com entry](https://chromestatus.com/feature/5107436833472512) | [Spec](https://github.com/flackr/carousel/tree/main/inert)

### CSS logical overflow

The `overflow-inline` and `overflow-block` CSS properties allow setting overflow in inline and block direction relative to the writing-mode. In a horizontal writing-mode `overflow-inline` maps to `overflow-x`, while in a vertical writing-mode it maps to `overflow-y`.

[Tracking bug #41489999](https://issues.chromium.org/issues/41489999) | [ChromeStatus.com entry](https://chromestatus.com/feature/4728308937523200) | [Spec](https://drafts.csswg.org/css-overflow-3/#overflow-control)

### CSS anchor positioning remembered scroll offset

Add support for the concept of _remembered scroll offset_.

When a positioned element has a default anchor, and is tethered to this anchor at one edge, and against the original containing block at the other edge, the scroll offset will be taken into account when it comes to sizing the element. This way you can use all visible space (using `position-area`) for the anchored element when the document is scrolled at a given scroll offset.

In order to avoid layout (resizing the element) every time the document is scrolled (which is undesired behavior, and also bad for performance), what will be used is a so-called "remembered scroll offset", rather than always using the current scroll offset. The remembered scroll offset is updated at a so-called "anchor recalculation point", which is either:

  * When the positioned element is initially displayed.
  * When a different position option (`position-try-fallbacks`) is chosen.

[Tracking bug #373874012](https://issues.chromium.org/issues/373874012) | [ChromeStatus.com entry](https://chromestatus.com/feature/4710507824807936) | [Spec](https://drafts.csswg.org/css-anchor-position-1/#scroll)

### CSS `shape()` function

The `shape()` function allows responsive free-form shapes in `clip-path`.

You can define a series of verbs, roughly equivalent to the verbs in `path()`, but where the verbs accept responsive units (such as `%` or `vw`), as well as any CSS values such as custom properties.

[Tracking bug #40829059](https://issues.chromium.org/issues/40829059) | [ChromeStatus.com entry](https://chromestatus.com/feature/5172258539307008) | [Spec](https://drafts.csswg.org/css-shapes-2/#shape-function)

### `safe-area-max-inset-*` variables

This feature adds `max-area-safe-inset-*` variables which don't change and represent the maximum possible safe area inset.

The use case this solves is to avoid needing to relayout the page in cases where the footer (for example) can simply slide as the safe area inset value grows, as opposed to changing size.

[Tracking bug #391621941](https://issues.chromium.org/issues/391621941) | [ChromeStatus.com entry](https://chromestatus.com/feature/6393888941801472) | [Spec](https://drafts.csswg.org/css-env-1/#safe-area-max-insets)

### Nested pseudo elements styling

Allows to style pseudo elements that are nested inside other pseudo elements. So far, support is defined for:

  * `::before::marker`
  * `::after::marker`

With `::column::scroll-marker` being supported in the future.

[Tracking bug #373478544](https://issues.chromium.org/issues/373478544) | [ChromeStatus.com entry](https://chromestatus.com/feature/5199947786616832) | [Spec](https://www.w3.org/TR/css-pseudo-4/#marker-pseudo)

## Audio and video

### Add MediaStreamTrack support to the Web Speech API

Add MediaStreamTrack support to the Web Speech API.

The Web Speech API is a web standard API that allows developers to incorporate speech recognition and synthesis into their web pages. Currently, the Web Speech API uses the user's default microphone as the audio input. MediaStreamTrack support allows websites to use the Web Speech API to caption other sources of audio including remote audio tracks.

[ChromeStatus.com entry](https://chromestatus.com/feature/5178378197139456) | [Spec](https://wicg.github.io/speech-api)

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

## WebGPU

  * [ Blog ](https://developer.chrome.com/blog)

#  What's New in WebGPU (Chrome 135)

Stay organized with collections  Save and categorize content based on your preferences. 

![François Beaufort](https://web.dev/images/authors/beaufortfrancois.jpg)

François Beaufort 

[ GitHub ](https://github.com/beaufortfrancois)

Published: March 26, 2025 

**Experimental:** WebGPU integration with WebXR is now available for developer testing on Windows and Android. Learn more at[ Experimenting with WebGPU in WebXR](https://toji.dev/2025/03/03/experimenting-with-webgpu-in-webxr.html).

### Allow creating pipeline layout with null bind group layout

Previously, creating an empty bind group layout required adding a bind group with zero bindings, which was inconvenient. This is no longer necessary as null bind group layouts are now allowed and ignored when creating a pipeline layout. This should make development easier.

For example, you might want to create a pipeline that uses only bind group layouts 0 and 2. You could assign bind group layout 1 to fragment data and bind group layout 2 to vertex data, and then render without a fragment shader. See [issue 377836524](https://issues.chromium.org/issues/377836524).
    
    
    const bgl0 = myDevice.createBindGroupLayout({ entries: myGlobalEntries });
    const bgl1 = myDevice.createBindGroupLayout({ entries: myFragmentEntries });
    const bgl2 = myDevice.createBindGroupLayout({ entries: myVertexEntries });
    
    // Create a pipeline layout that will be used to render without a fragment shader.
    const myPipelineLayout = myDevice.createPipelineLayout({
      bindGroupLayouts: [bgl0, null, bgl2],
    });
    

### Allow viewports to extend past the render targets bounds

The requirements for viewport validation have been relaxed to allow viewports to go beyond the render target boundaries. This is especially useful for drawing 2D elements such as UI that may extend outside the current viewport. See [issue 390162929](https://issues.chromium.org/issues/390162929).
    
    
    const passEncoder = myCommandEncoder.beginRenderPass({
      colorAttachments: [
        {
          view: myColorTexture.createView(),
          loadOp: "clear",
          storeOp: "store",
        },
      ],
    });
    
    // Set a viewport that extends past the render target's bounds by 8 pixels
    // in all directions.
    passEncoder.setViewport(
      /*x=*/ -8,
      /*y=*/ -8,
      /*width=*/ myColorTexture.width + 16,
      /*height=*/ myColorTexture.height + 16,
      /*minDepth=*/ 0,
      /*maxDepth=*/ 1,
    );
    
    // Draw geometry and complete the render pass as usual.
    

### Easier access to the experimental compatibility mode on Android

The `chrome://flags/#enable-unsafe-webgpu` flag alone now enables all capabilities required for the experimental [WebGPU compatibility mode](/blog/new-in-webgpu-122#expand_reach_with_compatibility_mode_feature_in_development) on Android. With that, you can request a GPUAdapter in compatibility mode with the `featureLevel: "compatibility"` option and even get access to the OpenGL ES backend on devices lacking support for Vulkan. See the following example and issue [dawn:389876644](https://issues.chromium.org/issues/389876644).
    
    
    // Request a GPUAdapter in compatibility mode.
    const adapter = await navigator.gpu.requestAdapter({ featureLevel: "compatibility" });
    

![WebGPU report page shows a GPUAdapter in compatibility mode on Android device.](/static/blog/new-in-webgpu-135/image/compatibility-mode-android.jpg) Compatibility mode adapter info in [webgpureport.org](https://webgpureport.org).

### Remove maxInterStageShaderComponents limit

As [previously announced](/blog/new-in-webgpu-133#deprecate_maxinterstageshadercomponents_limit), the maxInterStageShaderComponents limit is removed due to a combination of factors:

  * Redundancy with `maxInterStageShaderVariables`: This limit already serves a similar purpose, controlling the amount of data passed between shader stages.
  * Minor discrepancies: While there are slight differences in how the two limits are calculated, these differences are minor and can be effectively managed within the `maxInterStageShaderVariables` limit.
  * Simplification: Removing `maxInterStageShaderComponents` streamlines the shader interface and reduces complexity for developers. Instead of managing two separate limits with subtle differences, they can focus on the more appropriately named and comprehensive `maxInterStageShaderVariables`.

See [intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/i5oJu9lZPAk) and [issue 364338810](https://issues.chromium.org/issues/364338810).

### Dawn updates

It's no longer possible to use a filtering sampler to sample a depth texture. As a reminder, a depth texture can only be used with a non filtering or a comparison sampler. See [issue 379788112](https://issues.chromium.org/issues/379788112).

The `WGPURequiredLimits` and `WGPUSupportedLimits` structures have been flattened into `WGPULimits`. See [issue 374263404](https://issues.chromium.org/issues/374263404).

The following structs have been renamed. See [issue 42240793](https://issues.chromium.org/issues/42240793).

  * `WGPUImageCopyBuffer` is now `WGPUTexelCopyBufferInfo`
  * `WGPUImageCopyTexture` is now `WGPUTexelCopyTextureInfo`
  * `WGPUTextureDataLayout` is now `WGPUTexelCopyBufferLayout`

The `subgroupMinSize` and `subgroupMaxSize` members have been added to the `WGPUAdapterInfo` struct. See [webgpu-headers PR](https://github.com/webgpu-native/webgpu-headers/pull/509).

Tracing Dawn API usage in Metal is now possible when running your program with the `DAWN_TRACE_FILE_BASE` environment variable which saves a .gputrace file that can be loaded later into XCode's Metal Debugger. See the [Debugging Dawn](https://dawn.googlesource.com/dawn/+/HEAD/docs/dawn/debugging.md#tracing-native-gpu-api-usage) documentation.

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/6998..chromium/7049?n=1000).

## Origin trials

### Device bound session credentials

A way for websites to securely bind a session to a single device.

It will let servers have a session be securely bound to a device. The browser will renew the session periodically as requested by the server, with proof of possession of a private key.

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/3911939226324697089) | [ChromeStatus.com entry](https://chromestatus.com/feature/5140168270413824) | [Spec](https://w3c.github.io/webappsec-dbsc)

### Interest invokers

This feature adds an `interesttarget` attribute to `<button>` and `<a>` elements. The `interesttarget` attribute adds "interest" behaviors to the element, such that when the user "shows interest" in the element, actions are triggered on the target element. Actions can include things like showing a popover. The user agent will handle detecting when the user "shows interest" in the element—when hovering the element with a mouse, hitting special hotkeys on the keyboard, or long-pressing the element on touchscreens. When interest is shown or lost, an `InterestEvent` will be fired on the target, which have default actions in the case of popovers - showing and hiding the popover.

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/813462682693795841) | [Tracking bug #326681249](https://issues.chromium.org/issues/326681249) | [ChromeStatus.com entry](https://chromestatus.com/feature/4530756656562176) | [Spec](https://github.com/whatwg/html/pull/11006)

### Signature-based integrity

This feature provides web developers with a mechanism to verify the provenance of resources they depend upon, creating a technical foundation for trust in a site's dependencies. In short: servers can sign responses with a Ed25519 key pair, and web developers can require the user agent to verify the signature using a specific public key. This offers a helpful addition to URL-based checks offered by Content Security Policy on the one hand, and Subresource Integrity's content-based checks on the other.

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/2704974526189404161) | [Tracking bug #375224898](https://issues.chromium.org/issues/375224898) | [ChromeStatus.com entry](https://chromestatus.com/feature/5032324620877824) | [Spec](https://wicg.github.io/signature-based-sri)

### Speculation rules: target_hint field

This extends speculation rules syntax to allow developers to specify the target_hint field.

This field provides a hint to indicate a target navigable where a prerendered page will eventually be activated. For example, when _blank is specified as a hint, a prerendered page can be activated for a navigable opened by window.open(). The field has no effect on prefetching.

The specification allows this field to accept any strings that are valid as navigable target name or keyword as the value, but this launch supports only one of `"_self"` or `"_blank"` strings. If the hint is not specified, it's treated as if `"_self"` is specified.

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/1858297796243750913) | [Tracking bug #40234240](https://issues.chromium.org/issues/40234240) | [ChromeStatus.com entry](https://chromestatus.com/feature/5162540351094784) | [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html)

## Deprecations and removals

### Remove deprecated `navigator.xr.supportsSession` method

The `navigator.xr.supportsSession` method was replaced in the WebXR spec by the `navigator.xr.isSessionSupported` method in September 2019 after receiving feedback on the API shape from the TAG. It has been marked as deprecated in Chromium since then, producing a console warning redirecting developers to the updated API.

Use of the call is very low, and all major frameworks that are used to build WebXR content have been confirmed to have been updated to use the newer call.

[ChromeStatus.com entry](https://chromestatus.com/feature/5114816316047360) | [Spec](https://immersive-web.github.io/webxr/#dom-xrsystem-issessionsupported)

### Remove WebGPU limit `maxInterStageShaderComponents`

The `maxInterStageShaderComponents` limit is being removed due to a combination of factors:

  * Redundancy with `maxInterStageShaderVariables`: This limit already serves a similar purpose, controlling the amount of data passed between shader stages.
  * Minor Discrepancies: While there are slight differences in how the two limits are calculated, these differences are minor and can be effectively managed within the `maxInterStageShaderVariables` limit.
  * Simplification: Removing `maxInterStageShaderComponents` streamlines the shader interface and reduces complexity for developers. Instead of managing two separate limits (that both apply simultaneously but with subtle differences), they can focus on the more appropriately named and comprehensive `maxInterStageShaderVariables`.

[Tracking bug #364338810](https://issues.chromium.org/issues/364338810) | [ChromeStatus.com entry](https://chromestatus.com/feature/4853767735083008) | [Spec](https://gpuweb.github.io/gpuweb/#dom-supported-limits-maxinterstageshadervariables)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-04-01 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-04-01 UTC."],[],[]] 
