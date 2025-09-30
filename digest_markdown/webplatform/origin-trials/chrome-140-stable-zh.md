领域摘要

Chrome 140 的 Origin Trials 专注于为已安装的 Web 应用扩展平台能力，并改进开发者遥测与后台协调。主要主题包括更丰富的 PWA 通知（来电 UI）、面向开发者的崩溃元数据、系统级剪贴板事件以及在 Android 上启用 SharedWorker。这些试验通过改进实时通信、提高可观测性以增强可靠性、增强系统集成和多标签资源共享来推进 Web 平台。总体而言，它们降低了 VoIP、远程桌面和多上下文 Web 应用的集成摩擦，同时暴露出开发者必须处理的安全和隐私权衡。

## 详细更新

以下是本次发布中每个 Origin Trial 的简明、面向开发者的说明，以及它们在实现、安全和常见使用场景方面的含义。

### Enable incoming call notifications（启用来电通知）

#### 新增内容
扩展了 Notifications API，以便已安装的 PWA 发送类似来电的通知，包含来电样式的操作和铃声，从而更明显地提示 VoIP 来电。

#### 技术细节
这是一个 Origin Trial，通过 Notifications API 为已安装的 PWA 暴露类似来电的通知能力。可预期的集成点包括 PWA 的安装状态、通知操作按钮以及播放铃声。请注意 Notifications 规范和平台通知行为施加的权限与用户体验约束。

#### 适用场景
VoIP 和视频通话 Web 应用可以展示可识别的来电界面，提高用户响应性并与原生来电通知达到接近的一致性。

#### 参考资料
- https://developer.chrome.com/origintrials/#/register_trial/2876111312029483009
- https://issues.chromium.org/issues/detail?id=1383570
- https://chromestatus.com/feature/5110990717321216
- https://notifications.spec.whatwg.org

### Crash Reporting key-value API（崩溃报告键值 API）

#### 新增内容
引入了一个针对文档的键值 API（暂名 window.crashReport），当 renderer 崩溃时，其映射内容会附加到崩溃报告中。

#### 技术细节
该 API 提供了一个文档作用域的后备映射，其条目在 renderer 进程失败时被序列化到 CrashReportBody。此 Origin Trial 为开发者提供了一个受控通道，用于将诊断元数据附加到崩溃报告中，从而改进事后分析，但需要谨慎处理敏感数据。

#### 适用场景
通过为渲染器崩溃添加上下文状态注释（功能标志、最近操作）来改进崩溃分诊。对复杂的单页应用、PWA 以及调试生产环境的稳定性回归特别有用。

#### 参考资料
- https://developer.chrome.com/origintrials/#/register_trial/1304355042077179905
- https://issues.chromium.org/issues/400432195
- https://chromestatus.com/feature/6228675846209536
- https://github.com/WICG/crash-reporting/pull/37

### Add the `clipboardchange` event（添加 `clipboardchange` 事件）

#### 新增内容
新增一个在系统剪贴板内容更改时触发的 clipboardchange 事件，使无需轮询即可高效同步。

#### 技术细节
此 Origin Trial 暴露了一个表示系统剪贴板变更的 DOM 事件。实现需调和平台剪贴板的隐私/安全模型，并可能通过焦点、权限或用户手势策略限制事件派发，以降低数据外泄风险。

#### 适用场景
远程桌面客户端和生产力类 Web 应用可以将页面内剪贴板状态与系统剪贴板保持同步，提升复制/粘贴工作流的用户体验。

#### 参考资料
- https://developer.chrome.com/origintrials/#/register_trial/137922738588221441
- https://issues.chromium.org/issues/41442253
- https://chromestatus.com/feature/5085102657503232
- https://github.com/w3c/clipboard-apis/pull/239

### Enable `SharedWorker` on Android（在 Android 上启用 `SharedWorker`）

#### 新增内容
在 Android 上启用 SharedWorker 支持，允许多个标签/上下文共享单个 worker，从而实现共享连接和资源高效的协调。

#### 技术细节
此 Origin Trial 在 Android 平台启用了 SharedWorker 接口。SharedWorkers 允许来自同一源的多个浏览上下文与共享的脚本上下文通信，适用于共享 WebSocket/SSE 连接和集中式状态。开发者应关注生命周期语义、跨文档消息传递以及与 HTML 规范的一致性。

#### 适用场景
通过在标签间共享单个 WebSocket 或 SSE 来节省资源；在 Android 上同一源的多个标签间协调后台任务或集中缓存。

#### 参考资料
- https://developer.chrome.com/origintrials/#/register_trial/4101090410674257921
- https://chromestatus.com/feature/6265472244514816
- https://html.spec.whatwg.org/multipage/workers.html#shared-workers-and-the-sharedworker-interface

已保存文件：digest_markdown/webplatform/Origin trials/chrome-140-stable-en.md