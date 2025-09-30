## 区域摘要

Chrome 140（stable）继续有针对性的弃用，以减少旧有行为并提升安全、隐私和可访问性。该版本移除了旧的 `Purpose: prefetch` 头，改为使用 `Sec-Purpose` 用于与预测相关的抓取，并弃用在某些分区元素内部对 H1 的特殊 HTML 字体大小规则。这些更改移除了不一致或遗留行为，简化了平台表面，并降低了可访问性问题与指纹识别风险。各团队应计划迁移到 `Sec-Purpose` 并更新 CSS/作者样式，避免依赖已弃用的 H1 规则。

## 详细更新

下面条目扩展了上文摘要，并为开发者和实现者提供可操作的细节。

### Stop sending `Purpose: prefetch` header from prefetches and prerenders（停止从 prefetch 和 prerender 发送 `Purpose: prefetch` 头）

#### 新增内容
Chromium 将停止为预获取（prefetch）和预渲染（prerender）预测性抓取发送旧的 `Purpose: prefetch` 头；这些请求将改为使用 `Sec-Purpose` 头。

#### 技术细节
此更改适用于预测规则 `prefetch` 和 `prerender`、`<link rel=prefetch>` 以及 Chromium 的非标准 `<link rel=prerender>`。行为上的变更是将旧的头替换为标准化的 `Sec-Purpose` 信号，以传达对预测性抓取的意图。

#### 适用场景
- 减少指纹识别并标准化对预测性抓取的意图信号。
- 服务器和分析系统应切换为检查 `Sec-Purpose`，而不是 `Purpose: prefetch`。
- 与旧头绑定的功能开关或服务器端优化必须迁移。

#### 参考资料
- https://issues.chromium.org/issues/420724819
- https://chromestatus.com/feature/5088012836536320
- https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch

### Deprecate special font size rules for H1 within some elements（弃用某些元素内 H1 的特殊字体大小规则）

#### 新增内容
根据旧版 HTML 呈现规则，在 `<article>`、`<aside>`、`<nav>` 或 `<section>` 内嵌套时对 `<h1>` 字体大小的特例化正在被弃用。

#### 技术细节
该弃用移除了根据分区祖先元素改变 H1 呈现的作者代理特殊规则。之所以进行此操作，是因为这些规则在各用户代理和辅助技术之间导致可访问性和一致性问题。

#### 适用场景
- 开发者不应依赖用户代理特有的在这些容器中对 H1 的字体大小调整；应使用显式的 CSS 来控制标题大小。
- 注重可访问性的团队应审计标题语义和样式以确保一致的阅读顺序和大小预期。
- 迁移：为文档结构中的标题添加显式 CSS 规则，而不要依赖已弃用的用户代理默认值。

#### 参考资料
- https://html.spec.whatwg.org/multipage/rendering.html#sections-and-headings
- https://issues.chromium.org/issues/394111284
- https://chromestatus.com/feature/6192419898654720
- https://github.com/whatwg/html/pull/11102
- https://creativecommons.org/licenses/by/4.0/
- https://www.apache.org/licenses/LICENSE-2.0
- https://developers.google.com/site-policies

要保存的文件： digest_markdown/webplatform/deprecation/chrome-140-stable-en.md