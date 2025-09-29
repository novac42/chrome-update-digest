---
layout: default
title: chrome-137-zh
---

## Area Summary

Chrome 137 (stable) 引入了一个针对性的多媒体控制：一个 origin-trial 的 permission policy，允许嵌入方暂停未渲染 iframe 中的媒体播放。主要目的是赋予嵌入站点对隐藏 iframe 内容播放的显式控制。此更改对嵌入第三方或跨源媒体且需要可预测播放行为的开发者影响最大。它通过将 permission-policy 控制扩展到多媒体播放场景，促进平台演进，帮助嵌入方管理用户体验和资源使用。

## Detailed Updates

Below are the Multimedia-area details for Chrome 137 (stable), focused on developer-facing behavior and integration points.

### Pause media playback on not-rendered iframes

#### What's New
Adds a `media-playback-while-not-rendered` permission policy to allow embedder websites to pause media playback of embedded iframes which aren't rendered—that is, have their display property set to `none`.

#### Technical Details
- Exposed as a permission policy named `media-playback-while-not-rendered`.
- Available as an Origin Trial for Chrome 137 (see references).

#### Use Cases
- Enables embedder sites to prevent audio/video from playing inside iframes that are not visually rendered, improving control over embedded content.
- Useful for embedding scenarios where hidden iframes should not consume audio output or playback resources.

#### References
- Origin Trial: https://developer.chrome.com/origintrials/#/trials/active
- Tracking bug #351354996: https://bugs.chromium.org/p/chromium/issues/detail?id=351354996
- ChromeStatus.com entry: https://chromestatus.com/feature/5082854470868992

## Area-Specific Expertise Notes (Multimedia-focused)

- css: Uses the rendered state concept (e.g., display:none) to decide playback suppression.
- webapi: Surface provided via a permission policy mechanism for embedders.
- multimedia: Impacts when codecs and decoders may be kept active for hidden embeds.
- performance: Gives embedders a lever to reduce wasted playback work for non-rendered iframes.
- security-privacy: Permission policy model maintains embedder authority over iframe playback behavior.
- javascript / pwa-service-worker / webassembly / devices / graphics-webgpu / deprecations: No new platform ABI or 弃用 indicated in the provided data.
