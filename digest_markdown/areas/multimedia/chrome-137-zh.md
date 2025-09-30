---
layout: default
title: chrome-137-zh
---

## 区域摘要

Chrome 137 引入了一个 origin-trial 权限策略，针对未渲染 iframe 的嵌入媒体播放控制。核心更改允许嵌入者暂停其 display 为 `none` 的 iframe 中的媒体，从而对嵌入内容进行更有意图的控制。对于需要优化用户体验并管理隐藏框架资源使用的开发者而言，这一改变很重要。该更新通过在跨框架边界的媒体行为中暴露一个由嵌入者控制的钩子，推动了 Web 平台的发展。

## 详细更新

以下为与上述摘要相关的多媒体领域更改。

### Pause media playback on not-rendered iframes (在未渲染的 iframe 上暂停媒体播放)

#### 新增内容
- 新增了 `media-playback-while-not-rendered` 权限策略，允许嵌入站点暂停未渲染（即其 display 属性设置为 `none`）的嵌入 iframe 的媒体播放。该能力以 origin trial 形式提供。

#### 技术细节
- 引入权限策略令牌 `media-playback-while-not-rendered`。
- 允许嵌入者控制当 iframe 未渲染（display: none）时其内部媒体是否继续播放。
- 通过 Chrome 的 origin trial 机制交付（有关注册和详细信息，请参阅 Origin Trial 链接）。

#### 适用场景
- 防止隐藏的 iframe 中的媒体继续播放，提升用户对音视频行为的可预测性。
- 通过在未渲染的框架中停止播放，减少无谓的 CPU/网络 资源消耗及潜在电池影响。
- 为嵌入站点提供更细粒度的跨框架多媒体行为控制，以优化用户体验和资源管理。

#### 参考资料
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=351354996
- https://chromestatus.com/feature/5082854470868992

此摘要的文件路径：
digest_markdown/webplatform/Multimedia/chrome-137-stable-en.md
