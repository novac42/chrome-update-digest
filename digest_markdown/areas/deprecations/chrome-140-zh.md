---
layout: default
title: chrome-140-zh
---

## 区域摘要

Chrome 140 的弃用集中在移除遗留行为并改进平台一致性与可访问性。此版本停止发送遗留的 `Purpose: prefetch` 标头，改为使用标准化的 `Sec-Purpose` 标头，同时弃用在某些分区元素内嵌套的 `<h1>` 的特殊字体大小规则。这些更改减少了实现之间的碎片化，并分别解决了可访问性问题。维护服务器、中间件和 CSS/UA 逻辑的人员应更新预期，以在各浏览器间保持正确行为和可访问性。

## 详细更新

以下条目扩展了上述摘要并指向迁移与实现指导的主要参考资料。

### Stop sending `Purpose: prefetch` header from prefetches and prerenders (停止从预取和预渲染发送 `Purpose: prefetch` 标头)

#### 新增内容
Prefetches 和 prerenders 现在使用 `Sec-Purpose` 标头；遗留的 `Purpose: prefetch` 标头将被移除。此更改适用于 speculation rules `prefetch`、speculation rules `prerender`、`<link rel=prefetch>`，以及 Chromium 的非标准 `<link rel=prerender>`。

#### 技术细节
随着 prefetch/prerender 请求发出的标头从 `Purpose: prefetch` 过渡到 `Sec-Purpose`，检查遗留标头的实现和服务器端逻辑必须识别并处理 `Sec-Purpose`。

#### 适用场景
依赖 `Purpose: prefetch` 的服务器、代理、分析或功能开关中间件应将检测和处理迁移到 `Sec-Purpose`，以维持对推测性获取和预渲染的正确处理。

#### 参考资料
- https://issues.chromium.org/issues/420724819 (Tracking bug #420724819)  
- https://chromestatus.com/feature/5088012836536320 (ChromeStatus.com entry)  
- https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch (Spec)  

### Deprecate special font size rules for H1 within some elements (弃用某些元素内 H1 的特殊字体大小规则)

#### 新增内容
HTML 规范中关于当 `<h1>` 嵌套在 `<article>`、`<aside>`、`<nav>` 或 `<section>` 内时的特殊渲染规则因可访问性问题而被弃用。

#### 技术细节
此次弃用针对 HTML 规范“sections and headings” 渲染指导中记录的规则。理由提及这些隐含的特殊大小行为存在可访问性问题；实现者和作者应查阅规范与跟踪讨论以获取详细信息。

#### 适用场景
作者和用户代理实现者应避免依赖这些已弃用的隐式标题大小规则。若需一致的呈现，优先使用显式的 CSS 大小或结构化标记，而非隐式的特殊情况行为。

#### 参考资料
- https://html.spec.whatwg.org/multipage/rendering.html#sections-and-headings (a list of special rules)  
- https://issues.chromium.org/issues/394111284 (Tracking bug #394111284)  
- https://chromestatus.com/feature/6192419898654720 (ChromeStatus.com entry)  
- https://github.com/whatwg/html/pull/11102 (Spec)  
- https://creativecommons.org/licenses/by/4.0/ (Creative Commons Attribution 4.0 License)  
- https://www.apache.org/licenses/LICENSE-2.0 (Apache 2.0 License)  
- https://developers.google.com/site-policies (Google Developers Site Policies)
