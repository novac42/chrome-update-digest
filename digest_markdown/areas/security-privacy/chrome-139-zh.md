---
layout: default
title: chrome-139-zh
---

## Area Summary

Chrome 139 在 worker 创建时加强了与 CSP 的集成，遵循 CSP3 规范：在 fetch 期间检查 CSP，当 CSP 阻止 worker 时，会触发异步 error 事件，而不是在调用 new Worker/new SharedWorker 时抛出异常。此更改影响开发者检测和处理 worker 加载失败的方式，并改进了符合规范的可预测失败语义。通过将 Chrome 与 W3C 的 CSP fetch-integration 行为对齐，推动了 Web 平台的互操作性，便于更一致的跨浏览器错误处理。团队应更新依赖于 new Worker/new SharedWorker 周围同步异常的逻辑，并添加健壮的错误事件处理和遥测。

## Detailed Updates

The single Security-Privacy change in this release refines worker failure semantics under Content Security Policy and is directly relevant to error handling, CSP reporting, and secure script loading patterns.

### Fire error event for Content Security Policy (CSP) blocked worker

#### What's New
Chrome now checks CSP during fetch and, when a worker script is blocked by CSP, fires an asynchronous error event instead of throwing an exception during the call to new Worker(url) or new SharedWorker(url).

#### Technical Details
- CSP evaluation occurs during the fetch for worker scripts per the CSP3 fetch-integration spec.
- When CSP blocks the fetch, the browser does not throw synchronously; it emits an error event on the Worker/SharedWorker object asynchronously.
- This behavior aligns Chrome with the W3C spec and changes observable control flow for worker creation failures.

#### Use Cases
- Update code that wraps new Worker(...) in try/catch to instead attach error listeners (worker.addEventListener('error', ...)) to reliably detect CSP blocks.
- Improve telemetry and CSP reporting by listening for worker error events and logging or reporting CSP-related failures.
- Libraries and frameworks that spawn workers should ensure they register error handlers before or immediately after worker creation to avoid missed failures.

#### References
- Tracking bug #41285169: https://issues.chromium.org/issues/41285169
- ChromeStatus.com entry: https://chromestatus.com/feature/5177205656911872
- Spec: https://www.w3.org/TR/CSP3/#fetch-integration

## Area-Specific Expertise (Security-Privacy focused guidance)

- css: 直接影响最小；影响内联样式或 `script-src` 的 CSP 仍然相关——确保 style/script 的 CSP 与 worker 脚本来源一致。
- webapi: Worker/SharedWorker 创建语义已更改——应依赖基于事件的失败信号，而不是同步异常。
- graphics-webgpu: 在 worker 中托管并加载模块的 GPU 工作应处理由 CSP 阻止引发的异步 worker error 事件。
- javascript: 不要依赖围绕 new Worker/new SharedWorker 的 try/catch 来处理 CSP 失败；应附加 `'error'` 处理器，并在需要时通过基于 Promise 的 API 传播错误。
- security-privacy: 将运行时强制与 CSP3 对齐；提高了可观测性并一致地执行跨域/脚本源限制。
- performance: 失败时机有轻微差异（异步 vs 同步）——确保启动流程能容忍延迟的失败回调。
- multimedia: 基于 worker 的媒体处理必须通过事件处理 worker 加载错误以实现优雅降级。
- devices: 在 worker 中访问硬件的代码应通过 error 事件验证 worker 可用性，然后再假定相关能力可用。
- pwa-service-worker: ServiceWorker API 本身不受此特性影响；但 PWA 使用的其他 worker 类型必须处理 CSP 阻止事件。
- webassembly: 通过 worker 加载 Wasm 模块时，CSP 阻止将通过 error 事件暴露；添加处理器以呈现模块加载失败。
- 弃用: 此处无弃用，但依赖同步异常的代码应迁移到新的基于事件的错误处理方式。

Save to: digest_markdown/webplatform/Security-Privacy/chrome-139-stable-en.md
