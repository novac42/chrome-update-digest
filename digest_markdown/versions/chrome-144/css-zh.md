---
layout: default
title: Chrome 144 Stable - CSS 更新
---

# Chrome 144 Stable - CSS 更新

## 领域摘要

Chrome 144 带来了一套全面的 CSS 增强功能，专注于改进开发者对视觉呈现、滚动行为和动态样式的控制。该版本包含 10 个 CSS 特性，提升了可访问性、布局定位和动画能力。主要亮点包括通过高亮伪元素实现的页面查找自定义、支持变换的增强型锚点定位，以及用于输入自定义的新 `caret-shape` 属性。这些更新反映了平台持续致力于为开发者提供更精细的用户界面样式控制，同时保持与现代 CSS 规范的强力对齐并解决长期存在的兼容性问题。

## 详细更新

Chrome 144 的 CSS 更新涵盖多个类别，从可访问性改进到高级定位和动画特性。以下特性代表了可供 Web 开发者使用的 CSS 工具包的重要补充。

### CSS find-in-page highlight pseudos

#### 新增内容
此特性将页面内查找的搜索结果样式作为高亮伪元素公开给开发者，类似于选择和拼写错误。开发者现在可以自定义用户使用浏览器查找功能时搜索结果的显示方式。

#### 技术细节
该特性提供了一个新的伪元素，允许修改页面内查找高亮的前景色和背景色，或添加文本装饰。这使开发者能够直接控制页面内搜索结果的呈现。

#### 适用场景
当浏览器默认的高亮颜色与页面颜色对比度不足或不适合时，此特性尤其有用。开发者可以确保页面内查找结果无论在何种网站配色方案下都保持可见和可访问，为具有自定义主题或特定可访问性需求的用户改善搜索体验。

