## 区域摘要

Chrome 140 (stable) 在 PWA 和 service worker 领域引入了两项重点更新：一个使 shared workers 从 blob 脚本 URL 继承 controller 的规范对齐修复，另一个为 ServiceWorker Static routing API 添加了计时遥测。SharedWorker 修复将运行时行为更改为与 ServiceWorker 规范一致，并由一个企业策略进行控制。计时添加在导航/资源计时中公开了与路由相关的标记，提升了开发者的可观测性。两者共同提升了平台一致性以及开发者测量和分析 service-worker 控制的导航与路由的能力。

## 详细更新

下面条目扩展了上文摘要，并展示了对 PWA 与 service-worker 开发的实际影响。

### `SharedWorker` script inherits controller for blob script URL（SharedWorker 对 blob 脚本 URL 继承 controller）

#### 新增内容
Chrome 现在与 ServiceWorker 规范对齐，允许由 blob 脚本 URL 创建的 shared workers 继承 controller，这与此前仅限于 dedicated workers 的行为一致。

#### 技术细节
此更改修复了 Chrome 先前在 blob URL 情形下只有 dedicated workers 会继承 controller 的偏差。发布说明中提到一个名为 SharedWorkerBlobURLFixEnabled 的企业策略用于控制该行为的推出。

#### 适用场景
- 确保依赖 controller 存在的代码路径（例如拦截 fetch 或消息流）在 dedicated workers 和 shared workers 之间具有一致的 controller 语义。
- 减少浏览器行为与规范之间的差异，简化跨浏览器 PWA 逻辑和调试。

#### 参考资料
- https://issues.chromium.org/issues/324939068
- https://chromestatus.com/feature/5137897664806912
- https://w3c.github.io/ServiceWorker/#control-and-use-worker-client

### Add `ServiceWorkerStaticRouterTimingInfo`（添加静态路由计时信息）

#### 新增内容
Chrome 为 ServiceWorker Static routing API 添加了相关的计时信息，并通过导航计时 API 和资源计时 API 将其暴露给开发者使用。

#### 技术细节
ServiceWorker 提供用于表示路由相关时间点的标记；此功能将两个与 Static routing API 相关的计时值暴露到平台计时 API 中，以便测量和诊断。

#### 适用场景
- 支持精确测量路由决策及其对导航性能的影响。
- 帮助开发者和性能工程师将 service-worker 路由活动与导航/资源计时数据相关联，以进行优化和调试。

#### 参考资料
- https://issues.chromium.org/issues/41496865
- https://chromestatus.com/feature/6309742380318720
- https://github.com/w3c/ServiceWorker

File: digest_markdown/webplatform/PWA and service worker/chrome-140-stable-en.md