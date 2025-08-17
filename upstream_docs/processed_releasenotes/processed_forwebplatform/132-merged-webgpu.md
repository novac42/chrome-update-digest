# Chrome 132 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/132

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Docs ](https://developer.chrome.com/docs)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 132

Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** January 14th, 2025

Unless otherwise noted, the following changes apply to Chrome 132 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 132](/blog/new-in-chrome-132). 

## HTML and DOM

### Throw exception for popovers and dialogs in non-active documents

Previously calling `showPopover()` or `showModal()` on a popover or dialog that resides within an inactive document would silently fail. No exception would be thrown, but as the document is inactive, no popover or dialog would be shown. As of Chrome 132, these situations now throw `InvalidStateError`.

[Tracking bug #373684393](https://issues.chromium.org/issues/373684393) | [ChromeStatus.com entry](https://chromestatus.com/feature/6352111728852992) | [Spec](https://github.com/whatwg/html/pull/10705)

### Dialog toggle events

It's useful to know when `<dialog>` elements open and close, and `popover` already has `ToggleEvent` which is dispatched when a popover opens or closes. Previously, to detect when a `<dialog>` opens you had to register a mutation observer to check for open, however, this is quite a lot of work where an event would be easier.

This change incorporates the same `ToggleEvent` that popovers dispatch, but for `<dialog>` elements: when `showModal` or `show` is called, `<dialog>` dispatches a `ToggleEvent` with `newState=open`. When a `<dialog>` is closed (using the form, button, or closewatcher) it should dispatch a `ToggleEvent` with `newState=closed`.

[Tracking bug #41494780](https://issues.chromium.org/issues/41494780) | [ChromeStatus.com entry](https://chromestatus.com/feature/5078613609938944) | [Spec](https://github.com/whatwg/html/pull/10091)

### Fix selection `isCollapsed` in Shadow DOM

Selection isCollapsed should return true if and only if the anchor and focus are the same. This should be true whether the selection starts or ends inside a light or a shadow tree.

[Demo](https://codepen.io/Di-Zhang/pen/jOjdeoX) | [Tracking bug #40400558](https://issues.chromium.org/issues/40400558) | [ChromeStatus.com entry](https://chromestatus.com/feature/5175599392620544) | [Spec](https://w3c.github.io/selection-api/#dom-selection-iscollapsed)

## CSS

### CSS Anchor Positioning: allow `anchor-size()` in `inset` and `margin` properties

Originally, `anchor-size()` was only allowed in sizing properties. The specification was changed to allow `anchor-size()` in insets and margins as well.

[Tracking bug #346521300](https://issues.chromium.org/issues/346521300) | [ChromeStatus.com entry](https://chromestatus.com/feature/5203950077476864) | [Spec](https://drafts.csswg.org/css-anchor-position-1/#anchor-size-fn)

### CSS sideways writing modes

Support of `sideways-rl` and `sideways-lr` keywords for the `writing-mode` CSS property. `sideways-rl` and `sideways-lr` are helpful to write non-CJK text vertically. They don't have behaviors favorable for CJK languages unlike `vertical-rl` and `vertical-lr`.

[MDN writing-mode](https://developer.mozilla.org/docs/Web/CSS/writing-mode) | [Tracking bug #40501131](https://issues.chromium.org/issues/40501131) | [ChromeStatus.com entry](https://chromestatus.com/feature/6201053052928000) | [Spec](https://drafts.csswg.org/css-writing-modes/#propdef-writing-mode)

## Loading

### Fetch: `Request.bytes()` and `Response.bytes()`

Add a `bytes()` method to the `Request` and `Response` interfaces, which returns a promise that resolves with a Uint8Array. While `Request` and `Response` have an `arrayBuffer()` method, you can't read directly from a buffer. You have to create a view such as a `Uint8Array` to read it. The `bytes()` method improves the ergonomics of getting the body of Request and Response.

**Baseline Newly Available:** This feature is now available in all three major browser engines. 

[Tracking bug #340206277](https://issues.chromium.org/issues/340206277) | [ChromeStatus.com entry](https://chromestatus.com/feature/5239268180754432) | [Spec](https://fetch.spec.whatwg.org/#dom-body-bytes)

### Ignore `Strict-Transport-Security` for localhost

`Strict-Transport-Security` (STS) response headers can cause problems for localhost web servers because STS applies host-wide, across all ports. This causes compatibility problems for web developers testing locally. It also affects end-users who use software packages that commonly start localhost web servers for ephemeral reasons. For example, communication of an auth token from a web login to a local software package. If one local listener sets `Strict-Transport-Security` on a localhost response, it's applied to all subsequent localhost requests regardless of port.

Chrome 132 resolves this problem by ignoring `Strict-Transport-Security` headers on responses from localhost URLs.

[Tracking bug #41251622](https://issues.chromium.org/issues/41251622) | [ChromeStatus.com entry](https://chromestatus.com/feature/5134293196865536)

## Media

### Capture all screens

Capture all the screens connected to the device using `getAllScreensMedia()`.

Calling `getDisplayMedia()` multiple times requires multiple user gestures, burdens the user with choosing the next screen each time, and does not guarantee to the app that all the screens were selected. The `getAllScreensMedia()` method improves on all of these fronts.

**Note:** As this feature has privacy ramifications, it is only exposed behind the `MultiScreenCaptureAllowedForUrls` enterprise policy, and users are warned before recording even starts, that recording _could_ start at some point. The API will only work for origins that are specified in the `MultiScreenCaptureAllowedForUrls` allowlist. Any origin not specified there, won't have access to it.

This feature is shipping on Desktop only.

[Design Doc](https://docs.google.com/document/d/1XB8rQRnY5N8G2PeEcNJpVO0q22CutvwW8GGKCZ1z_vc/preview?tab=t.0) | [Tracking bug #40216442](https://issues.chromium.org/issues/40216442) | [ChromeStatus.com entry](https://chromestatus.com/feature/6284029979525120) | [Spec](https://screen-share.github.io/capture-all-screens)

### Element Capture

Given a video `MediaStreamTrack` obtained through pre-existing means to initiate tab-capture, [Element Capture](/docs/web-platform/element-capture) allows mutating the track to only capture a subtree of the DOM starting at a given Element.

The API bears some resemblance to the Region Capture API, but affords greater flexibility for applications, because occluding and occluded content are both excluded from the capture.

[Demo](https://element-capture-demo.glitch.me/) | [Tracking bug #270230413](https://issues.chromium.org/issues/270230413) | [ChromeStatus.com entry](https://chromestatus.com/feature/5198989277790208) | [Spec](https://screen-share.github.io/element-capture)

## Web APIs

### `PushMessageData::bytes()`

The `PushMessageData` interface mimics the `Body` interface, which was amended earlier this year with a new `bytes()` method, following the principle that APIs should generally vend byte buffers as `Uint8Arrays`. Chrome 132 realigns with the `Body` interface by providing the `bytes()` accessor on the `PushMessageData` interface as well.

**Baseline Newly Available:** This feature is now available in all three major browser engines. 

[MDN PushMessageData: bytes() method](https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData/bytes) | [Tracking bug #373336950](https://issues.chromium.org/issues/373336950) | [ChromeStatus.com entry](https://chromestatus.com/feature/5117729756151808) | [Spec](https://www.w3.org/TR/push-api/#dom-pushmessagedata-bytes)

### Keyboard focusable scroll containers

The rollout of this feature (from Chrome 130) was stopped due to an accessibility regression. This is fixed and the feature continues to roll out with Chrome 132.

[Keyboard focusable scrollers](/blog/keyboard-focusable-scrollers) | [Tracking bug #40113891](https://issues.chromium.org/issues/40113891) | [ChromeStatus.com entry](https://chromestatus.com/feature/5231964663578624) | [Spec](https://drafts.csswg.org/css-overflow-3/#scroll-container)

### Device Posture API

This API helps developers to detect the current posture of a foldable device. The _device posture_ is the physical position in which a device holds which may be derived from sensors in addition to the angle.

From enhancing the usability of a website by avoiding the area of a fold, to enabling innovative use cases for the web, knowing the posture of a device can help developers tailor their content to different devices.

Content can be consumed and browsed even when the device is not flat, in which case the developer might want to provide a different layout for it depending on the posture state in which the device is being used.

[Git Repo](https://github.com/foldable-devices) | [Tracking bug #40124716](https://issues.chromium.org/issues/40124716) | [ChromeStatus.com entry](https://chromestatus.com/feature/5185813744975872) | [Spec](https://www.w3.org/TR/device-posture)

### Saved queries in `sharedStorage.selectURL`

`sharedStorage.selectURL()` now allows queries to be saved and reused on a per-page basis, where the two per-page-load budgets are charged the first time a saved query is run but not for subsequent runs of the saved query during the same page-load. This is accomplished with a `savedQuery` parameter in the options for `selectURL()` that names the query.

[Tracking bug #367440966](https://issues.chromium.org/issues/367440966) | [ChromeStatus.com entry](https://chromestatus.com/feature/5098690386329600) | [Spec](https://github.com/WICG/shared-storage/pull/188)

### Private State Token API Permissions Policy default allowlist wildcard

Access to the Private State Token API is gated by Permissions Policy features. Chrome 132 updates the default allowlist for both `private-state-token-issuance` and `private-state-token-redemption` features from `self` to `*` (wildcard).

[ChromeStatus.com entry](https://chromestatus.com/feature/5205548434456576) | [Spec](https://github.com/WICG/trust-token-api/pull/306)

### FedCM Mode API and Use Other Account API

Two new extensions for FedCM:

  * **Mode** : The `active` mode allows websites to call FedCM inside a button click (for example, clicking on a **Sign-in to IdP** button), which requires FedCM to guarantee it will always respond with a visible user interface. Calling the FedCM API in _active mode_ takes users to login to the Identity Provider (IdP) when users are logged-out. Also, because the active mode is called within an explicit user gesture, the UI is also more prominent (for example, centered and modal) compared to the UI from the passive mode (which doesn't require a user gesture requirement and can be called on page load).
  * **Use Other Account** : With this extension, an IdP can allow users to sign into other accounts.

[Demo](https://fedcm-button.glitch.me/) | [Tracking bug #370694829](https://issues.chromium.org/issues/370694829) | [ChromeStatus.com entry](https://chromestatus.com/feature/4689551782313984) | [Spec](https://github.com/w3c-fedid/FedCM/pull/660)

### File System Access for Android and WebView

This API enables developers to build powerful apps that interact with other (non-Web) apps on the user's device using the device's file system. After a user grants a web app access, this API allows the app to read or save changes directly to files and folders selected by the user. Beyond reading and writing files, this API provides the ability to open a directory and enumerate its contents, as well as store file and directory handles in IndexedDB to later regain access to the same content.

[File System access](/docs/capabilities/web-apis/file-system-access) shipped on Desktop in Chrome 86, with Chrome 132 it's available on Android and WebView.

[The File System Access API](/docs/capabilities/web-apis/file-system-access) | [Tracking bug #40091667](https://issues.chromium.org/issues/40091667) | [ChromeStatus.com entry](https://chromestatus.com/feature/6284708426022912) | [Spec](https://wicg.github.io/file-system-access)

### WebAuthn Signal API

Allows WebAuthn relying parties to signal information about existing credentials back to credential storage providers, so that incorrect or revoked credentials can be updated or removed from provider and system UI.

Learn more about [the Signal API for passkeys on Chrome desktop](/blog/passkeys-signal-api).

[Demo](https://signal-api-demo.glitch.me/) | [Tracking bug #361751877](https://issues.chromium.org/issues/361751877) | [ChromeStatus.com entry](https://chromestatus.com/feature/5101778518147072) | [Spec](https://pr-preview.s3.amazonaws.com/nsatragno/webauthn/pull/2093.html#sctn-signal-methods)

## Rendering and graphics

### WebGPU: 32-bit float textures blending

The `float32-blendable` GPU feature makes GPU textures with formats `r32float`, `rg32float`, and `rgba32float` blendable.

[Tracking bug #369649348](https://issues.chromium.org/issues/369649348) | [ChromeStatus.com entry](https://chromestatus.com/feature/5173655901044736) | [Spec](https://www.w3.org/TR/webgpu/#float32-blendable)

### WebGPU: Expose `GPUAdapterInfo` from `GPUDevice`

The GPUDevice `adapterInfo` attribute exposes the same `GPUAdapterInfo` as the `GPUAdapter` object.

[Tracking bug #376600838](https://issues.chromium.org/issues/376600838) | [ChromeStatus.com entry](https://chromestatus.com/feature/6221851301511168) | [Spec](https://www.w3.org/TR/webgpu/#dom-gpudevice-adapterinfo)

### WebGPU: Texture view usage

Adds an optional field to WebGPU texture view creation to request a subset of the usage flags from the source texture.

By default, texture view usage inherits from the source texture but there are view formats which can be incompatible with the full set of inherited usages. Adding a usage field to texture view creation allows the user to request a subset of the source texture's usages that are valid with the view format and specific to their intended usage of the texture view.

WebGPU implementations can also optimize the creation of low level resources and improve performance when using views with more specialized usage flags.

[Tracking bug #363903526](https://issues.chromium.org/issues/363903526) | [ChromeStatus.com entry](https://chromestatus.com/feature/5155252832305152) | [Spec](https://github.com/gpuweb/gpuweb/commit/b39d86d356eb759d7564bc7c808ca62fce8bbf3e)

## WebGPU

### Texture view usage

GPU texture views currently inherit all usage flags from their source GPU texture. This can be problematic as some view formats are incompatible with certain usages. To address this issue, calling [`createView()`](https://developer.mozilla.org/docs/Web/API/GPUTexture/createView) with the optional [`usage`](https://gpuweb.github.io/gpuweb/#dom-gputextureviewdescriptor-usage) member lets you explicitly specify a subset of the source texture's usage flags that are compatible with the chosen view format.

This change allows for upfront validation and more fine-grained control over how the view is used. It also aligns with other graphics APIs where usage flags are common parameters in view creation, offering optimization opportunities.

See the following snippet, the [chromestatus entry](https://chromestatus.com/feature/5155252832305152), and [issue 363903526](https://issues.chromium.org/issues/363903526).
    
    
    const texture = myDevice.createTexture({
      size: [4, 4],
      format: "rgba8unorm",
      usage:
        GPUTextureUsage.RENDER_ATTACHMENT |
        GPUTextureUsage.TEXTURE_BINDING |
        GPUTextureUsage.STORAGE_BINDING,
      viewFormats: ["rgba8unorm-srgb"],
    });
    
    const view = texture.createView({
      format: 'rgba8unorm-srgb',
      usage: GPUTextureUsage.RENDER_ATTACHMENT, // Restrict allowed usage.
    });
    

### 32-bit float textures blending

32-bit floating-point textures are essential for HDR rendering to preserve a wide range of color values and prevent color banding artifacts. For example in scientific visualization.

The new [`"float32-blendable"`](https://gpuweb.github.io/gpuweb/#float32-blendable) GPU feature makes GPU textures with formats `"r32float"`, `"rg32float"`, and `"rgba32float"` blendable. Creating a render pipeline that uses blending with any float32-format attachment is now possible when requesting a GPU device with this feature.

See the following snippet, the [chromestatus entry](https://chromestatus.com/feature/5173655901044736), and [issue 369649348](https://issues.chromium.org/issues/369649348).
    
    
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter.features.has("float32-blendable")) {
      throw new Error("32-bit float textures blending support is not available");
    }
    // Explicitly request 32-bit float textures blending support.
    const device = await adapter.requestDevice({
      requiredFeatures: ["float32-blendable"],
    });
    
    // ... Creation of shader modules is omitted for readability.
    
    // Create a render pipeline that uses blending for the rgba32float format.
    device.createRenderPipeline({
      vertex: { module: myVertexShaderModule },
      fragment: {
        module: myFragmentShaderModule,
        targets: [
          {
            format: "rgba32float",
            blend: { color: {}, alpha: {} },
          },
        ],
      },
      layout: "auto",
    });
    
    // Create the GPU texture with rgba32float format and
    // send the appropriate commands to the GPU...
    

**Note:** Chrome incorrectly considers any texture type which supports float filtering as blendable. This incorrect behavior is being phased out with the `"float32-blendable"` GPU feature and will soon be eliminated entirely. For more details, see [issue 364987733](https://issues.chromium.org/issues/364987733).

### GPUDevice `adapterInfo` attribute

It's important for libraries that take user-provided `GPUDevice` objects to access information about the physical GPU, as they may need to optimize or implement workarounds based on the GPU architecture. While it is possible to access to this information through the `GPUAdapter` object, there is no direct way to get it from a `GPUDevice` alone. This can be inconvenient, as it may require users to provide additional information alongside the `GPUDevice`.

To address this problem, [`GPUAdapterInfo`](https://developer.mozilla.org/docs/Web/API/GPUAdapterInfo) is now exposed through the `GPUDevice` [`adapterInfo`](https://gpuweb.github.io/gpuweb/#dom-gpudevice-adapterinfo) attribute. Those are similar to the existing `GPUAdapter` [`info`](https://developer.mozilla.org/docs/Web/API/GPUAdapter/info) attribute.

See the following snippet, the [chromestatus entry](https://chromestatus.com/feature/6221851301511168), and [issue 376600838](https://issues.chromium.org/issues/376600838).
    
    
    function optimizeForGpuDevice(device) {
      if (device.adapterInfo.vendor === "amd") {
        // Use AMD-specific optimizations.
      } else if (device.adapterInfo.architecture.includes("turing")) {
        // Optimize for NVIDIA Turing architecture.
      }
    }
    

### Configuring canvas context with invalid format throw JavaScript error

Previously, using an invalid texture format with the [`configure()`](https://developer.mozilla.org/docs/Web/API/GPUCanvasContext/configure) method of the GPU canvas context resulted in a GPU validation error. This has been changed to throw a JavaScript `TypeError`. This prevents scenarios where [`getCurrentTexture()`](https://developer.mozilla.org/docs/Web/API/GPUCanvasContext/getCurrentTexture) returns a valid GPU texture despite the GPU canvas context being configured incorrectly. More information can be found in [issue 372837859](https://issues.chromium.org/issues/372837859).

### Filtering sampler restrictions on textures

Using `"sint"`, `"uint"`, and "`depth"` format textures with filtering samples was allowed previously. It now correctly disallows using an `"sint"` or `"uint"` format texture with a filtering sampler. Note that it currently emits a warning if you use a "`depth"` texture with a filtering sampler as it will be disallowed in the future. See [issue 376497143](https://issues.chromium.org/issues/376497143).

Those restrictions means using a depth texture with a non-filtering sampler requires manual creation of bind group layouts. This is because the "auto" generated bind group layouts don't support this combination yet. [Spec issue 4952](https://github.com/gpuweb/gpuweb/issues/4952) contains a proposal under consideration to address this limitation in the future.

### Extended subgroups experimentation

The [subgroups experimentation](/blog/new-in-webgpu-128#experimenting_with_subgroups), initially set to end in Chrome 131, has been extended to Chrome 133, concluding on April 16, 2025. While the first origin trial focused on performance, it lacked crucial [portability safeguards](https://github.com/gpuweb/gpuweb/pull/4963). These safeguards will now be added, potentially causing errors in existing code.

### Improving developer experience

A warning is now visible in DevTools when the `powerPreference` option is used with [`requestAdapter()`](https://developer.mozilla.org/docs/Web/API/GPU/requestAdapter) on Windows. This warning will be removed when Chrome knows how to use two different GPUs and composite the results between them. See [issue 369219127](https://issues.chromium.org/issues/369219127).

The size of the GPU buffer is now present in the error message when creating a GPU buffer that is too large. See [issue 374167798](https://issues.chromium.org/issues/374167798).

### Experimental support for 16-bit normalized texture formats

16-bit signed normalized and unsigned normalized texture formats are now available experimentally respectively behind the `"chromium-experimental-snorm16-texture-formats"` and `"chromium-experimental-unorm16-texture-formats"` GPU features while they're being [discussed for standardization](https://github.com/gpuweb/gpuweb/issues/3001).

These features add support for 16-bit normalized texture formats with `COPY_SRC`, `COPY_DST`, `TEXTURE_BINDING`, `RENDER_ATTACHMENT` usages, multisampling, and resolving capabilities. The additional formats are `"r16unorm"`, `"rg16unorm"`, `"rgba16unorm"`, `"r16snorm"`, `"rg16snorm"`, and `"rgba16snorm"`.

Until these experimental features are standardized, enable the "Unsafe WebGPU Support" flag at `chrome://flags/#enable-unsafe-webgpu` to make them available in Chrome.

See the following snippet and [issue 374790898](https://issues.chromium.org/issues/374790898).
    
    
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter.features.has("chromium-experimental-snorm16-texture-formats")) {
      throw new Error("16-bit signed normalized formats support is not available");
    }
    // Explicitly request 16-bit signed normalized formats support.
    const device = await adapter.requestDevice({
      requiredFeatures: ["chromium-experimental-snorm16-texture-formats"],
    });
    
    // Create a texture with the rgba16snorm format which consists of four
    // components, each of which is a 16-bit, normalized, signed integer value.
    const texture = device.createTexture({
      size: [4, 4],
      format: "rgba16snorm",
      usage: GPUTextureUsage.RENDER_ATTACHMENT | GPUTextureUsage.TEXTURE_BINDING,
    });
    
    // Send the appropriate commands to the GPU...
    

### Dawn updates

The `EnumerateFeatures(FeatureName * features)` methods from `wgpu::Adapter` and `wgpu::Device` are deprecated in favor of using `GetFeatures(SupportedFeatures * features)`. See [issue 368672123](https://issues.chromium.org/issues/368672123).

The webgpu.h C API has changed all `char const *` to a [`WGPUStringView`](https://webgpu-native.github.io/webgpu-headers/Strings.html) structure that defines a view into a UTF-8 encoded string. It acts like a pointer to the string's data, coupled with a length. This lets you work with parts of a string without needing to copy it. See [issue 42241188](https://issues.chromium.org/issues/42241188).

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/6778..chromium/6834?n=1000).

## Origin trials

### Explicit compile hints with magic comments

This feature lets you attach information about which functions should be eagerly parsed and compiled in JavaScript files. The information will be encoded as magic comments.

[Origin Trial](/origintrials#/view_trial/4317826142741463041) | [Explainer](https://explainers-by-googlers.github.io/explicit-javascript-compile-hints-file-based) | [Tracking bug #42203853](https://issues.chromium.org/issues/42203853) | [ChromeStatus.com entry](https://chromestatus.com/feature/5100466238652416)

### `Document-Isolation-Policy`

`Document-Isolation-Policy` allows a document to enable `crossOriginIsolation` for itself, without having to deploy COOP or COEP, and regardless of the `crossOriginIsolation` status of the page. The policy is backed by process isolation. Additionally, the document non-CORS cross-origin subresources will either be loaded without credentials or will need to have a CORP header.

[Origin Trial](/origintrials#/view_trial/3670996646260375553) | [Tracking bug #333029146](https://issues.chromium.org/issues/333029146) | [ChromeStatus.com entry](https://chromestatus.com/feature/5141940204208128) | [Spec](https://wicg.github.io/document-isolation-policy)

## Deprecations and removals

### `navigator.storage` no longer an `EventTarget`

`navigator.storage` was made an `EventTarget` for the Storage Pressure Event, which never made it past the prototype phase. This dead code is being removed and as a result, `navigator.storage` will no longer extend `EventTarget`.

[ChromeStatus.com entry](https://chromestatus.com/feature/5132158480678912) | [Spec](https://storage.spec.whatwg.org/)

### Remove prefixed `HTMLVideoElement` fullscreen APIs

The prefixed `HTMLVideoElement` fullscreen APIs have been deprecated from Chrome.

They were replaced by the `Element.requestFullscreen()` API, which first shipped unprefixed in Chrome 71, in 2018. As of 2024, most browsers have had support for the unprefixed APIs for a few years now.

Chrome 132 removes the following from `HTMLVideoElement`:

  * The `webkitSupportsFullscreen` attribute.
  * The `webkitDisplayingFullscreen` attribute.
  * The `webkitEnterFullscreen()` method.
  * The `webkitExitFullscreen()` method. Note the different capitalization of the "S" in FullScreen.
  * The `webkitEnterFullScreen()` method.
  * The `webkitExitFullScreen()` method.

These methods are now only aliases for the modern API. Their use has declined steadily over the years.

[ChromeStatus.com entry](https://chromestatus.com/feature/5111638103687168)

## Further reading

Looking for more? Check out these additional resources.

  * [What's new in Chrome 132](/blog/new-in-chrome-132)
  * [What's new in Chrome DevTools 132](/blog/new-in-devtools-132)
  * [ChromeStatus.com updates for Chrome 132](https://chromestatus.com/features#milestone%3D132)
  * [Chrome release calendar](https://chromiumdash.appspot.com/schedule)
  * [Upcoming deprecations](https://chromestatus.com/features#browsers.chrome.status%3A%22Deprecated%22)
  * [Upcoming removals](https://chromestatus.com/features#browsers.chrome.status%3A%22Removed%22)

## Download Google Chrome

Download Chrome for [Android](https://play.google.com/store/apps/details?id=com.android.chrome), [Desktop](https://www.google.com/chrome/), or [iOS](https://apps.apple.com/us/app/google-chrome/id535886823). 

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-01-14 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-01-14 UTC."],[],[]] 
