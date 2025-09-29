---
layout: default
title: Chrome 140 - Origin Trials Analysis
---

# Chrome 140 - Origin Trials Analysis

## Area Summary

Chrome 140 带来了四项重要的原生试验，扩展了网络平台在通信、调试、剪贴板集成和多线程方面的能力。最具影响力的更改包括为 PWA 提供来电通知、崩溃报告诊断、实时剪贴板同步以及在 Android 上支持 SharedWorker。这些功能通过更好的 VoIP 集成、改进的调试工作流、无缝剪贴板操作以及跨移动平台标签页的资源高效后台处理，共同提升了用户体验。

## Detailed Updates

此版本专注于为开发者提供高级通信、诊断和系统集成 API，同时扩展跨设备平台的一致性。

### Enable incoming call notifications

#### What's New
此功能扩展了 Notifications API，允许已安装的 PWA 发送带有通话样式按钮和铃声支持的来电通知，创造更具吸引力的 VoIP 体验。

#### Technical Details
该增强功能基于现有的 Notifications API，通过添加包含原生通话界面元素和音频能力的专门通话通知类型。这允许 PWA 与操作系统的通话界面进行更深度的集成。

#### Use Cases
VoIP 应用现在可以提供类似原生的通话体验，使用户更容易识别和响应来电。这对商务通信工具、视频会议平台以及具有语音通话功能的消息应用特别有价值。

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/2876111312029483009)
- [Tracking bug #detail?id=1383570](https://issues.chromium.org/issues/detail?id=1383570)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5110990717321216)
- [Spec](https://notifications.spec.whatwg.org)

### Crash Reporting key-value API

#### What's New
此功能引入了一个新的键值 API（暂定为 `window.crashReport`），允许开发者将自定义调试数据附加到崩溃报告中，以进行更好的错误分析。

#### Technical Details
该 API 维护一个按文档划分的映射，保存开发者定义的数据，当渲染器进程发生崩溃时，这些数据会自动包含在 `CrashReportBody` 中。这提供了有助于诊断导致崩溃的情况的上下文信息。

#### Use Cases
开发者可以跟踪用户操作、应用状态、功能标志或自定义指标，这些为调试崩溃提供关键上下文。对于复杂的网络应用，理解用户在崩溃前的操作路径对根本原因分析至关重要。

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/1304355042077179905)
- [Tracking bug #400432195](https://issues.chromium.org/issues/400432195)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6228675846209536)
- [Spec](https://github.com/WICG/crash-reporting/pull/37)

### Add the `clipboardchange` event

#### What's New
`clipboardchange` 事件在系统剪贴板内容发生更改时触发，无论是来自当前网络应用还是任何其他系统应用，实现实时剪贴板同步。

#### Technical Details
此事件通过自动通知应用程序更改，提供了轮询剪贴板的高效替代方案。它在整个系统范围内工作，不仅限于浏览器上下文，允许进行全面的剪贴板监控。

#### Use Cases
远程桌面客户端可以在本地和远程系统之间保持同步的剪贴板。剪贴板管理器、生产力工具和协作应用可以在不同上下文和应用程序之间提供无缝的复制粘贴体验。

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/137922738588221441)
- [Tracking bug #41442253](https://issues.chromium.org/issues/41442253)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5085102657503232)
- [Spec](https://github.com/w3c/clipboard-apis/pull/239)

### Enable `SharedWorker` on Android

#### What's New
SharedWorker 支持现在通过原生试验在 Android 上可用，解决了开发者长期以来对移动平台上跨标签页资源共享和后台处理能力的需求。

#### Technical Details
SharedWorkers 使多个浏览器上下文（标签页、窗口）能够共享单个后台线程，允许在同一网络应用的多个实例之间进行高效的资源利用和状态管理。

#### Use Cases
开发者现在可以在 Android 上跨多个标签页共享 WebSocket 连接或 Server-Sent Events，节省带宽和电池寿命。这为聊天应用、实时协作工具以及任何受益于持久后台连接的网络应用提供了更好的资源管理。

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/4101090410674257921)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6265472244514816)
- [Spec](https://html.spec.whatwg.org/multipage/workers.html#shared-workers-and-the-sharedworker-interface)
