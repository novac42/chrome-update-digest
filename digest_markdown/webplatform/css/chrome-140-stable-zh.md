## 领域摘要

Chrome 140（stable）在 CSS 方面的进展集中于更强的类型感知数学、更细粒度的动画控制、改进的视图过渡保真度，以及更明确的滚动和字体控制。对开发者有影响的关键更改包括用于单位安全计算的 CSS typed arithmetic、扩展的视图过渡继承与嵌套以实现更顺滑的 UI 动画，以及像 `scroll-target-group` 和为 `scrollIntoView` 添加 `container` 选项等新的滚动原语。这些更新简化了作者工作量，提升了无障碍性和动画一致性，并在复杂组件树中使布局与滚动行为更可预测。

## 详细更新

下面的条目扩展了上述摘要，并列出在 Chrome 140 中公开的每个 CSS 领域功能。

### CSS typed arithmetic (类型化算术)

#### 新增内容
Typed arithmetic 允许在 CSS 中编写具单位意识的表达式（例如 `calc(10em / 1px)`），支持在 `calc()` 内在类型化值与非类型化值之间进行转换。

#### 技术细节
表达式按照 CSS Values Level 4 规范执行类型检查的算术运算，允许作者将类型化值转换为数字并安全地重新组合单位。

#### 适用场景
适用于排版以及任何需要单位转换或在接受数字的属性中重用类型化值的布局。

