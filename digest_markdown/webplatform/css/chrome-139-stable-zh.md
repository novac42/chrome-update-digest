---
layout: default
title: Chrome 139 稳定版 – CSS 更新摘要
---

````markdown
保存至：`digest_markdown/webplatform/css/chrome-139-stable-zh.md`

---

# Chrome 139 稳定版 – CSS 更新摘要

## 1. 执行摘要

Chrome 139 在 CSS 方面带来了重要进展，重点提升了字体特性支持、新的自定义函数能力、更丰富的圆角形状，以及与最新规范的更好对齐。亮点包括对 CSS 自定义函数、`font-width` 属性、高级圆角形状（如 `superellipse` 和 `squircle`）的支持，以及过渡和滚动锚定行为的优化。这些更新共同为开发者在现代网页设计中提供了更强的表现力、性能和标准兼容性。

## 2. 主要影响

### 技术影响

- **现有实现**：大多数更改为新增或标准对齐，破坏性较小，但需关注属性和描述符的更新（如 `font-width` 与 `font-stretch`）。
- **新能力**：开发者现在可利用自定义 CSS 函数、高级字体特性和丰富的圆角形状，实现更具表现力的 UI 和排版。
- **技术债务**：应审查并更新对 `font-stretch` 等属性的遗留用法，以保持前向兼容性。

## 3. 风险评估

**关键风险**：
- 本次发布未发现明确的破坏性更改或安全问题。

**中等风险**：
- **弃用**：`font-stretch` 现为遗留别名，继续依赖可能导致未来兼容性问题。
- **性能影响**：异步 SVG 脚本和新 CSS 函数的引入，若管理不当，可能影响渲染或脚本执行时机。

## 4. 推荐操作

### 立即行动

- 检查代码库中 `font-stretch` 的使用，并开始迁移至 `font-width`。
- 在非关键 UI 组件中尝试新的圆角形状和自定义函数特性。
- 在复杂布局中复查过渡和滚动锚定行为。

### 短期规划

- 更新样式指南和组件库，纳入新 CSS 特性。
- 关注其他引擎对这些特性的兼容性表。
- 向团队成员讲解自定义函数和高级字体描述符的影响。

### 长期策略

- 用标准对齐的属性和描述符逐步替换遗留 CSS 模式。
- 制定渐进增强策略，充分利用新 CSS 能力。
- 跟踪 CSS 规范的持续变化，提前预判未来浏览器更新。

## 5. 特性分析

---

### Short-circuiting `var()` and `attr()`

**影响级别**：🟡 重要

**变更内容**：
当未采用回退值时，`var()` 和 `attr()` 函数现在会在不查找回退中的循环的情况下进行求值，从而提升效率和可预测性。

**意义**：
该更改优化了 CSS 变量和属性函数的求值过程，减少了不必要的计算和循环依赖问题的可能性。

**实施建议**：
- 优化 CSS，尽量避免在 `var()` 和 `attr()` 中使用不必要的回退。
- 测试此前回退循环可能掩盖问题的边界情况。

