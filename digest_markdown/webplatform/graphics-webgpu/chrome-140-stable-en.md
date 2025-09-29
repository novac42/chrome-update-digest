# Chrome 140 Graphics and WebGPU Updates

## Area Summary

Chrome 140 brings significant refinements to the WebGPU API, focusing on specification compliance and developer ergonomics. The most notable improvements include texture handling simplifications with direct GPUTexture usage, expanded WGSL capabilities for 1D textures, and stricter adherence to WebGPU standards through adapter consumption enforcement and format deprecations. These updates collectively enhance GPU programming workflows while ensuring better portability and consistency across different hardware configurations.

## Detailed Updates

This release emphasizes WebGPU maturation through specification alignment and API ergonomics improvements, making GPU programming more intuitive for web developers.

### Device requests consume adapter

#### What's New
WebGPU adapters are now properly marked as "consumed" after successful device requests, preventing multiple device creation from the same adapter instance.

#### Technical Details
Following the WebGPU specification, any subsequent `requestDevice()` calls on a consumed adapter will result in rejected promises. This ensures proper resource management and prevents potential conflicts when multiple contexts attempt to use the same adapter.

#### Use Cases
Improves application reliability by enforcing single-device-per-adapter patterns and provides clearer error handling for GPU resource allocation scenarios.

#### References
- [WebGPU specification](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1)
- [issue 415825174](https://issues.chromium.org/issues/415825174)

### Shorthand for using texture where texture view is used

#### What's New
GPUTexture objects can now be used directly as GPUBindingResource and in render pass attachments, eliminating the need to explicitly create texture views in many common scenarios.

#### Technical Details
This shorthand allows GPUTexture to be used directly in binding groups, render pass color attachments, and depth-stencil attachments where a GPUTextureView was previously required. The API automatically handles view creation behind the scenes.

#### Use Cases
Simplifies shader resource binding code, reduces boilerplate for common texture usage patterns, and makes WebGPU more approachable for developers transitioning from other graphics APIs.

#### References
- [GPUTexture](https://gpuweb.github.io/gpuweb/#gputexture)
- [GPUBindingResource](https://gpuweb.github.io/gpuweb/#typedefdef-gpubindingresource)
- [GPUTextureView](https://gpuweb.github.io/gpuweb/#dictdef-gpubufferbinding)
- [issue 425906323](https://issues.chromium.org/issues/425906323)

### WGSL textureSampleLevel supports 1D textures

#### What's New
The `textureSampleLevel()` function in WGSL now supports 1D textures, enabling level-of-detail sampling from vertex shaders.

#### Technical Details
This enhancement brings consistency with 2D texture sampling capabilities. Previously, 1D textures could only be sampled from fragment shaders using `textureSample()`. Now vertex shaders can also sample 1D textures with explicit level-of-detail control.

#### Use Cases
Enables advanced vertex shader techniques like displacement mapping with 1D lookup textures, procedural animation with noise textures, and consistent sampling patterns across shader stages.

#### References
- [sampled](https://gpuweb.github.io/gpuweb/wgsl/#texturesamplelevel)
- [issue 382514673](https://issues.chromium.org/issues/382514673)

### Deprecate bgra8unorm read-only storage texture usage

#### What's New
The `"bgra8unorm"` format is now deprecated for read-only storage textures, aligning with WebGPU specification requirements.

#### Technical Details
This format was previously allowed in Chrome due to a bug, but the WebGPU specification explicitly disallows read-only storage access for `bgra8unorm`. The format is designed for write-only access and lacks portability across different GPU vendors and drivers.

#### Use Cases
Developers should migrate to supported read-only storage texture formats like `rgba8unorm` or `rgba8snorm` for cross-platform compatibility and specification compliance.

#### References
- [issue 427681156](https://issues.chromium.org/issues/427681156)

### Remove GPUAdapter isFallbackAdapter attribute

#### What's New
The deprecated `isFallbackAdapter` attribute has been removed from GPUAdapter, completing the migration to GPUAdapterInfo introduced in Chrome 136.

#### Technical Details
Applications should now access fallback adapter information through the `GPUAdapterInfo.isFallbackAdapter` attribute instead of the removed `GPUAdapter.isFallbackAdapter` property.

#### Use Cases
Ensures consistent adapter information access patterns and enables more detailed adapter capability queries through the unified GPUAdapterInfo interface.

#### References
- [intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/Wzr22XXV3s8)

### Dawn updates

#### What's New
Multiple Dawn native API improvements including WGSL language feature query updates, enhanced Vulkan framebuffer caching, and various bug fixes.

#### Technical Details
The `wgpuInstanceGetWGSLLanguageFeatures()` function no longer returns a status value since it cannot fail. Vulkan backend improvements include better framebuffer caching for performance optimization. Additional fixes address device creation, debugging capabilities, and memory management.

#### Use Cases
Native WebGPU applications benefit from improved performance, more reliable device creation, and enhanced debugging capabilities for development workflows.

#### References
- [issue 429178774](https://issues.chromium.org/issues/429178774)
- [issue 425930323](https://issues.chromium.org/issues/425930323)
- [issue 415825174](https://issues.chromium.org/issues/415825174)
- [debugging purposes](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/debugging.md)
- [issue 429187478](http://issues.chromium.org/issues/429187478)
- [caching VkFramebuffers](https://dawn.googlesource.com/dawn/+/ddf2e1f61d20171ecd10ae3be70acb750a56686d)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7258..chromium/7339?n=1000)