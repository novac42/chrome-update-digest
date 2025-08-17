# Chrome 133 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/133

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Docs ](https://developer.chrome.com/docs)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 133

Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** February 4th, 2025

Unless otherwise noted, the following changes apply to Chrome 133 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 133](/blog/new-in-chrome-133). 

## HTML and DOM

### The hint value of the popover attribute

The Popover API specifies the behavior for two values of the popover attribute: auto and manual. This feature describes a third value, `popover=hint`. Hints, which are most often associated with "tooltip" type behaviors, have slightly different behaviors. Primarily, the difference is that a hint is subordinate to auto when opening nested stacks of popovers. So it is possible to open an unrelated hint popover while an existing stack of auto popovers stays open.

The canonical example is that a `<select>` picker is open (`popover=auto`) and a hover-triggered tooltip (`popover=hint`) is shown. That action does not close the `<select>` picker.

[Tracking bug #1416284](https://issues.chromium.org/issues/1416284) | [ChromeStatus.com entry](https://chromestatus.com/feature/5073251081912320)

### Popover invoker and anchor positioning improvements

Adds an imperative way to set invoker relationships between popovers with `popover.showPopover({source})`. Enables invoker relationships to create implicit anchor element references.

[Tracking bug #364669918](https://issues.chromium.org/issues/364669918) | [ChromeStatus.com entry](https://chromestatus.com/feature/5120638407409664)

### Popover nested inside invoker shouldn't re-invoke it

In the following case clicking the button properly activates the popover, however, clicking on the popover itself after that shouldn't close the popover.
    
    
    <button popovertarget=foo>Activate
      <div popover id=foo>Clicking me shouldn't close me</div>
    </button>
    

Previously this happened, because the popover click bubbles to the `<button>` and activates the invoker, which toggles the popover closed. This has now been changed to the expected behavior.

[Tracking bug #https://crbug.com/379241451](https://issues.chromium.org/issues/https://crbug.com/379241451) | [ChromeStatus.com entry](https://chromestatus.com/feature/4821788884992000)

## CSS

### CSS advanced `attr()` function

Implements the augmentation to `attr()` specified in CSS Level 5, which allows types besides `<string>` and use in all CSS properties (in addition to the existing support for the pseudo-element content).

[MDN attr()](https://developer.mozilla.org/en-US/docs/Web/CSS/attr) | [Tracking bug #246571](https://issues.chromium.org/issues/246571) | [ChromeStatus.com entry](https://chromestatus.com/feature/4680129030651904) | [Spec](https://drafts.csswg.org/css-values-5/#attr-notation)

### CSS `:open` pseudo-class

The `:open` pseudo-class matches `<dialog>` and `<details>` when they are in their open state, and matches `<select>` and `<input>` when they are in modes which have a picker and the picker is showing.

[Tracking bug #324293874](https://issues.chromium.org/issues/324293874) | [ChromeStatus.com entry](https://chromestatus.com/feature/5085419215781888) | [Spec](https://drafts.csswg.org/selectors-4/#open-state)

### CSS scroll state container queries

Use container queries to style descendants of containers based on their scroll state.

The query container is either a scroll container, or an element affected by the scroll position of a scroll container. The following states can be queried:

  * `stuck`: A sticky positioned container is stuck to one of the edges of the scroll box.
  * `snapped`: A scroll snap aligned container is currently snapped horizontally or vertically.
  * `scrollable`: Whether a scroll container can be scrolled in a queried direction.

A new container-type: `scroll-state` lets containers be queried.

[Tracking bug #40268059](https://issues.chromium.org/issues/40268059) | [ChromeStatus.com entry](https://chromestatus.com/feature/5072263730167808) | [Spec](https://www.w3.org/TR/css-conditional-5/#scroll-state-container)

### CSS `text-box`, `text-box-trim`, and `text-box-edge`

To achieve optimal balance of text content, the `text-box-trim` and text-box-edge properties, along with the text-box shorthand property, make finer control of vertical alignment of text possible.

The `text-box-trim` property specifies the sides to trim, above or below, and the `text-box-edge` property specifies how the edge should be trimmed.

These properties let you control vertical spacing precisely by using the font metrics.

[Tracking bug #1411581](https://issues.chromium.org/issues/1411581) | [ChromeStatus.com entry](https://chromestatus.com/feature/5174589850648576) | [Spec](https://drafts.csswg.org/css-inline-3/#text-edges)

### Web APIs

### `Animation.overallProgress`

Provides developers with a convenient and consistent representation of how far along an animation has advanced across its iterations and regardless of the nature of its timeline. Without the `overallProgress` property, you need to manually compute how far an animation has advanced, factoring in the number of iterations of the animation and whether the `currentTime` of the animation is a percentage of total time (as in the case of scroll-driven animations) or an absolute time quantity (as in the case of time-driven animations).

[Tracking bug #40914396](https://issues.chromium.org/issues/40914396) | [ChromeStatus.com entry](https://chromestatus.com/feature/5083257285378048) | [Spec](https://drafts.csswg.org/web-animations-2/#the-overall-progress-of-an-animation)

### The `pause()` method of the `Atomics` object

Adds the `pause()` method to the `Atomics` namespace object, to hint the CPU that the current code is executing a spinlock.

[ChromeStatus.com entry](https://chromestatus.com/feature/5106098833719296) | [Spec](https://tc39.es/proposal-atomics-microwait)

### CSP hash reporting for scripts

Complex web applications often need to keep track of the subresources that they download, for security purposes.

In particular, upcoming industry standards and best practices (for example, PCI-DSS v4) require that web applications keep an inventory of all the scripts they download and execute.

This feature builds on CSP and the Reporting API to report the URLs and hashes (for CORS/same-origin) of all the script resources that the document loads.

[Tracking bug #377830102](https://issues.chromium.org/issues/377830102) | [ChromeStatus.com entry](https://chromestatus.com/feature/6337535507431424)

### DOM state-preserving move

Adds a DOM primitive (`Node.prototype.moveBefore`) that lets you move elements around a DOM tree, without resetting the element's state.

When moving instead of removing and inserting, following state such as the following is preserved:

  * `<iframe>` elements remain loaded.
  * The active element remains focus.
  * Popovers, fullscreen, and modal dialogs remain open.
  * CSS transitions and animations continue.

[ChromeStatus.com entry](https://chromestatus.com/feature/5135990159835136)

### Expose `attributionsrc` attribute on `<area>`.

Aligns exposure of the `attributionsrc` attribute on `<area>` with the existing processing behavior of the attribute, even when it wasn't exposed.

Additionally, it makes sense to support the attribute on `<area>`, as that element is a first-class navigation surface, and Chrome already supports this on the other surfaces of `<a>` and `window.open`.

[Tracking bug #379275911](https://issues.chromium.org/issues/379275911) | [ChromeStatus.com entry](https://chromestatus.com/feature/6547509428879360) | [Spec](https://wicg.github.io/attribution-reporting-api/#html-monkeypatches)

### The `FileSystemObserver` interface

The `FileSystemObserver` interface notifies websites of changes to the file system. Sites observe changes to files and directories, to which the user has previously granted permission, in the user's local device, or in the Bucket File System (also known as the Origin Private File System), and are notified of basic change info, such as the change type.

[Tracking bug #40105284](https://issues.chromium.org/issues/40105284) | [ChromeStatus.com entry](https://chromestatus.com/feature/4622243656630272)

### Multiple import maps

Import maps currently have to load before any ES module and there can only be a single import map per document. That makes them fragile and potentially slow to use in real-life scenarios: Any module that loads before them breaks the entire app, and in apps with many modules they become a large blocking resource, as the entire map for all possible modules needs to load first.

This feature enables multiple import maps per document, by merging them in a consistent and deterministic way.

[ChromeStatus.com entry](https://chromestatus.com/feature/5121916248260608)

### Storage Access Headers

Offers an alternate way for authenticated embeds to opt in for unpartitioned cookies. These headers indicate whether unpartitioned cookies are (or can be) included in a given network request, and allow servers to activate 'storage-access' permissions they have already been granted. Giving an alternative way to activate the 'storage-access' permission allows usage by non-iframe resources, and can reduce latency for authenticated embeds.

[Tracking bug #329698698](https://issues.chromium.org/issues/329698698) | [ChromeStatus.com entry](https://chromestatus.com/feature/6146353156849664) | [Spec](https://privacycg.github.io/storage-access-headers)

### Support creating `ClipboardItem` with `Promise<DOMString>`

The `ClipboardItem`, which is the input to the async clipboard `write()` method, now accepts string values in addition to Blobs in its constructor. `ClipboardItemData` can be a Blob, a string, or a Promise that resolves to either a Blob or a string.

[Tracking bug #40766145](https://issues.chromium.org/issues/40766145) | [ChromeStatus.com entry](https://chromestatus.com/feature/4926138582040576) | [Spec](https://www.w3.org/TR/clipboard-apis/#typedefdef-clipboarditemdata)

### WebAssembly Memory64

The memory64 proposal adds support for linear WebAssembly memories with size larger than 2^32 bits. It provides no new instructions, but instead extends the existing instructions to allow 64-bit indexes for memories and tables.

[ChromeStatus.com entry](https://chromestatus.com/feature/5070065734516736) | [Spec](https://github.com/WebAssembly/memory64/blob/main/proposals/memory64/Overview.md)

### Web Authentication API: `PublicKeyCredential` `getClientCapabilities()` method

The `PublicKeyCredential` `getClientCapabilities()` method lets you determine which WebAuthn features are supported by the user's client. The method returns a list of supported capabilities, allowing developers to tailor authentication experiences and workflows based on the client's specific functionality.

[Tracking bug #360327828](https://issues.chromium.org/issues/360327828) | [ChromeStatus.com entry](https://chromestatus.com/feature/5128205875544064) | [Spec](https://w3c.github.io/webauthn/#sctn-getClientCapabilities)

### X25519 algorithm of the Web Cryptography API

The "X25519" algorithm provides tools to perform key agreement using the X25519 function specified in [RFC7748]. The "X25519" algorithm identifier can be used in the SubtleCrypto interface to access the implemented operations: generateKey, importKey, exportKey, deriveKey and deriveBits.

[Tracking bug #378856322](https://issues.chromium.org/issues/378856322) | [ChromeStatus.com entry](https://chromestatus.com/feature/6291245926973440) | [Spec](https://w3c.github.io/webcrypto/#x25519)

## Performance

### Freezing on Energy Saver

When Energy Saver is active, Chrome will freeze a "browsing context group" that has been hidden and silent for over five minutes if any subgroup of same-origin frames within it exceeds a CPU usage threshold, unless it:

  * Provides audio- or video-conferencing functionality (detected by identifying microphone, camera or screen/window/tab capture or an RTCPeerConnection with an 'open' RTCDataChannel or a 'live' MediaStreamTrack).
  * Controls an external device (detected with use of WebUSB, Web Bluetooth, WebHID, or Web Serial).
  * Holds a Web Lock or an IndexedDB connection that blocks a version update or a transaction on a different connection.
  * Freezing consists of pausing execution. It is formally defined in the Page Lifecycle API.

The CPU usage threshold will be calibrated to freeze approximately 10% of background tabs when Energy Saver is active.

[Tracking bug #325954772](https://issues.chromium.org/issues/325954772) | [ChromeStatus.com entry](https://chromestatus.com/feature/5158599457767424)

### Expose coarsened cross-origin `renderTime` in element timing and LCP (regardless of `Timing-Allow-Origin`)

Element timing and LCP entries have a `renderTime` attribute, aligned with the first frame in which an image or text was painted.

This attribute is currently guarded for cross-origin images by requiring a `Timing-Allow-Origin` header on the image resource. However, that restriction is easy to work around (for example, by displaying a same-origin and cross-origin image in the same frame).

Since this has been a source of confusion, we instead plan to remove this restriction, and instead coarsen all render times by 4 ms when the document is not cross-origin-isolated. This is seemingly coarse enough to avoid leaking any useful decoding-time information about cross-origin images.

[Tracking bug #373263977](https://issues.chromium.org/issues/373263977) | [ChromeStatus.com entry](https://chromestatus.com/feature/5128261284397056) | [Spec](https://w3c.github.io/paint-timing/#mark-paint-timing)

### Revert `responseStart` and introduce `firstResponseHeadersStart`

With 103 Early Hints enabled, responses have two timestamps:

  * When the Early Hints arrive (103)
  * When the final headers arrive (e.g. 200)
  * When Chrome 115 shipped `firstInterimResponseStart` to allow measuring of these two timestamps, we also changed the meaning of `responseStart` (used by Time to First Byte (TTFB)) to mean "the final headers". This created a web compatibility issue with browsers and tools that did not make a similar change for this commonly used metric.

Chrome 133 reverts this `responseStart` change to resolve this compatibility issue and instead introduces `firstResponseHeadersStart` to allow sites to measure the time to the final headers, while retaining the original definition of TTFB.

[Tracking bug #40251053](https://issues.chromium.org/issues/40251053) | [ChromeStatus.com entry](https://chromestatus.com/feature/5158830722514944) | [Spec](https://w3c.github.io/resource-timing/#dom-performanceresourcetiming-finalresponseheadersstart)

## Rendering and graphics

### WebGPU: 1-component vertex formats (and unorm8x4-bgra)

Adds additional vertex formats not present in the initial release of WebGPU due to lack of support or old macOS versions (which are no longer supported by any browser). The 1-component vertex formats let applications request only the necessary data when previously they had to request at least two times more for 8 and 16-bit data types. The unorm8x4-bgra format makes it slightly more convenient to load BGRA-encoded vertex colors while keeping the same shader.

[Tracking bug #376924407](https://issues.chromium.org/issues/376924407) | [ChromeStatus.com entry](https://chromestatus.com/feature/4609840973086720)

## Origin trials

### Opt out of freezing on Energy Saver

This opt out trial lets sites opt out from the freezing on Energy Saver behavior that ships in Chrome 133.

[Origin Trial](/origintrials#/register_trial/4254212798004854785) | [Tracking bug #325954772](https://issues.chromium.org/issues/325954772) | [ChromeStatus.com entry](https://chromestatus.com/feature/5158599457767424) | [Spec](https://wicg.github.io/page-lifecycle)

### Reference Target for Cross-root ARIA

Reference Target is a feature to enable using IDREF attributes such as `for` and `aria-labelledby` to refer to elements inside a component's shadow DOM, while maintaining encapsulation of the internal details of the shadow DOM. The main goal of this feature is to enable ARIA to work across shadow root boundaries.

A component can specify an element in its shadow tree to act as its "reference target". When the host component is the target of a IDREF like a label's `for` attribute, the reference target becomes the effective target of the label.

The shadow root specifies the ID of the target element inside the shadow DOM. This is done either in JavaScript with the `referenceTarget` attribute on the `ShadowRoot` object, or in HTML markup using the `shadowrootreferencetarget` attribute on the `<template>` element.

[Origin Trial](/origintrials#/register_trial/2164542570904944641) | [ChromeStatus.com entry](https://chromestatus.com/feature/5188237101891584)

## Deprecations and removals

### Deprecate WebGPU limit `maxInterStageShaderComponents`

The `maxInterStageShaderComponents limit` is deprecated due to a combination of factors. The intended removal date in Chrome 135.

  * Redundancy with `maxInterStageShaderVariables`: This limit already serves a similar purpose, controlling the amount of data passed between shader stages.
  * Minor discrepancies: While there are slight differences in how the two limits are calculated, these differences are minor and can be effectively managed within the `maxInterStageShaderVariables` limit.
  * Simplification: Removing `maxInterStageShaderComponents` streamlines the shader interface and reduces complexity for developers. Instead of managing two separate limits with subtle differences, they can focus on the more appropriately named and comprehensive `maxInterStageShaderVariables`.

[ChromeStatus.com entry](https://chromestatus.com/feature/4853767735083008)

### Remove `<link rel=prefetch>` five-minute rule

Previously, when a resource was prefetched using `<link rel=prefetch>`, Chrome ignored its cache semantics (namely `max-age` and `no-cache`) for the first use within five minutes, to avoid refetching. Now, Chrome removes this special case and uses normal HTTP cache semantics.

This means web developers need to include appropriate caching headers (Cache-Control or Expires) to see benefits from `<link rel=prefetch>`.

This also affects the nonstandard `<link rel=prerender>`.

[Tracking bug #40232065](https://issues.chromium.org/issues/40232065) | [ChromeStatus.com entry](https://chromestatus.com/feature/5087526916718592)

### Remove Chrome Welcome page triggering with initial prefs first run tabs

Including `chrome://welcome` in the `first_run_tabs` property of the `initial_preferences` file will now have no effect. This is removed because that page is redundant with the First Run Experience that triggers on desktop platforms.

[ChromeStatus.com entry](https://chromestatus.com/feature/5118328941838336)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-02-04 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-02-04 UTC."],[],[]] 
