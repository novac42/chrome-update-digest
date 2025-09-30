---
layout: default
title: navigation-loading-zh
---

### 1. Area Summary（领域摘要）

Chrome 137 通过根据 Storage Key（top-level site、frame origin 和 has-cross-site-ancestor 布尔值）对 Blob URL 访问进行分区，继续推进 Storage Partitioning 工作，但对顶级导航有例外：顶级导航仍仅按 frame origin 分区。对开发者影响最大的是 Blob URLs 现在更严格地按 Storage Key 进行作用域限制，这改变了在 fetch 和导航期间使用的 blob 的访问边界。此举通过在框架和站点之间收紧存储与资源隔离，降低跨站点泄露风险，从而推进了 Web 平台。团队应审查任何依赖跨源或跨框共享 Blob URL 访问的工作流，以确保兼容性。

## 详细更新

下面是与从事导航、fetch 和存储隔离的开发者相关的 Navigation-Loading 更改。

### Blob URL Partitioning: Fetching/Navigation（Blob URL 访问按 Storage Key 分区）

#### 新增内容
Partitioning of Blob URL access is implemented by Storage Key (top-level site, frame origin, and has-cross-site-ancestor boolean); top-level navigations remain partitioned only by frame origin.

#### 技术细节
Blob URL access checks now consider the Storage Key triple (top-level site, frame origin, has-cross-site-ancestor) when deciding whether a blob is accessible from a given context. Top-level navigations are treated as an exception and continue to be partitioned solely by frame origin.

#### 适用场景
- Audit and update codepaths that generate Blob URLs and share them across frames or origins.
- Validate service-worker or fetch flows that expect cross-frame Blob accessibility.
- Test navigations that rely on Blob URLs to ensure they still resolve under the more granular Storage Key partitioning.

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40057646 （跟踪 bug #40057646）
- https://chromestatus.com/feature/5037311976488960 （ChromeStatus.com 条目）

## 领域专长

- css: 布局和渲染不会受到直接影响，但用于图像或媒体的基于 Blob 的资源，如果之前跨框共享，可能无法在框之间访问。
- webapi: Blob URL 解析现在会参考 Storage Key；在上下文之间传递 Blob URLs 的 APIs 应该进行审查。
- graphics-webgpu: 没有直接变化，但引用 blob 支持资产的 GPU 资源应验证其跨上下文访问性。
- javascript: 脚本中 Blob URL 的创建和传递语义必须考虑 Storage Key 的作用域。
- security-privacy: 通过减少跨站点的 blob 暴露来加强隔离，降低跨源数据泄露的风险面。
- performance: 如果开发者需要在分区之间重新获取 blob，可能会出现轻微的性能回退；考虑针对每个 Storage Key 的缓存策略。
- multimedia: 使用 blob: URLs 作为源的媒体元素应在跨框和导航场景下测试访问失败情况。
- devices: 设备捕获数据（例如摄像头）的 Blob 传递可能会按 Storage Key 分区；检查共享工作流。
- pwa-service-worker: 与 blob 交互的 service workers 应确保 blob 在该 service worker 的 Storage Key 上下文中可用。
- webassembly: WASM 模块使用来自 blob 的二进制文件时，应在新的分区策略下验证模块获取路径。
- 弃用: 本次更改未明确弃用；将其视为行为上的分区更新，可能需要对跨源 blob 共享模式进行迁移。

生成的摘要文件路径：digest_markdown/webplatform/Navigation-Loading/chrome-137-stable-en.md
