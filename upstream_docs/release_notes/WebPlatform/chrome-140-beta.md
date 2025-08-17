# Chrome 140 Release Notes (Beta)

Source: https://developer.chrome.com/blog/chrome-140-beta

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Blog ](https://developer.chrome.com/blog)

#  Chrome 140 beta

Stay organized with collections  Save and categorize content based on your preferences. 

![Rachel Andrew](https://web.dev/images/authors/rachelandrew.jpg)

Rachel Andrew 

[ X ](https://twitter.com/rachelandrew) [ GitHub ](https://github.com/rachelandrew) [ LinkedIn ](https://www.linkedin.com/in/rachelandrew) [ Mastodon ](https://front-end.social/@rachelandrew) [ Bluesky ](https://bsky.app/profile/rachelandrew.bsky.social) [ Homepage ](https://rachelandrew.co.uk)

Published: August 6, 2025 

Unless otherwise noted, the following changes apply to the newest Chrome beta channel release for Android, ChromeOS, Linux, macOS, and Windows. Learn more about the features listed here through the provided links or from the list on ChromeStatus.com. Chrome 140 is in beta as of August 6, 2025. You can download the latest on the [official Chrome website](https://www.google.com/chrome/beta/) for desktop or on Google Play Store on Android.

## CSS and UI

### CSS typed arithmetic

Typed arithmetic lets you write expressions in CSS such as `calc(10em / 1px)` or `calc(20% / 0.5em * 1px)`. This is useful in, for example, typography, as it lets you convert a typed value into an untyped one and reuse it for number accepting properties. Another use case is to multiply the unitless value by another type. For example, you can cast from pixels to degrees.

### The `scroll-target-group` property

The `scroll-target-group` property specifies whether the element is a scroll marker group container. It accepts one of the following values:

  * 'none': The element does not establish a scroll marker group container.
  * 'auto': The element establishes a scroll marker group container forming a scroll marker group containing all of the scroll marker elements for which this is the nearest ancestor scroll marker group container.

Establishing a scroll marker group container lets any anchor HTML elements with a fragment identifier that are inside such a container to be the HTML equivalent of `::scroll-marker` pseudo-elements. The anchor element whose scroll target is currently in view can be styled using the `:target-current` pseudo-class.

### Enable `counter()` and `counters()` in the `content` property's alt text

This feature adds the ability to use `counter()` and `counters()` in the alt text of the `content` property. This provides more meaningful information to improve accessibility.

### View transition pseudos inherit more animation properties

The view transition pseudo tree now inherits a number of animation properties:

  * `animation-delay`
  * `animation-timing-function`
  * `animation-iteration-count`
  * `animation-direction`
  * `animation-play-state`

### Enable nested view transitions

This feature allows view transitions to generate a nested pseudo-element tree rather than a flat one. This allows the view transition to appear more in line with its original elements and visual intent. It enables clipping, nested 3D transforms, and proper application of effects like opacity, masking, and filters.

### Propagate viewport `overscroll-behavior` from root

This change propagates `overscroll-behavior` from the root instead of the body. The CSS working group resolved not to propagate properties from the `<body>` to the viewport. Instead, properties of the viewport propagate from the root (`<html>`) element. As such, `overscroll-behavior` should propagate from the root element. However, Chrome has had a longstanding issue: it propagates `overscroll-behavior` from the `<body>` rather than the root. This behavior is not interoperable with other browsers. This change makes Chrome comply with the specification and become interoperable with other implementations.

### `ScrollIntoView` container option

The `ScrollIntoViewOptions` container option allows developers to perform a `scrollIntoView` operation that only scrolls the nearest ancestor scroll container. For example, the following snippet only scrolls the scroll container of `target` to bring `target` into view, but won't scroll all of the scroll containers to the viewport:
    
    
    target.scrollIntoView({container: 'nearest'});
    

### Add the CSS `caret-animation` property

Chromium supports animation of the `caret-color` property. However, when animated, the caret's default blinking behavior interferes with the animation.

The CSS `caret-animation` property has two possible values: `auto` and `manual`. `auto` means browser default (blinking), and `manual` means the developer controls the caret animation. Additionally, users who are disturbed by or have adverse reactions to blinking or flashing visuals can disable the blinking with a user stylesheet.

### The `highlightsFromPoint` API

The `highlightsFromPoint` API enables developers to interact with custom highlights. It detects which highlights exist at a specific point within a document. This interactivity is valuable for complex web features where multiple highlights may overlap or exist within shadow DOM. By providing precise point-based highlight detection, the API empowers developers to manage dynamic interactions with custom highlights more effectively. For example, developers can respond to user clicks or hover events on highlighted regions to trigger custom tooltips, context menus, or other interactive features.

### Change View Transition finished promise timing

The current finished promise timing happens within the rendering lifecycle steps. This means that code that runs as a result of promise resolution happens after the visual frame that removes the view transition has been produced. This can cause a flicker at the end of the animation if the script moves styles to preserve a visually similar state. This change resolves the issue by moving the ViewTransition cleanup steps to run asynchronously after the lifecycle is completed.

### Add the `ToggleEvent` source attribute

The `source` attribute of a `ToggleEvent` contains the element that triggered the `ToggleEvent` to be fired, if applicable. For example, if a user clicks a `<button>` element with the `popovertarget` or `commandfor` attribute set to open a popover, the `ToggleEvent` fired on the popover will have its source attribute set to the invoking `<button>`.

### Prevent SVG `foreignObject` from tainting the canvas for blob URLs

All browsers have long supported using an `<img>` element with an SVG source in an HTML canvas `drawImage` operation. However, canvas tainting behavior varies across platforms. All browsers taint the canvas when the SVG source includes a `foreignObject` tag and is referenced with an HTTP URI. When the same SVG is referenced through a data URI, all browsers don't taint the canvas. However, when a blob URI is used, both Chromium (before this change) and WebKit taint the canvas, but Gecko does not. When this feature ships, Chromium's behavior matches that of Gecko, allowing a wider range of SVG content to be used in canvas `drawImage` calls without tainting.

### Support the `font-variation-settings` descriptor in `@font-face rule`

CSS allows developers to adjust a font's weight, width, slant, and other axes using the `font-variation-settings` property on individual elements. However, Chromium-based browsers lack support for this property within `@font-face` declarations. This feature supports the string-based syntax for `font-variation-settings` as defined in CSS Fonts Level 4. Invalid or unrecognized feature tags are ignored per specification. No binary or non-standard forms are supported. Variable fonts are becoming more widely adopted for both performance and typographic flexibility. Adding support for this descriptor in Chromium enhances control, reduces repetition, and supports a more scalable, modern approach to web typography.

## Web APIs

### Convert `Uint8Array` to and from base64 and hex

Base64 is a common way to represent arbitrary binary data as ASCII. JavaScript has `Uint8Arrays` for binary data. However, it lacks a built-in mechanism to encode that data as base64, or to take base64 data and produce a corresponding `Uint8Array`. This feature adds the ability and methods for converting between hex strings and `Uint8Arrays`.

### Use the `ReadableStreamBYOBReader` `min` option

This feature introduces a `min` option to the existing `ReadableStreamBYOBReader.read(view)` method. The method already accepts an `ArrayBufferView` into which it reads data, but currently does not guarantee how many elements are written before the read resolves. By specifying a `min` value, you can require that the stream wait until at least that many elements are available before resolving the read. This improves upon the current behavior, where reads may resolve with fewer elements than the view can hold.

### Http cookie prefix

In some cases, it's important to distinguish on the server side between cookies set by the server and those set by the client. One such case involves cookies normally always set by the server. However, unexpected code (such as an XSS exploit, a malicious extension, or a commit from a confused developer) might set them on the client. This proposal adds a signal that lets servers make such a distinction. More specifically, it defines the `__Http` and `__HostHttp` prefixes, which ensure a cookie is not set on the client side using script.

### Local network access restrictions

Chrome 140 restricts the ability to make requests to the user's local network, requiring a permission prompt. A local network request is any request from a public website to a local IP address or loopback, or from a local website (such as an intranet) to loopback. Gating the ability for websites to perform these requests behind a permission mitigates the risk of cross-site request forgery attacks against local network devices, such as routers. It also reduces the ability of sites to use these requests to fingerprint the user's local network. This permission is restricted to secure contexts. If granted, the permission also relaxes mixed content blocking for local network requests, since many local devices cannot obtain publicly trusted TLS certificates for various reasons.

Learn more in [New permission prompt for Local Network Access](/blog/local-network-access).

**Note:** An origin trial is available to temporarily opt out of this behavior.

### Enable SharedWorker scripts to inherit controller for blob script URLs

The specification states that workers should inherit controllers for the blob URL. However, existing code allows only dedicated workers to inherit the controller; shared workers don't. This fixes Chrome's behavior to align with the specification. The `SharedWorkerBlobURLFixEnabled` enterprise policy controls this feature.

### Add `ServiceWorkerStaticRouterTimingInfo`

This feature adds timing information for the ServiceWorker Static routing API, exposed in the navigation timing API and resource timing API for developer use. ServiceWorker provides timing information to mark certain points in time.

This feature adds two pieces of Static routing API-relevant timing information:

  * `RouterEvaluationStart`: Time to start matching a request with registered router rules.
  * `CacheLookupStart`: Time to start looking up the cache storage if the source is `"cache"`.

Additionally, this feature adds two pieces of router source information: the matched router source and the final router source.

### Enable Web Authentication conditional create on Android (not shipping)

**Note:** This post previously stated that this feature was shipping on Android. This was incorrect and the feature is not included in this beta.

## Isolated Web Apps

### Introduce the Controlled Frame API

This feature adds a Controlled Frame API available only to Isolated Web Apps (IWAs). Like similarly-named APIs on other platforms, Controlled Frame allows embedding all content, even third-party content that cannot be embedded in `<iframe>`. Controlled Frame also allows controlling embedded content with a collection of API methods and events. For more information about Isolated Web Apps, see the [Isolated Web Apps explainer](https://github.com/WICG/isolated-web-apps/blob/main/README.md).

## New origin trials

In Chrome 140 you can opt into the following new [origin trials](/docs/web-platform/origin-trials).

### Add the `clipboardchange` event

The `clipboardchange` event fires whenever a web app or any other system application changes the system clipboard contents. This allows web apps like remote desktop clients to keep their clipboards synchronized with the system clipboard. It provides an efficient alternative to polling the clipboard with JavaScript for changes.

### Enable incoming call notifications

This feature extends the Notifications API to allow installed PWAs to send incoming call notifications—notifications with call-styled buttons and a ringtone. This extension helps VoIP web apps create more engaging experiences by making it easier for users to recognize and answer calling notifications. Additionally, this feature helps bridge the gap between native and web implementations of apps that have them both.

### Introduce the Crash Reporting key-value API

This feature introduces a new key-value API, tentatively `window.crashReport`, backed by a per-document map that holds data appended to crash reports.

The data placed in this API's backing map is sent in the `CrashReportBody` if any renderer process crashes occur on the site. This lets developers debug what specific state in their application might be causing a given crash.

## Deprecations and removals

This version of Chrome introduces the deprecations and removals listed below. Visit ChromeStatus.com for lists of planned deprecations, current deprecations and previous removals.

This release of Chrome deprecates one feature.

### Deprecate special font size rules for `<h1>` within some elements

The HTML spec contains a list of special rules for `<h1>` tags nested within `<article>`, `<aside>`, `<nav>`, or `<section>` elements.

These special rules are deprecated because they cause accessibility issues. Namely, they visually reduce the font size for nested `<h1>`s so that they _look_ like `<h2>`s, but nothing in the accessibility tree reflects this visual change.

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-08-06 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-08-06 UTC."],[],[]] 
