---
layout: default
title: graphics-webgpu-zh
---

## 领域摘要

Chrome 140 (stable) 继续使 WebGPU 和 WGSL 的行为与不断演进的 GPUWeb 规范和 Dawn 运行时对齐，重点是更严格的规范一致性、API 清理和着色器使用便利性。对开发者影响最大的更改包括 adapter 对 requestDevice() 的消费语义、在此前需要 GPUTextureView 的位置接受 GPUTexture 的简写、WGSL 支持使用 textureSampleLevel() 对 1D 纹理采样，以及对不可移植或冗余 API 的弃用/移除。这些更改提升了跨实现的 GPU 代码可移植性和可预测性、减少样板代码，并要求现有应用做少量迁移或校验工作。

## 详细更新

下面是 Chrome 140 中每项 Graphics and WebGPU 更新的简洁、面向开发者的分解。

### Device requests consume adapter（适配器被消耗）

#### 新增内容
在成功的 requestDevice() 调用之后，adapter 会被标记为“已消耗”；对同一 adapter 进行的后续 requestDevice() 调用将被拒绝。

#### 技术细节
这强制实施了 WebGPU 规范中针对 DOM adapter 的状态机：一旦 adapter 产生了 device，该 adapter 即被视为已消耗，不能再产生额外的 device。实现会拒绝对该 adapter 的后续 requestDevice() 返回的 promise。

#### 适用场景
- 防止意外地从同一 adapter 分配多个 device。
- 需要以前依赖对同一 adapter 重复调用 requestDevice() 的应用改为创建新的 adapter 或重新设计初始化流程。

#### 参考资料
- [WebGPU 规范](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1)
- [issue 415825174](https://issues.chromium.org/issues/415825174)

### Shorthand for using texture where texture view is used（在需要 texture view 的位置使用 texture 的简写）

#### 新增内容
可以直接将 GPUTexture 用作 GPUBindingResource，以及在此前需要 GPUTextureView 的位置（例如 render pass color attachment view）直接使用。

#### 技术细节
接收 GPUBindingResource 的 API 或类型为 GPUTextureView 的字段现在也接受 GPUTexture 对象作为简写。平台会执行等效的隐式 view 处理，因此开发者可以直接传入 texture。

#### 适用场景
- 在默认纹理视图已足够的常见模式下减少样板代码。
- 简化构造 pass 和 binding 描述符的代码路径。

#### 参考资料
- [GPUTexture](https://gpuweb.github.io/gpuweb/#gputexture)
- [GPUBindingResource](https://gpuweb.github.io/gpuweb/#typedefdef-gpubindingresource)
- [GPUTextureView](https://gpuweb.github.io/gpuweb/#dictdef-gpubufferbinding)
- [issue 425906323](https://issues.chromium.org/issues/425906323)

### WGSL textureSampleLevel supports 1D textures（支持对 1D 纹理采样）

#### 新增内容
WGSL 的 textureSampleLevel() 现在可以对 1D 纹理进行采样，使得在顶点着色器中对 1D 纹理的采样类似于对 2D 纹理的采样成为可能。

#### 技术细节
WGSL 内置的 textureSampleLevel() 已扩展为接受 1D 纹理类型，因此允许在顶点阶段对 1D 纹理进行采样，并采用与 2D 采样相同的语义。

#### 适用场景
- 允许在顶点着色器中使用 1D 纹理进行程序化或曲线采样。
- 在 1D 和 2D 纹理之间实现一致的着色器代码路径，而无需对采样函数进行特殊处理。

#### 参考资料
- [sampled](https://gpuweb.github.io/gpuweb/wgsl/#texturesamplelevel)
- [issue 382514673](https://issues.chromium.org/issues/382514673)

### Deprecate bgra8unorm read-only storage texture usage（弃用将 bgra8unorm 用作只读存储纹理的用法）

#### 新增内容
将 "bgra8unorm" 与只读存储纹理一同使用已被弃用；此前 Chrome 允许这种用法，但 WebGPU 规范禁止此类用法。

#### 技术细节
"bgra8unorm" 旨在用于只写存储使用，并不适合用于只读存储，因此在可移植性方面不可保证。Chrome 之前的允许行为正在被移除，以符合规范并避免不可移植的行为。

#### 适用场景
- 开发者必须避免依赖对 bgra8unorm 纹理的只读存储访问，并迁移到受支持的格式或使用模式以保证可移植性。

#### 参考资料
- [issue 427681156](https://issues.chromium.org/issues/427681156)

### Remove GPUAdapter isFallbackAdapter attribute（移除 GPUAdapter 的 isFallbackAdapter 属性）

#### 新增内容
已移除 GPUAdapter.isFallbackAdapter；请改用在 Chrome 136 中引入的 GPUAdapterInfo.isFallbackAdapter。

#### 技术细节
adapter 级别的布尔值已被弃用并移除，转而在 GPUAdapterInfo 上使用 isFallbackAdapter 标志，以整合 device/adapter 元数据并减少冗余。

#### 适用场景
- 迁移：将 adapter.isFallbackAdapter 的用法替换为 adapter.requestAdapterInfo().isFallbackAdapter 或等价的 GPUAdapterInfo 访问方式。

#### 参考资料
- [intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/Wzr22XXV3s8)

### Dawn updates（Dawn 更新）

#### 新增内容
Dawn 的更改包括 API 清理，例如 wgpuInstanceGetWGSLLanguageFeatures() 不再返回 WGPUStatus（因为它不会失败），以及列入 Chromium 的多个内部修复和提交。

#### 技术细节
- wgpuInstanceGetWGSLLanguageFeatures() 现在通过 out-参数返回，不再使用状态码。
- 其他 Dawn 更改包括调试文档、帧缓冲区缓存以及一系列用于 Chromium 的提交。

#### 适用场景
- 原生嵌入者和引擎维护者应更新对已修改 Dawn API 的调用。
- 有助于减少对保证成功的函数的错误处理噪音。

#### 参考资料
- [issue 429178774](https://issues.chromium.org/issues/429178774)
- [issue 425930323](https://issues.chromium.org/issues/425930323)
- [issue 415825174](https://issues.chromium.org/issues/415825174)
- [调试文档](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/debugging.md)
- [issue 429187478](http://issues.chromium.org/issues/429187478)
- [caching VkFramebuffers](https://dawn.googlesource.com/dawn/+/ddf2e1f61d20171ecd10ae3be70acb750a56686d)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7258..chromium/7339?n=1000)
