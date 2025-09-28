---
layout: default
title: Chrome 136 设备更新分析
---

# Chrome 136 设备更新分析

## 区域摘要

Chrome 136 为**设备**领域引入了一项重要增强功能，即音频输出设备 API 的新 `setDefaultSinkId()` 方法。此更新解决了开发者长期以来对 Web 应用程序中精细音频输出控制的需求，特别是在复杂的多框架场景中。该功能使顶级框架能够以编程方式管理其子框架的默认音频输出设备，提升了 Web 平台在富媒体应用程序方面的能力。此项新增代表了 Chrome 在为开发者提供全面设备管理 API 方面的持续承诺，这些 API 弥合了 Web 和原生应用程序能力之间的差距。

## 详细更新

基于设备控制 API 的战略重要性，Chrome 136 提供了一个专注但有影响力的更新，增强了音频输出管理能力。

### Audio Output Devices API: setDefaultSinkId()

#### 新功能
`setDefaultSinkId()` 方法已添加到 `MediaDevices` 接口，允许顶级框架以编程方式设置其子框架将使用的默认音频输出设备。此方法为多框架 Web 应用程序中的音频路由提供集中控制。

#### 技术细节
该实现通过一个接受设备 ID 参数的新方法扩展了现有的 MediaDevices API，以指定目标音频输出设备。当从顶级框架调用时，此方法会更改子框架内所有音频上下文和媒体元素的默认接收器，提供了音频设备管理的分层方法。该功能利用现有的 Web Audio API 基础设施，同时添加跨框架设备控制能力。

#### 用例
此 API 对于媒体制作应用程序、视频会议平台以及需要确保多个嵌入组件之间音频输出一致性的多媒体 Web 应用程序特别有价值。开发者现在可以构建允许用户在应用程序级别一次性选择其首选音频输出设备的应用程序，而不需要在每个嵌入框架或组件内进行设备选择。

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5066644096548864)
- [Spec](https://webaudio.github.io/web-audio-api/#dom-mediadevices-setdefaultsinkid)
