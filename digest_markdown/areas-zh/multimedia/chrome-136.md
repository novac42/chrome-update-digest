---
layout: default
title: Chrome 136 多媒体更新 - 开发者分析
---

# Chrome 136 多媒体更新 - 开发者分析

## 领域总结

Chrome 136 在多媒体能力方面带来了重大进展，专注于增强音频管理、屏幕捕获控制和编解码器支持扩展。最具影响力的变化包括新的 AudioContext 中断状态以实现更好的音频会话处理、用于屏幕共享应用的全面捕获表面控制 API，以及通过在 WebRTC 和 MediaRecorder 中集成 H265/HEVC 来扩展编解码器支持。这些更新共同强化了 Chrome 作为高质量多媒体应用平台的地位，为开发者提供了对音频上下文的更精细控制、高级屏幕共享能力，以及对现代视频流和录制工作流程的更广泛编解码器兼容性。

## 详细更新

基于 Chrome 的多媒体基础，此版本引入了多个面向开发者的增强功能，扩展了音频、视频和屏幕捕获领域的控制和兼容性。

### AudioContext Interrupted State

#### 新功能
向 AudioContextState 枚举引入新的"interrupted"状态，允许用户代理在独占音频访问场景或硬件事件（如笔记本电脑合盖）期间暂停音频播放。

#### 技术细节
中断状态扩展了现有的 AudioContext 状态机，为浏览器处理音频中断提供了标准化方式，而无需终止整个音频上下文。此状态在临时暂停播放的同时保留音频图，在中断结束时能够无缝恢复。

#### 用例
- VoIP 应用可以优雅地处理独占音频访问要求
- 媒体播放器可以恰当地响应合盖等硬件事件
- 音频应用获得与系统级音频管理的更好集成
- 开发者可以实现更健壮的音频会话处理

#### 参考资料
[跟踪 bug #374805121](https://bugs.chromium.org/p/chromium/issues/detail?id=374805121) | [ChromeStatus.com 条目](https://chromestatus.com/feature/5087843301908480) | [规范](https://webaudio.github.io/web-audio-api/#AudioContextState)

### Captured Surface Control

#### 新功能
一个全面的 Web API，使 Web 应用能够通过转发滚轮事件和管理屏幕共享会话期间捕获标签页的缩放级别来与捕获表面交互。

#### 技术细节
该 API 为捕获表面提供直接控制机制，允许应用将滚轮滚动等用户交互转发到捕获内容，并以编程方式调整缩放级别。这通过连接捕获和被捕获上下文之间的差距，创造了更具交互性的屏幕共享体验。

#### 用例
- 屏幕共享应用可以启用交互式远程桌面体验
- 协作工具可以允许参与者直接导航共享内容
- 远程支持应用获得增强的控制能力
- 视频会议平台可以提供更具吸引力的屏幕共享功能

#### 参考资料
[跟踪 bug #1466247](https://bugs.chromium.org/p/chromium/issues/detail?id=1466247) | [ChromeStatus.com 条目](https://chromestatus.com/feature/5064816815276032) | [规范](https://wicg.github.io/captured-surface-control/)

### CapturedSurfaceResolution

#### 新功能
在屏幕共享期间公开捕获表面的像素比率，为应用提供关于共享内容的物理和逻辑分辨率的详细信息。

#### 技术细节
此功能揭示了捕获表面上物理像素与逻辑单位之间的关系，使应用能够基于捕获内容的实际分辨率特性做出明智的资源分配和质量优化决策。应用现在可以根据捕获内容的实际分辨率特性调整其处理管线。

#### 用例
- 视频会议应用可以基于实际像素密度优化带宽使用
- 屏幕录制工具可以调整质量设置以匹配源分辨率
- 远程桌面应用可以实现智能缩放算法
- 流媒体平台可以调整压缩参数以获得最佳视觉质量

#### 参考资料
[跟踪 bug #383946052](https://bugs.chromium.org/p/chromium/issues/detail?id=383946052) | [ChromeStatus.com 条目](https://chromestatus.com/feature/5100866324422656) | [规范](https://w3c.github.io/mediacapture-screen-share-extensions/#capturedsurfaceresolution)

### H265 (HEVC) codec support in WebRTC

#### 新功能
向 WebRTC 添加 H265/HEVC 编解码器支持，在 VP8、H.264、VP9 和 AV1 基础上扩展了可用的编解码器选项。支持通过 MediaCapabilities API 发现运行时编解码器可用性。

#### 技术细节
WebRTC 中的 HEVC 集成提供了相比旧编解码器更优的压缩效率，在保持视频质量的同时可能减少带宽需求。该实现遵循 WebRTC 编解码器能力标准，并与现有编解码器协商机制集成。

#### 用例
- 视频会议应用可以在带宽受限场景中利用更优的压缩
- 直播平台获得更高效的编码选项
- 移动应用可以在保持视频质量的同时减少数据使用
- 企业视频解决方案可以优化网络利用率

#### 参考资料
[跟踪 bug #391903235](https://bugs.chromium.org/p/chromium/issues/detail?id=391903235) | [ChromeStatus.com 条目](https://chromestatus.com/feature/5104835309936640) | [规范](https://www.w3.org/TR/webrtc/#dom-rtcrtpcodeccapability)

### H26x Codec support updates for MediaRecorder

#### 新功能
MediaRecorder API 现在支持使用 `hvc1.*` 编解码器字符串的 HEVC 编码，并引入新的编解码器变体（`hev1.*` 和 `avc3.*`），支持 MP4 容器中的可变分辨率视频。

#### 技术细节
此更新基于 Chrome 130 中添加到 WebCodecs 的 HEVC 平台编码支持，将编解码器支持扩展到 MediaRecorder 以实现一致的视频录制能力。新的编解码器字符串提供对编码参数和容器兼容性的更精细控制。

#### 用例
- 屏幕录制应用可以利用 HEVC 的压缩效率
- 视频编辑工具获得现代编解码器变体的访问
- 内容创作平台可以提供改进的录制质量
- 移动应用可以在保持质量的同时创建更小的视频文件

#### 参考资料
[ChromeStatus.com 条目](https://chromestatus.com/feature/5103892473503744)

### Use DOMPointInit for getCharNumAtPosition, isPointInFill, isPointInStroke

#### 新功能
更新 SVGGeometryElement 和 SVGPathElement 方法，对 `getCharNumAtPosition`、`isPointInFill` 和 `isPointInStroke` 方法使用 DOMPointInit 而不是 SVGPoint，与最新的 W3C 规范保持一致。

#### 技术细节
此更改通过采用更灵活的 DOMPointInit 接口现代化了 SVG API 表面，该接口提供与现代 Web 平台 API 的更好集成以及在 SVG 上下文中基于点操作的改进开发者体验。

#### 用例
- SVG 操作库受益于现代化的 API 接口
- 图形应用在 Web API 中获得更一致的点处理
- 开发者工具可以提供更好的 SVG 交互能力
- 动画框架可以利用改进的 SVG 几何方法

#### 参考资料
[跟踪 bug #40572887](https://bugs.chromium.org/p/chromium/issues/detail?id=40572887) | [ChromeStatus.com 条目](https://chromestatus.com/feature/5084627093929984) | [规范](https://www.w3.org/TR/SVG2/types.html#InterfaceDOMPointInit)