---
layout: default
title: javascript-zh
---

## Area Summary

Chrome 137 的 JavaScript 领域更新聚焦于 JavaScript Promise Integration (JSPI)，这是一个在 WebAssembly 与 JavaScript Promise 之间搭建桥梁的能力。最重要的更改允许 WebAssembly 模块既能生成 Promise，又能直接与带有 Promise 的 API 交互，从而简化异步互操作性。此举通过减少粘合代码并在 JS/WASM 边界处实现更清晰的异步模式，推动平台发展。对于构建性能敏感或计算密集型的 WebAssembly 模块并需要参与 JavaScript 异步生态的团队，这些更新具有重要意义。

## Detailed Updates

Below are the JavaScript-area changes relevant to developers working with WebAssembly and async JavaScript.

### JavaScript promise integration (JavaScript Promise 集成)

#### What's New
JavaScript Promise Integration (JSPI) 是一组 API，允许 WebAssembly 应用与 JavaScript Promise 集成。它使 WebAssembly 程序可以作为 Promise 的生成者，并允许该程序与带有 Promise 的 API 交互。

#### Technical Details
- Enables WebAssembly code to produce and consume JavaScript Promises, formalizing async interop across the WASM/JS boundary.
- Primary tags associated with the feature: webassembly, javascript.

#### Use Cases
- WebAssembly modules that need to expose async operations to JavaScript consumers as Promises.
- WASM code that must call into JavaScript async APIs and handle Promise results without heavy JS wrapper layers.
- Cleaner async control flow in mixed JS + WASM applications (e.g., compute tasks returning Promise-based results).

#### References
- https://chromestatus.com/feature/5059306691878912
- https://github.com/WebAssembly/js-promise-integration

## Area-Specific Expertise (JavaScript-focused)

- javascript / webassembly: 直接相关 — JSPI 针对 WASM↔JS 的异步互操作性。
- webapi: 影响 WASM 如何与 promise-bearing 浏览器 API 交互。
- performance: 减少 JS glue 并能改善计算密集型 WASM 模块的异步调用路径。
- pwa-service-worker: 使 WASM 更直接参与基于 Promise 的 service-worker 流程（fetch、caching）。
- 弃用: 本功能无相关项；关注点为增加性的互操作性。
