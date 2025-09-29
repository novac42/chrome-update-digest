---
layout: default
title: Chrome 140 CSS 更新 - 开发者分析
---

# Chrome 140 CSS 更新 - 开发者分析

## Area Summary

Chrome 140 为 CSS 提供了重要增强，推进了视觉效果和开发者生产力的发展。此版本引入了强大的新能力，包括用于数学表达式的类型化算术、通过嵌套伪元素树改进的视图过渡，以及增强的自定义高亮交互。更新涵盖了通过字体变化控制的排版改进、通过内容替代文本中的计数器函数实现的无障碍增强，以及滚动行为优化。这些功能共同增强了 CSS 作为成熟样式语言的地位，同时为开发者提供了对动画、布局和用户交互更精确的控制。

## Detailed Updates

基于 Chrome 对推进 Web 平台能力的承诺，此版本专注于 CSS 生态系统中的数学精度、视觉过渡和开发者体验。

### CSS typed arithmetic

#### What's New
CSS 现在支持类型化算术表达式，可以实现单位转换和不同值类型之间的数学运算，例如 `calc(10em / 1px)` 或 `calc(20% / 0.5em * 1px)`。

#### Technical Details
类型化算术系统允许开发者将类型化的 CSS 值转换为无单位数字，并在接受不同单位类型的属性中重复使用它们。这种数学精度在 CSS 表达式中实现了更复杂的计算。

#### Use Cases
对于需要在相对单位和绝对单位之间转换的排版工作特别有价值。开发者现在可以通过直接在 CSS 计算中执行复杂的单位转换来创建更灵活的响应式设计。