**参考资料**：
- [ChromeStatus.com entry](https://chromestatus.com/feature/6212939656462336)

---

### Support `font-feature-settings` descriptor in `@font-face` rule

**影响级别**：🟡 重要

**变更内容**：
Chrome 现已支持 CSS Fonts Level 4 中 `@font-face` 的基于字符串的 `font-feature-settings` 语法。无效或无法识别的标签会被忽略，仅支持标准形式。

**意义**：
可在字体声明中实现更细致的排版控制，与现代字体技术和规范保持一致。

**实施建议**：
- 在 `@font-face` 中使用字符串形式的 `font-feature-settings` 实现高级排版。
- 校验特性标签的正确性，避免静默失效。

**参考资料**：
- [Tracking bug #40398871](https://issues.chromium.org/issues/40398871)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5102801981800448)
- [Spec](https://www.w3.org/TR/css-fonts-4/#font-rend-desc)

---

### CSS custom functions

**影响级别**：🔴 严重

**变更内容**：
自定义函数允许作者定义可复用的 CSS 逻辑，可基于参数、其他自定义属性及条件返回值。

**意义**：
这是实现动态、DRY（Don't Repeat Yourself）CSS 的重要一步，使样式表更易维护且更具表现力。

**实施建议**：
- 在重复或参数化样式逻辑中尝试使用自定义函数进行原型开发。
- 针对尚不支持该特性的浏览器，确保有回退方案。

**参考资料**：
- [Tracking bug #325504770](https://issues.chromium.org/issues/325504770)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5179721933651968)
- [Spec](https://drafts.csswg.org/css-mixins-1/#defining-custom-functions)

---

### Continue running transitions when switching to initial transition value

**影响级别**：🟡 重要

**变更内容**：
与过渡相关的属性更改现在只影响新启动的过渡，进行中的过渡不会受影响，除非其动画属性发生变化。

**意义**：
提升了动画的可预测性，并与 CSS Transitions 规范保持一致，减少了动画意外中断的情况。

**实施建议**：
- 检查过渡逻辑，确保动态更新过渡属性时行为符合预期。
- 测试复杂动画序列的一致性。

**参考资料**：
- [ChromeStatus.com entry](https://chromestatus.com/feature/5194501932711936)
- [Spec](https://www.w3.org/TR/css-transitions-1/#starting)

---

### Corner shaping (`corner-shape`, `superellipse`, `squircle`)

**影响级别**：🟡 重要

**变更内容**：
新增对超越 `border-radius` 的高级圆角形状支持，包括 superellipse 和 squircle，并支持它们之间的动画。

**意义**：
为 UI 设计解锁了更多创意空间，可实现更自然和美观的形状。

**实施建议**：
- 在设计原型中尝试使用 `corner-shape` 及相关属性。
- 使用复杂形状时，注意可访问性和渲染性能。

**参考资料**：
- [Tracking bug #393145930](https://issues.chromium.org/issues/393145930)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5357329815699456)
- [Spec](https://drafts.csswg.org/css-borders-4/#corner-shaping)

---

### Add `font-width` property and descriptor and make `font-stretch` a legacy alias

**影响级别**：🟡 重要

**变更内容**：
Chrome 现将 `font-width` 作为标准属性识别，`font-stretch` 降为遗留别名，与当前规范保持一致。

**意义**：
确保与 CSS Fonts 规范及其他浏览器的一致性，减少跨浏览器差异。

**实施建议**：
- 将样式表中的 `font-stretch` 更新为 `font-width`。
- 迁移过程中关注渲染差异。

**参考资料**：
- [Tracking bug #356670472](https://issues.chromium.org/issues/356670472)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5190141555245056)

---

### Support async attribute for SVG `<script>` element

**影响级别**：🟢 可选

**变更内容**：
SVG `<script>` 元素现已支持 `async` 属性，可实现类似 HTML 的异步脚本执行。

**意义**：
通过非阻塞脚本执行，提升了 SVG 密集型应用的性能和响应速度。

**实施建议**：
- 当脚本执行顺序不重要时，在 SVG 脚本中使用 `async`。
- 测试 SVG 脚本中的竞态条件或依赖关系。

**参考资料**：
- [Tracking bug #40067618](https://issues.chromium.org/issues/40067618)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6114615389585408)
- [Spec](https://svgwg.org/svg2-draft/interact.html#ScriptElement:~:text=%E2%80%98script%E2%80%99%20element-,SVG%202%20Requirement%3A,Consider%20allowing%20async/defer%20on%20%E2%80%98script%E2%80%99.,-Resolution%3A)

---

### The `request-close` invoker command

**影响级别**：🟢 可选

**变更内容**：
对话框元素现在可通过 `requestClose()` JavaScript 函数关闭，会触发取消事件，开发者可根据需要阻止关闭。

**意义**：
为对话框生命周期和用户交互提供了更细致的控制，提升可访问性和用户体验。

**实施建议**：
- 对需条件关闭逻辑的对话框使用 `requestClose()`。
- 确保取消事件处理程序健壮且可访问。

**参考资料**：
- [Tracking bug #400647849](https://issues.chromium.org/issues/400647849)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5592399713402880)
- [Spec](https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-command-request-close-state)

---

### Scroll anchoring priority candidate fix

**影响级别**：🟡 重要

**变更内容**：
滚动锚定算法现在会选择屏幕上最深的元素作为锚点，提升动态内容变更时的滚动稳定性。

**意义**：
减少了意外的滚动跳动，尤其是在内容丰富或动态更新的布局中。

**实施建议**：
- 在动态或无限滚动界面中测试滚动行为。
- 如滚动锚定变化影响用户体验，调整布局策略。

**参考资料**：
- [ChromeStatus.com entry](https://chromestatus.com/feature/5070370113323008)

---
````