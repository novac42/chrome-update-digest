---
layout: default
title: chrome-137-zh
---

## 详细更新

以下是 Chrome 137 中每个 Web API 更改的重点摘要及面向开发者的影响。

### Blob URL Partitioning: Fetching/Navigation

#### 新增内容
作为 Storage Partitioning 的一部分，Chrome 按 Storage Key（top-level site、frame origin 和 has-cross-site-ancestor 布尔值）对 Blob URL 访问进行分区。顶级导航仍然仅按 frame origin 分区。

#### 技术细节
分区使用 Storage Key 的组成部分来限定 Blob URL 的访问范围，从而减少跨框架和跨站点的数据泄露。顶级导航行为是一个明确的例外，仍然按 frame origin 分区。

#### 适用场景
帮助构建多源应用或嵌入内容的开发者避免跨存储分区意外通过 Blob 泄露数据，并且更好地与站点隔离存储的预期保持一致。

#### 参考资料
- 跟踪 bug #40057646: https://bugs.chromium.org/p/chromium/issues/detail?id=40057646
- ChromeStatus.com 条目: https://chromestatus.com/feature/5037311976488960

### Call stacks in crash reports from unresponsive web pages

#### 新增内容
当页面因长时间运行或无限 JavaScript 执行而变得无响应时，Chrome 会捕获 JavaScript 的调用栈；该调用栈被包含在崩溃/无响应报告中。

#### 技术细节
此功能在无响应发生时收集运行时的 JS 调用栈并将其附加到报告工件中，与报告/崩溃遥测流程对齐，以便于根因分析。

#### 适用场景
改进对因长时间计算或失控循环而挂起页面的调试；对可观测性、错误分类以及为性能或正确性相关的挂起优先修复非常有用。

#### 参考资料
- 跟踪 bug #1445539: https://bugs.chromium.org/p/chromium/issues/detail?id=1445539
- ChromeStatus.com 条目: https://chromestatus.com/feature/5045134925406208
- 规范: https://w3c.github.io/reporting/#crash-report

### Document-Isolation-Policy

#### 新增内容
Document-Isolation-Policy 允许单个文档为自身启用 crossOriginIsolation，而无需在站点范围内部署 COOP/COEP，且由进程隔离支持。

#### 技术细节
该策略对文档级别隔离（进程隔离）进行信号指示，并影响非 CORS 的跨源子资源的处理（行为在链接的规范/说明中描述）。它提供了一种机制，使文档能够独立于嵌入页面的全局头部选择更强的隔离。

#### 适用场景
使第三方或嵌入的文档能够为需要 cross-origin isolation 的功能（例如某些强大 API）选择性开启隔离，而无需站点范围内部署 COOP/COEP。

#### 参考资料
- 跟踪 bug #333029146: https://bugs.chromium.org/p/chromium/issues/detail?id=333029146
- ChromeStatus.com 条目: https://chromestatus.com/feature/5048940296830976
- 规范: https://wicg.github.io/document-isolation-policy/

### Ed25519 in web cryptography

#### 新增内容
Chrome 在 Web Cryptography API 中添加了对 Curve25519 算法的支持，具体是 Ed25519 签名算法。

#### 技术细节
Ed25519 支持通过 Web Crypto API（SubtleCrypto）以本地签名/验证原语的形式暴露，使浏览器的加密能力与 RFC 8032 中的 Ed25519 签名保持一致。

#### 适用场景
允许 Web 应用使用 Ed25519 执行现代且安全的签名操作（例如认证令牌、签名元数据），而无需随包发布 JS/WASM 加密库。

#### 参考资料
- 跟踪 bug #1370697: https://bugs.chromium.org/p/chromium/issues/detail?id=1370697
- ChromeStatus.com 条目: https://chromestatus.com/feature/5056122982457344
- 规范: https://www.rfc-editor.org/rfc/rfc8032.html

### HSTS tracking prevention

#### 新增内容
Chrome 通过仅允许顶级导航进行 HSTS 升级并阻止子资源请求的 HSTS 升级，来防止第三方使用 HSTS 缓存进行跟踪。

#### 技术细节
HSTS 升级会根据请求上下文受限：顶级导航可以被升级，而子资源请求被阻止进行由 HSTS 驱动的升级，从而减少第三方通过 HSTS 状态对用户进行指纹识别的能力。

#### 适用场景
缓解依赖 HSTS 状态在站点间区分用户的跟踪技术；与关注隐私默认设置和第三方资源加载行为的开发者相关。

#### 参考资料
- 跟踪 bug #40725781: https://bugs.chromium.org/p/chromium/issues/detail?id=40725781
- ChromeStatus.com 条目: https://chromestatus.com/feature/5065878464307200

文件目标路径:
digest_markdown/webplatform/Web API/chrome-137-stable-en.md
