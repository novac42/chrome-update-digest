---
layout: default
title: graphics-webgpu-en
---

## Area Summary

Chrome 133 continues to expand and stabilize the WebGPU surface area: new vertex formats (including 1-component types and unorm8x4-bgra), WGSL alignment and discard-related changes for correctness and performance, improved handling of external textures and image orientations, and device/limit ergonomics. The release also advances compatibility and API hygiene via deprecations, experimental feature cleanup, and Dawn implementation updates. For developers this means finer-grained vertex input options, fewer surprising runtime limit errors, better external-media-to-texture fidelity, and measurable shader performance improvements. These updates collectively make advanced GPU features more predictable and easier to integrate into web apps and engines.

## Detailed Updates

The bullets below expand on the summary above with individual feature notes drawn from the Chrome 133 release data.

### Rendering and graphics

#### What's New
This section aggregates both Chrome WebGPU highlights and detailed WebGPU release notes.

#### Technical Details
Noted as the umbrella for WebGPU changes in this release.

#### Use Cases
Serves as the entry point for developers tracking WebGPU and rendering improvements.

#### References
None provided

### WebGPU: 1-component vertex formats (and unorm8x4-bgra)

#### What's New
Adds additional vertex formats that were omitted from the initial WebGPU release; 1-component vertex formats allow requesting only the needed data rather than a minimum of two components.

#### Technical Details
Addresses earlier omissions caused by platform support gaps (e.g., old macOS). See tracking links for progress and status.

#### Use Cases
Reduces memory and bandwidth when vertex attributes are single-value (e.g., scalar weights, offsets).

