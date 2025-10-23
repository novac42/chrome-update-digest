---
layout: default
title: javascript-zh
---

## 领域摘要

Chrome 141（稳定版）针对可通过 JavaScript 访问的 WebRTC 统计数据，聚焦规范对齐与互操作性。主要更改澄清了何时创建 RTP 统计对象，确保各实现间行为一致。这提升了开发者通过 RTP 统计观察与分析媒体流时的可靠性，使诊断与监控更清晰。此更新通过加强规范遵循、减少统计生命周期的歧义，推进了 Web 平台的进展。

## 详细更新

以下是 Chrome 141 中与 JavaScript 相关的更改，并提供面向开发者的实用背景。

### Align implementations on when RTP stats should be created（对齐 RTP 统计创建时机）

#### 新增内容
类型为 "outbound-rtp" 或 "inbound-rtp" 的 RTP 统计对象表示一个 WebRTC 流。该流由其 SSRC（一个数字）标识。此更改使 Chrome 与规范在这些统计应何时创建的问题上保持一致。

#### 技术细节
- 本次更新使 Chrome 在 RTP 统计对象的创建时机方面与 W3C WebRTC Stats 规范保持一致。
- 对象以 SSRC 为键，并在 RTP 统计层级中表示 "outbound-rtp" 或 "inbound-rtp" 流。

#### 适用场景
- 跨浏览器更一致、可预测的统计，用于监测媒体质量。
- 更清晰且与规范对齐的行为，简化 WebRTC 应用的调试与分析。
- 改进依赖 RTP 统计对象的工具的互操作性。

#### 参考资料
- https://issues.chromium.org/issues/406585888
- https://chromestatus.com/feature/4580748730040320
- https://w3c.github.io/webrtc-stats/#the-rtp-statistics-hierarchy
