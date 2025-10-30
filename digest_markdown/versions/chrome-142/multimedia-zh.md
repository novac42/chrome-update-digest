---
layout: default
title: multimedia-zh
---

### 1. 领域摘要

Chrome 142 的多媒体更新集中在改进 Media Session API，以为 Picture-in-Picture (PiP) 交互提供更丰富的上下文。最重要的更改是在 `enterpictureinpicture` 操作详情中添加一个 reason 字段，使开发者能够区分用户发起的 PiP 与其他触发方式。这有助于应用层在 UI/行为上做出更合理的决策，并使 Web 平台在媒体控制语义上更清晰。这些渐进的 API 改进帮助开发者构建更可预测且尊重用户的媒体体验。

### 2. 详细更新

下面列出实现上述摘要的多媒体领域更改及其对开发者的意义。

### Media session: add reason to `enterpictureinpicture` action details（在 `enterpictureinpicture` 操作详情中添加原因字段）

#### 新增内容
在传递给 Media Session API 中 `enterpictureinpicture` 操作的 `MediaSessionActionDetails` 中添加 `enterPictureInPictureReason` 字段，允许开发者区分由用户明确触发的 `enterpictureinpicture` 操作与其他触发方式。

#### 技术细节
在传递给 `enterpictureinpicture` 操作处理器的 `MediaSessionActionDetails` 对象中加入了新的字段 `enterPictureInPictureReason`。处理器可以检查该字段以确定 PiP 请求的来源（例如，用户代理 UI 与编程触发）。

#### 适用场景
- 当 PiP 是由用户明确请求而非通过编程方式启动时，调整 UI 或同意流程。
- 基于 PiP 进入原因实施不同的分析、遥测或可访问性行为。
- 为通过编程触发的 PiP 提供更安全的默认设置或保护措施。

#### 参考资料
- [跟踪错误 #446738067](https://issues.chromium.org/issues/446738067)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6415506970116096)  
- [规范](https://github.com/w3c/mediasession/pull/362)

关于相关性的说明：此更新的主要标签包括 webapi、multimedia 和 webgpu（如提供），直接适用于 Media Session API 的使用者和以媒体为中心的 Web 应用。
