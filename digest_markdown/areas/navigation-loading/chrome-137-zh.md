---
layout: default
title: 领域摘要
---

# 领域摘要

Chrome 137 (stable) 通过引入基于 Storage Key 的 Blob URL 访问分区，继续推进 Storage Partitioning 工作。此更新使用 Storage Key 的组件（top-level site、frame origin 和 has-cross-site-ancestor boolean）来隔离 Blob URL 访问，但对 top-level navigations 有一个特例：它们仍仅按 frame origin 分区。此更改改变了跨框架和站点中 Blob URLs 的解析与访问方式，影响跨站点资源隔离以及开发者对 Blob URL 可见性的预期。开发者应注意在涉及 Blob URLs 的 fetch/导航 场景中可能出现的行为差异。

## 详细更新

以下条目说明了 Blob URL 分区更改及其对导航和加载的影响。

### Blob URL Partitioning: Fetching/Navigation（获取/导航）

#### 新增内容
按 Storage Key（top-level site、frame origin 和 has-cross-site-ancestor boolean）对 Blob URL 访问进行分区的功能已实现，作为 Storage Partitioning 工作的延续。top-level navigations 是一个例外，它们仍然仅按 frame origin 分区。

#### 技术细节
- Blob URL 访问现在由 Storage Key 的组件作用域控制：top-level site、frame origin 和 has-cross-site-ancestor boolean。
- 对于 top-level navigations，分区仅限于 frame origin。
- 这种行为是更广泛 Storage Partitioning 项目的延续表现。

#### 适用场景
- 改善了不同 top-level sites 及跨站点框架之间的 Blob URL 访问隔离。
- 可能改变在 fetch 或导航 上下文中使用的 Blob URLs 的运行时可见性和访问模式。
- 开发者应审查跨源 Blob URL 的使用情况以及假定全局可访问 Blob URL 的测试。

#### 参考资料
- 跟踪 bug #40057646: https://bugs.chromium.org/p/chromium/issues/detail?id=40057646
- ChromeStatus.com 条目: https://chromestatus.com/feature/5037311976488960

输出文件：digest_markdown/webplatform/Navigation-Loading/chrome-137-stable-en.md
