---
layout: default
title: graphics-webgpu-en
---

## Area Summary

Chrome 140 (stable) continues aligning WebGPU and WGSL behavior with the evolving GPUWeb specification and Dawn runtime, focusing on stricter spec conformance, API cleanup, and shader convenience. The most impactful changes for developers are the adapter consumption semantics for requestDevice(), shorthand acceptance of GPUTexture in places previously requiring GPUTextureView, WGSL support for sampling 1D textures with textureSampleLevel(), and the deprecation/removal of non-portable or redundant APIs. These changes improve portability and predictability of GPU code across implementations, reduce boilerplate, and require minor migration or validation work in existing apps.

## Detailed Updates

Below are concise, developer-focused breakdowns of each Graphics and WebGPU update in Chrome 140.

### Device requests consume adapter

#### What's New
An adapter is now marked as "consumed" after a successful requestDevice() call; further requestDevice() calls using the same adapter will be rejected.

#### Technical Details
This enforces the WebGPU spec state machine for DOM adapters: once an adapter yields a device, the adapter is considered consumed and cannot produce additional devices. Implementations will reject subsequent promises from requestDevice() on that adapter.

#### Use Cases
- Prevents accidental multiple device allocations from the same adapter.
- Requires apps that previously relied on repeated requestDevice() from one adapter to create a new adapter or redesign initialization flow.

#### References
- [WebGPU specification](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1)
- [issue 415825174](https://issues.chromium.org/issues/415825174)

### Shorthand for using texture where texture view is used

#### What's New
A GPUTexture can be used directly as a GPUBindingResource and in places that previously required a GPUTextureView (e.g., render pass color attachment view).

#### Technical Details
APIs accepting GPUBindingResource or fields typed as GPUTextureView now accept GPUTexture objects as a shorthand. The platform performs the equivalent implicit view handling so developers can pass the texture directly.

#### Use Cases
- Reduces boilerplate for common patterns where the default texture view is sufficient.
- Simplifies code paths that construct descriptors for passes and bindings.

#### References
- [GPUTexture](https://gpuweb.github.io/gpuweb/#gputexture)
- [GPUBindingResource](https://gpuweb.github.io/gpuweb/#typedefdef-gpubindingresource)
- [GPUTextureView](https://gpuweb.github.io/gpuweb/#dictdef-gpubufferbinding)
- [issue 425906323](https://issues.chromium.org/issues/425906323)

### WGSL textureSampleLevel supports 1D textures

#### What's New
WGSL's textureSampleLevel() can now sample 1D textures, enabling sampling from vertex shaders similar to 2D textures.

#### Technical Details
The WGSL builtin textureSampleLevel() has been extended to accept 1D texture types so vertex-stage sampling of 1D textures is allowed and follows the same semantics as 2D sampling.

#### Use Cases
- Allows procedural or curve sampling in vertex shaders using 1D textures.
- Enables consistent shader code paths across 1D and 2D textures without special-casing sampling functions.

#### References
- [sampled](https://gpuweb.github.io/gpuweb/wgsl/#texturesamplelevel)
- [issue 382514673](https://issues.chromium.org/issues/382514673)

### Deprecate bgra8unorm read-only storage texture usage

#### What's New
Using "bgra8unorm" with read-only storage textures is deprecated; this usage was previously allowed in Chrome but is disallowed by the WebGPU specification.

#### Technical Details
"bgra8unorm" is intended for write-only storage usage and is not portable for read-only storage. Chrome's prior allowance is being removed to match the specification and avoid non-portable behavior.

#### Use Cases
- Developers must avoid relying on read-only storage access to bgra8unorm textures and migrate to supported formats or usage patterns for portability.

#### References
- [issue 427681156](https://issues.chromium.org/issues/427681156)

### Remove GPUAdapter isFallbackAdapter attribute

#### What's New
GPUAdapter.isFallbackAdapter has been removed; use GPUAdapterInfo.isFallbackAdapter (introduced in Chrome 136) instead.

#### Technical Details
The adapter-level boolean was deprecated and is now removed in favor of the isFallbackAdapter flag on GPUAdapterInfo, consolidating device/adapter metadata and reducing redundancy.

#### Use Cases
- Migration: replace usages of adapter.isFallbackAdapter with adapter.requestAdapterInfo().isFallbackAdapter or equivalent GPUAdapterInfo access.

#### References
- [intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/Wzr22XXV3s8)

### Dawn updates

#### What's New
Dawn changes include API cleanup such as wgpuInstanceGetWGSLLanguageFeatures() no longer returning a WGPUStatus since it cannot fail, plus multiple internal fixes and commits listed for Chromium.

#### Technical Details
- wgpuInstanceGetWGSLLanguageFeatures() now returns via out-parameters without a status code.
- Additional Dawn changes include debugging docs, framebuffer caching, and a series of commits referenced for Chromium's Dawn integration.

#### Use Cases
- Native embedder and engine maintainers should update calls to the revised Dawn APIs.
- Helps reduce error-handling noise for functions guaranteed to succeed.

#### References
- [issue 429178774](https://issues.chromium.org/issues/429178774)
- [issue 425930323](https://issues.chromium.org/issues/425930323)
- [issue 415825174](https://issues.chromium.org/issues/415825174)
- [debugging purposes](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/debugging.md)
- [issue 429187478](http://issues.chromium.org/issues/429187478)
- [caching VkFramebuffers](https://dawn.googlesource.com/dawn/+/ddf2e1f61d20171ecd10ae3be70acb750a56686d)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7258..chromium/7339?n=1000)
