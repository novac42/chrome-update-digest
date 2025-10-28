---
layout: default
title: deprecations-zh
---

## 领域摘要

Chrome 140 的弃用集中在移除导致兼容性和可访问性问题的遗留行为。最具影响的更改是用标准化的 `Sec-Purpose` 头替换 prefetch/prerender 请求中的旧 `Purpose` 头，以及移除在某些分区元素内对 `<h1>` 的特殊字体大小规则。这些更新减少了用于功能检测的歧义，并改善了用户代理之间的可访问性和一致性。开发者应审计对旧头和隐式标题大小的依赖，并采用显式、符合标准的做法。

## 详细更新

下面是对每项弃用的简明、面向开发者的描述以及后续建议。

### Stop sending `Purpose: prefetch` header from prefetches and prerenders（停止从 prefetch 和 prerender 请求中发送 `Purpose: prefetch` 头）

#### 新增内容
Prefetch 和 prerender 不再发送旧的请求头 `Purpose: prefetch`；取而代之的是使用标准化的 `Sec-Purpose` 头。

#### 技术细节
此更改影响 speculation rules `prefetch` 和 `prerender`、`<link rel=prefetch>`，以及 Chromium 的非标准 `<link rel=prerender>`。旧的 `Purpose` 头正在被移除，改用 nav-speculation 草案中定义的 `Sec-Purpose` 头。

#### 适用场景
- 此前依赖 `Purpose: prefetch` 的服务器端逻辑必须更新为检查 `Sec-Purpose`。
- 检查请求头以识别 prefetch 行为的分析或缓存层应迁移到新头。
- 基于旧头的功能检测或启发式应改为使用标准信号。

#### 参考资料
- [跟踪错误 #420724819](https://issues.chromium.org/issues/420724819)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5088012836536320)
- [规范](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

### Deprecate special font size rules for H1 within some elements（弃用某些元素内对 H1 的特殊字体大小规则）

#### 新增内容
HTML 规范中对在 `<article>`、`<aside>`、`<nav>` 或 `<section>` 内嵌套的 `<h1>` 调整字体大小的遗留特殊规则因可访问性问题而被弃用。

#### 技术细节
被弃用的规则是 HTML 渲染部分中关于 sections 和 headings 列出的那些规则。该更改移除了隐式的用户代理大小例外，因此作者不应依赖在这些元素中对 `<h1>` 的内置特殊缩放。

#### 适用场景
- 作者应在 CSS 中显式控制标题大小，而不是依赖用户代理的特殊规则。
- 以可访问性为重点的工作流程和自动化测试应显式验证标题语义和大小。
- 组件库和主题必须通过设置显式 CSS 规则，确保在各上下文中标题样式一致。

#### 参考资料
- [一份特殊规则清单](https://html.spec.whatwg.org/multipage/rendering.html#sections-and-headings)
- [跟踪错误 #394111284](https://issues.chromium.org/issues/394111284)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6192419898654720)
- [规范](https://github.com/whatwg/html/pull/11102)
- [知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)
- [Google 开发者站点政策](https://developers.google.com/site-policies)

## 领域专门知识（弃用）

- css: 不要依赖用户代理的特殊标题大小；在组件和主题中为标题设置显式 CSS 规则。
- webapi: 更新服务端和客户端逻辑以读取 `Sec-Purpose`（而非 `Purpose`）来识别 prefetch/prerender 信号。
- graphics-webgpu: 这些弃用对其没有直接影响。
- javascript: 避免进行检查旧 `Purpose` 头的功能检测；改用标准化的 fetch 请求语义。
- security-privacy: 切换到 `Sec-Purpose` 与标准化的头范围和意图信号保持一致；更新隐私敏感的服务器端逻辑。
- performance: prefetch/prerender 的功能行为未改变，但头的更改可能影响缓存/分析——相应地更新处理流水线。
- multimedia: 这些弃用对其没有直接影响。
- devices: 这些弃用对其没有直接影响。
- pwa-service-worker: 有条件响应 prefetch 请求的 Service Worker 应查找 `Sec-Purpose`。
- webassembly: 这些弃用对其没有直接影响。
- deprecations: 迁移路径——将对 `Purpose: prefetch` 的检查替换为 `Sec-Purpose`，并显式设置标题样式，而不是依赖已弃用的用户代理规则。
