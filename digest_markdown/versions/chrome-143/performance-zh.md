---
layout: default
title: performance-zh
---

## 领域摘要

Chrome 143（stable）引入了一个专注的 Performance 更改：移动端 `eager` eagerness 的推测规则现在在 HTML 锚元素短暂保留在视口中时触发预取和预渲染。此更改对开发者影响中等，改善了移动端的推测加载行为。它通过使推测更响应用户可见的链接候选，减少链接密集的移动体验的感知导航延迟，推进了 Web 平台。团队应注意行为更改，以优化资源使用和用户体验。

## 详细更新

以下是与上述摘要相关的 Performance 领域更新。

### Speculation rules: mobile `eager` eagerness improvements（推测规则：移动端 `eager` eagerness 改进）

#### 新增内容
在移动端，`eager` eagerness 推测规则预取和预渲染现在在 HTML 锚元素短时间位于视口中时触发。

#### 技术细节
此更改调整了 `eager` 级别推测加载在移动设备上激活的时机——特别是与锚元素短暂可见于视口中相关联。实现和跟踪在 Chromium 跟踪错误和 HTML 推测加载规范中捕获。

#### 适用场景
- 链接密集的移动站点可以通过更早的预取/预渲染激活实现更快的感知导航。
- 开发者应考虑推测加载时机如何影响移动端的资源预算和用户体验。

#### 参考资料
- [跟踪错误 #436705485](https://issues.chromium.org/issues/436705485)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5086053979521024)
- [规范](https://html.spec.whatwg.org/multipage/speculative-loading.html#speculative-loading)
