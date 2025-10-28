---
layout: default
title: 领域摘要
---

# 领域摘要

Chrome 138 的 On-device AI 更新以新的 Summarizer API 为中心，这是一个 JavaScript 接口，暴露了用于生成文本摘要的内置语言模型。这样可以减少站点捆绑或获取数 GB 模型的需要，通过启用本地可用的摘要来改善性能、带宽和隐私。对开发者而言，最具影响力的变化是一个标准化的 Web 摘要 API，可在不托管外部模型的情况下集成到 Web 应用中。这些能力通过将原生 AI 文本处理引入浏览器运行时，推动了 Web 平台的发展，支持更丰富的客户端功能。

## 详细更新

下面列出本次发布中与 On-device AI 相关的具体更改以及开发者如何使用它们。

### Summarizer API（摘要器 API）

#### 新增内容
Summarizer API 是一个 JavaScript API，使用可供浏览器/OS 访问的内置 AI 语言模型，对输入文本生成摘要。通过将该模型以标准 API 暴露，站点可在无需下载自有大型模型的情况下使用摘要功能。

#### 技术细节
该 API 通过 JavaScript 向网页呈现由模型支持的摘要功能。底层设计假定浏览器或宿主 OS 将提供对本地语言模型实现的访问，从而允许该 API 在无需每个站点下载模型的情况下运行。有关接口细节请参阅规范，并查看 Chromium 跟踪条目以了解状态。

#### 适用场景
- 在浏览器内对文章或转录进行内联摘要，以改进阅读工作流。
- 对隐私敏感内容进行客户端摘要（保持文本本地化）。
- 相较于获取远程摘要服务或传输大型模型，减少延迟和带宽消耗。
- 支持渐进增强：站点在可用时可以调用该 API，否则回退。

#### 参考资料
- [Link](https://developer.mozilla.org/docs/Web/API/Summarizer)
- [Tracking bug](https://bugs.chromium.org/p/chromium/issues/detail?id=351744634)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5134971702001664)
- [Spec](https://wicg.github.io/summarization-api/)

## 领域相关专业说明

- css: 摘要输出通常集成到 UI 流中；请为可变长度摘要考虑响应式布局，并使用 ARIA 以实现无障碍的呈现。
- webapi: Summarizer API 符合渐进增强模型 — 做功能检测并提供回退。
- graphics-webgpu: On-device AI 可能会共享 GPU 资源；在密集计算与渲染预算间协调，以避免卡顿（jank）。
- javascript: 使用异步模式（Promises/async-await）调用该 API 以避免阻塞主线程；若后处理密集，可将工作卸载到 Web Workers。
- security-privacy: 优先使用本地摘要以尽量减少数据外泄；在集成时审查 CSP 和权限模型。
- performance: 利用设备内模型以降低网络延迟；在目标设备上基准测试内存/CPU。
- multimedia: 转录或字幕的摘要可在客户端生成以增强媒体用户体验（UX）。
- devices: 设备能力检测很重要 — 为低资源设备提供回退。
- pwa-service-worker: 考虑通过 service workers 缓存摘要结果和离线策略。
- webassembly: 若需要 polyfills 或本地模型运行时，WASM 可作为实现路径。
- 弃用: 采用标准化 API 以避免定制客户端模型导致的包体积增大。

Save path:
```text
digest_markdown/webplatform/On-device AI/chrome-138-stable-en.md
