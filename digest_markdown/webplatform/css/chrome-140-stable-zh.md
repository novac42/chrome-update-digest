# Chrome 更新分析器 - 领域专家分析 (中文)

## 摘要

Chrome 140 稳定版引入了 11 项重要的 CSS 增强功能，专注于改进开发者控制能力、可访问性和高级样式功能。主要更新包括用于复杂计算的 CSS 类型化算术、光标动画控制、带有嵌套组和改进动画属性继承的增强视图过渡，以及新的滚动相关功能。此版本还通过内容替代文本中的计数器支持和正确的视口行为修复带来了重要的可访问性改进。

## 功能详情

### CSS typed arithmetic

**更改内容**:
此功能在 CSS 计算中启用类型化算术表达式，允许开发者编写复杂的表达式，如 `calc(10em / 1px)` 或 `calc(20% / 0.5em * 1px)`。这对于需要将类型化值转换为无类型值以便在接受数字的不同属性间重复使用的排版工作流程特别有用。该功能在保持 CSS 计算类型安全性的同时启用更复杂的数学运算。

**参考资料**:
- [跟踪问题 #40768696](https://issues.chromium.org/issues/40768696)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4740780497043456)
- [规范](https://www.w3.org/TR/css-values-4/#calc-type-checking)

### CSS `caret-animation` 属性

**更改内容**:
新的 `caret-animation` 属性提供对光标闪烁行为的控制，以防止干扰 `caret-color` 动画。该属性接受两个值：`auto`（默认浏览器闪烁行为）和 `manual`（开发者控制的动画，无自动闪烁）。这解决了动画光标颜色被浏览器默认闪烁机制干扰的问题。

**参考资料**:
- [跟踪问题 #329301988](https://issues.chromium.org/issues/329301988)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5082469066604544)
- [规范](https://drafts.csswg.org/css-ui/#caret-animation)

### highlightsFromPoint API

**更改内容**:
`highlightsFromPoint` API 使开发者能够通过检测特定文档坐标处存在哪些高亮来与自定义高亮进行交互。这为复杂高亮场景提供精确控制，其中多个高亮可能重叠或存在于 shadow DOM 中。该 API 对于构建需要基于点的高亮检测的复杂文本编辑和注释功能至关重要。

**参考资料**:
- [跟踪问题 #365046212](https://issues.chromium.org/issues/365046212)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4552801607483392)
- [规范](https://drafts.csswg.org/css-highlight-api-1/#interactions)

### `ScrollIntoView` container 选项

**更改内容**:
新的 `ScrollIntoViewOptions` container 选项允许开发者在使用 `scrollIntoView` 时将滚动限制为仅限最近的祖先滚动容器。这提供了对滚动行为的更细粒度控制，使开发者能够将元素显示在视图中而不影响直接祖先之外的父滚动容器。

**参考资料**:
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5100036528275456)
- [规范](https://drafts.csswg.org/cssom-view/#dom-scrollintoviewoptions-container)

### View transitions: 继承更多动画属性

**更改内容**:
视图过渡现在通过伪元素树继承额外的动画属性，包括 `animation-timing-function`、`animation-iteration-count`、`animation-direction` 和 `animation-play-state`。这项增强为开发者提供了对视图过渡动画更全面的控制，并确保整个过渡伪元素层次结构中动画行为的一致性。

**参考资料**:
- [跟踪问题 #427741151](https://issues.chromium.org/issues/427741151)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5154752085884928)
- [规范](https://www.w3.org/TR/css-view-transitions-2)

### View transition 伪元素继承 animation-delay

**更改内容**:
基于之前的动画属性继承改进，`animation-delay` 属性现在也通过视图过渡伪元素树继承。这完善了可在视图过渡伪元素间一致应用的动画属性集，为开发者提供对过渡动画的完整时间控制。

**参考资料**:
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5424291457531904)
- [规范](https://www.w3.org/TR/css-view-transitions-2)

### 嵌套视图过渡组

**更改内容**:
此功能允许视图过渡生成嵌套的伪元素树而不是扁平结构。这种架构改进使视图过渡能够更好地反映原始元素层次结构和视觉意图。它支持高级效果，如裁剪、嵌套 3D 变换，以及正确应用不透明度和遮罩效果，这些在扁平伪元素结构中是不可能实现的。

**参考资料**:
- [跟踪问题 #399431227](https://issues.chromium.org/issues/399431227)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5162799714795520)
- [规范](https://www.w3.org/TR/css-view-transitions-2/#view-transition-group-prop)

### 从根元素传播视口 `overscroll-behavior`

**更改内容**:
此更改通过将 `overscroll-behavior` 从根元素（`<html>`）而不是 `<body>` 元素传播到视口，使 Chrome 与 CSS 工作组决议保持一致。这标准化了视口属性传播行为，并确保与影响视口的其他 CSS 属性的一致性。

**参考资料**:
- [跟踪问题 #41453796](https://issues.chromium.org/issues/41453796)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6210047134400512)
- [规范](https://drafts.csswg.org/css-overscroll-behavior-1)

### CSS `counter()` 和 `counters()` 在 `content` 属性的替代文本中

**更改内容**:
这项可访问性增强允许在 `content` 属性的替代文本部分使用 `counter()` 和 `counters()` 函数。这使开发者能够提供更有意义和动态的替代文本，反映文档结构和编号，显著改善屏幕阅读器和其他辅助技术的可访问性。

**参考资料**:
- [跟踪问题 #417488055](https://issues.chromium.org/issues/417488055)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5185442420621312)
- [规范](https://drafts.csswg.org/css-content/#content-property)

### CSS `scroll-target-group` 属性

**更改内容**:
新的 `scroll-target-group` 属性指定元素是否建立滚动标记组容器。它接受值 'none'（无滚动标记组）和 'auto'（建立滚动标记组容器）。此属性是滚动驱动动画规范的一部分，支持更复杂的基于滚动的交互和动画。

**参考资料**:
- [跟踪问题 #6607668](https://issues.chromium.org/issues/6607668)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5189126177161216)
- [规范](https://drafts.csswg.org/css-overflow-5/#scroll-target-group)

### 在 `@font-face` 规则中支持 `font-variation-settings` 描述符

**更改内容**:
Chrome 现在支持 `@font-face` 声明中的 `font-variation-settings` 描述符，填补了可变字体支持的空白。虽然开发者之前可以调整元素上的字体变化，但无法在字体声明中指定默认变化设置。此功能支持字体变化设置的基于字符串的语法，在字体定义级别启用更复杂的排版控制。

**参考资料**:
- [跟踪问题 #40398871](https://issues.chromium.org/issues/40398871)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5221379619946496)
- [规范](https://www.w3.org/TR/css-fonts-4/#font-rend-desc)