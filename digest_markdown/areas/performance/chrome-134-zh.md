---
layout: default
title: chrome-134-zh
---

## 领域摘要

Chrome 134 的 Performance 更新着重于让开发者更细粒度地控制资源生命周期，减少页面加载期间不必要的推测性工作，并改进高性能的度量工具以获得更准确的测量。最具影响力的更改包括显式资源管理（异步和同步变体），一个可在 Document Policy 中选择退出关联资源推测处理的钩子，以及扩展的 console.timeStamp API，用于在 DevTools 中提供更丰富的时序数据。这些特性共同推动平台前进：实现确定性的清理、减少加载期间浪费的抓取/CPU，以及提供更高保真度的运行时诊断——这对优化内存、启动和运行时性能很重要。

## 详细更新

下面是 Chrome 134 中每个 Performance 领域特性面向开发者的简明描述，包含实现上下文和实际使用场景。

### Document-Policy: `expect-no-linked-resources` (提示无关联资源)

#### 新增内容
Document Policy 中的 `expect-no-linked-resources` 配置点允许文档向用户代理提示以优化其加载顺序，例如通过避免对关联资源的默认推测解析行为。

#### 技术细节
此提示告知用户代理的 HTML 解析/获取 启发式，使其可以跳过推测性解析和对关联资源的推测性抓取，这些抓取本来会由标准解析优化触发。

#### 适用场景
- 明确没有关联资源（样式表、脚本、preload 等）的页面或嵌入文档，可以通过选择退出推测性解析来减少浪费的网络请求和 CPU。
- 控制其资源抓取的单页应用或孤立组件可以在启动期间避免冗余的推测性抓取。

#### 参考资料
- 跟踪问题 #365632977: https://issues.chromium.org/issues/365632977
- ChromeStatus.com 条目: https://chromestatus.com/feature/5202800863346688
- 规范: https://github.com/whatwg/html/pull/10718

### Explicit resource management (async) (异步)

#### 新增内容
为在异步上下文中分配并显式释放资源这一常见模式添加了语言层面的特性，改进了对内存和 I/O 的确定性清理。

#### 技术细节
这些特性暴露了 API 和语义，使异步代码在不再需要关键资源时能够显式释放它们，从而使异步流程中的分配与释放模式保持一致。

#### 适用场景
- 管理文件句柄、流或网络连接的异步 API 可以公开确定性的释放操作，以减少资源保留和 GC 压力。
- 长运行的 Web 应用和 PWA 可以在逻辑任务完成后显式释放资源，从而减少内存和句柄泄漏。

#### 参考资料
- 跟踪问题 #42203814: https://issues.chromium.org/issues/42203814
- ChromeStatus.com 条目: https://chromestatus.com/feature/5087324181102592
- 规范: https://tc39.es/proposal-explicit-resource-management

### Explicit resource management (sync) (同步)

#### 新增内容
为显式资源管理提供了同步对应项，使得在非异步代码路径中也能确定性地释放资源。

#### 技术细节
这些同步特性遵循相同的分配/释放模式，但针对需要立即清理语义的同步使用场景进行了设计。

#### 适用场景
- 需要立即回收资源的底层 API 和库（例如图形或设备句柄）可以提供同步释放机制以避免延迟清理。
- 将类原生的资源管理模式移植到 JS 的开发者可以在不完全依赖 GC 的情况下建模可预测的生命周期。

#### 参考资料
- 跟踪问题 #42203506: https://issues.chromium.org/issues/42203506
- ChromeStatus.com 条目: https://chromestatus.com/feature/5071680358842368
- 规范: https://tc39.es/proposal-explicit-resource-management

### Extend the `console.timeStamp` API to support measurements and presentation options (支持测量与呈现选项)

#### 新增内容
向 `console.timeStamp()` 以向后兼容的方式扩展，提供一种高性能的方式用于插桩并将时序数据呈现在 DevTools 的 Performance 面板中。新条目可以包含自定义时间戳、持续时间和呈现选项。

#### 技术细节
API 扩展会生成与 Performance 面板兼容的时序条目，并可选地携带元数据（时间戳、持续时间、呈现标志），同时保留现有 `console.timeStamp` 在旧用法下的行为。

#### 适用场景
- 在不使用较重的 `performance.mark`/`measure` 工作流的情况下，对子任务持续时间进行低开销插桩。
- 在 DevTools 时间线中使用自定义呈现来注释数据，使性能跟踪对优化更具可操作性。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5133241999425536
- 规范: https://docs.google.com/document/d/1juT7esZ62ydio-SQwEVsY7pdidKhjAphvUghWrlw0II/edit?tab=t.0#heading=h.ekp1q3o1v7v3
