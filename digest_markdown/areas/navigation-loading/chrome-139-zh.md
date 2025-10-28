---
layout: default
title: chrome-139-zh
---

## 领域摘要

Chrome 139（stable）引入了一项以隐私为中心的 Navigation-Loading 更改：当导航导致浏览上下文组切换时，清除 `window.name`。此举主要缓解通过 `window.name` 导致的信息泄露，从而减少跨站点跟踪向量。对开发者而言，最重要的影响是：在可能跨越浏览上下文组的导航中，不能再依赖 `window.name` 来在导航间持久化数据。该更新加强了导航模型中的隐私保障，并使行为与 HTML 规范保持一致。

## 详细更新

本次发布中的单一 Navigation-Loading 更改在跨站点导航期间加强了隐私保护。详情如下。

### Clear window name for cross-site navigations that switches browsing context group（在跨站点且切换浏览上下文组的导航中清除 window.name）

#### 新增内容
在导航导致浏览上下文组切换时，清除 `window.name` 属性的值，以避免通过该值泄露可用于跟踪的信息。

#### 技术细节
此行为在改变浏览上下文组的导航上强制重置 `window.name`，与 HTML 规范中的 resetBCName 步骤一致。此更改旨在防止跨站点携带 `window.name` 状态。

#### 适用场景
- 防止将 `window.name` 用作跨站点跟踪通道。
- 开发者不应依赖 `window.name` 在可能切换浏览上下文组的导航间持久化数据；应改用显式存储或消息传递模式。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/1090128)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5962406356320256)
- [Spec](https://html.spec.whatwg.org/multipage/browsing-the-web.html#resetBCName)
