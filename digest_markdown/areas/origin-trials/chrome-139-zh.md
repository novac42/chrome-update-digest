---
layout: default
title: chrome-139-zh
---

## Area Summary

Chrome 139 的 Origin trials 聚焦于扩展实验性平台能力，供开发者在标准化之前选择加入新的 API 和行为。主要主题包括多模态 AI 交互（Prompt API）、更长生命周期的后台 JavaScript（extended SharedWorker lifetime）、更细粒度的性能遥测（SoftNavigation）、简化的认证 UX（WebAuth immediate mediation）、渲染器资源控制（full-frame-rate render blocking）以及对 GPU 工作负载更广泛的设备支持（WebGPU compatibility mode）。这些试验允许团队在功能广泛发布前对集成模式、性能影响及安全/兼容性约束进行原型验证和评估，从而在尽量降低风险的同时影响 Web 平台的发展。

## Detailed Updates

Below are the origin-trialized features in Chrome 139 that development teams can opt into to experiment and gather feedback.

### Prompt API

#### What's New
一个用于使用文本、图像和音频输入与 AI 语言模型交互的 API。它支持生成图像标题、视觉搜索、音频转录、声音事件分类、引导式文本生成和抽取等用例。

#### Technical Details
通过一个实验性接口向 Web 应用暴露多模态输入处理（text、image、audio），以便与模型交互。需要进行 origin trial 注册才能测试该能力。

#### Use Cases
- 集成设备端或云端 AI 功能：图像字幕、视觉搜索、转录。
- 原型化将音频、图像和文本输入结合的多模态用户界面。
- 在公开发布前评估 AI 驱动功能的隐私、延迟和用户体验。

#### References
- Origin Trial — https://developer.chrome.com/origintrials/#/register_trial/2533837740349325313
- Tracking bug #417530643 — https://issues.chromium.org/issues/417530643
- ChromeStatus.com entry — https://chromestatus.com/feature/5134603979063296

### Extended lifetime shared workers

#### What's New
Adds an `extendedLifetime: true` option to the `SharedWorker` constructor to request keeping a shared worker alive after all current clients unload.

#### Technical Details
The new constructor option signals the browser to retain the shared worker for post-unload asynchronous work. Pages opting into this origin trial can exercise lifecycle behaviors that persist beyond the last connected client.

#### Use Cases
- 在页面卸载后执行后台清理、遥测上报或最终化任务。
- 支持多标签协同以及无法在卸载前完成的后到达异步工作。
- 评估更长生命周期 worker 在内存和能耗方面的权衡。

#### References
- Origin Trial — https://developer.chrome.com/origintrials/#/register_trial/3056255297124302849
- Tracking bug #400473072 — https://issues.chromium.org/issues/400473072
- ChromeStatus.com entry — https://chromestatus.com/feature/5138641357373440

### `SoftNavigation` performance entry

#### What's New
Exposes experimental soft navigation heuristics via `PerformanceObserver` and the performance timeline, reporting a `soft-navigation` entry and related timing slicing.

#### Technical Details
Reports new performance entries (including `soft-navigation`) and defines a new `timeOrigin` to help slice time ranges for soft navigations. The feature is observable through standard performance APIs while under origin trial control.

#### Use Cases
- 测量并优化重用页面上下文的用户发起导航（软导航）。
- 将交互时序与渲染和网络活动关联，用于单页应用风格的过渡。
- 增强性能分析和 RUM 工具，以考虑页面内导航语义。

#### References
- Origin Trial — https://developer.chrome.com/origintrials#/view_trial/21392098230009857
- Tracking bug #1338390 — https://issues.chromium.org/issues/1338390
- ChromeStatus.com entry — https://chromestatus.com/feature/5144837209194496
- Spec — https://wicg.github.io/soft-navigations

### Web Authentication immediate mediation

#### What's New
A mediation mode for `navigator.credentials.get()` that displays browser sign-in UI immediately if the browser knows a passkey or password for the site; otherwise it rejects with `NotAllowedError`.

#### Technical Details
Immediate mediation changes the get() mediation behavior to proactively surface sign-in UI only when a credential is immediately available to the browser; absence of a known credential leads to a deterministic rejection rather than fallthrough behavior.

#### Use Cases
- 简化浏览器能够立即提供已知凭证的登录流程。
- 在不存在凭证时避免不必要的发现提示，从而改善用户体验和安全明确性。
- 测试与基于 passkey 的认证流程的集成并衡量用户体验影响。

#### References
- Tracking bug #408002783 — https://issues.chromium.org/issues/408002783
- ChromeStatus.com entry — https://chromestatus.com/feature/5164322780872704
- Spec — https://github.com/w3c/webauthn/pull/2291

### Full frame rate render blocking attribute

#### What's New
Adds a new render-blocking token `full-frame-rate` to blocking attributes so the renderer can be blocked with that token and run at a lower frame rate to reserve resources for loading.

#### Technical Details
This attribute introduces a render-blocking token that signals the renderer should lower its frame rate while blocked, allowing more resources to be allocated to loading work. The capability is available via origin trial registration.

#### Use Cases
- 在资源受限设备上，通过在关键加载期间减少合成器/渲染预算来改善加载性能。
- 评估视觉流畅性与更快内容就绪之间的权衡。
- 集成到自适应加载策略中，通过限制渲染以优先处理网络和解析工作。

#### References
- Origin Trial — https://developer.chrome.com/origintrials/#/register_trial/3578672853899280385
- Tracking bug #397832388 — https://issues.chromium.org/issues/397832388
- ChromeStatus.com entry — https://chromestatus.com/feature/5207202081800192

### WebGPU compatibility mode

#### What's New
An opt-in, lightly restricted subset of the WebGPU API that can run on older graphics backends (e.g., OpenGL, Direct3D11), enabling WebGPU apps to reach older devices.

#### Technical Details
Compatibility mode provides a constrained WebGPU subset and requires developers to opt in and obey specific constraints. This allows implementations to map the mode to legacy graphics APIs while preserving a defined surface of WebGPU functionality.

#### Use Cases
- 提高 WebGPU 应用在没有现代图形驱动的设备上的覆盖范围。
- 原型化回退策略并测量原生 WebGPU 与兼容模式实现之间的性能/功能差距。
- 验证着色器/工作负载的可移植性及开发者工具，以支持更广泛的设备。

#### References
- Origin Trial — https://developer.chrome.com/origintrials/#/register_trial/1489002626799370241
- Tracking bug #40266903 — https://issues.chromium.org/issues/40266903
- ChromeStatus.com entry — https://chromestatus.com/feature/6436406437871616
- Spec — https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md

已保存至: digest_markdown/webplatform/Origin trials/chrome-139-stable-en.md
