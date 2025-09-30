---
layout: default
title: Area Summary
---

# Area Summary

Chrome 140's Graphics and WebGPU updates focus on tightening WebGPU spec conformance, improving WGSL consistency, and cleaning up legacy or incorrect API surface. The most impactful changes for developers are adapter lifecycle semantics (consumed adapters), new shorthand and sampler behaviors for textures (including 1D support in WGSL), and deprecations/removals that affect portability and migration (bgra8unorm storage usage and isFallbackAdapter). These updates advance the web platform by reducing implementation inconsistencies, improving shader expressivity, and removing non-portable or redundant API pieces—lowering risk for cross‑platform GPU code and tooling. Teams should evaluate device/adapter lifecycle in their resource management, adjust shader and binding code for the shorthand and 1D sampling, and follow deprecation/migration guidance to avoid runtime failures.

## Detailed Updates

Below are the Graphics and WebGPU changes in Chrome 140 with concise technical notes and developer-centric use cases.

### Device requests consume adapter

#### What's New
An adapter is now marked as "consumed" upon a successful device request. Subsequent `requestDevice()` calls on the same adapter will reject.

#### Technical Details
This aligns Chrome behavior with the WebGPU specification rule that an adapter's state becomes consumed after creating a GPUDevice. Requesting another device from the same adapter is no longer allowed and results in a rejected promise.

#### Use Cases
- Update adapter/device lifecycle handling in apps and engines that create multiple devices from the same adapter.
- Ensure resource allocation and teardown occur when a device is created, and avoid reuse patterns that assume multiple devices per adapter.

#### References
- [WebGPU specification](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1)  
- [issue 415825174](https://issues.chromium.org/issues/415825174)

### Shorthand for using texture where texture view is used

#### What's New
A GPUTexture can now be used directly as a GPUBindingResource and in places where a GPUTextureView was previously required (e.g., render pass color attachment `view`).

#### Technical Details
This shorthand reduces boilerplate by allowing the texture to be implicitly treated as a texture view for binding and attachment points, matching updates in the spec to accept GPUTexture in those roles.

#### Use Cases
- Simplify bind/group setup and render pass creation code by omitting explicit texture view creation in common cases.
- Reduce code paths and allocations in engines that frequently create single-use views.

#### References
- [GPUTexture](https://gpuweb.github.io/gpuweb/#gputexture)  
- [GPUBindingResource](https://gpuweb.github.io/gpuweb/#typedefdef-gpubindingresource)  
- [GPUTextureView](https://gpuweb.github.io/gpuweb/#dictdef-gpubufferbinding)  
- [issue 425906323](https://issues.chromium.org/issues/425906323)

### WGSL textureSampleLevel supports 1D textures

#### What's New
`textureSampleLevel()` now supports sampling 1D textures, enabling its use from shaders (including vertex shaders) in the same way as 2D textures.

#### Technical Details
This change brings 1D textures into parity with 2D for the textureSampleLevel builtin, allowing explicit LOD sampling calls from shader stages that previously had restricted sampling behavior.

#### Use Cases
- Use explicit LOD sampling of 1D textures in vertex or compute shaders for procedural or curve-based lookups.
- Port shader code that relied on fragment-only sampling patterns to earlier pipeline stages.

#### References
- [sampled](https://gpuweb.github.io/gpuweb/wgsl/#texturesamplelevel)  
- [issue 382514673](https://issues.chromium.org/issues/382514673)

### Deprecate bgra8unorm read-only storage texture usage

#### What's New
Using the "bgra8unorm" format as a read-only storage texture is deprecated; prior allowance in Chrome was a bug.

#### Technical Details
The WebGPU specification disallows read-only storage access for this format because it's intended for write-only usage and is not portable. Chrome is now deprecating that previously permitted usage to move toward spec-compliant behavior.

#### Use Cases
- Audit code that binds bgra8unorm textures as read-only storage and migrate to portable formats or access patterns.
- Prefer formats explicitly allowed for read-only storage to ensure cross‑browser portability and correct behavior.

#### References
- [issue 427681156](https://issues.chromium.org/issues/427681156)

### Remove GPUAdapter isFallbackAdapter attribute

#### What's New
The GPUAdapter `isFallbackAdapter` attribute has been removed; the attribute now lives on GPUAdapterInfo and was introduced earlier.

#### Technical Details
This completes the deprecation/removal announced earlier and centralizes fallback information in GPUAdapterInfo (added in Chrome 136), removing redundancy from GPUAdapter.

#### Use Cases
- Update adapter inspection logic to read `isFallbackAdapter` from GPUAdapterInfo rather than GPUAdapter.
- Remove fallback-related feature checks against GPUAdapter properties in engine/platform detection layers.

#### References
- [intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/Wzr22XXV3s8)

### Dawn updates

#### What's New
Dawn's `wgpuInstanceGetWGSLLanguageFeatures()` no longer returns a `WGPUStatus` value since it cannot fail; other internal changes include various bugfixes and debug improvements.

#### Technical Details
API was simplified to remove an unnecessary status return. The Dawn updates also include changes like caching VkFramebuffers and debugging docs/commits listed in the linked resources.

#### Use Cases
- Native tooling and embedders using Dawn should update call sites to the new signature.
- Review Dawn changelog entries for performance and backend fixes that may affect GPU behavior and resource caching.

#### References
- [issue 429178774](https://issues.chromium.org/issues/429178774)  
- [issue 425930323](https://issues.chromium.org/issues/425930323)  
- [issue 415825174](https://issues.chromium.org/issues/415825174)  
- [debugging purposes](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/debugging.md)  
- [issue 429187478](http://issues.chromium.org/issues/429187478)  
- [caching VkFramebuffers](https://dawn.googlesource.com/dawn/+/ddf2e1f61d20171ecd10ae3be70acb750a56686d)  
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7258..chromium/7339?n=1000)

Saved to: digest_markdown/webplatform/Graphics and WebGPU/chrome-140-stable-en.md
