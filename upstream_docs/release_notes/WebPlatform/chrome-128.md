# Chrome 128 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/128

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Docs ](https://developer.chrome.com/docs)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 128

Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** August 20th, 2024

Unless otherwise noted, the following changes apply to Chrome 128 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 128](/blog/new-in-chrome-128). 

## CSS

### CSS `ruby-align` property

There are multiple ways to align characters when the length of ruby annotations and the base characters don't match, and the `ruby-align` property lets you choose the one that works best for your design. The property takes one of the following keyword values:

  * `space-around`
  * `space-between`
  * `start`
  * `center`

[Tracking bug #40249572](https://issues.chromium.org/issues/40249572) | [ChromeStatus.com entry](https://chromestatus.com/feature/5152412192210944) | [Spec](https://drafts.csswg.org/css-ruby/#ruby-align-property)

### Line-breakable ruby

Makes line-breaks possible within elements with `display: ruby`.

Previously a single pair of a ruby-base and a ruby-text was not line-breakable, and would be pushed to the next line if the current line had not enough space for the entire pair. Now each of the ruby-base and the ruby-text can be split into multiple lines.

[Tracking bug #324111880](https://issues.chromium.org/issues/324111880) | [ChromeStatus.com entry](https://chromestatus.com/feature/5077282711666688) | [Spec](https://drafts.csswg.org/css-ruby/#break-within)

### Minimum size of `<option>` within `<select>` drop-down

The WCAG accessibility guidelines specify that the size of pointer inputs must be at least 24 by 24 CSS pixels. This change makes the `<option>` element within the `<select>` drop-down meet this height requirement.

[Tracking bug #339141283](https://issues.chromium.org/issues/339141283) | [ChromeStatus.com entry](https://chromestatus.com/feature/5152633181700096) | [Spec](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

### Standardized CSS `zoom` property

Updates the existing implementation of the previously non-standard CSS [`zoom`](https://developer.mozilla.org/docs/Web/CSS/zoom) property to align with the new standard. This changes various JavaScript APIs to align with the spec, changes zoom to apply to iframe content documents, and changes it to apply to all inherited length properties (previously it only changed the inherited `font-size`).

[Demo](https://jsbin.com/wasafateko/edit?html,css,js,output) | [ChromeStatus.com entry](https://chromestatus.com/feature/5198254868529152)

## Web APIs

### Additions to Attribution Reporting

Chrome 128 includes two additional features for [Attribution Reporting](https://developer.mozilla.org/docs/Web/Attribution_Reporting_API). There are changes to source-destination-limit logic, with the aim of reducing the rate of transmission loss. Flexible contributions filtering will improve API report batching capabilities.

[ChromeStatus.com entry](https://chromestatus.com/feature/6320694358179840)

### `document.caretPositionFromPoint`

Returns the current caret position from a given screen point in the form of a `CaretPosition` object representing the caret position indicating current text insertion point including the containing DOM node, caret's character offset, and the client rectangle of caret range. This feature also supports getting the `CaretPosition` inside Shadow DOM.

[Tracking bug #388976](https://issues.chromium.org/issues/388976) | [ChromeStatus.com entry](https://chromestatus.com/feature/5201014343073792) | [Spec](https://drafts.csswg.org/cssom-view/#dom-document-caretpositionfrompoint)

### Web Share API on macOS

The API enables web developers to build share buttons that display the same system share dialog boxes used by mobile applications. This previously shipped on Android, Windows, and ChromeOS, and is now also coming to macOS. 

[Docs](https://web.dev/articles/web-share)

## Media

### `AudioContext.onerror`

AudioContext creation and audio rendering errors are now reported to web applications with a callback assigned to `AudioContext.onerror`.

[Tracking bug #41495720](https://issues.chromium.org/issues/41495720) | [ChromeStatus.com entry](https://chromestatus.com/feature/5113439453446144) | [Spec](https://webaudio.github.io/web-audio-api/#dom-audiocontext-onerror)

### `PointerEvent.deviceProperties` for multi-pen inking

Currently, developers have no way to distinguish between two individual pens on an ink-enabled digitizer. The existing `PointerEvent.id` attribute is implemented in different ways and does not always persist for each ink stroke or interaction with the screen.

This change provides a secure and reliable way to identify individual pen (pointers) interacting with the screen to set specific colors or pen shapes for each device interacting with the digitizer. It extends the `PointerEvent` interface to include a new attribute, `deviceProperties`. This contains the attribute `uniqueId`, that represents a session-persistent, document isolated, unique identifier that a developer can reliably use to identify individual pens interacting with the page.

[ChromeStatus.com entry](https://chromestatus.com/feature/5114132234240000) | [Spec](https://github.com/MicrosoftEdge/MSEdgeExplainers/blob/main/PointerEventDeviceId/explainer.md)

### SkipAd media session action

Supports the SkipAd media session action. This action lets browsers show a button in the system media controls or in the Picture-in-Picture window.

[Demo](https://googlechrome.github.io/samples/picture-in-picture/skip-ad.html) | [ChromeStatus.com entry](https://chromestatus.com/feature/4749278882824192) | [Spec](https://wicg.github.io/picture-in-picture/#media-session)

## Privacy

### Cross-site ancestor chain bit for CookiePartitionKey of partitioned cookies

Chrome 128 adds a cross-site ancestor bit to the key ring of the partitioned cookie's `CookiePartitionKey`. This change unifies the partition key with the partition key values used in storage partitioning and adds protection against clickjacking attacks by preventing cross-site embedded frames from having access to the top-level-site's partitioned cookies.

[Tracking bug #41486025](https://issues.chromium.org/issues/41486025) | [ChromeStatus.com entry](https://chromestatus.com/feature/5144832583663616) | [Spec](https://github.com/explainers-by-googlers/CHIPS-spec)

### Private Aggregation API: client-side contribution merging

Modifies the [Private Aggregation API](https://developers.google.com/privacy-sandbox/relevance/private-aggregation) to merge histogram contributions with the same bucket and filtering ID before embedding in the aggregatable report's encrypted payload.

Private Aggregation imposes a limit on the number of contributions that can be embedded in a single aggregatable report, with any additional contributions being dropped. By merging contributions where possible, we can get additional utility out of the limit. Note that, ignoring the dropping of excess contributions, merging these sorts of contributions shouldn't have any impact on the final summary reports.

[Tracking bug #330744610](https://issues.chromium.org/issues/330744610) | [ChromeStatus.com entry](https://chromestatus.com/feature/4793172803977216) | [Spec](https://github.com/patcg-individual-drafts/private-aggregation-api/pull/123)

## JavaScript

### `Promise.try`

`Promise.try` is a [TC39 proposal](https://tc39.es/proposal-promise-try/) for a new static method. `Promise.try(f)` is shorthand for `new Promise(resolve => resolve(f()))`.

[ChromeStatus.com entry](https://chromestatus.com/feature/6315704705089536) | [Spec](https://tc39.es/proposal-promise-try)

### WebAuthn hints

The new `hints` parameter in WebAuthn requests lets sites provide guidance to browsers to guide their UI. The canonical use case is enterprises that know their internal sites use only security keys and want to be able to communicate so that browsers focus the UI on that case.

Hints also resolve a tension where the current `authenticatorAttachment` parameter is strict: setting it to `platform` excludes all cross-platform options.

[ChromeStatus.com entry](https://chromestatus.com/feature/5145737733341184) | [Spec](https://w3c.github.io/webauthn/#enum-hints)

### Write `image/svg+xml` content in UTF-8 format on Windows

Switch to UTF-8 on Windows while writing `image/svg+xml` format to the clipboard. HTML format already uses UTF-* on Windows and this will allow copying and pasting SVG images from the clipboard.

On all other supported platforms, `image/svg+xml` is serialized into UTF-8 before it gets written to the clipboard.

[Demo](https://webdbg.com/test/svg) | [Tracking bug #338250106](https://issues.chromium.org/issues/338250106) | [ChromeStatus.com entry](https://chromestatus.com/feature/5417299782926336) | [Spec](https://w3c.github.io/clipboard-apis/#optional-data-types-x)

## New origin trials

### Digital Credentials API

Websites can request credentials from mobile wallet apps through a variety of mechanisms today, for example custom URL handlers and QR code scanning. This feature lets sites request identity information from digital credentials inside wallets using Android's IdentityCredential CredMan system. It's extensible to support multiple credential formats (for example, ISO mDoc and W3C verifiable credential) and allows multiple wallet apps to be used. The API also includes mechanisms to reduce the risk of ecosystem-scale abuse of sensitive identity information.

[Origin Trial](/origintrials#/view_trial/3139571890230657025) | [Tracking bug #40257092](https://issues.chromium.org/issues/40257092) | [ChromeStatus.com entry](https://chromestatus.com/feature/5166035265650688) | [Spec](https://wicg.github.io/digital-credentials)

### FedCM multiple identity providers in single `get()` call

Allows FedCM to show multiple identity providers in the same dialog. This gives developers a convenient way to present all supported identity providers to users. We are planning to first tackle the case of having all providers in the same `get()` call.

[Origin Trial](/origintrials#/view_trial/1280578044871901185) | [ChromeStatus.com entry](https://chromestatus.com/feature/5067784766095360)

### Disable standardized CSS zoom

The implementation of the previously non-standard CSS `zoom` property has been updated to align with the new standard. This changes various JavaScript APIs to align with the specification, changes `zoom` to apply to iframe content documents, and changes it to apply to all inherited length properties where previously it only changed the inherited `font-size`.

This trial lets you opt back into the previous behavior to have more time to adjust your code.

[Origin Trial](/origintrials#/view_trial/3499859860420296705)

### WebGPU Subgroups experimentation

Adds subgroup functionality to WebGPU. Subgroup operations perform SIMT operations to provide efficient communication and data sharing among groups of invocations. These operations can be used to accelerate applications by reducing memory overheads incurred by inter-invocation communication. 

[ChromeStatus.com entry](https://chromestatus.com/feature/5126409856221184)

## Further reading

Looking for more? Check out these additional resources.

  * [What's new in Chrome 128](/blog/new-in-chrome-128)
  * [What's new in Chrome DevTools 128](/blog/new-in-devtools-128)
  * [ChromeStatus.com updates for Chrome 128](https://chromestatus.com/features#milestone%3D128)
  * [Chrome release calendar](https://chromiumdash.appspot.com/schedule)
  * [Upcoming deprecations](https://chromestatus.com/features#browsers.chrome.status%3A%22Deprecated%22)
  * [Upcoming removals](https://chromestatus.com/features#browsers.chrome.status%3A%22Removed%22)

## Download Google Chrome

Download Chrome for [Android](https://play.google.com/store/apps/details?id=com.android.chrome), [Desktop](https://www.google.com/chrome/), or [iOS](https://apps.apple.com/us/app/google-chrome/id535886823). 

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2024-08-20 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2024-08-20 UTC."],[],[]] 
