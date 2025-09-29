# Area Summary

Chrome 137 (stable) 继续推进 Storage Partitioning 的工作，针对导航和 fetch 场景引入了对 Blob URL 的分区。主要方向是按 Storage Key（top-level site、frame origin 以及 has-cross-site-ancestor boolean）更严格地隔离对 Blob URL 的访问，但对顶层导航有一项声明的例外（仅按 frame origin 分区）。此更改最影响依赖在不同源、iframe 或存储分区之间共享 blob: URL 的开发者，并通过收紧隐私与存储隔离边界推动 Web 平台发展。由于发行说明文本被截断，请参阅参考链接以获取完整背景。

## Detailed Updates

Below are the Navigation-Loading–specific changes in this release and what they mean for developers.

### Blob URL Partitioning: Fetching/Navigation (Blob URL 分区：导航与获取)

#### What's New
Chrome 将对 Blob URL 的访问按 Storage Key（top-level site、frame origin、has-cross-site-ancestor boolean）进行分区，但顶层导航作为特殊情况，仅按 frame origin 分区。

#### Technical Details
发行说明指出 Blob URL 访问与 Storage Key 的组成部分（top-level site、frame origin、has-cross-site-ancestor boolean）相关联。顶层导航被视为特殊情况，仍仅按 frame origin 分区。所给的描述被截断；请参阅下面的链接以获取完整的跟踪细节。

#### Use Cases
- 在不同 iframe 或源之间创建并传递 blob: URL 的站点，在 Storage Key 不同时可能会遇到不同的可访问性语义。
- 在相同 Storage Key 内用于导航或 fetch 的单一源 blob: URL 应继续可用，但跨分区重用可能会受到限制。
- 使用 blob 与 service workers、跨源 iframe 或复杂多站点流程的开发者应审计 blob 使用情况，并在分区环境下测试导航/获取行为。

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40057646 (Tracking bug #40057646)  
- https://chromestatus.com/feature/5037311976488960 (ChromeStatus.com entry)

## Area-Specific Expertise (Navigation-Loading relevance)

- css: Blob URL 分区与 CSS 布局无直接关联，但会影响通过 blob: URL 引用的资源（图像、字体）在渲染流程中的可见性。
- webapi: 直接影响 — Blob URL 的访问规则属于 fetch/导航 语义和资源解析的一部分。
- graphics-webgpu: 直接影响有限；作为二进制输入用于 GPU 工作流的 blob: 资源应验证其在分区中的可见性。
- javascript: 由 JS 创建的对象 URL（`URL.createObjectURL`）可能在不同 Storage Key 之间不再可访问；应审查跨上下文的消息传递。
- security-privacy: 通过将 blob: 访问按 Storage Key 作用域化，加强隔离并减少跨站数据泄露向量。
- performance: 分区可能会增加缓存碎片或在分区间重复数据；应测量存储和获取模式的影响。
- multimedia: 用于媒体回放的 Blob URL 应在不同框架/源下测试，以确保分区不会破坏回放。
- devices: 直接影响较小；接受 blob: 输入的设备 API 应遵循相同的访问约束。
- pwa-service-worker: 向客户端提供 blob 或依赖共享 blob URL 的 service worker 可能需要调整以确保在分区内覆盖。
- webassembly: 通过 blob: URL 加载的 WASM 模块受相同分区规则约束；验证模块加载路径。
- 弃用: 将此视为行为迁移项 — 在跨分区 blob 共享模式上进行测试并更新。

Saved to: digest_markdown/webplatform/Navigation-Loading/chrome-137-stable-en.md