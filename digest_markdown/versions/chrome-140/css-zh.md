---
layout: default
title: css-zh
---

## 区域摘要

Chrome 140 Stable 在 CSS 方面有若干改进，提升了精度（typed arithmetic）、动画控制（`caret-animation` 和扩展的 view-transition 继承）以及布局/滚动的可用性（`scroll-target-group`、container-scoped `scrollIntoView` 和 `overscroll-behavior` 的更改）。若干新增功能面向交互性与可访问性：`highlightsFromPoint`、在生成内容的替代文本中使用 `counter()`/`counters()`，以及在 `@font-face` 中对字体变体的更好支持。总体来看，这些更改为开发者在布局、动画和可访问性方面提供了更细粒度的控制，同时使 Chromium 与不断演进的 CSS 规范保持一致。

## 详细更新

Below are the CSS-focused changes in Chrome 140 Stable that follow from the summary above.

### CSS typed arithmetic（类型感知的运算）

#### 新增内容
Typed arithmetic 允许在 CSS 中编写诸如 `calc(10em / 1px)` 或 `calc(20% / 0.5em * 1px)` 的表达式，使得在 `calc` 表达式内可以在有类型和值无类型之间进行转换。

#### 技术细节
根据 CSS Values Level 4 规范实现了类型感知的 `calc` 表达式，以允许单位转换和尊重值类型的算术运算。

#### 适用场景
排版和响应式布局计算中，当需要在单位之间（例如 em 到 px）转换或将百分比与绝对单位结合时非常有用。

#### 参考资料
- https://issues.chromium.org/issues/40768696
- https://chromestatus.com/feature/4740780497043456
- https://www.w3.org/TR/css-values-4/#calc-type-checking

### CSS `caret-animation` property（光标动画属性）

#### 新增内容
引入了 `caret-animation` 属性，取值为 `auto` 和 `manual`，用于控制 `caret-color` 动画与默认光标闪烁之间的交互。

#### 技术细节
提供一种机制以禁用或保留浏览器默认的闪烁（`auto`），或选择手动控制（`manual`），以便动画化的 `caret-color` 转换不会被闪烁定时打断。

#### 适用场景
在编辑器、表单输入或自定义文本控件中平滑地动画化光标颜色，而不与闪烁行为冲突。

#### 参考资料
- https://issues.chromium.org/issues/329301988
- https://chromestatus.com/feature/5082469066604544
- https://drafts.csswg.org/css-ui/#caret-animation

### highlightsFromPoint API（高亮点查询 API）

#### 新增内容
新增 `highlightsFromPoint` API，用于查询文档某一点处存在哪些自定义高亮，包括 shadow DOM 内的高亮。

#### 技术细节
允许在坐标处精确检测重叠或嵌套的高亮，改进了对 CSS Highlight API 的程序化交互能力。

#### 适用场景
需要检查或操作指针下高亮的交互式注释工具、编辑器 UI 或可访问性覆盖层。

#### 参考资料
- https://issues.chromium.org/issues/365046212
- https://chromestatus.com/feature/4552801607483392
- https://drafts.csswg.org/css-highlight-api-1/#interactions

### `ScrollIntoView` container option（ScrollIntoView 的 container 选项）

#### 新增内容
为 ScrollIntoViewOptions 添加了 `container` 选项，以便仅滚动最近的祖先滚动容器来将目标元素带入可视区域。

#### 技术细节
将滚动进入视图的行为限定为最近的滚动容器，而不是视口或所有可滚动祖先。

#### 适用场景
组件库和可滚动控件需要在不影响外部页面滚动的情况下将元素带入可视区域。

#### 参考资料
- https://chromestatus.com/feature/5100036528275456
- https://drafts.csswg.org/cssom-view/#dom-scrollintoviewoptions-container

### View transitions: Inherit more animation properties（视图过渡：继承更多动画属性）

#### 新增内容
View transitions 现在通过伪树继承额外的动画属性：`animation-timing-function`、`animation-iteration-count`、`animation-direction` 和 `animation-play-state`。

#### 技术细节
扩展了视图过渡伪元素可继承的与动画相关的属性，使过渡更好地反映原始元素的动画行为。

#### 适用场景
在视图过渡中更一致且更具表现力地保留预期的定时、迭代、方向和播放状态语义。

