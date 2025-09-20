---
layout: default
title: Chrome 140 Release Notes
---

# Chrome 140 Release Notes

[← Back to all versions](../)

## Areas with Updates

- [Graphics & WebGPU](./graphics-webgpu.html)

## Navigation

- [Chrome 139 (Older) →](../chrome-139/)
- [View all versions](../)
- [Browse by feature area](../../areas/)

## Graphics & WebGPU

Below is a focused digest of the WebGPU / graphics-related platform changes in Chrome 140. (Bilingual English / 中文)

### Device Adapter Consumption / 设备适配器消耗

**Device requests consume adapter**  
According to the WebGPU specification, an adapter is marked as "consumed" upon a successful device request. Subsequent `requestDevice()` calls using the same adapter now reject instead of returning an immediately-lost device.

根据 WebGPU 规范，适配器在成功请求设备后会被标记为“已消耗”。对同一适配器的后续 `requestDevice()` 调用现在会直接拒绝，而不是返回一个创建时就已丢失的设备。

```javascript
const adapter = await navigator.gpu.requestAdapter();
const device = await adapter.requestDevice();
await adapter.requestDevice(); // Rejected: adapter already consumed
```

### Texture Usage Simplification / 纹理使用简化

**Use a GPUTexture where a view was required**  
A `GPUTexture` can now be supplied directly as a binding resource or render pass attachment where a `GPUTextureView` was previously required.

现在可以在需要 `GPUTextureView` 的位置直接提供 `GPUTexture`，用于绑定或渲染通道附件。

```javascript
const bindGroup = device.createBindGroup({
  layout: pipeline.getBindGroupLayout(0),
  entries: [
    { binding: 0, resource: sampler },
    { binding: 1, resource: colorTexture }, // implicit .createView()
  ],
});
```

### WGSL Enhancements / WGSL 增强

`textureSampleLevel()` now supports 1D textures, aligning capability parity with 2D texture sampling from additional shader stages.

`textureSampleLevel()` 现在支持 1D 纹理，使其与 2D 纹理的阶段能力保持一致。

### Storage Texture Deprecation / 存储纹理弃用

Read-only storage usage of format `bgra8unorm` is deprecated (previous allowance was a Chrome bug). The format is intended for write-only / non-portable cases.

`bgra8unorm` 作为只读存储纹理的用法已弃用（之前允许是实现缺陷），该格式应视为非可移植、仅写场景。

### Adapter Attribute Removal / 适配器属性移除

`GPUAdapter.isFallbackAdapter` removed in favor of `GPUAdapterInfo.isFallbackAdapter` (introduced earlier for structured querying).

删除 `GPUAdapter.isFallbackAdapter`，使用更结构化的 `GPUAdapterInfo.isFallbackAdapter`。

### Dawn Implementation Updates / Dawn 实现更新

Key internal improvements spanning API cleanup, multi-device support, shader debugging toggles, and Vulkan backend submission efficiency (especially for mobile GPUs).

内部改进：API 精简、多设备支持、着色器调试开关、以及 Vulkan 后端提交效率优化（移动 GPU 受益显著）。

## Impact Summary / 影响摘要

1. Spec compliance (adapter consumption, attribute cleanup)  
2. Ergonomics (direct texture binding shorthand)  
3. Capability parity (1D sampling in `textureSampleLevel`)  
4. Stability & performance (Dawn/Vulkan optimizations)  
5. API hygiene (removals + deprecations)

1. 规范合规（适配器消耗、属性清理）  
2. 易用性（纹理直接绑定简化）  
3. 能力对齐（1D 采样支持）  
4. 稳定与性能（Dawn / Vulkan 优化）  
5. API 卫生（移除与弃用）

---

*Generated on September 20, 2025 | 生成于 2025年9月20日*
