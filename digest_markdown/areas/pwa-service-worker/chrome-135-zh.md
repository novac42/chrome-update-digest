---
layout: default
title: Chrome 135 PWA 与 Service Worker 领域摘要
---

# Chrome 135 PWA 与 Service Worker 领域摘要

## 1. 领域摘要

Chrome 135 针对 PWA 与 service worker 生态系统进行了有针对性的改进，重点提升了客户端处理的一致性和标准对齐。主要方向包括增强对嵌入内容的 service worker 覆盖范围，以及更严格地遵循 service worker 客户端 URL 的预期语义。这些更改减少了边缘情况的差异，使离线和资源拦截行为对开发者来说更加可预测。通过优化 service worker 与 iframe 及文档历史的交互方式，Chrome 135 提升了现代 Web 应用的可靠性与互操作性，尤其适用于采用高级导航或动态内容嵌入的场景。

## 2. 详细更新

以下是 Chrome 135 针对 PWA 与 service worker 的主要更新，并为开发者提供了实用见解。

### Create service worker client and inherit service worker controller for srcdoc iframe（为 srcdoc iframe 创建 service worker 客户端并继承 controller）

#### 新增内容
Srcdoc iframe（通过 `srcdoc` 属性内联 HTML 的 iframe）现在会被识别为 service worker 客户端，并继承其父文档的 service worker controller。

#### 技术细节
此前，srcdoc iframe 并未被视为 service worker 客户端，导致如资源请求无法被拦截、Resource Timing 数据不完整等不一致问题。此次更新后，srcdoc iframe 会被正确注册为客户端，其网络请求可由父级的 service worker 拦截和管理。这使其行为与其他类型 iframe 及 service worker 规范保持一致。

#### 适用场景
- 确保嵌入动态内容的离线和缓存行为一致。
- 支持分析或调试时准确拦截资源并获取时序数据。
- 减少在 PWA 中使用 srcdoc iframe 时出现的意外差异。

#### 参考资料
- [跟踪 bug #41411856](https://issues.chromium.org/issues/41411856)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5128675425779712)
- [规范](https://github.com/w3c/ServiceWorker/issues/765)

### Service Worker client URL ignore `history.pushState()` changes（Service Worker 客户端 URL 忽略 `history.pushState()` 变更）

#### 新增内容
Service worker 客户端的 `Client.url` 属性现在会忽略由 `history.pushState()` 及类似历史 API 引起的变更，仅反映文档最初创建时的 URL。

#### 技术细节
此前，service worker 客户端会报告当前 URL，包括通过 History API 修改后的地址。此次更新确保 `Client.url` 始终固定为文档的初始 URL，符合 service worker 标准。这一更改提升了各浏览器间的一致性，并避免在 service worker 脚本中跟踪或匹配客户端时产生混淆。

#### 适用场景
- 简化 service worker 代码中客户端匹配逻辑，尤其适用于导航和消息传递。
- 防止单页应用（SPA）中因动态 URL 变更导致的 bug。
- 遵循 service worker 规范，提升跨浏览器兼容性。

#### 参考资料
- [跟踪 bug #41337436](https://issues.chromium.org/issues/41337436)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4996996949344256)
- [规范](https://www.w3.org/TR/service-workers/#client-url)
