---
layout: default
title: chrome-140-zh
---

## 详细更新

下面是 Chrome 140 stable 中引入的每个 Origin Trial 的简明、面向开发者的分解，与上文摘要相对应。

### Enable incoming call notifications（启用来电通知）

#### 新增内容
对 Notifications API 的扩展，允许已安装的 PWA 发送包含来电样式操作按钮和铃声的来电通知，以便更易识别和响应的 VoIP 通知。

#### 技术细节
- 通过为注册站点发放 Origin Trial token 的方式，将其作为 Notifications API 的扩展呈现。
- 目标是让已安装的 PWA 展示更丰富的通知 UI 和声音反馈；集成依赖于平台通知通道。
- 相关领域：webapi、multimedia、devices、pwa-service-worker、security-privacy（用户同意和通知权限）。

#### 适用场景
- 提供类原生来电提示的 VoIP 和远程会议 Web 应用。
- 通过展示铃声和专用操作按钮来提高用户参与度并减少漏接来电。

#### 参考资料
- https://developer.chrome.com/origintrials/#/register_trial/2876111312029483009
- https://issues.chromium.org/issues/detail?id=1383570
- https://chromestatus.com/feature/5110990717321216
- https://notifications.spec.whatwg.org

### Crash Reporting key-value API（崩溃报告 键值 API）

#### 新增内容
一个试验性的 window.crashReport 键值 API，公开了一个每文档的映射，可用于在渲染器崩溃时将键/值数据附加到 CrashReportBody 中。

#### 技术细节
- API 面向脚本的每文档映射；条目在渲染器崩溃时序列化到 CrashReportBody 中。
- 旨在在无需服务器端插装的情况下协助崩溃后的诊断；必须评估隐私和数据泄露风险。
- 相关领域：webapi、security-privacy、performance（调试影响）、弃用（从自定义日志模式的迁移）。

#### 适用场景
- 附加上下文调试元数据（状态标识、功能标志）以协助崩溃排查。
- 提高复杂单页应用和 PWA 的崩溃分析准确性。

#### 参考资料
- https://developer.chrome.com/origintrials/#/register_trial/1304355042077179905
- https://issues.chromium.org/issues/400432195
- https://chromestatus.com/feature/6228675846209536
- https://github.com/WICG/crash-reporting/pull/37

### Add the `clipboardchange` event（添加 `clipboardchange` 事件）

#### 新增内容
一个在系统剪贴板更改时触发的 DOM 事件，使 Web 应用能够在不轮询的情况下同步其内部剪贴板状态。

#### 技术细节
- 事件分发给通过 Origin Trial 选择加入的页面；它反映来自任意应用的系统级剪贴板更改。
- 设计者必须考虑用户隐私和权限模型，因为剪贴板内容可能包含敏感数据。
- 相关领域：webapi、security-privacy、performance、devices（输入）、multimedia（文本/媒体剪贴板）。

#### 适用场景
- 远程桌面和协作应用高效地保持本地与远程剪贴板同步。
- 消除昂贵的周期性剪贴板轮询，从而降低 CPU 和电池消耗。

#### 参考资料
- https://developer.chrome.com/origintrials/#/register_trial/137922738588221441
- https://issues.chromium.org/issues/41442253
- https://chromestatus.com/feature/5085102657503232
- https://github.com/w3c/clipboard-apis/pull/239

### Enable `SharedWorker` on Android（在 Android 上启用 `SharedWorker`）

#### 新增内容
一个 Origin Trial，使 Android 上支持 SharedWorker，从而允许多个浏览上下文（选项卡）共享单个 worker 实例。

#### 技术细节
- 在 Android 构建中通过 Origin Trial token 启用 SharedWorker API，以便站点测试跨选项卡共享脚本和连接。
- 解决资源共享场景，例如共享 WebSocket 或 SSE 连接，以减少重复的网络和 CPU 工作。
- 相关领域：webapi、performance、pwa-service-worker、devices、security-privacy（origin 隔离和生命周期）。

#### 适用场景
- 在多个选项卡之间共享单个 WebSocket/SSE，以减少连接数和内存占用。
- 在移动端实现选项卡之间的集中协调，用于缓存、状态同步和后台工作。

#### 参考资料
- https://developer.chrome.com/origintrials/#/register_trial/4101090410674257921
- https://chromestatus.com/feature/6265472244514816
- https://html.spec.whatwg.org/multipage/workers.html#shared-workers-and-the-sharedworker-interface

已保存文件路径：digest_markdown/webplatform/Origin trials/chrome-140-stable-en.md
