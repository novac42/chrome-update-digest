---
layout: default
title: 领域摘要
---

# 领域摘要

Chrome 136 引入了多媒体功能，重点在于提升编码器平台一致性、对被捕获表面的更细粒度控制，以及改进音频和 SVG 命中测试语义。最具影响力的更改包括在 WebRTC 和 MediaRecorder 中对 HEVC (H.265) 的支持，以及新的屏幕捕获控制（捕获表面控制和分辨率），这些功能支持更高质量的会议、录制和自适应流媒体工作流。AudioContext 增加了一个 "interrupted" 状态以反映独占音频使用场景，改善 VoIP 和合上笔记本盖子情形下的用户体验和资源处理。这些更新通过向 Web 应用公开设备和编码器能力、使实现与规范保持一致并实现更高效的媒体处理，推动了 Web 平台的发展。

## 详细更新

下面的条目将上述摘要与实际实现和开发者注意事项联系起来。

### AudioContext Interrupted State（中断状态）

#### 新增内容
向 AudioContextState 枚举添加了一个 "interrupted" 值，以表示来自独占音频访问（例如 VoIP）或系统操作（如合上笔记本盖子）的临时暂停。

#### 技术细节
- 根据 WebAudio 规范扩展了 Web Audio API 的 AudioContextState。
- 允许用户代理发出与 "suspended" 或 "closed" 不同的非终止性暂停信号。

#### 适用场景
- 会议应用可以检测到中断与正常挂起的区别并调整 UI/行为。
- 媒体播放器可以保留播放状态，并在独占音频结束后恢复。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=374805121
- https://chromestatus.com/feature/5087843301908480
- https://webaudio.github.io/web-audio-api/#AudioContextState

### Captured surface control（捕获表面控制）

#### 新增内容
引入了一个 Web API，允许将滚轮事件转发到被捕获的标签页，并读取/更改被捕获标签页的缩放级别。

#### 技术细节
- 该 API 面向捕获上下文需要对用户交互和远端/被捕获表面的视觉缩放进行细粒度控制的场景。
- 遵循 WICG 关于 captured surface control 的提案。

#### 适用场景
- 希望将滚动手势转发到被捕获内容的屏幕共享 UI。
- 需要调整缩放以提高可读性或减少带宽使用的远程控制流程。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=1466247
- https://chromestatus.com/feature/5064816815276032
- https://wicg.github.io/captured-surface-control/

### CapturedSurfaceResolution（捕获表面分辨率）

#### 新增内容
在屏幕共享期间公开被捕获表面的像素比，便于应用区分物理和逻辑分辨率。

#### 技术细节
- 表面像素比信息允许调用者了解被捕获源的 devicePixelRatio 或等效值。
- 规范与 mediacapture-screen-share-extensions 的扩展点保持一致。

#### 适用场景
- 自适应编码器可根据源像素密度选择分辨率/比特率权衡。
- 录制和流媒体应用可以避免不必要的上/下采样，从而节省 CPU/GPU 资源。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=383946052
- https://chromestatus.com/feature/5100866324422656
- https://w3c.github.io/mediacapture-screen-share-extensions/#capturedsurfaceresolution

### H265 (HEVC) codec support in WebRTC（在 WebRTC 中支持 HEVC）

#### 新增内容
HEVC (H.265) 被加入到可用于 WebRTC 的编码器集合中；支持可通过 MediaCapabilities API 查询。

#### 技术细节
- HEVC 成为可查询的编码器能力，与 VP8/VP9/H.264/AV1 并列。
- 集成遵循 WebRTC 规范中的 RTCRtpCodecCapability 语义。

#### 适用场景
- 在支持硬件的情况下，企业和工作流偏好使用 HEVC 以提高效率，可在点对点连接中协商使用。
- 通过 MediaCapabilities 查询实现自适应 UX：根据硬件/软件可用性选择编码器。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=391903235
- https://chromestatus.com/feature/5104835309936640
- https://www.w3.org/TR/webrtc/#dom-rtcrtpcodeccapability

### H26x Codec support updates for MediaRecorder（MediaRecorder 的 H26x 编解码器支持更新）

#### 新增内容
MediaRecorder 现在支持使用 `hvc1.*` 编解码器字符串进行 HEVC 编码，并添加了 `hev1.*` 和 `avc3.*` 编解码器字符串以支持可变分辨率 MP4。这与早期版本中添加到 WebCodecs 的平台编码支持保持一致。

#### 技术细节
- 扩展了 MediaRecorder 的输出编解码器标识，以反映现代容器和编解码器信号。
- 使在可用时依赖平台 HEVC 编码器的录制工作流可行。

#### 适用场景
- 使用 HEVC 进行高效本地录制以降低存储或带宽需求。
- 录制可变分辨率的 MP4 输出，以便与下游工具（期望 `avc3`/`hev1`/`hvc1` 标签）互操作。

#### 参考资料
- https://chromestatus.com/feature/5103892473503744

### Use DOMPointInit for getCharNumAtPosition, isPointInFill, isPointInStroke（在 getCharNumAtPosition、isPointInFill、isPointInStroke 中使用 DOMPointInit）

#### 新增内容
Chromium 更新了 SVGGeometryElement 和 SVGPathElement API，使 getCharNumAtPosition、isPointInFill 和 isPointInStroke 使用 DOMPointInit 而不是 SVGPoint，以与最新的 W3C 规范保持一致。

#### 技术细节
- API 表面改为接受 DOMPointInit（普通对象），而非 SVGPoint 实例。
- 提高了与现代 DOM 点处理的一致性，并减少对遗留 API 的依赖。

#### 适用场景
- SVG 命中测试和文本布局代码可以传递简单的 JS 对象来表示点坐标。
- 更容易与其他 DOM API 互操作，减少对创建遗留 SVG 对象的依赖。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40572887
- https://chromestatus.com/feature/5084627093929984
- https://www.w3.org/TR/SVG2/types.html#InterfaceDOMPointInit

Saved file:
digest_markdown/webplatform/Multimedia/chrome-136-stable-en.md
