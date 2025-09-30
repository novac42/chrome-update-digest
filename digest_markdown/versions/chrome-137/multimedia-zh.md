---
layout: default
title: 领域摘要
---

# 领域摘要

Chrome 137 引入了一项以多媒体为中心的权限策略，该策略让嵌入方能够对未渲染 iframe 中的媒体播放进行显式控制。该变更以 Origin Trial 形式公开，面向需要在其 CSS display 属性被设置为 `none` 的嵌入上下文中暂停媒体的嵌入网站。此更新对嵌入第三方媒体的开发者很重要，因为它将非渲染 iframe 的播放行为形式化为一个控制点，并通过 Origin Trial 和 Chromium issue 进行跟踪。

## 详细更新

以下是 Chrome 137 中多媒体更改的详细信息及其对开发者的实际影响。

### Pause media playback on not-rendered iframes（在未渲染 iframe 上暂停媒体播放）

#### 新增内容
新增 `media-playback-while-not-rendered` 权限策略，允许嵌入站点暂停未渲染的嵌入 iframe 的媒体播放——即其 CSS `display` 属性被设置为 `none`。源文中的发布说明在 "improve the p..." 之后被截断。

#### 技术细节
- 引入名为 `media-playback-while-not-rendered` 的权限策略。
- 适用于其 CSS `display` 为 `none` 的嵌入 iframe（注释中“未渲染”的定义）。
- 在提供的元数据中被标记为 Origin Trial。

#### 适用场景
- 嵌入方可以选择在未渲染的 iframe 中暂停媒体，以更好地控制用户体验（如所述）。
- 源文中有进一步解释性文本被截断；有关实现和推出的详细信息，请参阅下方的 Origin Trial 和跟踪链接。

#### 领域特定影响
- css: 依赖 `display: none` 状态作为触发“未渲染”行为的条件。
- webapi: 为嵌入页面公开了一个权限策略控制面，以管理 iframe 的播放。
- performance: 通过允许暂停未渲染 iframe 中的媒体，嵌入方可能减少不必要的后台活动。
- multimedia: 直接影响嵌入媒体的播放行为和嵌入方驱动的播放策略。
- security-privacy: 权限策略是一种面向 Web 的控制，影响跨源嵌入行为。
- javascript, graphics-webgpu, devices, pwa-service-worker, webassembly, deprecations: 源文未提供其他详情；如需相关 API 交互或迁移指南，请参阅 Origin Trial 和跟踪 bug。

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)
- [跟踪 bug #351354996](https://bugs.chromium.org/p/chromium/issues/detail?id=351354996)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5082854470868992)
