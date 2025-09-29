# Chrome 140 Graphics and WebGPU Updates

## Area Summary

Chrome 140 为 WebGPU API 带来了重要改进，专注于规范合规性和开发者体验。最显著的改进包括通过直接使用 GPUTexture 来简化纹理处理、扩展 WGSL 对 1D 纹理的支持能力，以及通过强制适配器消费和格式弃用来更严格地遵循 WebGPU 标准。这些更新整体提升了 GPU 编程工作流程，同时确保了跨不同硬件配置的更好可移植性和一致性。

## Detailed Updates

此版本通过规范对齐和 API 人体工程学改进来强调 WebGPU 的成熟化，使 GPU 编程对 Web 开发者更加直观。

### Device requests consume adapter

#### What's New
WebGPU 适配器现在在成功的设备请求后会被正确标记为"已消费"，防止从同一个适配器实例创建多个设备。

#### Technical Details
遵循 WebGPU 规范，在已消费的适配器上进行任何后续的 `requestDevice()` 调用都将导致 promise 被拒绝。这确保了适当的资源管理，并防止多个上下文尝试使用同一个适配器时可能出现的冲突。

#### Use Cases
通过强制执行单设备每适配器模式来提高应用程序可靠性，并为 GPU 资源分配场景提供更清晰的错误处理。

#### References
- [WebGPU specification](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1)
- [issue 415825174](https://issues.chromium.org/issues/415825174)

### Shorthand for using texture where texture view is used

#### What's New
GPUTexture 对象现在可以直接用作 GPUBindingResource 和渲染通道附件，在许多常见场景中消除了显式创建纹理视图的需求。

#### Technical Details
这种简写允许 GPUTexture 直接用于绑定组、渲染通道颜色附件和深度模板附件中，之前这些地方需要 GPUTextureView。API 会在幕后自动处理视图创建。

#### Use Cases
简化着色器资源绑定代码，减少常见纹理使用模式的样板代码，使 WebGPU 对从其他图形 API 转换的开发者更加友好。

#### References
- [GPUTexture](https://gpuweb.github.io/gpuweb/#gputexture)
- [GPUBindingResource](https://gpuweb.github.io/gpuweb/#typedefdef-gpubindingresource)
- [GPUTextureView](https://gpuweb.github.io/gpuweb/#dictdef-gpubufferbinding)
- [issue 425906323](https://issues.chromium.org/issues/425906323)

### WGSL textureSampleLevel supports 1D textures

#### What's New
WGSL 中的 `textureSampleLevel()` 函数现在支持 1D 纹理，使顶点着色器能够进行细节级别采样。

#### Technical Details
此增强功能与 2D 纹理采样能力保持一致。之前，1D 纹理只能在片段着色器中使用 `textureSample()` 进行采样。现在顶点着色器也可以通过显式细节级别控制来采样 1D 纹理。

#### Use Cases
支持高级顶点着色器技术，如使用 1D 查找纹理的位移映射、使用噪声纹理的程序化动画，以及跨着色器阶段的一致采样模式。

#### References
- [sampled](https://gpuweb.github.io/gpuweb/wgsl/#texturesamplelevel)
- [issue 382514673](https://issues.chromium.org/issues/382514673)

### Deprecate bgra8unorm read-only storage texture usage

#### What's New
`"bgra8unorm"` 格式现在被弃用于只读存储纹理，与 WebGPU 规范要求保持一致。

#### Technical Details
此格式之前在 Chrome 中由于错误而被允许，但 WebGPU 规范明确禁止对 `bgra8unorm` 进行只读存储访问。该格式设计用于只写访问，在不同 GPU 供应商和驱动程序间缺乏可移植性。

#### Use Cases
开发者应该迁移到支持的只读存储纹理格式，如 `rgba8unorm` 或 `rgba8snorm`，以实现跨平台兼容性和规范合规性。

#### References
- [issue 427681156](https://issues.chromium.org/issues/427681156)

### Remove GPUAdapter isFallbackAdapter attribute

#### What's New
已弃用的 `isFallbackAdapter` 属性已从 GPUAdapter 中移除，完成了向 Chrome 136 中引入的 GPUAdapterInfo 的迁移。

#### Technical Details
应用程序现在应该通过 `GPUAdapterInfo.isFallbackAdapter` 属性访问后备适配器信息，而不是已移除的 `GPUAdapter.isFallbackAdapter` 属性。

#### Use Cases
确保一致的适配器信息访问模式，并通过统一的 GPUAdapterInfo 接口支持更详细的适配器能力查询。

#### References
- [intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/Wzr22XXV3s8)

### Dawn updates

#### What's New
多项 Dawn 原生 API 改进，包括 WGSL 语言特性查询更新、增强的 Vulkan 帧缓冲缓存以及各种错误修复。

#### Technical Details
`wgpuInstanceGetWGSLLanguageFeatures()` 函数不再返回状态值，因为它不会失败。Vulkan 后端改进包括更好的帧缓冲缓存以优化性能。其他修复解决了设备创建、调试能力和内存管理问题。

#### Use Cases
原生 WebGPU 应用程序受益于改进的性能、更可靠的设备创建，以及为开发工作流程增强的调试能力。

#### References
- [issue 429178774](https://issues.chromium.org/issues/429178774)
- [issue 425930323](https://issues.chromium.org/issues/425930323)
- [issue 415825174](https://issues.chromium.org/issues/415825174)
- [debugging purposes](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/debugging.md)
- [issue 429187478](http://issues.chromium.org/issues/429187478)
- [caching VkFramebuffers](https://dawn.googlesource.com/dawn/+/ddf2e1f61d20171ecd10ae3be70acb750a56686d)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7258..chromium/7339?n=1000)