#### 参考资料
- https://issues.chromium.org/issues/427741151
- https://chromestatus.com/feature/5154752085884928
- https://www.w3.org/TR/css-view-transitions-2

### View transition pseudos inherit animation-delay.（视图过渡伪元素继承 animation-delay。）

#### 新增内容
通过视图过渡伪树加入了对 `animation-delay` 的继承。

#### 技术细节
确保在视图过渡期间保留由 `animation-delay` 指定的动画开始偏移。

#### 适用场景
协调元素动画与视图过渡伪元素之间的延迟，以实现平滑的分阶段过渡。

#### 参考资料
- https://chromestatus.com/feature/5424291457531904
- https://www.w3.org/TR/css-view-transitions-2

### Nested view transitions groups（嵌套视图过渡组）

#### 新增内容
View transitions 可以生成嵌套的伪元素树，而非扁平结构，从而实现更真实的视觉呈现。

#### 技术细节
嵌套伪树允许按元素分层，支持裁剪、嵌套的 3D 变换，以及在组内正确应用效果（不透明度、蒙版等）。

#### 适用场景
需要视图过渡尊重元素叠放与裁剪语义的复杂界面，尤其是使用嵌套变换或蒙版的场景。

#### 参考资料
- https://issues.chromium.org/issues/399431227
- https://chromestatus.com/feature/5162799714795520
- https://www.w3.org/TR/css-view-transitions-2/#view-transition-group-prop

### Propagate viewport `overscroll-behavior` from root（从根元素传播视口的 overscroll-behavior）

#### 新增内容
视口的 `overscroll-behavior` 现在从根元素（`<html>`）传播，而不是从 `<body>`。

#### 技术细节
使 Chromium 与 CSSWG 的决议保持一致：视口属性应从根元素传播，而非 body，从而影响哪个元素的属性会作用于视口行为。

#### 适用场景
依赖 overscroll 控制（例如防止下拉刷新或链式滚动）的应用应在根元素上配置该行为以获得一致结果。

#### 参考资料
- https://issues.chromium.org/issues/41453796
- https://chromestatus.com/feature/6210047134400512
- https://drafts.csswg.org/css-overscroll-behavior-1

### CSS `counter()` and `counters()` in alt text of `content` property（在 `content` 属性的替代文本中支持 `counter()` 和 `counters()`）

#### 新增内容
允许在 `content` 的替代文本中使用 `counter()` 和 `counters()`，改善生成内容的语义表达。

#### 技术细节
扩展了内容生成允许的表达式，使计数器能够贡献到通过 `content` 定义的可访问替代文本中。

#### 适用场景
可访问的列表、有编号的说明和生成标签场景中，计数器应当向辅助技术暴露。

#### 参考资料
- https://issues.chromium.org/issues/417488055
- https://chromestatus.com/feature/5185442420621312
- https://drafts.csswg.org/css-content/#content-property

### CSS `scroll-target-group` property（scroll-target-group 属性）

#### 新增内容
引入了 `scroll-target-group` 属性，用于将元素标记为滚动标记组容器，其取值包括 `none` 和 `auto`。

#### 技术细节
定义了元素是否建立滚动标记组容器，从而影响滚动捕捉标记和相关行为的分组方式。

#### 适用场景
在复杂滚动布局和跨嵌套滚动容器的捕捉行为中，需要对滚动标记分组进行精细控制时使用。

#### 参考资料
- https://issues.chromium.org/issues/6607668
- https://chromestatus.com/feature/5189126177161216
- https://drafts.csswg.org/css-overflow-5/#scroll-target-group

### Support `font-variation-settings` descriptor in `@font-face` rule（在 `@font-face` 中支持 `font-variation-settings` 描述符）

#### 新增内容
在 `@font-face` 声明中添加了对基于字符串的 `font-variation-settings` 描述符的支持。

#### 技术细节
允许在 font-face 层级指定可变字体轴的默认值，从而在声明字体时配置字体变体轴。

#### 适用场景
嵌入的可变字体需要在 `@font-face` 中定义默认轴位置（如 weight/width/slant）以便在各元素间获得一致渲染。

#### 参考资料
- https://issues.chromium.org/issues/40398871
- https://chromestatus.com/feature/5221379619946496
- https://www.w3.org/TR/css-fonts-4/#font-rend-desc

已保存至: digest_markdown/webplatform/CSS/chrome-140-stable-en.md
