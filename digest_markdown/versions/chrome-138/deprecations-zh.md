---
layout: default
title: deprecations-zh
---

## 领域摘要

Chrome 138 弃用 WebGPU API 属性 `GPUAdapter.isFallbackAdapter`，将回退信息合并到 `GPUAdapterInfo.isFallbackAdapter`。这减少了平台 WebGPU 表面的冗余，并要求对检查旧属性的代码进行少量迁移更新。对于开发者，最重要的变化是将运行时检查和测试从引用 `GPUAdapter` 更新为引用 `GPUAdapterInfo`。这精简了 WebGPU API 表面并减少了平台的维护面。

## 详细更新

以下是与 WebGPU 相关的 Chrome 138 弃用条目及团队接下来的建议。

### WebGPU: Deprecate GPUAdapter isFallbackAdapter attribute (弃用 GPUAdapter.isFallbackAdapter 属性)

#### 新增内容
`GPUAdapter.isFallbackAdapter` 布尔属性已被弃用，因为它与 `GPUAdapterInfo.isFallbackAdapter` 属性重复。

#### 技术细节
该属性将在未来的更改中移除；代码不应依赖 `GPUAdapter.isFallbackAdapter`。相反，应从适配器信息结构暴露的 `GPUAdapterInfo.isFallbackAdapter` 获取回退信息。

#### 适用场景
- 将功能检测和运行时检查更新为读取 `GPUAdapterInfo.isFallbackAdapter`。
- 调整断言 `GPUAdapter.isFallbackAdapter` 的单元和集成测试。
- 审计在回退适配器上分支的代码路径（例如能力变通）并将其迁移为使用适配器信息。

#### 参考资料
- 跟踪 bug #409259074: https://bugs.chromium.org/p/chromium/issues/detail?id=409259074
- ChromeStatus.com 条目: https://chromestatus.com/feature/5125671816847360
- 规范: https://gpuweb.github.io/gpuweb/#gpu-adapter
