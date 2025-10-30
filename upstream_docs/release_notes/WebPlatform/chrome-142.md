# Chrome 142 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/142

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 142 Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** October 28th, 2025

Unless otherwise noted, the following changes apply to Chrome 142 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 142](/blog/new-in-chrome-142). 

## CSS and UI

### Absolute positioning for the `::view-transition` element

View transitions use a pseudo subtree of the element, with `::view-transition` being the root of that transition. Previously, the `::view-transition` element was specified to have `position: fixed`. The CSS Working Group resolved to make this `position: absolute` and so Chrome now reflects that change.

This change shouldn't be noticeable because this element's containing block remains the snapshot containing block in either the absolute or fixed case. The only noticeable difference is in `getComputedStyle`.

[Tracking bug #439800102](https://issues.chromium.org/issues/439800102) | [ChromeStatus.com entry](https://chromestatus.com/feature/6155213736116224) | [Spec](https://github.com/w3c/csswg-drafts/issues/12116)

### `activeViewTransition` property on document

The View Transitions API lets developers start visual transitions between different states. The primary SPA entry point is `startViewTransition()`, which returns a transition object. This object contains several promises and functionality to track transition progress, and lets you manipulate transitions, for example, by skipping the transition or modifying its types.

From Chrome 142, developers no longer need to store this object. A `document.activeViewTransition` property represents this object, or `null` if no transition is ongoing.

This also applies to MPA transitions, where the object is only available through `pageswap` and `pagereveal` events. In this update, `document.activeViewTransition` is set to this object for the duration of the transition.

[Tracking bug #434949972](https://issues.chromium.org/issues/434949972) | [ChromeStatus.com entry](https://chromestatus.com/feature/5067126381215744) | [Spec](https://drafts.csswg.org/css-view-transitions-2)

### `:target-before` and `:target-after` pseudo-classes

These pseudo-classes match scroll markers that are before or after the active marker (matching `:target-current`) within the same scroll marker group, as determined by flat tree order:

  * `:target-before`: Matches all scroll markers that precede the active marker in the flat tree order within the group.
  * `:target-after`: Matches all scroll markers that follow the active marker in the flat tree order within the group.

[Tracking bug #440475008](https://issues.chromium.org/issues/440475008) | [ChromeStatus.com entry](https://chromestatus.com/feature/5120827674722304) | [Spec](https://drafts.csswg.org/css-overflow-5/#active-before-after-scroll-markers)

### Range syntax for style container queries and `if()`

Chrome enhances CSS style queries and the `if()` function by adding support for range syntax.

It extends style queries beyond exact value matching (for example, `style(--theme: dark)`). Developers can use comparison operators (such as `>` and `<`) to compare custom properties, literal values (for example, 10px or 25%), and values from substitution functions like `attr()` and `env()`. For a valid comparison, both sides must resolve to the same data type. It is limited to the following numeric types: `<length>`, `<number>`, `<percentage>`, `<angle>`, `<time>`, `<frequency>`, and `<resolution>`.

[Tracking bug #408011559](https://issues.chromium.org/issues/408011559) | [ChromeStatus.com entry](https://chromestatus.com/feature/5184992749289472) | [Spec](https://drafts.csswg.org/css-conditional-5/#typedef-style-range)

### Interest Invokers (the `interestfor` attribute)

Chrome adds an `interestfor` attribute to `<button>` and `<a>` elements. This attribute adds "interest" behaviors to the element. When a user "shows interest" in the element, actions are triggered on the target element, for example, showing a popover. The user agent detects when a user "shows interest" in the element through methods such as holding the pointer over the element, hitting special hotkeys on the keyboard, or long-pressing the element on touchscreens. When interest is shown or lost, an `InterestEvent` fires on the target, which has default actions for popovers, such as showing and hiding the popover.

[Tracking bug #326681249](https://issues.chromium.org/issues/326681249) | [ChromeStatus.com entry](https://chromestatus.com/feature/4530756656562176) | [Spec](https://github.com/whatwg/html/pull/11006)

### Mobile and desktop parity for select element rendering modes

By using the `size` and `multiple` attributes, the `<select>` element can be rendered as an in-page listbox or a button with a popup. However, these modes don't have consistent availability across mobile and desktop Chrome. In-page listbox rendering is unavailable on mobile, and a button with a popup is unavailable on desktop when the `multiple` attribute is present.

This update adds the listbox to mobile and a multi-select popup to desktop, and ensures that opt-ins with the `size` and `multiple` attributes result in the same rendering mode across mobile and desktop. The changes are summarized as follows:

  * When the `size` attribute has a value greater than `1`, in-page rendering is always used. Mobile devices ignored this before.
  * When the `multiple` attribute is set with no `size` attribute, in-page rendering is used. Mobile devices previously used a popup instead of an in-page listbox.
  * When the `multiple` attribute is set with `size=1`, a popup is used. Desktop devices previously used an in-page listbox.

[Tracking bug #439964654](https://issues.chromium.org/issues/439964654) | [ChromeStatus.com entry](https://chromestatus.com/feature/5412736871825408) | [Spec](https://github.com/whatwg/html/pull/11460)

### Support `download` attribute in SVG `<a>` element

This feature introduces support for the download attribute on the SVGAElement interface in Chromium, aligning with the SVG 2 specification. The download attribute enables authors to specify that the target of an SVG hyperlink should be downloaded rather than navigated to, mirroring the behavior already supported in HTMLAnchorElement. This enhancement promotes interoperability across major browsers and ensures consistent behavior between HTML and SVG link elements, thereby improving developer experience and user expectations.

[Tracking bug #40589293](https://issues.chromium.org/issues/40589293) | [ChromeStatus.com entry](https://chromestatus.com/feature/6265596395913216) | [Spec](https://svgwg.org/svg2-draft/linking.html#InterfaceSVGAElement)

## Graphics

### WebGPU: `primitive_index` feature

WebGPU adds a new optional capability that exposes a new WGSL shader built-in, `primitive_index`. It provides a per-primitive index to fragment shaders on supported hardware, similar to the `vertex_index` and `instance_index` built-ins. The primitive index is useful for advanced graphical techniques, such as virtualized geometry.

[Tracking bug #342172182](https://issues.chromium.org/issues/342172182) | [ChromeStatus.com entry](https://chromestatus.com/feature/6467722716250112) | [Spec](https://gpuweb.github.io/gpuweb/#dom-gpufeaturename-primitive-index)

### WebGPU: Texture formats tier1 and tier2

Extend GPU texture format support with capabilities like render attachment, blending, multisampling, resolve and storage_binding.

[Tracking bug #445725447](https://issues.chromium.org/issues/445725447) | [ChromeStatus.com entry](https://chromestatus.com/feature/5116926821007360) | [Spec](https://www.w3.org/TR/webgpu/#texture-formats-tier1)

## Web APIs

### FedCM—Support showing third-party iframe origins in the UI

Before Chrome 142, FedCM always showed the top-level site in its UI.

This works well when the iframe is conceptually first-party (for example, `foo.com` might have an iframe `foostatic.com`, which is not meaningful to the user).

But if the iframe is actually third-party, it is better to show the iframe origin in the UI so users better understand who they are sharing their credentials with. For example, a photo editor might be embedded in a book publishing web app and might want to let users access files they stored before with the photo editor. This capability is now available.

[Tracking bug #390581529](https://issues.chromium.org/issues/390581529) | [ChromeStatus.com entry](https://chromestatus.com/feature/5176474637959168) | [Spec](https://github.com/w3c-fedid/FedCM/pull/774)

### Stricter `*+json` MIME token validation for JSON modules

Reject JSON module script responses whose MIME type's type or subtype contains non-HTTP token code points (for example, spaces) when matched with `*+json`. This aligns with the MIME Sniffing specification and other engines. It is part of the Interop2025 modules focus area.

[Tracking bug #440128360](https://issues.chromium.org/issues/440128360) | [ChromeStatus.com entry](https://chromestatus.com/feature/5182756304846848) | [Spec](https://mimesniff.spec.whatwg.org/#parse-a-mime-type)

### Web Speech API contextual biasing

This feature enables websites to support contextual biasing for speech recognition by adding a recognition phrase list to the Web Speech API.

Developers can provide a list of phrases as well as updating them to apply a bias to the speech recognition models in favor of those phrases. This helps improve accuracy and relevance for domain-specific and personalized speech recognition.

[ChromeStatus.com entry](https://chromestatus.com/feature/5225615177023488) | [Spec](https://webaudio.github.io/web-speech-api/#speechreco-phraselist)

### Media session: add reason to `enterpictureinpicture` action details

Adds `enterPictureInPictureReason` to the `MediaSessionActionDetails` sent to the `enterpictureinpicture` action in the Media Session API. This allows developers to distinguish between `enterpictureinpicture` actions triggered explicitly by the user (e.g. from a button in the user agent) and `enterpictureinpicture` actions triggered automatically by the user agent due to the content becoming occluded.

[Tracking bug #446738067](https://issues.chromium.org/issues/446738067) | [ChromeStatus.com entry](https://chromestatus.com/feature/6415506970116096) | [Spec](https://github.com/w3c/mediasession/pull/362)

## Security

### Local network access restrictions

Chrome 142 restricts the ability to make requests to the user's local network, gated behind a permission prompt.

A local network request is any request from a public website to a local IP address or loopback, or from a local website (for example, an intranet) to loopback. Gating the ability for websites to perform these requests behind a permission mitigates the risk of cross-site request forgery attacks against local network devices such as routers, and reduces the ability of sites to use these requests to fingerprint the user's local network.

This permission is restricted to secure contexts. If granted, the permissions additionally relaxes mixed content blocking for local network requests (since many local devices are not able to obtain publicly trusted TLS certificates for various reasons).

Learn more in [New permission prompt for Local Network Access](/blog/local-network-access).

[Tracking bug #394009026](https://issues.chromium.org/issues/394009026) | [ChromeStatus.com entry](https://chromestatus.com/feature/5152728072060928) | [Spec](https://wicg.github.io/local-network-access)

## User input

### Interoperable pointerrawupdate events exposed only in secure contexts

The PointerEvents specification restricted `pointerrawupdate` to secure contexts in 2020, hiding both the event firing and the global event listeners from insecure contexts. Through this feature, Chrome will match the updated specification and become interoperable with other major browsers.

[Tracking bug #404479704](https://issues.chromium.org/issues/404479704) | [ChromeStatus.com entry](https://chromestatus.com/feature/5151468306956288) | [Spec](https://w3c.github.io/pointerevents/#the-pointerrawupdate-event)

### Sticky user activation across same-origin renderer-initiated navigations

This feature preserves the sticky user activation state after a page navigates to another same-origin page. The lack of user activation in the post-navigation page prevents some use cases like showing virtual keyboards on auto-focus, and this has been a blocker for the developers who want to build MPAs over SPAs.

**Note:** Browser-initiated navigation requests (reload, history navigation, typed URL in address bar) are not covered by this feature.

[Tracking bug #433729626](https://issues.chromium.org/issues/433729626) | [ChromeStatus.com entry](https://chromestatus.com/feature/5078337520926720) | [Spec](https://github.com/whatwg/html/pull/11454)

## Origin trials

### Device Bound Session Credentials

A way for websites to securely bind a session to a single device.

It lets servers have a session be securely bound to a device. The browser will renew the session periodically as requested by the server, with proof of possession of a private key.

[Origin Trial](https://developer.chrome.com/origintrials#/view_trial/3357996472158126081) | [Device Bound Session Credentials: Second origin trial begins](/blog/dbsc-origin-trial-update) | [ChromeStatus.com entry](https://chromestatus.com/feature/5140168270413824) | [Spec](https://w3c.github.io/webappsec-dbsc)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-10-28 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-10-28 UTC."],[],[]] 
