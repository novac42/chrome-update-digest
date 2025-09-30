---
layout: default
title: css-zh
---

## 区域摘要

Chrome 137 引入了一系列以 CSS 为中心的改进，强调条件样式、可访问性感知的布局顺序、更丰富的 SVG/CSS 集成，以及动画/过渡的人机工程学。对开发者来说，显著变化包括用于行内条件值的 CSS `if()` 函数、用于逻辑焦点与辅助顺序控制的 `reading-flow`/`reading-order`，以及用于 SPA 动画连续性的 `view-transition-name: match-element`。这些功能通过提供更具表达力、可访问且对动画友好的 CSS 原语，减少对大量 JS 权宜之计的需求，从而推动平台进步。更新降低了实现常见 UI 模式（可访问性、响应式动画路径、系统主题化）的难度，并改善了与 Web 平台规范的互操作性。

## 详细更新

以下条目扩展了上文摘要，并为 Chrome 137 中交付的每个 CSS 领域功能提供实用和技术上下文。

### CSS if() function

#### 新增内容
CSS `if()` 函数提供了一种简洁方式，使用以分号分隔的一系列条件-值对来表达条件值。它按顺序评估条件并返回与第一个为真的条件关联的值。

#### 技术细节
实现了来自 CSS Values Level 5 draft 的规范定义的 `if()`，在 CSS 表达式中处理条件/值对。

#### 适用场景
在无需 CSS 自定义属性和 JS 权宜之计的情况下实现行内条件样式；适用于回退样式、响应式变体以及简化复杂的 calc/链式场景。

