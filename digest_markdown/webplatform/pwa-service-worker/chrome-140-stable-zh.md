# Chrome 140 正式版 - PWA 和 Service Worker 更新

## 概述

Chrome 140 引入了对 service worker 功能的重大改进，专注于增强规范合规性和更好的开发者调试能力。最显著的变化包括修复 blob URL 的 SharedWorker 控制器继承问题以符合 Web 标准，以及为 ServiceWorker Static routing API 添加全面的时序信息以改进性能监控和调试。

## 功能详情

### `SharedWorker` 脚本为 blob 脚本 URL 继承控制器

**变更内容**：
此更新修复了 Chrome 实现与 Web 规范之间关于 service worker 控制器的长期差异。之前，虽然专用 worker 可以按规范为 blob URL 继承控制器，但共享 worker 无法做到这一点。Chrome 140 纠正了此行为，确保 SharedWorker 脚本在使用 blob 脚本 URL 时现在能够正确继承控制器，使 Chrome 完全符合 ServiceWorker 规范。此更改由 `SharedWorkerBlobURLFixEnabled` 企业策略控制，以便渐进式推出，并在需要时进行回滚。

**参考资料**：
- [跟踪错误 #324939068](https://issues.chromium.org/issues/324939068)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5137897664806912)
- [规范](https://w3c.github.io/ServiceWorker/#control-and-use-worker-client)

### 添加 `ServiceWorkerStaticRouterTimingInfo`

**变更内容**：
Chrome 140 为 ServiceWorker Static routing API 引入了全面的时序信息，通过导航时序 API 和资源时序 API 暴露详细的性能指标。此增强为开发者提供了关于 service worker 性能的重要洞察，通过添加两个与 Static routing API 相关的关键时序数据。这些指标帮助开发者了解其 service worker 路由决策的性能特征，使离线优先应用程序和 PWA 能够进行更好的优化。时序信息标记了与静态路由相关的 service worker 生命周期中的特定时点，为开发者提供识别瓶颈和改善用户体验所需的数据。

**参考资料**：
- [跟踪错误 #41496865](https://issues.chromium.org/issues/41496865)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6309742380318720)
- [规范](https://github.com/w3c/ServiceWorker)