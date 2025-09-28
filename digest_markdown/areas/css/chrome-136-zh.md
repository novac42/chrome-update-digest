---
layout: default
title: Chrome 136 CSS 更新 - 稳定版
---

# Chrome 136 CSS 更新 - 稳定版

## 区域概览

Chrome 136 带来了重要的 CSS 改进，重点关注打印样式、HDR 内容管理和访问链接样式的增强安全性。最具影响力的更改包括 `print-color-adjust` 的标准化（移除 webkit 前缀）、用于 HDR 显示器的新 `dynamic-range-limit` 属性，以及通过分区 `:visited` 链接历史记录改进隐私保护。这些更新在保持向后兼容性的同时，增强了 CSS 在打印媒体和现代显示技术方面的能力。该版本还包括对 CSS 自定义属性和属性函数的改进，展现了 CSS 基础功能的持续演进。

## 详细更新

Chrome 136 中的这些 CSS 更新涵盖了从新的 HDR 显示能力到重要的安全改进和标准化工作。

### The dynamic-range-limit property

#### 新功能
引入了一个新的 CSS 属性，允许网页限制 HDR（高动态范围）内容的最大亮度，为 HDR 兼容设备上的内容显示提供更好的控制。

#### 技术细节
该属性与 CSS Color HDR 规范配合使用，动态管理亮度级别。它使开发者能够设置 HDR 内容显示亮度的约束，确保在不同显示能力的设备上提供一致的观看体验。

#### 用例
特别适用于媒体丰富的应用程序、游戏网站和内容平台，其中控制 HDR 亮度对用户体验至关重要。有助于防止过亮的内容在某些显示器上造成不适或问题。

#### 参考资料
[跟踪 bug #1470298](https://bugs.chromium.org/p/chromium/issues/detail?id=1470298) | [ChromeStatus.com 条目](https://chromestatus.com/feature/5023877486493696) | [规范](https://www.w3.org/TR/css-color-hdr/#dynamic-range-limit)

### Partition :visited links history

#### 新功能
实现了一项重要的安全改进，对 `:visited` 伪类行为进行分区，以防止跨不同站点和源的浏览历史记录泄露。

#### 技术细节
锚元素现在只有在从相同的顶级站点和框架源点击过的情况下才会接收 `:visited` 样式。系统为"自链接"提供了例外，允许站点将指向自己页面的链接样式设置为 `:visited`，即使在该特定上下文中没有先前的点击。

#### 用例
此更改主要是安全增强，通过防止恶意站点检测用户访问过哪些外部站点来保护用户隐私。Web 开发者应测试其样式，确保访问链接外观在新的分区模型下按预期工作。

#### 参考资料
[跟踪 bug #1448609](https://bugs.chromium.org/p/chromium/issues/detail?id=1448609) | [ChromeStatus.com 条目](https://chromestatus.com/feature/5029851625472000) | [规范](https://www.w3.org/TR/css-pseudo-4/#visited-pseudo)

### Unprefixed print-color-adjust

#### 新功能
`print-color-adjust` 属性现在可以不使用 `-webkit-` 前缀，这标志着向标准化 CSS 打印样式控制的迈进。

#### 技术细节
该属性控制打印网页中的颜色调整，功能与现有的 `-webkit-print-color-adjust` 属性完全相同。webkit 前缀版本仍然支持向后兼容性，允许平滑的过渡期。

#### 用例
对于需要控制颜色在打印媒体中显示方式的网站至关重要，例如文档、报告或任何为打印设计的内容。开发者现在可以使用标准属性名称，同时保持与旧实现的兼容性。

#### 参考资料
[MDN 文档](https://developer.mozilla.org/docs/Web/CSS/print-color-adjust) | [跟踪 bug #376381169](https://bugs.chromium.org/p/chromium/issues/detail?id=376381169) | [ChromeStatus.com 条目](https://chromestatus.com/feature/5090690412953600) | [规范](https://www.w3.org/TR/css-color-adjust-1/#print-color-adjust)

### Rename string attr() type to raw-string

#### 新功能
更新 CSS `attr()` 函数语法，使用 `raw-string` 代替 `string` 作为类型参数，遵循 CSS 工作组决议。

#### 技术细节
该更改将语法从 `attr(data-foo string)` 更新为 `attr(data-foo raw-string)`。此修改与最新的 CSS 规范保持一致，为属性值类型处理提供更精确的术语。

#### 用例
影响任何使用带有字符串类型规范的 `attr()` 函数的 CSS。使用此功能的开发者应更新其 CSS 以使用新的 `raw-string` 语法，尽管功能保持不变。

#### 参考资料
[跟踪 bug #400981738](https://bugs.chromium.org/p/chromium/issues/detail?id=400981738) | [ChromeStatus.com 条目](https://chromestatus.com/feature/5110654344216576) | [规范](https://www.w3.org/TR/css-values-5/#attr-notation)

### Type-agnostic var() fallback

#### 新功能
修改 `var()` 函数行为，使回退值不再根据所引用自定义属性的类型进行验证。

#### 技术细节
此更改通过移除自定义属性及其回退值之间的类型检查，使回退机制更加灵活。回退值现在可以是任何有效的 CSS 类型，无论自定义属性最初定义为接受什么类型。

#### 用例
在使用 CSS 自定义属性时提供更多灵活性，允许更强大的回退策略。在组件系统中特别有用，其中回退值可能需要与主要自定义属性值不同的类型。

#### 参考资料
[跟踪 bug #372475301](https://bugs.chromium.org/p/chromium/issues/detail?id=372475301) | [ChromeStatus.com 条目](https://chromestatus.com/feature/5049845796618240)
