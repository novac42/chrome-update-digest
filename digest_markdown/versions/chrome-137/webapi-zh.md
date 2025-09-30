---
layout: default
title: webapi-zh
---

## 区域摘要

Chrome 137 (stable) 专注于加强平台隔离、隐私和密码学，同时改进开发者诊断。关键主题包括更细粒度的存储和资源分区（Blob URL partitioning、HSTS tracking prevention、Document-Isolation-Policy）、更强的加密原语（Web Crypto 中的 Ed25519）以及改进的调试数据（针对无响应页面的调用栈）。这些更新提升了安全和隐私保障，使跨源资源处理更明确，并为开发者提供更清晰的信号以修复性能和正确性问题。对于 Web API 团队来说，这些更改将集成和迁移的考虑转向每文档隔离和扩展的加密能力。

## 详细更新

以下条目扩展了上述高层主题并总结了开发者需要了解的要点。

### Blob URL Partitioning: Fetching/Navigation（Blob URL 访问分区）

#### 新增内容
Chrome 将 Blob URL 访问按 Storage Key（top-level site、frame origin 和 has-cross-site-ancestor 布尔值）进行分区，但顶层导航仍仅按 frame origin 分区。

#### 技术细节
分区将 Blob URL 的访问检查与 Storage Key 绑定，减少通过 blob URLs 的跨站泄露。顶层导航行为是一个例外，仍然按 frame origin 分区。

#### 适用场景
- 防止具有不同 Storage Key 的框架之间通过 blob: URLs 进行跨站跟踪或数据泄露。
- 适用于在不同源或框架之间生成并共享 blob URLs 的应用。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40057646 — 跟踪 bug #40057646
- https://chromestatus.com/feature/5037311976488960 — ChromeStatus.com 条目

### Call stacks in crash reports from unresponsive web pages（无响应网页崩溃报告中的调用栈）

#### 新增内容
当页面因长时间运行的 JavaScript（例如无限循环）而变得无响应时，Chrome 会捕获 JavaScript 调用栈并将其包含在崩溃/报告数据中，以帮助开发者确定原因。

#### 技术细节
该功能在检测到无响应时捕获 JS 调用栈，并将其附加到用于诊断和开发者反馈的报告/崩溃数据中。

#### 适用场景
- 帮助开发者定位并修复导致 UI 卡顿的热点循环或长时间的同步计算。
- 通过更丰富的诊断负载改进无响应页面崩溃的分类处理。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=1445539 — 跟踪 bug #1445539
- https://chromestatus.com/feature/5045134925406208 — ChromeStatus.com 条目
- https://w3c.github.io/reporting/#crash-report — 规范

### Document-Isolation-Policy（文档隔离策略）

#### 新增内容
Document-Isolation-Policy 允许文档为自身启用 crossOriginIsolation，而无需部署 COOP/COEP，并且独立于页面的 crossOriginIsolation 状态；该策略由进程隔离提供支持。

#### 技术细节
该策略启用每文档的 cross-origin isolation，并使用进程隔离来强制实施。YAML 摘要指出对非 CORS 的跨源子资源还有额外影响。

#### 适用场景
- 需要 cross-origin-isolated 特性的站点或嵌入文档（例如某些性能 API 或 SharedArrayBuffer）可以对单个文档进行选择。
- 对于需要更强隔离但不希望修改页面级别 COOP/COEP 的 iframes 或嵌入小部件很有用。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=333029146 — 跟踪 bug #333029146
- https://chromestatus.com/feature/5048940296830976 — ChromeStatus.com 条目
- https://wicg.github.io/document-isolation-policy/ — 规范

### Ed25519 in web cryptography（Web 密码学中的 Ed25519）

#### 新增内容
在 Web Cryptography API 中添加对 Curve25519 算法的支持，特别是 Ed25519 签名算法。

#### 技术细节
Ed25519 支持将基于 Curve25519 的签名操作集成到 Web Crypto API 接口中，使得在本地生成、签名和验证这一现代签名方案成为可能。

#### 适用场景
- 需要现代、高性能签名算法用于认证、加密消息或密码学协议的网络应用。
- 简化在 Web 环境中使用 Ed25519，而无需依赖外部库或 WASM 绑定。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=1370697 — 跟踪 bug #1370697
- https://chromestatus.com/feature/5056122982457344 — ChromeStatus.com 条目
- https://www.rfc-editor.org/rfc/rfc8032.html — 规范

### HSTS tracking prevention（HSTS 跟踪防护）

#### 新增内容
通过允许仅对顶层导航进行 HSTS 升级并阻止子资源请求的 HSTS 升级，减轻 HSTS 缓存被用于第三方跟踪的问题。

#### 技术细节
该功能在子资源上下文中限制基于 HSTS 的升级，使第三方无法利用 HSTS 缓存创建跨站标识符。

#### 适用场景
- 防止第三方域使用的基于 HSTS 的跨站跟踪向量。
- 会影响依赖子资源 HSTS 升级的集成；开发者应确保资源在 HTTPS 上可访问或处理降级行为。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40725781 — 跟踪 bug #40725781
- https://chromestatus.com/feature/5065878464307200 — ChromeStatus.com 条目

已保存文件：digest_markdown/webplatform/Web API/chrome-137-stable-en.md
