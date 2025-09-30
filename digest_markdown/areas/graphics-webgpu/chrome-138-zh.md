---
layout: default
title: chrome-138-zh
---

## 领域摘要

Chrome 138（stable）继续改进 WebGPU 在图形工作负载方面的人机工程、正确性和平台自省。显著主题包括 API 简化（绑定资源）、更严格的安全/验证（mappedAtCreation 大小对齐）、扩展的 GPU 架构报告、弃用整合，以及上游工具链（Dawn/emscripten）改进。这些更改减少了开发者摩擦，暴露更准确的硬件能力，并收紧运行时保证——帮助开发者编写更快、更可移植且更安全的 GPU 加速 Web 应用。以下细节突出了针对 WebGPU 的实际影响和迁移注意事项。

## 详细更新

下面的条目扩展了摘要内容，并说明每项更改如何影响实现、测试和部署。

### Shorthand for Using Buffer as a Binding Resource（将 Buffer 用作绑定资源的简写）

#### 新增内容
开发者现在可以直接提供一个 GPUBuffer 作为 GPUBindingResource，从而简化 bind group 构建并使 buffer 的使用与其他资源类型保持一致。

#### 技术细节
此更改消除了在将缓冲区绑定到着色器阶段时需要额外包装对象的需求；运行时在期望 GPUBindingResource 的地方接受 GPUBuffer 实例。

#### 适用场景
- 为 uniform/storage buffers 提供更清晰的 bind group 创建代码。
- 将本地 GPU 代码模式移植到 WebGPU 时减少样板代码。

#### 参考资料
未提供。

### Size Requirement Changes for Buffers Mapped at Creation（创建时映射的缓冲区的大小要求更改）

#### 新增内容
使用 `mappedAtCreation: true` 创建缓冲区现在如果 `size` 不是 4 的倍数会抛出 RangeError。

#### 技术细节
在使用 `mappedAtCreation` 时，缓冲区分配路径会在创建时验证大小对齐。未对齐的大小（例如 42）现在会立即导致 RangeError，而不是创建带有隐式填充行为的缓冲区。

#### 适用场景
- 防止在将类型化数组视图写入映射缓冲区时出现微妙的数据损坏或运行时不匹配。
- 强制代码生成器和绑定在显式处理对齐（这对模糊测试和自动化构建系统很重要）。

#### 参考资料
```javascript
myDevice.createBuffer({
  mappedAtCreation: true,
  size: 42, // This will now throw a RangeError
  usage: GPUBufferUsage.STORAGE,
});
```

### Architecture Report for Recent GPUs（近期 GPU 的架构报告）

#### 新增内容
Chrome 现在报告新的 GPU 架构标识符：
- Nvidia: "blackwell"
- AMD: "rdna4"

#### 技术细节
这些标识符出现在 GPU adapter 报告表面，提升了 GPU 能力检测的细粒度，并使更精细的功能分流或遥测成为可能。

#### 适用场景
- 基于精确 GPU 架构的自适应渲染路径或着色器调优。
- 针对新 GPU 家族生成优化着色器变体的分析和构建流水线。

#### 参考资料
未提供。

### Deprecation of GPUAdapter isFallbackAdapter Attribute（弃用 GPUAdapter isFallbackAdapter 属性）

#### 新增内容
GPUAdapter.isFallbackAdapter 属性被弃用；应迁移到 GPUAdapterInfo.isFallbackAdapter（已在 Chrome 136 引入）。

#### 技术细节
适配器的 fallback 状态已移入 GPUAdapterInfo 结构以集中适配器元数据。现有读取 GPUAdapter.isFallbackAdapter 的代码应更新为调用 adapter.requestAdapter() 并在可用时检查 adapter.adapterInfo.isFallbackAdapter。

#### 适用场景
- 在设备选择代码和功能分流中更新适配器检测逻辑。
- 通过迁移到 GPUAdapterInfo 属性确保未来兼容的代码。

#### 参考资料
未提供。

### Dawn Updates（Dawn 更新）

#### 新增内容
包含在 Chrome 138 中的 Dawn 与 Emscripten 工具链改进：
- Emscripten 现在在 CMake 构建中支持 Dawn GLFW。
- 在包发行中包含了一个“remote” Emdawnwebgpu 端口。
- 从 `emcc -sUSE_WEBGPU` 切换到 Emdawnwebgpu 只需一个标志改动：`emcc --use-port=emdawnwebgpu`。

#### 技术细节
这些更新简化了面向 Dawn 实现目标的本地 C/C++ 项目的构建和测试，并为使用 Emscripten 的项目提供了更简单的端口迁移路径。

#### 适用场景
- 使用 Dawn 通过 WebAssembly 目标的应用在本地开发和 CI 构建中更容易。
- 简化将本地工具链和示例移植到浏览器或远程/WebDriver 类环境的过程。

#### 参考资料
未提供。

---
已保存摘要的文件路径:
digest_markdown/webplatform/Graphics and WebGPU/chrome-138-stable-en.md
