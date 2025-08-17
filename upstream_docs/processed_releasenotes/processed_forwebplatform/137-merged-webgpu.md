# Chrome 137 Release Notes

**Stable release date:** May 27th, 2025

Unless otherwise noted, the following changes apply to Chrome 137 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. Want just the highlights? Check out [New in Chrome 137](https://developer.chrome.com/blog/new-in-chrome-137).

## CSS and UI

### CSS if() function

The CSS `if()` function provides a concise way to express conditional values. It accepts a series of condition-value pairs, delimited by semicolons. The function evaluates each condition sequentially and returns the value associated with the first true condition. If none of the conditions evaluate to true, the function returns an empty token stream. This lets you express complex conditional logic in a simple and concise way.

**Example:**
```css
div {
  color: var(--color);
  background-color: if(style(--color: white): black; else: white);
}
.dark { --color: black; }
.light { --color: white; }
```

```html
<div class="dark">dark</div>
<div class="light">light</div>
```

**References:** [Tracking bug #346977961](https://bugs.chromium.org/p/chromium/issues/detail?id=346977961) | [ChromeStatus.com entry](https://chromestatus.com/feature/5084924504915968) | [Spec](https://www.w3.org/TR/css-values-5/#if-function)

### CSS reading-flow, reading-order properties

The `reading-flow` CSS property controls the order in which elements in a flex, grid, or block layout are exposed to accessibility tools and focused using tab keyboard focus navigation. The `reading-order` CSS property allows authors to manually-override the order within a reading flow container. It is an integer with default value of 0. Learn more about these properties in [Use CSS reading-flow for logical sequential focus navigation](https://developer.chrome.com/blog/reading-flow), and try out some examples.

**References:** [Tracking bug #40932006](https://bugs.chromium.org/p/chromium/issues/detail?id=40932006) | [ChromeStatus.com entry](https://chromestatus.com/feature/5061928169472000) | [Spec](https://drafts.csswg.org/css-display-4/#reading-flow)

### Ignore letter spacing in cursive scripts

This feature adds logic to ignore the letter-spacing setting for cursive scripts as specified by the developer, in line with the specification, to ensure that letter spacing does not disrupt word structure and aims to produce better user experience for users relying on cursive scripts. With this feature, Chrome ensures that cursive scripts will be readable and properly spaced, even if the fonts don't have advanced typographic features. The scripts this applies to in Chromium are Arabic, Hanifi Rohingya, Mandaic, Mongolian, N'Ko, Phags Pa, and Syriac as these scripts are considered cursive as per the specification.

**References:** [Tracking bug #40618336](https://bugs.chromium.org/p/chromium/issues/detail?id=40618336) | [ChromeStatus.com entry](https://chromestatus.com/feature/5088256061988864) | [Spec](https://www.w3.org/TR/css-text-3/#letter-spacing-property)

### Selection API getComposedRanges and direction

This feature ships two new API methods for the Selection API:
- `Selection.direction` which returns the selection's direction as either `none`, `forward`, or `backward`
- `Selection.getComposedRanges()` which returns a list of 0 or 1 composed StaticRange

A composed StaticRange is allowed to cross shadow boundaries, which a normal Range cannot.

**Example:**
```javascript
const range = getSelection().getComposedRanges({shadowRoots: [root]});
```

If the selection crosses a shadow root boundary that isn't provided in the shadowRoots list, then the endpoints of the StaticRange will be rescoped to be outside that tree. This makes sure Chrome doesn't expose unknown shadow trees.

**References:** [Tracking bug #40286116](https://bugs.chromium.org/p/chromium/issues/detail?id=40286116) | [ChromeStatus.com entry](https://chromestatus.com/feature/5069063455711232) | [Spec](https://w3c.github.io/selection-api/#dom-selection-getcomposedranges)

### Support offset-path: shape()

Support `offset-path: shape()`, to allow using responsive shapes to set the animation path.

**References:** [Tracking bug #389713717](https://bugs.chromium.org/p/chromium/issues/detail?id=389713717) | [ChromeStatus.com entry](https://chromestatus.com/feature/5062848242884608) | [Spec](https://www.w3.org/TR/css-shapes-2/#shape-function)

### Support the transform attribute on SVGSVGElement

This feature enables the application of transformation properties—such as scaling, rotation, translation, and skewing—directly to the `<svg>` root element using its transform attribute. This enhancement lets you manipulate the entire SVG coordinate system or its contents as a whole, providing greater flexibility in creating dynamic, responsive, and interactive vector graphics. By supporting this attribute, the `<svg>` element can be transformed without requiring additional wrapper elements or complex CSS workarounds, streamlining the process of building scalable and animated web graphics.

**References:** [Tracking bug #40313130](https://bugs.chromium.org/p/chromium/issues/detail?id=40313130) | [ChromeStatus.com entry](https://chromestatus.com/feature/5070863647424512) | [Spec](https://www.w3.org/TR/SVG2/types.html#InterfaceSVGTransformable)

### System accent color for accent-color property

This lets you use the operating system's accent color for form elements. By using the `accent-color` CSS property, you can ensure that form elements such as checkboxes, radio buttons, and progress bars automatically adopt the accent color defined by the user's operating system. This has been supported on macOS since 2021, and is now supported on Windows and ChromeOS.

**References:** [Tracking bug #40764875](https://bugs.chromium.org/p/chromium/issues/detail?id=40764875) | [ChromeStatus.com entry](https://chromestatus.com/feature/5088516877221888) | [Spec](https://www.w3.org/TR/css-ui-4/#accent-color)

### Allow <use> to reference an external document's root element by omitting the fragment

This feature streamlines the SVG `<use>` element by loosening referencing requirements. Before Chrome 137, you had to explicitly reference fragments within the SVG document. If no fragment ID is given `<use>` won't be able to resolve the target and nothing will be rendered or referred.

**Example:**
A `<use>` element referencing an external file with fragment identifier:
```html
<svg>
  <use xlink:href="myshape.svg#icon"></use>
</svg>
```

In this example, `#icon` is the fragment identifier pointing to an element with `id="icon"` within `myshape.svg`.

Without a fragment identifier:
```html
<svg>
  <use xlink:href="myshape.svg"></use>
</svg>
```

With this feature, omitting fragments or just giving the external svg file name will automatically reference the root element, eliminating the need for you to alter the referenced document just to assign an ID to the root. This enhancement simplifies this manual editing process and improves efficiency.

**References:** [Tracking bug #40362369](https://bugs.chromium.org/p/chromium/issues/detail?id=40362369) | [ChromeStatus.com entry](https://chromestatus.com/feature/5078775255900160) | [Spec](https://www.w3.org/TR/SVG2/struct.html#UseElement)

### Canvas floating point color types

Introduces the ability to use floating point pixel formats (as opposed to 8-bit fixed point) with `CanvasRenderingContext2D`, `OffscreenCanvasRenderingContext2D`, and `ImageData`. This is necessary for high precision applications (for example, medical visualization), high dynamic range content, and linear working color spaces.

**References:** [Tracking bug #40245602](https://bugs.chromium.org/p/chromium/issues/detail?id=40245602) | [ChromeStatus.com entry](https://chromestatus.com/feature/5053734768197632) | [Spec](https://html.spec.whatwg.org/multipage/canvas.html#the-2d-rendering-context)

### view-transition-name: match-element

The `match-element` value generates a unique ID based on the element's identity and renames the same for this element. This is used in Single Page App cases where the element is being moved around and you want to animate it with a view transition.

**References:** [Tracking bug #365997248](https://bugs.chromium.org/p/chromium/issues/detail?id=365997248) | [ChromeStatus.com entry](https://chromestatus.com/feature/5092488609931264) | [Spec](https://drafts.csswg.org/css-view-transitions-2/#view-transition-name-prop)

## Payments

### Align error type thrown for payment WebAuthn credential creation: SecurityError becomes NotAllowedError

Correct the error type thrown during WebAuthn credential creation for payment credentials. Due to a historic specification mismatch, creating a payment credential in a cross-origin iframe without a user activation would throw a `SecurityError` instead of a `NotAllowedError`, which is what is thrown for non-payment credentials. This is a breaking change, albeit a niche one. Code that previously detected the type of error thrown (for example, `e instanceof SecurityError`) is affected. Code that just generally handles errors during credential creation (for example, `catch (e)`) will continue to function correctly.

**References:** [Tracking bug #41484826](https://bugs.chromium.org/p/chromium/issues/detail?id=41484826) | [ChromeStatus.com entry](https://chromestatus.com/feature/5096945194598400) | [Spec](https://w3c.github.io/webauthn/#sctn-creating-a-credential)

## Web APIs

### Blob URL Partitioning: Fetching/Navigation

As a continuation of Storage Partitioning, Chrome has implemented partitioning of Blob URL access by Storage Key (top-level site, frame origin, and the has-cross-site-ancestor boolean), with the exception of top-level navigations which will remain partitioned only by frame origin. This behavior is similar to what's currently implemented by both Firefox and Safari, and aligns Blob URL usage with the partitioning scheme used by other storage APIs as part of Storage Partitioning. In addition, Chrome now enforces noopener on renderer-initiated top-level navigations to Blob URLs where the corresponding site is cross-site to the top-level site performing the navigation. This aligns Chrome with similar behavior in Safari, and the relevant specs have been updated to reflect these changes.

**Note:** This change can be temporarily reverted by setting the `PartitionedBlobURLUsage` policy. The policy will be deprecated when the other storage partitioning related enterprise policies are deprecated.

**References:** [Tracking bug #40057646](https://bugs.chromium.org/p/chromium/issues/detail?id=40057646) | [ChromeStatus.com entry](https://chromestatus.com/feature/5037311976488960)

### Call stacks in crash reports from unresponsive web pages

This feature captures the JavaScript call stack when a web page becomes unresponsive due to JavaScript code running an infinite loop or other very long computation. This helps developers to identify the cause of the unresponsiveness and fix it more easily. The JavaScript call stack is included in the crash reporting API when the reason is unresponsive.

**References:** [Tracking bug #1445539](https://bugs.chromium.org/p/chromium/issues/detail?id=1445539) | [ChromeStatus.com entry](https://chromestatus.com/feature/5045134925406208) | [Spec](https://w3c.github.io/reporting/#crash-report)

### Document-Isolation-Policy

Document-Isolation-Policy lets a document enable crossOriginIsolation for itself, without having to deploy COOP or COEP, and regardless of the crossOriginIsolation status of the page. The policy is backed by process isolation. Additionally, the document non-CORS cross-origin subresources will either be loaded without credentials or will need to have a CORP header.

**References:** [Tracking bug #333029146](https://bugs.chromium.org/p/chromium/issues/detail?id=333029146) | [ChromeStatus.com entry](https://chromestatus.com/feature/5048940296830976) | [Spec](https://wicg.github.io/document-isolation-policy/)

### Ed25519 in web cryptography

This feature adds support for Curve25519 algorithms in the Web Cryptography API, namely the signature algorithm Ed25519.

**References:** [Tracking bug #1370697](https://bugs.chromium.org/p/chromium/issues/detail?id=1370697) | [ChromeStatus.com entry](https://chromestatus.com/feature/5056122982457344) | [Spec](https://www.rfc-editor.org/rfc/rfc8032.html)

### HSTS tracking prevention

Mitigates user tracking by third-parties using the HSTS cache. This feature only allows HSTS upgrades for top-level navigations and blocks HSTS upgrades for sub-resource requests. Doing so makes it infeasible for third-party sites to use the HSTS cache in order to track users across the web.

**References:** [Tracking bug #40725781](https://bugs.chromium.org/p/chromium/issues/detail?id=40725781) | [ChromeStatus.com entry](https://chromestatus.com/feature/5065878464307200)

## WebAssembly

### JavaScript promise integration

JavaScript Promise Integration (JSPI) is an API that allows WebAssembly applications to integrate with JavaScript Promises. It allows a WebAssembly program to act as the generator of a Promise, and it allows the WebAssembly program to interact with Promise-bearing APIs. In particular, when an application uses JSPI to call a Promise-bearing (JavaScript) API, the WebAssembly code is suspended; and the original caller to the WebAssembly program is given a Promise that will be fulfilled when the WebAssembly program finally completes.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5059306691878912) | [Spec](https://github.com/WebAssembly/js-promise-integration)

### Branch Hints

Improves the performance of compiled WebAssembly code by informing the engine that a particular branch instruction is very likely to take a specific path. This allows the engine to make better decisions for code layout (improving instruction cache hits) and register allocation.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5089072889290752) | [Spec](https://github.com/WebAssembly/branch-hinting)

## WebGPU

### GPUTextureView for externalTexture binding

A `GPUTextureView` is now allowed to be used for an `externalTexture` binding when creating a `GPUBindGroup`.

**References:** [Tracking bug #398752857](https://bugs.chromium.org/p/chromium/issues/detail?id=398752857) | [ChromeStatus.com entry](https://chromestatus.com/feature/5107071463104512) | [Spec](https://gpuweb.github.io/gpuweb/#gpubindgroup)

### copyBufferToBuffer overload

The `GPUCommandEncoder` `copyBufferToBuffer()` method now includes a simpler way to copy entire buffers using a new overload with optional offsets and size parameters.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5103419089608704) | [Spec](https://gpuweb.github.io/gpuweb/#dom-gpucommandencoder-copybuffertobuffer)

## Enterprise

### IP address logging and reporting

Chrome Enterprise is enhancing security monitoring and incident response capabilities by collecting and reporting local and remote IP addresses and sending those IP addresses to the Security Investigation Logs (SIT). In addition, Chrome Enterprise will allow admins to optionally send the IP addresses to first-party and third-party SIEM providers through the Chrome Enterprise Reporting connector. This is available for Chrome Enterprise Core customers.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5110849951309824)

## WebGPU

### Key Updates

#### 1. Texture View for External Texture Binding
- Now allows a compatible `GPUTextureView` to be used in place of a `GPUExternalTexture` binding
- Simplifies shader logic in video effects pipelines
- Reduces need for dynamically compiling shaders

```javascript
const bindGroup = myDevice.createBindGroup({
  layout: pipeline.getBindGroupLayout(0),
  entries: [
    { binding: 0, resource: texture.createView() }, // Texture view for external texture
    { binding: 1, resource: { buffer: myBuffer } },
  ],
});
```

#### 2. Buffer Copy Simplification
- New method overload allows omitting offsets and size parameters in `copyBufferToBuffer()`
- Simplifies copying entire buffers

```javascript
// Copy entire buffer without specifying offsets
myCommandEncoder.copyBufferToBuffer(srcBuffer, dstBuffer);
```

#### 3. WGSL Workgroup Uniform Load
- New `workgroupUniformLoad(ptr)` overload for atomic loads
- Atomically loads value for all workgroup invocations

```wgsl
@compute @workgroup_size(1, 1)
fn main(@builtin(local_invocation_index) lid: u32) {
  if (lid == 0) {
    atomicStore(&(wgvar), 42u);
  }
  buffer[lid] = workgroupUniformLoad(&wgvar);
}
```

#### 4. GPUAdapterInfo Power Preference
- Non-standard `powerPreference` attribute available with "WebGPU Developer Features" flag
- Returns `"low-power"` or `"high-performance"`

```javascript
function checkPowerPreferenceForGpuDevice(device) {
  const powerPreference = device.adapterInfo.powerPreference;
  // Adjust settings based on GPU power preference
}
```

#### 5. Removed Compatibility Mode Attribute
- Experimental `compatibilityMode` attribute removed
- Replaced by standardized approach for compatibility

## Origin trials

### Full frame rate render blocking attribute

Adds a new render blocking token `full-frame-rate` to the blocking attributes. When the renderer is blocked with the `full-frame-rate` token, the renderer will work at a lower frame rate so as to reserve more resources for loading.

**References:** [Tracking bug #397832388](https://bugs.chromium.org/p/chromium/issues/detail?id=397832388) | [ChromeStatus.com entry](https://chromestatus.com/feature/5109023781429248)

### Pause media playback on not-rendered iframes

Adds a `media-playback-while-not-rendered` permission policy to allow embedder websites to pause media playback of embedded iframes which aren't rendered—that is, have their display property set to `none`. This should allow developers to build more user-friendly experiences and to also improve the performance by letting the browser handle the playback of content that is not visible to users.

**References:** [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #351354996](https://bugs.chromium.org/p/chromium/issues/detail?id=351354996) | [ChromeStatus.com entry](https://chromestatus.com/feature/5082854470868992)

### Rewriter API

The Rewriter API transforms and rephrases input text in requested ways, backed by an on-device AI language model. Developers may use this API to remove redundancies within a text in order to fit into a word limit, rephrase messages to suit the intended audience or to be more constructive if a message is found to use toxic language, rephrasing a post or article to use simpler words and concepts and more.

**References:** [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #358214322](https://bugs.chromium.org/p/chromium/issues/detail?id=358214322) | [ChromeStatus.com entry](https://chromestatus.com/feature/5089854436556800) | [Spec](https://wicg.github.io/rewriter-api/)

### Writer API

The Writer API can be used for writing new material given a writing task prompt, backed by an on-device AI language model. Developers will be able to use this API to generate textual explanations of structured data, composing a post about a product based on reviews or product description, expanding on pro and con lists into full views and more.

**References:** [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #357967382](https://bugs.chromium.org/p/chromium/issues/detail?id=357967382) | [ChromeStatus.com entry](https://chromestatus.com/feature/5089855470993408) | [Spec](https://wicg.github.io/writer-api/)

---

*Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.*

*Last updated 2025-05-27 UTC.*