#### 参考资料
- [跟踪问题 #346977961](https://bugs.chromium.org/p/chromium/issues/detail?id=346977961)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5084924504915968)  
- [规范](https://www.w3.org/TR/css-values-5/#if-function)

### CSS reading-flow, reading-order properties

#### 新增内容
添加了 `reading-flow` 来控制元素向可访问性工具和制表焦点暴露的顺序，添加了 `reading-order` 以允许作者在阅读流容器内覆盖顺序。

#### 技术细节
实现了来自 Display Level 4 drafts 的 reading-flow 模型，以影响可访问性 API 和顺序焦点导航使用的逻辑序列。

#### 适用场景
在无需重排 DOM 的情况下控制键盘/制表顺序和辅助技术的阅读顺序，适用于复杂布局（flex、grid、block）；改善了旋转、多栏或仅视觉排序场景下的可访问性。

#### 参考资料
- [跟踪问题 #40932006](https://bugs.chromium.org/p/chromium/issues/detail?id=40932006)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5061928169472000)  
- [规范](https://drafts.csswg.org/css-display-4/#reading-flow)  
- [使用 CSS reading-flow 实现逻辑顺序的焦点导航](https://developer.chrome.com/blog/reading-flow)

### Ignore letter spacing in cursive scripts

#### 新增内容
添加了在手动指定 `letter-spacing` 时对草书/连笔文字忽略间距的行为，符合 CSS Text 规范，以避免破坏单词形状和可读性。

#### 技术细节
实现了文本模块的指导，选择性地在会损害字形连结完整性的草书/手写字体上忽略 `letter-spacing`。

#### 适用场景
通过防止开发者设置的字间距破坏字形连结和单词识别，改进草书和手写语言的排版；对本地化敏感的 UI 至关重要。

#### 参考资料
- [跟踪问题 #40618336](https://bugs.chromium.org/p/chromium/issues/detail?id=40618336)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5088256061988864)  
- [规范](https://www.w3.org/TR/css-text-3/#letter-spacing-property)

### Selection API getComposedRanges and direction

#### 新增内容
交付了两个 Selection API 补充：`Selection.direction`（返回 `none`、`forward` 或 `backward`）和 `Selection.getComposedRanges()`（返回 0 或 1 个 composed StaticRange，可能跨越 shadow 边界）。

#### 技术细节
使 Selection 行为与 Selection API 草案对齐，以公开选择的重力和对在 shadow/slot 上下文中有用的组合范围抽象。

#### 适用场景
改进富组件和 shadow DOM 中对用户文本选择的编程处理，使编辑器和可访问性工具能够实现准确的插入点/选择逻辑。

#### 参考资料
- [跟踪问题 #40286116](https://bugs.chromium.org/p/chromium/issues/detail?id=40286116)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5069063455711232)  
- [规范](https://w3c.github.io/selection-api/#dom-selection-getcomposedranges)

### Support offset-path: shape()

#### 新增内容
支持 `offset-path: shape()`，允许使用响应式形状驱动动画运动路径。

#### 技术细节
实现了 CSS Motion Path / Shapes Level 规范中为 `offset-path` 定义的 `shape()` 函数，使路径能够适应布局。

#### 适用场景
创建遵循布局感知形状（例如边界框或响应式形状）的运动路径动画，而无需手动重新计算路径。

#### 参考资料
- [跟踪问题 #389713717](https://bugs.chromium.org/p/chromium/issues/detail?id=389713717)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5062848242884608)  
- [规范](https://www.w3.org/TR/css-shapes-2/#shape-function)

### Support the transform attribute on SVGSVGElement

#### 新增内容
允许在 `<svg>` 根元素上使用 `transform` 属性，以对整个 SVG 坐标系或其内容应用缩放、旋转、平移、倾斜等变换。

#### 技术细节
实现了 SVG2 中对根 `<svg>` 元素的可变换性，使行为与 InterfaceSVGTransformable 规范一致。

#### 适用场景
无需额外包装元素即可简化全局 SVG 变换；便于通过 CSS 或属性缩放/旋转整个 SVG。

#### 参考资料
- [跟踪问题 #40313130](https://bugs.chromium.org/p/chromium/issues/detail?id=40313130)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5070863647424512)  
- [规范](https://www.w3.org/TR/SVG2/types.html#InterfaceSVGTransformable)

### System accent color for accent-color property

#### 新增内容
`accent-color` 现在可以使用操作系统的强调色，使表单控件（复选框、单选按钮、进度条）自动采用用户的操作系统强调色。

#### 技术细节
使 `accent-color` 的行为与 CSS UI Level 4 对齐，将系统强调色令牌映射到表单元素的渲染。

#### 适用场景
确保内置控件的原生一致主题，改善与平台 UI 的视觉融合，并减少自定义样式需求。

#### 参考资料
- [跟踪问题 #40764875](https://bugs.chromium.org/p/chromium/issues/detail?id=40764875)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5088516877221888)  
- [规范](https://www.w3.org/TR/css-ui-4/#accent-color)

### Allow <use> to reference an external document's root element by omitting the fragment

#### 新增内容
放宽了 `<use>` 的引用要求，当引用外部 SVG 文档且省略片段时，解析为该文档的根元素。

#### 技术细节
调整了跨文档引用的 `<use>` 解析逻辑，以在未提供片段时接受外部文档根目标，符合 SVG2 结构规则。

#### 适用场景
简化通过 `<use>` 重用整个外部 SVG 文档的流程，无需内部片段 ID；改善 SVG 组合工作流。

#### 参考资料
- [跟踪问题 #40362369](https://bugs.chromium.org/p/chromium/issues/detail?id=40362369)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5078775255900160)  
- [规范](https://www.w3.org/TR/SVG2/struct.html#UseElement)

### Canvas floating point color types

#### 新增内容
在 Canvas 2D 上下文和 ImageData 中添加对浮点像素格式（而非 8 位）的支持，以实现更高精度的颜色表示。

#### 技术细节
扩展了 CanvasRenderingContext2D、OffscreenCanvasRenderingContext2D 和 ImageData，以按照 HTML Canvas 规范扩展支持浮点颜色类型。

#### 适用场景
对于需要高动态范围或高精度渲染的场景（医学可视化、科学成像、HDR 工作流），8 位颜色量化不足时这是必要的。

#### 参考资料
- [跟踪问题 #40245602](https://bugs.chromium.org/p/chromium/issues/detail?id=40245602)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5053734768197632)  
- [规范](https://html.spec.whatwg.org/multipage/canvas.html#the-2d-rendering-context)

### view-transition-name: match-element

#### 新增内容
`view-transition-name` 的 `match-element` 值基于元素的身份生成唯一 ID，从而在视图过渡中为在 SPA 中移动的元素提供一致的命名。

#### 技术细节
实现了 View Transitions Level 2 draft 中的视图过渡命名机制，以匹配在 DOM 中移动的元素，而无需手动 ID。

#### 适用场景
简化为在客户端导航期间移动或更改父级的元素（SPA 路由中常见）创建无缝过渡，提升动画连续性而无需管理 DOM ID。

#### 参考资料
- [跟踪问题 #365997248](https://bugs.chromium.org/p/chromium/issues/detail?id=365997248)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5092488609931264)  
- [规范](https://drafts.csswg.org/css-view-transitions-2/#view-transition-name-prop)
