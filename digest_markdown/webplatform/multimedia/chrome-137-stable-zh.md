## 领域摘要

Chrome 137 引入了一项针对多媒体的精简更新：在未渲染的 iframe 中暂停媒体播放的权限策略。面向开发者的主要变更是新的 `media-playback-while-not-rendered` permission policy，允许嵌入方停止那些 `display: none` 的 iframe 中的媒体播放。这使站点能够明确控制嵌入媒体的行为，并通过 origin trials 逐步推出并在 Chromium 中跟踪。此类更改的重要性在于它们使开发者能够减少意外的后台播放并更好地控制嵌入媒体的生命周期。

## 详细更新

下面是 Chrome 137 中多媒体更改的详细信息以及开发者应了解的要点。

### Pause media playback on not-rendered iframes (在未渲染的 iframe 上暂停媒体播放)

#### 新增内容
新增了一个 `media-playback-while-not-rendered` permission policy，允许嵌入方网站暂停那些未渲染的嵌入 iframe 的媒体播放——即其 display 属性被设置为 `none` 的 iframe。

#### 技术细节
- 以名为 `media-playback-while-not-rendered` 的 permission policy 形式暴露。
- 目标是未渲染的 iframe（发布数据中明确指出以 `display: none` 作为标识）。
- 在发布元数据中标记为 origin-trials 功能，以便分阶段推出。

#### 适用场景
- 使嵌入方能够阻止隐藏的 iframe 中的音频/视频播放。
- 允许开发者实现更可预测的嵌入媒体用户体验（发行说明指出这“应该允许开发者构建更以用户为中心的体验”）。

#### 参考资料
- Origin Trial: https://developer.chrome.com/origintrials/#/trials/active
- 跟踪 bug #351354996: https://bugs.chromium.org/p/chromium/issues/detail?id=351354996
- ChromeStatus.com 条目: https://chromestatus.com/feature/5082854470868992

## 领域专长（多媒体要点）

- css: 以 `display: none` 作为“未渲染”的信号；在与此策略交互时请有意地调整 CSS。
- webapi: 作为 permission policy 呈现；嵌入方将通过文档级别的策略头或属性选择控制 iframe 媒体。
- graphics-webgpu: 对 GPU 管线没有直接的 API 更改；在某些场景下，暂停隐藏 iframe 中的媒体可减少渲染压力。
- javascript: 控制权仍在嵌入方策略层；脚本仍可切换 iframe 的渲染状态以影响播放行为。
- security-privacy: 作为 permission policy 实现，将控制权保留在嵌入源而非跨源内容。
- performance: 暂停隐藏 iframe 的媒体有助于避免用户不可见的媒体元素引起的不必要 CPU/网络 使用。
- multimedia: 直接影响嵌入音频/视频的播放行为；有助于减少不希望的后台播放。
- devices: 通过停止隐藏媒体播放，间接降低设备资源消耗。
- pwa-service-worker: 对 service worker 没有直接更改，但嵌入媒体的生命周期在离线/前台场景中可能更可预测。
- webassembly: 对 WASM 运行时无影响；收益体现在嵌入/DOM 层。
- 弃用: 通过 origin trial 发布——请监控 ChromeStatus 和跟踪 bug 以获取推出与迁移指南。