---
layout: default
title: css-zh
---

## 领域摘要

Chrome 142 继续改进以 CSS 为驱动的 UI 和交互面，重点包括 view transitions、scroll-marker 伪类、style-query 的表达能力以及表单控件在各平台间的渲染一致性。此版本强调与规范对齐的行为（例如 `::view-transition` 定位和 SVG `<a download>`），新增面向作者的入口点（`activeViewTransition`、`interestfor`），以及更丰富的条件样式（style queries 的范围语法和 `if()`）。这些更改让开发者对过渡、响应式行为和跨设备一致渲染拥有更细粒度的控制，推进 Web 平台朝向更可预测、声明式的 UI 模式发展。

## 详细更新

下面是本次发布中每项 CSS 领域更改的简洁、面向开发者的分解。

### Absolute positioning for the `::view-transition` element

#### 新增内容
CSS WG 将根 view-transition 伪元素的指定定位由 `fixed` 改为 `absolute`，Chrome 已实现该更改。

#### 技术细节
`::view-transition` 伪子树是 View Transitions API 使用的根。定位的变化会影响视图切换期间的布局和堆叠行为，并使 Chrome 与更新后的规范决策保持一致。

#### 适用场景
在视图切换期间获得更可预测的布局，尤其是在将过渡与周围布局集成或依赖过渡伪件的绝对定位语义时。

#### 参考资料
- [跟踪错误 #439800102](https://issues.chromium.org/issues/439800102)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6155213736116224)  
- [规范](https://github.com/w3c/csswg-drafts/issues/12116)

### activeViewTransition property on document

#### 新增内容
在 `document` 上公开了新的 `activeViewTransition` 属性，用于暴露通过 `startViewTransition()` 启动的活动视图过渡对象。

#### 技术细节
`startViewTransition()` 返回一个过渡对象，该对象暴露 promise 和方法以跟踪/操作过渡进度；`document.activeViewTransition` 提供了一个以编程方式观察当前过渡状态的入口点。

#### 适用场景
单页应用和框架可以在无需在组件间传递过渡对象的情况下监控或协调全局过渡状态，从而集中处理覆盖层、动画或中断处理逻辑。

#### 参考资料
- [跟踪错误 #434949972](https://issues.chromium.org/issues/434949972)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5067126381215744)  
- [规范](https://drafts.csswg.org/css-view-transitions-2)

### `:target-before` and `:target-after` pseudo-classes

#### 新增内容
新增伪类 `:target-before` 和 `:target-after`，用于匹配位于同一 scroll-marker 组内相对于活动滚动标记（`:target-current`）在 flat tree order 之前或之后的滚动标记。

#### 技术细节
这些选择器作用于滚动标记，并使用 flat tree order 来确定相对于活动标记的前序或后序标记，使作者能够根据当前滚动目标对项进行样式化。

#### 适用场景
相对于导航目标为容器中的前/后项设置样式（例如高亮当前项并淡化前后项），改善与滚动位置相关的导航体验。

#### 参考资料
- [跟踪错误 #440475008](https://issues.chromium.org/issues/440475008)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5120827674722304)  
- [规范](https://drafts.csswg.org/css-overflow-5/#active-before-after-scroll-markers)

### Range syntax for style container queries and `if()`

#### 新增内容
Chrome 在样式查询和 `if()` 函数中添加了对范围语法的支持，允许使用比较（例如 `>`、`<`）而不仅限于精确值匹配。

#### 技术细节
样式查询现在可以针对自定义属性或字面值表达范围和比较，将条件样式从等值检查扩展到符合 conditional spec typedef 的 style-range 所定义的更广泛情形。

#### 适用场景
基于数值阈值适配的响应式组件样式（例如在容器尺寸落在某个范围时应用样式），无需使用 JS 即可实现更具表达力的条件规则。

#### 参考资料
- [跟踪错误 #408011559](https://issues.chromium.org/issues/408011559)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5184992749289472)  
- [规范](https://drafts.csswg.org/css-conditional-5/#typedef-style-range)

### Interest Invokers (the `interestfor` attribute)

#### 新增内容
在 `<button>` 和 `<a>` 元素上可使用 `interestfor` 属性，将这些元素选择加入用户“interest”检测，进而对目标元素触发动作。

#### 技术细节
当用户“表示兴趣”（由用户代理检测）时，通过 `interestfor` 指定的行为会对引用的目标调用动作，例如在目标上显示弹出框；具体的兴趣手势由用户代理决定。

#### 适用场景
用于声明式触发上下文 UI（例如在悬停/聚焦/预览时显示弹出框、预览或临时 UI），无需在 JavaScript 中自定义事件绑定。

#### 参考资料
- [跟踪错误 #326681249](https://issues.chromium.org/issues/326681249)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4530756656562176)  
- [规范](https://github.com/whatwg/html/pull/11006)

### Mobile and desktop parity for select element rendering modes

#### 新增内容
Chrome 致力于在移动端与桌面端之间实现 `<select>` 渲染模式（页面内 listbox 与 button+popup）的一致性，这些模式由 `size` 和 `multiple` 控制。

#### 技术细节
`size` 和 `multiple` 属性决定 `<select>` 是渲染为页面内的 listbox 还是作为打开弹出框的按钮；此次更新解决了这些模式在移动端与桌面端可用性不一致的问题。

#### 适用场景
作者可以在不同设备上依赖一致的 `<select>` 行为，改进响应式表单并减少平台特定的变通方案。

#### 参考资料
- [跟踪错误 #439964654](https://issues.chromium.org/issues/439964654)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5412736871825408)  
- [规范](https://github.com/whatwg/html/pull/11460)

### Support `download` attribute in SVG `<a>` element

#### 新增内容
Chromium 为 SVGAElement 实现了 `download` 属性，使其行为与 SVG 2 规范一致。

#### 技术细节
SVG `<a>` 元素上的 `download` 属性指示用户代理下载超链接目标而不是导航到它，这与现有的 HTML 锚点行为和 SVG2 的 linking 接口相一致。

#### 适用场景
直接从 SVG 文档提供可下载的链接资源（例如资源或生成内容），无需额外脚本。

#### 参考资料
- [跟踪错误 #40589293](https://issues.chromium.org/issues/40589293)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6265596395913216)  
- [规范](https://svgwg.org/svg2-draft/linking.html#InterfaceSVGAElement)
