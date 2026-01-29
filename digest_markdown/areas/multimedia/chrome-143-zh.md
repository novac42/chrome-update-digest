---
layout: default
title: chrome-143-zh
---

## 领域摘要

Chrome 143 引入了针对性的 WebRTC 信令更改，在后续的 offer/answer 交换中稳定 RTP 标头扩展排序。主要主题是增加 WebRTC 协商的确定性，以避免标头扩展的意外重新映射，减少实时多媒体应用和中间盒的破坏。此更改对 WebRTC SDK、SFU 和依赖稳定扩展槽分配的复杂点对点应用的开发者影响最大。通过使实现与规范保持一致，该平台提高了互操作性，并简化了开发者对重新协商期间 RTP 扩展处理的推理。

## 详细更新

此版本中的单个 Multimedia 更新加强了 RTP 标头扩展在 offer/answer 之间的处理方式；详细信息和实际影响如下所列。

### WebRTC RTP header extension behavior change（WebRTC RTP 标头扩展行为更改）

#### 新增内容
offer/answer 行为被更改，使后续的 offer 或 answer 不会排列（重新排序或重新映射）已协商的 RTP 标头扩展，除非用户明确请求此类修改。

#### 技术细节
- 实现了 WebRTC 扩展草案中的规范更改，以在默认情况下保持扩展映射在重新协商之间的稳定。
- 影响 SDP/RTCPeerConnection offer/answer 流程以及如何保留标头扩展 ID 和映射。
- 意图是防止已协商扩展槽的隐式排列，减少令人惊讶的运行时重新映射。

#### 适用场景
- 依赖一致标头扩展索引来处理音频电平、MID 或时间戳偏移等特性的 SFU 和媒体服务器将在重新协商时看到更少的中断。
- 以编程方式操作 offer/answer 的 WebRTC SDK 和应用可以假定稳定的扩展映射，除非它们选择更改。
- 简化调试并避免由于通话中重新协商期间意外扩展重新映射引起的瞬态媒体处理问题。

#### 参考资料
- [跟踪错误 #439514253](https://issues.chromium.org/issues/439514253)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5135528638939136)
- [规范](https://w3c.github.io/webrtc-extensions/#rtp-header-extension-control-modifications)
