---
layout: default
title: multimedia-zh
---

## Area Summary

Chrome 139 (stable) 在多媒体方面的进展包括公开更丰富的运行时元数据并改进影响媒体 UX 的凭证调解。两个突出变化是：为已编码的 WebRTC 帧新增音量级别暴露，以及 navigator.credentials.get() 的“immediate”调解模式。这些更新帮助开发者构建更响应的实时音频功能（电平计、VAD、遥测）和更顺畅的凭证驱动 UX，这对媒体应用很重要。它们共同将 Web 平台推进到更底层的媒体可观察性和更快的凭证驱动体验。

## Detailed Updates

Below are concise, developer-focused explanations of each Multimedia-area change and why they matter to real-time media applications and services.

### Audio level for RTC encoded frames (为 RTC 编码帧提供音量级别)

#### What's New
This feature exposes the audio level of an encoded audio frame transmitted via RTCPeerConnection and surfaced to web code using WebRTC encoded transforms.

#### Technical Details
The capability is defined in the encoded-transform WebRTC specification for RTCEncodedAudioFrame metadata (see spec link). It surfaces per-frame audio level information from encoded frames so web-level transforms and analytics can access energy/level metrics without decoding raw PCM.

#### Use Cases
- 在 encoded-transform 中实现的语音活动检测或静音检测，而无需完全解码。
- 用于诊断和分析的 UI 级别音频电平计和按参与者的电平遥测。
- 基于每帧能量测量的信息进行自适应比特率或编解码器选择启发式。
- 在 encoded transforms 内基于电平的内容审核和录制触发。

#### References
- https://issues.chromium.org/issues/418116079
- https://chromestatus.com/feature/5206106602995712
- https://w3c.github.io/webrtc-encoded-transform/#dom-rtcencodedaudioframemetadata-audiolevel

### Web Authentication immediate mediation (立即型凭证调解)

#### What's New
Adds an "immediate" mediation mode for navigator.credentials.get() that prompts the browser sign-in UI only when a passkey or password for the site is immediately known to the browser; otherwise the call rejects with NotAllowedError.

#### Technical Details
This mediation mode is surfaced as an additional option to navigator.credentials.get() (origin-trial-tagged in this release). It changes the credential selection UX to be immediate-only, avoiding fallback prompts when no known credential exists. See the linked spec PR and tracking bug for implementation notes and origin-trial status.

#### Use Cases
- 媒体服务的快速登录路径，减少摩擦以改善播放/认证流程。
- 嵌入式或自动化媒体客户端中需要确定性凭证流程的场景，能够立即判断浏览器是否持有凭证。
- 面向媒体的 Web 应用中的无密码/优先使用 passkey 的 UX，需将对播放或采集流程的中断降到最低。

#### References
- https://issues.chromium.org/issues/408002783
- https://chromestatus.com/feature/5164322780872704
- https://github.com/w3c/webauthn/pull/2291

File saved to: digest_markdown/webplatform/Multimedia/chrome-139-stable-en.md
