# 领域摘要

Chrome 138 引入了对 speculation-rules prefetch 的 ServiceWorker 支持，允许对由 ServiceWorker 控制的目标进行预取。对开发者影响最大的一点是，当检测到控制的 ServiceWorker 时，不再取消预取，从而改善了针对 SW 控制站点的缓存预热和导航响应性。此更改通过使导航预测与 ServiceWorker 控制对齐，推动了 Web 平台的发展，使离线优先和性能优化更加可靠。这些更新很重要，因为它们减少了无谓的工作并提高了 PWA 预取策略的有效性。

## 详细更新

上面的简要摘要概述了此版本中的单一更改；以下为详细信息和对开发者的影响。

### ServiceWorker support for Speculation Rules Prefetch（对 ServiceWorker 控制目标的预取支持）

#### 新增内容
允许对由 ServiceWorker 控制的 URL 执行 speculation-rules 预取，而不是在检测到控制的 ServiceWorker 时取消这些预取。

#### 技术细节
通过 Nav Speculation 规则与 ServiceWorker 控制的集成，现在允许由 ServiceWorker 控制的预取。此前，浏览器在检测到控制的 ServiceWorker 时会取消一个 speculation 预取，阻止该预取填充由 ServiceWorker 控制的 fetch 路径。更改后，预取可以继续进行，并在适用时由 ServiceWorker 提供/处理。

#### 适用场景
- 使用 ServiceWorker 进行离线缓存的 PWA 可以通过 speculation 规则在导航前预热 SW 缓存，从而改善感知加载时间。
- 使用导航预测来预取可能导航的站点，在存在 ServiceWorker 时将减少无谓工作并提高缓存命中率。
- 开发者可以将 speculation-rules 作为端到端性能策略的一部分，结合 SW 路由和缓存共同使用。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40947546 (跟踪 bug #40947546)  
- https://chromestatus.com/feature/5121066433150976 (ChromeStatus.com 条目)  
- https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-sw-integration (规范)

# 领域专门知识（PWA 与 ServiceWorker 关注点）

- css: 预取与 SW 的交互可以通过确保关键 CSS 从 SW 缓存提供来提高初始渲染速度。
- webapi: 当 speculation 预取针对由 SW 控制的作用域时，此更改会影响 fetch 流程和 fetch 事件生命周期。
- graphics-webgpu: 降低的导航延迟可通过更早的资源可用性改善 GPU 密集型页面的首帧时间。
- javascript: ServiceWorker 脚本生命周期和 fetch 处理器应考虑由预取发起的请求，并以幂等方式处理。
- security-privacy: 开发者必须确保预取处理符合 CORS、凭证和与 SW fetch 语义一致的隐私约束。
- performance: 使缓存预热策略更有效，减少导航停滞并改善感知性能。
- multimedia: 通过由 SW 控制的作用域预取媒体资源可以平滑 PWA 的播放启动。
- devices: 更快的导航在 PWA 预取硬件访问所需资源时有助于设备 API 的初始化。
- pwa-service-worker: 通过允许 SW 提供 speculation 预取，直接改进离线优先和后台资源预热策略。
- webassembly: 可以将 WASM 模块预取到 SW 缓存中，以加速计算密集型页面的启动。
- 弃用: 此更改没有弃用；评估现有预取策略以在适用时利用 SW 集成。