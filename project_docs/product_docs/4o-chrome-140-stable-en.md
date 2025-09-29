# Chrome Update Digest for Graphics and WebGPU - Chrome 140 (Stable)

## Area Summary

Chrome 140 introduces several impactful updates in the Graphics and WebGPU domain. These changes enhance developer ergonomics, improve performance, and align with the latest WebGPU specifications. Key highlights include the deprecation of non-portable texture formats, support for 1D texture sampling, and updates to the Dawn graphics library. These updates empower developers to build more efficient and standards-compliant GPU-accelerated applications.

## Detailed Updates

### Device requests consume adapter

#### What's New

Adapters are now marked as "consumed" upon a successful device request. Subsequent `requestDevice()` calls on the same adapter will fail, ensuring compliance with the WebGPU specification.

#### Technical Details

Previously, multiple `requestDevice()` calls on the same adapter would return a lost device. Now, the adapter is marked as consumed after the first successful request, and further calls will reject the promise.

#### Use Cases

This change prevents unintended behavior when managing GPU devices, ensuring developers handle adapters correctly.

#### References

- [WebGPU specification](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1)
- [Issue 415825174](https://issues.chromium.org/issues/415825174)

### Shorthand for using texture where texture view is used

#### What's New

`GPUTexture` can now be used directly as a `GPUBindingResource` and in various render pass attachments, simplifying the workflow.

#### Technical Details

This update eliminates the need to create a `GPUTextureView` for default views, allowing direct usage of `GPUTexture` in bindings and attachments.

#### Use Cases

Developers benefit from reduced boilerplate code and improved ergonomics when working with textures.

#### References

- [GPUTexture](https://gpuweb.github.io/gpuweb/#gputexture)
- [GPUBindingResource](https://gpuweb.github.io/gpuweb/#typedefdef-gpubindingresource)
- [GPUTextureView](https://gpuweb.github.io/gpuweb/#dictdef-gpubufferbinding)
- [Issue 425906323](https://issues.chromium.org/issues/425906323)

### WGSL textureSampleLevel supports 1D textures

#### What's New

1D textures can now be sampled using `textureSampleLevel()` for consistency with 2D textures.

#### Technical Details

This feature enables sampling 1D textures from vertex shaders, which was previously limited to fragment shaders using `textureSample()`.

#### Use Cases

Developers can now use 1D textures in more shader stages, expanding their utility in graphics pipelines.

#### References

- [Sampled](https://gpuweb.github.io/gpuweb/wgsl/#texturesamplelevel)
- [Issue 382514673](https://issues.chromium.org/issues/382514673)

### Deprecate bgra8unorm read-only storage texture usage

#### What's New

The `bgra8unorm` format is now deprecated for read-only storage textures, aligning with the WebGPU specification.

#### Technical Details

This format was previously allowed due to a bug but is intended for write-only access. Its deprecation ensures portability and standards compliance.

#### Use Cases

Developers must migrate to supported formats for read-only storage textures, ensuring compatibility across platforms.

#### References

- [Issue 427681156](https://issues.chromium.org/issues/427681156)

### Remove GPUAdapter isFallbackAdapter attribute

#### What's New

The `isFallbackAdapter` attribute has been removed from `GPUAdapter` and replaced by `GPUAdapterInfo.isFallbackAdapter`.

#### Technical Details

This change was announced in Chrome 138 and is now finalized, improving the clarity of adapter fallback status.

#### Use Cases

Developers should update their code to use the new `GPUAdapterInfo` attribute for fallback checks.

#### References

- [Intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/Wzr22XXV3s8)

### Dawn updates

#### What's New

The Dawn graphics library has received multiple updates, including new features, bug fixes, and performance improvements.

#### Technical Details

- `wgpuInstanceGetWGSLLanguageFeatures()` no longer returns a value.
- `wgpuSurfacePresent()` now returns a `WGPUStatus` error if the surface lacks a current texture.
- New `wgpu::InstanceFeatureName::MultipleDevicesPerAdapter` feature allows multiple devices per adapter.
- `dump_shaders_on_failure` toggle added for debugging.
- Vulkan backend optimizations reduce render pass overhead, especially on mobile GPUs.

#### Use Cases

These updates enhance the developer experience, improve debugging capabilities, and optimize performance for GPU-intensive applications.

#### References

- [Issue 429178774](https://issues.chromium.org/issues/429178774)
- [Issue 425930323](https://issues.chromium.org/issues/425930323)
- [Issue 415825174](https://issues.chromium.org/issues/415825174)
- [Debugging purposes](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/debugging.md)
- [Issue 429187478](http://issues.chromium.org/issues/429187478)
- [Caching VkFramebuffers](https://dawn.googlesource.com/dawn/+/ddf2e1f61d20171ecd10ae3be70acb750a56686d)
- [List of commits](https://dawn.googlesource.com/dawn/+log/chromium/7258..chromium/7339?n=1000)