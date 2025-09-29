---
layout: default
title: Chrome 140 Stable - Deprecation Updates
---

# Chrome 140 Stable - Deprecation Updates

## Area Summary

Chrome 140 引入了两项重要的弃用，在改善可访问性和标准化的同时使 Web 平台行为现代化。移除传统的 `Purpose: prefetch` 标头完成了向所有预取和预渲染操作的标准化 `Sec-Purpose` 标头的转换。此外，Chrome 弃用了嵌套在分节元素中的 H1 元素的问题字体大小规则，解决了标题层级在视觉上变得误导性的长期可访问性问题。这些更改反映了 Chrome 对 Web 标准合规性和包容性设计原则的承诺。

## Detailed Updates

这些弃用代表了迈向更一致和可访问的 Web 平台的重要步骤，移除了导致开发者困惑和用户体验问题的传统行为。

### Stop sending `Purpose: prefetch` header from prefetches and prerenders

#### What's New
Chrome 140 从所有预取和预渲染操作中移除传统的 `Purpose: prefetch` 标头，完成向早期版本中引入的标准化 `Sec-Purpose` 标头的迁移。

#### Technical Details
此更改影响平台上的多种预取机制：
- 推测规则 `prefetch` 和 `prerender`
- `<link rel=prefetch>` 元素
- Chromium 的非标准 `<link rel=prerender>` 元素

所有这些机制现在仅使用 `Sec-Purpose` 标头，消除了之前与现代标准一起发送的冗余传统标头。

#### Use Cases
构建了围绕检测预取请求的服务器端逻辑的开发者应确保他们的代码依赖 `Sec-Purpose` 标头而非已弃用的 `Purpose` 标头。这种标准化改善了互操作性并与资源加载提示的当前 Web 规范保持一致。

#### References
- [Tracking bug #420724819](https://issues.chromium.org/issues/420724819)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320)
- [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

### Deprecate special font size rules for H1 within some elements

#### What's New
Chrome 140 弃用 HTML 规范中的特殊字体大小规则，这些规则在 `<h1>` 元素嵌套在 `<article>`、`<aside>`、`<nav>` 或 `<section>` 标签内时会减小其大小。

#### Technical Details
HTML 规范历史上包含了基于 `<h1>` 元素在分节元素内的嵌套深度逐步减小其字体大小的规则。这些规则创建的视觉层级与标题级别的语义意义不匹配，导致可访问性问题，屏幕阅读器和其他辅助技术对文档结构的解释与视觉呈现不同。

#### Use Cases
这项弃用解决了关键的可访问性问题，依赖辅助技术的用户因视觉和语义标题层级之间的不匹配而感到困惑。开发者应明确使用适当的标题级别（`<h1>` 到 `<h6>`）来创建正确的文档结构，而不是依赖这些自动字体大小调整。此更改鼓励更好的语义 HTML 实践并改善残障用户的体验。

#### References
- [a list of special rules](https://html.spec.whatwg.org/multipage/rendering.html#sections-and-headings)
- [Tracking bug #394111284](https://issues.chromium.org/issues/394111284)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6192419898654720)
- [Spec](https://github.com/whatwg/html/pull/11102)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)
