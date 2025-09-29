## Area Summary

Chrome 137's Origin Trials 专注于渲染性能的实验性控制、嵌入内容中的媒体行为以及设备端生成文本的 API。最具影响力的更改允许开发者管理渲染资源分配（`full-frame-rate` token）、通过权限策略暂停不可见 iframe 的媒体播放，以及在设备端测试两个新的 AI 驱动文本 API（Rewriter 和 Writer）。这些更新通过向开发者暴露性能和嵌入行为的控制项，同时在隐私和资源意识的设备端机器学习能力上进行迭代，推动平台发展。团队应评估 origin trial 的注册，以便尽早原型化集成并评估隐私、用户体验和性能的权衡。

## Detailed Updates

Below are the Chrome 137 origin-trial features with succinct developer-focused explanations and relevant links.

### Full frame rate render blocking attribute

#### What's New
Adds a new render blocking token named `full-frame-rate`. When a renderer is blocked with this token, it runs at a lower frame rate to reserve resources for loading.

#### Technical Details
这是一个 origin-trial 级别的标志，暴露了一个渲染阻塞属性。当渲染器带有 `full-frame-rate` token 时，它会降低帧率，以便为加载保留资源，进而影响 compositor/渲染管线和调度，优先处理加载任务而不是高频渲染。

#### Use Cases
- 在网络或 CPU 负载较重时，通过降低渲染开销来改善感知加载性能。
- 在复杂页面上，当加载优先级应暂时高于平滑动画时，实现更好的资源分配。

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=397832388
- https://chromestatus.com/feature/5109023781429248

### Pause media playback on not-rendered iframes

#### What's New
Introduces a `media-playback-while-not-rendered` permission policy that allows embedders to pause media playback in iframes that are not rendered (e.g., `display:none`).

#### Technical Details
该权限策略扩展了嵌入方的控制面（Permissions Policy），并钩入嵌套浏览上下文的媒体播放语义。当计算出的 display 为 `none` 时，用户代理可以挂起播放，从而减少不可见 iframe 的 CPU/多媒体解码使用。

#### Use Cases
- 通过暂停隐藏嵌入中的音视频，减少 CPU 和电池消耗。
- 防止来自屏外或隐藏第三方内容的意外音频，改善用户体验。
- 对于性能敏感的页面和嵌入第三方媒体的 PWA 非常有用。

#### References
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=351354996
- https://chromestatus.com/feature/5082854470868992

### Rewriter API

#### What's New
An origin-trial API that transforms and rephrases input text using an on-device AI language model (e.g., shorten, rephrase, make constructive).

#### Technical Details
暴露了一个在设备端通过本地模型执行文本转换的 web API。集成会触及 webapi 表面（新的 DOM interfaces）、隐私控制，并可能与资源管理（用于模型推理的 CPU/GPU 使用）交互。规范来自 WICG；需通过 origin trials 仪表盘注册参与。

#### Use Cases
- 在提交前对用户生成内容进行内联摘要或缩短。
- 客户端侧重写以调整语气或适配受众，避免往返服务器。
- 在本地进行预处理以强制内容长度限制并改善用户体验。

#### References
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=358214322
- https://chromestatus.com/feature/5089854436556800
- https://wicg.github.io/rewriter-api/

### Writer API

#### What's New
An origin-trial API to generate new textual content from a writing task prompt using an on-device AI language model.

#### Technical Details
提供了一个基于设备端模型、根据结构化提示生成文本的生成型 API 表面。作为 origin trial，这涉及请求/响应接口的 webapi 工作、围绕本地模型使用的隐私考量，以及潜在的许可/策略影响。为开发者审阅提供了规范和策略/许可参考资料。

#### Use Cases
- 为用户可见内容生成结构化数据的说明。
- 在客户端编辑器中自动撰写商品描述或扩展大纲。
- 在 Web 应用中直接集成的辅助写作工具，无需服务器端生成。

#### References
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=357967382
- https://chromestatus.com/feature/5089855470993408
- https://wicg.github.io/writer-api/
- https://creativecommons.org/licenses/by/4.0/
- https://www.apache.org/licenses/LICENSE-2.0
- https://developers.google.com/site-policies

已保存的文件路径：
digest_markdown/webplatform/Origin trials/chrome-137-stable-en.md