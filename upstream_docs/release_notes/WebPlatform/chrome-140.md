# Chrome 140 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/140

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Docs ](https://developer.chrome.com/docs)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 140

Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** September 2nd, 2025

Unless otherwise noted, the following changes apply to Chrome 140 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 140](/blog/new-in-chrome-140). 

## CSS

### CSS typed arithmetic

Typed arithmetic lets you write expressions in CSS such as `calc(10em / 1px)` or `calc(20% / 0.5em * 1px)`. This is useful in, for example, typography, as it lets you convert a typed value into an untyped one and reuse it for number accepting properties. Another use case is to multiply the unitless value by another type. For example, you can now cast from pixels to degrees.

[Tracking bug #40768696](https://issues.chromium.org/issues/40768696) | [ChromeStatus.com entry](https://chromestatus.com/feature/4740780497043456) | [Spec](https://www.w3.org/TR/css-values-4/#calc-type-checking)

### CSS `caret-animation` property

Chromium supports animation of the `caret-color` property. However, when animated, the caret's default blinking behavior interferes with the animation.

The CSS `caret-animation` property has two possible values: `auto` and `manual`. `auto` means browser default (blinking), and `manual` means the developer controls the caret animation. Additionally, users who are disturbed by or have adverse reactions to blinking or flashing visuals can disable the blinking with a user stylesheet.

[Tracking bug #329301988](https://issues.chromium.org/issues/329301988) | [ChromeStatus.com entry](https://chromestatus.com/feature/5082469066604544) | [Spec](https://drafts.csswg.org/css-ui/#caret-animation)

### highlightsFromPoint API

The `highlightsFromPoint` API lets developers interact with custom highlights. It detects which highlights exist at a specific point within a document. This interactivity is valuable for complex web features where multiple highlights may overlap or exist within shadow DOM. By providing precise point-based highlight detection, the API empowers developers to manage dynamic interactions with custom highlights more effectively. For example, developers can respond to user clicks or hover events on highlighted regions to trigger custom tooltips, context menus, or other interactive features.

[Tracking bug #365046212](https://issues.chromium.org/issues/365046212) | [ChromeStatus.com entry](https://chromestatus.com/feature/4552801607483392) | [Spec](https://drafts.csswg.org/css-highlight-api-1/#interactions)

### `ScrollIntoView` container option

The `ScrollIntoViewOptions` container option allows developers to perform a `scrollIntoView` operation that only scrolls the nearest ancestor scroll container. For example, the following snippet only scrolls the scroll container of `target` to bring `target` into view, but won't scroll all of the scroll containers to the viewport:
    
    
    target.scrollIntoView({container: 'nearest'});
    

[ChromeStatus.com entry](https://chromestatus.com/feature/5100036528275456) | [Spec](https://drafts.csswg.org/cssom-view/#dom-scrollintoviewoptions-container)

### View transitions: Inherit more animation properties

Adds more animation properties to inherit through the view transition pseudo tree:

  * `animation-timing-function`
  * `animation-iteration-count`
  * `animation-direction`
  * `animation-play-state`

[Tracking bug #427741151](https://issues.chromium.org/issues/427741151) | [ChromeStatus.com entry](https://chromestatus.com/feature/5154752085884928) | [Spec](https://www.w3.org/TR/css-view-transitions-2)

### View transition pseudos inherit animation-delay.

In addition to the previous update, the `animation-delay` property is now inherited through the view transition pseudo tree.

[ChromeStatus.com entry](https://chromestatus.com/feature/5424291457531904) | [Spec](https://www.w3.org/TR/css-view-transitions-2)

### Nested view transitions groups

This feature allows view transitions to generate a nested pseudo-element tree rather than a flat one. This allows the view transition to appear more in line with its original elements and visual intent. It enables clipping, nested 3D transforms, and proper application of effects like opacity, masking, and filters.

[Tracking bug #399431227](https://issues.chromium.org/issues/399431227) | [ChromeStatus.com entry](https://chromestatus.com/feature/5162799714795520) | [Spec](https://www.w3.org/TR/css-view-transitions-2/#view-transition-group-prop)

### Propagate viewport `overscroll-behavior` from root

This change propagates `overscroll-behavior` from the root instead of the body.

The CSS working group resolved not to propagate properties from the `<body>` to the viewport. Instead, properties of the viewport propagate from the root (`<html>`) element. As such, `overscroll-behavior` should propagate from the root element. However, Chrome has had a longstanding issue: it propagates `overscroll-behavior` from the `<body>` rather than the root. This behavior is not interoperable with other browsers. This change makes Chrome comply with the specification and become interoperable with other implementations.

[Tracking bug #41453796](https://issues.chromium.org/issues/41453796) | [ChromeStatus.com entry](https://chromestatus.com/feature/6210047134400512) | [Spec](https://drafts.csswg.org/css-overscroll-behavior-1)

### CSS `counter()` and `counters()` in alt text of `content` property

This feature adds the ability to use `counter()` and `counters()` in the alt text of the `content` property. This provides more meaningful information to improve accessibility.

[Tracking bug #417488055](https://issues.chromium.org/issues/417488055) | [ChromeStatus.com entry](https://chromestatus.com/feature/5185442420621312) | [Spec](https://drafts.csswg.org/css-content/#content-property)

### CSS `scroll-target-group` property

The `scroll-target-group` property specifies whether the element is a scroll marker group container. It accepts one of the following values:

  * 'none': The element does not establish a scroll marker group container.
  * 'auto': The element establishes a scroll marker group container forming a scroll marker group containing all of the scroll marker elements for which this is the nearest ancestor scroll marker group container.

Establishing a scroll marker group container lets any anchor HTML elements with a fragment identifier that are inside such a container to be the HTML equivalent of `::scroll-marker` pseudo-elements. The anchor element whose scroll target is currently in view can be styled using the `:target-current` pseudo-class.

[Tracking bug #6607668](https://issues.chromium.org/issues/6607668) | [ChromeStatus.com entry](https://chromestatus.com/feature/5189126177161216) | [Spec](https://drafts.csswg.org/css-overflow-5/#scroll-target-group)

### Support `font-variation-settings` descriptor in `@font-face` rule

CSS allows developers to adjust a font's weight, width, slant, and other axes using the `font-variation-settings` property on individual elements. However, Chromium-based browsers lack support for this property within `@font-face` declarations. This feature supports the string-based syntax for `font-variation-settings` as defined in CSS Fonts Level 4. Invalid or unrecognized feature tags are ignored per specification. No binary or non-standard forms are supported. Variable fonts are becoming more widely adopted for both performance and typographic flexibility. Adding support for this descriptor in Chromium enhances control, reduces repetition, and supports a more scalable, modern approach to web typography.

[Tracking bug #40398871](https://issues.chromium.org/issues/40398871) | [ChromeStatus.com entry](https://chromestatus.com/feature/5221379619946496) | [Spec](https://www.w3.org/TR/css-fonts-4/#font-rend-desc)

## DOM

### `ToggleEvent` source attribute

The `source` attribute of a `ToggleEvent` contains the element that triggered the `ToggleEvent` to be fired, if applicable. For example, if a user clicks a `<button>` element with the `popovertarget` or `commandfor` attribute set to open a popover, the `ToggleEvent` fired on the popover will have its source attribute set to the invoking `<button>`.

[ChromeStatus.com entry](https://chromestatus.com/feature/5165304401100800) | [Spec](https://html.spec.whatwg.org/multipage/interaction.html#the-toggleevent-interface)

## Isolated Web Apps (IWAs)

### Controlled Frame API (available only to IWAs)

This feature adds a Controlled Frame API available only to Isolated Web Apps (IWAs). Like similarly-named APIs on other platforms, Controlled Frame allows embedding all content, even third-party content that cannot be embedded in `<iframe>`. Controlled Frame also allows controlling embedded content with a collection of API methods and events. For more information about Isolated Web Apps, see the [Isolated Web Apps explainer](https://github.com/WICG/isolated-web-apps/blob/main/README.md).

[Tracking bug #40191772](https://issues.chromium.org/issues/40191772) | [ChromeStatus.com entry](https://chromestatus.com/feature/5199572022853632) | [Spec](https://wicg.github.io/controlled-frame)

## JavaScript

### `Uint8Array` to and from base64 and hex

Base64 is a common way to represent arbitrary binary data as ASCII. JavaScript has `Uint8Arrays` for binary data. However, it lacks a built-in mechanism to encode that data as base64, or to take base64 data and produce a corresponding `Uint8Array`. This feature adds the ability and methods for converting between hex strings and `Uint8Arrays`.

[ChromeStatus.com entry](https://chromestatus.com/feature/6281131254874112) | [Spec](https://tc39.es/proposal-arraybuffer-base64/spec)

### View transition finished promise timing change

The current finished promise timing happens within the rendering lifecycle steps. This means that code that runs as a result of promise resolution happens after the visual frame that removes the view transition has been produced. This can cause a flicker at the end of the animation if the script moves styles to preserve a visually similar state. This change resolves the issue by moving the view transition cleanup steps to run asynchronously after the lifecycle is completed.

[Tracking bug #430018991](https://issues.chromium.org/issues/430018991) | [ChromeStatus.com entry](https://chromestatus.com/feature/5143135809961984)

## Web APIs

### `ReadableStreamBYOBReader` `min` option

This feature introduces a `min` option to the existing `ReadableStreamBYOBReader.read(view)` method. The method already accepts an `ArrayBufferView` into which it reads data, but currently does not guarantee how many elements are written before the read resolves. By specifying a `min` value, you can require that the stream wait until at least that many elements are available before resolving the read. This improves upon the current behavior, where reads may resolve with fewer elements than the view can hold.

[Tracking bug #40942083](https://issues.chromium.org/issues/40942083) | [ChromeStatus.com entry](https://chromestatus.com/feature/6396991665602560) | [Spec](https://streams.spec.whatwg.org/#byob-reader-read)

### Get Installed Related Apps API on desktop

The Get Installed Related Apps API (navigator.getInstalledRelatedApps) provides sites access to if their corresponding related applications are installed. Sites are only allowed to use this API if the application has an established association with the web origin.

The API was launched in Chrome 80 for Android. Additional support for web apps on Desktop was enabled in Chrome 140.

[Docs](/docs/capabilities/get-installed-related-apps) | [Tracking bug #895854](https://issues.chromium.org/issues/895854) | [ChromeStatus.com entry](https://chromestatus.com/feature/5695378309513216) | [Spec](https://wicg.github.io/get-installed-related-apps/spec)

### Http cookie prefix

In some cases, it's important to distinguish on the server side between cookies set by the server and those set by the client. One such case involves cookies normally always set by the server. However, unexpected code (such as an XSS exploit, a malicious extension, or a commit from a confused developer) might set them on the client. This proposal adds a signal that lets servers make such a distinction. More specifically, it defines the `__Http` and `__HostHttp` prefixes, which ensure a cookie is not set on the client side using script.

[Tracking bug #426096760](https://issues.chromium.org/issues/426096760) | [ChromeStatus.com entry](https://chromestatus.com/feature/5170139586363392) | [Spec](https://github.com/httpwg/http-extensions/pull/3110)

## Service worker

### `SharedWorker` script inherits controller for blob script URL

The specification states that workers should inherit controllers for the blob URL. However, existing code allows only dedicated workers to inherit the controller; shared workers don't. This fixes Chrome's behavior to align with the specification. The `SharedWorkerBlobURLFixEnabled` enterprise policy controls this feature.

[Tracking bug #324939068](https://issues.chromium.org/issues/324939068) | [ChromeStatus.com entry](https://chromestatus.com/feature/5137897664806912) | [Spec](https://w3c.github.io/ServiceWorker/#control-and-use-worker-client)

### Add `ServiceWorkerStaticRouterTimingInfo`

This feature adds timing information for the ServiceWorker Static routing API, exposed in the navigation timing API and resource timing API for developer use. ServiceWorker provides timing information to mark certain points in time.

This feature adds two pieces of Static routing API-relevant timing information:

  * `RouterEvaluationStart`: Time to start matching a request with registered router rules.
  * `CacheLookupStart`: Time to start looking up the cache storage if the source is `"cache"`.

Additionally, this feature adds two pieces of router source information: the matched router source and the final router source.

[Tracking bug #41496865](https://issues.chromium.org/issues/41496865) | [ChromeStatus.com entry](https://chromestatus.com/feature/6309742380318720) | [Spec](https://github.com/w3c/ServiceWorker)

## Origin trials

### Enable incoming call notifications

This feature extends the Notifications API to allow installed PWAs to send incoming call notifications—notifications with call-styled buttons and a ringtone. This extension helps VoIP web apps create more engaging experiences by making it easier for users to recognize and answer calling notifications. Additionally, this feature helps bridge the gap between native and web implementations of apps that have them both.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/2876111312029483009) | [Tracking bug #detail?id=1383570](https://issues.chromium.org/issues/detail?id=1383570) | [ChromeStatus.com entry](https://chromestatus.com/feature/5110990717321216) | [Spec](https://notifications.spec.whatwg.org)

### Crash Reporting key-value API

This feature introduces a new key-value API, tentatively `window.crashReport`, backed by a per-document map that holds data appended to crash reports.

The data placed in this API's backing map is sent in the `CrashReportBody` if any renderer process crashes occur on the site. This lets developers debug what specific state in their application might be causing a given crash.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/1304355042077179905) | [Tracking bug #400432195](https://issues.chromium.org/issues/400432195) | [ChromeStatus.com entry](https://chromestatus.com/feature/6228675846209536) | [Spec](https://github.com/WICG/crash-reporting/pull/37)

### Add the `clipboardchange` event

The `clipboardchange` event fires whenever a web app or any other system application changes the system clipboard contents. This allows web apps like remote desktop clients to keep their clipboards synchronized with the system clipboard. It provides an efficient alternative to polling the clipboard with JavaScript for changes.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/137922738588221441) | [Tracking bug #41442253](https://issues.chromium.org/issues/41442253) | [ChromeStatus.com entry](https://chromestatus.com/feature/5085102657503232) | [Spec](https://github.com/w3c/clipboard-apis/pull/239)

### Enable `SharedWorker` on Android

The long-standing demand for SharedWorker support on Android stems from several needs expressed by web developers:

  * **Resource sharing and efficiency** : Developers aim to share a single WebSocket or Server-Sent Events (SSE) connection across multiple tabs, thereby conserving resources.
  * **Persistent resource management** : A requirement to share and persist resources across tabs, particularly for technologies like WASM-based SQLite.
  * **Closing a feature gap** : Other major mobile browsers, including Safari on iOS and Firefox on Android, already support SharedWorker, making Chrome on Android the last major browser to address this gap.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/4101090410674257921) | [ChromeStatus.com entry](https://chromestatus.com/feature/6265472244514816) | [Spec](https://html.spec.whatwg.org/multipage/workers.html#shared-workers-and-the-sharedworker-interface)

## Removals

### Stop sending `Purpose: prefetch` header from prefetches and prerenders

Prefetches and prerenders now use the `Sec-Purpose` header, therefore the legacy `Purpose: prefetch` header is being removed.

This will be scoped to speculation rules `prefetch`, speculation rules `prerender`, `<link rel=prefetch>`, and Chromium's non-standard `<link rel=prerender>`.

[Tracking bug #420724819](https://issues.chromium.org/issues/420724819) | [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320) | [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

### Deprecate special font size rules for H1 within some elements

The HTML spec contains [a list of special rules](https://html.spec.whatwg.org/multipage/rendering.html#sections-and-headings) for `<h1>` tags nested within `<article>`, `<aside>`, `<nav>`, or `<section>` tags:

These special rules are deprecated, because they cause accessibility issues. Namely, they visually reduce the font size for nested `<h1>` elements so that they "look" like `<h2>` elements, but nothing in the accessibility tree reflects this demotion.

[Tracking bug #394111284](https://issues.chromium.org/issues/394111284) | [ChromeStatus.com entry](https://chromestatus.com/feature/6192419898654720) | [Spec](https://github.com/whatwg/html/pull/11102)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-02 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-09-02 UTC."],[],[],null,[]] 
