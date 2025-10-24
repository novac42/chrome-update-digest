---
layout: default
title: css-zh
---

## 领域摘要

Chrome 137 在布局、SVG 和 UI 控件方面提升了 CSS 的表达力、可访问性和互操作性。关键主题包括条件值表达式（if()）、改进的阅读与焦点顺序控制、增强的 SVG/CSS 集成（transform 在 <svg> 上、<use> 引用）、以及动画/路径的改进（offset-path: shape()，view-transition 匹配）。这些更新让开发者在动画、响应式布局和平台一致的 UI 样式上拥有更多声明式控制，改善了创作可用性和可访问性。其重要性在于它们减少了对 JS 的权宜之计、启用更丰富的原生动画，并使浏览器行为与不断发展的规范保持一致。

## 详细更新

下面条目基于上文摘要，提供面向开发者的简洁技术与实用指导。

### CSS if() function (CSS if() 函数)

#### 新增内容
一个新的 CSS 函数，它评估条件—值对并返回第一个为真的条件对应的值，使纯 CSS 中能书写简洁的条件表达式。

#### 技术细节
接受由分号分隔的一系列条件/值对，按序评估，遵循 CSS Values 5 规范的定义。

#### 适用场景
在 CSS 中直接替代 JS 或自定义属性的技巧以进行简单的条件值选择（例如回退尺寸、基于主题的值）。

#### 参考资料
- 跟踪 bug #346977961: https://bugs.chromium.org/p/chromium/issues/detail?id=346977961
- ChromeStatus.com 条目: https://chromestatus.com/feature/5084924504915968
- 规范: https://www.w3.org/TR/css-values-5/#if-function

### CSS reading-flow, reading-order properties (CSS reading-flow, reading-order 属性)

#### 新增内容
用于控制元素向助残技术暴露的顺序和阅读流容器内顺序键盘导航的属性。

#### 技术细节
引入了 reading-flow 容器概念以及 reading-order，使作者能在 flex、grid 和块布局中覆盖逻辑暴露顺序，符合 Display 4 草案。

#### 适用场景
在复杂布局（响应式重排、多列内容）中，在不重排 DOM 的情况下改善可访问性与键盘导航。

#### 参考资料
- 跟踪 bug #40932006: https://bugs.chromium.org/p/chromium/issues/detail?id=40932006
- ChromeStatus.com 条目: https://chromestatus.com/feature/5061928169472000
- 规范: https://drafts.csswg.org/css-display-4/#reading-flow
- 使用 CSS reading-flow 实现逻辑顺序的焦点导航: https://developer.chrome.com/blog/reading-flow

### Ignore letter spacing in cursive scripts (在连笔/草写脚本中忽略字距)

#### 新增内容
按规范可为连笔脚本忽略 letter-spacing，从而避免破坏单词结构。

#### 技术细节
实现了规范指导的逻辑，在指定的连笔脚本文本渲染中忽略 letter-spacing，以产生正确的字形连接。

#### 适用场景
为连笔/连接书写体系提供更好的排版，提升可读性和本地化外观，避免字符间距断开字形连接。

#### 参考资料
- 跟踪 bug #40618336: https://bugs.chromium.org/p/chromium/issues/detail?id=40618336
- ChromeStatus.com 条目: https://chromestatus.com/feature/5088256061988864
- 规范: https://www.w3.org/TR/css-text-3/#letter-spacing-property

### Selection API getComposedRanges and direction (Selection API getComposedRanges 与 direction)

#### 新增内容
发布了 Selection.direction 和 Selection.getComposedRanges()，暴露选择方向以及可能跨越 shadow/slot 边界的合成 StaticRange(s)。

#### 技术细节
Selection.direction 返回 none|forward|backward。getComposedRanges() 返回最多一个合成的 StaticRange；合成范围可按 Selection API 规范跨越树边界。

#### 适用场景
用于精确的编辑器/注释工具、富选择处理，以及在 shadow DOM 场景中实现正确的插入点/选择行为。

#### 参考资料
- 跟踪 bug #40286116: https://bugs.chromium.org/p/chromium/issues/detail?id=40286116
- ChromeStatus.com 条目: https://chromestatus.com/feature/5069063455711232
- 规范: https://w3c.github.io/selection-api/#dom-selection-getcomposedranges

### Support offset-path: shape() (支持 offset-path: shape())

#### 新增内容
为 offset-path: shape() 提供支持，使响应式形状可用作动画运动路径。

#### 技术细节
按照 CSS Shapes Level 2 规范实现了 shape() 函数，用以驱动 offset-position 沿自定义形状移动。

