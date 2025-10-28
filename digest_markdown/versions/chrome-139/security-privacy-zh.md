---
layout: default
title: security-privacy-zh
---

## 领域摘要

Chrome 139 将 worker 创建行为与 CSP3 的 fetch 集成规范对齐：在 fetch 期间检查 Content Security Policy，并在被阻止时触发异步错误事件，而不是在 "new Worker(url)" 或 "new SharedWorker(url)" 时抛出同步异常。此更改减少了页面脚本中的意外异常，为开发者提供基于事件的失败处理模式以应对被 CSP 阻止的 worker 加载。对于 Web 平台安全，这提高了不同用户代理之间的一致性，并在不破坏脚本执行流程的情况下使 CSP 的强制变得可观察。开发者应更新 worker 创建的错误处理，监听错误事件而不是依赖可捕获的异常。

## 详细更新

下面这条 Security-Privacy 更新详细说明了 Chrome 如何在 CSP 下更改 worker 失败行为以及开发者应如何调整。

### Fire error event for Content Security Policy (CSP) blocked worker（当 CSP 阻止 worker 时触发错误事件）

#### 新增内容
- Chrome 现在在用于创建 Worker 和 SharedWorker 的 fetch 期间检查 Content Security Policy；当 CSP 阻止该 fetch 时，会触发一个异步 error 事件，而不是在 "new Worker(url)" 或 "new SharedWorker(url)" 构造时抛出同步异常。

#### 技术细节
- 行为更改实现了 CSP3 的 fetch 集成指导：在 worker 的 fetch 期间评估 CSP，被阻止的 fetch 会导致向 worker 对象派发一个错误事件。
- 错误以异步方式发出，保留脚本执行流程，避免在构造时抛出同步异常。
- 这使 Chrome 与规范及 Chromium 中跟踪的实现工作保持一致。

#### 适用场景
- 稳健的 worker 创建：服务作者可以在 Worker/SharedWorker 实例上附加 "error" 处理器，以检测 CSP 拒绝并实现回退策略（例如，加载替代脚本、通知用户或降级功能）。
- 错误遥测：可观察性得到改善，因为被阻止的 fetch 会发出事件，可以在不对 worker 构造使用 try/catch 的情况下记录。
- 渐进增强：单页应用和 PWA 可以避免因意外异常而中断初始化流程，而是动态处理 worker 的可用性。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/41285169)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5177205656911872)
- [Spec](https://www.w3.org/TR/CSP3/#fetch-integration)

## 面向领域的专长与开发者指南（Security-Privacy 焦点）

- security-privacy: 该更改澄清了在 worker fetch 中 CSP 的强制语义；审计代码以在 Workers 和 SharedWorkers 上附加 "error" 监听器，避免依赖构造函数异常。
- pwa-service-worker: 对于 PWAs，确保 service worker 注册和基于 worker 的功能能够处理异步失败事件，并在离线时提供回退方案。
- webapi & javascript: 更新客户端模式，使用基于事件的错误处理来管理 worker 生命周期，而不是在构造函数周围使用 try/catch；这与基于事件的 DOM APIs 保持一致。
- deprecations & performance: 此处无弃用，但在添加 error 监听器和回退逻辑时，应审查初始化路径以防止性能回退。
- Other areas (css, graphics-webgpu, multimedia, devices, webassembly): 虽然不会直接受到影响，但当 worker 使用涉及这些领域时，跨团队的知悉很有价值（例如，通过 workers 将大量计算卸载到 WebGPU 或 WASM）。
