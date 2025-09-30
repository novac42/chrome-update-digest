---
layout: default
title: chrome-138-zh
---

## 详细更新

Below are the Devices-area updates from the Chrome 138 stable release, with concise technical context and developer-focused use cases.

### Web serial over Bluetooth on Android（Android 上通过蓝牙的 Web Serial）

#### 新增内容
Chrome 在 Android 上支持通过蓝牙 RFCOMM 的 Web Serial API，使网页和 Web 应用能够连接 Android 设备上通过蓝牙暴露的串口。现有的企业策略（如 DefaultSerialGuardSetting、SerialAllowAllPortsForUrls 和 SerialAllowUsbDevicesForUrls）依然适用。

#### 技术细节
实现使 Chromium for Android 上的 Web Serial API 能通过蓝牙 RFCOMM 作为传输层工作，按照 Web Serial 规范枚举并打开此传输上的串口。

#### 适用场景
- 通过蓝牙与微控制器、传感器或遗留串行外设通信的 Web 界面。
- 在企业或受管理设备场景中，由策略管理 Web 应用对串口访问的情况。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=375245353
- https://chromestatus.com/feature/5085754267189248
- https://wicg.github.io/serial/

### Viewport Segments Enumeration API（视口段枚举 API）

#### 新增内容
The Viewport Segments API enables developers to adapt layouts for foldable and multi-segment displays by exposing the position and dimensions of logically separate viewport regions. Viewport segments are created when the viewport is split by one or more hardware features.

#### 技术细节
该 API 可以枚举由硬件驱动的分割（铰链、折痕、缺口）产生的视口段，允许应用查询段的几何信息并按照 Visual Viewport 工作的定义对分割视口做出响应。

#### 适用场景
- 针对可折叠设备的响应式两栏或多栏布局。
- 在铰链/折痕边界上动态放置交互式 UI 以避免遮挡。
- 在分割视口上改进媒体和内容布局策略。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=1039050
- https://chromestatus.com/feature/5131631321964544
- https://wicg.github.io/visual-viewport/
