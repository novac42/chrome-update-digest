---
layout: default
title: chrome-138-zh
---

## 领域摘要

Chrome 138（stable）在 WebGPU 方面包含一项重点弃用：移除冗余的 `GPUAdapter.isFallbackAdapter` 属性，转而使用 `GPUAdapterInfo.isFallbackAdapter` 字段。对于直接从 `GPUAdapter` 读取该属性的代码，此更改是一次次要的破坏性更改；开发者应将对该属性的访问迁移到 `GPUAdapterInfo`。合并该 API 可以减少重复、澄清适配器信息模型，从而提升 API 一致性和 WebGPU 实现的长期可维护性。依赖适配器特性检测的团队应更新代码路径和测试，以避免运行时回归。

## 详细更新

下面的单项弃用衍生自上述摘要，并说明技术影响与迁移指导。

### WebGPU: Deprecate GPUAdapter isFallbackAdapter attribute（弃用 GPUAdapter.isFallbackAdapter 属性）

#### 新增内容
`GPUAdapter` 上的布尔属性 `GPUAdapter.isFallbackAdapter` 已被弃用并计划移除，因为相同的布尔值可以通过 `GPUAdapterInfo` 的 `isFallbackAdapter` 获取。

#### 技术细节
- 该属性与 `GPUAdapterInfo.isFallbackAdapter` 冗余。
- 之前读取 `adapter.isFallbackAdapter` 的代码应改为获取 `adapter.adapterInfo`（或等效 API），并从 `GPUAdapterInfo` 结构中读取 `isFallbackAdapter`。
- 这被描述为一次次要的破坏性更改；请在初始化和能力检测路径中更新相关点。

#### 适用场景
- 迁移：将直接读取 `GPUAdapter.isFallbackAdapter` 的操作替换为从 `GPUAdapterInfo.isFallbackAdapter` 读取。
- 测试与特性检测：更新断言适配器属性的单元和集成测试；确保序列化适配器信息的工具使用 `GPUAdapterInfo` 字段。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=409259074
- https://chromestatus.com/feature/5125671816847360
- https://gpuweb.github.io/gpuweb/#gpu-adapter
