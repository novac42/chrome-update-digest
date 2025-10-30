---
layout: default
title: chrome-142-en
---

## Area Summary

Chrome 142 continues to expand WebGPU and graphics platform capabilities, focusing on richer shader inputs (primitive index), broader texture format support (tier1/tier2), and runtime/library improvements (Dawn). The most impactful changes for developers are the new WGSL built-in `primitive_index` for per-primitive shading and extended texture formats that reduce porting friction for existing GPU assets. Together these updates advance the web platform by closing gaps with native graphics APIs, improving visual fidelity and compatibility, and simplifying cross-platform GPU development. These updates matter because they reduce workarounds for advanced rendering and make WebGPU a more viable target for high-performance graphics and compute on the web.

## Detailed Updates

The items below expand on the summary above and list each Graphics and WebGPU-related feature in Chrome 142 with concise technical notes, developer use cases, and references.

### Graphics

#### What's New
This entry groups the WebGPU highlights and detailed release notes for graphics in Chrome 142.

#### Technical Details
Summary grouping that points to the WebGPU release coverage in Chrome 142.

#### Use Cases
General pointer for developers to review WebGPU changes in this release.

#### References
- [Chrome for Developers](https://developer.chrome.com/)
- [Blog](https://developer.chrome.com/blog)

### WebGPU: `primitive_index` feature

#### What's New
WebGPU adds an optional capability exposing a WGSL built-in `primitive_index` to fragment shaders, providing a per-primitive index similar to `vertex_index` and `instance_index`.

#### Technical Details
The capability is optional and enabled on supported hardware; `primitive_index` increments per primitive (point/line/triangle) and is available inside fragment stage shaders.

#### Use Cases
Primitive-level picking, procedural patterning per-primitive, and debugging/visualization techniques where per-primitive identity is required.

#### References
- [Tracking bug #342172182](https://issues.chromium.org/issues/342172182)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6467722716250112)
- [Spec](https://gpuweb.github.io/gpuweb/#dom-gpufeaturename-primitive-index)

### WebGPU: Texture formats tier1 and tier2

#### What's New
Chrome 142 extends GPU texture format support via the texture format tiering model, enabling features like render attachment, blending, multisampling, resolve, and storage_binding for more formats.

#### Technical Details
Tiered texture format capabilities are defined by the WebGPU spec; tier1/tier2 expose additional format capabilities to improve parity with native APIs.

#### Use Cases
Porting existing assets and engines that rely on more advanced texture formats and operations without rewriting shaders or texture pipelines.

#### References
- [Tracking bug #445725447](https://issues.chromium.org/issues/445725447)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5116926821007360)
- [Spec](https://www.w3.org/TR/webgpu/#texture-formats-tier1)

### Detailed WebGPU Updates

#### What's New
Pointer to the Chrome developer blog coverage of what's new in WebGPU for this release.

#### Technical Details
Aggregated release notes and examples on developer.chrome.com and the Chrome blog.

#### Use Cases
Developers should consult the linked resources for migration notes, samples, and full release details.

#### References
- [Chrome for Developers](https://developer.chrome.com/)
- [Blog](https://developer.chrome.com/blog)

### Texture format support capabilities extended

#### What's New
The `texture-formats-tier1` and `texture-formats-tier2` features let WebGPU support additional texture formats (e.g., 16-bit channels) and capabilities so existing content can be ported more easily.

#### Technical Details
These GPU features expose formats like `r16unorm`, `r16snorm`, `rg16unorm`, `rg16snorm`, and higher-precision RGBA variants with support for rendering and storage operations as specified in the GPUWeb spec.

#### Use Cases
Game engines, image processing, and visual effects pipelines that depend on half-precision formats or specific render/resolve behavior can now migrate to WebGPU with fewer changes.

#### References
- ["texture-formats-tier1"](https://gpuweb.github.io/gpuweb/#texture-formats-tier1)
- ["texture-formats-tier2"](https://gpuweb.github.io/gpuweb/#texture-formats-tier2)
- [chromestatus entry](https://chromestatus.com/feature/5116926821007360)

### Primitive index in WGSL

#### What's New
The WGSL built-in `primitive_index` uniquely identifies the primitive processed by the fragment shader; it starts at 0 and increments per primitive.

#### Technical Details
Defined in WGSL built-in values, `primitive_index` is provided per-fragment and compatible with applications that require per-primitive metadata in shading.

#### Use Cases
Primitive picking, custom rasterization effects, or shader-based object identification where vertex/instance indices are insufficient.

#### References
- [`primitive_index`](https://gpuweb.github.io/gpuweb/wgsl/#built-in-values-primitive_index)
- [Primitive Picking sample](https://webgpu.github.io/webgpu-samples/?sample=primitivePicking)
- [chromestatus entry](https://chromestatus.com/feature/6467722716250112)

### Dawn updates

#### What's New
Build and runtime updates in Dawn: the default for `DAWN_BUILD_MONOLITHIC_LIBRARY` changed to `STATIC`, and PresentMode handling improved, among other commits.

#### Technical Details
CMake default changed so `libwebgpu*` files are generated by default; runtime now properly handles `wgpu::PresentMode::Undefined` defaulting.

#### Use Cases
Project build systems and downstream embedders of Dawn should review the changed default and adjust CMake or linking expectations accordingly.

#### References
- [issue 441410668](https://issues.chromium.org/issues/441410668)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7390..chromium/7444?n=1000)

### FedCM—Support showing third-party iframe origins in the UI

#### What's New
FedCM UI can now show third-party iframe origins when the iframe is actually third-party, improving transparency.

#### Technical Details
Previously the FedCM UI always showed the top-level site; this change surfaces the iframe origin as appropriate per the updated UX decision.

#### Use Cases
Auth and federated identity flows embedded in third-party iframes will present clearer origin information to users, aiding security and developer UX.

#### References
- [Tracking bug #390581529](https://issues.chromium.org/issues/390581529)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5176474637959168)
- [Spec](https://github.com/w3c-fedid/FedCM/pull/774)

### Stricter `*+json` MIME token validation for JSON modules

#### What's New
Chrome 142 rejects JSON module script responses whose MIME type type or subtype contain non-HTTP token code points when matched with `*+json`, aligning with MIME Sniffing spec and Interop2025.

#### Technical Details
Validation follows the MIME Sniffing specification parsing rules and tightens acceptance criteria for `*+json` matches.

#### Use Cases
Developers delivering JSON modules should ensure MIME types are well-formed tokens (no spaces or invalid characters) to avoid module load failures.

#### References
- [Tracking bug #440128360](https://issues.chromium.org/issues/440128360)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5182756304846848)
- [Spec](https://mimesniff.spec.whatwg.org/#parse-a-mime-type)

### Web Speech API contextual biasing

#### What's New
Sites can provide and update a phrase list to bias the Web Speech API's recognition models toward specified phrases.

#### Technical Details
The API exposes recognition phrase lists and allows updates that influence the speech recognition model's preferences per the spec.

#### Use Cases
Improve recognition accuracy in domain-specific apps (voice UIs, dictation in specialized vocabularies) by biasing toward expected phrases.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5225615177023488)
- [Spec](https://webaudio.github.io/web-speech-api/#speechreco-phraselist)

### Media session: add reason to `enterpictureinpicture` action details

#### What's New
Adds `enterPictureInPictureReason` to `MediaSessionActionDetails` so developers can distinguish user-initiated vs. programmatic PiP entry.

#### Technical Details
The Media Session API's action details for `enterpictureinpicture` now include a reason field as specified in the linked PR.

#### Use Cases
Adaptive UI behavior based on whether PiP was entered by a user action or by script (analytics, consent flows, or UX adjustments).

#### References
- [Tracking bug #446738067](https://issues.chromium.org/issues/446738067)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6415506970116096)
- [Spec](https://github.com/w3c/mediasession/pull/362)

### Local network access restrictions

#### What's New
Chrome 142 gates requests to local network addresses behind a permission prompt to restrict cross-origin access to local IPs and loopback.

#### Technical Details
Requests from public websites to local IPs/loopback, or from local sites to loopback, will trigger a permission prompt per the WICG local-network-access proposal.

#### Use Cases
Improves security posture for web apps interacting with LAN devices; developers of LAN management tools must handle permission prompts and failure modes.

#### References
- [Tracking bug #394009026](https://issues.chromium.org/issues/394009026)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5152728072060928)
- [Spec](https://wicg.github.io/local-network-access)

### Interoperable pointerrawupdate events exposed only in secure contexts

#### What's New
`pointerrawupdate` event and global listeners are restricted to secure contexts to match the PointerEvents spec and other browsers.

#### Technical Details
Chrome now hides event firing and global listener availability in insecure contexts, aligning with the spec behavior from 2020.

#### Use Cases
Developers relying on raw pointer updates should ensure pages are served over secure contexts; improves cross-browser interoperability for low-level pointer input.

#### References
- [Tracking bug #404479704](https://issues.chromium.org/issues/404479704)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5151468306956288)
- [Spec](https://w3c.github.io/pointerevents/#the-pointerrawupdate-event)

### Sticky user activation across same-origin renderer-initiated navigations

#### What's New
Preserves sticky user activation state when navigating to another same-origin page, enabling behaviors that depend on user activation across navigations.

#### Technical Details
Sticky activation state is retained for same-origin renderer-initiated navigations per the linked spec change.

#### Use Cases
Useful for single-origin apps that navigate internally and need to preserve user activation (e.g., auto-focusing inputs that invoke virtual keyboards).

#### References
- [Tracking bug #433729626](https://issues.chromium.org/issues/433729626)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5078337520926720)
- [Spec](https://github.com/whatwg/html/pull/11454)

### Device Bound Session Credentials

#### What's New
Introduces a mechanism for servers to bind sessions to a single device with periodic browser-renewed proofs involving a private key.

#### Technical Details
The browser performs periodic renewals with proof of possession of a private key; the feature has an Origin Trial and follows the WebAppSec DBSC spec.

#### Use Cases
Enhances session security for sensitive applications by making stolen session tokens less usable on other devices; relevant for banking and enterprise apps.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials#/view_trial/3357996472158126081)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5140168270413824)
- [Spec](https://w3c.github.io/webappsec-dbsc)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)

Saved file: digest_markdown/webplatform/Graphics and WebGPU/chrome-142-stable-en.md
