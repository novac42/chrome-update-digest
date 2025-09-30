---
layout: default
title: origin-trials-zh
---

## 领域摘要

Chrome 137 的 Origin Trials 侧重于为开发者提供更细粒度的资源使用控制，并试验设备端 AI 文本生成 API。最具影响力的更新是资源管理控制（一个渲染阻塞令牌和一个媒体播放权限策略）以及两个实验性设备端语言 API（Rewriter 和 Writer）。这些试验通过在来源级别启用对性能、多媒体行为和集成 AI 能力的试验，同时在更广泛发布前让开发者看到影响，从而推动平台发展。团队应在 origin trial 令牌下评估用户体验、隐私和性能权衡。

## 详细更新

下面列出 Chrome 137 中的 origin-trial 特性，附带简明技术说明和面向开发者的用例。

### Full frame rate render blocking attribute

#### 新增内容
添加了一个新的渲染阻塞令牌 `full-frame-rate` 到阻塞属性中。当渲染器被 `full-frame-rate` 令牌阻塞时，渲染器将以较低帧率运行，以为加载保留更多资源。

#### 技术细节
- 引入了名为 `full-frame-rate` 的渲染阻塞令牌。
- 应用时，被阻塞的渲染器在降低帧率的同时，将资源重新分配给加载任务。

#### 适用场景
- 在资源负载较重时，通过降低视觉帧更新优先级来改善加载性能。
- 对希望以短暂的流畅性为代价换取更快加载时间的页面有用。

#### 参考资料
- [跟踪 bug #397832388](https://bugs.chromium.org/p/chromium/issues/detail?id=397832388)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5109023781429248)

### Pause media playback on not-rendered iframes

#### 新增内容
添加了一个 `media-playback-while-not-rendered` 权限策略，允许嵌入者网站暂停未被渲染的嵌入 iframe（即具有 `display: none` 的 iframe）中的媒体播放。

#### 技术细节
- 新的 permission-policy 指令：`media-playback-while-not-rendered`。
- 赋予嵌入者控制非渲染 iframe 是否继续媒体播放的能力。

#### 适用场景
- 防止隐藏的 iframe 消耗 CPU/音频资源。
- 改善嵌入第三方媒体的页面的用户体验和资源使用。

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)  
- [跟踪 bug #351354996](https://bugs.chromium.org/p/chromium/issues/detail?id=351354996)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5082854470868992)

### Rewriter API

#### 新增内容
Rewriter API 可按请求方式转换和改写输入文本，由设备端 AI 语言模型支持。它可以删除冗余、符合字数限制或改变语气。

#### 技术细节
- 新的 Web API（受 origin-trial 限制），提供由设备端模型驱动的文本转换功能。
- 在试验期间向页面公开可编程的改写和文本规范化能力。

#### 适用场景
- 自动压缩或调整用户生成文本以满足约束（例如字符限制）。
- 应用内辅助编辑功能，用于为了清晰度或语气而改写文本。

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)  
- [跟踪 bug #358214322](https://bugs.chromium.org/p/chromium/issues/detail?id=358214322)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5089854436556800)  
- [Spec](https://wicg.github.io/rewriter-api/)

### Writer API

#### 新增内容
Writer API 可从写作任务提示生成新的文本内容，由设备端 AI 语言模型支持。它支持撰写帖子、生成解释或扩展描述等任务。

#### 技术细节
- 受 origin-trial 限制的 API，使用设备端模型从提示生成文本输出。
- 试验材料中提供了相关规范和治理链接。

#### 适用场景
- 从结构化输入生成产品描述、摘要或解释性文本。
- 需要程序化内容生成的 Web 应用内辅助创作工具。

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)  
- [跟踪 bug #357967382](https://bugs.chromium.org/p/chromium/issues/detail?id=357967382)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5089855470993408)  
- [Spec](https://wicg.github.io/writer-api/)  
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)  
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)  
- [Google Developers Site Policies](https://developers.google.com/site-policies)

领域特定影响与注意事项（origin trials 重点）
- css: `full-frame-rate` 令牌会影响渲染时序和绘制节奏；在降低帧率时请审核布局/动画行为。  
- webapi / javascript: Rewriter 和 Writer 在 origin trials 下公开新的 JS API —— 为非试验客户端设计优雅的回退路径。  
- graphics-webgpu / performance: 降低渲染器帧率会重新分配 GPU/CPU 周期；衡量渲染与加载之间的权衡。  
- multimedia: iframe 播放策略赋予嵌入者在隐藏媒体上停止播放以降低资源使用的控制权。  
- security-privacy: 设备端 AI 模型（Rewriter/Writer）将数据处理转移到客户端设备，影响数据流和隐私考量。  
- devices: 设备端 API 会消耗本地计算资源；对设备能力和电池影响进行性能分析。  
- pwa-service-worker / webassembly / 弃用: 未列出弃用；在适用时考虑与 PWA 或本地计算策略的集成点。
