# Chrome 124 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/124

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Docs ](https://developer.chrome.com/docs)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 124

Stay organized with collections  Save and categorize content based on your preferences. 

Unless otherwise noted, the following changes apply to Chrome 124 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. Learn more about the features listed here through the provided links or from the list on [ChromeStatus.com](https://chromestatus.com/features#milestone%3D124). Chrome 124 is stable as of 16 April 2024. You can download the latest on [Google.com](https://www.google.com/chrome/) for desktop or on the [Google Play Store](https://play.google.com/store/apps/details?id=com.android.chrome) for Android.

Want just the highlights? Check out [New in Chrome 124](/blog/new-in-chrome-124).

## Browser Changes and Developer Tools

### Universal install

Make any page installable even those not meeting the current PWA installability criteria.

### Keyboard-focusable scroll containers

Improves accessibility by making scroll containers focusable using sequential focus navigation. Prior to this change, the tab key doesn't focus scrollers unless `tabIndex` is explicitly set to 0 or more.

By making scrollers focusable by default, users who can't (or don't want to) use a mouse will be able to focus clipped content using a keyboard's tab and arrow keys. This behavior is enabled only if the scroller does not contain any keyboard focusable children.

This feature will be rolled out slowly starting from Chrome 124, and available to all users by Chrome 125.

[Keyboard focusable scrollers](/blog/keyboard-focusable-scrollers) | [Tracking bug #40113891](https://issues.chromium.org/issues/40113891) | [ChromeStatus.com entry](https://chromestatus.com/feature/5231964663578624) | [Spec](https://html.spec.whatwg.org/multipage/interaction.html#attr-tabindex)

### Permissions Prompt for Web MIDI API

This feature gates access to the [Web MIDI API](https://developer.mozilla.org/docs/Web/API/Web_MIDI_API) behind a permissions prompt. Previously, the use of SysEx messages with the Web MIDI API requires an explicit user permission.From Chrome 125, all access to the Web MIDI API requires a user permission.

This feature will be rolled out slowly starting from Chrome 124, and available to all users by Chrome 125.

[Tracking bug #40063295](https://issues.chromium.org/issues/40063295) | [ChromeStatus.com entry](https://chromestatus.com/feature/5087054662205440) | [Spec](https://www.w3.org/TR/webmidi/#methods)

## HTML and DOM

### The `writingsuggestions` attribute

Browsers are starting to provide writing suggestions to users as they type on various editable fields across the web. While this is generally useful for users, there are cases when developers may want to turn off browser-provided writing assistance, such as extensions or sites that provide similar functionality of their own.

The new attribute `writingsuggestions` has values of `true` or `false` that allow developers to turn on or off browser-provided writing suggestions. The attribute's state for an element can also be inherited from ancestor elements, thereby allowing developers to control this ability at a per-element or per-document or sub-document scale.

[ChromeStatus.com entry](https://chromestatus.com/feature/5153375153029120) | [Spec](https://html.spec.whatwg.org/multipage/interaction.html#writing-suggestions)

## Loading

### Sec-CH-UA-Form-Factors client hint

This hint gives a server information about the user agent's form-factors. It returns one or more of the following form-factor values:

  * **Desktop** : A user-agent running on a personal computer.
  * **Automotive** : A user-agent embedded in a vehicle, where the user may be responsible for operating the vehicle and unable to attend to small details.
  * **Mobile** : Small, touch-oriented device typically carried on a user's person.
  * **Tablet** : A touch-oriented device larger than "Mobile" and not typically carried on a user's person.
  * **XR** : Immersive devices that augment or replace the environment around the user.
  * **EInk** : A device characterized by slow screen updates and limited or no color resolution.
  * **Watch** : A mobile device with a tiny screen (typically less than two inches), carried in such a way that the user can glance at it quickly.

[ChromeStatus.com entry](https://chromestatus.com/feature/5162545698045952) | [Spec](https://wicg.github.io/ua-client-hints/#sec-ch-ua-form-factor)

### Private Network Access permission to relax mixed content

To establish connections to devices on a local network that don't have globally unique names, and therefore cannot obtain TLS certificates, this feature introduces a new option to `fetch()` to declare a developers' intent to talk to such a device. This includes a new policy-controlled feature to gate each site's access to this capability, and new headers for the server's preflight response to provide additional metadata.

[ChromeStatus.com entry](https://chromestatus.com/feature/5954091755241472) | [Spec](https://wicg.github.io/private-network-access)

### `priority` HTTP request header

This adds the `priority` request header for all HTTP requests with the priority information for the request at the time that it was sent.

RFC 9218 (Extensible Prioritization Scheme for HTTP) defines a `priority` HTTP request header to use for signaling request priority to origins (and intermediaries). It also defines negotiation processes and protocol-level frames for HTTP/2 and HTTP/3 to carry the same priority information.

The header can only signal the initial priority for a resource when it was first requested while the frame-based mechanisms allow for modifying the priority after the fact.

The header can operate end-to-end to the origin servers (and provide a mechanism for the origin to override the priority if recognized by intermediaries) while the frames are limited to operating on a link level.

This feature is specifically for supporting the header-based prioritization scheme.

[Tracking bug #40252001](https://issues.chromium.org/issues/40252001) | [ChromeStatus.com entry](https://chromestatus.com/feature/5109106573049856) | [Spec](https://datatracker.ietf.org/doc/rfc9218)

### Document render-blocking

This feature enables authors to block rendering of a document until the critical content has been parsed, ensuring a consistent first paint across all browsers. Without this feature, the first paint's state depends on the heuristics for parser yielding which can vary across browsers.

This is particularly important for View Transitions where the parsed DOM state on the first frame can drastically change the transition created.

Note that this feature implements a `<link rel=expect href="#id">` syntax that allows a link element to reference another expected element on the page. The rendering is then blocked until the expected element is fully parsed. This supersedes the previous implementation of an HTML attribute that allows the whole document to be render-blocked.

[ChromeStatus.com entry](https://chromestatus.com/feature/5113053598711808) | [Spec](https://html.spec.whatwg.org/multipage/links.html#link-type-expect)

### X25519Kyber768 key encapsulation for TLS

Protects current Chrome TLS traffic against future quantum cryptanalysis by deploying the Kyber768 quantum-resistant key agreement algorithm.

This is a hybrid X25519 and Kyber768 key agreement based on an IETF standard. This specification and launch is outside the scope of W3C. This key agreement will be launched as a TLS cipher, and should be transparent to users.

[Protecting Chrome Traffic with Hybrid Kyber KEM](https://blog.chromium.org/2023/08/protecting-chrome-traffic-with-hybrid.html) | [Tracking bug #40910498](https://issues.chromium.org/issues/40910498) | [ChromeStatus.com entry](https://chromestatus.com/feature/5257822742249472) | [Spec](https://www.ietf.org/archive/id/draft-tls-westerbaan-xyber768d00-02.html)

## Media

### `jitterBufferTarget` attribute

The `jitterBufferTarget` attribute allows applications to specify a target duration of time in milliseconds of media for the `RTCRtpReceiver` jitter buffer to hold. This influences the amount of buffering done by the user agent, which in turn affects retransmissions and packet loss recovery. Altering the target value allows applications to control the tradeoff between playout delay and the risk of running out of audio or video frames due to network jitter.

[Tracking bug #324276557](https://issues.chromium.org/issues/324276557) | [ChromeStatus.com entry](https://chromestatus.com/feature/5930772496384000) | [Spec](https://w3c.github.io/webrtc-extensions/#dom-rtcrtpreceiver-jitterbuffertarget)

## Web APIs

### The WebSocketStream API

The WebSocket API provides a JavaScript interface to the RFC6455 WebSocket protocol. While it has served well, it is awkward from an ergonomics perspective and is missing the important feature of backpressure. The intent of the WebSocketStream API is to resolve these deficiencies by integrating WHATWG Streams with the WebSocket API.

[WebSocketStream: integrating streams with the WebSocket API](/docs/capabilities/web-apis/websocketstream) | [Tracking bug #41470216](https://issues.chromium.org/issues/41470216) | [ChromeStatus.com entry](https://chromestatus.com/feature/5189728691290112) | [Spec](https://github.com/whatwg/websockets/pull/48)

### `setHTMLUnsafe` and `parseHTMLUnsafe`

The `setHTMLUnsafe` and `parseHTMLUnsafe` methods allow the Declarative Shadow DOM to be used from JavaScript. These methods also offer an easier way to imperatively parse HTML into DOM, as compared to `innerHTML` or `DOMParser`.

[ChromeStatus.com entry](https://chromestatus.com/feature/6560361081995264) | [Spec](https://html.spec.whatwg.org/C/#unsafe-html-parsing-methods)

### Streams API: ReadableStream async iteration

The streams APIs provide ubiquitous, interoperable primitives for creating, composing, and consuming streams of data. This change adds support for the [async iterable protocol to the ReadableStream API](https://web.dev/articles/streams#asynchronous_iteration), enabling readable streams to be used as the source of for `await...of` loops.

[Tracking bug #40612900](https://issues.chromium.org/issues/40612900) | [ChromeStatus.com entry](https://chromestatus.com/feature/5143121161879552) | [Spec](https://streams.spec.whatwg.org/#rs-asynciterator)

### `pageswap` event

The `pageswap` event is fired on a document's window object when a navigation will replace this document with a new document. The event provides activation info about the navigation (`type`, `NavigationHistoryEntry` for the new document).

If the navigation has a cross-document view transition, the event is dispatched before capturing state for the old document. This allows the developer to configure the old state captured for the transition based on the navigation's activation info and the current visual state of the old document.

[Tracking bug #41495176](https://issues.chromium.org/issues/41495176) | [ChromeStatus.com entry](https://chromestatus.com/feature/5479301497749504) | [Spec](https://html.spec.whatwg.org/#the-pageswapevent-interface)

### Additions to the Attribution Reporting API

Features have been added to the [Attribution Reporting API](https://developers.google.com/privacy-sandbox/relevance/attribution-reporting) to create additional debugging capabilities by supporting parsing failure debug reports, improve API ergonomics by supporting a field to specify preferred registration platform, and improve privacy.

### Document picture-in-picture: add option to hide back-to-tab button

This adds a new parameter (`disallowReturnToOpener`) to the [Document picture-in-picture API](https://developer.mozilla.org/docs/Web/API/Document_Picture-in-Picture_API) that, when set to true, hints to the browser that it shouldn't show a button in the picture-in-picture window that allows the user to go back to the opener tab.

While having a button to return to the opener tab always makes sense in the video picture-in-picture case (the video stream can be returned to the video element in the opener tab), this is not always the case for document picture-in-picture experiences. This gives developers more control over the user experience when they determine that such a button does not make sense for their use case.

[Documentation for Document picture-in-picture](/docs/web-platform/document-picture-in-picture#hide_the_back_to_tab_button_of_the_picture-in-picture_window) | [ChromeStatus.com entry](https://chromestatus.com/feature/6223347936657408) | [Spec](https://github.com/WICG/document-picture-in-picture/pull/114)

## Rendering and Graphics

### SVG `context-fill` and `context-stroke`

Implements an existing SVG feature that allows the keywords `context-fill` and `context-stroke` when specifying fill and stroke properties. This only affects SVG sub-trees that are instantiated with a `<use>` element, and `<marker>` elements that are instantiated using the `marker` property on a `<path>` element. In those circumstances, `context-fill` and `context-stroke` are resolved to the value of the `fill` and `stroke` properties on the `<use>` or `<path>`.

[ChromeStatus.com entry](https://chromestatus.com/feature/5146558556536832) | [Spec](https://svgwg.org/svg2-draft/painting.html#context-paint)

### WebGPU: ServiceWorker and SharedWorker support

[ServiceWorker and SharedWorker support](/blog/new-in-webgpu-124#service_workers_and_shared_workers_support) is added to WebGPU, aligning with existing WebGL capabilities.

Service Workers enable offline capabilities and background processing for WebGPU. This means graphics-intensive web applications or Chrome Extensions can cache resources and perform computations even when the user isn't actively interacting with the page.

Shared Workers allow multiple tabs or extension contexts to coordinate and share WebGPU resources. This leads to smoother performance and more efficient use of the user's graphics hardware.

[Tracking bug #41494731](https://issues.chromium.org/issues/41494731) | [ChromeStatus.com entry](https://chromestatus.com/feature/4875951026733056) | [Spec](https://gpuweb.github.io/gpuweb/#navigator-gpu)

## Origin trials in progress

In Chrome 124 you can opt into the following new [origin trials](/docs/web-platform/origin-trials).

### Deprecation trial for mutation events

Mutation events, including `DOMSubtreeModified`, `DOMNodeInserted`, `DOMNodeRemoved`, `DOMNodeRemovedFromDocument`, `DOMNodeInsertedIntoDocument`, and `DOMCharacterDataModified`, can damage page performance, and also significantly increase the complexity of adding new features to the Web. These APIs were deprecated from the specification in 2011, and were replaced (in 2012) by the much better-behaved Mutation Observer API.

Mutation event support [will be disabled by default starting in Chrome 127](/blog/mutation-events-deprecation), around July 30, 2024. Code should be migrated to the Mutation Observer API before that date to avoid site breakage. If more time is needed, register for [Mutation events deprecation trial](/origintrials#/view_trial/919297273937002497) to re-enable the feature for a limited time on a given site. This can be used through Chrome 134, ending March 25, 2025.

Alternatively, a `MutationEventsEnabled` enterprise policy can also be used for the same purpose, also through Chrome 134.

[Origin Trial](/origintrials#/view_trial/919297273937002497) | [Tracking bug #40268638](https://issues.chromium.org/issues/40268638) | [ChromeStatus.com entry](https://chromestatus.com/feature/5083947249172480) | [Spec](https://w3c.github.io/uievents/#legacy-event-types)

## Deprecations and removals

This version of Chrome introduces the following deprecations and removals. Visit [ChromeStatus.com](https://chromestatus.com) for lists of [deprecations](https://chromestatus.com/features#browsers.chrome.status%3A%22Deprecated%22) and [removals](https://chromestatus.com/features#browsers.chrome.status%3A%22Removed%22).

There are no deprecations or removals in Chrome 124.

## Further reading

Looking for more? Check out these additional resources.

  * [What's new in Chrome (124)](/blog/new-in-chrome-124)
  * [What's new in Chrome DevTools (124)](/blog/new-in-devtools-124)
  * [ChromeStatus.com updates for Chrome 124](https://chromestatus.com/features#milestone%3D124)
  * [Chromium source repository change list](https://chromium.googlesource.com/chromium/src/+log/123.0.6312.129..124.0.6261.52)
  * [Chrome release calendar](https://chromiumdash.appspot.com/schedule)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2024-04-16 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2024-04-16 UTC."],[],[]] 
