---
layout: default
title: devices-zh
---

## 领域摘要

Chrome 143 在 Devices 领域引入了对游戏手柄连接生命周期事件处理程序属性的原生支持。此更新向 WindowEventHandlers mixin 添加了 ongamepadconnected 和 ongamepaddisconnected 属性，从而更容易在全局目标上（例如 window 和 document.body）附加处理程序。对开发者而言，这减少了用于检测游戏手柄连接/断开事件的样板代码，并使浏览器行为与 Gamepad API 规范保持一致。该更改通过标准化一种便捷且声明式的方式来观察硬件连接变化，推动了 Web 平台的发展。

## 详细更新

下面是 Chrome 143 中基于上述摘要的 Devices 领域更改。

### Gamepad `ongamepadconnected` and `ongamepaddisconnected` event handler attributes（游戏手柄事件处理程序属性）

#### 新增内容
向 `WindowEventHandlers` interface mixin 添加了 `ongamepadconnected` 和 `ongamepaddisconnected` 事件处理程序，支持在全局目标上使用事件处理程序属性（例如 `window.ongamepadconnected` 以及类似的 `document.body` 属性）。

#### 技术细节
此更改通过扩展 `WindowEventHandlers` mixin 来实现 Gamepad API 指定的事件处理程序属性添加。有关权威细节和实现状态，请参阅下列跟踪和规范链接。

#### 适用场景
- 在 Web 应用和游戏中以简洁、声明式方式处理游戏手柄连接/断开事件。
- 对依赖全局处理程序属性而非 addEventListener 绑定的页面，更易于渐进增强和兼容性处理。
- 适用于快速原型、嵌入式小部件或希望在 window/document.body 上公开内联处理程序的页面。

#### 参考资料
- [跟踪错误 #40175074](https://issues.chromium.org/issues/40175074)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5109540852989952)  
- [规范](https://w3c.github.io/gamepad/#extensions-to-the-windoweventhandlers-interface-mixin)
