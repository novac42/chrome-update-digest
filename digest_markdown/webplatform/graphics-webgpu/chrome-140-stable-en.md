# Chrome 140 Stable - Graphics and WebGPU Update Analysis

## Summary

Chrome 140 brings significant improvements to WebGPU with enhanced texture handling, adapter consumption management, and WGSL shader capabilities. Key highlights include simplified texture usage patterns, improved 1D texture support in vertex shaders, and important deprecations to align with WebGPU specifications. The update also includes Dawn engine improvements and removes deprecated adapter attributes.

## Feature Details

### Device requests consume adapter

**What Changed**:
WebGPU adapters are now properly marked as "consumed" after a successful device request, following the WebGPU specification. Once an adapter has been used to create a device, any subsequent `requestDevice()` calls on the same adapter will be rejected with a promise rejection. This change ensures proper resource management and prevents multiple device creation from the same adapter, which could lead to undefined behavior or resource conflicts.

**References**:
- [WebGPU specification](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1)
- [issue 415825174](https://issues.chromium.org/issues/415825174)

### Shorthand for using texture where texture view is used

**What Changed**:
GPUTexture objects can now be used directly as GPUBindingResource for shader binding, eliminating the need to create explicit texture views in many common scenarios. This applies to render pass color attachments, depth/stencil attachments, and general binding operations. The change simplifies WebGPU code by reducing boilerplate texture view creation while maintaining full compatibility with existing explicit texture view usage patterns.

**References**:
- [GPUTexture](https://gpuweb.github.io/gpuweb/#gputexture)
- [GPUBindingResource](https://gpuweb.github.io/gpuweb/#typedefdef-gpubindingresource)
- [GPUTextureView](https://gpuweb.github.io/gpuweb/#dictdef-gpubufferbinding)
- [issue 425906323](https://issues.chromium.org/issues/425906323)

### WGSL textureSampleLevel supports 1D textures

**What Changed**:
The `textureSampleLevel()` function in WGSL now supports 1D textures, bringing consistency with 2D texture sampling. This enhancement allows 1D textures to be sampled from vertex shaders, which was previously only possible from fragment shaders using `textureSample()`. This improvement expands the flexibility of 1D texture usage in graphics pipelines and enables more sophisticated vertex shader techniques.

**References**:
- [sampled](https://gpuweb.github.io/gpuweb/wgsl/#texturesamplelevel)
- [issue 382514673](https://issues.chromium.org/issues/382514673)

### Deprecate bgra8unorm read-only storage texture usage

**What Changed**:
The use of "bgra8unorm" format with read-only storage textures is now deprecated. This format was incorrectly allowed in previous Chrome versions but is explicitly disallowed by the WebGPU specification. The bgra8unorm format is designed for write-only access and lacks portability across different graphics hardware. Developers should migrate to appropriate read-compatible formats for storage texture operations.

**References**:
- [issue 427681156](https://issues.chromium.org/issues/427681156)

### Remove GPUAdapter isFallbackAdapter attribute

**What Changed**:
The deprecated `isFallbackAdapter` attribute has been removed from GPUAdapter objects. This attribute was replaced by the `isFallbackAdapter` attribute in GPUAdapterInfo, which was introduced in Chrome 136. Applications should update their code to access fallback adapter information through `adapter.info.isFallbackAdapter` instead of the now-removed direct adapter property.

**References**:
- [intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/Wzr22XXV3s8)

### Dawn updates

**What Changed**:
The Dawn WebGPU implementation received several important updates. The `wgpuInstanceGetWGSLLanguageFeatures()` function no longer returns a WGSLStatus value since it cannot fail. Additional improvements include enhanced Vulkan framebuffer caching, better debugging capabilities, and various performance optimizations. These changes improve the underlying graphics engine stability and performance for WebGPU applications.

**References**:
- [issue 429178774](https://issues.chromium.org/issues/429178774)
- [issue 425930323](https://issues.chromium.org/issues/425930323)
- [issue 415825174](https://issues.chromium.org/issues/415825174)
- [debugging purposes](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/debugging.md)
- [issue 429187478](http://issues.chromium.org/issues/429187478)
- [caching VkFramebuffers](https://dawn.googlesource.com/dawn/+/ddf2e1f61d20171ecd10ae3be70acb750a56686d)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7258..chromium/7339?n=1000)