#### References
- [Tracking bug #40768696](https://issues.chromium.org/issues/40768696)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4740780497043456)
- [Spec](https://www.w3.org/TR/css-values-4/#calc-type-checking)

### CSS `caret-animation` property

#### What's New
`caret-animation` 属性提供对文本光标动画行为的控制，支持 `auto`（默认闪烁）和 `manual`（开发者控制）值。

#### Technical Details
当 `caret-color` 被动画化时，浏览器的默认闪烁会干扰自定义动画。`manual` 值禁用默认闪烁，允许流畅的自定义光标动画正常运行。

#### Use Cases
对于富文本编辑器、自定义输入组件和交互式文本体验至关重要，其中精确的光标动画控制可以增强用户界面而不与浏览器默认行为冲突。

#### References
- [Tracking bug #329301988](https://issues.chromium.org/issues/329301988)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5082469066604544)
- [Spec](https://drafts.csswg.org/css-ui/#caret-animation)

### highlightsFromPoint API

#### What's New
`highlightsFromPoint` API 能够检测特定文档坐标处的自定义高亮，为重叠或影子 DOM 高亮提供交互性。

#### Technical Details
此 API 返回给定点存在哪些自定义高亮，支持多个高亮可能重叠或存在于影子 DOM 边界内的复杂交互。

#### Use Cases
对于高级文本编辑应用程序、注释系统、代码编辑器和需要精确高亮交互和选择管理的协作文档工具至关重要。

#### References
- [Tracking bug #365046212](https://issues.chromium.org/issues/365046212)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4552801607483392)
- [Spec](https://drafts.csswg.org/css-highlight-api-1/#interactions)

### `ScrollIntoView` container option

#### What's New
`ScrollIntoViewOptions` 容器选项将滚动限制为仅最近的祖先滚动容器，防止不必要的页面级滚动。

#### Technical Details
此选项通过将滚动操作约束到特定容器级别，而不是影响整个文档滚动链，提供对滚动行为的细粒度控制。

#### Use Cases
对于模态对话框、嵌入式小部件和复杂布局有价值，其中滚动应该保持在特定 UI 组件内，而不会干扰更广泛的页面上下文。

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5100036528275456)
- [Spec](https://drafts.csswg.org/cssom-view/#dom-scrollintoviewoptions-container)

### View transitions: Inherit more animation properties

#### What's New
视图过渡现在通过伪元素树继承更多动画属性：`animation-timing-function`、`animation-iteration-count`、`animation-direction` 和 `animation-play-state`。

#### Technical Details
扩展的继承模型确保动画控制属性在视图过渡伪元素层次结构中得到适当传播，提供更一致的动画行为。

#### Use Cases
支持更复杂的页面过渡，具有精确的时序控制、自定义缓动函数和复杂的动画序列，在过渡伪元素树中保持一致性。

#### References
- [Tracking bug #427741151](https://issues.chromium.org/issues/427741151)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5154752085884928)
- [Spec](https://www.w3.org/TR/css-view-transitions-2)

### View transition pseudos inherit animation-delay

#### What's New
`animation-delay` 属性现在通过视图过渡伪元素树继承，补充了之前的动画属性继承更新。

#### Technical Details
这种继承确保时序延迟在视图过渡中的所有伪元素之间得到适当协调，在复杂过渡中保持时间同步。

#### Use Cases
对于编排的页面过渡至关重要，其中不同元素需要协调的时序延迟来创建复杂的进入和退出动画。

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5424291457531904)
- [Spec](https://www.w3.org/TR/css-view-transitions-2)

### Nested view transitions groups

#### What's New
视图过渡现在可以生成嵌套的伪元素树而不是扁平结构，更好地保持原始元素的视觉层次结构和意图。

#### Technical Details
嵌套结构支持正确的裁剪、嵌套 3D 变换，以及正确应用尊重原始元素层次结构的效果，如不透明度和遮罩。

#### Use Cases
对于复杂布局至关重要，其中元素之间的视觉关系必须在过渡期间得到维护，例如卡片布局、嵌套导航结构和分层内容组织。

#### References
- [Tracking bug #399431227](https://issues.chromium.org/issues/399431227)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5162799714795520)
- [Spec](https://www.w3.org/TR/css-view-transitions-2/#view-transition-group-prop)

### Propagate viewport `overscroll-behavior` from root

#### What's New
`overscroll-behavior` 属性现在从根元素（`<html>`）而不是 `<body>` 元素传播，与 CSS 工作组规范保持一致。

#### Technical Details
此更改标准化了视口属性传播行为，确保过度滚动行为由文档根而不是 body 元素控制。

#### Use Cases
为全页应用程序提供更可预测的过度滚动行为控制，对于需要精确滚动边界管理的移动 Web 应用程序和沉浸式体验特别重要。

#### References
- [Tracking bug #41453796](https://issues.chromium.org/issues/41453796)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6210047134400512)
- [Spec](https://drafts.csswg.org/css-overscroll-behavior-1)

### CSS `counter()` and `counters()` in alt text of `content` property

#### What's New
`counter()` 和 `counters()` 函数现在可以在 `content` 属性的替代文本部分中使用，增强无障碍性。

#### Technical Details
此功能允许在替代文本描述中包含动态计数器值，使生成的内容对辅助技术更有意义。

#### Use Cases
对于可访问的文档结构至关重要，其中自动编号的章节、列表或图表需要包含其顺序位置或层次编号的描述性替代文本。

#### References
- [Tracking bug #417488055](https://issues.chromium.org/issues/417488055)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5185442420621312)
- [Spec](https://drafts.csswg.org/css-content/#content-property)

### CSS `scroll-target-group` property

#### What's New
`scroll-target-group` 属性指定元素是否建立滚动标记组容器，具有 `none` 和 `auto` 值。

#### Technical Details
当设置为 `auto` 时，元素创建一个滚动标记组容器，形成滚动标记组，在相关元素之间实现协调的滚动行为。

#### Use Cases
对于轮播组件、选项卡界面和分页内容有价值，其中多个元素需要协调的滚动行为和视觉指示器。

#### References
- [Tracking bug #6607668](https://issues.chromium.org/issues/6607668)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5189126177161216)
- [Spec](https://drafts.csswg.org/css-overflow-5/#scroll-target-group)

### Support `font-variation-settings` descriptor in `@font-face` rule

#### What's New
`@font-face` 声明中现在支持 `font-variation-settings` 描述符，在字体定义级别实现字体变化控制。

#### Technical Details
此功能支持直接在字体面声明中使用基于字符串的字体变化设置语法，允许在字体加载期间对可变字体轴进行精确控制。

#### Use Cases
对于以排版为重点的应用程序至关重要，其中特定字体变化需要在字体面级别定义而不是应用于单个元素，提供更好的性能和更可预测的渲染。

#### References
- [Tracking bug #40398871](https://issues.chromium.org/issues/40398871)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5221379619946496)
- [Spec](https://www.w3.org/TR/css-fonts-4/#font-rend-desc)
