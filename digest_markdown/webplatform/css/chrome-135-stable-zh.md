# 领域摘要

Chrome 135 带来了大量 CSS 增强，重点提升了交互式 UI 元素、布局灵活性和高级样式能力。主要主题包括：为可滚动界面扩展伪元素支持、引入新的逻辑属性以支持国际化，以及更具表现力的形状与定位工具。这些更新让开发者能够更轻松地创建更丰富、更易访问、更具适应性的网页体验，减少对 JavaScript 或复杂变通方案的依赖。通过紧密对齐不断演进的 CSS 规范，Chrome 135 推动了 Web 平台在实现现代、高性能和视觉吸引力应用方面的能力。

## 详细更新

以下是 Chrome 135 中每项新 CSS 功能的详细分解，突出其技术细节和实际开发者收益。

### `::column` pseudo-element for carousels（用于轮播的 `::column` 伪元素）

#### 新增内容
允许使用 `::column` 伪元素为生成的列片段应用有限的样式，特别适用于多列布局和轮播组件。

#### 技术细节
`::column` 伪元素可在布局后为列片段设置样式，但仅限于不会影响布局本身的属性。这确保了性能和可预测性。

#### 适用场景
- 为轮播或多列文本布局中的列设置背景或边框样式。
- 增强视觉分隔效果，同时不影响内容流或重排。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5192332683771904)

---

### `::scroll-button()` pseudo-elements（`::scroll-button()` 伪元素）

#### 新增内容
引入交互式滚动按钮伪元素，如 `::scroll-button(inline-start)` 和 `::scroll-button(inline-end)`，用于可滚动容器。

#### 技术细节
开发者可直接在 CSS 中定义滚动按钮的内容和样式，实现无需自定义 JavaScript 的原生滚动控制。

#### 适用场景
- 为轮播或溢出容器添加可访问、可自定义的滚动按钮。
- 改善横向或纵向可滚动内容的导航体验。

#### 参考资料
- [跟踪问题 #370067113](https://issues.chromium.org/issues/370067113)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5093129273999360)
- [规范](https://drafts.csswg.org/css-overflow-5/#scroll-buttons)

---

### `::scroll-marker` and `::scroll-marker-group`（`::scroll-marker` 和 `::scroll-marker-group`）

#### 新增内容
为滚动容器新增 `::scroll-marker` 和 `::scroll-marker-group` 伪元素，可为关联项提供可聚焦的标记。

#### 技术细节
这些伪元素允许开发者在可滚动区域内直观地指示和设置滚动位置或项目分组的样式。

#### 适用场景
- 为长列表中的章节、部分或项目创建可视化标记。
- 在复杂滚动容器中提升导航性和可访问性。

#### 参考资料
- [跟踪问题 #332396355](https://issues.chromium.org/issues/332396355)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5160035463462912)
- [规范](https://drafts.csswg.org/css-overflow-5/#scroll-markers)

---

### CSS Inertness—the `interactivity` property（CSS 惰性——`interactivity` 属性）

#### 新增内容
引入 `interactivity` 属性，用于控制元素及其后代是否为惰性（不可交互）。

#### 技术细节
设置 `interactivity: none` 后，元素将无法聚焦、编辑、选择，并从可访问性树和页面查找结果中移除。

#### 适用场景
- 临时禁用模态对话框或遮罩层中的 UI 区域。
- 通过管理焦点和交互状态，提升可访问性和用户体验。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5107436833472512)
- [规范](https://github.com/flackr/carousel/tree/main/inert)

---

### CSS logical overflow（CSS 逻辑溢出）

#### 新增内容
新增 `overflow-inline` 和 `overflow-block` 属性，用于按逻辑方向控制溢出，适应不同书写模式。

#### 技术细节
`overflow-inline` 和 `overflow-block` 会根据文档的书写模式映射到 `overflow-x` 和 `overflow-y`，更好地支持国际化。

#### 适用场景
- 创建能无缝适应不同语言和书写方向的布局。
- 在多语言应用中减少条件 CSS 的需求。

#### 参考资料
- [跟踪问题 #41489999](https://issues.chromium.org/issues/41489999)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4728308937523200)
- [规范](https://drafts.csswg.org/css-overflow-3/#overflow-control)

---

### CSS anchor positioning remembered scroll offset（CSS 锚点定位记忆滚动偏移）

#### 新增内容
支持锚点定位的“记忆滚动偏移”，提升定位元素对滚动的响应能力。

#### 技术细节
当元素在锚点与其包含块之间锚定和连接时，滚动偏移会被纳入尺寸计算，从而实现更可预测的定位效果。

#### 适用场景
- 工具提示、弹出框或下拉菜单在滚动事件中保持正确定位。
- 需要精确跟踪锚点元素的复杂 UI 覆盖层。

#### 参考资料
- [跟踪问题 #373874012](https://issues.chromium.org/issues/373874012)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4710507824807936)
- [规范](https://drafts.csswg.org/css-anchor-position-1/#scroll)

---

### CSS `shape()` function（CSS `shape()` 函数）

#### 新增内容
引入 `shape()` 函数，可在 `clip-path` 中定义响应式、自由形状。

#### 技术细节
`shape()` 接受与 `path()` 类似的动词，但支持响应式单位（如 `%`、`vw`）和 CSS 自定义属性，实现动态、可适应的形状。

#### 适用场景
- 为图片或 UI 元素创建复杂、响应式的遮罩和裁剪路径。
- 通过流畅、可适应的形状增强视觉设计。

#### 参考资料
- [跟踪问题 #40829059](https://issues.chromium.org/issues/40829059)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5172258539307008)
- [规范](https://drafts.csswg.org/css-shapes-2/#shape-function)

---

### `safe-area-max-inset-*` variables（`safe-area-max-inset-*` 变量）

#### 新增内容
新增 `max-area-safe-inset-*` CSS 环境变量，表示最大可能的安全区域内边距。

#### 技术细节
这些变量保持不变，使布局能够预判最大安全区域（如刘海或圆角），无需因安全区域变化而触发重排。

#### 适用场景
- 设计能平滑适应设备安全区域的页脚或页眉。
- 防止在具有动态安全区域内边距的设备上出现不必要的布局跳动。

#### 参考资料
- [跟踪问题 #391621941](https://issues.chromium.org/issues/391621941)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6393888941801472)
- [规范](https://drafts.csswg.org/css-env-1/#safe-area-max-insets)

---

### Nested pseudo elements styling（嵌套伪元素样式）

#### 新增内容
支持为嵌套在其他伪元素内的伪元素设置样式，如 `::before::marker` 和 `::after::marker`。

#### 技术细节
该功能允许更细致、丰富地为列表标记和其他生成内容设置样式，未来还将支持更多组合。

#### 适用场景
- 在生成内容中自定义列表标记，实现高级排版效果。
- 满足以往需额外标记或脚本才能实现的设计需求。

#### 参考资料
- [跟踪问题 #373478544](https://issues.chromium.org/issues/373478544)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5199947786616832)
- [规范](https://www.w3.org/TR/css-pseudo-4/#marker-pseudo)