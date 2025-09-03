```markdown
# Chrome 139 稳定版 - CSS 更新摘要

## 1. 执行摘要

Chrome 139 带来了多项重要的 CSS 增强，包括自定义函数、高级圆角造型、改进的字体特性支持，以及字体属性处理的更新。这些变更使 Chrome 更加贴合不断发展的 CSS 规范，提升设计灵活性，并改善与其他浏览器的互操作性。开发者获得了布局、排版和动画的新表达工具，同时部分旧有行为因标准合规性被弃用。

## 2. 关键影响

### 技术影响

- **现有实现**：字体属性使用和过渡行为可能需做小幅调整。建议检查对 `font-stretch` 的旧有依赖。
- **新能力**：自定义 CSS 函数、超级椭圆/圆角造型，以及异步 SVG 脚本扩展了设计和性能选项。
- **技术债务**：弃用或旧有特性（如 `font-stretch` 别名）应重构，以避免未来兼容性问题。

## 3. 风险评估

**关键风险**：
- 未发现重大破坏性更改，但若从 `font-stretch` 迁移到 `font-width` 不当，可能导致渲染不一致。
- 安全性：本次发布无直接 CSS 相关安全问题。

**中等风险**：
- 弃用旧字体属性别名可能影响老旧代码库。
- 性能：异步 SVG 脚本和滚动锚定算法变更在边缘场景下可能影响渲染性能。

## 4. 推荐措施

### 立即行动

- 检查 `font-stretch` 的使用，并在适当情况下迁移到 `font-width`。
- 在预发布环境测试自定义函数和圆角造型特性。
- 检查依赖属性变更的动画过渡行为。

### 短期规划

- 更新设计系统，利用新的圆角造型和字体特性设置。
- 重构 SVG 脚本，使用 async 属性提升性能。
- 在复杂布局中监控滚动锚定行为。

### 长期策略

- 所有字体属性使用与当前规范保持一致。
- 将自定义函数纳入可复用的 CSS 框架。
- 持续关注更多 CSS 混入和边框增强进展。

## 5. 特性分析

### Short-circuiting `var()` and `attr()`

**影响级别**：🟡 重要

**变更内容**：
`var()` 和 `attr()` 函数在未采用 fallback 时，将不再在 fallback 中查找循环引用。

**意义**：
提升 CSS 变量解析的性能和可预测性，减少不必要的计算。

**实施建议**：
- 重构复杂变量链以利用此优化。
- 测试此前 fallback 循环可能导致问题的边缘场景。

**参考资料**：
- [ChromeStatus.com entry](https://chromestatus.com/feature/6212939656462336)

---

### Support `font-feature-settings` descriptor in `@font-face` rule

**影响级别**：🟡 重要

**变更内容**：
`@font-face` 规则现已支持基于字符串的 `font-feature-settings` 语法，符合 CSS Fonts Level 4。无效标签将被忽略，仅接受标准形式。

**意义**：
实现更细致的排版控制和更好的 OpenType 特性支持，贴合现代字体使用需求。

**实施建议**：
- 在字体定义中使用字符串形式的 `font-feature-settings`。
- 校验特性标签以确保兼容性。

**参考资料**：
- [Tracking bug #40398871](https://issues.chromium.org/issues/40398871)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5102801981800448)
- [Spec](https://www.w3.org/TR/css-fonts-4/#font-rend-desc)

---

### CSS custom functions

**影响级别**：🔴 关键

**变更内容**：
自定义函数允许在 CSS 中通过参数、自定义属性和条件动态计算值。

**意义**：
极大提升 CSS 的表达力和复用性，可直接在样式表中实现高级设计模式和逻辑。

**实施建议**：
- 尝试用自定义函数实现主题和布局逻辑。
- 为不支持的浏览器准备 fallback 策略。

**参考资料**：
- [Tracking bug #325504770](https://issues.chromium.org/issues/325504770)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5179721933651968)
- [Spec](https://drafts.csswg.org/css-mixins-1/#defining-custom-functions)

---

### Continue running transitions when switching to initial transition value

**影响级别**：🟡 重要

**变更内容**：
过渡属性变更仅影响新过渡，现有动画在其动画属性未变时将继续运行。

**意义**：
提升动画一致性，并与 CSS Transitions 规范保持一致。

**实施建议**：
- 检查动画逻辑，确保过渡属性更新时行为符合预期。
- 测试动画持续性，避免意外的动画残留。

**参考资料**：
- [ChromeStatus.com entry](https://chromestatus.com/feature/5194501932711936)
- [Spec](https://www.w3.org/TR/css-transitions-1/#starting)

---

### Corner shaping (`corner-shape`, `superellipse`, `squircle`)

**影响级别**：🟡 重要

**变更内容**：
新增属性支持高级圆角造型（如超级椭圆、squircle 等），突破传统 `border-radius` 限制。

**意义**：
拓展 UI 元素设计可能性，支持现代美学和流畅形状过渡。

**实施建议**：
- 更新组件库以支持新圆角造型。
- 在 UI 效果中实现圆角造型动画。

**参考资料**：
- [Tracking bug #393145930](https://issues.chromium.org/issues/393145930)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5357329815699456)
- [Spec](https://drafts.csswg.org/css-borders-4/#corner-shaping)

---

### Add `font-width` property and descriptor and make `font-stretch` a legacy alias

**影响级别**：🟡 重要

**变更内容**：
Chrome 现已按规范识别 `font-width`，`font-stretch` 被弃用为旧有别名。

**意义**：
提升标准兼容性，并改善与其他浏览器的互操作性。

**实施建议**：
- 在所有样式表中用 `font-width` 替换 `font-stretch`。
- 测试字体渲染，确保各浏览器一致性。

**参考资料**：
- [Tracking bug #356670472](https://issues.chromium.org/issues/356670472)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5190141555245056)

---

### Support async attribute for SVG `<script>` element

**影响级别**：🟢 可选

**变更内容**：
SVG `<script>` 元素现已支持 async 属性，可实现异步脚本执行。

**意义**：
提升 SVG 性能和响应速度，尤其适用于交互式图形场景。

**实施建议**：
- 对非阻塞 SVG 脚本使用 async 属性。
- 测试与现有 SVG 工作流的兼容性。

**参考资料**：
- [Tracking bug #40067618](https://issues.chromium.org/issues/40067618)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6114615389585408)
- [Spec](https://svgwg.org/svg2-draft/interact.html#ScriptElement:~:text=%E2%80%98script%E2%80%99%20element-,SVG%202%20Requirement%3A,Consider%20allowing%20async/defer%20on%20%E2%80%98script%E2%80%99.,-Resolution%3A)

---

### The `request-close` invoker command

**影响级别**：🟢 可选

**变更内容**：
对话框现可通过 `requestClose()` JavaScript 函数关闭，并触发 cancel 事件以便开发者控制。

**意义**：
增强对话框管理和用户体验，支持更细致的关闭控制。

**实施建议**：
- 在自定义对话框流程中使用 `requestClose()`。
- 处理 cancel 事件以防止非预期关闭。

**参考资料**：
- [Tracking bug #400647849](https://issues.chromium.org/issues/400647849)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5592399713402880)
- [Spec](https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-command-request-close-state)

---

### Scroll anchoring priority candidate fix

**影响级别**：🟡 重要

**变更内容**：
滚动锚定算法现会选择屏幕上最深的元素作为锚点，提升滚动稳定性。

**意义**：
减少动态内容变更时意外滚动跳动，优化用户体验。

**实施建议**：
- 在动态布局中测试滚动行为。
- 若使用自定义滚动逻辑，调整锚点候选。

**参考资料**：
- [ChromeStatus.com entry](https://chromestatus.com/feature/5070370113323008)
```