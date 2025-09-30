---
layout: default
title: chrome-138-zh
---

## 领域摘要

Chrome 138 通过新的数学与环境特性、布局关键字和可感知兄弟元素的函数增强了 CSS 的表达能力。关键更改允许作者计算值（`abs()`、`sign()`、`progress()`），查询兄弟元素的位置/计数，并通过 `stretch` 关键字使元素精确填充可用空间，同时向 CSS 暴露操作系统字体缩放以改善无障碍性。这些功能减少了对用于动态样式的 JavaScript 的依赖，提供更细粒度的布局和排版控制，并提升响应性与可访问性。开发者应评估何处可用声明式 CSS 代替脚本驱动的逻辑，并调整响应性与无障碍测试以考虑操作系统字体缩放。

## 详细更新

以下条目扩展了上文摘要，描述了变更内容、工作原理、实际用途，以及指向跟踪问题和规范的链接。

### CSS Sign-Related Functions: abs(), sign()（符号相关函数）

#### 新增内容
与符号相关的函数 `abs()` 与 `sign()` 计算与其参数符号相关的值；`abs(A)` 返回 A 的绝对值并保留输入类型。

#### 技术细节
这些是添加到 CSS 值处理中的数学函数，定义于 CSS Values Level 4。它们在数值输入上运行，并返回可在其他值表达式中使用的数值输出。

#### 适用场景
在 `calc()` 与其他计算值上下文中使用以规范化值、为动画创建对称行为，或在无需 JS 的情况下推导条件样式。

#### 参考资料
- MDN 文档: abs() - https://developer.mozilla.org/docs/Web/CSS/abs
- 跟踪 bug #40253181 - https://bugs.chromium.org/p/chromium/issues/detail?id=40253181
- ChromeStatus.com 条目 - https://chromestatus.com/feature/5196860094464000
- 规范 - https://www.w3.org/TR/css-values-4/#sign-funcs

### Interpolation progress functional notation: CSS progress() function（插值进度函数）

#### 新增内容
`progress()` 函数表示在起始值和结束值之间某次计算的位置，返回一个 `<number>`，从而支持在 CSS 中进行插值数学计算。

#### 技术细节
定义于 CSS Values Level 5，`progress()` 在两个其他计算之间计算出归一化的进度值，并可嵌入值表达式以驱动插值。

#### 适用场景
用于驱动类时间线的插值以实现动画、过渡曲线或参数化样式，而无需外部定时代码；对声明式运动和响应式插值特别有用。

#### 参考资料
- 跟踪 bug #40944203 - https://bugs.chromium.org/p/chromium/issues/detail?id=40944203
- ChromeStatus.com 条目 - https://chromestatus.com/feature/5096136905244672
- 规范 - https://www.w3.org/TR/css-values-5/#progress-notation

### CSS sibling-index() and sibling-count()（基于兄弟元素的位置/计数）

#### 新增内容
`sibling-index()` 和 `sibling-count()` 返回表示元素在兄弟节点中的位置和兄弟总数的整数值，可直接在 CSS 属性值和 `calc()` 中使用。

#### 技术细节
这些函数是 CSS Values Level 5 的一部分，提供可组合进属性值的整数输出，从而无需 DOM 脚本即可实现基于位置的样式。

#### 适用场景
为列表项、网格子项或基于位置的动态生成内容（例如基于 nth 的尺寸、错开动画或基于位置的颜色）设定样式，而无需添加类或 JS。

#### 参考资料
- 跟踪 bug #40282719 - https://bugs.chromium.org/p/chromium/issues/detail?id=40282719
- ChromeStatus.com 条目 - https://chromestatus.com/feature/5649901281918976
- 规范 - https://www.w3.org/TR/css-values-5/#sibling-functions

### CSS stretch sizing keyword（stretch 尺寸关键字）

#### 新增内容
一个尺寸关键字，允许诸如 `width` 和 `height` 的属性增长以精确填充包含块的可用空间，应用于元素的 margin box（不同于与 box-sizing 相关的百分比尺寸）。

#### 技术细节
定义于 CSS Sizing Level 4，`stretch` 计算为填充包含块 margin box 的可用空间，提供一种确定性的填充行为，有别于基于百分比的尺寸。

#### 适用场景
用于需要全幅展示的 UI 元素、必须精确填充包含器（包含 margin）的布局，以及在无需复杂 `calc()` 表达式的情况下简化响应式尺寸处理。

#### 参考资料
- 跟踪 bug #41253915 - https://bugs.chromium.org/p/chromium/issues/detail?id=41253915
- ChromeStatus.com 条目 - https://chromestatus.com/feature/5102457485459456
- 规范 - https://www.w3.org/TR/css-sizing-4/#valdef-width-stretch

### CSS env variable for OS-level font scale（用于操作系统字体缩放的 env 变量）

#### 新增内容
通过环境变量向 CSS 暴露用户首选的操作系统级别字体缩放，使页面能够检测并适应用户的系统字体缩放偏好。

#### 技术细节
在 CSS Environment Variables Module 中指定，此 `env()` 变量反映操作系统选择的字体缩放，可在 CSS 中读取以调整排版尺寸或布局决策。

#### 适用场景
通过按系统字体缩放调整排版系统、基于系统字体缩放调节行高和间距，以及在用户更改操作系统字体设置时避免布局断裂，从而改善无障碍性并与用户偏好保持一致。

#### 参考资料
- 跟踪 bug #397737223 - https://bugs.chromium.org/p/chromium/issues/detail?id=397737223
- ChromeStatus.com 条目 - https://chromestatus.com/feature/5106542883938304
- 规范 - https://www.w3.org/TR/css-env-1/#os-font-scale

已保存文件路径: digest_markdown/webplatform/CSS/chrome-138-stable-en.md
