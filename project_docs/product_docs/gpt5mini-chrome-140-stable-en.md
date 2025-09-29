## Area Summary

Chrome 140's Graphics and WebGPU updates focus on API ergonomics, correctness aligned with the WebGPU specification, and runtime/tooling improvements. Key themes include stricter adapter/device semantics, simpler texture-binding ergonomics, expanded WGSL sampling capabilities, and the removal/deprecation of non-portable or legacy attributes. These changes improve portability and developer ergonomics while reducing surprising behavior at runtime. Together they advance the platform by tightening spec conformance and making common tasks (binding textures, sampling, debugging) more predictable and efficient for implementers and developers.

## Detailed Updates

Below are the area-specific highlights from Chrome 140 for Graphics and WebGPU, with technical notes and practical guidance for developers.

### Device requests consume adapter

#### What's New
Per the WebGPU specification, an adapter is marked as "consumed" after a successful `requestDevice()` call. Subsequent `requestDevice()` calls on the same adapter will reject the promise instead of returning a device that is already lost.

#### Technical Details
The change brings Chromium's behavior into line with the specification referenced in the release notes. Once an adapter has produced a device, the adapter's state transitions to consumed and further device requests using that adapter are explicitly disallowed and will reject.

#### Use Cases
- Avoid relying on multiple `requestDevice()` calls from the same adapter. Request a device once per adapter or explicitly plan for creating multiple adapters if needed.
- This prevents surprising "lost-at-creation" devices and makes error handling deterministic.

#### References
- https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1
- https://issues.chromium.org/issues/415825174

### Shorthand for using texture where texture view is used

#### What's New
A `GPUTexture` can now be used directly as a `GPUBindingResource` and in places where a `GPUTextureView` was previously required (for example as a render-pass color attachment `view` or `resolveTarget`). This provides a simpler ergonomic path than creating a default `GPUTextureView` explicitly.

#### Technical Details
When a `GPUTexture` is accepted where a `GPUTextureView` was previously required, the implementation acts as if the default view for that texture were used. The release notes show a bind group example where `resource: myTexture` is equivalent to `resource: myTexture.createView()`.

#### Use Cases
- Shorter, clearer code when the default texture view is intended (reduces boilerplate).
- Helpful for common pipelines that use the default full-texture view and for bindings where an explicit view creation adds no value.

#### References
- https://gpuweb.github.io/gpuweb/#gputexture
- https://gpuweb.github.io/gpuweb/#typedefdef-gpubindingresource
- https://gpuweb.github.io/gpuweb/#dictdef-gpubufferbinding
- https://issues.chromium.org/issues/425906323

### WGSL textureSampleLevel supports 1D textures

#### What's New
`textureSampleLevel()` in WGSL can now sample 1D textures, enabling sampling from a vertex shader as well as a fragment shader for 1D textures.

#### Technical Details
This update extends the sampling capability of `textureSampleLevel()` to be consistent across texture dimensionalities. Previously, 1D textures could only be sampled from fragment shaders with `textureSample()`.

#### Use Cases
- Vertex-stage sampling from 1D textures for procedural or curve-based vertex computations.
- Makes shader code more consistent across 1D/2D texture use and can simplify cross-dimensional shader libraries.

#### References
- https://gpuweb.github.io/gpuweb/wgsl/#texturesamplelevel
- https://issues.chromium.org/issues/382514673

### Deprecate bgra8unorm read-only storage texture usage

#### What's New
Using the `bgra8unorm` format with read-only storage textures is deprecated. That usage was previously allowed in Chrome but is disallowed by the specification.

#### Technical Details
The `bgra8unorm` format is intended for write-only access and allowing it as read-only storage was a portability bug. Deprecation aligns Chromium with the WebGPU spec to avoid non-portable behavior.

#### Use Cases
- Developers should avoid relying on read-side accesses to `bgra8unorm` storage textures and migrate to formats and access patterns that are spec-compliant.
- This helps prevent unexpected behavior when targeting multiple implementations.

#### References
- https://issues.chromium.org/issues/427681156

### Remove GPUAdapter isFallbackAdapter attribute

#### What's New
The `GPUAdapter.isFallbackAdapter` attribute has been removed. Its replacement is the `GPUAdapterInfo.isFallbackAdapter` attribute introduced in Chrome 136.

#### Technical Details
The older attribute was deprecated earlier and has now been removed in favor of the `GPUAdapterInfo`-scoped property. The change was previously announced in the project's blog and discussed on the Blink developer list.

#### Use Cases
- Use `GPUAdapterInfo.isFallbackAdapter` where adapter fallback detection is required; update code that relied on the removed attribute.

#### References
- /blog/new-in-webgpu-138#deprecate_gpuadapter_isfallbackadapter_attribute
- https://groups.google.com/a/chromium.org/g/blink-dev/c/Wzr22XXV3s8

### Dawn updates

#### What's New
Multiple Dawn (the WebGPU native implementation) changes landed: function return-type changes, new instance/feature flags, debugging toggles, presentation error reporting updates, and several Vulkan backend performance improvements.

#### Technical Details
- `wgpuInstanceGetWGSLLanguageFeatures()` no longer returns a `WGPUStatus` because it cannot fail.
- `wgpuSurfacePresent()` now returns a `WGPUStatus` error when a surface has no current texture.
- A new `MultipleDevicesPerAdapter` instance feature enables creating multiple devices from an adapter without marking it consumed (related to adapter/device lifecycle behavior).
- A `dump_shaders_on_failure` device toggle was introduced to dump shaders only on failure (currently D3 backends).
- Vulkan backend changes include caching and other optimizations to reduce render-pass submission overhead.

#### Use Cases
- Tooling and native code that interact with Dawn should update to the new function signatures and check new status returns where applicable.
- The `MultipleDevicesPerAdapter` feature can be used by embedder code that needs multiple device instances from the same adapter.
- Debugging builds can benefit from `dump_shaders_on_failure` to gather shader diagnostics only when needed.

#### References
- https://issues.chromium.org/issues/429178774
- https://issues.chromium.org/issues/425930323
- https://issues.chromium.org/issues/415825174
- https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/debugging.md
- http://issues.chromium.org/issues/429187478
- https://dawn.googlesource.com/dawn/+/ddf2e1f61d20171ecd10ae3be70acb750a56686d
- https://dawn.googlesource.com/dawn/+log/chromium/7258..chromium/7339?n=1000
