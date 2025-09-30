领域摘要

Chrome 137 引入了一组与 CSS 和 SVG 相关的改进，侧重于作者易用性、可访问性以及动画/视觉保真度。主要主题包括条件 CSS 值（`if()`）、改进的逻辑顺序与焦点导航（reading-flow/reading-order）、SVG 与动画增强（SVG 根变换、`offset-path: shape()`、视图过渡匹配），以及更高保真度的渲染选项（Canvas 浮点颜色类型、系统 `accent-color`）。这些更改帮助开发者编写更具表达力、可访问性和视觉准确性的体验，同时减少变通方法和平台碎片化。

## 详细更新

下面是 Chrome 137 在 CSS 领域的更新，扩展了面向 Web 开发者的表达能力、可访问性和渲染能力。

### CSS if() function (条件值函数)

#### 新增内容
CSS 的 `if()` 函数提供了一种简洁方式来表达条件值。它接受以分号分隔的一系列条件-值对，并返回第一个为真的条件对应的值。

#### 技术细节
按顺序评估条件-值对，并返回第一个评估为真的条件所关联的值。提供了规范引用。

#### 适用场景
在样式表中简化条件样式的编写，无需自定义属性或 JS 回退——对响应式或依赖状态的值很有用。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=346977961
- https://chromestatus.com/feature/5084924504915968
- https://www.w3.org/TR/css-values-5/#if-function

### CSS reading-flow, reading-order properties (阅读流与阅读顺序属性)

#### 新增内容
`reading-flow` 控制元素向辅助工具和标签键盘焦点导航的暴露顺序；`reading-order` 允许作者在一个 reading-flow 容器内覆盖顺序。

#### 技术细节
这些属性影响辅助技术和键盘导航在 flex、grid 或块级布局中使用的逻辑序列，使作者能够定义或覆盖顺序化的阅读/焦点顺序。

#### 适用场景
改善复杂布局（例如 grid/flex UI）的键盘和屏幕阅读器导航，让作者在不改变 DOM 顺序的情况下确保逻辑性焦点/阅读顺序。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40932006
- https://chromestatus.com/feature/5061928169472000
- https://drafts.csswg.org/css-display-4/#reading-flow
- https://developer.chrome.com/blog/reading-flow

### Ignore letter spacing in cursive scripts (在草书/连写脚本中忽略字间距)

#### 新增内容
添加行为以在指定的草书脚本中忽略 `letter-spacing` 设置，避免破坏这些脚本的词结构。

#### 技术细节
实现与 CSS Text 规范一致的逻辑，使得在会损害可读性和词结构的草书脚本中可以忽略 `letter-spacing`。

#### 适用场景
当作者对全局设置 `letter-spacing` 时，改进草书脚本语言的排版渲染和可读性。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40618336
- https://chromestatus.com/feature/5088256061988864
- https://www.w3.org/TR/css-text-3/#letter-spacing-property

### Selection API getComposedRanges and direction (Selection API 的 getComposedRanges 与 direction)

#### 新增内容
发布了两个 Selection API 的补充：`Selection.direction`（返回 `none`、`forward` 或 `backward`）和 `Selection.getComposedRanges()`（返回 0 个或 1 个合成的 StaticRange 列表）。

#### 技术细节
`Selection.direction` 暴露选择的逻辑方向。`getComposedRanges()` 提供可由作者在程序化交互中使用的合成 StaticRange 结果；包含规范链接。

#### 适用场景
为富编辑和感知选择的功能（自定义编辑器、复制/粘贴处理、复杂选择逻辑）提供更可靠的选择方向和合成范围访问。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40286116
- https://chromestatus.com/feature/5069063455711232
- https://w3c.github.io/selection-api/#dom-selection-getcomposedranges

### Support offset-path: shape() (支持 offset-path: shape())

#### 新增内容
支持 `offset-path: shape()`，允许使用响应式形状来定义动画路径。

