# Chrome 127 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/127

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Docs ](https://developer.chrome.com/docs)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 127

Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** July 23rd, 2024

Unless otherwise noted, the following changes apply to Chrome 127 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 127](/blog/new-in-chrome-127). 

## CSS

### CSS font-size-adjust

The [`font-size-adjust`](https://developer.mozilla.org/docs/Web/CSS/font-size-adjust) CSS property provides a way to modify the size of lowercase letters relative to the size of uppercase letters, which defines the overall font-size. This property is useful for situations where font fallback can occur.

Chrome 127 includes the two value syntax to pass in a font metric and a value.

[Tracking bug #451346](https://issues.chromium.org/issues/451346) | [ChromeStatus.com entry](https://chromestatus.com/feature/5720910061371392) | [Spec](http://www.w3.org/TR/css-fonts-3/#propdef-font-size-adjust)

### Multi-argument alt text in CSS Generated Content

The CSS `content` property lets you specify alternative text for accessibility with the following syntax: `css .has-before-content::before { content: url("cat.jpg") / "A cute cat"; }`

This functionality, where the alt text is given by a single string, is already supported in Chrome. From Chrome 127 the alt text can be given by an arbitrary number of elements, which in addition to strings can be `attr()` functions or counters. For example:
    
    
    .has-before-content::before {
      content: url("cat.jpg") / "A cute " attr(data-animal);
    }
    

Note that this feature entry doesn't include the addition of counter support.

[ChromeStatus.com entry](https://chromestatus.com/feature/5168344402755584) | [Spec](https://www.w3.org/TR/css-content-3/#valdef-content---string--counter)

### Support for the View Transition API in iframes

From Chrome 127 concurrent same-document view transitions in a main frame and same-origin iframe will be available.

Previously, running a view transition using the `document.startViewTransition` in a same-origin iframe wouldn't work if the main frame was running a transition at the same time. The iframe's transition would be automatically skipped. Now, both transitions will execute.

View transitions on same-origin cross-document navigations in an iframe will also be supported.

### Text size adjust improvements

The `text-size-adjust` property adjusts font sizes on mobile devices. Values other than `auto` disable automatic text size adjustments. Percentage values increase the computed size of text.

This makes `text-size-adjust` more consistent, so it works like a direct multiplier of the font size (and line height). The major changes are:

  * `text-size-adjust` works with or without a meta viewport.
  * Values other than `auto` disable all automatic text size adjustments.
  * Percentages apply directly, without any heuristics.
  * Layout bugs are fixed.

[Tracking bug #340389272](https://issues.chromium.org/issues/340389272) | [ChromeStatus.com entry](https://chromestatus.com/feature/5111875942744064) | [Spec](https://drafts.csswg.org/css-size-adjust/#propdef-text-size-adjust)

## Web APIs

### Automatic fullscreen content setting

A new "automatic fullscreen" content setting lets enterprise admins allow sites to enter fullscreen without a user gesture. Users may also allow Isolated Web Apps to use this feature through site settings pages.

Combined with the Window Management permission and unblocked popups, this unlocks valuable fullscreen capabilities:

  * Open a fullscreen popup on another display, from one gesture.
  * Show fullscreen content on multiple displays from one gesture.
  * Show fullscreen content on a new display, when it's connected.
  * Swap fullscreen windows between displays with one gesture.
  * Show fullscreen content after user gesture expiry or consumption.

[Demo](https://github.com/michaelwasserman/iwa-windowing-example) | [Tracking bug #1501130](https://issues.chromium.org/issues/1501130) | [ChromeStatus.com entry](https://chromestatus.com/feature/6218822004768768)

### WebGPU: GPUAdapter `info` attribute

Adds a synchronous GPUAdapter info attribute to retrieve the same information about the physical adapter as with the asynchronous GPUAdapter `requestAdapterInfo()` method.

[Tracking bug #335383516](https://issues.chromium.org/issues/335383516) | [ChromeStatus.com entry](https://chromestatus.com/feature/5087914701881344) | [Spec](https://gpuweb.github.io/gpuweb/#dom-gpuadapter-info)

## Media

### Video chapter in `MediaMetadata`

You can now [add individual chapter information](https://web.dev/articles/media-session#:%7E:text=add%20also%20individual-,chapter%20information,-%2C%20such%20as%20the), such as the title of the section, its timestamp, and a screenshot image to media metadata. This allows users to navigate through the content of the media.

This will currently only show up in ChromeOS media notifications, and not in Chrome Browser global media controls.

[Demo](https://googlechrome.github.io/samples/media-session/video.html) | [ChromeStatus.com entry](https://chromestatus.com/feature/6682585059295232) | [Spec](https://www.w3.org/TR/mediasession/#the-chapterinformation-interface/)

### Document picture-in-picture: propagate user activation

This makes user activations in a document picture-in-picture window usable inside its opener window and the other way around. This makes it more ergonomic to use user-activation-gated APIs, since often event handlers in the document picture-in-picture window are actually run in the opener's context, so the opener's context needs access to the user gesture.

[Demo](https://steimelchrome.github.io/document-pip/user-gesture.html) | [Tracking bug #331246719](https://issues.chromium.org/issues/331246719) | [ChromeStatus.com entry](https://chromestatus.com/feature/5185710702460928)

## JavaScript

### Importmap integrity

Imported ES modules can't currently have their integrity checked, and hence cannot run in environments that require Subresource Integrity or with `require-sri-for` CSP directives.

This feature adds an `integrity` section to import maps, enabling developers to map ES module URLs to their integrity metadata, and ensure they only load when they match their expected hashes.

[Tracking bug #334251999](https://issues.chromium.org/issues/334251999) | [ChromeStatus.com entry](https://chromestatus.com/feature/5157245026566144)

### Snap Events

Snap Events allow developers to reliably listen for when the _snap target_ of a scroller changes and perform style adjustments as desired.

CSS scroll snap points are often used as a mechanism to create scroll interactive selection components, where selection is determined with JavaScript intersection observers and a scroll end guesstimate. By creating built-in events, the invisible state will become actionable, at the right time, and always correct.

This feature adds two JavaScript events: `scrollsnapchange` and `scrollsnapchanging`. The `scrollsnapchange` event lets developers know, at the completion of a scroll operation (including snapping), that the element to which a scroller is snapped has changed. The `scrollsnapchanging` event gives developers a hint, during a scroll operation, that the user agent intends to snap the scroll container to a new snap target based on the scrolling input so far.

## Privacy

### Aggregate Debug Reporting in Attribution Reporting API

This change is so the API can continue to provide some form of debugging information after third-party cookie deprecation. This is a new report type that is not tied to third-party cookies and provides similar debug information. This feature allows API callers to request and receive debug signals in aggregate form. This feature is very similar to current Aggregate Reports supported by the API, except these new reports will be specifically for debug signals.

[ChromeStatus.com entry](https://chromestatus.com/feature/5086433709916160) | [Spec](https://wicg.github.io/attribution-reporting-api/#aggregatable-debug-reporting-config)

## Accessibility

### Keyboard focusable scroll containers

This feature introduces the following changes:

Scrollers are click-focusable and programmatically-focusable by default. Scrollers without focusable children are keyboard-focusable by default.

This is an important improvement to help make scrollers and contents within scrollers more accessible to all users. You can read more about its benefits in the post [Keyboard focusable scrollers](/blog/keyboard-focusable-scrollers). Keyboard focusable scrollers will be enabled by default starting in Chrome 127. If websites need time to adjust to this new feature, there are a few options:

  * The [Keyboard focusable scrollers opt out deprecation trial](/origintrials#/view_trial/2455024746870341633\)) can be used to opt back out of the feature for a limited time on a given site. This can be used through Chrome 132, ending March 18, 2025.
  * The [KeyboardFocusableScrollersEnabled enterprise policy](https://chromeenterprise.google/policies/#KeyboardFocusableScrollersEnabled) will be available in Chrome 127, and can be used for the same purpose.

[Keyboard focusable scrollers](/blog/keyboard-focusable-scrollers) | [Tracking bug #1040141](https://issues.chromium.org/issues/1040141) | [ChromeStatus.com entry](https://chromestatus.com/feature/5231964663578624) | [Spec](https://drafts.csswg.org/css-overflow-3/#scroll-container)

## Loading

### `No-Vary-Search` support for prerender

Extends `No-Vary-Search` support to prerender on top of [the previous prefetch support](/docs/web-platform/prerender-pages#no-vary-search). This enables a prerender entry to match even if certain URL query parameters change. The No-Vary-Search HTTP response header declares that some or all parts of a URL's query can be ignored for cache matching purposes.

[Tracking bug #41494389](https://issues.chromium.org/issues/41494389) | [ChromeStatus.com entry](https://chromestatus.com/feature/5099218903760896) | [Spec](https://wicg.github.io/nav-speculation/no-vary-search.html)

## WebGPU

  * [ Blog ](https://developer.chrome.com/blog)

#  What's New in WebGPU (Chrome 127)

Stay organized with collections  Save and categorize content based on your preferences. 

![François Beaufort](https://web.dev/images/authors/beaufortfrancois.jpg)

François Beaufort 

[ GitHub ](https://github.com/beaufortfrancois)

### Experimental support for OpenGL ES on Android

You can now access a `GPUAdapter` from the OpenGL ES backend when requesting the experimental [WebGPU compatibility mode](/blog/new-in-webgpu-122#expand_reach_with_compatibility_mode_feature_in_development) in Chrome for Android. This is especially useful for Android devices lacking support for Vulkan 1.1 or greater. See the following example and [issue dawn:1545](https://bugs.chromium.org/p/dawn/issues/detail?id=1545).
    
    
    // Request a GPUAdapter in compatibility mode
    const adapter = await navigator.gpu.requestAdapter({ compatibilityMode: true });
    

![WebGPU report page shows GPUAdapter info from the OpenGL ES backend on Android device.](/static/blog/new-in-webgpu-127/image/opengl-es-android.jpg) OpenGL ES adapter info in [webgpureport.org](https://webgpureport.org)

As this feature is still in an experimental stage, you will need to perform the following steps:

  1. Enable the following Chrome flags: "Unsafe WebGPU Support", "WebGPU Developer Features", and "Enable command line on non-rooted devices".
  2. Enable USB Debugging on your Android Device.
  3. Connect your Android device to your workstation, run `adb shell 'echo "_ --use-webgpu-adapter=opengles" > /data/local/tmp/chrome-command-line'` to prefer the OpenGL ES backend over Vulkan, and restart Chrome.

### GPUAdapter info attribute

Getting identifying information about an adapter can now be done in a synchronous way with the GPUAdapter `info` attribute. Previously, calling the asynchronous GPUAdapter `requestAdapterInfo()` method was the only way to get adapter info. However, `requestAdapterInfo()` has been removed from the WebGPU spec and will be removed in Chrome later this year to give enough time to web developers to make the necessary transition. See the following example, [Chrome Status](https://chromestatus.com/feature/5087914701881344), and [issue 335383516](https://issues.chromium.org/issues/335383516).
    
    
    const adapter = await navigator.gpu.requestAdapter();
    const info = adapter.info;
    
    // During the transition period, you can use the following:
    // const info = adapter.info || await adapter.requestAdapterInfo();
    
    console.log(`Vendor: ${info.vendor}`); // "arm"
    console.log(`Architecture: ${info.architecture}`); // "valhall"
    

### WebAssembly interop improvements

To accommodate for WebAssembly heaps being passed directly to WebGPU, the sizes of the following BufferSource arguments are no longer restricted to 2 GB: `dynamicOffsetsData` in [`setBindGroup()`](https://gpuweb.github.io/gpuweb/#dom-gpubindingcommandsmixin-setbindgroup-index-bindgroup-dynamicoffsetsdata-dynamicoffsetsdatastart-dynamicoffsetsdatalength-dynamicoffsetsdata), source `data` in [`writeBuffer()`](https://gpuweb.github.io/gpuweb/#dom-gpuqueue-writebuffer), and source `data` Pin [`writeTexture()`](https://gpuweb.github.io/gpuweb/#dom-gpuqueue-writetexture). See [issue 339049388](https://issues.chromium.org/issues/339049388).

### Improved command encoder errors

Some validation errors raised from command encoders will now have improved contextual information. For example, attempting to start a compute pass while a render pass was still open resulted in the following error.
    
    
    Command cannot be recorded while [CommandEncoder (unlabeled)] is locked and [RenderPassEncoder (unlabeled)] is currently open.
        at CheckCurrentEncoder (..\..\third_party\dawn\src\dawn\native\EncodingContext.h:106)
    

This does describe the reason for the error, however it doesn't indicate which call actually caused the validation error. The following error shows the improved messaging which includes the command that triggered the error. See [change 192245](https://dawn-review.googlesource.com/c/dawn/+/192245).
    
    
    Command cannot be recorded while [CommandEncoder (unlabeled)] is locked and [RenderPassEncoder (unlabeled)] is currently open.
     - While encoding [CommandEncoder (unlabeled)].BeginComputePass([ComputePassDescriptor]).
    

### Dawn updates

The [webgpu.h](https://github.com/webgpu-native/webgpu-headers/blob/main/webgpu.h) C API no longer exposes `wgpuSurfaceGetPreferredFormat()`, the C equivalent of Dawn's `wgpu::Surface::GetPreferredFormat()`. Instead, use `wgpu::Surface::GetCapabilities()` to get the list of supported formats, then use `formats[0]` to get the texture format preferred for this surface. In the meantime, calling `wgpu::Surface::GetPreferredFormat()` emits a deprecation warning. See [issue 290](https://github.com/webgpu-native/webgpu-headers/issues/290).

The supported texture usages of a surface are now available through `wgpu::SurfaceCapabilities::usages` when calling `wgpu::Surface::GetCapabilities()`. They are expected to always include `wgpu::TextureUsage::RenderAttachment`. See [issue 301](https://github.com/webgpu-native/webgpu-headers/pull/301).

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/6478..chromium/6533?n=1000).

## New origin trials

### Compression dictionary transport with Shared Brotli and Shared Zstandard

This feature adds support for using designated previous responses, as an external dictionary for HTTP responses that compress Brotli or Zstandard.

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/3693514644397228033) | [Demo](https://compression-dictionary-transport-shop-demo.glitch.me) | [Tracking bug #1413922](https://issues.chromium.org/issues/1413922) | [ChromeStatus.com entry](https://chromestatus.com/feature/5124977788977152) | [Spec](https://github.com/WICG/compression-dictionary-transport)

### Deprecate third-party cookies

We intend to deprecate and remove default access to third-party cookies (also known as cross-site cookies), starting with an initial 1% testing period in Q1 2024, followed by a gradual phaseout planned to begin in Q1 2025, subject to addressing any remaining competition concerns of the UK's Competition and Markets Authority.

[Phasing out third-party cookies](https://goo.gle/3pcd) is a central effort to the Privacy Sandbox initiative, which aims to responsibly reduce cross-site tracking on the web (and beyond) while supporting key use cases through new technologies.

[Demo](https://compression-dictionary-transport-shop-demo.glitch.me) | [ChromeStatus.com entry](https://chromestatus.com/feature/5133113939722240) | [Spec](https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis-12#name-the-cookie-header-field)

### Partitioning storage, service workers, and communication APIs

From Chrome 115, storage, service workers, and communication APIs are partitioned in third-party contexts. From Chrome 113 to 126, sites were able to take part in a deprecation trial to temporarily unpartition and restore prior behavior of storage, service workers, and communication APIs.

From Chrome 125, non-cookie storage in the Storage Access API is supported, which should address the majority of use cases for unpartitioned storage. Where those use cases aren't met, it is now possible to request a renewal for the DisableThirdPartyStoragePartitioning deprecation trial for an additional 6 milestones, for users on Chrome 127 to 132 (inclusive).

See the [Storage Partitioning deprecation trial renewal blog post](https://developers.google.com/privacy-sandbox/blog/storage-partitioning-deprecation-trial-renewal) for more information.

[Tracking bug #1191114](https://issues.chromium.org/issues/1191114) | [ChromeStatus.com entry](https://chromestatus.com/feature/5723617717387264)

### Keyboard focusable scroll containers deprecation trial

This feature introduces the following changes:

Scrollers are click-focusable and programmatically-focusable by default. Scrollers without focusable children are keyboard-focusable by default.

We attempted to ship these changes, and found that a limited number of sites had broken expectations around some of their components. As a result, we had to unship the feature to avoid this breakage. Given the benefits mentioned above, the feature will begin shipping in 127. To allow more time for the affected sites to migrate their components, we are starting a Deprecation Trial. When enabled, this will disable the KeyboardFocusableScrollers feature.

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/2455024746870341633) | [Keyboard focusable scrollers](/blog/keyboard-focusable-scrollers) | [Tracking bug #1040141](https://issues.chromium.org/issues/1040141) | [ChromeStatus.com entry](https://chromestatus.com/feature/5231964663578624) | [Spec](https://drafts.csswg.org/css-overflow-3/#scroll-container)

## Deprecations and removals

This version of Chrome introduces the deprecations and removals listed below. Visit ChromeStatus.com for lists of planned deprecations, current deprecations and previous removals.

This release of Chrome removes three features.

### Mutation events

Mutation event support will be disabled by default starting in Chrome 127. Code should be migrated before that date to avoid site breakage. If more time is needed, there are a few options:

  * The Mutation Events deprecation trial (https://developer.chrome.com/origintrials/#/view_trial/919297273937002497) can be used to re-enable the feature for a limited time on a given site. This can be used through Chrome 134, ending March 25, 2025.
  * The [MutationEventsEnabled enterprise policy](https://chromeenterprise.google/policies/#MutationEventsEnabled) can be used for the same purpose, also through Chrome 134.

See the blog post [Mutation events deprecation](/blog/mutation-events-deprecation) for more details.

[Tracking bug #40268638](https://issues.chromium.org/issues/40268638) | [ChromeStatus.com entry](https://chromestatus.com/feature/5083947249172480) | [Spec](https://w3c.github.io/uievents/#legacy-event-types)

### Restrict "private network requests" for subresources from public websites to secure contexts

Requires that private network requests for subresources from public websites may only be initiated from a secure context. Examples include internet to intranet requests and internet to loopback requests.

This is a first step towards fully implementing [Private Network Access](https://wicg.github.io/private-network-access/).

[Tracking bug #986744](https://issues.chromium.org/issues/986744) | [ChromeStatus.com entry](https://chromestatus.com/feature/5436853517811712) | [Spec](https://wicg.github.io/private-network-access)

### Remove old CSS custom state syntax

The CSS custom state pseudo-class is being renamed from `:--foo` to `:state(foo)`. The new syntax, `:state(foo)`, has been enabled by default, therefore we are removing the `:--foo` syntax.

Firefox and Safari never implemented the old syntax and they have both shipped the new syntax.

Enterprise customers who need more time can use the `CSSCustomStateDeprecatedSyntaxEnabled` policy. This policy will be removed in Chrome 131.

[Tracking bug #41486953](https://issues.chromium.org/issues/41486953) | [ChromeStatus.com entry](https://chromestatus.com/feature/5140610730426368)

## Further reading

Looking for more? Check out these additional resources.

  * [What's new in Chrome 127](/blog/new-in-chrome-127)
  * [What's new in Chrome DevTools 127](/blog/new-in-devtools-127)
  * [ChromeStatus.com updates for Chrome 127](https://chromestatus.com/features#milestone%3D127)
  * [Chrome release calendar](https://chromiumdash.appspot.com/schedule)
  * [Upcoming deprecations](https://chromestatus.com/features#browsers.chrome.status%3A%22Deprecated%22)
  * [Upcoming removals](https://chromestatus.com/features#browsers.chrome.status%3A%22Removed%22)

## Download Google Chrome

Download Chrome for [Android](https://play.google.com/store/apps/details?id=com.android.chrome), [Desktop](https://www.google.com/chrome/), or [iOS](https://apps.apple.com/us/app/google-chrome/id535886823). 

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2024-07-23 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2024-07-23 UTC."],[],[]] 
