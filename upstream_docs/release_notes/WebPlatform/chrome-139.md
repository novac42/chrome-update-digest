# Chrome 139 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/139

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 139

Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** August 5th, 2025

Unless otherwise noted, the following changes apply to Chrome 139 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 139](/blog/new-in-chrome-139). 

## CSS and UI

### Short-circuiting `var()` and `attr()`

When the fallback is not taken, `var()` and `attr()` functions evaluate without looking for cycles in that fallback.

[ChromeStatus.com entry](https://chromestatus.com/feature/6212939656462336)

### Support `font-feature-settings` descriptor in `@font-face` rule

This feature supports the string-based syntax for `font-feature-settings` as defined in CSS Fonts Level 4. Invalid or unrecognized feature tags will be ignored per specification. No binary or non-standard forms are supported.

As OpenType fonts become more widely adopted, this enhancement will improve typographic control, reduce redundancy, and support a more scalable, modern approach to web design.

[Tracking bug #40398871](https://issues.chromium.org/issues/40398871) | [ChromeStatus.com entry](https://chromestatus.com/feature/5102801981800448) | [Spec](https://www.w3.org/TR/css-fonts-4/#font-rend-desc)

### CSS custom functions

Custom functions are similar to custom properties, but instead of returning a single, fixed value, they return values based on other custom properties, parameters, and conditionals.

[Tracking bug #325504770](https://issues.chromium.org/issues/325504770) | [ChromeStatus.com entry](https://chromestatus.com/feature/5179721933651968) | [Spec](https://drafts.csswg.org/css-mixins-1/#defining-custom-functions)

### Continue running transitions when switching to initial transition value

When the transition related properties change, they are only supposed to affect newly started transitions. This means that if you change the transition properties, unless you also change the properties which have active transition animations, those transition animations will continue with the previously specified duration and easing.

Chrome incorrectly canceled transitions when the transition property was set to `none`, even though it doesn't cancel them if you only change the `transition-duration`. This change makes Chrome consistent with Safari and Firefox, allowing active transitions to continue running, until their property value changes triggering a new transition update.

[ChromeStatus.com entry](https://chromestatus.com/feature/5194501932711936) | [Spec](https://www.w3.org/TR/css-transitions-1/#starting)

### Corner shaping (`corner-shape`, `superellipse`, `squircle`)

Enable styling corners, on top of the existing `border-radius`, by expressing the shape and curvature of the corner as a superellipse.

This allows shapes like squircles, notches, and scoops, and animating between them.

[Tracking bug #393145930](https://issues.chromium.org/issues/393145930) | [ChromeStatus.com entry](https://chromestatus.com/feature/5357329815699456) | [Spec](https://drafts.csswg.org/css-borders-4/#corner-shaping)

### Add `font-width` property and descriptor and make `font-stretch` a legacy alias

Before this change Chrome didn't recognize `font-width` as a valid property, instead using `font-stretch` which is now considered a legacy alias.

This change brings Chrome into line with the specification and other browsers.

[Tracking bug #356670472](https://issues.chromium.org/issues/356670472) | [ChromeStatus.com entry](https://chromestatus.com/feature/5190141555245056)

### Support async attribute for SVG `<script>` element

The `SVGScriptElement` interface in SVG 2.0 introduces the async attribute, similar to the `HTMLScriptElement`. This attribute allows scripts to be executed asynchronously, improving the performance and responsiveness of web applications that use SVG.

[Tracking bug #40067618](https://issues.chromium.org/issues/40067618) | [ChromeStatus.com entry](https://chromestatus.com/feature/6114615389585408) | [Spec](https://svgwg.org/svg2-draft/interact.html#ScriptElement:~:text=%E2%80%98script%E2%80%99%20element-,SVG%202%20Requirement%3A,Consider%20allowing%20async/defer%20on%20%E2%80%98script%E2%80%99.,-Resolution%3A)

### The `request-close` invoker command

Dialog elements can be closed through a variety of mechanisms, sometimes developers want to have the ability to prevent closure. To achieve this dialogs fire a cancel event. Originally this was only fired via a close request (for example, an `ESC` key press), recently a `requestClose()` JavaScript function was added which also fires the cancel event.

The `request-close` command brings that new ability to the declarative invoker commands API.

[Tracking bug #400647849](https://issues.chromium.org/issues/400647849) | [ChromeStatus.com entry](https://chromestatus.com/feature/5592399713402880) | [Spec](https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-command-request-close-state)

### Scroll anchoring priority candidate fix

Changes the scroll anchoring algorithm. Instead of selecting the priority candidate as the anchor, choose the candidate as the scope or root of the regular anchor selection algorithm which will select the deepest onscreen element as the anchor.

[ChromeStatus.com entry](https://chromestatus.com/feature/5070370113323008)

## Device

### WebXR depth sensing performance improvements

Exposes several new mechanisms to customize the behavior of the depth sensing feature within a WebXR session, with the goal of improving the performance of the generation or consumption of the depth buffer.

The key mechanisms exposed are: the ability to request the raw or smooth depth buffer, the ability to request that the runtime stop or resume providing the depth buffer, and the ability to expose a depth buffer that does not align with the user's view exactly, so that the user agent does not need to perform unnecessary re-projections every frame.

[Tracking bug #410607163](https://issues.chromium.org/issues/410607163) | [ChromeStatus.com entry](https://chromestatus.com/feature/5074096916004864) | [Spec](https://immersive-web.github.io/depth-sensing)

## DOM

### Allow more characters in JavaScript DOM APIs

The HTML parser has always (or for a long time) allowed elements and attributes to have a wide variety of valid characters and names, but the JavaScript DOM APIs to create the same elements and attributes are more strict and don't match the parser.

This change relaxes the validation of the javascript DOM APIs to match the HTML parser.

[Tracking bug #40228234](https://issues.chromium.org/issues/40228234) | [ChromeStatus.com entry](https://chromestatus.com/feature/6278918763708416) | [Spec](https://dom.spec.whatwg.org/#namespaces)

## Graphics

### WebGPU: 3D texture support for BC and ASTC compressed formats

The `texture-compression-bc-sliced-3d` and `texture-compression-astc-sliced-3d` WebGPU features add respectively 3D texture support for BC and ASTC compressed formats.

[Tracking bug #342840940](https://issues.chromium.org/issues/342840940) | [ChromeStatus.com entry](https://chromestatus.com/feature/5080855386783744) | [Spec](https://gpuweb.github.io/gpuweb/#texture-compression-bc-sliced-3d)

## Secure Payment Confirmation (SPC)

### The `securePaymentConfirmationAvailability` API

This is a JavaScript API to provide an easier way to check if the Secure Payment Confirmation (SPC) feature is available. With this API, the only way to determine SPC's availability was to create a `PaymentRequest` with the required parameters, which is clunky and difficult in the case where a developer wants to check for SPC before starting to process a payment.

[Tracking bug #40258712](https://issues.chromium.org/issues/40258712) | [ChromeStatus.com entry](https://chromestatus.com/feature/5165040614768640) | [Spec](https://github.com/w3c/secure-payment-confirmation/pull/285)

### Secure Payment Confirmation: Browser Bound Keys

Adds an additional cryptographic signature over Secure Payment Confirmation assertions and credential creation. The corresponding private key is not synced across devices. This helps web developers meet requirements for device binding for payment transactions.

[Tracking bug #377278827](https://issues.chromium.org/issues/377278827) | [ChromeStatus.com entry](https://chromestatus.com/feature/5106102997614592) | [Spec](https://w3c.github.io/secure-payment-confirmation/#sctn-browser-bound-key-store)

## On-device AI

### On-device Web Speech API

This feature adds on-device speech recognition support to the Web Speech API, allowing websites to ensure that neither audio nor transcribed speech are sent to a third-party service for processing.

Websites can query the availability of on-device speech recognition for specific languages, prompt users to install the necessary resources for on-device speech recognition, and choose between on-device or cloud-based speech recognition as needed.

[ChromeStatus.com entry](https://chromestatus.com/feature/6090916291674112) | [Spec](https://webaudio.github.io/web-speech-api)

## Navigation

### Clear window name for cross-site navigations that switches browsing context group

Clears the value of the `window.name` property when navigation switches browsing context groups, to avoid leaking information that could be used as a tracking vector.

[Tracking bug #1090128](https://issues.chromium.org/issues/1090128) | [ChromeStatus.com entry](https://chromestatus.com/feature/5962406356320256) | [Spec](https://html.spec.whatwg.org/multipage/browsing-the-web.html#resetBCName)

## Network

### Reduce fingerprinting in Accept-Language header information

Reduces the amount of information the `Accept-Language` header value string exposes in HTTP requests and in `navigator.languages`. Instead of sending a full list of the user's preferred languages on every HTTP request using the `Accept-Language` header, Chrome only sends the user's most preferred language.

[Tracking bug #1306905](https://issues.chromium.org/issues/1306905) | [ChromeStatus.com entry](https://chromestatus.com/feature/5188040623390720)

### Randomize TCP port allocation on Windows

This launch enables TCP port randomization on versions of Windows (2020 or later) where we don't expect to see issues with re-use of prior ports occurring too fast (causing rejection due to timeouts on port re-use). The rapid port re-use issue arises from the Birthday problem, where the probability of randomly re-picking a port already seen rapidly converges with 100% for each new port chosen when compared to port re-use in a sequential model.

[Tracking bug #40744069](https://issues.chromium.org/issues/40744069) | [ChromeStatus.com entry](https://chromestatus.com/feature/5106900286570496)

## Performance

### Faster background freezing on Android

Shortens the time to freezing background pages (and associated workers) from five minutes to one minute on Android.

[Tracking bug #435623337](https://issues.chromium.org/issues/435623337) | [ChromeStatus.com entry](https://chromestatus.com/feature/5386725031149568)

## Security

### Fire error event for Content Security Policy (CSP) blocked worker

Makes Chrome conform to the specification, checking the CSP during fetch and firing the error event asynchronously instead of throwing exception when script runs "new Worker(url)" or "new SharedWorker(url)".

[Tracking bug #41285169](https://issues.chromium.org/issues/41285169) | [ChromeStatus.com entry](https://chromestatus.com/feature/5177205656911872) | [Spec](https://www.w3.org/TR/CSP3/#fetch-integration)

## WebRTC

### Audio level for RTC encoded frames

This feature exposes to the web the audio level of an encoded frame transmitted using `RTCPeerConnection` and exposed using WebRTC encoded transform.

[Tracking bug #418116079](https://issues.chromium.org/issues/418116079) | [ChromeStatus.com entry](https://chromestatus.com/feature/5206106602995712) | [Spec](https://w3c.github.io/webrtc-encoded-transform/#dom-rtcencodedaudioframemetadata-audiolevel)

## Web APIs

### Web app scope extensions

Adds a `scope_extensions` web app manifest field that enables web apps to extend their scope to other origins.

This allows sites that control multiple subdomains and top level domains to be presented as a single web app.

Requires listed origins to confirm association with the web app using a `.well-known/web-app-origin-association` configuration file.

[Tracking bug #detail?id=1250011](https://issues.chromium.org/issues/detail?id=1250011) | [ChromeStatus.com entry](https://chromestatus.com/feature/5746537956114432) | [Spec](https://github.com/WICG/manifest-incubations/pull/113)

### Specification-compliant JSON MIME type detection

Chrome now recognizes all valid JSON MIME types as defined by the WHATWG mimesniff specification. This includes any MIME type whose subtype ends with `+json`, in addition to `application/json` and `text/json`. This change ensures that web APIs and features relying on JSON detection behave consistently with the web platform standard and other browsers.

[ChromeStatus.com entry](https://chromestatus.com/feature/5470594816278528) | [Spec](https://mimesniff.spec.whatwg.org/#json-mime-type)

### WebGPU `core-features-and-limits`

The `core-features-and-limits` feature signifies a WebGPU adapter and device support the core features and limits of the spec.

[Tracking bug #418025721](https://issues.chromium.org/issues/418025721) | [ChromeStatus.com entry](https://chromestatus.com/feature/4744775089258496) | [Spec](https://gpuweb.github.io/gpuweb/#core-features-and-limits)

### Crash Reporting API: Specify `crash-reporting` to receive only crash reports

This feature ensures developers receive only crash reports by specifying the endpoint named `crash-reporting`. By default, crash reports are delivered to the `default` endpoint which receives many other kinds of reports besides crash reports. Developers can supply a separate URL to the well-known endpoint named `crash-reporting`, to direct crash reports there, instead of the `default` endpoint.

[Tracking bug #414723480](https://issues.chromium.org/issues/414723480) | [ChromeStatus.com entry](https://chromestatus.com/feature/5129218731802624) | [Spec](https://wicg.github.io/crash-reporting/#crash-reports-delivery-priority)

## Origin trials

### Prompt API

An API designed for interacting with an AI language model using text, image, and audio inputs. It supports various use cases, from generating image captions and performing visual searches to transcribing audio, classifying sound events, generating text following specific instructions, and extracting information or insights from text. It supports structured outputs which ensure that responses adhere to a predefined format, typically expressed as a JSON schema, to enhance response conformance and facilitate seamless integration with downstream applications that require standardized output formats.

This API is also exposed in Chrome Extensions. This feature entry tracks the exposure on the web. An enterprise policy (`GenAILocalFoundationalModelSettings`) is available to disable the underlying model downloading which would render this API unavailable.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/2533837740349325313) | [Origin trial blog post](/blog/prompt-multimodal-origin-trial) | [Tracking bug #417530643](https://issues.chromium.org/issues/417530643) | [ChromeStatus.com entry](https://chromestatus.com/feature/5134603979063296)

### Extended lifetime shared workers

This adds a new option, `extendedLifetime: true`, to the `SharedWorker` constructor. This requests that the shared worker be kept alive even after all current clients have unloaded. The primary use case is to allow pages to perform asynchronous work that requires JavaScript after a page unloads, without needing to rely on a service worker.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/3056255297124302849) | [Origin trial blog post](/blog/extended-lifetime-shared-workers-origin-trial) | [Tracking bug #400473072](https://issues.chromium.org/issues/400473072) | [ChromeStatus.com entry](https://chromestatus.com/feature/5138641357373440)

### `SoftNavigation` performance entry

Exposes the (experimental) soft navigation heuristics to web developers, using both `PerformanceObserver` and the performance timeline.

This feature reports two new performance entries:

  * `soft-navigation`, for user interactions which navigate the page. Defines a new `timeOrigin` to help slice the performance timeline.
  * `interaction-contentful-paint`, which reports on the loading performance of interactions (beyond just next paint), used as LCP for soft-navigations.

[Origin Trial](https://developer.chrome.com/origintrials#/view_trial/21392098230009857) | [Origin trial blog post](/blog/new-soft-navigations-origin-trial) | [Tracking bug #1338390](https://issues.chromium.org/issues/1338390) | [ChromeStatus.com entry](https://chromestatus.com/feature/5144837209194496) | [Spec](https://wicg.github.io/soft-navigations)

### Web Authentication immediate mediation

A mediation mode for `navigator.credentials.get()` that causes browser sign-in UI to be displayed to the user if there is a passkey or password for the site that is immediately known to the browser. Otherwise, it rejects the with `NotAllowedError` if there is no such credential available. This allows the site to avoid showing a sign-in page if the browser can offer a choice of sign-in credentials that are likely to succeed, while still allowing a sign-in page flow for cases where there are no such credentials.

[Tracking bug #408002783](https://issues.chromium.org/issues/408002783) | [ChromeStatus.com entry](https://chromestatus.com/feature/5164322780872704) | [Spec](https://github.com/w3c/webauthn/pull/2291)

### Full frame rate render blocking attribute

Adds a new render blocking token full-frame-rate to the blocking attributes. When the renderer is blocked with the full-frame-rate token, the renderer will work at a lower frame rate so as to reserve more resources for loading.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/3578672853899280385) | [Tracking bug #397832388](https://issues.chromium.org/issues/397832388) | [ChromeStatus.com entry](https://chromestatus.com/feature/5207202081800192)

### WebGPU compatibility mode

Adds an opt-in, lightly restricted subset of the WebGPU API capable of running older graphics APIs such as OpenGL and Direct3D11. By opting into this mode and obeying its constraints, developers can extend the reach of their WebGPU applications to many older devices that don't have the modern, explicit graphics APIs that core WebGPU requires.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/1489002626799370241) | [Tracking bug #40266903](https://issues.chromium.org/issues/40266903) | [ChromeStatus.com entry](https://chromestatus.com/feature/6436406437871616) | [Spec](https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md)

## Deprecations and removals

### Stop sending Purpose: prefetch header from prefetches and prerenders

Now that prefetches and prerenders are using the `Sec-Purpose` header for prefetches and prerenders, we will move to remove the legacy Purpose: prefetch header that is still currently passed. This will be behind a feature flag/ kill switch to prevent compat issues.

This will be scoped to speculation rules prefetch, speculation rules prerender, `<link rel=prefetch>`, and Chrome's non-standard `<link rel=prerender>`.

[Tracking bug #420724819](https://issues.chromium.org/issues/420724819) | [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320) | [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

### Remove support for macOS 11

Chrome 138 is the last release to support macOS 11. From Chrome 139 macOS 11 is not supported.

On Macs running macOS 11, Chrome will continue to work, showing a warning infobar, but won't update any further. To update Chrome, you need to update their computer to a supported version of macOS.

For new installations from Chrome 139, macOS 12 or greater will be required.

[ChromeStatus.com entry](https://chromestatus.com/feature/4504090090143744)

### Remove auto-detection of `ISO-2022-JP` charset in HTML

There are [known security issues](https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/) around charset auto-detection for `ISO-2022-JP`. Given that the usage is very low, and Safari does not support auto-detection of `ISO-2022-JP`, support is removed from Chrome 139.

[Tracking bug #40089450](https://issues.chromium.org/issues/40089450) | [ChromeStatus.com entry](https://chromestatus.com/feature/6576566521561088)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-08-05 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-08-05 UTC."],[],[]] 
