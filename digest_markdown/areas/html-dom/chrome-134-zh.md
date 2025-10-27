---
layout: default
title: chrome-134-zh
---

### 1. 领域摘要

Chrome 134 在 HTML-DOM 的更新集中于为开发者提供对内置 UI 基元的更细粒度控制，并使 HTML 解析器对现实世界的标记更宽松。影响最大的更改是可通过 CSS 自定义 `<select>` 的呈现、解析器放宽以接受 `<select>` 内的更多标签，以及通过 `closedby` 属性为 `<dialog>` 引入新的轻量关闭控制。这些更新通过扩展基于 CSS 的自定义能力、使对话框行为与 Popover API 对齐，以及引入用于兼容性的过渡解析器策略来推动平台发展。开发者应注意解析器放宽在临时策略下受限，并在该策略结束前规划迁移。

## 详细更新

Below are the HTML-DOM changes in Chrome 134 that flow directly from the summary above.

### Customizable `<select>` Element（可自定义的 `<select>` 呈现）

#### 新增内容
Customizable `<select>` 允许开发者通过添加 `appearance: base-select` CSS 属性和值，完全控制 `<select>` 元素的呈现。该功能依赖于 `SelectParserRelaxation` 标志，该标志更改 HTML 解析器以允许在 `<select>` 内使用更多标签...

#### 技术细节
- CSS：引入 `appearance: base-select`，使 `<select>` 进入一个页面样式可以完全控制的可呈现基线。
- 解析器依赖：该功能依赖由 SelectParserRelaxation 标志暴露的解析器更改，以允许额外的子标签。
- 实现说明：该更改与 Chromium 特性门控绑定。

#### 适用场景
- 允许在保留原生表单语义的同时构建自定义样式的 select 控件。
- 支持需要对 select 呈现进行完全视觉控制的更丰富的 UI 组合。

#### 参考资料
- [跟踪问题 #40146374](https://issues.chromium.org/issues/40146374)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5737365999976448)
- [规范](https://github.com/whatwg/html/issues/9799)

### Select parser relaxation（解析器放宽）

#### 新增内容
此更改使 HTML 解析器允许在 `<select>` 中使用除了 `<option>`、`<optgroup>` 和 `<hr>` 之外的其他标签。该功能受临时策略（`SelectParserRelaxationEnabled`）控制。此为过渡期策略，且该策略将在 Chrome 141 之后停止生效。

#### 技术细节
- DOM/解析器：放宽解析器对 `<select>` 的允许内容模型，改变对畸形或扩展标记生成 DOM 树的方式。
- 策略：由名为 `SelectParserRelaxationEnabled` 的临时策略控制；开发者应准备在 Chrome 141 前该策略被移除。
- 兼容性：旨在作为过渡，以减少包含非标准子元素的现有页面的破坏性更改。

#### 适用场景
- 提高对在 `<select>` 内包含遗留或不合规范标记的页面的稳健性。
- 通过确保解析器允许更丰富的子结构来促进 `appearance: base-select` 的采用。

#### 参考资料
- [跟踪问题 #335456114](https://issues.chromium.org/issues/335456114)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5145948356083712)
- [规范](https://github.com/whatwg/html/pull/10557)

### Dialog light dismiss（对话框轻量关闭）

#### 新增内容
Popover API 的一项很好的特性是其轻量关闭行为。该行为现在成为 `<dialog>` 的一部分，新增的 `closedby` 属性可控制该行为：

  * `<dialog closedby="none">`：完全禁止用户触发的对话框关闭。
  * `<dialog closedby="closerequest">`：按下...

#### 技术细节
- Web API / DOM：在 `<dialog>` 上添加 `closedby` 内容属性以控制轻量关闭语义，使对话框行为与 Popover API 的交互模型保持一致。
- 可用性：提供一种声明式方式，使对话框可以选择是否响应用户触发的关闭手势。
- 互操作性：遵循 HTML 规范中关于该新属性的条目以标准化行为。

#### 适用场景
- 对是否让对话框响应外部点击、Escape 或其他关闭手势提供细粒度控制。
- 符合来自 Popover API 使用者的期望，使对话框行为更可预测。

#### 参考资料
- [跟踪问题 #376516550](https://issues.chromium.org/issues/376516550)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5097714453577728)
- [规范](https://html.spec.whatwg.org/#attr-dialog-closedby)
