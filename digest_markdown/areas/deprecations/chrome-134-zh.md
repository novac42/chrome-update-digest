---
layout: default
title: chrome-134-zh
---

## 领域摘要

Chrome 134（稳定）从 `getUserMedia` 中移除遗留的、非标准的以 `goog` 为前缀的音频约束。此更改针对很少使用的 Blink 特定约束（根据约束不同，使用率报告在 0.000001% 到 0.0009% 之间），其中一些约束已不再生效。对开发者而言，最关键的影响是必须审核并将对这些过时约束的任何依赖迁移到 W3C 规范中的标准约束，以确保跨浏览器兼容性。此清理通过减少遗留表面、提升规范一致性并简化各实现间的媒体采集行为来推进平台改进。

## 详细更新

下面的这一项弃用直接呼应上述摘要，要求处理媒体采集的开发者审查约束的使用情况。

### Remove nonstandard `getUserMedia` audio constraints（移除非标准的 getUserMedia 音频约束）

#### 新增内容
Blink 正在移除此前由 `getUserMedia` 接受的多个非标准的以 `goog` 为前缀的音频约束的支持。

#### 技术细节
- 这些是 Blink 特有的扩展，而非标准化的 Media Capture 约束的一部分。
- 观察到的使用率极低（取决于约束，介于 0.000001% 和 0.0009% 之间），并且由于之前的更改，有些约束已不再产生任何效果。
- 开发者应依赖 W3C media capture 规范中定义的标准约束模型。

#### 适用场景
- 审计应用代码和第三方库中对以 `goog` 为前缀的 `getUserMedia` 约束的使用，并将其替换为 W3C 规范中的标准约束。
- 更新对这些非标准约束相关行为断言的自动化测试。
- 迁移到标准约束后验证跨浏览器行为，以确保音频采集和设备选择一致。

#### 参考资料
- 跟踪 bug #377131184: https://issues.chromium.org/issues/377131184
- ChromeStatus.com 条目: https://chromestatus.com/feature/5097536380207104
- 规范: https://w3c.github.io/mediacapture-main/#media-track-constraints
- 知识共享署名 4.0 许可: https://creativecommons.org/licenses/by/4.0/
- Apache 2.0 许可: https://www.apache.org/licenses/LICENSE-2.0
- Google Developers 网站政策: https://developers.google.com/site-policies

## 领域专长（针对弃用的指导）

- css: 无直接影响；在约束变更时确保音频相关的 UI 控件继续工作。
- webapi: 用 W3C Media Capture 规范中定义的属性替换非标准的 getUserMedia 约束。
- graphics-webgpu: 此次弃用不适用。
- javascript: 在调用 getUserMedia 之前，移除或保护设置 `goog` 前缀约束键的代码路径。
- security-privacy: 审计约束的使用以避免跨浏览器出现意外的权限或设备选择差异。
- performance: 更少的遗留代码路径可简化约束处理并降低维护开销。
- multimedia: 在迁移到标准约束后验证音频采集行为（采样率、设备选择、约束）。
- devices: 确认在没有 Blink 特定约束的情况下设备枚举和选择仍然正确。
- pwa-service-worker: 无直接影响，但应测试捕获音频的 PWA 的媒体采集兼容性。
- webassembly: 不受直接影响。
- deprecations: 规划迁移路径：清点使用情况、替换为符合规范的约束、更新测试并验证跨浏览器行为。
