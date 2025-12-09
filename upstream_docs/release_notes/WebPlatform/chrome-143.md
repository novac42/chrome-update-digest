# Chrome 143 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/143

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 143 Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** December 2nd, 2025

Unless otherwise noted, the following changes apply to Chrome 143 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 143](/blog/new-in-chrome-143). 

## CSS and UI

### CSS anchored fallback container queries

Introduces `@container anchored(fallback)` to style descendants of anchor positioned elements based on which of `position-try-fallbacks` is applied.

Such queries can be used to style an anchored element's tether or its animations, based on how the anchor and the anchored element are positioned relative to each other.

[Tracking bug #417621241](https://issues.chromium.org/issues/417621241) | [ChromeStatus.com entry](https://chromestatus.com/feature/5177580990496768) | [Spec](https://drafts.csswg.org/css-anchor-position-2/#anchored-container-queries)

### Side-relative syntax for `background-position-x/y` longhands

Defines the background image's position relative to one of its edges.

This syntax provides a more flexible and responsive mechanism to define the background image position, instead of using fixed values that need to be adapted to the window or frame size.

This feature is applied also to the `-webkit-mask-position` property to ensure webcompat levels are the same.

[Tracking bug #40468636](https://issues.chromium.org/issues/40468636) | [ChromeStatus.com entry](https://chromestatus.com/feature/5073321259565056) | [Spec](https://drafts.csswg.org/css-backgrounds-4/#background-position-longhands)

### Implement CSS property `font-language-override`

Introduces support for `font-language-override` CSS property. The property allows developers to override the system language used for OpenType glyph substitution by specifying a four-character language tag directly in CSS.

This enables fine-grained typographic control, particularly useful for multilingual content or fonts with language-specific glyph variants.

[Tracking bug #41170551](https://issues.chromium.org/issues/41170551) | [ChromeStatus.com entry](https://chromestatus.com/feature/5149766073843712) | [Spec](https://www.w3.org/TR/css-fonts-4/#font-language-override-prop)

### Web App Manifest: specify update eligibility

Specify an update eligibility algorithm in the manifest specification. This makes the update process more deterministic and predictable, giving the dev more control over whether (and when) updates should apply to existing installations, and allowing removal of the _update check throttle_ that user agents currently need to implement to avoid wasting network resources.

[Tracking bug #403253129](https://issues.chromium.org/issues/403253129) | [ChromeStatus.com entry](https://chromestatus.com/feature/5148463647686656)

## Device

### Gamepad `ongamepadconnected` and `ongamepaddisconnected` event handler attributes

Adds `ongamepadconnected` and `ongamepaddisconnected` event handlers to the `WindowEventHandlers` interface mixin.

This enables support for the following event handler attributes:

  * `window.ongamepadconnected`
  * `document.body.ongamepadconnected`
  * `window.ongamepaddisconnected`
  * `document.body.ongamepaddisconnected`

[Tracking bug #40175074](https://issues.chromium.org/issues/40175074) | [ChromeStatus.com entry](https://chromestatus.com/feature/5109540852989952) | [Spec](https://w3c.github.io/gamepad/#extensions-to-the-windoweventhandlers-interface-mixin)

## DOM

### Allow more characters in JavaScript DOM APIs

The HTML parser lets elements and attributes have a wide variety of valid characters and names, but the JavaScript DOM APIs to create the same elements and attributes are more strict and don't match the parser.

This change relaxes the validation of the JavaScript DOM APIs to match the HTML parser.

[Tracking bug #40228234](https://issues.chromium.org/issues/40228234) | [ChromeStatus.com entry](https://chromestatus.com/feature/6278918763708416) | [Spec](https://dom.spec.whatwg.org/#namespaces)

## Graphics

### WebGPU: Texture component swizzle

Allows `GPUTextureViews` to rearrange or replace the color components from texture's red/green/blue/alpha channels when accessed by a shader.

[Tracking bug #414312052](https://issues.chromium.org/issues/414312052) | [ChromeStatus.com entry](https://chromestatus.com/feature/5110223547269120) | [Spec](https://gpuweb.github.io/gpuweb/#dom-gpufeaturename-texture-component-swizzle)

## JavaScript

### ICU 77 (supporting Unicode 16)

The Unicode support library ICU (International Components for Unicode) is upgraded from version 74.2 to 77.1, adding support for Unicode 16 and updating locale data. Two changes could pose some risk for web applications that assume a specific format from the Intl JS APIs:

  1. The default Italian number formatting changed to omit the thousand separator for 4-digit numbers. For example `new Intl.NumberFormat("it").format(1234)` will return 1234 instead of 1.234. The old behavior can be achieved with the `useGrouping` parameter for the `Intl.NumberFormat` constructor.
  2. In some English locales (`en-AU`, `en-GB`, and `en-IN`), a comma was added after full-length weekdays, for example, changing Saturday 30 April 2011 to Saturday, 30 April 2011. Web applications should avoid relying on the precise formatting of dates and they may change again in future.

[Tracking bug #421834885](https://issues.chromium.org/issues/421834885) | [ChromeStatus.com entry](https://chromestatus.com/feature/5143313833000960) | [Spec](https://tc39.es/ecma402)

### EditContext: TextFormat underlineStyle and underlineThickness

The [EditContext API](https://developer.mozilla.org/docs/Web/API/EditContext) shipped with a bug in Chrome where the [`TextFormat`](https://developer.mozilla.org/docs/Web/API/TextFormat) object supplied by the [textformatupdate event](https://developer.mozilla.org/docs/Web/API/EditContext/textformatupdate_event) provides incorrect values for the `underlineStyle` and `underlineThickness` properties. Before Chrome 143 the possible values are `None`, `Solid`, `Dotted`, `Dashed`, `Squiggle` and `None`, `Thin`, `Thick`. However the specification lists `none`, `solid`, `dotted`, `dashed`, `wavy` and `none`, `thin`, `thick`.

The correct values as specified are now implemented from Chrome 143.

[Tracking bug #354497121](https://issues.chromium.org/issues/354497121) | [ChromeStatus.com entry](https://chromestatus.com/feature/6229300214890496) | [Spec](https://w3c.github.io/edit-context/#textformatupdateevent)

### `DataTransfer` property for `insertFromPaste`, `insertFromDrop` and `insertReplacementText` input events

Populate the `dataTransfer` property on input events with an `inputType` of `insertFromPaste`, `insertFromDrop`, and `insertReplacementText` to provide access to clipboard and drag-drop data during editing operations in contenteditable elements.

The `dataTransfer` object contains the same data that was available during the `beforeinput` event.

This feature only applies to contenteditable elements. For form controls (textarea, input), the behavior remains unchanged—the data property contains the inserted text and `dataTransfer` remains null.

[Tracking bug #401593412](https://issues.chromium.org/issues/401593412) | [ChromeStatus.com entry](https://chromestatus.com/feature/6715253274181632) | [Spec](https://w3c.github.io/input-events/#dom-inputevent-datatransfer)

### FedCM: Support structured JSON responses from IdPs

Allows Identity Providers (IdPs) to return structured JSON objects instead of plain strings to Relying Parties (RPs) using the `id_assertion_endpoint`.

This change simplifies integration for developers by eliminating the need to manually serialize and parse JSON strings. It enables more dynamic and flexible authentication flows, allowing RPs to interpret complex responses directly and support varied protocols like OAuth2, OIDC, or IndieAuth without out-of-band agreements.

[Tracking bug #346567168](https://issues.chromium.org/issues/346567168) | [ChromeStatus.com entry](https://chromestatus.com/feature/5153509557272576) | [Spec](https://github.com/w3c-fedid/FedCM/pull/771)

## Network

### WebTransport Application Protocol Negotiation

WebTransport Application Protocol Negotiation allows negotiation of the protocol used by the web application within the WebTransport handshake.

A web application can specify a list of application protocols offered when constructing a `WebTransport` object, which are then conveyed to the server using HTTP headers; if the server picks one of those protocols, it can indicate that within response headers, and that reply is available within the WebTransport object.

[Tracking bug #416080492](https://issues.chromium.org/issues/416080492) | [ChromeStatus.com entry](https://chromestatus.com/feature/6521719678042112) | [Spec](https://w3c.github.io/webtransport/#dom-webtransportoptions-protocols)

## Performance

### Speculation rules: mobile `eager` eagerness improvements

On mobile, `eager` eagerness speculation rules prefetches and prerenders now trigger when HTML anchor elements are in the viewport for a short time.

[Tracking bug #436705485](https://issues.chromium.org/issues/436705485) | [ChromeStatus.com entry](https://chromestatus.com/feature/5086053979521024) | [Spec](https://html.spec.whatwg.org/multipage/speculative-loading.html#speculative-loading)

## WebRTC

### WebRTC RTP header extension behavior change

Implements a change to the specification that ensures that subsequent offer or answer does not permute the header extensions negotiated unless the user wants that to happen.

[Tracking bug #439514253](https://issues.chromium.org/issues/439514253) | [ChromeStatus.com entry](https://chromestatus.com/feature/5135528638939136) | [Spec](https://w3c.github.io/webrtc-extensions/#rtp-header-extension-control-modifications)

## Isolated Web Apps

### Web Smart Card API for Isolated Web Apps

Available on Isolated Web Apps (IWA) only. Enables smart card (PC/SC) applications to move to the Web platform. It gives them access to the PC/SC implementation (and card reader drivers) available in the host OS.

Administrators can control the availability of this API either:

  * Globally—using the `DefaultSmartCardConnectSetting` policy.
  * Per-application—using the `SmartCardConnectAllowedForUrls` and `SmartCardConnectBlockedForUrls` policies.

[Tracking bug #1386175](https://issues.chromium.org/issues/1386175) | [ChromeStatus.com entry](https://chromestatus.com/feature/6411735804674048) | [Spec](https://wicg.github.io/web-smart-card)

## Origin trials

### Digital Credentials API (issuance support)

This feature lets issuing websites (for example, a university, government agency, or bank) to securely initiate the provisioning (issuance) process of digital credentials directly into a user's mobile wallet application. On Android, this capability uses the Android `IdentityCredential` CredMan system (Credential Manager). On Desktop, it uses cross-device approaches using the CTAP protocol similar to Digital Credentials presentation.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/385620718093598721) | [Tracking bug #378330032](https://issues.chromium.org/issues/378330032) | [ChromeStatus.com entry](https://chromestatus.com/feature/5099333963874304) | [Spec](https://w3c-fedid.github.io/digital-credentials)

### Web Install API

Provides the ability to install a web app. When invoked, the website installs either itself, or another site from a different origin, as a web app (depending on the provided parameters).

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/2367204554136616961) | [Tracking bug #333795265](https://issues.chromium.org/issues/333795265) | [ChromeStatus.com entry](https://chromestatus.com/feature/5183481574850560) | [Spec](https://github.com/w3c/manifest/pull/1175)

## Deprecations and removals

## Deprecate XSLT

XSLT v1.0, which all browsers adhere to, was standardized in 1999. In the meantime, XSLT has evolved to v2.0 and v3.0, adding features, and growing apart from the version frozen into browsers. This lack of advancement, coupled with the rise of JavaScript libraries and frameworks that offer more flexible and powerful DOM manipulation, has led to a significant decline in the use of client-side XSLT. Its role within the web browser has been largely superseded by JavaScript-based technologies, such as JSON and React.

Chromium uses the libxslt library to process these transformations, and libxslt was unmaintained for around 6 months of 2025. Libxslt is a complex, aging C codebase of the type notoriously susceptible to memory safety vulnerabilities like buffer overflows, which can lead to arbitrary code execution. Because client-side XSLT is now a niche, rarely-used feature, these libraries receive far less maintenance and security scrutiny than core JavaScript engines, yet they represent a direct, potent attack surface for processing untrusted web content. Indeed, XSLT is the source of several recent high-profile security exploits that continue to put browser users at risk. For these reasons, Chromium (along with both other browser engines) plans to deprecate and remove XSLT from the web platform. For more details, see [Removing XSLT for a more secure browser](/docs/web-platform/deprecating-xslt).

[ChromeStatus.com entry](https://chromestatus.com/feature/4709671889534976)

### Deprecate getters of Intl Locale Info

Intl Locale Info API is a Stage 3 ECMAScript TC39 proposal to enhance the Intl.Locale object by exposing Locale information, such as week data (first day in a week, weekend start day, weekend end day, minimum day in the first week), and text direction hour cycle used in the locale.

Changes in Stage 3 of the specification moves several getters to functions. These are now being updated in Chrome to match the specification.

[Tracking bug #42203770](https://issues.chromium.org/issues/42203770) | [ChromeStatus.com entry](https://chromestatus.com/feature/5148228059398144) | [Spec](https://tc39.es/proposal-intl-locale-info)

### FedCM Privacy Enforcement for Client Metadata

To address cross-site identity correlation risks in the FedCM API, Identity Providers (IdPs) that use client_metadata within their FedCM configuration are required to implement the direct endpoints format in the `.well-known/web-identity` file. This mandate ensures that both accounts_endpoint and login_url are explicitly defined whenever a client_metadata_endpoint is present. This approach strengthens privacy protections by preventing relying parties from exploiting metadata to correlate user identities across multiple sites.

In Chrome 143 (Warning Phase): If client_metadata_endpoint exists but accounts_endpoint or login_url is missing, the browser will display console warnings. This gives IdPs time to update configurations.

[ChromeStatus.com entry](https://chromestatus.com/feature/4614417052467200) | [Spec](https://github.com/w3c-fedid/FedCM/pull/760)

### FedCM-Migration of nonce to params field and renaming of `IdentityCredentialError` `code` attribute to `error`

Migration of nonce to params field: The nonce parameter in navigator.credentials.get() is moving from a top-level field to the params object for better API design, extensibility, and maintainability. This structured approach simplifies parsing for Identity Providers, supports future-proofing without versioning, and aligns with modern API patterns. For Relying Parties, the impact is minimal—they provide the same nonce value in a new location.

In Chrome 143 (Warning Phase): nonce accepted both at top level and inside params. Top-level usage triggers a console warning.

Rename code to error in `IdentityCredentialError`: The `code` attribute in `IdentityCredentialError` is renamed to `error` for clearer semantics, better developer experience, and alignment with web standards. This change reduces ambiguity and avoids conflicts with `DOMException.code`. Additionally, `error.code` becomes `error.error`, retaining its DOMString type.

In Chrome 143 (Warning Phase): Both `error` and `code` attributes are supported. Using `code` triggers a console warning, guiding developers to migrate.

[Tracking bug #427474985](https://issues.chromium.org/issues/427474985) | [ChromeStatus.com entry](https://chromestatus.com/feature/5124072820310016) | [Spec](https://github.com/w3c-fedid/FedCM/pull/768)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-02 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-12-02 UTC."],[],[]] 
