区域摘要

Chrome 137 的 Origin Trials 强调实验性平台控制和本地设备上的生成式 API。对开发者影响最大的更改包括：用于管理资源分配的新渲染阻塞语义、用于暂停未渲染 iframe 媒体的权限策略，以及通过 origin trials 提供的两个由 AI 支持的文本 API（Rewriter 和 Writer）。这些更新使嵌入方能够更细粒度地控制资源与用户体验行为，并在无需服务器依赖的情况下暴露受限的本地 ML 能力。团队应评估权限策略和受 origin-trial 限制的 API 的集成点，以对行为和安全影响进行原型验证。

## 详细更新

Below are concise, developer-focused descriptions of each origin-trial feature in Chrome 137 and how they affect implementation, security, and use cases.

### Full frame rate render blocking attribute（全帧率渲染阻塞属性）

#### 新增内容
新增一个名为 `full-frame-rate` 的渲染阻塞令牌。当渲染器被该令牌阻塞时，它会降低自身帧率以保留 CPU/GPU 资源用于加载。

#### 技术细节
这引入了一个由渲染器的节流逻辑检查的阻塞属性令牌；遵守该令牌的渲染器在被阻塞时将降低帧率，从而将资源重新分配到加载上。origin-trial 的门控允许开发者在更广泛发布前测试其对性能和响应性的影响。

#### 适用场景
- 通过降低动画顺滑性来改善重加载页面的加载性能。
- 测试复杂单页应用或媒体密集型站点的资源管理策略。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=397832388
- https://chromestatus.com/feature/5109023781429248

### Pause media playback on not-rendered iframes（在未渲染的 iframe 上暂停媒体播放）

#### 新增内容
引入一个权限策略 `media-playback-while-not-rendered`，允许嵌入站点在嵌入的 iframe 显示为 `none`（未渲染）时暂停媒体。

#### 技术细节
以权限策略形式暴露，由嵌入方控制；当禁用时，嵌入方可以在未渲染的嵌入框架中暂停或阻止播放。该功能作为 origin-trial 门控特性实现，以观察互操作性和用户体验影响。

#### 适用场景
- 减少后台或隐藏 iframe 媒体产生的不必要 CPU/带宽消耗。
- 改善复杂页面和广告容器中嵌入媒体的电池寿命和性能。

#### 参考资料
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=351354996
- https://chromestatus.com/feature/5082854470868992

### Rewriter API（重写器 API）

#### 新增内容
一个 origin-trial API，使用本地设备上的 AI 语言模型对输入文本进行转换或改写（例如，缩短至字数限制、改变语气）。

#### 技术细节
暴露用于文本转换的 Web API，模型推理在本地设备上执行；规范和试验允许开发者在客户端进行隐私保护的文本重写实验，同时评估模型限制和性能。

#### 适用场景
- 在提交前对用户生成内容进行摘要或简化的 UI 功能。
- 保持文本在本地的客户端编辑工具以尊重隐私。

#### 参考资料
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=358214322
- https://chromestatus.com/feature/5089854436556800
- https://wicg.github.io/rewriter-api/

### Writer API（写作 API）

#### 新增内容
一个 origin-trial API，使得可通过本地 AI 模型根据提示生成新的文本内容。

#### 技术细节
在客户端提供基于提示的文本生成编程接口。origin-trial 的暴露让开发者评估内容质量、性能以及与策略/合规相关的考量。与实现相关的许可与策略文件包含在试验参考资料中。

#### 适用场景
- 在无需服务器端 ML 的情况下生成结构化数据的解释、产品描述或草稿内容。
- 通过本地执行文本生成增强 PWA 的离线能力。

#### 参考资料
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=357967382
- https://chromestatus.com/feature/5089855470993408
- https://wicg.github.io/writer-api/
- https://creativecommons.org/licenses/by/4.0/
- https://www.apache.org/licenses/LICENSE-2.0
- https://developers.google.com/site-policies

此摘要的文件路径:
digest_markdown/webplatform/Origin trials/chrome-137-stable-en.md