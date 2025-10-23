---
layout: default
title: multimedia-zh
---

## 领域摘要

Chrome 141 的 Multimedia 更新聚焦于 WebRTC 媒体处理与音频采集控制。WebRTC Encoded Transform (V2) 使得可对通过 RTCPeerConnection 传输的编码媒体进行处理，并使 Chrome 与最新规范及其他浏览器保持一致。`getUserMedia()` 的新 `echoCancellationMode` 在现有约束基础上增加取值，从而细化音频输入行为。这些变更共同提升跨浏览器互操作性，并为开发者提供更精细、与标准一致的实时媒体质量控制。

## 详细更新

这些更新围绕可互操作的实时媒体处理与改进的音频采集可配置性展开。

### WebRTC Encoded Transform (V2)（编码转换 V2）

#### 新增内容
允许在编码媒体通过 RTCPeerConnection 流动时进行处理，将 Chrome 升级到该 API 的较新版本。

#### 技术细节
- Chrome 曾在 2020 年发布过该 API 的早期版本；此后规范已发生变化。
- 其他浏览器已发布更新版本（Safari 于 2022 年，Firefox 于 2023 年）。
- 此次发布使 Chrome 与更新后的规范和跨浏览器行为保持一致。

#### 适用场景
- 在需要访问编码数据的场景下，对 WebRTC 管线中的编码媒体进行实时处理。

#### 参考资料
- 跟踪 bug #354881878: https://issues.chromium.org/issues/354881878
- ChromeStatus.com 条目: https://chromestatus.com/feature/5175278159265792
- 规范: https://github.com/w3c/webrtc-encoded-transform

### `echoCancellationMode` for `getUserMedia()`

#### 新增内容
扩展 `MediaTrackConstraints` 字典中 `echoCancellation` 的行为，在 true/false 之外接受取值 "all" 和 "remote-only"。

#### 技术细节
- 适用于来自麦克风的音频轨。
- 提供额外模式以调整回声消除行为。

#### 适用场景
- 对麦克风回声消除进行精细控制，以满足应用的音频需求。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5585747985563648
- 规范: https://www.w3.org/TR/mediacapture-streams/#dom-echocancellationmodeenum
