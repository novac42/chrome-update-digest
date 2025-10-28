---
layout: default
title: html-dom-zh
---

## 领域摘要

Chrome 136 为 Canvas 文本绘制样式添加了语言/区域设置感知，弥补了主线程 <canvas> 与 OffscreenCanvas 渲染之间的差距。对开发者影响最大的是在 worker 上下文中改进了文本渲染的国际化，允许在绘制到 OffscreenCanvas 时进行正确的字体选择和基于区域设置的字形处理。这使 OffscreenCanvas 的行为与现有的 DOM canvas 保持一致，改善了跨线程模型的一致性，并推进了平台对多语言排版的支持。对于在主线程外渲染文本的应用（例如基于 canvas 的编辑器、游戏和服务器端渲染），在字形选择和布局一致性重要的情况下，这些更新很重要。

## 详细更新

以下为实现上述摘要的具体更改。

### Language support for CanvasTextDrawingStyles（CanvasTextDrawingStyles 的语言支持）

#### 新增内容
canvas 文本绘制行为现在在此前不可用的上下文（尤其是 OffscreenCanvas）中尊重 CanvasTextDrawingStyles 的语言/区域设置信息，提供基于区域设置的字体选择和字形处理。

#### 技术细节
- `<canvas>` elements already accept a lang attribute which influences font selection for glyphs with locale variants.
- OffscreenCanvas previously lacked a mechanism to carry locale information to text rendering.
- This update bridges that gap so OffscreenCanvas text drawing can receive the same language context as DOM canvas rendering, ensuring consistent font fallback and glyph selection.

#### 适用场景
- 使用 OffscreenCanvas 的 worker 中实现精确的国际化文本渲染。
- Web 应用、游戏和图形工具在主线程与异步线程间实现一致的排版。
- 在后台线程绘制时，提高对具有区域设置特定字形变体语言（例如 CJK、Arabic、Indic 脚本）的渲染保真度。

#### 参考资料
- [Tracking bug](https://bugs.chromium.org/p/chromium/issues/detail?id=385006131)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5101829618114560)
- [Spec](https://html.spec.whatwg.org/multipage/canvas.html#canvastextdrawingstyles)

## 领域专长（HTML-DOM 焦点）

- css: 此更改影响渲染管线中的字体选择和回退行为；当字形变体依赖于区域设置时，预计能改善布局稳定性。
- webapi: 通过传播语言上下文，使 OffscreenCanvas 文本绘制语义与 DOM canvas API 对齐。
- graphics-webgpu: 将 GPU 支持的渲染与文本层结合使用的 OffscreenCanvas 用户将在跨线程情形下获得更可预测的字形结果。
- javascript: 基于 worker 的绘图脚本在使用 OffscreenCanvas 时现在可以依赖支持区域设置的文本度量和字形选择。
- security-privacy: 未引入新的攻击面；仅遵循现有 canvas 模型传递语言元数据。
- performance: 在不牺牲本地化正确性的前提下，允许更安全的主线程外文本渲染，从而在保持响应性的同时维持渲染保真度。
- multimedia: 改善通过 canvas 在本地化媒体体验中渲染的文本覆盖和字幕。
- devices: 使使用 worker 将文本合成到图形上的设备无关渲染管线受益。
- pwa-service-worker: 在 service worker 上下文用于渲染/离屏任务的 PWA 将渲染出符合区域设置的文本。
- webassembly: 驱动 OffscreenCanvas 文本渲染的 WASM 模块现在可以依赖一致的基于区域设置的字形选择。
- deprecations: 未伴随任何弃用；这是一个减少绕过方案需要的增强。

文件已保存至：digest_markdown/webplatform/HTML-DOM/chrome-136-stable-en.md
