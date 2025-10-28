---
layout: default
title: chrome-133-zh
---

## 领域摘要

Chrome 133 的 HTML-DOM 更新聚焦于更丰富的弹出框语义与开发者体验优化，以及保留元素状态的 DOM 原语和更灵活的剪贴板输入。与弹出框相关的更改（新的 `hint` 值、改进的 invoker API、以及嵌套 invoker 行为修复）使得类提示气泡的 UI 模式更可预测且更易实现。用于在不重置状态的情况下移动节点的新 DOM 原语使得对重元素（如 iframe、处于活动状态的元素）进行更安全的重新父级化成为可能，并能减少框架中的权宜之计。允许 ClipboardItem 数据为字符串或解析为字符串的 Promise 简化了异步剪贴板写入并减少了转换为 Blob 的需要。

## 详细更新

下面的细节扩展了上述摘要并列出 Chrome 133 中添加的每项 HTML-DOM 功能。

### The hint value of the popover attribute（popover 属性的 hint 值）

#### 新增内容
引入了 popover 属性的第三个值：`popover=hint`。该值用于目标为提示/工具提示类行为的弹出框，这些行为与现有的 `auto` 和 `manual` 模式略有不同。

#### 技术细节
根据 Popover API，该属性现在接受 `hint` 作为面向语义的选项，用于表示轻量级提示的弹出框。该特性文档指出 hint 弹出框在行为上与其他弹出框模式略有不同。

#### 适用场景
实现类工具提示的提示，使用更明确的语义并减少自定义行为。需要轻量、短暂说明性弹出框的 UI 组件可以采用 `popover=hint` 以获得一致行为。

#### 参考资料
- [跟踪问题 #1416284](https://issues.chromium.org/issues/1416284)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5073251081912320)

### Popover invoker and anchor positioning improvements（Popover 调用者与锚点定位改进）

#### 新增内容
添加了用于建立 invoker 关系的命令式 API：`popover.showPopover({source})`，并使 invoker 关系能够为定位创建隐式锚点元素引用。

#### 技术细节
该 API 提供了一种以编程方式设置弹出框与其 invoker/source 之间关系的方法，允许从 invoker 关系中派生隐式锚点以用于定位逻辑。

#### 适用场景
在弹出框通过编程方式显示的动态 UI（例如由复杂交互触发的上下文菜单或工具提示）中，可以使用此命令式 API 来确保正确的锚定与定位。

#### 参考资料
- [跟踪问题 #364669918](https://issues.chromium.org/issues/364669918)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5120638407409664)

### Popover nested inside invoker shouldn't re-invoke it（嵌套在 invoker 内的 Popover 不应重新触发）

#### 新增内容
修复了当弹出框嵌套在其 invoker 元素内时的行为，使得与弹出框自身交互不会重新触发或关闭该弹出框。

#### 技术细节
示例场景：
```html
<button popovertarget=foo>Activate
  <div popover id=foo>Clicking me shouldn't close me</div>
</button>
```
以前，点击嵌套的弹出框可能会错误地触发重新调用行为；此次更新阻止了这种不希望的关闭/重新打开序列。

#### 适用场景
包含在按钮内的弹出框以及嵌套的交互式弹出框内容将不再无意间关闭或重新触发 invoker，从而改善嵌套交互控件的用户体验。

#### 参考资料
- [跟踪问题 #379241451](https://issues.chromium.org/issues/379241451)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4821788884992000)

### DOM state-preserving move（保留状态的 DOM 移动）

#### 新增内容
添加了一个 DOM 原语 `Node.prototype.moveBefore`，用于在 DOM 内移动元素而不重置其运行时状态。

#### 技术细节
使用该原语移动节点会保留在移除并重新插入节点时本会丢失的元素状态。文档中列出的被保留状态包括已加载的 `<iframe>` 元素及其他正在进行的元素状态。

#### 适用场景
在为协调或布局更改而重新父级化节点的框架和库中，可以在不迫使重新加载或重置活动/焦点状态的情况下移动节点，从而减少变通办法并提高大型子树的性能。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5135990159835136)

### Support creating `ClipboardItem` with `Promise<DOMString>`（支持使用 Promise<DOMString> 创建 ClipboardItem）

#### 新增内容
`ClipboardItem` 构造函数现在接受字符串值（除了 Blob 之外）。`ClipboardItemData` 可以是 Blob、字符串或解析为任一者的 Promise。

#### 技术细节
这扩展了异步剪贴板 `write()` 的输入，以接受惰性或异步的字符串数据（即 `Promise<DOMString>`），从而减少在写入前将字符串转换为 Blob 的需要。

#### 适用场景
在异步流程中将文本或延迟生成的字符串内容写入剪贴板时简化了操作，无需中间的 Blob 转换。

#### 参考资料
- [跟踪问题 #40766145](https://issues.chromium.org/issues/40766145)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4926138582040576)
- [规范](https://www.w3.org/TR/clipboard-apis/#typedefdef-clipboarditemdata)

已保存到: digest_markdown/webplatform/HTML-DOM/chrome-133-stable-en.md
