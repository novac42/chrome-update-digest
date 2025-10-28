---
layout: default
title: graphics-webgpu-zh
---

## 领域摘要

Chrome 141 的 Graphics 和 WebGPU 更新围绕编译器/工具链的成熟度以及后端能力升级展开。关键主题包括完成一次重要的 Tint IR 重构、在 WGSL 编译器中逐步推出整数范围分析、在可用的平台上为 Vulkan 后端提供 SPIR-V 1.4 支持，以及上游 WebGPU C API 头文件的稳定化。这些更改主要提升着色器编译效率，启用更强的代码生成路径，并为原生集成提供更高的 API 稳定性。总体上，它们强化了 WebGPU 生态，并推动 Web 上可预测且高性能的图形与计算。

## 详细更新

基于上述主题，以下功能突出展示了开发者在 Chrome 141 中可以利用的具体改进。

### Tint IR completed（Tint IR 完成）

#### 新增内容
经过多年的工作，在 WGSL 编译器 Tint 内部新增了一个位于 AST 与后端代码生成器之间的中间表示（IR），以提升内部性能。

#### 技术细节
- 该 IR 位于现有 AST 与后端代码生成阶段之间。
- 这一架构层使着色器编译过程中的内部变换与优化更高效。

#### 适用场景
- 为复杂的 WGSL 代码库提供更快且更具可扩展性的着色器编译管线。
- 为未来的编译器优化与后端改进奠定基础，而无需更改 WGSL 源代码。

#### 参考资料


### Integer range analysis in WGSL compiler（WGSL 编译器中的整数范围分析）

#### 新增内容
Chrome 正在逐步在 Tint 中推出整数范围分析，以在不执行程序的情况下估计整数变量可能取值的最小和最大范围。

#### 技术细节
- 静态分析过程会在各程序路径上推断整数取值边界。
- 这些结果可用于在编译器管线中做出更安全、更高效的代码生成决策。

#### 适用场景
- 对于大量使用整数控制流或索引的着色器，可进行更有根据的优化。
- 在已证明取值范围的情况下，生成代码有望减少保守性。

#### 参考资料
- [问题 348701956](https://issuetracker.google.com/348701956)

### SPIR-V 1.4 update for Vulkan backend（Vulkan 后端的 SPIR-V 1.4 更新）

#### 新增内容
在可用的 Android 和 ChromeOS 设备上推出 SPIR-V 1.4 支持，使 Tint 能在某些 Vulkan 编译场景下利用更新的 SPIR-V 特性、放宽规则与指令。

#### 技术细节
- 在面向 Vulkan 时，Tint 可生成 SPIR-V 1.4，以利用兼容设备/驱动的能力。
- 更新的指令与放宽规则可带来更高效的着色器代码生成路径。

#### 适用场景
- 在支持 SPIR-V 1.4 的、具备 Vulkan 能力的 Android 与 ChromeOS 设备上改进着色器生成。
- 对可受益于 1.4 特性的着色器，可能获得性能与效率提升。

#### 参考资料
- [问题 427717267](https://issuetracker.google.com/427717267)

### Dawn updates（Dawn 更新）

#### 新增内容
定义核心 WebGPU C API 的标准化头文件 `webgpu.h` 已被认为对上游核心 API 稳定（不包含实现层扩展）。

#### 技术细节
- 稳定性仅适用于上游定义的核心 API 表面。
- 特定实现的扩展不在此稳定性声明的覆盖范围内。

#### 适用场景
- 面向稳定的核心 WebGPU C API 的原生集成与工具将更可预测。
- 通过 `webgpu.h` 绑定 Dawn 的项目将更易维护并提升兼容性。

#### 参考资料
- [`webgpu.h`](https://github.com/webgpu-native/webgpu-headers/blob/main/webgpu.h)
- [file a bug](https://crbug.com/dawn/new)
- [William Candillon](https://github.com/wcandillon)
- [Dawn PR #39](https://github.com/google/dawn/pull/39)
- [示例](https://github.com/google/dawn/actions/runs/17429395587#artifacts)
- [提交列表](https://dawn.googlesource.com/dawn/+log/chromium/7339..chromium/7390?n=1000)
