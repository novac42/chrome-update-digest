# Chrome Update Analyzer - PWA and Service Worker (Chrome 140)

## Area Summary

Chrome 140 带来了针对 service worker 功能的改进，增强了规范合规性和开发者可观察性。本次发布专注于修复共享 worker 和专用 worker 之间长期存在的行为不一致问题，同时为 ServiceWorker Static routing API 添加了关键的时序测量工具。这些更新通过确保更可预测的 service worker 行为并为开发者提供更好的路由决策性能监控能力，加强了 Progressive Web Apps 的基础。

## Detailed Updates

在核心 service worker 改进的基础上，Chrome 140 引入了合规性修复和新的开发者工具，这将增强 PWA 开发工作流程。

### `SharedWorker` script inherits controller for blob script URL

#### What's New
Chrome 现在正确实现了规范要求，即共享 worker 在使用 blob URL 时应继承 service worker 控制器，使行为与专用 worker 保持一致。

#### Technical Details
此前，Chrome 仅允许专用 worker 为 blob URL 继承 service worker 控制器，而共享 worker 尽管规范要求如此，却不会继承此控制器。此修复确保了不同 worker 类型间的一致行为。`SharedWorkerBlobURLFixEnabled` 企业策略为可能需要管理此过渡的企业环境提供了对此更改的控制。

#### Use Cases
此修复确保在使用带有 blob 脚本的共享 worker 时，PWA 行为更加可预测，对于依赖 service worker 拦截进行缓存或路由的应用程序特别重要。开发者现在可以期待一致的 service worker 控制，无论他们使用专用 worker 还是带有 blob URL 的共享 worker。

#### References
- [Tracking bug #324939068](https://issues.chromium.org/issues/324939068)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5137897664806912)
- [Spec](https://w3c.github.io/ServiceWorker/#control-and-use-worker-client)

### Add `ServiceWorkerStaticRouterTimingInfo`

#### What's New
Chrome 现在通过 Navigation Timing API 和 Resource Timing API 公开 ServiceWorker Static routing API 的时序信息，为开发者提供路由性能的可见性。

#### Technical Details
此功能为 Static routing API 添加了两个关键时序测量：路由决策制定时的时序标记，以及帮助开发者理解静态路由对其应用程序性能影响的性能指标。时序信息与现有的 web 性能 API 集成，使其可通过标准性能测量工具访问。

#### Use Cases
开发者现在可以通过分析时序数据来监控和优化他们的 ServiceWorker 静态路由配置。这对具有复杂路由逻辑的 PWA 特别有价值，允许团队识别其 service worker 路由决策中的性能瓶颈并相应优化。时序数据有助于量化静态路由相对于传统 service worker 拦截的性能优势。

#### References
- [Tracking bug #41496865](https://issues.chromium.org/issues/41496865)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6309742380318720)
- [Spec](https://github.com/w3c/ServiceWorker)