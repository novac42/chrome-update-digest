---
layout: default
title: multimedia-zh
---

### 1. 领域摘要

Chrome 134 在 Blink 中从 getUserMedia 中移除了遗留的、非标准的 goog-prefixed 音频约束，反映出它们的使用率极低并且需要与标准保持一致。对开发者影响最大的是，任何依赖这些遗留约束的代码将停止工作；请迁移到由 W3C 定义的标准化 Media Track Constraints。此举缩小了浏览器的暴露面，简化了 WebRTC 音频采集行为，并减少了维护和隐私攻击面。总体而言，该更改通过在实现间强制单一、符合规范的约束模型，推动了 Web 平台 的发展。

## 详细更新

Below are the Multimedia-specific details and practical guidance for teams that use getUserMedia audio constraints.

### Remove nonstandard `getUserMedia` audio constraints (移除非标准的 getUserMedia 音频约束)

#### 新增内容
Chrome 134 移除了 Blink 先前支持的若干非标准的、以 goog- 为前缀的音频约束的支持。根据不同约束，其使用率已下降到 0.000001% 到 0.0009% 之间，部分约束已无效。

#### 技术细节
- Blink 过去接受早于约束标准化的 goog-prefixed 约束。Chrome 134 删除了这些遗留捷径，以符合 W3C 的媒体捕获约束模型。
- 开发者必须使用通过 `navigator.mediaDevices.getUserMedia` 暴露的、标准化的 Media Track Constraints（参见规范链接）。
- 这是一次由弃用驱动的简化，减少了实现差异和潜在的隐私/权限边缘情况。

相关领域映射： webapi (getUserMedia 约束模型), multimedia (音频采集语义), security-privacy (较小的遗留面), performance (降低遗留处理), devices (音频输入处理), deprecations (需要迁移)。

#### 适用场景
- 迁移：将任何以 goog- 为前缀的约束检测替换为标准约束名称，或通过符合规范的 API 进行特性检测。
- 互操作测试：使用 W3C 约束名称验证各浏览器之间的音频采集行为。
- 维护：删除针对 goog- 前缀约束的保护代码路径，以简化媒体采集逻辑和权限用户体验。

#### 参考资料
- 跟踪 bug #377131184: https://issues.chromium.org/issues/377131184
- ChromeStatus.com 条目: https://chromestatus.com/feature/5097536380207104
- 规范: https://w3c.github.io/mediacapture-main/#media-track-constraints
- 知识共享署名 4.0 许可: https://creativecommons.org/licenses/by/4.0/
- Apache 2.0 许可: https://www.apache.org/licenses/LICENSE-2.0
- Google 开发者站点策略: https://developers.google.com/site-policies

文件名: digest_markdown/webplatform/Multimedia/chrome-134-stable-en.md
