---
layout: default
title: 区域摘要
---

# 区域摘要

Chrome 140 在 Graphics 和 WebGPU 方面的更新侧重于加强对 WebGPU 规范的一致性、改进 WGSL 的一致性，以及清理遗留或不正确的 API 表面。对开发者影响最大的更改包括适配器生命周期语义（已消耗的 adapters）、纹理的简写和采样器行为（包括 WGSL 中对 1D 支持），以及影响可移植性和迁移的弃用/移除（如 bgra8unorm 作为 storage 的使用和 isFallbackAdapter）。这些更新通过减少实现不一致、提高着色器表达能力并移除不可移植或冗余的 API 元素，推动了 Web 平台的发展——降低了跨平台 GPU 代码和工具链的风险。团队应评估设备/适配器生命周期在资源管理中的影响，调整着色器和绑定代码以适应简写和 1D 采样，并遵循弃用/迁移指导以避免运行时失败。

## 详细更新

下面列出 Chrome 140 中 Graphics 和 WebGPU 的变更，包含简明的技术说明和以开发者为中心的使用场景。

### Device requests consume adapter（设备请求将消耗 adapter）

#### 新增内容
在成功请求设备后，适配器现在会被标记为“已消耗”。对同一适配器的后续 `requestDevice()` 调用将会被拒绝。

#### 技术细节
此行为使 Chrome 与 WebGPU 规范一致：创建 GPUDevice 后，适配器的状态变为已消耗。对同一适配器再次请求设备不再被允许，并会导致返回被拒绝的 promise。

#### 适用场景
- 更新在应用和引擎中对 adapter/device 生命周期的处理，避免从同一适配器创建多个设备的模式。
- 在创建设备时确保进行资源分配和清理，避免假设可以为同一适配器复用多个设备的用法。

#### 参考资料
- [WebGPU 规范](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1)  
- [issue 415825174](https://issues.chromium.org/issues/415825174)

### Shorthand for using texture where texture view is used（在需要 texture view 的地方使用 texture 的简写）

#### 新增内容
`GPUTexture` 现在可以直接用作 `GPUBindingResource`，并可用于此前需要 `GPUTextureView` 的位置（例如渲染通道颜色附件的 `view`）。

#### 技术细节
该简写通过允许纹理在绑定和附件点被隐式视为纹理视图，减少样板代码，符合规范中接受 `GPUTexture` 在这些角色中的更新。

#### 适用场景
- 在常见情况下，通过省略显式的纹理视图创建来简化绑定/组设置和渲染通道创建代码。
- 在频繁创建一次性视图的引擎中减少代码路径和分配。

#### 参考资料
- [GPUTexture](https://gpuweb.github.io/gpuweb/#gputexture)  
- [GPUBindingResource](https://gpuweb.github.io/gpuweb/#typedefdef-gpubindingresource)  
- [GPUTextureView](https://gpuweb.github.io/gpuweb/#dictdef-gpubufferbinding)  
- [issue 425906323](https://issues.chromium.org/issues/425906323)

### WGSL textureSampleLevel supports 1D textures（WGSL 的 textureSampleLevel 支持 1D 纹理）

#### 新增内容
`textureSampleLevel()` 现在支持对 1D 纹理的采样，使其在着色器（包括顶点着色器）中的使用方式与 2D 纹理相同。

#### 技术细节
此更改使 1D 纹理在 `textureSampleLevel` 内与 2D 达到一致，允许在之前受限的采样行为之外，从着色器阶段显式调用 LOD 采样。

#### 适用场景
- 在顶点或计算着色器中对 1D 纹理进行显式 LOD 采样，用于程序化或基于曲线的查找。
- 将依赖于仅片段采样模式的着色器代码移植到更早的管线阶段。

#### 参考资料
- [sampled](https://gpuweb.github.io/gpuweb/wgsl/#texturesamplelevel)  
- [issue 382514673](https://issues.chromium.org/issues/382514673)

### Deprecate bgra8unorm read-only storage texture usage（弃用将 bgra8unorm 用作只读 storage texture 的用法）

#### 新增内容
将 "bgra8unorm" 格式用作只读 storage 纹理的用法已被弃用；此前 Chrome 中允许该用法是一个 bug。

#### 技术细节
WebGPU 规范不允许对该格式进行只读 storage 访问，因为它旨在用于写入且不可移植。Chrome 现已弃用此前允许的该用法，以趋向于符合规范的行为。

#### 适用场景
- 审计将 bgra8unorm 绑定为只读 storage 的代码，并迁移到可移植的格式或访问模式。
- 优先使用明确允许作为只读 storage 的格式，以保证跨浏览器的可移植性和正确行为。

#### 参考资料
- [issue 427681156](https://issues.chromium.org/issues/427681156)

### Remove GPUAdapter isFallbackAdapter attribute（移除 GPUAdapter 的 isFallbackAdapter 属性）

#### 新增内容
GPUAdapter 的 `isFallbackAdapter` 属性已被移除；该属性已迁移到 `GPUAdapterInfo` 并在之前引入。

#### 技术细节
此举完成了此前宣布的弃用/移除，将回退信息集中到 `GPUAdapterInfo`（在 Chrome 136 中添加），从 GPUAdapter 中移除了冗余信息。

#### 适用场景
- 更新适配器检测逻辑，从 `GPUAdapterInfo` 而非 `GPUAdapter` 读取 `isFallbackAdapter`。
- 在引擎/平台检测层移除针对 GPUAdapter 属性的回退相关检测。

#### 参考资料
- [intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/Wzr22XXV3s8)

### Dawn updates（Dawn 更新）

#### 新增内容
Dawn 的 `wgpuInstanceGetWGSLLanguageFeatures()` 不再返回 `WGPUStatus` 值，因为它不会失败；其他内部更改包括若干 bug 修复和调试改进。

#### 技术细节
API 简化以移除不必要的状态返回。Dawn 更新还包括如缓存 VkFramebuffers 和调试文档/提交中的若干更改，详见链接资源。

#### 适用场景
- 使用 Dawn 的原生工具和嵌入者应更新调用点以匹配新签名。
- 审阅 Dawn 的变更日志，留意可能影响 GPU 行为和资源缓存的性能与后端修复。

#### 参考资料
- [issue 429178774](https://issues.chromium.org/issues/429178774)  
- [issue 425930323](https://issues.chromium.org/issues/425930323)  
- [issue 415825174](https://issues.chromium.org/issues/415825174)  
- [调试用途](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/debugging.md)  
- [issue 429187478](http://issues.chromium.org/issues/429187478)  
- [缓存 VkFramebuffers](https://dawn.googlesource.com/dawn/+/ddf2e1f61d20171ecd10ae3be70acb750a56686d)  
- [提交列表](https://dawn.googlesource.com/dawn/+log/chromium/7258..chromium/7339?n=1000)

已保存到：digest_markdown/webplatform/Graphics and WebGPU/chrome-140-stable-en.md
