区域摘要

Chrome 138 Stable 在图形和 WebGPU 方面的重点是整理 WebGPU API（尤其是弃用）、改善开发者易用性以及提高平台精确性。本次发布移除了冗余的 adapter 属性，新增了直接绑定 GPUBuffer 的简写，并在创建时映射（mapped-at-creation）的缓冲区上收紧了大小校验。附加更新包括新的 GPU 架构标识以及针对 Dawn/Emdawnwebgpu 的工具改进，这些有助于通过 Emscripten 实现类原生构建。这些更改提升了安全性、功能检测准确性和开发工作流程的可移植性，因此团队应审查代码以应对弃用，并调整缓冲区分配与绑定方式。

## 详细更新

下面条目扩展了上述摘要，并展示了对图形和 WebGPU 工作的实际影响。

### WebGPU: Deprecate GPUAdapter isFallbackAdapter attribute（弃用 GPUAdapter.isFallbackAdapter 属性）

#### 新增内容
`GPUAdapter.isFallbackAdapter` boolean 属性已被弃用，改为使用 `GPUAdapterInfo.isFallbackAdapter`，以消除冗余。

#### 技术细节
移除该属性使 API 表面与规范中的 GPU adapter info 对象模型保持一致。对于直接从 `GPUAdapter` 读取该属性的代码，这是一个小的破坏性更改。

#### 适用场景
- 代码迁移：在适用处调用 `adapter.requestAdapterInfo()` 或使用 `adapterInfo.isFallbackAdapter`。
- 功能检测：使用 `GPUAdapterInfo` 进行回退检测，而不是依赖 adapter 级别的字段。

#### 参考资料
https://bugs.chromium.org/p/chromium/issues/detail?id=409259074
https://chromestatus.com/feature/5125671816847360
https://gpuweb.github.io/gpuweb/#gpu-adapter

### Shorthand for Using Buffer as a Binding Resource（将 Buffer 作为绑定资源的简写）

#### 新增内容
在创建绑定组时，现在可以直接将 `GPUBuffer` 用作 `GPUBindingResource`。

#### 技术细节
绑定组条目现在直接接受 `GPUBuffer` 实例，常见情况下不再需要将其包裹到 `GPUBufferBinding` 对象中。

#### 适用场景
- 简化 uniform/storage 缓冲区的着色器资源设置。
- 减少 JS 绑定代码的样板，并使缓冲区绑定与其他资源简写保持一致。

#### 参考资料
无

### Size Requirement Changes for Buffers Mapped at Creation（创建时映射缓冲区的大小要求更改）

#### 新增内容
当使用 `mappedAtCreation: true` 创建缓冲区时，如果 `size` 不是 4 的倍数，现在会抛出 `RangeError`。

#### 技术细节
后端和 WebGPU 规范要求映射的缓冲视图遵守 4 字节对齐；Chrome 现在在创建时强制执行此要求，以防止细微的内存布局问题。

#### 适用场景
- 在为类型数组视图映射缓冲区时防止未定义行为。
- 开发者应将缓冲区大小对齐到 4 字节；在必要时调整分配并添加填充。

#### 示例
```javascript
// javascript
// Now throws RangeError if size is not multiple of 4
myDevice.createBuffer({
  mappedAtCreation: true,
  size: 42, // will now throw
  usage: GPUBufferUsage.STORAGE,
});
```

#### 参考资料
无

### Architecture Report for Recent GPUs（近期 GPU 架构报告）

#### 新增内容
Chrome 报告了新的 GPU 架构标识：
- Nvidia: "blackwell"
- AMD: "rdna4"

#### 技术细节
这些字符串出现在适配器/驱动报告中，可用于更细粒度的供应商与代数级平台/功能检测。

#### 适用场景
- 运行时功能开关或规避措施可以针对特定架构。
- 遥测和诊断在性能调优方面获得更细粒度的信息。

#### 参考资料
无

### Deprecation of GPUAdapter isFallbackAdapter Attribute（GPUAdapter.isFallbackAdapter 属性的弃用）

#### 新增内容
再次提醒弃用：`GPUAdapter.isFallbackAdapter` 已弃用，并由 `GPUAdapterInfo.isFallbackAdapter` 取代（该字段在 Chrome 136 中引入）。

#### 技术细节
强化了迁移路径：迁移到集中管理适配器元数据的 adapter info 对象。

#### 适用场景
- 审核现有检查适配器属性的代码路径，并更新为使用 `GPUAdapterInfo`。

#### 参考资料
无

### Dawn Updates（Dawn 更新）

#### 新增内容
Dawn 构建和分发增强：
- Emscripten 在 CMake 构建中支持 Dawn GLFW。
- 包发布中包含了一个 “remote” Emdawnwebgpu 端口。
- 切换到 Emdawnwebgpu 现在只需将 `emcc -sUSE_WEBGPU` 改为 `emcc --use-port=emdawnwebgpu` 这一标志切换。

#### 技术细节
这些更新简化了通过 Emscripten 进行类原生风格的 WebGPU 应用构建，并简化了针对 WebAssembly/WebGPU 目标的端口切换。

#### 适用场景
- 使用 Dawn 的 WebAssembly 开发者可以更容易地使用 GLFW 和 emdawnwebgpu 端口进行构建/测试。
- CI 与本地构建可以只通过更改单个 emcc 标志来切换端口。

#### 示例
```bash
# shell
# Switch to the emdawnwebgpu port
emcc --use-port=emdawnwebgpu
```

#### 参考资料
无

已保存至: digest_markdown/webplatform/Graphics and WebGPU/chrome-138-stable-en.md