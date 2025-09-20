# Chrome 140 WebPlatform Features Digest

## Overview / 概览

Chrome 140 brings several important updates to WebGPU, focusing on specification compliance and performance improvements. The key areas include WebGPU feature enhancements, storage texture deprecations, and Dawn backend optimizations.

Chrome 140 为 WebGPU 带来了多项重要更新，专注于规范合规性和性能改进。主要领域包括 WebGPU 功能增强、存储纹理弃用和 Dawn 后端优化。

## Graphics and WebGPU / 图形和WebGPU

### Device Adapter Consumption / 设备适配器消耗

**Device requests consume adapter**

According to the [WebGPU specification](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1), an adapter is marked as "consumed" upon a successful device request. Consequently, any subsequent `requestDevice()` calls using the same adapter will now result in a rejected promise. Previously, these calls would return a device that was lost at creation.

根据 [WebGPU 规范](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1)，适配器在成功请求设备后被标记为"已消耗"。因此，使用同一适配器的任何后续 `requestDevice()` 调用现在将导致被拒绝的 promise。以前，这些调用会返回一个在创建时就丢失的设备。

```javascript
const adapter = await navigator.gpu.requestAdapter();
const device = await adapter.requestDevice();

await adapter.requestDevice(); // Fails because adapter has been consumed
```

### Texture Usage Simplification / 纹理使用简化

**Shorthand for using texture where texture view is used**

A [GPUTexture](https://gpuweb.github.io/gpuweb/#gputexture) can now be used directly as a [GPUBindingResource](https://gpuweb.github.io/gpuweb/#typedefdef-gpubindingresource) to expose to the shader for binding. It can also be used as a GPURenderPassColorAttachment `view`, a GPURenderPassColorAttachment `resolveTarget`, and a GPURenderPassDepthStencilAttachment `view` for improved ergonomics.

现在可以直接将 [GPUTexture](https://gpuweb.github.io/gpuweb/#gputexture) 用作 [GPUBindingResource](https://gpuweb.github.io/gpuweb/#typedefdef-gpubindingresource) 来公开给着色器进行绑定。它还可以用作 GPURenderPassColorAttachment `view`、GPURenderPassColorAttachment `resolveTarget` 和 GPURenderPassDepthStencilAttachment `view` 以改善人体工程学。

```javascript
const bindGroup = myDevice.createBindGroup({
  layout: myPipeline.getBindGroupLayout(0),
  entries: [
    { binding: 0, resource: mySampler },
    { binding: 1, resource: myTexture }, // Same as myTexture.createView()
    { binding: 2, resource: myExternalTexture },
    { binding: 3, resource: myBuffer },
  ],
});
```

### WGSL Enhancements / WGSL 增强

**WGSL textureSampleLevel supports 1D textures**

1D textures can now be [sampled](https://gpuweb.github.io/gpuweb/wgsl/#texturesamplelevel) using `textureSampleLevel()` for consistency with 2D textures. This lets you sample a 1D texture from a vertex shader which was previously only possible from a fragment shader with `textureSample()`.

现在可以使用 `textureSampleLevel()` [采样](https://gpuweb.github.io/gpuweb/wgsl/#texturesamplelevel) 1D 纹理，以与 2D 纹理保持一致。这允许您从顶点着色器中采样 1D 纹理，这在以前只能使用 `textureSample()` 从片段着色器中实现。

### Storage Texture Deprecation / 存储纹理弃用

**Deprecate bgra8unorm read-only storage texture usage**

Using `"bgra8unorm"` format with read-only storage textures is now deprecated. The WebGPU specification explicitly disallows this, and its prior allowance in Chrome was a bug, as this format is intended for write-only access and is not portable.

现在已弃用在只读存储纹理中使用 `"bgra8unorm"` 格式。WebGPU 规范明确禁止这样做，Chrome 之前允许这样做是一个错误，因为此格式仅用于只写访问且不可移植。

### Adapter Attribute Removal / 适配器属性删除

**Remove GPUAdapter isFallbackAdapter attribute**

The GPUAdapter `isFallbackAdapter` attribute is now removed. It's replaced by the GPUAdapterInfo `isFallbackAdapter` attribute that was introduced in Chrome 136.

GPUAdapter `isFallbackAdapter` 属性现已删除。它被 Chrome 136 中引入的 GPUAdapterInfo `isFallbackAdapter` 属性所取代。

### Dawn Updates / Dawn 更新

**Multiple Dawn backend improvements**

Several important updates to the Dawn WebGPU implementation:

Dawn WebGPU 实现的几个重要更新：

- **API Changes**: The `wgpuInstanceGetWGSLLanguageFeatures()` function no longer returns a `WGPUStatus` value since it can't fail
- **Surface Presentation**: `wgpuSurfacePresent()` now returns a `WGPUStatus` error if the surface doesn't have a current texture
- **Multiple Devices**: New `wgpu::InstanceFeatureName::MultipleDevicesPerAdapter` feature allows adapters to create multiple devices without being "consumed"
- **Debugging**: The `dump_shaders_on_failure` device toggle enables shader dumping only on failure for D3 backends
- **Performance**: Multiple optimizations to the Vulkan backend to reduce overhead when submitting render passes, especially for mobile GPUs

- **API 变更**：`wgpuInstanceGetWGSLLanguageFeatures()` 函数不再返回 `WGPUStatus` 值，因为它不会失败
- **表面呈现**：如果表面没有当前纹理，`wgpuSurfacePresent()` 现在返回 `WGPUStatus` 错误
- **多设备**：新的 `wgpu::InstanceFeatureName::MultipleDevicesPerAdapter` 功能允许适配器创建多个设备而不被"消耗"
- **调试**：`dump_shaders_on_failure` 设备切换仅在 D3 后端失败时启用着色器转储
- **性能**：对 Vulkan 后端进行多项优化，以减少提交渲染通道时的开销，特别是对于移动 GPU

## Impact Summary / 影响摘要

Chrome 140's WebGPU updates focus on:

Chrome 140 的 WebGPU 更新专注于：

1. **Specification Compliance**: Enforcing adapter consumption rules and removing deprecated attributes
2. **Developer Experience**: Simplifying texture usage patterns and expanding WGSL capabilities  
3. **Performance**: Optimizing Dawn backend, especially for mobile GPUs
4. **API Cleanup**: Removing deprecated features and updating function signatures

1. **规范合规性**：执行适配器消耗规则并删除已弃用的属性
2. **开发者体验**：简化纹理使用模式并扩展 WGSL 功能
3. **性能**：优化 Dawn 后端，特别是为移动 GPU
4. **API 清理**：删除已弃用的功能并更新函数签名

---

*Generated on September 20, 2025 | 生成于 2025年9月20日*