# Chrome 125 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/125

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Docs ](https://developer.chrome.com/docs)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 125

Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** May 14th, 2024

Unless otherwise noted, the following changes apply to Chrome 125 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 125](/blog/new-in-chrome-125). 

## HTML and DOM

### Declarative shadow DOM serialization

A feature to let developers serialize DOM trees containing shadow roots, recently standardized in the HTML standard.

[Tracking bug #41490936](https://issues.chromium.org/issues/41490936) | [ChromeStatus.com entry](https://chromestatus.com/feature/5102952270528512) | [Spec](https://html.spec.whatwg.org/#dom-element-gethtml)

## CSS

### CSS Anchor Positioning

CSS anchor positioning lets developers _tether_ an absolutely positioned element to one or more other elements on the page (the _anchors_), in a declarative way, without the use of JavaScript. Anchor positioning works performantly when the anchors are scrollable. A common use case is to position a popover such as a tooltip next to the element that invoked it, or a select menu and its popover options list. Before the anchor positioning feature, these use cases required JavaScript to dynamically position the popover, and keep it anchored as the invoking element was scrolled, which is a performance footgun and difficult to get right. With anchor positioning, these use cases can be implemented performantly and declaratively.

The anchor positioning feature consists of a large number of CSS properties. A few of the key properties are as follows:

  * `anchor-name`: sets up an element to be an anchor for other elements.
  * `position-anchor`: describes the "default" anchor that an anchored element should use for anchor positioning.
  * The `anchor()` function: used to refer to the position of the anchor element, in positioning the anchored element.
  * `inset-area`: a shorthand for positioning, for common relative positions.

[Introducing the CSS anchor positioning API](/blog/anchor-positioning-api) | [Tracking bug #40059176](https://issues.chromium.org/issues/40059176) | [ChromeStatus.com entry](https://chromestatus.com/feature/5124922471874560) | [Spec](https://drafts.csswg.org/css-anchor-position-1)

### CSS stepped value functions—`round()`, `mod()`, and `rem()`

The stepped-value functions, [`round()`](https://developer.mozilla.org/docs/Web/CSS/round), [`mod()`](https://developer.mozilla.org/docs/Web/CSS/mod), and [`rem()`](https://developer.mozilla.org/docs/Web/CSS/rem), all transform a given value according to another "step value".

The `round()` CSS function returns a rounded number based on a selected rounding strategy.

The `mod()` CSS function returns a modulus left over when the first parameter is divided by the second parameter, similar to the JavaScript remainder operator (%). The modulus is the value left over when one operand, the dividend, is divided by a second operand, the divisor. It always takes the sign of the divisor.

The `rem()` CSS function returns a remainder left over when the first parameter is divided by the second parameter, similar to the JavaScript remainder operator (%). The remainder is the value left over when one operand, the dividend, is divided by a second operand, the divisor. It always takes the sign of the dividend.

[Tracking bug #40253179](https://issues.chromium.org/issues/40253179) | [ChromeStatus.com entry](https://chromestatus.com/feature/5500897196244992) | [Spec](https://drafts.csswg.org/css-values/#round-func)

**Baseline Newly Available:** This feature is now available in all three major browser engines. 

### New syntax for CSS custom `:state()`

CSS custom state lets custom elements expose their own pseudo-classes. The syntax has now been spec'ed in the CSSWG, and Chrome 125 now supports the new syntax `:state(foo)`. This change will have a window where Chrome will support both the old syntax (`:--foo`) and the new syntax so websites can switch to the new one.

[ChromeStatus.com entry](https://chromestatus.com/feature/5586433790443520) | [Spec](https://html.spec.whatwg.org/multipage/custom-elements.html#custom-state-pseudo-class)

### Remove discontinuity for Oklab and Oklch colors with lightness of nearly 100% or 0

Before this change, all Lab, LCH, Oklab and Oklch colors with a lightness value of 100% were rendered as white, regardless of the other two parameters. All colors in these spaces with a lightness value of 0 were rendered as black. These two mappings caused discontinuities in gradients and were unexpected to web developers.

With this rollback, these colors are no longer mapped artificially and the resulting displayed color will be continuous with nearby colors and depend on the gamut mapping of the display.

[ChromeStatus.com entry](https://chromestatus.com/feature/5534009582157824) | [Spec](https://html.spec.whatwg.org/#dom-element-gethtml)

### Used color scheme root scrollbars

Makes the browser use the user's preferred color scheme to render the viewport scrollbars if the value of "page's supported color schemes" is 'normal' or not specified, and the computed value of [`color-scheme`](https://www.w3.org/TR/css-color-adjust-1/#color-scheme-prop) for the root element is `normal`. Viewport scrollbars can be considered to be outside the web content. Therefore, the user agents should honor the user's preferred color scheme when rendering viewport scrollbars if the developer has not explicitly specified support for color schemes.

This change does not prevent developers from controlling the color scheme for scrollbars. The new behavior makes the browser use the user's preferred color-scheme to render viewport non-overlay scrollbars only if the developer hasn't specified the color scheme for the root element.

[title](/release-notes/125/url) | [Tracking bug #40259909](https://issues.chromium.org/issues/40259909) | [ChromeStatus.com entry](https://chromestatus.com/feature/5089486318075904) | [Spec](https://www.w3.org/TR/css-color-adjust-1)

### `view-transitions` class

There's a new CSS property `view-transition-class` which allows the you to specify one or more view transition classes. You can then select the `ViewTransition` pseudo elements using these classes, for example `::view-transition-group(*.class)`.

This is an extension to the [ViewTransition API](/docs/web-platform/view-transitions) that simplifies styling of view transition pseudo elements in a similar way that CSS classes simplify styling of regular DOM elements.

[Tracking bug #41492972](https://issues.chromium.org/issues/41492972) | [ChromeStatus.com entry](https://chromestatus.com/feature/5064894363992064) | [Spec](https://drafts.csswg.org/css-view-transitions-2/#view-transition-class-prop)

## Loading

### Accept HTTP and HTTPS URLs when constructing WebSocket

This update enables HTTP and HTTPS schemes in the WebSocket constructor, therefore also letting developers use relative URLs. These are normalized to the `ws:` and `wss:` internal schemes.

[Tracking bug #325979102](https://issues.chromium.org/issues/325979102) | [ChromeStatus.com entry](https://chromestatus.com/feature/5848709993857024) | [Spec](https://github.com/whatwg/websockets/pull/45)

## Web APIs

### Additions to the Attribution Reporting API

Features have been added to the Attribution Reporting API to create additional debugging capabilities by supporting parsing failure debug reports, improve API ergonomics by supporting a field to specify preferred registration platform, and improve privacy.

[ChromeStatus.com entry](https://chromestatus.com/feature/5146883686400000)

### The Compute Pressure API

The [Compute Pressure API](/docs/web-platform/compute-pressure) offers high-level states that represent the CPU load on the system. It allows the implementation to use the right underlying hardware metrics to ensure that users can take advantage of all the processing power available to them as long as the system is not under unmanageable stress.

Intel led the design and implementation work for this API, which will let video conferencing apps dynamically balance features and performance.

[Compute Pressure API](/docs/web-platform/compute-pressure) | [Tracking bug #40683064](https://issues.chromium.org/issues/40683064) | [ChromeStatus.com entry](https://chromestatus.com/feature/5597608644968448) | [Spec](https://html.spec.whatwg.org/#dom-element-gethtml)

### Extending Storage Access API (SAA) to non-cookie storage

This launches the proposed extension of the Storage Access API (backwards compatible and has been in origin trial) to allow access to unpartitioned cookie and non-cookie storage in a third-party context. The current API only provides access to cookies, which have different use-cases than non-cookie storage.

[Tracking bug #40282415](https://issues.chromium.org/issues/40282415) | [ChromeStatus.com entry](https://chromestatus.com/feature/5175585823522816) | [Spec](https://privacycg.github.io/saa-non-cookie-storage)

### FedCM CORS requirement on ID assertion endpoint

The fetches in the FedCM API are hard to reason about because of the properties required of them. While there is ongoing discussion regarding the accounts endpoint, there is also largely consensus that the ID assertion endpoint should use CORS. This update aligns security properties of this fetch more closely to other fetches in the web platform.

[FedCM updates: Button Mode API origin trial, CORS and SameSite](https://developers.google.com/privacy-sandbox/blog/fedcm-chrome-125-updates#cors-and-samesite) | [Tracking bug #40284123](https://issues.chromium.org/issues/40284123) | [ChromeStatus.com entry](https://chromestatus.com/feature/5094763339710464)

### FedCM credentialed request no longer sends SameSite=Strict cookie

FedCM now sends ID assertion requests with CORS. That change means that Chrome no longer send `SameSite=Strict` cookies to the ID assertion endpoint, though Chrome stills send `SameSite=None`. Since it does not make sense to send a different set of cookies to the accounts endpoint and the ID assertion endpoint, this change makes them consistent.

Not sending `SameSite=Strict` cookies is also consistent with [`requestStorageAccess` behavior](https://developers.google.com/privacy-sandbox/3pcd/related-website-sets-integration#cookie_requirements) and cross-site requests in general.

[Tracking bug #329145816](https://issues.chromium.org/issues/329145816) | [ChromeStatus.com entry](https://chromestatus.com/feature/5092883024838656) | [Spec](https://fedidcg.github.io/FedCM/#fetch-identity-assertion)

### Interoperable mousemove default action

Chrome allowed canceling mousemove events to prevent other APIs like text selection (and even drag-and-drop in the past). This does not match other major browsers; nor does it conform to the UI Event spec. Now text selection will no longer be the default action of mousemove. Text selection and drag-and-drop can still be prevented through canceling `selectstart` and `dragstart` events respectively.

This feature will be rolled out slowly starting from Chrome 125, and is expected to be available to all users by Chrome 126.

[Demo](https://codepen.io/mustaqahmed/full/wvNYGEP) | [Tracking bug #40078978](https://issues.chromium.org/issues/40078978) | [ChromeStatus.com entry](https://chromestatus.com/feature/5145305056280576) | [Spec](https://w3c.github.io/uievents/#event-type-mousemove)

### Regular expression modifiers

Regular expression modifiers adds the ability to locally modify the `i`, `m`, and `s`' flags inside a pattern.

To enable a flag for a subexpression, use `(?X:subexpr)` where `X` is one of `i`, `m`, or `s`. To disable a flag for a subexpression, use `(-X:subexpr)`.

For example, for the case-insensitivity `i` flag:
    
    
    const re1 = /^[a-z](?-i:[a-z])$/i;
    re1.test("ab"); // true
    re1.test("Ab"); // true
    re1.test("aB"); // false
    
    const re2 = /^(?i:[a-z])[a-z]$/;
    re2.test("ab"); // true
    re2.test("Ab"); // true
    re2.test("aB"); // false
    

[ChromeStatus.com entry](https://chromestatus.com/feature/5100254548721664) | [Spec](https://tc39.es/proposal-regexp-modifiers)

### Regular expression duplicate named capture groups

Duplicate named capture groups lets you use the same capturing group name across alternatives. For example
    
    
    const re = /(?<year>[0-9]{4})-[0-9]{2}|[0-9]{2}-(?<year>[0-9]{4})/;
    

In this case, `year` is valid for either the 1st alternative (`(?<year>[0-9]{4})-[0-9]{2}`), or the 2nd alternative (`[0-9]{2}-(?<year>[0-9]{4})`).

[ChromeStatus.com entry](https://chromestatus.com/feature/5149208388829184) | [Spec](https://github.com/tc39/ecma262/pull/2721)

## Chrome Apps

### Direct Sockets API in Chrome Apps

This update helps ease the transition of specialized apps from Chrome Apps to Isolated Web Apps by enabling Direct Sockets in Chrome Apps, letting web apps establish direct transmission control protocol (TCP) and user datagram protocol (UDP) communications with network devices and systems.

[ChromeStatus.com entry](https://chromestatus.com/feature/5168654087094272) | [Spec](https://wicg.github.io/direct-sockets)

## New origin trials

### FedCM Button Mode API and Use Other Account API

This origin trial includes the following two FedCM APIs.

The Button Mode API lets websites call FedCM inside a button click, such as clicking on a **Sign-in to IdP** button. This requires FedCM to guarantee it always responds with a visible user interface, as opposed to widget mode, which doesn't show a UI when users log out. Calling the FedCM API in _button mode_ takes users to login to the IdP (in a dialog window), when users are logged-out.

Also, because the button mode is called within an explicit user gesture, the UI may also be more prominent (for example, centered and modal) compared to the UI from the widget mode (which doesn't have such explicit intention). Learn more about how the Button Mode API works in [FedCM updates: Button Mode API origin trial, CORS and SameSite](https://developers.google.com/privacy-sandbox/blog/fedcm-chrome-125-updates#button-mode-api)

The Use Other Account API lets an Identity Provider allow users to sign in to other accounts.

[Origin Trial](/origintrials#/view_trial/3196429835526209537) | [Demo](https://fedcm-button.glitch.me/) | [Tracking bug #40284792](https://issues.chromium.org/issues/40284792) | [ChromeStatus.com entry](https://chromestatus.com/feature/4689551782313984) | [Spec](https://github.com/fedidcg/FedCM/issues/442#issuecomment-1949323416)

### Foldable APIs

This origin trial includes the Device Posture API and Viewport Segments Enumeration API. These APIs are designed to help developers target foldable devices.

[Origin Trial](/origintrials#/view_trial/4188910603407982593) | [Origin trial for Foldable APIs](/blog/foldable-apis-ot) | [ChromeStatus.com entry](https://chromestatus.com/feature/5121612962856960) | [Spec](https://www.w3.org/TR/device-posture)

### Deprecation trial for prefixed HTMLVideoElement Fullscreen properties and methods

This deprecation trial lets you opt back into support for the prefixed HTMLVideoElement properties and methods if you need more time to adjust your code.

[Origin Trial](/origintrials#/register_trial/300896750103691264) | [ChromeStatus.com entry](https://chromestatus.com/feature/5111638103687168)

### Skip preload scanning

Skips the [preload scanner](https://web.dev/articles/preload-scanner) to explore performance tradeoffs for pages with no sub-resource fetches.

The preload scanner step benefits performance of pages with sub-resource fetches, through implementation of the speculative prefetch. However, for pages that don't benefit from this step, that is, for pages with no sub-resources, this is additional processing overhead with little benefit.

For advanced web users who would like to benefit by reducing this overhead, this experiment provides a page-level control to disable the preload scanner. Data collected from this experiment could evaluate if a modified API or a different implementation of the HTML preload scanner would be helpful.

[Origin Trial](/origintrials#/view_trial/919297273937002497) | [Tracking bug #330802493](https://issues.chromium.org/issues/330802493) | [ChromeStatus.com entry](https://chromestatus.com/feature/5190976638550016) | [Spec](https://docs.google.com/document/d/1wiaTL5TeONTZamycMVMjo76nMcbhHNYznQy7I_zCVRY/preview)

## Deprecations and removals

### Remove "window-placement" alias for permission and permission policy "window-management"

Removes the "window-placement" alias for permission and permission policy "window-management". This is part of a larger effort to rename the strings by eventually [deprecating and removing "window-placement"](/docs/capabilities/web-apis/window-management#the_window-management_permission). The terminology change improves the longevity of the descriptor as the Window Management API evolves over time.

[title](/release-notes/125/url) | [Tracking bug #40842072](https://issues.chromium.org/issues/40842072) | [ChromeStatus.com entry](https://chromestatus.com/feature/5137018030391296) | [Spec](https://w3c.github.io/window-management/#api-permission-api-integration)

### Removal of Enterprise policy: `NewBaseUrlInheritanceBehaviorAllowed`

The underlying code change (enable new base URL inheritance behavior) that this enterprise policy overrides has been enabled in stable releases since August 2023 (Chrome 118). Since known issues have been dealt with, this enterprise policy has been removed in Chrome 125.

[ChromeStatus.com entry](https://chromestatus.com/feature/5122505296838656)

### Removal of prefixed HTMLVideoElement Fullscreen properties and methods

The prefixed `HTMLVideoElement` fullscreen APIs have been deprecated since Chrome 38. They were replaced by `Element.requestFullscreen()`, which first shipped un-prefixed in 2018 in Chrome 71.

The following properties and methods will be removed from HTMLVideoElement:

  * `webkitSupportsFullscreen`
  * `webkitDisplayingFullscreen`
  * `webkitEnterFullscreen()`
  * `webkitExitFullscreen()`
  * `webkitEnterFullScreen()` (note the different capitalization of the "S" in FullScreen)
  * `webkitExitFullScreen()`

Register for the deprecation trial listed in this post, if your site still relies on these and you need more time for updating code.

[ChromeStatus.com entry](https://chromestatus.com/feature/5111638103687168)

## Further reading

Looking for more? Check out these additional resources.

  * [What's new in Chrome 125](/blog/new-in-chrome-125)
  * [What's new in Chrome DevTools 125](/blog/new-in-devtools-125)
  * [ChromeStatus.com updates for Chrome 125](https://chromestatus.com/features#milestone%3D125)
  * [Chrome release calendar](https://chromiumdash.appspot.com/schedule)
  * [Upcoming deprecations](https://chromestatus.com/features#browsers.chrome.status%3A%22Deprecated%22)
  * [Upcoming removals](https://chromestatus.com/features#browsers.chrome.status%3A%22Removed%22)

## Download Google Chrome

Download Chrome for [Android](https://play.google.com/store/apps/details?id=com.android.chrome), [Desktop](https://www.google.com/chrome/), or [iOS](https://apps.apple.com/us/app/google-chrome/id535886823). 

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2024-05-14 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2024-05-14 UTC."],[],[]] 
