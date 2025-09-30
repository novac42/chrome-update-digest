---
layout: default
title: chrome-138-zh
---

### 1. 区域摘要

Chrome 138（stable）新增对由 Speculation Rules API 驱动且受 ServiceWorker 控制的预取支持。对开发者影响最大的一点是，speculation-rules 预取现在可以通过控制它们的 Service Worker 路由，而不是在检测到 Service Worker 存在时被取消。这使浏览器行为与 nav-speculation integration spec 保持一致，并为预取的导航目标提供更一致的缓存和离线处理。这些更新重要，因为它们减少了 PWAs 中预取与正常导航之间令人意外的差异，并提高了 Service Worker 控制的可预测性。

## 详细更新

下面是将摘要与本次发布中列出的该项更改连接起来的详细信息。

### ServiceWorker support for Speculation Rules Prefetch (Service Worker 控制的预取支持)

#### 新增内容
启用由 ServiceWorker 控制的预取：对于由 Service Worker 控制的 URL，speculation-rules 发起的预取在检测到控制它们的 Service Worker 时不再被取消。

#### 技术细节
根据所链接的规范，通过 Speculation Rules API 发起的预取可以与 Service Worker 控制集成，使得这些 fetch 遵循与正常导航相同的 Service Worker 处理模型。有关实现说明和状态，请参阅规范和跟踪 bug。

#### 适用场景
- PWAs：预取的导航可以由 Service Worker 提供，从而改善缓存利用率并提升预取与后续导航之间的一致性。
- Offline-first flows：预取可以为未来导航预热 Service Worker 缓存。
- Performance testing：减少预取响应与正常导航期间提供的响应之间的差异，简化性能调优。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40947546
- https://chromestatus.com/feature/5121066433150976
- https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-sw-integration

文件已保存至：
```text
digest_markdown/webplatform/PWA and service worker/chrome-138-stable-en.md