#### 参考资料
- [跟踪错误 #339298411](https://issues.chromium.org/issues/339298411)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5195073796177920)
- [规范](https://drafts.csswg.org/css-pseudo-4/#selectordef-search-text)

### Non-tree-scoped container-name matching

#### 新增内容
容器名称现在可以跨 shadow DOM 边界匹配，在匹配 `@container` 查询的 `container-name` 时忽略树作用域。

#### 技术细节
以前，容器查询的 `container-name` 匹配使用树作用域名称或引用进行匹配。这意味着如果 `@container` 规则和 `container-type` 属性源自不同的树，例如 `container-type` 声明来自内部 shadow 树，则相同的名称不会匹配。通过此更改，无论 `@container` 规则或 `container-type` 声明的来源如何，容器名称都会匹配。

#### 适用场景
此更改使得在使用 Web 组件和 shadow DOM 时容器查询的行为更加可预测和直观。开发者现在可以跨组件边界使用容器查询，而无需担心树作用域的限制，使基于组件的架构更加灵活。

#### 参考资料
- [跟踪错误 #440049800](https://issues.chromium.org/issues/440049800)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5194034339512320)
- [规范](https://drafts.csswg.org/css-conditional-5/#container-name)

### CSS anchor positioning with transforms

#### 新增内容
当锚点定位元素与具有变换的锚点关联时，`anchor()` 和 `anchor-size()` 函数现在会根据变换后锚点的边界框进行解析。

#### 技术细节
此更新确保锚点定位计算正确考虑了变换的锚点或由具有变换的元素包含的锚点。定位系统现在使用变换后的边界框，而不是原始未变换的坐标。

#### 适用场景
此增强使开发者能够创建更复杂的布局，将 CSS 变换与锚点定位相结合，例如旋转或缩放的锚点与正确定位的工具提示或弹出窗口。它消除了以前阻止这些特性无缝协作的主要限制。

#### 参考资料
- [跟踪错误 #382294252](https://issues.chromium.org/issues/382294252)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5201048700583936)
- [规范](https://drafts.csswg.org/css-anchor-position-1/#anchor-position-size)

### CSS `caret-shape` property

#### 新增内容
新的 `caret-shape` 属性允许网站选择可编辑元素内文本光标的形状。可识别的属性值为 `auto`、`bar`、`block` 和 `underscore`。

#### 技术细节
在原生应用程序中，光标的形状最常见的是竖线、下划线或矩形块。此外，形状通常会根据输入模式而变化，例如插入或替换模式。此 CSS 属性将相同级别的控制带到了 Web 应用程序。

#### 适用场景
此特性对于文本编辑器、代码编辑器和其他具有富文本输入的应用程序很有价值，其中光标形状可以提供有关编辑模式的有意义的反馈。开发者现在可以创建与桌面应用程序视觉约定相匹配的基于 Web 的编辑器，或选择更适合其应用程序设计语言的光标样式。

#### 参考资料
- [跟踪错误 #353713061](https://issues.chromium.org/issues/353713061)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6106160780017664)
- [规范](https://drafts.csswg.org/css-ui/#caret-shape)

### SVG2 CSS cascading

#### 新增内容
Chrome 的实现现在与 SVG2 规范对 `<use>` 元素树中匹配 CSS 规则的定义对齐。

#### 技术细节
选择器现在匹配 `<use>` 实例化元素，而不是原始元素子树。这意味着选择器不再匹配克隆子树之外的祖先和兄弟元素。更重要的是，状态选择器（例如 `:hover`）现在开始在 `<use>` 实例中匹配。

#### 适用场景
此更改使通过 `<use>` 引用的 SVG 元素能够正确地应用交互式样式，例如悬停效果、焦点状态和其他以前无法正常工作的伪类样式。开发者现在可以创建更动态和交互式的 SVG 图形，其可重用组件能够按预期响应用户交互。

#### 参考资料
- [跟踪错误 #40550039](https://issues.chromium.org/issues/40550039)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5134266027606016)
- [规范](https://www.w3.org/TR/SVG2/struct.html#UseElement)

### Respect `overscroll-behavior` on non-scrollable scroll containers

#### 新增内容
`overscroll-behavior` 属性现在适用于所有滚动容器元素，无论这些元素当前是否具有溢出内容或用户是否可滚动。

#### 技术细节
开发者可以使用 `overscroll-behavior` 来防止 `overflow: hidden` 背景或 `overflow: auto` 元素上的滚动传播，而无需考虑它当前是否会溢出。即使容器当前不可滚动，该属性现在也会被遵守。

#### 适用场景
这简化了模态对话框、叠加层和其他 UI 模式，开发者希望防止滚动链接而无需动态检查内容是否溢出。它在不同的内容状态下提供了更可预测的滚动行为。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5129635997941760)
- [规范](https://www.w3.org/TR/css-overscroll-1/#propdef-overscroll-behavior)

### Respect `overscroll-behavior` for keyboard scrolls

#### 新增内容
当您将 `overscroll-behavior` 设置为 `auto` 以外的值时，浏览器现在除了鼠标和触摸滚动外，还会对键盘滚动遵守此设置。

#### 技术细节
浏览器对鼠标或触摸滚动遵守 `overscroll-behavior`，但键盘滚动以前会忽略它。此更改使键盘滚动也遵守 `overscroll-behavior`，确保所有滚动输入方法的行为一致。

#### 适用场景
这改善了可访问性并为键盘用户提供了一致的滚动行为。开发者不再需要单独的解决方法来防止键盘导航的滚动链接，使实现更简单且更易于维护。

#### 参考资料
- [跟踪错误 #41378182](https://issues.chromium.org/issues/41378182)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5099117340655616)
- [规范](https://www.w3.org/TR/css-overscroll-1)

### `@scroll-state` `scrolled` support

#### 新增内容
此特性允许开发者根据最近的滚动方向为容器的后代设置样式。

#### 技术细节
带有 `scrolled` 支持的 `@scroll-state` 条件规则使 CSS 能够对滚动状态更改做出反应，允许根据容器是否在特定方向上滚动进行动态样式设置。

#### 适用场景
开发者可以创建更具响应性和上下文感知的界面，根据滚动行为调整样式，例如显示或隐藏导航元素、根据滚动位置更改标题样式，或在不需要 JavaScript 的情况下提供有关滚动状态的视觉反馈。

#### 参考资料
- [跟踪错误 #414556050](https://issues.chromium.org/issues/414556050)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5083137520173056)
- [规范](https://drafts.csswg.org/css-conditional-5/#scrolled)

### Side-relative syntax for `background-position-x/y` longhands

#### 新增内容
开发者现在可以使用 `background-position-x` 和 `background-position-y` 长属性的新边缘相对语法，相对于其边缘之一定义背景图像位置。

#### 技术细节
此语法为开发者提供了更灵活和响应式的机制来定义背景图像位置，而不是使用需要适应窗口或框架大小的固定值。此特性还适用于 `-webkit-mask-position` 属性以确保 Web 兼容性。

#### 适用场景
此增强对于响应式设计特别有价值，其中背景图像需要与特定边缘对齐，无论容器大小如何。它消除了对 JavaScript 或媒体查询解决方法的需求，以实现边缘相对定位，使响应式背景定位完全声明化。

#### 参考资料
- [跟踪错误 #40468636](https://issues.chromium.org/issues/40468636)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5073321259565056)
- [规范](https://drafts.csswg.org/css-backgrounds-4/#background-position-longhands)

### View transitions `waitUntil()` method

#### 新增内容
`ViewTransition` 对象上的新 `waitUntil()` 方法通过接受一个 promise 来实现对视图过渡伪元素生命周期的高级控制，该 promise 会延迟伪树的销毁直到其完成。

#### 技术细节
视图过渡会自动构建一个伪元素树来显示和动画化参与的元素。根据规范，此子树在视图过渡开始动画时构建，并在与所有视图过渡伪元素关联的动画处于完成状态时销毁。然而，对于将视图过渡与滚动驱动动画关联等高级情况，子树需要在动画完成状态之后持续存在。`waitUntil()` 函数解决了这一需求。

#### 适用场景
一个关键示例是将视图过渡与滚动驱动动画关联。当滚动时间轴控制动画时，子树不应在动画完成时销毁，因为向后滚动应该仍然为伪元素设置动画。这使得能够以以前无法实现的方式结合多个 CSS 动画特性的复杂动画模式。

#### 参考资料
- [跟踪错误 #346976175](https://issues.chromium.org/issues/346976175)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4812903832223744)
- [规范](https://drafts.csswg.org/css-view-transitions-2/#dom-viewtransition-waituntil)
