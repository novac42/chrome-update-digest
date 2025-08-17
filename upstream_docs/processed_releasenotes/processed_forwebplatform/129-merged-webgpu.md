# Chrome 129 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/129

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Docs ](https://developer.chrome.com/docs)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 129

Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** September 17th, 2024

Unless otherwise noted, the following changes apply to Chrome 129 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 129](/blog/new-in-chrome-129). 

## Browser changes and development tools

### Compute Pressure WebDriver extension commands

Exposes WebDriver commands for creating, removing and updating pressure source samples for _virtual pressure sources_. Such pressure sources don't depend on underlying hardware or operating system support and can be used for testing.

[Tracking bug #347031400](https://issues.chromium.org/issues/347031400) | [ChromeStatus.com entry](https://chromestatus.com/feature/5130657352384512) | [Spec](https://github.com/w3c/compute-pressure/pull/284)

## CSS

### CSS interpolate-size property and calc-size() function

The CSS `interpolate-size` property lets a page opt into animations and transitions of CSS intrinsic sizing keywords such as `auto`, `min-content`, and `fit-content`, in the cases where those keywords can be animated.

The CSS `calc-size()` function is a CSS function similar to `calc()`, however it also supports operations on exactly one supported sizing keyword. Supported sizing keywords are `auto`, `min-content`, `max-content`, and `fit-content`. Other sizing keywords that may be supported in the future include `stretch` (currently supported as prefixed `-webkit-fill-available`) and `contain`. This function is used to represent the values in the middle of the animations allowed by the `interpolate-size` property.

[Tracking bug #40339056](https://issues.chromium.org/issues/40339056) | [ChromeStatus.com entry](https://chromestatus.com/feature/5196713071738880) | [Spec](https://drafts.csswg.org/css-values-5/#calc-size)

### Rename CSS anchor positioning `inset-area` to `position-area`

The [CSSWG resolved to rename this property](https://github.com/w3c/csswg-drafts/issues/10209#issuecomment-2221005001) from `inset-area` to `position-area`. Chrome 129 ships `position-area`, the `inset-area` name will be removed in a future release.

[Blog post](/blog/anchor-syntax-changes) | [ChromeStatus.com entry](https://chromestatus.com/feature/5142143019253760) | [Spec](https://github.com/w3c/csswg-drafts/issues/10209#issuecomment-2221005001)

### Update CSS backdrop-filter to use mirror edgeMode

The `backdrop-filter` CSS property applies one or more filters to the _backdrop_ of an element. The backdrop is the painted content that lies behind the element. A common filter is a blur allowing designers to construct "frosted glass" dialog boxes, video overlays, translucent navigation headers, and more.

This was initially implemented the same way as a regular blur, but sampling beyond the edges of the element allowed colors from the edges to bleed in. The spec was changed to sample pixels outside the backdrop edges by duplicating the pixels at the edge. This however, results in extreme flickering of content as it enters the backdrop edge. The latest specification change mirrors the backdrop when sampling beyond the edge which allows for a smooth gradual introduction of new colors at the edges without overweighting on single lines of color.

[Demo](https://jsbin.com/fumeloh/edit?html,css,output) | [Tracking bug #40040614](https://issues.chromium.org/issues/40040614) | [ChromeStatus.com entry](https://chromestatus.com/feature/5382638738341888) | [Spec](https://drafts.fxtf.org/filter-effects-2/#backdrop-filter-operation)

## Media

### Blob support in WebRTC data channels

Implements `RTCDataChannel.send(Blob)`, and the `onMessage` event can now optionally receive data of type Blob using the `binaryType` attribute.

In addition to supporting sending strings and ArrayBuffers, you can now choose to send a Blob instead as long as its size is below the SCTP transport `maxMessageSize` as indicated in the [WebRTC specification](https://www.w3.org/TR/webrtc/#dom-rtcsctptransport-maxmessagesize).

Using the `binaryType` attribute set to `blob`, the `onMessage` event data attribute will be of type Blob instead of ArrayBuffer.

[Tracking bug #41370769](https://issues.chromium.org/issues/41370769) | [ChromeStatus.com entry](https://chromestatus.com/feature/5686378455105536) | [Spec](https://www.w3.org/TR/webrtc)

## Web APIs

### Intl.DurationFormat

Provides a method of formatting durations, for example "1 hr 40 min 30 sec" that supports multiple locales.

[MDN Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DurationFormat) | [Tracking bug #42201655](https://issues.chromium.org/issues/42201655) | [ChromeStatus.com entry](https://chromestatus.com/feature/5193021205774336) | [Spec](https://tc39.es/proposal-intl-duration-format)

### Snap Events

Snap Events allow developers reliably listen for when the "snap target" of a scroller changes and perform style adjustments as selected.

[Scroll snap events](/blog/scroll-snap-events) | [Tracking bug #40273052](https://issues.chromium.org/issues/40273052) | [ChromeStatus.com entry](https://chromestatus.com/feature/5826089036808192) | [Spec](https://drafts.csswg.org/css-scroll-snap-2#snap-events)

### Private Aggregation API: client-side contribution merging

Modifies the Private Aggregation API to merge histogram contributions with the same bucket and filtering ID before embedding in the aggregatable report's encrypted payload.

Private Aggregation imposes a limit on the number of contributions that can be embedded in a single aggregatable report, with any additional contributions being dropped. By merging together contributions where possible, we can get additional utility out of the limit. Note that, ignoring the dropping of excess contributions, merging these sorts of contributions shouldn't have any impact on the final outputs, for example summary reports.

[Tracking bug #349980058](https://issues.chromium.org/issues/349980058) | [ChromeStatus.com entry](https://chromestatus.com/feature/5094168719523840) | [Spec](https://github.com/patcg-individual-drafts/private-aggregation-api/pull/136)

### `scheduler.yield()`

Provides a method for yielding control to the browser, which can be used to break up long tasks. Awaiting the promise returned by `scheduler.yield()` causes the current task to yield, continuing in a new browser task. This can be used to improve responsiveness issues caused by long tasks. Continuations are prioritized to mitigate performance problems of existing alternatives.

[Docs](https://web.dev/articles/optimize-long-tasks#scheduler-dot-yield) | [Tracking bug #40633887](https://issues.chromium.org/issues/40633887) | [ChromeStatus.com entry](https://chromestatus.com/feature/6266249336586240) | [Spec](https://wicg.github.io/scheduling-apis/#dom-scheduler-yield)

### Web Authentication API: JSON serialization methods

The WebAuthn `PublicKeyCredential.toJSON()`, `parseCreationOptionsFromJSON()`, and `parseRequestOptionsFromJSON()` methods let developers serialize a WebAuthn response into a JSON object or deserialize a WebAuthn request object from its JSON representation.

[Tracking bug #40250593](https://issues.chromium.org/issues/40250593) | [ChromeStatus.com entry](https://chromestatus.com/feature/5141695044255744) | [Spec](https://w3c.github.io/webauthn/#publickeycredential)

## Rendering and graphics

### WebGPU extended range (HDR) support

Adds tone mapping parameters to the WebGPU canvas configuration, and adds options of `standard` (the current behavior of restricting content to the SDR range of the display) as the default, and `extended` (not imposing this restriction) as a new behavior. This allows WebGPU content to use the full range of a display.

[Demo](https://ccameron-chromium.github.io/webgpu-hdr/example.html) | [Tracking bug #333967627](https://issues.chromium.org/issues/333967627) | [ChromeStatus.com entry](https://chromestatus.com/feature/6196313866895360) | [Spec](https://github.com/ccameron-chromium/webgpu-hdr/blob/main/EXPLAINER.md)

## WebGPU

  * [ Blog ](https://developer.chrome.com/blog)

#  What's New in WebGPU (Chrome 129)

Stay organized with collections  Save and categorize content based on your preferences. 

![François Beaufort](https://web.dev/images/authors/beaufortfrancois.jpg)

François Beaufort 

[ GitHub ](https://github.com/beaufortfrancois)

### HDR support with canvas tone mapping mode

Web developers have limited options for delivering HDR content, relying primarily on `<img>` and `<video>` elements. The `<canvas>` element, however, remains restricted to SDR. Generating dynamic HDR content within a canvas requires encoding its contents as an HDR image before displaying it (for an example see this [demo](https://gkjohnson.github.io/three-gpu-pathtracer/example/bundle/hdr.html)).

The new [`GPUCanvasToneMappingMode`](https://www.w3.org/TR/webgpu/#gpucanvastonemappingmode) parameter in the WebGPU canvas configuration now allows WebGPU to draw colors brighter than white (`#FFFFFF`). It does so through the following modes:

  * `"standard"`: The default behavior restricts content to the SDR range of the screen. This mode is accomplished by clamping all color values in the color space of the screen to the `[0, 1]` interval.

  * `"extended"`: Unlocks the full HDR range of the screen. This mode matches `"standard"` in the `[0, 1]` range of the screen. Clamping or projection is done to the extended dynamic range of the screen but not `[0, 1]`.

The following code snippet shows you to configure a canvas for high dynamic range.
    
    
    const adapter = await navigator.gpu.requestAdapter();
    const device = await adapter.requestDevice();
    
    const canvas = document.querySelector("canvas");
    const context = canvas.getContext("webgpu");
    
    context.configure({
      device,
      format: "rgba16float",
      toneMapping: { mode: "extended" },
    });
    

Explore HDR with WebGPU by checking out the [Particles (HDR) sample](https://webgpu.github.io/webgpu-samples/?sample=particles) and [WebGPU HDR example](https://ccameron-chromium.github.io/webgpu-hdr/example.html), and see the [chromestatus entry](https://chromestatus.com/feature/6196313866895360).

![A laptop with an HDR screen displaying a vibrant image.](/static/blog/new-in-webgpu-129/image/particles.jpg) The Particles (HDR) sample displayed on a HDR screen.

### Expanded subgroups support

Following the announcement of [subgroups experimentation](/blog/new-in-webgpu-128#experimenting_with_subgroups), the subgroup built-ins functions are now available for use in both compute shaders and fragment shaders. They are no longer restricted to just compute shaders. See [issue 354738715](https://issues.chromium.org/issues/354738715).

Note that the `subgroup_size` built-in value is currently [buggy](https://issues.chromium.org/issues/361593660) in fragment shaders. Avoid it for now.

Furthermore, the following subgroup built-ins functions have been added:

  * `subgroupAdd(value)`: Returns the summation of all active invocations `value`s across the subgroup.
  * `subgroupExclusiveAdd(value)`: Returns the exclusive scan summation of all active invocations `value`s across the subgroup.
  * `subgroupMul(value)`: Returns the multiplication of all active invocations `value`s across the subgroup.
  * `subgroupExclusiveMul(value)`: Returns the exclusive scan multiplication of all active invocations `value`s across the subgroup.   
  

  * `subgroupAnd(value)`: Returns the binary AND of all active invocations `value`s across the subgroup.
  * `subgroupOr(value)`: Returns the binary OR of all active invocations `value`s across the subgroup.
  * `subgroupXor(value)`: Returns the binary XOR of all active invocations `value`s across the subgroup.   
  

  * `subgroupMin(value)`: Returns the minimal value of all active invocations `value`s across the subgroup.
  * `subgroupMax(value)`: Returns the maximal value of all active invocations `value`s across the subgroup.   
  

  * `subgroupAll(value)`: Returns true if `value` is true for all active invocations in the subgroup.
  * `subgroupAny(value)`: Returns true if `value` is true for any active invocation in the subgroup.   
  

  * `subgroupElect()`: Returns true if this invocation has the lowest `subgroup_invocation_id` among active invocations in the subgroup.
  * `subgroupBroadcastFirst(value)`: Broadcasts `value` from the active invocation with the lowest `subgroup_invocation_id` in the subgroup to all other active invocations.   
  

  * `subgroupShuffle(value, id)`: Returns `value` from the active invocation whose `subgroup_invocation_id` matches `id`.
  * `subgroupShuffleXor(value, mask)`: Returns `value` from the active invocation whose `subgroup_invocation_id` matches `subgroup_invocation_id ^ mask`. `mask` must be dynamically uniform.
  * `subgroupShuffleUp(value, delta)`: Returns `value` from the active invocation whose `subgroup_invocation_id` matches `subgroup_invocation_id - delta`.
  * `subgroupShuffleDown(value, delta)`: Returns `value` from the active invocation whose `subgroup_invocation_id` matches `subgroup_invocation_id + delta`.   
  

  * `quadBroadcast(value, id)`: Broadcasts `value` from the quad invocation with id equal to `id`. `id` must be a constant-expression.
  * `quadSwapX(value)`: Swaps `value` between invocations in the quad in the X direction.
  * `quadSwapY(value)`: Swaps `value` between invocations in the quad in the Y direction.
  * `quadSwapDiagonal(value)`: Swaps `value` between invocations in the quad diagonally.

### Dawn updates

The `wgpu::PrimitiveState` struct now directly includes depth clip control setting, eliminating the need for a separate `wgpu::PrimitiveDepthClipControl` struct. To learn more, see the following code snippet and the [webgpu-headers PR](https://github.com/webgpu-native/webgpu-headers/pull/311).
    
    
    // Before
    wgpu::PrimitiveState primitive = {};
    wgpu::PrimitiveDepthClipControl depthClipControl;
    depthClipControl.unclippedDepth = true;
    primitive.nextInChain = &depthClipControl;
    
    
    
    // Now
    wgpu::PrimitiveState primitive = {};
    primitive.unclippedDepth = true;
    

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/6613..chromium/6668?n=1000).

## Origin trials

### FileSystemObserver interface

The FileSystemObserver interface notifies websites of changes to the file system. Sites observe changes to files and directories in the user's local device (as specified in WICG/file-system-access) or in the Bucket File System (as specified in whatwg/fs), and are notified of basic change info, such as the change type.

[Docs](https://docs.google.com/document/d/1d6YoPvk0rdNBQaZcoFP-V5u4CBjgahvmnVsZpbn0Gmo/edit?usp=sharing) | [Tracking bug #40105284](https://issues.chromium.org/issues/40105284) | [ChromeStatus.com entry](https://chromestatus.com/feature/4622243656630272) | [Spec](https://github.com/whatwg/fs/pull/165)

### Mesh2D Canvas API

A high-performance Canvas 2D triangle mesh API that can be used to batch-render a large number of textured triangles.

This will enable advanced texture mapping and geometry deformation effects in a 2D context.

[Demo](https://demos.skia.org/demo/mesh2d) | [Tracking bug #40282920](https://issues.chromium.org/issues/40282920) | [ChromeStatus.com entry](https://chromestatus.com/feature/6247948082216960) | [Spec](https://github.com/fserb/canvas2D/blob/master/spec/mesh2d.md)

## Deprecations and removals

### Deprecate 0.0.0.0 for Private Network Access

Chrome will block access to IP address `0.0.0.0` in advance of Private Network Access (PNA) completely rolling out.

Chrome is deprecating direct access to private network endpoints from public websites as part of the [PNA specification](/blog/private-network-access-preflight). Services listening on localhost (`127.0.0.0/8`) are considered private according to the specification. Chrome's PNA protection can be bypassed using the IP address `0.0.0.0` to access services listening on the localhost on macOS and Linux.

This can also be abused in DNS rebinding attacks targeting a web application listening on the localhost.

This release of Chrome removes three features.

[ChromeStatus.com entry](https://chromestatus.com/feature/5106143060033536) | [Spec](https://wicg.github.io/private-network-access)

### Remove the includeShadowRoots argument on DOMParser

The `includeShadowRoots` argument was a never-standardized argument to the `DOMParser.parseFromString()` function, which was there to allow imperative parsing of HTML content that contains declarative shadow DOM. This was shipped in Chrome 90 as part of the initial shipment of declarative shadow DOM.

Now that a standardized version of this feature is available with the `setHTMLUnsafe()` and `parseHTMLUnsafe()` methods, the non-standard `includeShadowRoots` argument will be removed. Code should be updated as follows:

Instead of:
    
    
    ((new DOMParser()).parseFromString(html,'text/html',{includeShadowRoots: true});
    

Use:
    
    
    Document.parseHTMLUnsafe(html);
    

[Tracking bug #329330085](https://issues.chromium.org/issues/329330085) | [ChromeStatus.com entry](https://chromestatus.com/feature/5116094370283520)

### Remove non-standard declarative shadow DOM serialization

The prototype implementation of declarative shadow DOM contained a method called `getInnerHTML()` used to serialize DOM trees containing shadow roots. That part of the prototype was not standardized with the rest of declarative shadow dom, and instead a replacement was designed—`getHTML()`.

Therefore the old `getInnerHTML()` method is now being removed from Chrome, you should use [`getHTML()`](https://developer.mozilla.org/docs/Web/API/Element/getHTML) as a replacement, which will soon be interoperable across browsers.

[Tracking bug #41492947](https://issues.chromium.org/issues/41492947) | [ChromeStatus.com entry](https://chromestatus.com/feature/5081733588582400)

### Remove PointerEvent.getCoalescedEvents() from insecure contexts

The Pointer Events Working Group made `PointerEvent.getCoalescedEvents()` restricted to secure contexts over four years ago, which removed the API from insecure contexts. Chrome originally shipped the old behavior and didn't follow the spec change immediately because of compat concerns.

We are now removing it from insecure contexts because Chrome usage in insecure contexts turned out to be very low.

[Tracking bug #40928769](https://issues.chromium.org/issues/40928769) | [ChromeStatus.com entry](https://chromestatus.com/feature/4941651093749760)

## Further reading

Looking for more? Check out these additional resources.

  * [What's new in Chrome 129](/blog/new-in-chrome-129)
  * [What's new in Chrome DevTools 129](/blog/new-in-devtools-129)
  * [ChromeStatus.com updates for Chrome 129](https://chromestatus.com/features#milestone%3D129)
  * [Chrome release calendar](https://chromiumdash.appspot.com/schedule)
  * [Upcoming deprecations](https://chromestatus.com/features#browsers.chrome.status%3A%22Deprecated%22)
  * [Upcoming removals](https://chromestatus.com/features#browsers.chrome.status%3A%22Removed%22)

## Download Google Chrome

Download Chrome for [Android](https://play.google.com/store/apps/details?id=com.android.chrome), [Desktop](https://www.google.com/chrome/), or [iOS](https://apps.apple.com/us/app/google-chrome/id535886823). 

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2024-09-17 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2024-09-17 UTC."],[],[]] 
