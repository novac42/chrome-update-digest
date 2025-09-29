---
layout: default
title: Chrome 140 Stable - HTML-DOM Updates
---

# Chrome 140 Stable - HTML-DOM Updates

## Area Summary

Chrome 140 针对 HTML-DOM 领域引入了一项重点增强功能，新增了 `ToggleEvent` source 属性。此更新加强了交互元素与其触发事件之间的连接，为开发者提供了关于导致弹出层等可切换元素状态变化的用户交互的更好上下文。该功能体现了 Chrome 持续努力使 DOM 事件对构建交互式 Web 应用程序的开发者更加信息丰富和可操作。此增强功能对于多个元素可能触发同一可切换组件的复杂 UI 模式特别有价值。

## Detailed Updates

基于 Chrome 致力于提供更丰富事件上下文的承诺，此版本提供了对 ToggleEvent 接口的针对性改进，增强了开发者对用户交互的理解。

### `ToggleEvent` source attribute

#### What's New
`ToggleEvent` 现在包含一个 `source` 属性，用于标识触发切换事件的元素。这提供了有关切换操作来源的关键上下文，在多个元素可以控制同一可切换组件时特别有用。

#### Technical Details
`source` 属性包含对启动 `ToggleEvent` 的 DOM 元素的引用。例如，当用户点击设置了 `popovertarget` 或 `commandfor` 属性以打开弹出层的 `<button>` 元素时，在弹出层上触发的结果 `ToggleEvent` 将其 `source` 属性指向该按钮元素。这在触发器和目标之间创建了清晰的程序化链接。

#### Use Cases
此功能使开发者能够：
- 通过了解哪个特定触发器导致了切换来构建更复杂的事件处理逻辑
- 基于源元素实现不同的行为（例如，不同的动画或定位）
- 通过维护焦点上下文创建更好的无障碍体验
- 更有效地调试与切换相关的交互
- 构建跟踪哪些 UI 元素在触发用户操作方面最有效的分析

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5165304401100800)
- [Spec](https://html.spec.whatwg.org/multipage/interaction.html#the-toggleevent-interface)
