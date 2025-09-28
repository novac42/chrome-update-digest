---
layout: default
title: Chrome 136 源试验 - 开发者预览功能
---

# Chrome 136 源试验 - 开发者预览功能

## 区域摘要

Chrome 136 引入了三个重要的源试验，解决了音频管理、性能监控和 canvas 渲染方面的关键开发者痛点。**音频输出设备 API** 增强功能中的 `setDefaultSinkId()` 为开发者提供了多框架应用中音频路由的编程控制能力。新的**双峰性能计时** API 帮助开发者理解和优化现实世界的性能变化，特别是在冷启动期间。此外，Chrome 正在测试**重新设计的 Canvas 文本渲染实现**，这可能对图形密集型应用的性能产生重大影响。这些试验共同推进了 Web 平台在媒体控制、性能分析和图形渲染优化方面的能力。

## 详细更新

这些源试验为开发者提供了实验性功能的早期访问机会，这些功能可能会重塑我们处理音频设备、性能测量和 canvas 操作的方式。每个试验都解决了开发者在生产环境中面临的特定技术挑战。

### Audio Output Devices API: setDefaultSinkId()

#### 新增内容
MediaDevices 接口新增了 `setDefaultSinkId()` 方法，允许顶级框架以编程方式更改其子框架使用的默认音频输出设备，提供集中的音频路由控制。

#### 技术细节
该 API 通过使父框架能够管理嵌入内容的音频输出目标，扩展了现有的音频输出设备功能。该方法在框架级别操作，允许应用在多个嵌套上下文中协调音频输出，而无需进行单独的框架级音频设备选择。

#### 用例
对于具有多个音频源的复杂 Web 应用、视频会议平台、多媒体编辑器以及需要在嵌入组件间保持一致音频路由的仪表板应用特别有价值。在音频输出协调至关重要的多框架应用中提供更好的用户体验。

#### 参考
[Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [ChromeStatus.com entry](https://chromestatus.com/feature/5066644096548864) | [Spec](https://webaudio.github.io/web-audio-api/#dom-mediadevices-setdefaultsinkid)

### Enable web applications to understand bimodal performance timings

#### 新增内容
新的性能监控 API，帮助开发者识别和测量页面加载时间的双峰性能分布，特别是区分"冷启动"和"热启动"场景。

#### 技术细节
Web 应用由于浏览器初始化状态、系统资源竞争和缓存效果，经常出现双峰性能模式。该 API 通过公开区分不同加载条件的计时数据，提供对这些性能变化的洞察，实现更准确的性能分析和优化策略。

#### 用例
对于需要了解现实世界加载行为、针对不同用户场景进行优化，以及基于数据驱动的资源加载策略决策的性能关键型应用至关重要。对于服务多样化用户群体（具有不同设备能力和网络条件）的应用特别有价值。

#### 参考
[Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #1413848](https://bugs.chromium.org/p/chromium/issues/detail?id=1413848) | [ChromeStatus.com entry](https://chromestatus.com/feature/5037395062800384) | [Spec](https://w3c.github.io/navigation-timing/)

### Update of Canvas text rendering implementation

#### 新增内容
Chrome 正在测试 Canvas 文本渲染方法（包括 `measureText()`、`fillText()` 和 `strokeText()`）的完全重新设计实现，专注于 canvas 密集型应用的性能改进。

#### 技术细节
这代表了 Canvas 文本操作内部处理方式的根本性架构变更。虽然没有引入新的 Web 暴露 API，但实现变更可能显著影响渲染性能、文本测量精度和整体 canvas 操作效率。源试验允许开发者针对新的渲染管线测试应用。

#### 用例
对于严重依赖 canvas 文本渲染的应用至关重要，包括数据可视化工具、游戏、绘图应用、PDF 查看器以及任何图形密集型 Web 应用。使开发者能够在新实现成为标准之前验证性能影响并确保兼容性。

#### 参考
[Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #389726691](https://bugs.chromium.org/p/chromium/issues/detail?id=389726691) | [ChromeStatus.com entry](https://chromestatus.com/feature/5104000067985408)
