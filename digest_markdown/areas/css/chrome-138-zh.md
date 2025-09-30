---
layout: default
title: chrome-138-zh
---

## 区域摘要

Chrome 138 添加了一组 CSS 原语，使作者能够在样式表中更直接地表达数学、布局感知和基于用户偏好的尺寸。关键主题包括新的数学函数（与符号相关和进度）、用于基于位置样式的同级感知函数、可填充可用空间的 sizing 关键字，以及暴露操作系统字体缩放以供可访问性使用的 env() 变量。这些更改减少了对用于布局和响应式行为的 JavaScript 的依赖，并改进了 CSS 与用户偏好之间的一致性。对于开发者而言，影响最大的项目是 sibling-index/count 和 OS font-scale env，它们使得无需运行时脚本即可实现更丰富、对布局敏感且可访问性友好的样式。

## 详细更新

以下条目扩展了上述摘要，并列出开发者应评估以确定即时影响的 Chrome 138 CSS 领域功能。

### CSS Sign-Related Functions: abs(), sign()（符号相关函数）

#### 新增内容
将符号相关函数 `abs()` 和 `sign()` 添加到 CSS 数学函数中。

#### 技术细节
`abs(A)` 返回 A 的绝对值，保留输入的数值类型；`sign()` 根据规范计算与符号相关的结果。

#### 适用场景
在 `calc()` 表达式和其他数值 CSS 情境中计算量值和条件数学，而无需 JavaScript。

#### 参考资料
- https://developer.mozilla.org/docs/Web/CSS/abs
- https://bugs.chromium.org/p/chromium/issues/detail?id=40253181
- https://chromestatus.com/feature/5196860094464000
- https://www.w3.org/TR/css-values-4/#sign-funcs

### Interpolation progress functional notation: CSS progress() function（插值进度表示法）

#### 新增内容
引入 `progress()` 函数，该函数返回一个 `<number>`，表示两次计算之间的插值位置。

#### 技术细节
`progress()` 是一种数学函数表示法，按照 Values & Units 规范计算起始和结束计算之间的进度值。

#### 适用场景
用于基于插值的过渡或计算值，其中元素的样式应依赖于两个数值表达式之间的相对位置。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40944203
- https://chromestatus.com/feature/5096136905244672
- https://www.w3.org/TR/css-values-5/#progress-notation

### CSS sibling-index() and sibling-count()（同级索引与计数）

#### 新增内容
添加可在 CSS 属性值中作为整数使用的 `sibling-index()` 和 `sibling-count()` 函数。

#### 技术细节
`sibling-index()` 返回元素在兄弟节点中的位置；`sibling-count()` 返回兄弟节点的总数。它们可以直接使用或放入 `calc()` 内。

#### 适用场景
根据序号位置样式化元素（例如无需选择器的 nth 类规则）、创建网格/序列感知的间距，或基于兄弟节点计数计算响应式偏移。

#### 参考資料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40282719
- https://chromestatus.com/feature/5649901281918976
- https://www.w3.org/TR/css-values-5/#sibling-functions

### CSS stretch sizing keyword（stretch 尺寸关键字）

#### 新增内容
为 CSS 尺寸属性引入 `stretch` 关键字，允许元素增长以精确填充其包含块的可用空间。

#### 技术细节
`stretch` 的行为类似于 `100%`，但根据 CSS Sizing 规范，它作用于元素的 margin 盒而不是由 `box-sizing` 决定的盒。

#### 适用场景
简化必须精确填充容器可用空间（包括外边距）的布局，无需额外计算或布局技巧。

#### 参考資料
- https://bugs.chromium.org/p/chromium/issues/detail?id=41253915
- https://chromestatus.com/feature/5102457485459456
- https://www.w3.org/TR/css-sizing-4/#valdef-width-stretch

### CSS env variable for OS-level font scale（用于操作系统级字体缩放的 env 变量）

#### 新增内容
公开一个 env() 变量，反映用户的操作系统级字体缩放偏好，供 CSS 使用。

#### 技术细节
该环境变量提供操作系统的字体缩放因子，使页面能够检测并响应用户选择的系统字体缩放。

#### 适用场景
通过根据操作系统偏好缩放 UI 或排版来提高可访问性，使页面能够在不依赖启发式检测的情况下尊重用户设置。

#### 参考資料
- https://bugs.chromium.org/p/chromium/issues/detail?id=397737223
- https://chromestatus.com/feature/5106542883938304
- https://www.w3.org/TR/css-env-1/#os-font-scale

已保存至: digest_markdown/webplatform/CSS/chrome-138-stable-en.md
