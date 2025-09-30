---
layout: default
title: devices-zh
---

## 区域摘要

Chrome 138 (stable) 在 Devices 领域朝两个互补方向推进：扩展硬件连接能力和改进可折叠硬件的布局支持。Android 上的 Web Serial API 通过 Bluetooth RFCOMM 扩展了网页对串行设备的访问模式，而 Viewport Segments Enumeration API 则规范了页面如何检测并适应可折叠设备上的分屏视口。这些功能推动平台朝向更丰富的设备集成和更可预测的多段布局，支持面向物联网、设备配置和可折叠用户体验的 Web 应用。对于开发者而言，这些更改意味着新的设备配对界面以及用于在非矩形视口上进行响应式布局的更清晰原语。

## 详细更新

下面是本次发布中 Devices 领域的两个更新以及它们对实现和产品场景的意义。

### Web serial over Bluetooth on Android（Android 上通过蓝牙的 Web 串口）

#### 新增内容
Chrome 在 Android 上支持通过 Bluetooth RFCOMM 的 Web Serial API，允许网页和 Web 应用在 Android 设备上通过蓝牙连接到串行端口。

#### 技术细节
- 在 Android 上启用 Web Serial API 通过 Bluetooth RFCOMM 传输的使用。
- 更改中引用了现有的企业策略（例如 `DefaultSerialGuardSetting`, `SerialAllowAllPortsForUrls`, `SerialAllowUsbDevicesForUrls`, `SerialAsk...`）。

#### 适用场景
- 基于 Web 的设备配置和为支持蓝牙的串行设备（物联网、嵌入式设备、测试设备）进行配置部署。
- 在浏览器内进行调试和维护的工具，通过蓝牙串行链路与设备通信。
- 依赖现有串行相关策略进行治理的企业管理部署。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=375245353
- https://chromestatus.com/feature/5085754267189248
- https://wicg.github.io/serial/

### Viewport Segments Enumeration API（视口分段枚举 API）

#### 新增内容
Viewport Segments API 暴露了由硬件特性分割视口时产生的逻辑独立区域（视口分段）的位置信息和尺寸，使得对可折叠设备的布局适配更完善。

#### 技术细节
- 引入对视口分段的枚举，当视口被一个或多个硬件特性分割时，这些分段表示不同的区域。
- 提供对分段几何信息的编程访问，以驱动布局和渲染决策。

#### 适用场景
- 响应式布局将内容放置到各个分段（例如多面板 UI），并避开铰链/折痕区域。
- 针对可折叠和双屏设备的渐进增强，其中分段几何决定内容流动和导航模式。
- CSS 与渲染引擎的集成点，以提升多分段布局的稳定性和性能。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=1039050
- https://chromestatus.com/feature/5131631321964544
- https://wicg.github.io/visual-viewport/

已保存文件：digest_markdown/webplatform/Devices/chrome-138-stable-en.md
