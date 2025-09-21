# Chrome 140 稳定版 - 图形和 WebGPU 更新分析

## 概述

Chrome 140 为 WebGPU 带来了重大改进，包括增强的纹理处理、适配器消费管理和 WGSL 着色器能力。主要亮点包括简化的纹理使用模式、改进的顶点着色器中 1D 纹理支持，以及与 WebGPU 规范保持一致的重要弃用。此次更新还包括 Dawn 引擎改进并移除了已弃用的适配器属性。

## 功能详情

### Device requests consume adapter

**更改内容**：
WebGPU 适配器现在在成功的设备请求后被正确标记为"已消费"，遵循 WebGPU 规范。一旦适配器被用于创建设备，对同一适配器的任何后续 `requestDevice()` 调用都将被拒绝并返回 promise 拒绝。此更改确保了正确的资源管理，防止从同一适配器创建多个设备，这可能导致未定义行为或资源冲突。

**参考**：
- [WebGPU specification](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1)
- [issue 415825174](https://issues.chromium.org/issues/415825174)

### Shorthand for using texture where texture view is used

**更改内容**：
GPUTexture 对象现在可以直接用作着色器绑定的 GPUBindingResource，在许多常见场景中无需创建显式纹理视图。这适用于渲染通道颜色附件、深度/模板附件和一般绑定操作。此更改通过减少样板纹理视图创建来简化 WebGPU 代码，同时保持与现有显式纹理视图使用模式的完全兼容性。

**参考**：
- [GPUTexture](https://gpuweb.github.io/gpuweb/#gputexture)
- [GPUBindingResource](https://gpuweb.github.io/gpuweb/#typedefdef-gpubindingresource)
- [GPUTextureView](https://gpuweb.github.io/gpuweb/#dictdef-gpubufferbinding)
- [issue 425906323](https://issues.chromium.org/issues/425906323)

### WGSL textureSampleLevel supports 1D textures

**更改内容**：
WGSL 中的 `textureSampleLevel()` 函数现在支持 1D 纹理，与 2D 纹理采样保持一致性。此增强功能允许从顶点着色器采样 1D 纹理，这以前只能在片段着色器中使用 `textureSample()` 实现。此改进扩展了 1D 纹理在图形管线中的使用灵活性，并支持更复杂的顶点着色器技术。

**参考**：
- [sampled](https://gpuweb.github.io/gpuweb/wgsl/#texturesamplelevel)
- [issue 382514673](https://issues.chromium.org/issues/382514673)

### Deprecate bgra8unorm read-only storage texture usage

**更改内容**：
现在弃用将"bgra8unorm"格式与只读存储纹理一起使用。此格式在之前的 Chrome 版本中被错误地允许，但被 WebGPU 规范明确禁止。bgra8unorm 格式设计用于只写访问，在不同图形硬件上缺乏可移植性。开发人员应迁移到适合存储纹理操作的读取兼容格式。

**参考**：
- [issue 427681156](https://issues.chromium.org/issues/427681156)

### Remove GPUAdapter isFallbackAdapter attribute

**更改内容**：
已从 GPUAdapter 对象中移除已弃用的 `isFallbackAdapter` 属性。此属性已被 GPUAdapterInfo 中的 `isFallbackAdapter` 属性替换，该属性在 Chrome 136 中引入。应用程序应更新其代码，通过 `adapter.info.isFallbackAdapter` 访问回退适配器信息，而不是现已移除的直接适配器属性。

**参考**：
- [intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/Wzr22XXV3s8)

### Dawn updates

**更改内容**：
Dawn WebGPU 实现收到了几项重要更新。`wgpuInstanceGetWGSLLanguageFeatures()` 函数不再返回 WGSLStatus 值，因为它不会失败。其他改进包括增强的 Vulkan 帧缓冲区缓存、更好的调试能力和各种性能优化。这些更改提高了 WebGPU 应用程序的底层图形引擎稳定性和性能。

**参考**：
- [issue 429178774](https://issues.chromium.org/issues/429178774)
- [issue 425930323](https://issues.chromium.org/issues/425930323)
- [issue 415825174](https://issues.chromium.org/issues/415825174)
- [debugging purposes](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/debugging.md)
- [issue 429187478](http://issues.chromium.org/issues/429187478)
- [caching VkFramebuffers](https://dawn.googlesource.com/dawn/+/ddf2e1f61d20171ecd10ae3be70acb750a56686d)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7258..chromium/7339?n=1000)