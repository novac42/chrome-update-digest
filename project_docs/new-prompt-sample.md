---
layout: default
title: chrome-140
---

## Graphics and WebGPU

### Area Summary

Chrome 140 continues to refine the WebGPU API with important ergonomic improvements and specification compliance updates. The release focuses on simplifying texture handling, enforcing proper adapter consumption patterns, and deprecating non-standard features to improve cross-browser compatibility. These changes demonstrate WebGPU's maturation as it moves toward broader adoption, with particular attention to developer experience through simpler APIs and clearer resource management patterns. Additionally, significant performance optimizations in the Dawn backend, especially for mobile GPUs, highlight Chrome's commitment to making WebGPU performant across all device categories.

### Detailed Updates

Building on the summary above, here are the specific improvements and changes in Chrome 140's WebGPU implementation:

#### Device requests consume adapter

**What's New**:
Adapters are now marked as "consumed" after a successful device request, preventing subsequent `requestDevice()` calls on the same adapter.

**Technical Details**:
Following the WebGPU specification, once `requestDevice()` succeeds on an adapter, that adapter becomes consumed. Any further attempts to request a device from the same adapter will result in a rejected promise, replacing the previous behavior where such calls would return a device that was lost at creation.

**Use Cases**:
This change enforces proper resource management patterns and prevents subtle bugs from reusing adapters. Developers must now explicitly request a new adapter if they need multiple devices, leading to clearer and more predictable code.

**References**:
[WebGPU specification](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1) | [Issue #415825174](https://issues.chromium.org/issues/415825174)

#### Shorthand for using texture where texture view is used

**What's New**:
GPUTexture objects can now be used directly as binding resources without explicitly creating texture views.

**Technical Details**:
A GPUTexture can be used directly as a GPUBindingResource for shader bindings, and as color attachments or depth-stencil attachments in render passes. This eliminates the need to call `createView()` for default texture views, as the texture itself now serves as shorthand for `myTexture.createView()`.

**Use Cases**:
Simplifies WebGPU code by reducing boilerplate when default texture views are sufficient. This is particularly useful in common rendering scenarios where custom view parameters aren't needed, making the API more approachable for newcomers.

**References**:
[GPUTexture](https://gpuweb.github.io/gpuweb/#gputexture) | [GPUBindingResource](https://gpuweb.github.io/gpuweb/#typedefdef-gpubindingresource) | [GPUTextureView](https://gpuweb.github.io/gpuweb/#dictdef-gpubufferbinding) | [Issue #425906323](https://issues.chromium.org/issues/425906323)

#### WGSL textureSampleLevel supports 1D textures

**What's New**:
The `textureSampleLevel()` function now supports 1D textures, enabling their use in vertex shaders.

**Technical Details**:
Previously, 1D textures could only be sampled in fragment shaders using `textureSample()`. This update brings consistency with 2D textures by allowing `textureSampleLevel()` to work with 1D textures, providing explicit level-of-detail control.

**Use Cases**:
Enables advanced rendering techniques that require 1D texture lookups in vertex shaders, such as displacement mapping or vertex animation using texture-based data. This consistency improvement removes an artificial limitation in the shading pipeline.

**References**:
[textureSampleLevel](https://gpuweb.github.io/gpuweb/wgsl/#texturesamplelevel) | [Issue #382514673](https://issues.chromium.org/issues/382514673)

#### Deprecate bgra8unorm read-only storage texture usage

**What's New**:
The `bgra8unorm` format is now deprecated for read-only storage textures, aligning with WebGPU specification requirements.

**Technical Details**:
The WebGPU specification explicitly disallows using `bgra8unorm` format with read-only storage textures. This format is intended for write-only access, and Chrome's previous allowance was a bug that created portability issues.

**Use Cases**:
Developers using `bgra8unorm` for read-only storage textures must migrate to appropriate formats. This change ensures code portability across different WebGPU implementations and prevents runtime errors on compliant browsers.

**References**:
[Issue #427681156](https://issues.chromium.org/issues/427681156)

#### Remove GPUAdapter isFallbackAdapter attribute

**What's New**:
The deprecated `GPUAdapter.isFallbackAdapter` attribute has been removed in favor of `GPUAdapterInfo.isFallbackAdapter`.

**Technical Details**:
As announced in Chrome 138, the `isFallbackAdapter` attribute has been moved from GPUAdapter to GPUAdapterInfo (introduced in Chrome 136). This aligns with the evolving WebGPU specification structure.

**Use Cases**:
Applications checking for fallback adapters must update their code to access this information through `adapter.info.isFallbackAdapter` instead of `adapter.isFallbackAdapter`. This provides a cleaner separation between adapter objects and their metadata.

**References**:
[Intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/Wzr22XXV3s8)

#### Dawn updates

**What's New**:
Multiple Dawn backend improvements including WGSL language feature queries, surface presentation error handling, multi-device support, and mobile GPU optimizations.

**Technical Details**:
Key updates include: `wgpuInstanceGetWGSLLanguageFeatures()` no longer returns a status value since it can't fail; `wgpuSurfacePresent()` now returns error status for surfaces without current textures; new `MultipleDevicesPerAdapter` feature allows creating multiple devices without consuming the adapter; `dump_shaders_on_failure` toggle aids debugging on D3D backends; Vulkan backend optimizations reduce render pass submission overhead through techniques like VkFramebuffer caching.

**Use Cases**:
These improvements benefit native Dawn users and contribute to better WebGPU performance in Chrome. Mobile developers particularly benefit from reduced overhead in render pass submission, while the debugging improvements help developers diagnose shader compilation issues.

**References**:
[Issue #429178774](https://issues.chromium.org/issues/429178774) | [Issue #425930323](https://issues.chromium.org/issues/425930323) | [Issue #415825174](https://issues.chromium.org/issues/415825174) | [Debugging documentation](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/debugging.md) | [Issue #429187478](http://issues.chromium.org/issues/429187478) | [VkFramebuffer caching](https://dawn.googlesource.com/dawn/+/ddf2e1f61d20171ecd10ae3be70acb750a56686d) | [Full commit list](https://dawn.googlesource.com/dawn/+log/chromium/7258..chromium/7339?n=1000)