## Area Summary

Chrome 137 在 CSS 方面带来一系列改进：新增值函数、布局/可访问性控制，以及针对 SVG 和动画的作者便利功能。对开发者的主要益处包括条件 CSS 函数 if()、用于可访问性和焦点导航的逻辑阅读流控制、改进的选择 API，以及用于 SPA 动画的视图过渡匹配。这些更改提升了表达力（条件值、基于形状的运动）、可访问性（阅读顺序、选择方向）以及与平台功能的互操作性（系统强调色、SVG 根变换）。总体而言，它们使复杂的 UI 行为、动画和对可访问性敏感的布局在整个 Web 平台上更容易实现且更稳健。

## Detailed Updates

Below are the CSS-focused updates extracted from Chrome 137 and what they mean for developers.

### CSS if() function

#### What's New
一个条件函数，接受条件/值对并返回第一个为真的条件对应的值，从而实现简洁的条件样式。

#### Technical Details
按顺序评估条件；作者按 CSS Values Level 5 规范提供以分号分隔的条件-值对。

#### Use Cases
在无需借助自定义属性 + calc 技巧或额外选择器的情况下，简化响应式或基于状态的属性设置。

#### References
- [Tracking bug #346977961](https://bugs.chromium.org/p/chromium/issues/detail?id=346977961)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5084924504915968)  
- [Spec](https://www.w3.org/TR/css-values-5/#if-function)

### CSS reading-flow, reading-order properties

#### What's New
新增属性用于控制元素对可访问性工具和键盘焦点顺序的顺序暴露，并允许在阅读流容器内手动覆盖顺序。

#### Technical Details
`reading-flow` 定义元素在逻辑阅读序列中的参与；`reading-order` 允许作者按 CSS Display Level 4 草案在阅读流容器内重排项目顺序。

#### Use Cases
在不更改 DOM 顺序的情况下改善复杂布局（flex/grid）中的键盘导航和屏幕阅读器顺序；对可访问组件和本地化布局很有用。

#### References
- [Tracking bug #40932006](https://bugs.chromium.org/p/chromium/issues/detail?id=40932006)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5061928169472000)  
- [Spec](https://drafts.csswg.org/css-display-4/#reading-flow)  
- [Use CSS reading-flow for logical sequential focus navigation](https://developer.chrome.com/blog/reading-flow)

### Ignore letter spacing in cursive scripts

#### What's New
在会破坏单词结构的草写脚本中，可以忽略 `letter-spacing`，以符合规范并改善这些脚本的文本渲染。

#### Technical Details
文本渲染逻辑遵循 CSS Text Level 3 的指导，在适当情况下绕过对草写脚本的 `letter-spacing` 处理。

#### Use Cases
提高草写脚本语言的排版准确性和可读性，确保作者指定的 `letter-spacing` 不会损害可读性或词形。

#### References
- [Tracking bug #40618336](https://bugs.chromium.org/p/chromium/issues/detail?id=40618336)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088256061988864)  
- [Spec](https://www.w3.org/TR/css-text-3/#letter-spacing-property)

### Selection API getComposedRanges and direction

#### What's New
两个新的 Selection API 功能：`Selection.direction` 用于读取选择方向（`none`、`forward`、`backward`），以及 `Selection.getComposedRanges()` 返回可能跨越影子边界的组合 StaticRange。

#### Technical Details
`getComposedRanges()` 可返回 0 或 1 个可跨树边界的组合 StaticRange；`direction` 暴露锚点/延伸顺序语义。

#### Use Cases
在编辑器、富文本组件和可访问性工具中改善精确选择处理，尤其是在处理 shadow DOM 或双向文本时。

#### References
- [Tracking bug #40286116](https://bugs.chromium.org/p/chromium/issues/detail?id=40286116)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5069063455711232)  
- [Spec](https://w3c.github.io/selection-api/#dom-selection-getcomposedranges)

### Support offset-path: shape()

#### What's New
增加对 `offset-path: shape()` 的支持，允许使用响应式形状定义动画运动路径。

#### Technical Details
将 CSS Shapes Level 2 的 `shape()` 函数实现为偏移定位 API 的有效运动路径。

#### Use Cases
为动画对象创建流畅的几何驱动运动（例如沿响应式曲线移动），减少 JS 驱动的路径计算并提升响应性。

#### References
- [Tracking bug #389713717](https://bugs.chromium.org/p/chromium/issues/detail?id=389713717)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5062848242884608)  
- [Spec](https://www.w3.org/TR/css-shapes-2/#shape-function)

### Support the transform attribute on SVGSVGElement

#### What's New
在 `<svg>` 根元素上启用 `transform` 属性，允许对整个 SVG 坐标系应用变换。

#### Technical Details
`SVGSVGElement` 在根上直接支持变换操作（缩放/旋转/平移/倾斜），影响整个 SVG 内容和坐标映射。

#### Use Cases
在无需包裹内容或更改 viewBox 的情况下操作整个 SVG（缩放、旋转），简化复杂 SVG UI 组件的编写。

#### References
- [Tracking bug #40313130](https://bugs.chromium.org/p/chromium/issues/detail?id=40313130)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5070863647424512)  
- [Spec](https://www.w3.org/TR/SVG2/types.html#InterfaceSVGTransformable)

### System accent color for accent-color property

#### What's New
`accent-color` 现在可以使用操作系统的强调色，用于复选框、单选按钮和进度条等表单控件。

#### Technical Details
当 `accent-color` 设置为系统强调色时，UA 样式将表单控件的视觉效果映射到操作系统强调色以保持原生外观。

#### Use Cases
使表单控件自动匹配用户的系统主题，提升跨平台 Web 应用的 UX 一致性并减少平台特定的 CSS 替代方案工作量。

#### References
- [Tracking bug #40764875](https://bugs.chromium.org/p/chromium/issues/detail?id=40764875)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088516877221888)  
- [Spec](https://www.w3.org/TR/css-ui-4/#accent-color)

### Allow <use> to reference an external document's root element by omitting the fragment

#### What's New
`<use>` 现在可以引用外部 SVG 文档的根元素，即使未提供片段 ID，从而简化外部引用。

#### Technical Details
此前解析 `<use>` 需要显式片段；现在省略片段将解析为被引用文档的根元素。

#### Use Cases
方便重复使用外部 SVG 文件作为符号或模板，而无需修改源 SVG 添加 ID；在跨文档组合 SVG 时降低摩擦。

#### References
- [Tracking bug #40362369](https://bugs.chromium.org/p/chromium/issues/detail?id=40362369)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5078775255900160)  
- [Spec](https://www.w3.org/TR/SVG2/struct.html#UseElement)

### Canvas floating point color types

#### What's New
Canvas 2D 上下文和 ImageData 现在支持浮点像素格式（超出 8 位定点），以实现更高精度和 HDR 工作流。

#### Technical Details
`CanvasRenderingContext2D`、`OffscreenCanvasRenderingContext2D` 和 `ImageData` 可根据 HTML canvas 规范扩展使用浮点颜色类型，以获得更高的动态范围和精度。

#### Use Cases
对于医学可视化、科学成像、HDR 渲染以及任何需要高精度颜色计算的管线是必需的。

#### References
- [Tracking bug #40245602](https://bugs.chromium.org/p/chromium/issues/detail?id=40245602)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5053734768197632)  
- [Spec](https://html.spec.whatwg.org/multipage/canvas.html#the-2d-rendering-context)

### view-transition-name: match-element

#### What's New
`view-transition-name: match-element` 从元素标识生成唯一 ID，以便在视图过渡中进行一致匹配，适用于在 DOM 中移动元素的 SPA 场景。

#### Technical Details
`match-element` 为元素分配生成的唯一标识符，并在视图过渡期间使用该标识符匹配源和目标元素，遵循 View Transitions 规范草案。

#### Use Cases
简化在单页应用导航过程中被移动或重建的元素的动画处理，提升连续性并减少手动匹配逻辑。

#### References
- [Tracking bug #365997248](https://bugs.chromium.org/p/chromium/issues/detail?id=365997248)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5092488609931264)  
- [Spec](https://drafts.csswg.org/css-view-transitions-2/#view-transition-name-prop)

已保存文件路径：digest_markdown/webplatform/CSS/chrome-137-stable-en.md