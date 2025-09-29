# Area Summary

Chrome 137 (stable) 的 origin trials 强调在资源管理、由嵌入者控制的媒体控制以及设备端 AI 文本能力方面的试验。最具影响力的更改允许开发者影响渲染器调度（一个新的 render-blocking token）、通过权限策略在未渲染的 iframe 中暂停媒体，以及原型化两种设备端生成式文本 API（Rewriter 和 Writer）。这些试验推动了平台发展，使开发者能够实现更细粒度的性能控件、改进嵌入者用户体验并节省电力/带宽，以及实现保护隐私的设备端 AI 交互。团队应评估这些试验如何映射到其应用中的 rendering、multimedia、web APIs 和隐私需求。

## Detailed Updates

The following entries expand on the summary above and highlight practical developer considerations for each origin trial.

### Full frame rate render blocking attribute

#### What's New
引入了一个名为 `full-frame-rate` 的 render-blocking token，并将其添加到 blocking attributes。 当渲染器因该 token 而被阻塞时，渲染器会以较低的帧率运行，以为加载保留资源。

#### Technical Details
- 该功能是一个 origin-trial-level 的 render-blocking attribute，指示在阻塞时采用降低帧率的行为。
- 目标是在存在 `full-frame-rate` token 时，将渲染器资源使用转移到加载工作上。

#### Use Cases
- 通过在关键加载期间限制渲染工作，改善复杂页面的感知加载速度。
- 在后台或高负载状态下减少 GPU/CPU 的无谓消耗，以优先处理网络或解析任务。
- 供需要对 renderer scheduling 和能耗/性能权衡进行细粒度控制的团队试验。

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=397832388
- https://chromestatus.com/feature/5109023781429248

### Pause media playback on not-rendered iframes

#### What's New
新增 `media-playback-while-not-rendered` permission policy，允许嵌入者暂停未渲染（例如使用 `display: none`）的 iframe 中的媒体播放。

#### Technical Details
- 在嵌入者层暴露了一项 permission policy 控制，用于暂停未渲染 iframe 中的媒体。
- 针对 DOM 中存在但未视觉呈现的 iframe 内容，启用嵌入者驱动的播放策略。

#### Use Cases
- 阻止隐藏/覆盖的 iframe 播放音频/视频，以改善电池寿命和用户体验。
- 让嵌入者对嵌入内容的行为拥有确定性控制，以便更好地管理 UX 和资源。
- 在复杂的嵌入场景（小部件、选项卡、模态）中，当显示切换时同时切换媒体活动非常有用。

#### References
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=351354996
- https://chromestatus.com/feature/5082854470868992

### Rewriter API

#### What's New
提供一个使用设备端 AI 语言模型对输入文本进行转换和改写的 API。可用于去除冗余、将文本调整为字数限制或针对目标受众改写等任务。

#### Technical Details
- 通过 origin trial API 暴露了一个设备端 AI 支持的端点，用于文本转换和改写。
- 聚焦于客户端转换，以避免将用户文本传输到服务器端。

#### Use Cases
- 在编辑器中集成内联改写工具，以缩短文本或使其符合样式指南。
- 通过为不同受众阅读水平提供替代措辞，改善无障碍性和清晰度。
- 在隐私和延迟敏感场景下实现离线可用的文本处理功能。

#### References
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=358214322
- https://chromestatus.com/feature/5089854436556800
- https://wicg.github.io/rewriter-api/

### Writer API

#### What's New
提供一个 API，使用设备端 AI 模型根据写作任务提示生成新的文本内容。用例包括撰写说明、产品描述或扩展简短输入。

#### Technical Details
- 作为 origin trial 提供的设备端生成 API，旨在根据结构化提示生成新文本。
- 强调客户端处理，使提示和输出保留在设备本地。

#### Use Cases
- 自动生成产品描述、摘要，或将结构化数据补足为可读内容。
- 在编辑器中提供辅助内容创建功能，同时最小化服务器端数据处理。
- 原型化与 UI 流（例如表单帮助、评论摘要）相关的上下文内容生成。

#### References
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=357967382
- https://chromestatus.com/feature/5089855470993408
- https://wicg.github.io/writer-api/
- https://creativecommons.org/licenses/by/4.0/
- https://www.apache.org/licenses/LICENSE-2.0
- https://developers.google.com/site-policies

Note: Relevant technical focus areas across these trials include webapi and javascript for API surface and integration, performance and css/layout engine considerations for the render-blocking token, multimedia and permission-policy semantics for iframe media control, and security-privacy for on-device AI usage and data residency.