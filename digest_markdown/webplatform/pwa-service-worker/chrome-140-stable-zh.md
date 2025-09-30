## 领域摘要

Chrome 140 针对 PWA and service worker 的更新侧重于与规范的一致性以及增强可观测性。一个更改修复了 SharedWorker 的行为，使 blob 脚本 shared workers 按照 ServiceWorker spec 继承 controllers，从而关闭了一个行为差异。另一个更改通过 navigation 和 resource timing APIs 暴露静态路由的时间点，提升了开发者衡量 service worker 路由延迟的能力。两项更新共同提升了正确性，并为开发者提供更好的诊断数据以优化离线和路由性能。

## 详细更新

以下条目对摘要做了扩展，并突出面向开发者的影响。

### `SharedWorker` script inherits controller for blob script URL（blob 脚本 URL 的 SharedWorker 继承 controller）

#### 新增内容
从 blob 脚本 URL 创建的 shared workers 现在会按 ServiceWorker spec 继承 service worker controller，与之前仅限于 dedicated workers 的行为一致。

#### 技术细节
Chrome 之前的实现将 controller 继承限制为 dedicated workers；此更改使 shared worker 的 blob URL 处理与 spec 中的 control-and-use-worker-client 规则保持一致。跟踪说明中提到一个企业策略 `SharedWorkerBlobURLFixEnabled` 以供管理控制。

#### 适用场景
- 从 blob URL 派生 shared workers 的 PWA 现在将看到与 dedicated workers 相同的受控上下文语义，从而支持一致的 fetch 拦截和客户端控制行为。
- 改善了依赖 service worker 控制网络行为的多页面或多上下文架构应用的可预测性。

#### 参考资料
- https://issues.chromium.org/issues/324939068
- https://chromestatus.com/feature/5137897664806912
- https://w3c.github.io/ServiceWorker/#control-and-use-worker-client

### Add `ServiceWorkerStaticRouterTimingInfo`（添加 ServiceWorkerStaticRouterTimingInfo）

#### 新增内容
为 ServiceWorker 静态路由向 navigation timing 和 resource timing APIs 添加了时间标记，提供关键路由事件的明确时间戳。

#### 技术细节
此更改通过标准的 timing APIs 暴露了两个与静态路由 API 相关的时间点，使浏览器能够报告 service worker 静态路由决策相对于导航和资源加载生命周期发生的时间。这将 service worker 路由遥测集成到现有的 Web 性能接口中。

#### 适用场景
- 测量和分析 service worker 静态路由在导航和资源加载中引入的延迟。
- 将路由时间与渲染和网络事件关联，以优先优化并在 PWA 启动和资源获取路径中检测性能回退。
- 在性能监控和合成测试中使用时间数据以验证跨版本的路由改进。

#### 参考资料
- https://issues.chromium.org/issues/41496865
- https://chromestatus.com/feature/6309742380318720
- https://github.com/w3c/ServiceWorker

文件已保存到：digest_markdown/webplatform/PWA and service worker/chrome-140-stable-en.md