#### 参考资料
- [跟踪 bug #40768696](https://issues.chromium.org/issues/40768696)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4740780497043456)
- [规范](https://www.w3.org/TR/css-values-4/#calc-type-checking)

### CSS `caret-animation` property (插入点动画属性)

#### 新增内容
引入 `caret-animation` 属性，值为 `auto` 和 `manual`，以防止默认的插入点闪烁干扰 `caret-color` 的动画。

#### 技术细节
`auto` 保持浏览器默认的闪烁；`manual` 禁用默认闪烁，使颜色动画可以平滑运行。

#### 适用场景
在自定义输入动画或编辑器 UI 中可靠地对插入点颜色进行动画处理。

#### 参考资料
- [跟踪 bug #329301988](https://issues.chromium.org/issues/329301988)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5082469066604544)
- [规范](https://drafts.csswg.org/css-ui/#caret-animation)

### highlightsFromPoint API (高亮点检测 API)

#### 新增内容
添加了一个 API，用于检测文档某点处的自定义高亮，包括 shadow DOM 内和重叠的高亮区域。

#### 技术细节
该 API 返回与某点相交的高亮，使得可以以编程方式与 CSS Highlight API 模型交互。

#### 适用场景
需要解析指针位置上存在哪些语义高亮或构建精确高亮交互的工具和编辑器。

#### 参考资料
- [跟踪 bug #365046212](https://issues.chromium.org/issues/365046212)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4552801607483392)
- [规范](https://drafts.csswg.org/css-highlight-api-1/#interactions)

### `ScrollIntoView` container option (ScrollIntoView 的容器选项)

#### 新增内容
为 `ScrollIntoViewOptions` 添加了 `container` 选项，以将滚动限制在最近的祖先滚动容器内。

#### 技术细节
当使用 `container` 时，仅会滚动最近的滚动容器以将目标置入视口；不会执行更高层级的滚动。

#### 适用场景
组件范围内的滚动（例如虚拟化列表或嵌套滚动容器），作者希望避免滚动整个视口时适用。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5100036528275456)
- [规范](https://drafts.csswg.org/cssom-view/#dom-scrollintoviewoptions-container)

### View transitions: Inherit more animation properties (视图过渡：继承更多动画属性)

#### 新增内容
视图过渡现在通过 view-transition 伪元素树继承额外的动画属性：`animation-timing-function`、`animation-iteration-count`、`animation-direction` 和 `animation-play-state`。

#### 技术细节
这些属性传播到过渡伪元素，以便在视图过渡期间更好地匹配源元素动画语义。

#### 适用场景
在使用 View Transitions API 时，可创建更一致的交叉淡入/淡出和运动效果，保留动画行为。

#### 参考资料
- [跟踪 bug #427741151](https://issues.chromium.org/issues/427741151)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5154752085884928)
- [规范](https://www.w3.org/TR/css-view-transitions-2)

### View transition pseudos inherit animation-delay. (视图过渡伪元素继承 animation-delay)

#### 新增内容
`animation-delay` 现在通过 view transition 伪元素树继承，以便源元素上的延迟适用于过渡伪元素。

#### 技术细节
`animation-delay` 的传播使伪元素与源动画在视图过渡期间对齐定时。

#### 适用场景
在依赖延迟的视图过渡中，可保留预期的动画定时。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5424291457531904)
- [规范](https://www.w3.org/TR/css-view-transitions-2)

### Nested view transitions groups (嵌套视图过渡组)

#### 新增内容
视图过渡可以生成嵌套的伪元素树，而不是平铺的树，从而能够更逼真地重现元素嵌套关系。

#### 技术细节
嵌套伪树允许嵌套裁剪、3D 变换，以及在视图过渡中正确应用诸如不透明度和遮罩等效果。

#### 适用场景
依赖嵌套变换、裁剪或堆叠上下文的复杂 UI 过渡，可以从更准确的视觉保真中受益。

#### 参考资料
- [跟踪 bug #399431227](https://issues.chromium.org/issues/399431227)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5162799714795520)
- [规范](https://www.w3.org/TR/css-view-transitions-2/#view-transition-group-prop)

### Propagate viewport `overscroll-behavior` from root (将视口的 overscroll-behavior 从根元素传播)

#### 新增内容
`overscroll-behavior` 现在从根元素（`<html>`）传播到视口，以符合 CSS 工作组的决议。

#### 技术细节
此更改不再依赖 `<body>` 来进行视口传播，而是使用根元素作为视口级 `overscroll-behavior` 的来源。

#### 适用场景
在页面和组件间提供更可预测的超滚动行为；作者应在 `:root`/`<html>` 上应用视口级控制。

#### 参考资料
- [跟踪 bug #41453796](https://issues.chromium.org/issues/41453796)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6210047134400512)
- [规范](https://drafts.csswg.org/css-overscroll-behavior-1)

### CSS `counter()` and `counters()` in alt text of `content` property (在 `content` 属性的替代文本中支持 `counter()` 与 `counters()`)

#### 新增内容
现在可以在 `content` 属性的替代文本部分使用 `counter()` 与 `counters()`，从而生成更丰富的可访问文本。

#### 技术细节
`content` 属性的替代文本子系统接受计数器函数，允许在生成的内容中包含动态计数器值。

#### 适用场景
改善生成内容（如列表或带注释的项）的可访问性，其中计数器用于传达语义顺序或编号。

#### 参考资料
- [跟踪 bug #417488055](https://issues.chromium.org/issues/417488055)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5185442420621312)
- [规范](https://drafts.csswg.org/css-content/#content-property)

### CSS `scroll-target-group` property (滚动目标分组属性)

#### 新增内容
引入 `scroll-target-group`，用于将元素标记为滚动标记组容器，值包括 `none` 和 `auto` 等。

#### 技术细节
该属性控制滚动标记的分组形成，遵循 CSS Overflow Module Level 5 草案。

#### 适用场景
作者可以控制滚动标记分组，以影响滚动捕捉、标记或容器组之间的相关滚动行为。

#### 参考资料
- [跟踪 bug #6607668](https://issues.chromium.org/issues/6607668)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5189126177161216)
- [规范](https://drafts.csswg.org/css-overflow-5/#scroll-target-group)

### Support `font-variation-settings` descriptor in `@font-face` rule (在 `@font-face` 规则中支持 `font-variation-settings` 描述符)

#### 新增内容
在 Chromium 中为 `@font-face` 规则内部的基于字符串的 `font-variation-settings` 描述符添加了支持。

#### 技术细节
该描述符允许作者在字体声明时指定默认的可变字体轴设置，而不仅仅通过元素级属性进行设置。

#### 适用场景
通过使作者能够注册具有特定变体轴默认值的 @font-face 变体，提高排版控制与渲染一致性。

#### 参考资料
- [跟踪 bug #40398871](https://issues.chromium.org/issues/40398871)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5221379619946496)
- [规范](https://www.w3.org/TR/css-fonts-4/#font-rend-desc)

已保存到：digest_markdown/webplatform/CSS/chrome-140-stable-en.md