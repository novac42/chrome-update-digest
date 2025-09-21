# Chrome 140 Stable - 弃用功能

## 总结

Chrome 140 引入了两个重要的弃用功能，专注于 Web 标准对齐和可访问性改进。此版本移除了传统的 `Purpose: prefetch` 标头，改用标准化的 `Sec-Purpose` 标头，并弃用了在分段元素中导致可访问性问题的有问题的 H1 字体大小规则。

## 功能详情

### Stop sending `Purpose: prefetch` header from prefetches and prerenders

**更改内容**：
Chrome 正在移除预取和预渲染操作中的传统 `Purpose: prefetch` 标头，将其替换为标准化的 `Sec-Purpose` 标头。此更改影响推测规则预取、推测规则预渲染、`<link rel=prefetch>` 以及 Chromium 的非标准 `<link rel=prerender>`。此弃用使 Chrome 与 Web 标准保持一致，并提高了预取机制之间的一致性。开发者应更新其服务器端逻辑以处理 `Sec-Purpose` 标头，而不是依赖已弃用的 `Purpose: prefetch` 标头。

**参考资料**：
- [Tracking bug #420724819](https://issues.chromium.org/issues/420724819)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320)
- [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

### Deprecate special font size rules for H1 within some elements

**更改内容**：
Chrome 正在弃用 HTML 规范中针对嵌套在 `<article>`、`<aside>`、`<nav>` 或 `<section>` 元素内的 `<h1>` 元素的特殊字体大小规则。这些规则会根据 H1 标题在分段元素内的嵌套深度自动减小其字体大小。此弃用解决了重大的可访问性问题，因为这些规则可能创建与视觉呈现不匹配的混乱标题层次结构，使屏幕阅读器用户更难导航内容。开发者应使用 CSS 显式设置标题样式，而不是依赖这些自动大小调整。

**参考资料**：
- [a list of special rules](https://html.spec.whatwg.org/multipage/rendering.html#sections-and-headings)
- [Tracking bug #394111284](https://issues.chromium.org/issues/394111284)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6192419898654720)
- [Spec](https://github.com/whatwg/html/pull/11102)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)