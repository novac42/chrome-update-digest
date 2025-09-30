---
layout: default
title: html-dom-zh
---

## 领域摘要

Chrome 140 在 HTML-DOM 领域引入了一项聚焦增强：`ToggleEvent` 增加了一个 `source` 属性，用于标识触发该事件的元素。此更改帮助开发者可靠地发现触发类似切换 UI（例如弹出框或基于命令的控件）的元素。通过在事件对象上标准化触发归因，它减少了自定义连接并使组件逻辑与无障碍处理更简单。该更新虽小但实用，推动了在 Web 平台上实现更具表现力的事件驱动 UI 模式。

## 详细更新

Chrome 140 中的单个 HTML-DOM 更改列在下方，并对上述摘要进行了扩展。

### `ToggleEvent` source attribute（source 属性）

#### 新增内容
`ToggleEvent` 的 `source` 属性包含触发该 `ToggleEvent` 被派发的元素（如果适用）。发行说明举例说明，当用户点击带有 `popovertarget` 或 `commandfor` 的 `<button>` 元素以打开弹出框时，在弹出框上触发的 `ToggleEvent` 将可以通过其 `source` 属性获得触发元素。

#### 技术细节
这是 `ToggleEvent` 上的事件级属性，携带对负责发起切换操作的元素的引用。有关完整规范细节和精确定义的接口，请查阅下面链接的规范。

#### 适用场景
- 确定哪个控件打开了弹出框或切换了某个 UI 区域，而无需依赖 DOM 遍历或自定义属性。  
- 简化必须将切换事件映射回其起源控件的组件代码（例如用于焦点管理或命令路由）。  
- 通过在 `ToggleEvent` 上提供明确的触发信息，使事件处理程序更清晰且更不脆弱。

#### 参考资料
- https://chromestatus.com/feature/5165304401100800 (ChromeStatus.com 条目)  
- https://html.spec.whatwg.org/multipage/interaction.html#the-toggleevent-interface (规范)
