---
layout: default
title: chrome-137-zh
---

## 详细更新

以下列出 Chrome 137 中新增的 On-device AI 功能，每项均说明新增内容、技术细节、开发者适用场景，以及指向规范、origin trial 和跟踪问题的链接。

### Rewriter API

#### 新增内容
Rewriter API 提供接口以按请求方式转换和改写输入文本，底层由本地设备的 AI 语言模型提供支持。

#### 技术细节
- API 面由 WICG Rewriter 规范定义。
- 通过 origin trial 启用以供测试。
- 实现和进展通过所提供的 Chromium issue 跟踪。

#### 适用场景
- 删除冗余以将文本控制在字数限制内。
- 按目标受众改写消息措辞。
- 使消息更具建设性或调整语气。

#### 参考资料
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=358214322
- https://chromestatus.com/feature/5089854436556800
- https://wicg.github.io/rewriter-api/

### Writer API

#### 新增内容
Writer API 允许在给定写作任务提示的情况下生成新文本，使用本地设备的 AI 语言模型。

#### 技术细节
- API 在 WICG Writer 规范中指定。
- 可通过 origin trial 进行试验。
- 实现和进展在所链接的 Chromium issue 中跟踪。
- 为内容和规范重用提供了相关许可和站点政策参考。

#### 适用场景
- 为结构化数据生成文本说明。
- 使用评价或产品描述撰写关于产品的帖子。
- 根据开发者提供的提示以编程方式生成写作内容。

#### 参考资料
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=357967382
- https://chromestatus.com/feature/5089855470993408
- https://wicg.github.io/writer-api/
- https://creativecommons.org/licenses/by/4.0/
- https://www.apache.org/licenses/LICENSE-2.0
- https://developers.google.com/site-policies

领域特定专长（On-device AI 的影响）

- css: 最小的直接影响；在嵌入编辑器控件时，重写/写入控制的 UI 应遵循响应式布局和可访问的表单控件。
- webapi: 这些 API 扩展了用于自然语言处理的 Web 平台表面，需要谨慎设计 API 易用性以及与现有 DOM APIs 一致的 promise/async 模式。
- graphics-webgpu: 本地设备模型加速可能利用 GPU 计算；团队应协调推理资源与图形工作负载的使用以避免争用。
- javascript: 集成将通过标准 JS promises/events 进行；在处理生成内容时，开发者应管理异步任务生命周期和内存。
- security-privacy: 本地执行减少了网络暴露；开发者仍需处理用户同意、内容政策以及输入/输出中的潜在 PII。
- performance: 本地推理改变了延迟特性——预计往返时间更低，但需考虑客户端设备的 CPU/GPU 和功耗影响。
- multimedia: 文本生成可以与 TTS 或字幕管线结合；在生成多媒体输出时确保同步和格式兼容性。
- devices: 硬件差异很重要；功能可用性和性能将取决于设备的 ML 能力和厂商驱动。
- pwa-service-worker: PWA 可以缓存提示并管理离线用户体验，但在模型驱动的任务期间，service workers 不应阻塞 UI 线程。
- webassembly: 当本地模型暴露本机运行时时，WASM 可以作为定制模型运行时或预/后处理的集成路径。
- 弃用: 此处未引入弃用；迁移指南应侧重于采用这些新 API，而非临时的 JS 库。

保存文件到: digest_markdown/webplatform/On-device AI/chrome-137-stable-en.md