#### 适用场景
在 CSS 中创建复杂的、响应式的运动路径动画，无需 SVG 路径备用或 JS 计算。

#### 参考资料
- 跟踪 bug #389713717: https://bugs.chromium.org/p/chromium/issues/detail?id=389713717
- ChromeStatus.com 条目: https://chromestatus.com/feature/5062848242884608
- 规范: https://www.w3.org/TR/css-shapes-2/#shape-function

### Support the transform attribute on SVGSVGElement (支持在 SVGSVGElement 上的 transform 属性)

#### 新增内容
允许在根 <svg> 元素上使用 transform 属性，将变换应用到整个 SVG 坐标系及其内容。

#### 技术细节
新增与 SVG2 可变换接口一致的支持，让根 <svg> 能像其他可变换的 SVG 元素一样接受变换。

#### 适用场景
以声明式方式旋转/缩放/平移整个 SVG 图形，简化影响完整 SVG 内容的布局与动画场景。

#### 参考资料
- 跟踪 bug #40313130: https://bugs.chromium.org/p/chromium/issues/detail?id=40313130
- ChromeStatus.com 条目: https://chromestatus.com/feature/5070863647424512
- 规范: https://www.w3.org/TR/SVG2/types.html#InterfaceSVGTransformable

### System accent color for accent-color property (accent-color 属性的系统强调色支持)

#### 新增内容
accent-color 可以采用操作系统的强调色，让表单控件与用户主题偏好一致。

#### 技术细节
accent-color 在支持的平台上与操作系统强调色集成，将其应用于复选框、单选框、进度条等控件，符合 CSS UI 4 规范。

#### 适用场景
使 UI 控件无须平台特定代码或图片即可呈现本机化且与用户主题一致的外观。

#### 参考资料
- 跟踪 bug #40764875: https://bugs.chromium.org/p/chromium/issues/detail?id=40764875
- ChromeStatus.com 条目: https://chromestatus.com/feature/5088516877221888
- 规范: https://www.w3.org/TR/css-ui-4/#accent-color

### Allow <use> to reference an external document's root element by omitting the fragment (允许在省略片段标识符时由 <use> 引用外部文档的根元素)

#### 新增内容
当未提供片段标识符时，允许 <use> 引用外部 SVG 文档的根元素。

#### 技术细节
放宽了以前的要求，使省略片段时可以解析为外部文档根节点，符合 SVG2 的结构规则。

#### 适用场景
在不要求显式片段 ID 的情况下简化重用整个外部 SVG 文档，便于资源组合。

#### 参考资料
- 跟踪 bug #40362369: https://bugs.chromium.org/p/chromium/issues/detail?id=40362369
- ChromeStatus.com 条目: https://chromestatus.com/feature/5078775255900160
- 规范: https://www.w3.org/TR/SVG2/struct.html#UseElement

### Canvas floating point color types (Canvas 浮点颜色类型)

#### 新增内容
为 CanvasRenderingContext2D、OffscreenCanvasRenderingContext2D 和 ImageData 引入浮点像素格式，以实现更高精度的渲染。

#### 技术细节
支持浮点像素缓冲区，取代 8 位固定格式，以便根据 HTML Canvas 规范启用 HDR 和高精度工作流。

#### 适用场景
医疗可视化、HDR 成像、科学可视化以及任何需要超过 8 位通道精度或高动态范围的情形。

#### 参考资料
- 跟踪 bug #40245602: https://bugs.chromium.org/p/chromium/issues/detail?id=40245602
- ChromeStatus.com 条目: https://chromestatus.com/feature/5053734768197632
- 规范: https://html.spec.whatwg.org/multipage/canvas.html#the-2d-rendering-context

### view-transition-name: match-element (view-transition-name: match-element)

#### 新增内容
match-element 值基于标识为元素生成唯一 ID，支持当元素在单页应用中位移时的视图过渡。

#### 技术细节
为元素生成并分配唯一的匹配 ID，以供 view transitions 使用，即使 DOM 位置发生改变也有助于元素匹配，符合 View Transitions Level 2 草案。

#### 适用场景
在客户端导航（SPA）期间平滑地为在 DOM 中被重新定位的元素做动画，而无需手动管理 ID。

#### 参考资料
- 跟踪 bug #365997248: https://bugs.chromium.org/p/chromium/issues/detail?id=365997248
- ChromeStatus.com 条目: https://chromestatus.com/feature/5092488609931264
- 规范: https://drafts.csswg.org/css-view-transitions-2/#view-transition-name-prop

另存为：digest_markdown/webplatform/CSS/chrome-137-stable-en.md
