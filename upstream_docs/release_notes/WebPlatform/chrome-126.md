# Chrome 126 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/126

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Docs ](https://developer.chrome.com/docs)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 126

Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** June 11th, 2024

Unless otherwise noted, the following changes apply to Chrome 126 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 126](/blog/new-in-chrome-126). 

## CSS

### Cross-document view transitions for same-origin navigations

Previously you had to rearchitect your website to an SPA to use the View Transitions API. This is no longer the case. View transitions are now enabled by default for same-origin navigations. You can create a view transition between two different documents that are the same-origin.

To enable a cross-document view transition, both ends need to opt-in. To do this, use the `@view-transition` at-rule and set the `navigation` descriptor to `auto`.
    
    
    @view-transition {
      navigation: auto;
    }
    

Cross-document view transitions use the same building blocks and principles as same-document view transitions. Elements that have a `view-transition-name` applied are captured, and you can customize the animations using CSS animations.

[Smooth transitions with the View Transition API](/docs/web-platform/view-transitions) | [Tracking bug #1372584](https://issues.chromium.org/issues/1372584) | [ChromeStatus.com entry](https://chromestatus.com/feature/5118874666663936) | [Spec](https://drafts.csswg.org/css-view-transitions-2)

## Web APIs

### Gamepad API trigger-rumble extension

Extends the `GamepadHapticActuator` interface to expose the [trigger-rumble capability](https://web.dev/articles/gamepad#trigger_rumble) on the Web for compatible gamepads. This extension will allow web applications that take advantage of the Gamepad API to also vibrate the triggers of gamepad devices that come equipped with this functionality.

[Tracking bug #40834175](https://issues.chromium.org/issues/40834175) | [ChromeStatus.com entry](https://chromestatus.com/feature/5162940951953408) | [Spec](https://w3c.github.io/gamepad/#dom-gamepadhapticeffecttype-trigger-rumble)

### ChromeOS tabbed web apps

PWAs in a standalone window can only have one page open at a time. Some apps expect users to have many pages open at once. Tabbed mode adds a tab strip to standalone web apps in ChromeOS that allows multiple tabs to be open at once.

The feature adds a new display mode of `"tabbed"` and a new manifest field to allow customizations to the tab strip.

[Tracking bug #40598974](https://issues.chromium.org/issues/40598974) | [ChromeStatus.com entry](https://chromestatus.com/feature/5128143454076928) | [Spec](https://wicg.github.io/manifest-incubations/#dfn-tabbed)

### `toJSON()` method for `GeolocationCoordinates` and `GeolocationPosition`

Adds `.toJSON()` methods to the `GeolocationCoordinates` and `GeolocationPosition` interfaces. This enables serialization of these objects with `JSON.stringify()`.

[ChromeStatus.com entry](https://chromestatus.com/feature/5606741606924288)

### WebGLObject Web IDL superinterface

This feature exposes the `WebGLObject` type in the same contexts where the WebGL API is exposed—on the main thread and workers.

[ChromeStatus.com entry](https://chromestatus.com/feature/5119115615535104) | [Spec](https://registry.khronos.org/webgl/specs/latest/1.0)

### Re-enabling the `CloseWatcher` API and close requests for `<dialog>` and `popover=""`

The `CloseWatcher` API allows handling close requests, like the `ESC` key on desktop platforms or the back gesture or button on Android, in a uniform way. This feature was originally shipped [in Chrome 120](/blog/new-in-chrome-120), but was disabled due to [an unexpected interaction with `<dialog>`](https://issues.chromium.org/issues/41484805). It has been reenabled in Chrome 126 after some improvements to its behavior to minimize the problems seen there.

[Demo](https://close-watcher-demo.glitch.me/) | [Tracking bug #1171318](https://issues.chromium.org/issues/1171318) | [ChromeStatus.com entry](https://chromestatus.com/feature/4722261258928128)

## Attribution Reporting API: Referrer policy for `attributionsrc` requests

`attributionsrc` requests are treated like other subresources on the page.

Previously when the API is called through the use of the `attributionsrc` attribution as part of various html elements (such as `<img>`, `<script>`, `<a>`, or `window.open`), it ignores the resource-level referrer policy attribute set on the `<html>` element.

With this change the `attributionsrc` request will now apply the same resource-level referrer policy set in the `<img>`, `<script>`, `<a>`, or `window.open`.

This allows ad-techs more control over whether or not they want to be more or less restrictive regarding the referrer information on their `attributionsrc` requests.

[ChromeStatus.com entry](https://chromestatus.com/feature/5191009960198144)

## Media

### MP4 container support for MediaRecorder

Adds support for muxing audio and video into MP4 containers with MediaRecorder.

[MediaRecorder](https://developer.mozilla.org/docs/Web/API/MediaRecorder) | [ChromeStatus.com entry](https://chromestatus.com/feature/5163469011943424) | [Spec](https://www.w3.org/TR/mediastream-recording/)

### OpusEncoderConfig `signal` and `application` parameters

The `OpusEncoderConfig.signal` and `OpusEncoderConfig.application` parameters are mapped directly to implementation specific encoder knobs. These allow web authors to provide hints as to what type of data is being encoded, and in which context the data is being used.

`signal` can be one of `"auto"`, `"music"`, `"voice"`. It configures the encoder for the best performance in encoding the specified type of data. `application` can be one of `"voip"`, `"audio"`, `"lowdelay"`. It configures the encoder to favor speech intelligibility, faithful reproduction of the original input, or minimal latency.

[ChromeStatus.com entry](https://chromestatus.com/feature/5165257615212544) | [Spec](https://w3c.github.io/webcodecs/opus_codec_registration.html#dom-opusencoderconfig-signal)

## JavaScript

### `visualViewport` `onscrollend` support

The `scrollend` JavaScript event fires to signal that a scrolling operation has come to an end.

The `visualViewport` interface includes an `onscrollend` event handler that should be invoked when a scrolling operation on the `visualViewport` has ended. Chrome already supports adding a scrollend event listener through `visualViewport.addEventListener("scrollend")`. This just makes it possible to also add an event listener using `visualViewport.onscrollend`.

[Tracking bug #325307785](https://issues.chromium.org/issues/325307785) | [ChromeStatus.com entry](https://chromestatus.com/feature/5774579609108480)

## Privacy

### Align navigator.cookieEnabled with spec

`navigator.cookieEnabled` currently indicates if "the user agent attempts to handle cookies" in a given context. A change in Chrome, shipping as part of third-party cookie deprecation (3PCD), would cause it to indicate whether unpartitioned cookie access is possible (causing it to return false in most cross-site iframes). We should restore the prior behavior of `navigator.cookieEnabled` which indicated only if cookies were enabled or disabled for the site and rely on the cross-vendor function `document.hasStorageAccess` to indicate if unpartitioned cookie access is possible.

[Tracking bug #335553590](https://issues.chromium.org/issues/335553590) | [ChromeStatus.com entry](https://chromestatus.com/feature/6227655153418240) | [Spec](https://html.spec.whatwg.org/multipage/system-state.html#cookies)

## Accessibility

### Support for the UI Automation Accessibility Framework on Windows

Modern assistive applications on Microsoft Windows use the platform's UI Automation accessibility framework to interoperate with other applications' user interfaces. Until now, Chromium has supported the older Microsoft Active Accessibility (MSAA) and IAccessible2 (IA2) framework for this purpose, which has led to problems with accessibility tools on Windows.

To solve this problem, Microsoft has worked with the Chrome team to support the UI Automation (UIA) framework on Windows directly, making it easier for accessibility tools to communicate with the browser. We'll be starting a gradual rollout to stable, starting in Chrome version 126. This will enable Voice Access to function in all Chromium-based browsers and will enhance the user experience for all UIA-based accessibility tools, such as Narrator and Magnifier.

[Introducing UIA support on Windows](https://developer.chrome.com/blog/windows-uia-support)

## New origin trials

### FedCM as a trust signal for the Storage Access API

Reconciles the FedCM and Storage Access APIs by making a prior FedCM grant a valid reason to automatically approve a storage access request.

When a user grants permission for using their identity with a third-party Identity Provider (IdP) on a Relying Party (RP), many IdPs require third-party cookies to function correctly and securely. This proposal aims to satisfy that requirement in a private and secure manner by updating the Storage Access API (SAA) permission checks to not only accept the permission grant that is given by a storage access prompt, but also the permission grant that is given by a FedCM prompt.

A key property of this mechanism is limiting the grant to cases explicitly allowed by the RP through the FedCM permissions policy, enforcing a per-frame control for the RP and preventing passive surveillance by the IdP beyond the capabilities that FedCM already grants.

[Origin Trial](/origintrials#/view_trial/4008766618313162753) | [Explainer](https://github.com/explainers-by-googlers/storage-access-for-fedcm) | [ChromeStatus.com entry](https://chromestatus.com/feature/5116478702747648)

### Media previews opt-out

This reverse origin trial excludes sites from the launch of Media Previews.

Chrome will provide real-time previews of camera and microphone input at the time camera and microphone permissions are requested by websites. These will also be available from the site's pageinfo.

In addition, users with multiple devices will be able to select a camera and microphone at the time permissions are requested, unless the site has requested a specific device through `getUserMedia()`.

[Origin Trial](/origintrials#/register_trial/3270176279424401409) | [Tracking bug #330762482](https://issues.chromium.org/issues/330762482) | [ChromeStatus.com entry](https://chromestatus.com/feature/5100528783851520)

### FedCM: Continuation API, Parameters API, Fields API, Multiple configURLs, Custom Account Labels

Developers can start taking part in an origin trial for a bundle of desktop FedCM features that can include authorization. The bundle consists of FedCM Continuation API, Parameter API, Fields API, Multiple configURLs, and Custom Account Labels. This enables an OAuth authorization flow-like experience involving an IdP-provided permission dialog.

[Tracking bug #40262526](https://issues.chromium.org/issues/40262526) | [ChromeStatus.com entry](https://chromestatus.com/feature/6495400321351680)

### Page-Embedded Permission Control

Provide a new HTML element that interacts with the permission flow.

The permission prompt is currently triggered directly from JavaScript without the user agent having any strong signal of the user's intent. Having an in-content element that the user uses to trigger the permission flow allows for improved permission prompt UX for users as well as a recovery path from the "denied" permission state for sites.

[ChromeStatus.com entry](https://chromestatus.com/feature/5125006551416832)

## Deprecations and removals

### Dreprecate and remove import assertion 'assert' syntax

Deprecate and remove the `assert` keyword in favor of the new `with` keyword in import attribute syntax.

That is, `import m from 'foo' assert { type: 'json' }` will now throw a SyntaxError, and developers must change to `import m from 'foo' with { type: 'json' }`.

[ChromeStatus.com entry](https://chromestatus.com/feature/4689167795879936) | [Spec](https://tc39.es/proposal-import-attributes)

## Further reading

Looking for more? Check out these additional resources.

  * [What's new in Chrome 126](/blog/new-in-chrome-126)
  * [What's new in Chrome DevTools 126](/blog/new-in-devtools-126)
  * [ChromeStatus.com updates for Chrome 126](https://chromestatus.com/features#milestone%3D126)
  * [Chrome release calendar](https://chromiumdash.appspot.com/schedule)
  * [Upcoming deprecations](https://chromestatus.com/features#browsers.chrome.status%3A%22Deprecated%22)
  * [Upcoming removals](https://chromestatus.com/features#browsers.chrome.status%3A%22Removed%22)

## Download Google Chrome

Download Chrome for [Android](https://play.google.com/store/apps/details?id=com.android.chrome), [Desktop](https://www.google.com/chrome/), or [iOS](https://apps.apple.com/us/app/google-chrome/id535886823). 

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2024-06-11 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2024-06-11 UTC."],[],[]] 
