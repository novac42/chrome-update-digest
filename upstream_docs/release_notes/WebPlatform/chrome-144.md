# Chrome 144 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/144

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Docs ](https://developer.chrome.com/docs)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 144 Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** January 13th, 2026

Unless otherwise noted, the following changes apply to Chrome 144 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 144](/blog/new-in-chrome-144). 

## CSS and UI

### CSS find-in-page highlight pseudos

This feature exposes _find-in-page_ search result styling to authors as a highlight pseudo-element, similar to selection and spelling errors. This lets developers change foreground and background colors or add text decorations. This is especially useful if browser defaults have insufficient contrast with page colors or are otherwise unsuitable.

[Tracking bug #339298411](https://issues.chromium.org/issues/339298411) | [ChromeStatus.com entry](https://chromestatus.com/feature/5195073796177920) | [Spec](https://drafts.csswg.org/css-pseudo-4/#selectordef-search-text)

### Non-tree-scoped container-name matching

Ignore tree-scope when matching `container-name` for `@container` queries.

Previously, `container-name` matching for container queries used tree-scoped names or references for matching. This meant the same name didn't match if the `@container` rule and the `container-type` property originated from different trees, such that the `container-type` declaration came from an inner shadow tree.

With this change, container names match regardless of `@container` rule or `container-type` declaration origins.

[Tracking bug #440049800](https://issues.chromium.org/issues/440049800) | [ChromeStatus.com entry](https://chromestatus.com/feature/5194034339512320) | [Spec](https://drafts.csswg.org/css-conditional-5/#container-name)

### CSS anchor positioning with transforms

When an anchor-positioned element is tethered against an anchor that has a transform (or is contained by an element with a transform), resolve `anchor()` and `anchor-size()` functions against the bounding box of the transformed anchor.

[Tracking bug #382294252](https://issues.chromium.org/issues/382294252) | [ChromeStatus.com entry](https://chromestatus.com/feature/5201048700583936) | [Spec](https://drafts.csswg.org/css-anchor-position-1/#anchor-position-size)

### CSS `caret-shape` property

The caret's shape in native applications is most commonly a vertical bar, an underscore, or a rectangular block. Additionally, the shape often varies depending on the input mode, for example, insert or replace. The CSS `caret-shape` property lets sites choose one of these shapes for the caret inside editable elements, or leave the choice to the browser. The recognized property values are `auto`, `bar`, `block`, and `underscore`.

[Tracking bug #353713061](https://issues.chromium.org/issues/353713061) | [ChromeStatus.com entry](https://chromestatus.com/feature/6106160780017664) | [Spec](https://drafts.csswg.org/css-ui/#caret-shape)

### SVG2 CSS cascading

Align the Chrome implementation with the SVG2 specification for matching CSS rules in `<use>` element trees.

Match selectors against the `<use>` instantiation elements instead of the originating element subtree. This means selectors no longer match ancestor and sibling elements outside the cloned subtree. More importantly, state selectors, for example, `:hover`, now start matching in `<use>` instances.

[Tracking bug #40550039](https://issues.chromium.org/issues/40550039) | [ChromeStatus.com entry](https://chromestatus.com/feature/5134266027606016) | [Spec](https://www.w3.org/TR/SVG2/struct.html#UseElement)

### Respect `overscroll-behavior` on non-scrollable scroll containers

The `overscroll-behavior` property applies to all scroll container elements, regardless of whether those elements currently have overflowing content or are user scrollable. Developers can use `overscroll-behavior` to prevent scroll propagation on an `overflow: hidden` backdrop or an `overflow: auto` element without considering whether it will currently be overflowing.

[ChromeStatus.com entry](https://chromestatus.com/feature/5129635997941760) | [Spec](https://www.w3.org/TR/css-overscroll-1/#propdef-overscroll-behavior)

### Respect `overscroll-behavior` for keyboard scrolls

When you set `overscroll-behavior` to a value other than `auto`, the browser shouldn't perform scroll chaining. The browser respects this for mouse or touch scrolling, but keyboard scrolls ignored it. This change makes keyboard scrolling also respect `overscroll-behavior`.

[Tracking bug #41378182](https://issues.chromium.org/issues/41378182) | [ChromeStatus.com entry](https://chromestatus.com/feature/5099117340655616) | [Spec](https://www.w3.org/TR/css-overscroll-1)

### `@scroll-state` `scrolled` support

Lets developers style descendants of containers based on the most recent scrolling direction.

[Tracking bug #414556050](https://issues.chromium.org/issues/414556050) | [ChromeStatus.com entry](https://chromestatus.com/feature/5083137520173056) | [Spec](https://drafts.csswg.org/css-conditional-5/#scrolled)

### Side-relative syntax for `background-position-x/y` longhands

Defines the background image position relative to one of its edges.

This syntax gives developers more flexible and responsive mechanisms to define the background image position, instead of using fixed values that need adaptation to the window or frame size.

This feature also applies to the `-webkit-mask-position` property to ensure web compatibility.

[Tracking bug #40468636](https://issues.chromium.org/issues/40468636) | [ChromeStatus.com entry](https://chromestatus.com/feature/5073321259565056) | [Spec](https://drafts.csswg.org/css-backgrounds-4/#background-position-longhands)

### View transitions `waitUntil()` method

View transitions automatically construct a pseudo-element tree to display and animate participating elements in the transition. Per the specification, this subtree is constructed when the view transition starts animating and is destroyed when the animations associated with all view transition pseudo-elements are in the finished state (or more precisely, in a non-running, non-paused state).

This works for most cases and provides a seamless experience for developers. However, for more advanced cases, this is insufficient because developers sometimes want the view transition pseudo-tree to persist beyond the animation finish state.

One example is tying view transitions with Scroll Driven Animations. When a scroll timeline controls the animation, the subtree shouldn't be destroyed when the animations finish because scrolling back should still animate the pseudo elements.

To enable advanced uses of view transition, this intent adds a `waitUntil()` function on the `ViewTransition` object that takes a promise. This promise delays destruction of the pseudo-tree until it settles.

[Tracking bug #346976175](https://issues.chromium.org/issues/346976175) | [ChromeStatus.com entry](https://chromestatus.com/feature/4812903832223744) | [Spec](https://drafts.csswg.org/css-view-transitions-2/#dom-viewtransition-waituntil)

## Device

### `XRVisibilityMaskChange`

Adds an `XRVisibilityMaskChange` event that provides a list of vertices and a list of indices to represent the mesh of the visible portion of the user's viewport. This data can then limit the amount of the viewport drawn to, which improves performance. To better support this event, `XRView` objects are also given unique identifiers to allow easier pairing with the associated masks. This extends the core WebXR specification.

[Tracking bug #450538226](https://issues.chromium.org/issues/450538226) | [ChromeStatus.com entry](https://chromestatus.com/feature/5073760055066624) | [Spec](https://immersive-web.github.io/webxr/#xrvisibilitymaskchangeevent-interface)

## DOM

### The `<geolocation>` element

Introduces the `<geolocation>` element, a declarative, user-activated control for accessing the user's location. It streamlines the user and developer journey by handling the permission flow and directly providing location data to the site. This often eliminates the need for a separate JavaScript API call.

This addresses the long-standing problem of permission prompts triggering directly from JavaScript without a strong signal of user intent. By embedding a browser-controlled element in the page, the user's click provides a clear, intentional signal. This enables a better prompt UX and, crucially, provides a recovery path for users who previously denied the permission.

**Note:** This feature was previously developed and tested in an origin trial as the more generic `<permission>` element. Based on feedback from developers and other browser vendors, it evolved into the capability-specific `<geolocation>` element to provide a more tailored and powerful developer experience.

[Tracking bug #435351699](https://issues.chromium.org/issues/435351699) | [ChromeStatus.com entry](https://chromestatus.com/feature/5125006551416832) | [Spec](https://wicg.github.io/PEPC/permission-elements.html)

## Graphics

### WebGPU: Uniform buffer standard layout

Uniform buffers declared in WGSL shaders are no longer required to have 16-byte alignment on array elements or to pad nested structure offsets to a multiple of 16 bytes.

[Tracking bug #452662924](https://issues.chromium.org/issues/452662924) | [ChromeStatus.com entry](https://chromestatus.com/feature/6680245553987584) | [Spec](https://www.w3.org/TR/WGSL/#language_extension-uniform_buffer_standard_layout)

### WebGPU: `subgroup_id` feature

The `subgroup_id` and `num_subgroups` built-in values are available when the subgroups extension is enabled.

[Tracking bug #454654255](https://issues.chromium.org/issues/454654255) | [ChromeStatus.com entry](https://chromestatus.com/feature/5072447137251328) | [Spec](https://www.w3.org/TR/WGSL/#language_extension-subgroup_id)

## JavaScript

### Temporal in ECMA262

The Temporal API in ECMA262 is a new API that provides standard objects and functions for working with dates and times. `Date` has been a long-standing pain point in ECMAScript. This proposes `Temporal`, a global `Object` that acts as a top-level namespace (similar to `Math`), which brings a modern date and time API to the ECMAScript language.

[Tracking bug #detail?id=11544](https://issues.chromium.org/issues/detail?id=11544) | [ChromeStatus.com entry](https://chromestatus.com/feature/5668291307634688) | [Spec](https://tc39.es/proposal-temporal/)

### Support `ping`, `hreflang`, `type`, and `referrerPolicy` for `SVGAElement`

Adds support for `ping`, `hreflang`, `type`, and `referrerPolicy` attributes on `SVGAElement`, aligning its behavior with `HTMLAnchorElement` for consistent link handling across HTML and SVG.

[Tracking bug #40589293](https://issues.chromium.org/issues/40589293) | [ChromeStatus.com entry](https://chromestatus.com/feature/5140707648077824) | [Spec](https://svgwg.org/svg2-draft/linking.html#InterfaceSVGAElement)

### Mirroring of RTL MathML operators

Supports character-level and glyph-level mirroring when rendering MathML operators in right-to-left mode.

When using RTL mode, some operators can be mirrored by changing them to another code point. For example, a right parenthesis becomes a left parenthesis. This is character-level mirroring, with equivalences defined by Unicode's `Bidi_Mirrored` property.

Some operators have no appropriate mirroring character. Glyph-level mirroring applies in this case, with the `rtlm` font feature, where another glyph can replace it in a mirrored context. Some existing implementations mirror the original glyph directly, but this might change the meaning for asymmetrical characters, for example, the clockwise contour integral.

[Tracking bug #40120782](https://issues.chromium.org/issues/40120782) | [ChromeStatus.com entry](https://chromestatus.com/feature/6317308531965952) | [Spec](https://w3c.github.io/mathml-core/#layout-of-operators)

### The `clipboardchange` event

The `clipboardchange` event fires whenever a web app or any other system application changes the system clipboard contents. This lets web apps, for example, remote desktop clients, keep their clipboards synchronized with the system clipboard. It provides an efficient alternative to polling the clipboard (using JavaScript) for changes.

[Tracking bug #41442253](https://issues.chromium.org/issues/41442253) | [ChromeStatus.com entry](https://chromestatus.com/feature/5085102657503232) | [Spec](https://github.com/w3c/clipboard-apis/pull/239)

## Permissions

### User-Agent Client Hints `ch-ua-high-entropy-values` permissions policy

Adds support for a `ch-ua-high-entropy-values` permissions policy that enables a top-level site to restrict which documents can collect high-entropy client hints with the `navigator.userAgentData.getHighEntropyValues()` JavaScript API.

Restricting collection of high-entropy hints over HTTP is possible through existing per-client-hint permissions policies.

[Tracking bug #385161047](https://issues.chromium.org/issues/385161047) | [ChromeStatus.com entry](https://chromestatus.com/feature/6176703867781120) | [Spec](https://wicg.github.io/ua-client-hints/#ch-ua-high-entropy-values)

## Performance

### Performance and Event Timing: `interactionCount`

The Event Timing API is part of the Performance Timeline and measures the performance of user interactions. Certain events have an `interactionId` value assigned to them. This is useful for grouping related interactions based on common physical user inputs or gestures.

This feature adds a `performance.interactionCount` property, which is the total number of interactions that occurred on the page.

In particular, this feature is useful for computing the Interaction to Next Paint (INP) metric value. This requires knowing the total number of interactions to compute a high percentile score (p98 for pages with more than 50 total interactions).

This feature has been specified for a long time, was prototyped in Chromium a long time ago but never shipped, is part of Interop 2025, and is available in other browsers.

**Note:** A more powerful `performance.eventCounts` map for specific events exists, but you can't accurately map event counts to interaction counts.

[ChromeStatus.com entry](https://chromestatus.com/feature/5153386492198912) | [Spec](https://www.w3.org/TR/event-timing/#dom-performance-interactioncount)

## User input

### Interoperable pointer and mouse boundary events after DOM changes

After an event target is removed from the DOM, the logical target of the pointer, as implied by the Pointer and Mouse boundary events (that is, `over`, `out`, `enter`, and `leave` events), should be the nearest ancestor still attached to the DOM.

The PEWG recently reached consensus on this behavior.

Chrome tracked a node even after it was removed from the DOM. As a result, if the pointer moves to a new node B after the hit-test node A is removed from the DOM, the boundary event sequence (`pointerover`, `pointerout`, `pointerenter`, `pointerleave` events, and the corresponding mouse events) implied a pointer movement from A to B. As per the new consensus, the event sequence implies a pointer movement from the "parent of A" to B.

[Tracking bug #1147998](https://issues.chromium.org/issues/1147998) | [ChromeStatus.com entry](https://chromestatus.com/feature/6266812908175360) | [Spec](https://www.w3.org/TR/uievents/#events-mouseevent-event-order)

### Pointer lock on Android

Provides access to raw mouse movement by locking the target of mouse events to a single element and hiding the mouse cursor.

[Tracking bug #40290045](https://issues.chromium.org/issues/40290045) | [ChromeStatus.com entry](https://chromestatus.com/feature/6739764319485952) | [Spec](https://www.w3.org/TR/pointerlock-2)

## WebRTC

### `RTCDegradationPreference` enum value `maintain-framerate-and-resolution`

`maintain-framerate-and-resolution` disables WebRTC's internal video adaptation. This lets the application implement its own adaptation logic and prevents interference from the internal adaptation.

From the WebRTC MediaStreamTrack Content Hints specification:

Maintain framerate and resolution regardless of video quality. The user agent shouldn't prefer reducing the framerate or resolution for quality and performance reasons, but might drop frames before encoding if necessary not to overuse network and encoder resources.

[Tracking bug #450044904](https://issues.chromium.org/issues/450044904) | [ChromeStatus.com entry](https://chromestatus.com/feature/5156290162720768) | [Spec](https://www.w3.org/TR/mst-content-hint/#dom-rtcdegradationpreference-maintain-framerate-and-resolution)

## Isolated Web Apps (IWA)

### Multicast Support for Direct Sockets API.

This feature lets Isolated Web Apps (IWAs) subscribe to multicast groups, receive User Datagram Protocol (UDP) packets from them, and specify additional parameters when sending UDP packets to multicast addresses.

[ChromeStatus.com entry](https://chromestatus.com/feature/5073740211814400) | [Spec](https://github.com/WICG/direct-sockets/pull/79)

## Origin trials

### Enhanced Canvas API `TextMetrics`

Expands the `TextMetrics` Canvas API to support selection rectangles, bounding box queries, and glyph cluster-based operations.

This new functionality enables complex text editing applications with accurate selection, caret positioning, and hit testing. Additionally, cluster-based rendering facilitates sophisticated text effects, for example, independent character animations and styling.

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/1646628613757337601) | [Tracking bug #341213359](https://issues.chromium.org/issues/341213359) | [ChromeStatus.com entry](https://chromestatus.com/feature/5075532483657728) | [Spec](https://github.com/whatwg/html/pull/11000)

### Context-aware media elements

Context-aware media elements, are a declarative, user-activated control for accessing the starting and interacting with media streams.

This addresses the long-standing problem of permission prompts being triggered directly from JavaScript without a strong signal of user intent. By embedding a browser-controlled element in the page, the user's click provides a clear, intentional signal. This enables a much better prompt UX and, crucially, provides a recovery path for users who have previously denied the permission.

**Note:** This feature was previously developed and tested in an Origin Trial as the more generic `<permission>` element. Based on feedback from developers and other browser vendors, it has evolved into capability-specific elements to provide a more tailored and powerful developer experience.

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/3736298840857247745) | [Tracking bug #443013457](https://issues.chromium.org/issues/443013457) | [ChromeStatus.com entry](https://chromestatus.com/feature/4926233538330624) | [Spec](https://wicg.github.io/PEPC/permission-elements.html)

## Deprecations and removals

### Deprecate and remove: Private Aggregation API

The Private Aggregation API is a generic mechanism for measuring aggregate, cross-site data in a privacy-preserving manner. It was originally designed for a future without third-party cookies.

Following Chrome's announcement that the current approach to third-party cookies will be maintained, Chrome plans to deprecate and remove the Private Aggregation API (along with certain other Privacy Sandbox APIs, as outlined on the Privacy Sandbox feature status page). This API is only exposed through the Shared Storage and Protected Audience APIs, which are also planned for deprecation and removal. Therefore, no additional work is required for Private Aggregation.

[ChromeStatus.com entry](https://chromestatus.com/feature/4683382919397376) | [Spec](https://patcg-individual-drafts.github.io/private-aggregation-api)

### Deprecate and Remove: Shared Storage API

The Shared Storage API is a privacy-preserving web API that enables storage not partitioned by a first-party site.

Following Chrome's announcement that the current approach to third-party cookies will be maintained, Chrome plans to deprecate and remove the Shared Storage API (along with certain other Privacy Sandbox APIs, as outlined on the Privacy Sandbox feature status page).

[Tracking bug #462465887](https://issues.chromium.org/issues/462465887) | [ChromeStatus.com entry](https://chromestatus.com/feature/5076349064708096) | [Spec](https://wicg.github.io/shared-storage)

### Deprecate and Remove Protected Audience

The Protected Audience API provides a method of interest-group advertising without third-party cookies or user tracking across sites.

Following Chrome's announcement that the current approach to third-party cookies will be maintained, Chrome plans to deprecate and remove the Protected Audience API (along with certain other Privacy Sandbox APIs, as outlined on the Privacy Sandbox feature status page).

[ChromeStatus.com entry](https://chromestatus.com/feature/6552486106234880) | [Spec](https://wicg.github.io/turtledove)

### Externally loaded entities in XML parsing

Chrome synchronously fetches external XML entities or DTDs and incorporates them into parsing under specific circumstances. This document proposes removing this functionality.

For example, `http/tests/security/contentTypeOptions/xml-external-entity.xml` shows how external entities can be defined in the trailing part of the `DOCTYPE` statement. These entities then refer to resources that are synchronously loaded and included as context when parsing XML.

Another syntax example is a `DOCTYPE` that, using the `SYSTEM` keyword followed by a URL, points to a DTD that contains additional entity definitions.

The parser passes up such external load requests.

According to the XML specification, non-validating processors are not required to read external entities.

Chrome plans to deprecate loading external entity definitions in XML documents that don't use XSLT.

[Tracking bug #455813733](https://issues.chromium.org/issues/455813733) | [ChromeStatus.com entry](https://chromestatus.com/feature/6734457763659776) | [Spec](https://www.w3.org/TR/xml/#proc-types)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-01-13 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-01-13 UTC."],[],[]] 