#### References
- [Tracking bug #376924407](https://issues.chromium.org/issues/376924407)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4609840973086720)

### Detailed WebGPU Updates

#### What's New
Reference pointer to the Chrome developer blog posts and WebGPU changelog for this release.

#### Technical Details
Source listing pointing to developer.chrome.com and the developer blog.

#### Use Cases
Use these resources for in-depth release notes and examples.

#### References
- [Chrome for Developers](https://developer.chrome.com/)
- [Blog](https://developer.chrome.com/blog)

### Additional unorm8x4-bgra and 1-component vertex formats

#### What's New
Adds "unorm8x4-bgra" and multiple 1-component formats: "uint8", "sint8", "unorm8", "snorm8", "uint16", "sint16", "unorm16", "snorm16", and "float16".

#### Technical Details
The unorm8x4-bgra format simplifies loading BGRA-encoded data; the listed 1-component types expand attribute granularity.

#### Use Cases
Better interop with BGRA sources and more compact vertex streams where single-component attributes are sufficient.

#### References
- [chromestatus entry](https://chromestatus.com/feature/4609840973086720)
- [issue 376924407](https://issues.chromium.org/issues/376924407)

### Allow unknown limits to be requested with undefined value

#### What's New
You can now request unknown GPU adapter limits by specifying `undefined` when requesting a GPU device.

#### Technical Details
This makes the WebGPU device request less brittle against evolving spec limits where `adapter.limits.someLimit` may be absent.

#### Use Cases
Safer device requests in applications that query adapter limits conditionally and want forward compatibility.

#### References
- [spec PR 4781](https://github.com/gpuweb/gpuweb/pull/4781)

### WGSL alignment rules changes

#### What's New
`@align(n)` on struct members is now required to divide RequiredAlignOf for all structs; too-small alignment values are no longer allowed.

#### Technical Details
This enforcement simplifies WGSL usage and removes certain classes of incorrect alignment annotations.

#### Use Cases
Improves portability and correctness of WGSL shaders across implementations.

#### References
- [`RequiredAlignOf`](https://gpuweb.github.io/gpuweb/wgsl/#requiredalignof)
- [spec PR](https://github.com/gpuweb/gpuweb/pull/4978)

### WGSL performance gains with discard

#### What's New
The WGSL discard statement uses platform-provided semantics to demote to a helper invocation when available, addressing a large performance drop seen in SSR.

#### Technical Details
Adopts platform semantics for discard/demote to avoid pathological performance regressions.

#### Use Cases
Restores expected performance for shaders that use discard, especially in complex screen-space effects.

#### References
- [discard statement](https://gpuweb.github.io/gpuweb/wgsl/#discard-statement)
- [issue 372714384](https://issues.chromium.org/372714384)

### Use VideoFrame displaySize for external textures

#### What's New
When importing a VideoFrame as a GPUExternalTexture, Chrome now uses the frame's `displayWidth` and `displayHeight` as the apparent size.

#### Technical Details
Previously the visible size was used, which caused issues when using `textureLoad()` on a GPUExternalTexture.

#### Use Cases
Improves correctness when sampling or loading from external video textures with differing coded and display sizes.

#### References
- [issue 377574981](https://issues.chromium.org/issues/377574981)

### Handle images with non-default orientations using copyExternalImageToTexture

#### What's New
`copyExternalImageToTexture()` now correctly handles images with non-default orientations (e.g., ImageBitmap with `imageOrientation: "from-image"`).

#### Technical Details
Fixes prior incorrect handling when the source had orientation metadata applied.

#### Use Cases
Accurate copies from canvases or images with orientation metadata into GPU textures without manual pre-rotation.

#### References
- ["`\"from-image\"`"](https://developer.mozilla.org/docs/Web/API/Window/createImageBitmap#from-image)
- [issue 384858956](https://issues.chromium.org/issues/384858956)

### Improving developer experience

#### What's New
Error messages around adapter limits have been expanded with hints that tell developers when they must explicitly request higher limits.

#### Technical Details
Aims to reduce surprises where `adapter.limits` shows high values but a device request fails to include needed higher limits.

#### Use Cases
Helps developers diagnose and fix device request errors before hitting runtime limits.

#### References
- [issue 42240683](https://issues.chromium.org/issues/42240683)

### Enable compatibility mode with featureLevel

#### What's New
You can request an adapter in the experimental compatibility mode by setting the standardized `featureLevel` option.

#### Technical Details
Exposes the compatibility proposal via the standardized `featureLevel` adapter request option.

#### Use Cases
Eases interoperability with legacy or non-standard GPU behaviors when needed.

#### References
- [experimental compatibility mode](https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md#webgpu-spec-changes)
- [`featureLevel`](https://gpuweb.github.io/gpuweb/#dom-gpurequestadapteroptions-featurelevel)
- [spec PR 4897](https://github.com/gpuweb/gpuweb/pull/4897)
- [webgpureport.org](https://webgpureport.org)

### Experimental subgroup features cleanup

#### What's New
Deprecated experimental subgroup features `"chromium-experimental-subgroups"` and `"chromium-experimental-subgroup-uniform-control-flow"` have been removed; the `"subgroups"` feature suffices now.

#### Technical Details
Cleanup follows upstream experimentation consolidation.

#### Use Cases
Simplifies feature flags for subgroup functionality.

#### References
- [issue 377868468](https://issues.chromium.org/issues/377868468)
- [issue 380244620](https://issues.chromium.org/issues/380244620)

### Deprecate maxInterStageShaderComponents limit

#### What's New
The `maxInterStageShaderComponents` limit is deprecated due to redundancy with `maxInterStageShaderVariables` and minor discrepancies.

#### Technical Details
Deprecation reduces API surface and avoids confusion between overlapping limits.

#### Use Cases
Developers should migrate to `maxInterStageShaderVariables` where applicable.

#### References
- [intent to deprecate](https://groups.google.com/a/chromium.org/g/blink-dev/c/i5oJu9lZPAk)
- [issue 364338810](https://issues.chromium.org/issues/364338810)

### Dawn updates

#### What's New
Dawn API changes: `wgpu::Device::GetAdapterInfo(adapterInfo)` added and `WGPUProgrammableStageDescriptor` renamed to `WGPUComputeState`, among other commits.

#### Technical Details
Implementation and API adjustments to keep Dawn aligned with spec and usage patterns.

#### Use Cases
Native engine authors and bindings maintainers should review these changes for binding updates.

#### References
- [issue 376600838](https://issues.chromium.org/issues/376600838)
- [issue 379059434](https://issues.chromium.org/issues/379059434)
- [issue 383147017](https://issues.chromium.org/issues/383147017)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/6834..chromium/6943?n=1000)

### Opt out of freezing on Energy Saver

#### What's New
An origin trial to let sites opt out of the Energy Saver freezing behavior shipping in Chrome 133.

#### Technical Details
Provided as an opt-out trial for site registration.

#### Use Cases
Sites that rely on continuous GPU work or media playback can opt out to avoid freezing on Energy Saver.

#### References
- [Tracking bug #325954772](https://issues.chromium.org/issues/325954772)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5158599457767424)
- [Spec](https://wicg.github.io/page-lifecycle)

### Reference Target for Cross-root ARIA

#### What's New
Reference Target enables IDREF attributes (e.g., `for`, `aria-labelledby`) to reference elements inside shadow DOM while keeping encapsulation.

#### Technical Details
Aims to let ARIA work across shadow roots without exposing internal DOM details.

#### Use Cases
Accessibility improvements for components using shadow DOM.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5188237101891584)

### Deprecate WebGPU limit `maxInterStageShaderComponents`

#### What's New
Duplicate/deprecation note: `maxInterStageShaderComponents` is deprecated with an intended removal date in Chrome 135.

#### Technical Details
Reiterates redundancy with `maxInterStageShaderVariables` and notes planned removal.

#### Use Cases
Prepare migration away from this limit before Chrome 135.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/4853767735083008)

### Remove `<link rel=prefetch>` five-minute rule

#### What's New
Chrome removes the special five-minute rule for prefetched resources; normal HTTP cache semantics (e.g., max-age, no-cache) now apply from first use.

#### Technical Details
Prefetches no longer override cache headers for an initial five-minute window.

#### Use Cases
Developers should rely on standard caching semantics for prefetch behavior.

#### References
- [Tracking bug #40232065](https://issues.chromium.org/issues/40232065)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5087526916718592)

### Remove Chrome Welcome page triggering with initial prefs first run tabs

#### What's New
Including `chrome://welcome` in `first_run_tabs` of `initial_preferences` no longer triggers the Welcome page.

#### Technical Details
Removed as redundant with existing First Run Experience on desktop.

#### Use Cases
Administrators and OEMs should not rely on this preference to trigger the Chrome Welcome page.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5118328941838336)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)
