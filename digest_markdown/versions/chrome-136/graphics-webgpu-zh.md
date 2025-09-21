---
layout: default
title: Chrome 136 图形和 WebGPU 更新
---

# Chrome 136 图形和 WebGPU 更新

## 区域摘要

Chrome 136 为 WebGPU 带来了重大增强，专注于开发者体验、性能优化和用户可访问性。最具影响力的更改包括引入 `isFallbackAdapter` 属性以更好地检测 GPU 适配器，通过 Tint 的新中间表示在 Windows 上大幅改善着色器编译，以及用户能够通过上下文菜单直接保存 WebGPU 画布内容。这些更新共同推进了 Web 平台的发展，使 WebGPU 对库开发者更加可预测，对 Windows 用户更加快速，对内容创作工作流程更加用户友好。

## 详细更新

基于之前 WebGPU 版本的基础，Chrome 136 提供了面向开发者的 API 改进和幕后性能增强，巩固了 WebGPU 作为 Web 顶级图形 API 的地位。

### GPUAdapterInfo isFallbackAdapter 属性

#### 新增功能
`GPUAdapterInfo` 接口现在包含一个布尔型 `isFallbackAdapter` 属性，用于指示 GPU 适配器是否为了更广泛的兼容性、更可预测的行为或改善的隐私性而在性能上有显著限制。

#### 技术细节
该属性帮助开发者和库识别何时使用的是可能无法提供最佳性能的回退适配器。此添加解决了接受用户提供的 `GPUDevice` 对象的库的关键需求，这些库需要对功能使用和性能预期做出明智决策。

#### 使用场景
WebGPU 库现在可以程序性地检测回退适配器并相应调整其行为，可能选择不同的渲染路径或警告用户性能影响。这对需要平衡兼容性与性能的图形密集型应用程序特别有价值。

#### 参考资料
- [issue 403172841](https://issues.chromium.org/issues/403172841)
- [intent to ship](https://groups.google.com/a/chromium.org/g/blink-dev/c/VUkzIOWd2n0)

### D3D12 上的着色器编译时间改进

#### 新增功能
Chrome 的 WebGPU 实现现在通过增强 Tint 着色器编译器，在使用 D3D12 后端的 Windows 系统上具有显著的着色器编译性能改进。

#### 技术细节
改进来自于为 Tint 添加中间表示（IR），位于抽象语法树（AST）和 HLSL 后端写入器之间。这个新的 IR 层使编译器架构更加高效，并为未来版本中的额外优化开辟了机会。

#### 使用场景
在 Windows 上构建 WebGPU 应用程序的开发者将体验到更快的着色器编译时间，从而减少加载时间并提供更流畅的开发工作流程。这对具有复杂着色器程序或在运行时编译着色器的应用程序特别有益。

#### 参考资料
- [issue 42251045](https://issues.chromium.org/issues/42251045)

### 解除兼容模式限制

#### 新增功能
实验性的 `"core-features-and-limits"` 功能允许开发者在启用不安全 WebGPU 标志时解除所有 WebGPU 兼容模式限制，提供对完整 WebGPU 功能和限制范围的访问。

#### 技术细节
当启用 `chrome://flags/#enable-unsafe-webgpu` 标志且实验性功能在 `GPUDevice` 上可用时，开发者可以绕过兼容模式通常施加的限制。此实验性功能专为需要最大 WebGPU 能力的测试和开发场景而设计。

#### 使用场景
此功能主要面向高级开发者和研究人员，他们需要访问前沿的 WebGPU 功能进行测试、原型设计或推动基于 Web 的图形可能性边界。对于想要利用最新 GPU 能力而无需等待完整规范稳定化的应用程序特别有用。

#### 参考资料
- [issue 395855517](https://issues.chromium.org/issues/395855517)
- [WebGPU compatibility mode](https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md)
- [issue 395855516](https://issues.chromium.org/issues/395855516)

### Dawn 更新

#### 新增功能
Dawn WebGPU 实现接收回调状态处理的更新，`InstanceDropped` 枚举值被重命名为 `CallbackCancelled` 以提高清晰度。

#### 技术细节
回调状态枚举更改阐明了当回调被取消时，与事件相关的任何后台处理（如管线编译）可能仍会继续。此命名更改更好地反映了实际行为，并帮助开发者理解回调取消的影响。

#### 使用场景
使用异步 WebGPU 操作的开发者将从更清晰的文档和处理回调取消时更可预测的行为中受益。这对管理复杂异步工作流程或需要优雅处理清理场景的应用程序特别重要。

#### 参考资料
- [callback status](https://webgpu-native.github.io/webgpu-headers/Asynchronous-Operations.html#CallbackStatuses)
- [issue 520](https://github.com/webgpu-native/webgpu-headers/issues/520)
- [issue 369](https://github.com/webgpu-native/webgpu-headers/issues/369)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7049..chromium/7103?n=1000)

### 保存和复制画布图像

#### 新增功能
Chrome 用户现在可以右键点击 WebGPU 画布元素来访问标准上下文菜单选项，包括"图片另存为..."和"复制图片"，使 WebGPU 画布与传统 Web 内容保持一致。

#### 技术细节
此功能将标准浏览器上下文菜单功能扩展到 WebGPU 画布元素，允许用户使用熟悉的浏览器模式与 GPU 渲染的内容交互。该实现确保复杂的 GPU 渲染场景可以像任何其他 Web 图像一样被捕获和保存。

#### 使用场景
此增强显著改善了 WebGPU 应用程序的用户体验，特别是那些专注于内容创作、数据可视化或艺术表达的应用程序。用户现在可以轻松保存 3D 场景截图、分享可视化内容或收集参考图像，而无需专门的应用程序功能。

#### 参考资料
- [issue 40902474](https://issues.chromium.org/issues/40902474)