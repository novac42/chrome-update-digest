## Web APIs

### Web App Manifest: specify update eligibility, icon URLs are `Cache-Control: immutable`

Specify an update eligibility algorithm in the manifest spec. This makes the update process more deterministic and predictable, giving developers more control over whether (and when) updates should apply to existing installations, and allowing removal of the 'update check throttle' that user agents currently need to implement to avoid wasting network resources.

### WebXR Depth Sensing Performance Improvements

Exposes several new mechanisms to customize the behavior of the depth sensing feature within a WebXR session, with the goal of improving the performance of the generation or consumption of the depth buffer. The key mechanisms exposed are: the ability to request the raw or smooth depth buffer, the ability to request that the runtime stop or resume providing the depth buffer, and the ability to expose a depth buffer that does not align with the user's view exactly, so that the user agent does not need to perform unnecessary re-projections every frame.

### Allow more characters in JavaScript DOM APIs

The HTML parser has always (or for a long time) allowed elements and attributes to have a wide variety of valid characters and names, but the JavaScript DOM APIs that create the same elements and attributes are more strict and don't match the parser. This change relaxes the validation of the JavaScript DOM APIs to match the HTML parser.

### `request-close` invoker command

Dialog elements can be closed through a variety of mechanisms, sometimes developers want to have the ability to prevent closure. To achieve this dialogs fire a cancel event. Originally this was only fired via a close request (for example, `Esc` key press), recently a `requestClose()` JS function was added which also fires the cancel event. The `request-close` command brings that new ability to the declarative invoker commands API.

### WebGPU: 3D texture support for BC and ASTC compressed formats

The `texture-compression-bc-sliced-3d` and `texture-compression-astc-sliced-3d` WebGPU features add respectively 3D texture support for BC and ASTC compressed formats.

### Secure Payment Confirmation: Browser Bound Keys

Adds an additional cryptographic signature over Secure Payment Confirmation assertions and credential creation. The corresponding private key is not synced across devices. This helps web developers meet requirements for device binding for payment transactions.

### Secure Payment Confirmation: UX Refresh

Updates the UX elements for the SPC dialog on Android Chrome. Other than just UX presentation the following are being added:

  * Lets merchants provide an optional list of payment entity logos related to the payment that will be displayed.
  * Returning different output states back to the merchant depending on whether the user wants to continue the transaction without SPC or to cancel the transaction.
  * Adds a new payment detail label field to the payment instrument so the text is presented across two lines.

### WebGPU `core-features-and-limits`

The `core-features-and-limits` feature signifies that a WebGPU adapter and device support the core features and limits of the spec.

### Scroll anchoring priority candidate fix

Currently, the scroll anchoring algorithm selects priority candidates when they are available as anchor targets. The priority candidates are currently a focused editable element and find-in-page highlights. This can cause suboptimal user experience if there is a large focused contenteditable element that has content changed offscreen (the cursor ends up being shifted as a consequence). This fix changes the algorithm: instead of selecting the priority candidate as the anchor, use the candidate as the scope or root of the regular anchor selection algorithm that selects the deepest onscreen element as the anchor.

### Support the `async` attribute for SVG `<script>` elements

The `SVGScriptElement` interface in SVG 2.0 introduces the `async` attribute, similar to the `HTMLScriptElement`. This attribute allows scripts to be executed asynchronously, improving the performance and responsiveness of web applications that use SVG.

### On-device Web Speech API

This feature adds on-device speech recognition support to the Web Speech API, allowing websites to ensure that neither audio nor transcribed speech are sent to a third-party service for processing. Websites can query the availability of on-device speech recognition for specific languages, prompt users to install the necessary resources for on-device speech recognition, and choose between on-device or cloud-based speech recognition as needed.

### Clear `window.name` for cross-site navigations that switch browsing context group

The value of the `window.name` property is currently preserved throughout the lifetime of a tab, even with navigation that switches browsing context groups, which can leak information and potentially be used as a tracking vector. Clearing the `window.name` property addresses this issue. This should be a low risk change since looking up a browsing context by name already doesn’t work if it's in another browsing context group, so the name isn't actually useful.

Enterprise Policy: `ClearWindowNameCrossSiteBrowsing` (will stop working in Chrome 142).

### Web app scope extensions

Adds a [`"scope_extensions"`](/docs/capabilities/scope-extensions) web app manifest field that enables web apps to extend their scope to other origins.

This allows sites that control multiple subdomains and top level domains to be presented as a single web app. Requires listed origins to confirm association with the web app using a `.well-known/web-app-origin-association` configuration file.

### Specification-compliant JSON MIME type detection

Chromium now recognizes all valid JSON MIME types as defined by the WHATWG mimesniff specification. This includes any MIME type whose subtype ends with `+json`, in addition to the traditional `application/json` and `text/json`. This change ensures that web APIs and features relying on JSON detection behave consistently with the web platform standard and other browsers. A key motivation for this change is to fix JSON module import behavior, where previously valid JSON MIME types like `text/html+json` and `image/svg+json` would fail to load as modules.

### Private Aggregation API: aggregate error reporting

There are a range of error conditions that can be hit when using the Private Aggregation API. For example, the privacy budget could run out, preventing any further histogram contributions. This feature allows developers to register histogram contributions that should only be sent if a particular type of error occurs. This feature supports measuring the frequency of the error conditions and to split these measurements on relevant developer-specified dimensions (e.g. version of deployed code). As the errors themselves may be cross-site information, we cannot simply expose them to the page for users without third-party cookies. Instead, this feature reuses the existing aggregate, noised reporting pipelines through the Aggregation Service.

### Crash Reporting API: Specify crash-reporting to receive only crash reports

This feature ensures developers receive only crash reports by specifying the endpoint named `crash-reporting`. By default, crash reports are delivered to the `default` endpoint which receives many other kinds of reports besides crash reports. Developers can supply a separate URL to the well-known endpoint named `crash-reporting`, to direct crash reports there, instead of the `default` endpoint.

### Reduce fingerprinting in `Accept-Language` header information

Reduces the amount of information the `Accept-Language` header value string exposes in HTTP requests and in `navigator.languages`. Instead of sending a full list of the user's preferred languages on every HTTP request with the `Accept-Language` header. We now send the user’s most preferred language in the `Accept-Language` header. To minimize compatibility risks, the initial launch reduces the information in the HTTP header, we’ll reduce the related `navigator.languages` JavaScript getters in the future.

### Fire error event instead of throwing for CSP blocked worker

When blocked by Content Security Policy (CSP), Chrome currently throws a `SecurityError` from the constructor of Worker and SharedWorker. The specification requires CSP to be checked as part of fetch and fires error events asynchronously instead of throwing an exception when a script runs `new Worker(url)` or `new SharedWorker(url)`. This change makes Chrome specification conformant: not throwing during constructor and firing error events asynchronously.

### Audio Level for RTC Encoded Frames

Exposes to the web the audio level of an encoded frame transmitted with `RTCPeerConnection` and exposed using WebRTC Encoded Transform.
