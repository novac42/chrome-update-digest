# Chrome 130 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/130

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Docs ](https://developer.chrome.com/docs)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 130

Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** October 15th, 2024

Unless otherwise noted, the following changes apply to Chrome 130 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 130](/blog/new-in-chrome-130). 

## CSS

### CSS Container Queries flat tree lookup

The specification for container queries changed to look up flat tree ancestors. This change is only relevant for shadow DOM where an element will now be able to see non-named containers inside shadow trees into which the element or one of its ancestors are slotted, even if the CSS rule does not use `::part()` or `::slotted()`.

[Tracking bug #340876720](https://issues.chromium.org/issues/340876720) | [ChromeStatus.com entry](https://chromestatus.com/feature/5242724333387776) | [Spec](https://drafts.csswg.org/css-conditional-5/#container-queries)

### CSS Nesting: The nested declarations rule

Keeps bare declarations following a nested rule in their place, by wrapping those declarations in `CSSNestedDeclarations` rules during parsing.

[CSS nesting improves with CSSNestedDeclarations](https://web.dev/blog/css-nesting-cssnesteddeclarations) | [ChromeStatus.com entry](https://chromestatus.com/feature/5084403030818816)

### Full and unprefixed `box-decoration-break` support

Adds support for `box-decoration-break: clone` both for inline fragmentation (line layout) and block fragmentation (pagination for printing and multicol).

Previously in Chrome, only `box-decoration-break:slice` (the initial value) was supported for block fragmentation, whereas for inline fragmentation, `box-decoration-break:clone` was also supported, but only when using the prefixed `-webkit-box-decoration-break` property.

[The box-decoration-break property in Chrome 130](/blog/box-decoration-break) | [Tracking bug #41295617](https://issues.chromium.org/issues/41295617) | [ChromeStatus.com entry](https://chromestatus.com/feature/5162398704205824) | [Spec](https://drafts.csswg.org/css-break/#break-decoration)

### Allow more pseudo-elements and pseudo-classes after `::part()`

CSS selectors that use the `::part()` pseudo-element are allowed to have other CSS pseudo-elements (except `::part()`) and many types of other CSS pseudo-classes after them. Combinators are still not allowed after `::part()`, and pseudo-classes that depend on tree structure are not allowed.

Previously Chrome only allowed a limited set of pseudo-classes and pseudo-elements after `::part()`. This change allows all of the pseudo-classes and pseudo-elements that should be allowed. It means selectors such as `::part(part-name):enabled` and `::part(part-name)::marker` are now allowed.

[Tracking bug #40623497](https://issues.chromium.org/issues/40623497) | [ChromeStatus.com entry](https://chromestatus.com/feature/5195333643272192) | [Spec](https://drafts.csswg.org/css-shadow-parts-1/#part)

## Web APIs

### Compression dictionary transport with shared Brotli and shared Zstandard

This feature adds support for using designated previous responses, as an external dictionary for content encoding compressing responses with Brotli or Zstandard.

Enterprises might experience potential compatibility issues with enterprise network infrastructure that intercepts HTTPS traffic and is sensitive to unknown content encodings. The enterprise policy `CompressionDictionaryTransportEnabled` is available to turn off the compression dictionary transport feature.

[Tracking bug #40255884](https://issues.chromium.org/issues/40255884) | [ChromeStatus.com entry](https://chromestatus.com/feature/5124977788977152) | [Spec](https://datatracker.ietf.org/doc/draft-ietf-httpbis-compression-dictionary)

### Concurrent smooth `scrollIntoView()`

The [`scrollIntoView()`](https://developer.mozilla.org/docs/Web/API/Element/scrollIntoView) method with `behavior: "smooth"` lets you create scroll containers that scroll to their descendants with a gentle scroll animation. This feature fixes Chrome's implementation of the API so that ongoing `scrollIntoView` animations are not canceled by unrelated scrolls on other scroll containers.

The feature also fixes cases where Chrome fails to scroll to a page's fragment anchor because of a competing `scrollIntoView` that is invoked when the page loads.

[Demo](https://davmila.github.io/MultiSmoothScrollDemo) | [Tracking bug #325081538](https://issues.chromium.org/issues/325081538) | [ChromeStatus.com entry](https://chromestatus.com/feature/6270155647352832) | [Spec](https://www.w3.org/TR/cssom-view-1/#dom-element-scrollintoview)

### Document picture-in-picture: add option to ignore window bounds cache

This adds a new parameter (`preferInitialWindowPlacement`) to the document picture-in-picture API that, when set to true, hints to the browser that it shouldn't try to reuse the position or size of the previous document picture-in-picture from this site when opening this one.

Often, a document picture-in-picture window will close and re-open multiple times for the same site, such as moving a video conference to and from PiP. The browser is free to re-open the PiP window at its most recent size and location, so that it stays where the user last moved it and provides continuity between the PiP windows. However, if the new window is semantically unrelated to the previous window, such as if it is a new video call, then you can use this parameter to provide a hint to the user agent that this window might be better opened in its default position and size instead.

Learn about how to [open the window in its default position and size](/docs/web-platform/document-picture-in-picture#open_the_picture-in-picture_window_in_its_default_position_and_size).

[Picture-in-Picture for any Element, not just video](https://developer.chrome.com/docs/web-platform/document-picture-in-picture#open_the_picture-in-picture_window_in_its_default_position_and_size) | [ChromeStatus.com entry](https://chromestatus.com/feature/5183881532932096) | [Spec](https://github.com/WICG/document-picture-in-picture/pull/119)

### Improved error reporting in IndexedDB for large value read failures

Change to reporting for certain error cases that were previously reported with a `DOMException` and the message "Failed to read large IndexedDB value".

Chrome now raises a `DOMException` with the name `"NotFoundError"` when the file containing the data being read by an IDBRequest is missing from the disk so that sites can take the appropriate corrective action when an unrecoverable failure occurs. Corrective actions could include deleting the entry from the database, notifying the user, or re-fetching the data from servers.

[Tracking bug #362123231](https://issues.chromium.org/issues/362123231) | [ChromeStatus.com entry](https://chromestatus.com/feature/5140210640486400) | [Spec](https://www.w3.org/TR/IndexedDB/#dom-idbrequest-error)

### Keyboard focusable scroll containers

This feature makes scrollers without focusable children keyboard-focusable by default.

This is an important improvement to help make scrollers and contents within scrollers more accessible to all users. You can read more about its benefits in [Keyboard focusable scrollers](/blog/keyboard-focusable-scrollers). Keyboard focusable scrollers will be enabled by default starting in Chrome 130. If websites need time to adjust to this new feature, there are a few options:

  * The [ Keyboard focusable scrollers opt out deprecation trial](/origintrials#/view_trial/2455024746870341633) can be used to opt back out of the feature for a limited time on a given site. This can be used through Chrome 132, ending March 18, 2025.
  * The [`KeyboardFocusableScrollersEnabled enterprise policy`](https://chromeenterprise.google/policies/#KeyboardFocusableScrollersEnabled) available from Chrome 127 can be used for the same purpose.

**Note:** The previous rollout of this feature (started in [Chrome 127](/release-notes/127)) was stopped due to web compatibility issues, which should be fixed in the new implementation.

[Keyboard focusable scrollers](/blog/keyboard-focusable-scrollers) | [Tracking bug #40113891](https://issues.chromium.org/issues/40113891) | [ChromeStatus.com entry](https://chromestatus.com/feature/5231964663578624) | [Spec](https://drafts.csswg.org/css-overflow-3/#scroll-container)

### Protected Audience Bidding and Auction Services

The Protected Audience API (formerly known as FLEDGE) is a Privacy Sandbox proposal to serve remarketing and custom audience use cases, designed so third parties cannot track user browsing behavior across sites.

This feature, Protected Audience Bidding and Auction Services, outlines a way to allow Protected Audience computation to take place on cloud servers in a trusted execution environment, rather than running locally on a user's device. Moving computations to cloud servers can help optimize the Protected Audience auction, to free up computational cycles and network bandwidth for a device.

[ChromeStatus.com entry](https://chromestatus.com/feature/4649601971257344) | [Spec](https://github.com/WICG/turtledove/blob/main/FLEDGE_browser_bidding_and_auction_API.md)

### Support non-special scheme URLs

Previously, Chrome's URL parser didn't support non-special URLs. The parser parses non-special URLs as if they had an "opaque path", which is not aligned with the URL Standard. Now, Chromium's URL parser parses non-special URLs correctly, following the URL Standard.

[Support Non-Special Scheme URLs](http://bit.ly/url-non-special) | [Tracking bug #40063064](https://issues.chromium.org/issues/40063064) | [ChromeStatus.com entry](https://chromestatus.com/feature/5201116810182656) | [Spec](https://url.spec.whatwg.org/)

### WebAssembly JavaScript String Builtins

This feature exposes common JavaScript string operations for import into WebAssembly. This lets you create and manipulate JavaScript strings from WebAssembly without support within WebAssembly. This still allows for a similar performance as supported string references.

[ChromeStatus.com entry](https://chromestatus.com/feature/6695587390423040) | [Spec](https://github.com/WebAssembly/js-string-builtins/blob/main/proposals/js-string-builtins/Overview.md)

### Web Serial: `connected` attribute and RFCOMM connection events

This feature adds a boolean `SerialPort.connected` attribute. The attribute returns `true` if the serial port is logically connected. For wired serial ports, a port is logically connected if the port is physically attached to the system. For wireless serial ports, a port is logically connected if the device hosting the port has any open connections to the host.

Previously, only wired serial ports dispatched connect and disconnect events. With this feature, Bluetooth RFCOMM serial ports will dispatch these events when the port becomes logically connected or disconnected.

This feature is intended to allow applications to detect when a Bluetooth RFCOMM serial port is available without opening the port.

Learn more in [Bluetooth RFCOMM updates in Web Serial](/blog/bluetooth-rfcomm-updates-web-serial).

[Bluetooth RFCOMM updates in Web Serial](/blog/bluetooth-rfcomm-updates-web-serial) | [Tracking bug #40283485](https://issues.chromium.org/issues/40283485) | [ChromeStatus.com entry](https://chromestatus.com/feature/5118102654418944) | [Spec](https://wicg.github.io/serial/#serialport-interface)

## Rendering and graphics

### WebGPU: Dual source blending

Adds the optional GPU feature "dual-source-blending" that enables combining two fragment shader outputs into a single framebuffer. This technique is particularly useful for applications that require complex blending operations, such as those based on Porter-Duff blend modes. By reducing the need for frequent pipeline state object changes, dual source blending can enhance performance and flexibility.

[Tracking bug #341973423](https://issues.chromium.org/issues/341973423) | [ChromeStatus.com entry](https://chromestatus.com/feature/5167711051841536) | [Spec](https://github.com/gpuweb/gpuweb/pull/4621)

## Privacy

### Attribution Reporting API feature (Attribution Scopes)

This change is based on ad tech feedback and the need for more fine grained filtering controls before the attribution process takes place. It lets API callers specify a field called "attribution scopes" which will be used for filtering before starting the regular attribution flow. This allows API callers more fine grained control over the attribution granularity and the ability to receive proper attribution reports when there are multiple different advertisers or campaigns that all convert on the same destination site.

[ChromeStatus.com entry](https://chromestatus.com/feature/5096560068395008)

### Attribution Reporting API feature (debug key privacy improvement)

This change helps to mitigate a potential privacy gap with debug keys.

Currently the API allows a source debug key or a trigger debug key to be specified if third-party cookies are available and can be set by API callers. If either a source or trigger debug key is specified then it will be included in the attribution report. This may lead to a privacy leak if third-party cookies are only allowed on either the publisher or the advertiser site but not both.

This change mitigates this issue by enforcing that source debug keys and trigger debug keys are only included in the attribution report if they're present on both the source and trigger, which would mean that third-party cookies were available on both the publisher and advertiser site. This change will apply to both event-level reports and aggregatable reports.

[ChromeStatus.com entry](https://chromestatus.com/feature/6257907243679744) | [Spec](https://wicg.github.io/attribution-reporting-api/#attribution-debugging)

## Origin trials

### Language Detector API

A JavaScript API for [detecting the language of text](/blog/august2024-language-detection), with confidence levels.

[Origin Trial](/origintrials#/view_trial/662592095176884225) | [Language detection API available for early preview](/blog/august2024-language-detection) | [ChromeStatus.com entry](https://chromestatus.com/feature/6494349985841152) | [Spec](https://github.com/WICG/translation-api/blob/main/README.md)

### WebAuthn `attestationFormats`

Support the `attestationFormats` field from WebAuthn level 3.

WebAuthn Level 3 supports a site expressing an ordered preference for credential attestation formats in the new `attestationFormats` field. This feature enables support for this on Android, where multiple formats can be supported by passkey providers.

[Origin Trial](/origintrials#/view_trial/1428204031829868545) | [ChromeStatus.com entry](https://chromestatus.com/feature/5121935290400768) | [Spec](https://w3c.github.io/webauthn/#dom-publickeycredentialcreationoptions-attestationformats)

## Deprecations and removals

### Remove `expectedImprovement` in `DelegatedInkTrailPresenter`

The `expectedImprovement` attribute tells web developers how much improvement the DelegatedInkTrails API will provide to their current ink latency. However, this attribute is not worth the increase to fingerprinting entropy.

[ChromeStatus.com entry](https://chromestatus.com/feature/5194773674328064) | [Spec](https://wicg.github.io/ink-enhancement)

## Further reading

Looking for more? Check out these additional resources.

  * [What's new in Chrome 130](/blog/new-in-chrome-130)
  * [What's new in Chrome DevTools 130](/blog/new-in-devtools-130)
  * [ChromeStatus.com updates for Chrome 130](https://chromestatus.com/features#milestone%3D130)
  * [Chrome release calendar](https://chromiumdash.appspot.com/schedule)
  * [Upcoming deprecations](https://chromestatus.com/features#browsers.chrome.status%3A%22Deprecated%22)
  * [Upcoming removals](https://chromestatus.com/features#browsers.chrome.status%3A%22Removed%22)

## Download Google Chrome

Download Chrome for [Android](https://play.google.com/store/apps/details?id=com.android.chrome), [Desktop](https://www.google.com/chrome/), or [iOS](https://apps.apple.com/us/app/google-chrome/id535886823). 

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2024-10-15 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2024-10-15 UTC."],[],[]] 
