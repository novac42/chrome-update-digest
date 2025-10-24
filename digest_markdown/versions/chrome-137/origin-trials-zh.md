---
layout: default
title: 领域摘要
---

# 领域摘要

Chrome 137 的 Origin Trials 侧重于用于资源管理和嵌入内容行为的实验性控制，以及两个供开发者试用的设备端 AI 文本 API。最有影响力的更改是用于保留资源的渲染阻塞标记 `full-frame-rate` 和允许嵌入者在未渲染 iframe 中暂停播放的权限策略，以及暴露设备端语言模型能力的 Rewriter 和 Writer API。这些更新通过为嵌入者提供更细粒度的控制（安全/隐私、多媒体、性能）并为 Web 应用公开本地 AI 驱动的内容转换，推进了平台发展。它们的重要性在于，origin trials 让团队在广泛部署前评估集成、用户体验和隐私影响。

## 详细更新

下面列出 Chrome 137 中的 origin-trial 功能，并提供简明的技术和面向开发者的细节。

### Full frame rate render blocking attribute（保留资源的渲染阻塞标记）

#### 新增内容
新增名为 `full-frame-rate` 的渲染阻塞标记。当渲染器被此标记阻塞时，渲染器会以较低的帧率运行以为加载保留更多资源。

#### 技术细节
该功能引入了用于渲染阻塞属性的 `full-frame-rate` token；应用后渲染器会降低帧率以优先处理加载工作。实现与跟踪可通过以下 Chromium issue 和 ChromeStatus 条目访问。

#### 适用场景
当你希望在繁重加载期间减少动画/绘制频率，以改善感知加载性能和资源分配时使用此标记。

#### 参考资料
- 跟踪 bug #397832388: https://bugs.chromium.org/p/chromium/issues/detail?id=397832388  
- ChromeStatus.com 条目: https://chromestatus.com/feature/5109023781429248

### Pause media playback on not-rendered iframes（在未渲染 iframe 上暂停媒体播放的权限策略）

#### 新增内容
引入了 `media-playback-while-not-rendered` 权限策略，允许嵌入站点对未被渲染（例如 display: none）的 iframe 暂停媒体播放。

#### 技术细节
该权限策略为嵌入者提供了一个开关，用以停止在未被渲染的嵌入框架中的媒体播放。此功能通过 origin trial 暴露，并通过下列问题和 ChromeStatus 条目进行跟踪。

#### 适用场景
嵌入者可以减少对隐藏 iframe 的不必要媒体解码和网络使用，从而提高电量和网络效率，并营造更友好的嵌入行为。

#### 参考资料
- Origin Trial: https://developer.chrome.com/origintrials/#/trials/active  
- 跟踪 bug #351354996: https://bugs.chromium.org/p/chromium/issues/detail?id=351354996  
- ChromeStatus.com 条目: https://chromestatus.com/feature/5082854470868992

### Rewriter API（文本重写 API）

#### 新增内容
一种设备端 API，使用设备端 AI 语言模型对输入文本进行转换和改写（例如删除冗余、针对受众/语气改写）。

#### 技术细节
Rewriter API 作为 origin trial 暴露。它通过设备端语言模型在本地运行转换；origin-trial 注册与跟踪信息可通过下列链接和规范获取。

#### 适用场景
开发者可以实现客户端的文本精简、语气调整或面向特定受众的重写，无需服务器往返，降低延迟并将文本处理保留在设备本地。

#### 参考资料
- Origin Trial: https://developer.chrome.com/origintrials/#/trials/active  
- 跟踪 bug #358214322: https://bugs.chromium.org/p/chromium/issues/detail?id=358214322  
- ChromeStatus.com 条目: https://chromestatus.com/feature/5089854436556800  
- 规范: https://wicg.github.io/rewriter-api/

### Writer API（文本生成 API）

#### 新增内容
一种设备端 API，可使用设备端 AI 语言模型根据提示生成新文本（例如撰写解释、扩展描述）。

#### 技术细节
Writer API 通过 origin trial 提供。它暴露了设备端生成能力；跟踪、规范及策略/许可链接用于评估和集成指导。

#### 适用场景
在客户端进行内容生成，例如创建产品摘要、将结构化数据扩展为文本或起草面向 UI 的文案——将生成保持在本地以降低延迟并考虑隐私。

#### 参考资料
- Origin Trial: https://developer.chrome.com/origintrials/#/trials/active  
- 跟踪 bug #357967382: https://bugs.chromium.org/p/chromium/issues/detail?id=357967382  
- ChromeStatus.com 条目: https://chromestatus.com/feature/5089855470993408  
- 规范: https://wicg.github.io/writer-api/  
- 知识共享 署名 4.0 许可: https://creativecommons.org/licenses/by/4.0/  
- Apache 2.0 许可: https://www.apache.org/licenses/LICENSE-2.0  
- Google 开发者站点政策: https://developers.google.com/site-policies

Saved to: digest_markdown/webplatform/Origin trials/chrome-137-stable-en.md
