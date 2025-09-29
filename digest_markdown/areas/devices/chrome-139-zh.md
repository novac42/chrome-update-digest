---
layout: default
title: chrome-139-zh
---

## Detailed Updates

下面的细节将上述摘要与 Chrome 139 在 Devices 领域的具体功能对应起来。

### On-device Web Speech API (设备端语音识别)

#### What's New
在 Web Speech API 中新增了设备端语音识别支持，允许网站确保音频和转录文本均不会发送到第三方服务进行处理。站点可以查询特定语言的可用性，并在支持时调用本地识别。

#### Technical Details
该功能将本地语音识别引擎与现有的 Web Speech API 对接，使浏览器能在不将音频或转录通过网络发送到外部服务的情况下执行识别。平台按语言公开可用性发现以支持渐进增强。

#### Use Cases
- 在对隐私敏感的语音输入场景中，要求音频和转录保持在设备上。
- 在网络受限的场景下实现离线语音交互和基于语音的用户界面。
- 渐进增强路径：检测设备能力，在不可用时回退到云服务。

#### References
- https://chromestatus.com/feature/6090916291674112
- https://webaudio.github.io/web-speech-api

### WebXR depth sensing performance improvements (WebXR 深度感知 性能改进)

#### What's New
Chrome 139 在 WebXR 会话中公开了用于定制深度感知行为的新机制，旨在提升深度缓冲区生成与使用的性能。

#### Technical Details
此次更新提供了请求不同深度缓冲表示（例如 raw 或 smooth depth）的控制项，以及额外的调优选项以影响应用生成和使用深度数据的方式。开发者可根据设备能力在质量与性能之间进行权衡。

#### Use Cases
- 需要更低延迟或更低成本深度数据以用于渲染或遮挡的 AR 应用。
- 移动/嵌入式设备场景，开发者需在原始传感器保真度与平滑深度之间为性能做出选择。
- 动态调整深度感知策略以节省能耗或满足运行时帧率目标的应用。

#### References
- https://issues.chromium.org/issues/410607163
- https://chromestatus.com/feature/5074096916004864
- https://immersive-web.github.io/depth-sensing
