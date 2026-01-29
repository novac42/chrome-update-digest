---
layout: default
title: Chrome 144 Stable - Multimedia 更新
---

# Chrome 144 Stable - Multimedia 更新

## 领域摘要

Chrome 144 引入了 WebRTC 视频自适应能力的重大增强，新增了 `maintain-framerate-and-resolution` 降级偏好选项。此更新使开发者能够实现自定义视频自适应策略，通过禁用浏览器内置的帧率和分辨率自动调整功能。该功能满足了应用程序对视频质量参数精细控制的关键需求，特别是在应用层自适应逻辑能够做出比浏览器默认行为更明智决策的场景中。此新增功能符合 WebRTC MediaStreamTrack Content Hints 规范，代表着向开发者提供更多实时通信质量管理控制权迈出的重要一步。

## 详细更新

本次发布专注于扩展开发者对 WebRTC 视频流行为的控制能力，提供了一种新机制来防止应用层和浏览器层自适应策略之间的冲突。

### `RTCDegradationPreference` enum value `maintain-framerate-and-resolution`

#### 新增内容

Chrome 144 为 `RTCDegradationPreference` 枚举添加了 `maintain-framerate-and-resolution` 值，该值会禁用 WebRTC 的内部视频自适应机制。这允许应用程序实现自己的自定义自适应逻辑，而不受浏览器自动质量调整的干扰。

#### 技术细节

当设置 `maintain-framerate-and-resolution` 时，浏览器会保持帧率和分辨率，而不考虑视频质量问题。用户代理不会为了质量或性能原因而优先降低任一参数。然而，浏览器在必要时仍可能在编码前丢弃帧，以避免过度使用网络和编码器资源。这可以防止内部自适应系统与应用层自适应策略发生冲突，同时仍为极端资源约束情况提供安全机制。

#### 适用场景

此功能特别适用于：
- 实现复杂自适应比特率流算法的应用程序，这些应用程序需要完全控制视频参数
- 应用程序比浏览器启发式算法更了解网络条件或用户偏好的场景
- 需要确定性质量管理行为的专业视频会议系统
- 需要维护特定帧率和分辨率特性的广播和直播应用程序

#### 参考资料

- [跟踪错误 #450044904](https://issues.chromium.org/issues/450044904)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5156290162720768)
- [规范](https://www.w3.org/TR/mst-content-hint/#dom-rtcdegradationpreference-maintain-framerate-and-resolution)
