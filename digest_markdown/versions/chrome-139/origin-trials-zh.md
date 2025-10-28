---
layout: default
title: 领域摘要
---

# 领域摘要

Chrome 139 的 origin trials 侧重于扩展平台在 AI 交互、后台工作、性能可观测性、身份验证体验、渲染资源管理和更广泛的 WebGPU 覆盖方面的能力。对开发者影响最大的更改包括：用于 AI 输入的多模态 Prompt API、用于卸载后工作的延长生命周期 `SharedWorker`、用于丰富交互遥测的新软导航性能条目、WebAuth 流程的即时调解、影响渲染器行为的全帧率渲染阻塞令牌，以及用于扩大 WebGPU 设备支持的兼容模式。这些试验共同提供了可提升应用响应性、离线/后台工作流、性能测量和图形可移植性的新原语，同时也暴露了开发者必须管理的权衡。

## 详细更新

下面的条目围绕上述主题展开，提供简明的技术背景、实际适用场景，以及指向 origin trial 注册、跟踪 bug 和规范的链接。

### Prompt API（提示 API）

#### 新增内容
一个使用文本、图像和音频输入与 AI 语言模型交互的 API，支持生成字幕、视觉搜索、转录、分类、遵循指令的文本生成和信息提取。

#### 技术细节
公开了一个面向 Web 的输入/输出模型，接受多模态输入；作为一个由 origin trial 保护的 web API 集成到 Web 平台中。开发者应为客户端直接调用模式以及在模型或计费受限时的服务器辅助流程做好规划。

#### 适用场景
图像字幕、页面内视觉搜索、客户端音频转录、嵌入网页应用的多模态助手，以及接收用户提供的图像/音频的自动化工作流。

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/2533837740349325313)
- [Tracking bug](https://issues.chromium.org/issues/417530643)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5134603979063296)

### Extended lifetime shared workers（延长生命周期的 shared workers）

#### 新增内容
在 `SharedWorker` 构造函数中新增 `extendedLifetime: true` 选项，用于请求在所有客户端卸载后继续保持 worker 存活，从而支持在页面卸载后继续运行的异步工作。

#### 技术细节
此 origin-trial 选项改变了 shared worker 的生命周期语义，允许在客户端卸载事件后继续执行后台 JS。开发者必须处理资源生命周期、持久化以及潜在的电量/性能影响；并考虑与 service worker 及页面卸载序列的集成。

#### 适用场景
在导航后进行的延迟上传或分析数据刷新，多页面之间的协调任务，以及避免在客户端卸载时立即终止的后台处理。

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/3056255297124302849)
- [Tracking bug](https://issues.chromium.org/issues/400473072)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5138641357373440)

### `SoftNavigation` performance entry（SoftNavigation 性能条目）

#### 新增内容
通过 `PerformanceObserver` 和性能时间线公开实验性软导航启发式，报告 `soft-navigation` 条目和新的 `timeOrigin`，以帮助切分过渡测量。

#### 技术细节
为软导航（无完整导航的用户交互）添加了性能时间线条目类型。开发者可以通过标准的 PerformanceObserver API 观察这些条目，并将其与其他时间线事件关联，以获得准确的交互到渲染度量。

#### 适用场景
测量和优化单页应用导航，量化路由过渡的交互延迟，以及通过识别代价高的软导航路径来改进 UX。

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials#/view_trial/21392098230009857)
- [Tracking bug](https://issues.chromium.org/issues/1338390)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5144837209194496)
- [Spec](https://wicg.github.io/soft-navigations)

### Web Authentication immediate mediation（Web Authentication 即时调解）

#### 新增内容
为 `navigator.credentials.get()` 引入一种调解模式，当网站的通行密钥或密码已知时会触发浏览器的登录 UI；否则会以 `NotAllowedError` 拒绝。

#### 技术细节
新增了一种影响凭证调解行为的即时调解模式，改变了 WebAuthn 流程的运行时 UX 路径，并影响凭证发现与用户提示的触发方式。

#### 适用场景
当凭证已存在时提供简化的登录体验、有条件的凭证提示流程，以及为希望在可用时提供即时低摩擦认证的网站改进新用户体验。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/408002783)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5164322780872704)
- [GitHub](https://github.com/w3c/webauthn/pull/2291)

### Full frame rate render blocking attribute（全帧率渲染阻塞属性）

#### 新增内容
引入一个作为阻塞属性的渲染阻塞令牌（"full-frame-rate"）；当被持有时，渲染器会以较低的帧率运行以保留资源用于加载。

#### 技术细节
提供了一个影响帧率预算和调度的渲染器级令牌，以优先考虑加载工作。该功能受 origin-trial 限制；开发者需在感知到的 UI 平滑度与关键加载期间的资源可用性之间进行权衡。

#### 适用场景
在资源密集的页面上优化关键路径资源加载，降低高帧率渲染与加载同时发生时引起的卡顿，并在页面过渡期间调整渲染器行为。

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/3578672853899280385)
- [Tracking bug](https://issues.chromium.org/issues/397832388)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5207202081800192)

### WebGPU compatibility mode（WebGPU 兼容模式）

#### 新增内容
一种可选的、受轻度限制的 WebGPU 子集，可在较旧的图形 API（例如 OpenGL、Direct3D11）上运行，从而将 WebGPU 应用的覆盖范围扩展到旧设备。

#### 技术细节
兼容模式限制或改变某些 WebGPU 能力，使实现可以映射到传统图形后端。origin-trial 注册允许开发者检测并选择加入该模式，优雅降级或调整着色器/工作流。

#### 适用场景
为 WebGPU 应用提供更广的设备支持、在高端特性为条件的渐进增强路径，以及简化将 WebGL/OpenGL 代码路径迁移到 WebGPU 的工作量。

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/1489002626799370241)
- [Tracking bug](https://issues.chromium.org/issues/40266903)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6436406437871616)
- [GitHub](https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md)

File: digest_markdown/webplatform/Origin trials/chrome-139-stable-en.md
