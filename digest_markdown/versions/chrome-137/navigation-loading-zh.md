---
layout: default
title: navigation-loading-zh
---

## 区域摘要

Chrome 137 继续推进 Storage Partitioning 工作，将 Storage Key 分区应用于 Navigation-Loading 领域的 Blob URL 访问。主要更改是按 Storage Key（top-level site、frame origin 和 has-cross-site-ancestor）对 Blob URL 访问进行分区，但明确例外是顶层导航仍仅按 frame origin 分区。此更新主要影响依赖 Blob URL 的跨站嵌入和导航流，收紧隐私边界，同时将顶层导航的破坏降到最低。开发者应评估跨源框架中 Blob URL 的使用，并更新测试以反映新的访问语义。

## 详细更新

This section lists the Navigation-Loading change in Chrome 137 and its developer implications.

### Blob URL Partitioning: Fetching/Navigation（Blob URL 分区：获取/导航）

#### 新增内容
Chrome 按 Storage Key（top-level site、frame origin 和 has-cross-site-ancestor 布尔值）对 Blob URL 访问进行分区，但顶层导航仍然仅按 frame origin 分区。

#### 技术细节
- Blob URL 访问被限定到由 top-level site、frame origin 及该帧是否具有跨站祖先（has-cross-site-ancestor）组成的 Storage Key。
- 存在例外：顶层导航仍仅按 frame origin 分区（而不是完整的 Storage Key）。
- 这使得 Blob URL 的访问控制与更广泛的 Storage Partitioning 模型保持一致，以减少跨站数据暴露。

#### 适用场景
- 防止在一个 Storage Key（例如嵌入的跨站框架）中创建的 Blob URLs 在不同的 Storage Key 中被使用，从而改善隐私边界。
- 通过使顶层导航仅按 frame origin 分区，尽量减少对顶层导航的回归影响。
- 要求开发者审查跨框架的 Blob URL 共享模式并更新依赖全局 Blob URL 可访问性的导航/测试流程。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40057646
- https://chromestatus.com/feature/5037311976488960

## 区域专门知识（Navigation-Loading 的影响）

- css: No direct CSS changes，但当 Blob URL 访问发生变化时，影响滚动/布局的跨源 iframe 行为可能需要重新验证。
- webapi: Blob URL fetch/navigation 语义现在是 Storage Key–scoped；创建或解析 Blob URLs 的 API 必须考虑存储分区边界。
- graphics-webgpu: 用作纹理或着色器的来自 Blob 的资源在跨站帧间可能会因 Storage Key 而不可访问；验证 GPU 渲染管线中的资源加载。
- javascript: 在帧间生成或使用 Blob URL 的 JS 必须处理存储分区访问和回退机制。
- security-privacy: 通过限制跨站 Blob 重用来加强隐私，降低通过 Blob URL 的跨站数据外泄风险。
- performance: 分区可能影响跨上下文对基于 Blob 的资源的缓存/记忆化；审查导航的性能假设。
- multimedia: 在跨源框架中使用 Blob URL 的媒体元素可能会受到访问限制；确保媒体供应考虑 Storage Key 范围。
- devices: 基于 Blob 的设备数据（例如相机捕获）以 Blob URL 存储时，在帧或导航间使用需尊重 Storage Key 边界。
- pwa-service-worker: 依赖 Blob URL 的 service worker fetchs 和导航流程应在 Storage Key 分区下进行测试。
- webassembly: 从 Blob URL 加载的 WASM 模块需要验证在多源场景中跨 Storage Key 的可访问性。
- 弃用: 将此视为行为更改而非弃用；提供迁移测试并为跨上下文的 Blob 共享提供显式处理。
