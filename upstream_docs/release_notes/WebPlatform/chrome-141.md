# Chrome 141 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/141

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Docs ](https://developer.chrome.com/docs)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 141

Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** September 30th, 2025

Unless otherwise noted, the following changes apply to Chrome 141 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 141](/blog/new-in-chrome-141). 

## CSS

### Custom property enumeration in `getComputedStyle()`

When iterating over `window.getComputedStyle(element)` in Chrome, there was a bug where it forgets to include any custom properties set on the element. Therefore, `length()` on the returned object forgets to account for the number of custom properties set. This bug is fixed from Chrome 141, aligning Chrome with Firefox and Safari.

[ChromeStatus.com entry](https://chromestatus.com/feature/5070655645155328) | [Spec](https://drafts.csswg.org/cssom/#dom-window-getcomputedstyle)

## DOM

### ARIA Notify API

`ariaNotify` provides a JavaScript API that lets content authors tell a screen reader what to read.

`ariaNotify` improves reliability and developer control compared to ARIA live regions, allowing for announcing changes not tied to DOM updates. This enables more consistent and ergonomic accessibility experiences across dynamic web applications. Iframe usage of this feature can be controlled using the `"aria-notify"` permission policy.

[Tracking bug #326277796](https://issues.chromium.org/issues/326277796) | [ChromeStatus.com entry](https://chromestatus.com/feature/5745430754230272) | [Spec](https://github.com/w3c/aria/pull/2577)

### Update `hidden=until-found` and details ancestor revealing algorithm

The specification recently had some small changes to the revealing algorithms for `hidden=until-found` and details elements to prevent the browser from getting stuck in an infinite loop, these are now shipping in Chrome.

[Tracking bug #433545121](https://issues.chromium.org/issues/433545121) | [ChromeStatus.com entry](https://chromestatus.com/feature/5179013869993984) | [Spec](https://github.com/whatwg/html/pull/11457)

## JavaScript

### Align implementations on when RTP stats should be created

RTP stats objects, of type "outbound-rtp" or "inbound-rtp" in this case, represents a WebRTC stream. The identifier of this stream is the SSRC (a number). This feature aligns with the specification on when these stats should be created.

[Tracking bug #406585888](https://issues.chromium.org/issues/406585888) | [ChromeStatus.com entry](https://chromestatus.com/feature/4580748730040320) | [Spec](https://w3c.github.io/webrtc-stats/#the-rtp-statistics-hierarchy)

## Media

### Support `restrictOwnAudio`

The `restrictOwnAudio` property is a captured display surfaces constrainable property. It changes the behavior of system audio in a captured display surface. The `restrictOwnAudio` constraint only has an effect if the captured display surface inherently includes system audio; otherwise, it will have no impact.

[ChromeStatus.com entry](https://chromestatus.com/feature/5128140732760064) | [Spec](https://www.w3.org/TR/screen-capture/#dfn-restrictownaudio)

### `windowAudio` for `getDisplayMedia()`

Extends `DisplayMediaStreamOptions` for `getDisplayMedia()` with a `windowAudio` option. This new option allows web applications to hint to the user agent whether the user should be offered the ability to share audio when a window is selected. `windowAudio` can be set to exclude, system, or window based on application preference.

A web application that is configured for audio capture but wants to limit system audio capture when a window is selected should set `windowAudio: "exclude"`.

[ChromeStatus.com entry](https://chromestatus.com/feature/5072779506089984) | [Spec](https://w3c.github.io/mediacapture-screen-share/#displaymediastreamoptions)

## Miscellaneous

### Support `width` and `height` as presentation attributes on nested `<svg>` elements

This feature supports applying `width` and `height` as presentation attributes on nested `<svg>` elements through both SVG markup and CSS. This dual approach provides even greater flexibility for developers, allowing them to manage and style SVG elements more efficiently within complex designs.

[Tracking bug #40409865](https://issues.chromium.org/issues/40409865) | [ChromeStatus.com entry](https://chromestatus.com/feature/5178789386256384) | [Spec](https://svgwg.org/svg2-draft/geometry.html#Sizing)

### Digital Credentials API (presentation support)

Websites retrieve credentials from mobile wallet apps using a variety of mechanisms, such as custom URL handlers and QR code scanning. This feature lets sites request identity information from wallets using Android's `IdentityCredential` CredMan system. It is extensible to support multiple credential formats (such as ISO mDoc and W3C verifiable credential) and allows multiple wallet apps to be used. This update adds mechanisms to help reduce the risk of ecosystem-scale abuse of real-world identity.

[Tracking bug #40257092](https://issues.chromium.org/issues/40257092) | [ChromeStatus.com entry](https://chromestatus.com/feature/5166035265650688) | [Spec](https://w3c-fedid.github.io/digital-credentials)

### Navigation API: deferred commit (precommit handlers)

Normally, when `navigateEvent.intercept()` is called, the intercepted navigation commits (and therefore the URL updates) as soon as the `NavigateEvent` finishes dispatch.

This feature adds a `precommitHandler` option to `navigateEvent.intercept()`, similar to `handler`. It defers the commit until that handler (and all other precommit handlers) are resolved, and it allows the handler to change the navigation's URL, info, status, and history handling behavior (push/replace).

[Tracking bug #440190720](https://issues.chromium.org/issues/440190720) | [ChromeStatus.com entry](https://chromestatus.com/feature/5134734612496384) | [Spec](https://github.com/whatwg/html/pull/10919)

### FedCM: Alternative fields in account selection

Adds support for phone numbers and usernames, in addition to or instead of a user's full name and email address as identifiers for disambiguating accounts in the account selector. Also, makes these new fields available for websites to affect the disclosure text.

[Tracking bug #382086282](https://issues.chromium.org/issues/382086282) | [ChromeStatus.com entry](https://chromestatus.com/feature/5121180773908480) | [Spec](https://github.com/w3c-fedid/FedCM/pull/718)

## Network / Connectivity

### No-Vary-Search support for the HTTP disk cache

Lets the HTTP disk cache use the `No-Vary-Search` response header to share a cache entry between URLs that differ only in the query parameters.

Developers can use `No-Vary-Search` to specify query parameters that have no impact on the user experience. A common example might be an ID used to track conversions. Supporting this header in the HTTP disk cache means that if the user later goes back to that same page without the conversion ID, it can be used or revalidated from the cache rather than having to be fetched from scratch from the network.

Previously, `No-Vary-Search` support shipped for the navigation prefetch cache, prefetch and prerender speculation rules, and prerender. This launch makes it generally available to any feature that uses the HTTP disk cache.

[Tracking bug #382394774](https://issues.chromium.org/issues/382394774) | [ChromeStatus.com entry](https://chromestatus.com/feature/5808599110254592) | [Spec](https://httpwg.org/http-extensions/draft-ietf-httpbis-no-vary-search.html)

## Offline / Storage

### IndexedDB `getAllRecords()` and direction option for `getAll()` and `getAllKeys()`

This feature adds the `getAllRecords()` method to the IndexedDB IDBObjectStore and IDBIndex. It also adds a direction parameter to `getAll()` and `getAllKeys()`. This functionality lets certain read patterns be significantly faster when compared to the existing alternative of iteration with cursors. In one test, a workload from a Microsoft property showed a 350ms improvement.

The `getAllRecords()` method combines `getAllKeys()` and `getAll()` by enumerating both primary keys and values at the same time. For an IDBIndex, `getAllRecords()` also provides the record's index key in addition to the primary key and value.

[Tracking bug #40746016](https://issues.chromium.org/issues/40746016) | [ChromeStatus.com entry](https://chromestatus.com/feature/5124331450138624) | [Spec](https://w3c.github.io/IndexedDB/#dom-idbobjectstore-getallrecords)

## Performance

### Speculation rules: desktop "eager" eagerness improvements

On desktop, "eager" eagerness speculation rules prefetches and prerenders now trigger when users hover on a link for a shorter time than the "moderate" mouse hover time.

The previous behavior, of starting prefetch and prerenders as soon as possible, was the same as "immediate" eagerness. This new behavior is more useful as it better reflects the author's intent to be more eager than the "moderate" and less eager than "immediate".

[ChromeStatus.com entry](https://chromestatus.com/feature/5113430155591680) | [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html#:~:text=early%20as%20possible.-,%22moderate%22,balance%20between%20%22eager%22%20and%20%22conservative%22.,-%22conservative%22)

## Security

### Strict Same Origin Policy for Storage Access API

Adjusts the Storage Access API semantics to strictly follow the Same Origin Policy with regard to security. That is, using `document.requestStorageAccess()` in a frame only attaches cookies to requests to the iframe's origin (not site) by default.

**Note:** The `CookiesAllowedForUrls` policy or Storage Access Headers may still be used to unblock cross-site cookies.

[Tracking bug #379030052](https://issues.chromium.org/issues/379030052) | [ChromeStatus.com entry](https://chromestatus.com/feature/5169937372676096) | [Spec](https://github.com/privacycg/storage-access/pull/213)

### Signature-based Integrity

This feature provides web developers with a mechanism to verify the provenance of resources they depend upon, creating a technical foundation for trust in a site's dependencies. In short: servers can sign responses with a Ed25519 key pair, and web developers can require the user agent to verify the signature using a specific public key. This offers a helpful addition to URL-based checks offered by Content Security Policy on the one hand, and Subresource Integrity's content-based checks on the other.

[Tracking bug #375224898](https://issues.chromium.org/issues/375224898) | [ChromeStatus.com entry](https://chromestatus.com/feature/5032324620877824) | [Spec](https://wicg.github.io/signature-based-sri)

## WebRTC

### WebRTC Encoded Transform (V2)

This API allows processing of encoded media flowing through an `RTCPeerConnection`. Chrome shipped an early version of this API in 2020. Since then, the specification has changed and other browsers have shipped the updated version (Safari in 2022 and Firefox in 2023). This launch aligns Chrome with the updated specification as part of Interop 2025.

This launch does not cover the `generateKeyFrame method`, which is still under discussion.

[Tracking bug #354881878](https://issues.chromium.org/issues/354881878) | [ChromeStatus.com entry](https://chromestatus.com/feature/5175278159265792) | [Spec](https://github.com/w3c/webrtc-encoded-transform)

### `echoCancellationMode` for `getUserMedia()`

Extends the `echoCancellation` behavior of the `MediaTrackConstraints` dictionary. his previously accepted `true` or `false` and now additionally accepts the values `"all"` and `"remote-only"`. This lets clients modify echo cancellation behavior applied to audio tracks received from microphones, controlling how much of the user system playout (all, or only audio received from `PeerConnections`) is removed from the microphone signal.

[ChromeStatus.com entry](https://chromestatus.com/feature/5585747985563648) | [Spec](https://www.w3.org/TR/mediacapture-streams/#dom-echocancellationmodeenum)

## Managed ChromeOS only

### Permissions Policy for Device Attributes API

The new Permissions Policy enables restricting access to the Device Attributes API, which is available only for policy-installed kiosk web apps and policy-installed Isolated Web Apps, both only on managed ChromeOS devices.

Additionally, the feature is controlled by content settings. Two new policies are introduced: `DeviceAttributesBlockedForOrigins` and `DefaultDeviceAttributesSetting`, to complement previously introduced `DeviceAttributesAllowedForOrigins`. The feature is enabled by default for policy-installed kiosk web apps and policy-installed Isolated Web Apps on managed ChromeOS devices.

[ChromeStatus.com entry](https://chromestatus.com/feature/4843520522977280) | [Spec](https://github.com/WICG/WebApiDevice/blob/main/DeviceAttributesPermissionsPolicyExplainer.md)

## Origin trials

### Local network access restrictions

Chrome 141 [restricts the ability to make requests to the user's local network](/blog/local-network-access), gated behind a permission prompt.

This origin trial temporarily allows for access to resources on local networks to originate from non-secure contexts. This will give developers more time to migrate Local Network Access requests to originate from a secure context.

[Origin Trial](/origintrials#/view_trial/3826370833404657665) | [Tracking bug #394009026](https://issues.chromium.org/issues/394009026) | [ChromeStatus.com entry](https://chromestatus.com/feature/5152728072060928) | [Spec](https://wicg.github.io/local-network-access)

### Proofreader API

A JavaScript API for [proofreading input text with suggested corrections](/blog/proofreader-api-ot), backed by an AI language model.

[Origin Trial](/origintrials#/register_trial/1988902185437495297) | [Tracking bug #403313556](https://issues.chromium.org/issues/403313556) | [ChromeStatus.com entry](https://chromestatus.com/feature/5164677291835392) | [Spec](https://github.com/webmachinelearning/proofreader-api/blob/main/README.md#full-api-surface-in-web-idl)

### Extend CSP `script-src` (also known as `script-src-v2`)

This feature adds new keywords to the `script-src` Content Security Policy (CSP) directive. This adds two new hash-based allowlisting mechanisms: script sources based on hashes of URLs and contents of `eval()` and `eval()`-like functions. This is sometimes referred to as script-src-v2, although it is backward compatible with the existing script-src, and uses the same directive.

Extending hashes to cover URL and `eval()` hashes lets developers set reasonably strict security policies by narrowly allowlisting scripts by their hashes even when script contents are subject to frequent changes, and known-safe contents of `eval()` without permitting unchecked use of `eval()` broadly.

The new keywords override host-based script-src when provided. This allows a single header to be compatible with browsers that both do or do not implement the new keywords.

[Tracking bug #392657736](https://issues.chromium.org/issues/392657736) | [ChromeStatus.com entry](https://chromestatus.com/feature/5196368819519488) | [Spec](https://github.com/w3c/webappsec-csp/pull/784)

### WebAssembly custom descriptors

Lets WebAssembly store data associated with source-level types more efficiently in new "custom descriptor" objects. These custom descriptors can be configured with prototypes for the WebAssembly objects of that source-level type. This lets you install methods on a WebAssembly object's prototype chain and call them directly from JavaScript using normal method call syntax. The prototypes and methods can be configured declaratively using an imported built-in function.

[Origin Trial](/origintrials#/view_trial/619807898716864513) | [ChromeStatus.com entry](https://chromestatus.com/feature/6024844719947776) | [Spec](https://github.com/WebAssembly/custom-descriptors/blob/main/proposals/custom-descriptors/Overview.md)

## Deprecations and removals

### Stop sending `Purpose: prefetch` header from prefetches and prerenders

Now that prefetches and prerenders are using the `Sec-Purpose` header for prefetches and prerenders, we will move to remove the legacy Purpose: prefetch header that is still currently passed. This will be behind a feature flag/ kill switch to prevent compat issues.

This will be scoped to speculation rules prefetch, speculation rules prerender, , and Chromium's non-standard .

[Tracking bug #420724819](https://issues.chromium.org/issues/420724819) | [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320) | [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-30 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-09-30 UTC."],[],[]] 
