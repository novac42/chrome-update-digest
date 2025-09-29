## Area Summary

Chrome 137 (stable) 引入了一项新的权限策略，使嵌入方能够对 iframe 媒体进行更细粒度的控制。本次 Multimedia 的主要主题是允许嵌入方暂停未渲染（例如 `display: none`）的 iframe 中的媒体，从而改善用户体验并降低资源使用。对开发者影响最大的是新的 media-playback-while-not-rendered 权限策略，该策略在 origin trial 期间公开。通过将媒体播放决策移向嵌入上下文，这些控制推动了 Web 平台的发展，使复杂页面具备更好的用户体验和潜在的性能提升。

## Detailed Updates

Below are the Multimedia-specific changes that follow from the summary above.

### Pause media playback on not-rendered iframes (暂停未渲染 iframe 中的媒体播放)

#### What's New
新增了 media-playback-while-not-rendered 权限策略，允许嵌入方网站暂停未渲染的嵌入 iframe 中的媒体播放——即其 display 属性被设置为 `none`。

#### Technical Details
该权限策略允许嵌入方选择在未渲染（`display: none`）的 iframe 内暂停媒体。该能力作为权限策略特性公开，并通过 origin trial 逐步推出。

#### Use Cases
- 嵌入方可以暂停或防止隐藏 iframe 中的媒体使用资源，以提升感知的用户体验和页面响应性。
- 嵌入第三方媒体的网站在 iframe 内容不可见时，可以减少后台 CPU/带宽 使用。

#### References
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=351354996
- https://chromestatus.com/feature/5082854470868992

## Area-Specific Expertise (Multimedia-focused)

- css: 该功能针对通过 CSS 导致的未渲染状态（`display: none`）的 iframe，使媒体行为与布局可见性一致。
- webapi: 通过权限策略（media-playback-while-not-rendered）向嵌入方暴露控制。
- multimedia: 通过在未渲染时允许暂停，直接影响 iframe 内的媒体生命周期。
- performance: 有助于降低不可见 iframe 内容的后台媒体开销（CPU、网络）。
- security-privacy: 通过正式的权限策略和 origin trial 推出，将控制权移至嵌入源，同时尊重 iframe 边界。
- javascript: 嵌入方可通过服务器端或属性配置切换该策略；iframe 内的脚本会感知已暂停的播放状态。
- devices / graphics-webgpu / pwa-service-worker / webassembly / deprecations: 本次发布中该功能未引入额外项目。