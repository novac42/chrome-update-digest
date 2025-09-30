---
layout: default
title: deprecation-zh
---

### 1. 区域摘要

Chrome 138 的弃用集中在通过移除冗余属性来简化 WebGPU API 表面。最重要的更改是弃用 `GPUAdapter.isFallbackAdapter` 属性，转而使用在 Chrome 136 中引入的 `GPUAdapterInfo.isFallbackAdapter`，这对 WebGPU 使用者来说是一个小的破坏性更改。此举减少了 API 的重复并明确了适配器元数据的归属，有助于可移植性和规范一致性。使用 WebGPU 的开发者应将检查迁移到 `GPUAdapterInfo`，以避免将来的中断。

## 详细更新

下面是与 WebGPU 相关并在 Chrome 138 中弃用的项目及迁移指导。

### WebGPU: Deprecate GPUAdapter isFallbackAdapter attribute（弃用 GPUAdapter isFallbackAdapter 属性）

#### 新增内容
弃用 `GPUAdapter` 的 `isFallbackAdapter` 布尔属性，因为它与 `GPUAdapterInfo.isFallbackAdapter` 冗余。

#### 技术细节
此属性移除是一次有意的 API 简化：适配器的回退信息已集中到 `GPUAdapterInfo` 中。对于读取 `GPUAdapter.isFallbackAdapter` 的代码来说，此变更是一个小的破坏性更改。

#### 适用场景
更新检查适配器回退状态的 WebGPU 代码，使用 `GPUAdapter.requestAdapter()` → 检查 `adapter.adapterInfo.isFallbackAdapter`（或等效的 `GPUAdapterInfo` 接口）以保持兼容性。

#### 参考资料
https://bugs.chromium.org/p/chromium/issues/detail?id=409259074
https://chromestatus.com/feature/5125671816847360
https://gpuweb.github.io/gpuweb/#gpu-adapter

### Deprecation of GPUAdapter isFallbackAdapter Attribute（弃用 GPUAdapter isFallbackAdapter 属性）

#### 新增内容
`GPUAdapter` 的 `isFallbackAdapter` 属性被弃用，并被在 Chrome 136 中引入的 `GPUAdapterInfo.isFallbackAdapter` 所取代。

#### 技术细节
此弃用将开发者引导至 `GPUAdapterInfo` 属性，作为适配器回退元数据的规范来源，从而整合适配器元数据。

#### 适用场景
将任何对 `GPUAdapter.isFallbackAdapter` 的直接读取迁移到 `GPUAdapterInfo.isFallbackAdapter` 字段，以避免将来的不兼容。

#### 参考资料
未提供。

保存到文件：
```text
digest_markdown/webplatform/deprecation/chrome-138-stable-en.md
