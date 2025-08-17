# Chrome 138 Release Notes

**Stable release date:** June 24th, 2025

Unless otherwise noted, the following changes apply to Chrome 138 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. Want just the highlights? Check out [New in Chrome 138](https://developer.chrome.com/blog/new-in-chrome-138).

## CSS and UI

### CSS Sign-Related Functions: abs(), sign()

The sign-related functions `abs()` and `sign()` compute various functions related to the sign of their argument. The `abs(A)` function contains one calculation A, and returns the absolute value of A, as the same type as the input: if A's numeric value is positive or 0⁺, just A again; otherwise -1 * A. The `sign(A)` function contains one calculation A, and returns -1 if A's numeric value is negative, +1 if A's numeric value is positive, 0⁺ if A's numeric value is 0⁺, and 0⁻ if A's numeric value is 0⁻. The return type is a `<number>`, made consistent with the type of the input calculation.

**References:** [MDN Docs:abs()](https://developer.mozilla.org/docs/Web/CSS/abs) | [Tracking bug #40253181](https://bugs.chromium.org/p/chromium/issues/detail?id=40253181) | [ChromeStatus.com entry](https://chromestatus.com/feature/5196860094464000) | [Spec](https://www.w3.org/TR/css-values-4/#sign-funcs)

### Interpolation progress functional notation: CSS progress() function

The `progress()` functional notation returns a `<number>` value representing the position of one calculation (the progress value) between two other calculations (the progress start value and progress end value). The `progress()` function is a math function.

**References:** [Tracking bug #40944203](https://bugs.chromium.org/p/chromium/issues/detail?id=40944203) | [ChromeStatus.com entry](https://chromestatus.com/feature/5096136905244672) | [Spec](https://www.w3.org/TR/css-values-5/#progress-notation)

### CSS sibling-index() and sibling-count()

The `sibling-index()` and `sibling-count()` functions can be used as integers in CSS property values to style elements based on their position among its siblings, or the total number of siblings respectively. These functions can be used directly as integer values, but more interestingly inside `calc()` expressions.

**References:** [Tracking bug #40282719](https://bugs.chromium.org/p/chromium/issues/detail?id=40282719) | [ChromeStatus.com entry](https://chromestatus.com/feature/5649901281918976) | [Spec](https://www.w3.org/TR/css-values-5/#sibling-functions)

### CSS stretch sizing keyword

A keyword for CSS sizing properties (for example, `width` and `height`) that lets elements grow to exactly fill their containing block's available space. It is similar to '100%', except the resulting size is applied to the element's margin box instead of the box indicated by `box-sizing`. Using this keyword lets the element keep its margins while still being as large as possible. An unprefixed version of `-webkit-fill-available`.

**References:** [Tracking bug #41253915](https://bugs.chromium.org/p/chromium/issues/detail?id=41253915) | [ChromeStatus.com entry](https://chromestatus.com/feature/5102457485459456) | [Spec](https://www.w3.org/TR/css-sizing-4/#valdef-width-stretch)

### CSS env variable for OS-level font scale

Exposes a user's preferred font scale to CSS. Without this, it's not practical for a page to detect if the user has changed their preferred font size using the Operating System's preferences. This CSS environment variable will reflect the scale chosen by the user.

**References:** [Tracking bug #397737223](https://bugs.chromium.org/p/chromium/issues/detail?id=397737223) | [ChromeStatus.com entry](https://chromestatus.com/feature/5106542883938304) | [Spec](https://www.w3.org/TR/css-env-1/#os-font-scale)

## Devices

### Web serial over Bluetooth on Android

This feature lets web pages and web apps connect to serial ports over Bluetooth on Android devices. Chrome on Android now supports Web Serial API over Bluetooth RFCOMM. Existing enterprise policies (`DefaultSerialGuardSetting`, `SerialAllowAllPortsForUrls`, `SerialAllowUsbDevicesForUrls`, `SerialAskForUrls` and `SerialBlockedForUrls`) on other platforms are enabled in future_on states for Android. All policies except `SerialAllowUsbDevicesForUrls` will be enabled after the feature is enabled. `SerialAllowUsbDevicesForUrls` will be enabled in a future launch after Android provides system level support of wired serial ports.

**References:** [Tracking bug #375245353](https://bugs.chromium.org/p/chromium/issues/detail?id=375245353) | [ChromeStatus.com entry](https://chromestatus.com/feature/5085754267189248) | [Spec](https://wicg.github.io/serial/)

### Viewport Segments Enumeration API

The Viewport Segments API allows developers to adapt their web layout to target foldable devices. The viewport segments defines the position and dimensions of a logically separate region of the viewport. Viewport segments are created when the viewport is split by one or more hardware features (such as a fold or a hinge between separate displays) that act as a divider; segments are the regions of the viewport that can be treated as logically distinct by the developer.

**References:** [Tracking bug #1039050](https://bugs.chromium.org/p/chromium/issues/detail?id=1039050) | [ChromeStatus.com entry](https://chromestatus.com/feature/5131631321964544) | [Spec](https://wicg.github.io/visual-viewport/)

## JavaScript

### Update QuotaExceededError to a DOMException derived interface

Previously, when the web platform wants to tell you when you've exceeded quota, it will use `DOMException` with the specific name property set to `QuotaExceededError`. However this does not allow carrying additional information. This proposes removing "QuotaExceededError" from the list of built-in DOMException names, and instead creates a class name `QuotaExceededError` from the list of built-in DOMException and has the additional optional properties `quota` and `requested`. We propose all instances of specs that throw "QuotaExceededError" `DOMException`s get upgraded to instead throw `QuotaExceededError`s. For now, such specs would leave the `quota` and `requested` properties at their default value of null, but they could eventually upgrade to include that data, if it's useful for their use case (and isn't, e.g., a privacy leak).

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5647993867927552) | [Spec](https://whatpr.org/dom/1245.html)

## Web APIs

### Translator API

A JavaScript API to provide language translation capabilities to web pages. Browsers are increasingly offering language translation to their users. Such translation capabilities can also be useful to web developers. This is especially the case when browser's built-in translation abilities cannot help. An enterprise policy (`GenAILocalFoundationalModelSettings`) is available to disable the underlying model downloading which would render this API unavailable.

**References:** [MDN Docs](https://developer.mozilla.org/docs/Web/API/Translator) | [Tracking bug #322229993](https://bugs.chromium.org/p/chromium/issues/detail?id=322229993) | [ChromeStatus.com entry](https://chromestatus.com/feature/5652970345332736) | [Spec](https://wicg.github.io/translation-api/)

### Language Detector API

A JavaScript API for detecting the language of text, with confidence levels. An important supplement to translation is language detection. This can be combined with translation, for example, taking user input in an unknown language and translating it to a specific target language. Browsers today often already have language detection capabilities, and we want to offer them to web developers through a JavaScript API, supplementing the translation API. An enterprise policy (`GenAILocalFoundationalModelSettings`) is available to disable the underlying model downloading which would render this API unavailable.

**References:** [MDN Docs](https://developer.mozilla.org/docs/Web/API/LanguageDetector) | [ChromeStatus.com entry](https://chromestatus.com/feature/5134901000871936) | [Spec](https://wicg.github.io/language-detection-api/)

### Summarizer API

Summarizer API is a JavaScript API for producing summaries of input text, backed by an AI language model. Browsers and operating systems are increasingly expected to gain access to a language model. By exposing this built-in model, we avoid every website needing to download their own multi-gigabyte language model, or send input text to third-party APIs. The summarizer API in particular exposes a high-level API for interfacing with a language model in order to summarize inputs for a variety of use cases, in a way that does not depend on the specific language model in question. An enterprise policy (`GenAILocalFoundationalModelSettings`) is available to disable the underlying model downloading which would render this API unavailable.

**References:** [MDN Docs](https://developer.mozilla.org/docs/Web/API/Summarizer) | [Tracking bug #351744634](https://bugs.chromium.org/p/chromium/issues/detail?id=351744634) | [ChromeStatus.com entry](https://chromestatus.com/feature/5134971702001664) | [Spec](https://wicg.github.io/summarization-api/)

### Escape < and > in attributes on serialization

Escape `<` and `>` in values of attributes on serialization. This mitigates the risk of mutation XSS attacks, which occur when value of an attribute is interpreted as a start tag token after being serialized and re-parsed.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5125509031477248) | [Spec](https://html.spec.whatwg.org/multipage/parsing.html#serializing-html-fragments)

### Crash Reporting API: is_top_level and visibility_state

This feature adds `is_top_level` and `visibility_state` string fields to the crash reporting API body that gets sent to the default reporting endpoint for crash reports.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5112885175918592) | [Spec](https://w3c.github.io/reporting/#crash-report)

### Fire the pushsubscriptionchange event upon resubscription

Fire the `pushsubscriptionchange` event in service workers when an origin for which a push subscription existed in the past, but which was revoked because of a permission change (from granted to deny/default), is re-granted notification permission. The event will be fired with an empty `oldSubscription` and `newSubscription`.

**References:** [Tracking bug #407523313](https://bugs.chromium.org/p/chromium/issues/detail?id=407523313) | [ChromeStatus.com entry](https://chromestatus.com/feature/5115983529336832) | [Spec](https://w3c.github.io/push-api/#the-pushsubscriptionchange-event)

## Multimedia

### Add support for video frame orientation metadata to WebCodecs

Introduces `rotation: int` and `flip: bool` values to various video related interfaces in WebCodecs so that developers can work with frame sources that have orientation (For example, Android cameras, certain media). The `VideoFrame` interface grows the ability to create VideoFrames with arbitrary rotation and flip as well as accessors for this information on the VideoFrame object. The `VideoDecoderConfig` object gains rotation and flip fields that are emitted on decoded VideoFrame objects automatically. The `VideoEncoder` class gains mechanisms for passing rotation and flip information from `encode()` to the VideoDecoderConfig emitted as part of `EncodedVideoChunkMetadata`. If `encode()` is called with frames with different orientations a nonfatal exception will be thrown. `configure()` may be used to reset the allowed orientation.

**References:** [Tracking bug #40243431](https://bugs.chromium.org/p/chromium/issues/detail?id=40243431) | [ChromeStatus.com entry](https://chromestatus.com/feature/5098495055380480) | [Spec](https://w3c.github.io/webcodecs/#videoframe-interface)

## Performance

### Add prefetchCache and prerenderCache to Clear-Site-Data header

Two new values for the Clear-Site-Data header to help developers target clearing the prerender and prefetch cache: "prefetchCache" and "prerenderCache".

**References:** [Tracking bug #398149359](https://bugs.chromium.org/p/chromium/issues/detail?id=398149359) | [ChromeStatus.com entry](https://chromestatus.com/feature/5110263659667456) | [Spec](https://w3c.github.io/webappsec-clear-site-data/#grammardef-cache-directive)

### Speculation rules: target_hint field

This extends speculation rules syntax to allow developers to specify the target_hint field. This field provides a hint to indicate a target navigable where a prerendered page will eventually be activated. For example, when `_blank` is specified as a hint, a prerendered page can be activated for a navigable opened by `window.open()`. The field has no effect on prefetching. The specification allows this field to accept any strings that are valid as navigable target name or keyword as the value, but this launch supports only one of "_self" or "_blank" strings. If the hint is not specified, it's treated like "_self" is specified.

**References:** [Tracking bug #40234240](https://bugs.chromium.org/p/chromium/issues/detail?id=40234240) | [ChromeStatus.com entry](https://chromestatus.com/feature/5084493854924800) | [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-target-hint)

## Security

### Integrity Policy for scripts

Subresource-Integrity (SRI) enables developers to make sure the assets they intend to load are indeed the assets they are loading. But there's no current way for developers to be sure that all of their scripts are validated using SRI. The Integrity-Policy header gives developers the ability to assert that every resource of a given type needs to be integrity-checked. If a resource of that type is attempted to be loaded without integrity metadata, that attempt will fail and trigger a violation report.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5104518463627264) | [Spec](https://w3c.github.io/webappsec-csp/#integrityPolicy)

## Service Worker

### ServiceWorker support for Speculation Rules Prefetch

This feature enables ServiceWorker-controlled prefetches, that is a speculation rules prefetch to URLs controlled by a Service Worker. Previously, the prefetch is cancelled upon detecting a controlling Service Worker, thus subsequent navigation to the prefetch target is served by the non-prefetch path. This feature will enable the prefetch request to go through the Service Worker's fetch handler and the response with the Service Worker interception is cached in the prefetch cache, resulting in a subsequent navigation being served by the prefetch cache. Use the enterprise policy `PrefetchWithServiceWorkerEnabled` to control this feature.

**References:** [Tracking bug #40947546](https://bugs.chromium.org/p/chromium/issues/detail?id=40947546) | [ChromeStatus.com entry](https://chromestatus.com/feature/5121066433150976) | [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-sw-integration)

## WebGPU

### Shorthand for Using Buffer as a Binding Resource

Developers can now use a `GPUBuffer` directly as a `GPUBindingResource`. This simplifies binding and makes it consistent with other binding types:

```javascript
const bindGroup = myDevice.createBindGroup({
  layout: myPipeline.getBindGroupLayout(0),
  entries: [
    { binding: 0, resource: mySampler },
    { binding: 1, resource: myTextureView },
    { binding: 2, resource: myExternalTexture },
    { binding: 3, resource: myBuffer }, // Simplified syntax
    { binding: 4, resource: { buffer: myOtherBuffer, offset: 42 } },
  ],
});
```

### Size Requirement Changes for Buffers Mapped at Creation

Creating a buffer with `mappedAtCreation: true` now throws a `RangeError` if the `size` is not a multiple of 4:

```javascript
myDevice.createBuffer({
  mappedAtCreation: true,
  size: 42, // This will now throw a RangeError
  usage: GPUBufferUsage.STORAGE,
});
```

### Architecture Report for Recent GPUs

New GPU architectures are now reported:
- Nvidia: `"blackwell"`
- AMD: `"rdna4"`

### Deprecation of GPUAdapter isFallbackAdapter Attribute

The `isFallbackAdapter` attribute for `GPUAdapter` is deprecated. It's replaced by the `GPUAdapterInfo.isFallbackAdapter` attribute introduced in Chrome 136.

### Dawn Updates

- Emscripten now supports Dawn GLFW for CMake builds
- A "remote" Emdawnwebgpu port is included in package releases
- Switching to Emdawnwebgpu is now a single flag change from `emcc -sUSE_WEBGPU` to `emcc --use-port=emdawnwebgpu`

## Deprecations and removals

### WebGPU: Deprecate GPUAdapter isFallbackAdapter attribute

Deprecates the `GPUAdapter` `isFallbackAdapter` boolean attribute from WebGPU, which is redundant with the `GPUAdapterInfo` `isFallbackAdapter` boolean attribute. This upcoming removal is a minor breaking change as support for fallback adapters has not yet been implemented in any browser, thereby resulting in both `isFallbackAdapter` attributes consistently returning a falsy value.

**References:** [Tracking bug #409259074](https://bugs.chromium.org/p/chromium/issues/detail?id=409259074) | [ChromeStatus.com entry](https://chromestatus.com/feature/5125671816847360) | [Spec](https://gpuweb.github.io/gpuweb/#gpu-adapter)

### Deprecate asynchronous range removal for Media Source Extensions

The Media Source standard long ago changed to disallow ambiguously defined behavior involving asynchronous range removals: `SourceBuffer.abort()` no longer aborts `SourceBuffer.remove()` operations. Setting `MediaSource.duration` can no longer truncate currently buffered media. Exceptions will be thrown in both of these cases now. Safari and Firefox have long shipped this behavior, Chromium is the last browser remaining with the old behavior. Use counters show that around 0.001%-0.005% of page loads hit the deprecated behavior. If a site hits this issue, playback may now break. Usage of `abort()` cancelling removals is increasing, so it's prudent to resolve this deprecation before more incompatible usage appears.

**References:** [Tracking bug #40474569](https://bugs.chromium.org/p/chromium/issues/detail?id=40474569) | [ChromeStatus.com entry](https://chromestatus.com/feature/5073717525970944) | [Spec](https://w3c.github.io/media-source/#dom-sourcebuffer-abort)

---

*Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.*

*Last updated 2025-06-24 UTC.*