#### 技术细节
为 `offset-path` 实现 `shape()` 函数，以便 `motion-offset/offset-path` 动画可以沿由 CSS 定义的响应式形状路径移动；提供规范和跟踪链接。

#### 适用场景
为动画元素创建可适应的运动路径（例如，响应式 UI 动画沿着在 CSS 中定义的形状移动）。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=389713717
- https://chromestatus.com/feature/5062848242884608
- https://www.w3.org/TR/css-shapes-2/#shape-function

### Support the transform attribute on SVGSVGElement (支持在 SVGSVGElement 上使用 transform 属性)

#### 新增内容
允许直接在 `<svg>` 根元素上使用其 `transform` 属性来应用变换。

#### 技术细节
为 SVGSVGElement 添加对 `transform` 属性的支持，以便根 `<svg>` 可以整体进行变换（缩放、旋转、平移、倾斜），符合 SVG 规范。

#### 适用场景
简化全局 SVG 坐标系调整和对整个 SVG 的变换，无需包装或额外容器。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40313130
- https://chromestatus.com/feature/5070863647424512
- https://www.w3.org/TR/SVG2/types.html#InterfaceSVGTransformable

### System accent color for accent-color property (用于 `accent-color` 属性的系统强调色)

#### 新增内容
允许作者通过 `accent-color` CSS 属性使用操作系统的强调色，使表单控件采用用户的系统强调色。

#### 技术细节
`accent-color` 可以反映操作系统定义的强调色，使复选框、单选按钮、进度条等表单元素无需手动主题化即可具有本地外观。

#### 适用场景
使表单控件在视觉上与平台主题和用户偏好保持一致，提升感知上的集成度和用户体验。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40764875
- https://chromestatus.com/feature/5088516877221888
- https://www.w3.org/TR/css-ui-4/#accent-color

### Allow <use> to reference an external document's root element by omitting the fragment (允许 <use> 在外部引用中通过省略片段引用外部文档的根元素)

#### 新增内容
放宽了 `<use>` 的引用规则：在外部引用中省略片段时，解析为外部文档的根元素。

#### 技术细节
之前外部 `<use>` 需要显式片段；Chrome 137 在解析 `<use>` 目标时，将省略片段视为引用外部文档根元素。

#### 适用场景
通过允许对根的简写引用，简化使用 `<use>` 重用整个外部 SVG 文档的过程，减少作者工作量。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40362369
- https://chromestatus.com/feature/5078775255900160
- https://www.w3.org/TR/SVG2/struct.html#UseElement

### Canvas floating point color types (Canvas 浮点颜色类型)

#### 新增内容
为 CanvasRenderingContext2D、OffscreenCanvasRenderingContext2D 和 ImageData 引入浮点像素格式（取代 8 位定点格式）。

#### 技术细节
为 2D Canvas 上下文和 ImageData 添加对高精度浮点颜色缓冲的支持，在需要时启用更高的动态范围和精度。

#### 适用场景
对于需要比 8 位通道更高颜色精度的高保真可视化（医学成像、科学可视化）、HDR 内容和工作负载非常重要。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40245602
- https://chromestatus.com/feature/5053734768197632
- https://html.spec.whatwg.org/multipage/canvas.html#the-2d-rendering-context

### view-transition-name: match-element (view-transition-name: match-element)

#### 新增内容
`view-transition-name` 的 `match-element` 值基于元素的身份生成唯一 ID，并在视图过渡中重命名它，有助于在 SPA 中元素移动时的动画。

#### 技术细节
`match-element` 生成一个基于元素身份的稳定名称，供视图过渡算法用于匹配和动画处理在文档内移动或跨 SPA 导航中被重定位的元素。

#### 适用场景
便于为由客户端路由或 DOM 重新父级化导致重定位的元素实现平滑过渡，而无需手动管理 ID。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=365997248
- https://chromestatus.com/feature/5092488609931264
- https://drafts.csswg.org/css-view-transitions-2/#view-transition-name-prop

保存摘要的文件路径：
digest_markdown/webplatform/CSS/chrome-137-stable-en.md