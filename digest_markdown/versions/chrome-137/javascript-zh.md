---
layout: default
title: javascript-zh
---

## 领域摘要

Chrome 137 引入了 JavaScript Promise Integration (JSPI)，这是一个专注的增强，用于桥接 WebAssembly 与 JavaScript 的异步模型。关键更改允许 WebAssembly 模块作为 JavaScript Promise 的生成器，并直接与携带 Promise 的 API 交互。这减少了在 WASM 与 Web 平台之间实现真实异步互操作时的摩擦，使 WASM 代码能实现更原生的异步工作流。对于开发者而言，它简化了 JS 与 WASM 之间的连接，并为将异步逻辑迁移到 WebAssembly 提供了更清晰的路径。

## 详细更新

下面的单个更新直接来源于摘要，并强调面向开发者的影响。

### JavaScript promise integration（JavaScript Promise 集成）

#### 新增内容
JavaScript Promise Integration (JSPI) 是一组 API，使 WebAssembly 应用能够与 JavaScript Promises 集成。它允许 WebAssembly 程序作为 Promise 的生成器，并与携带 Promise 的 API 进行交互。

#### 技术细节
- 使 WASM 模块能够创建和操作 JavaScript Promise 对象，并参与基于 Promise 的控制流。
- 支持双向互操作：WebAssembly 可以作为 Promise 的生成器，并可消费现有返回 Promise 的浏览器 API。
- 实现与规范工作在所提供的 spec 和 ChromeStatus 条目中跟踪。

#### 适用场景
- 需要启动异步操作并向 JS 调用者暴露基于 Promise 的 API 的 WebAssembly 模块。
- 在 WASM 中直接消费返回 Promise 的浏览器 API，而无需复杂的手写粘合代码。
- 希望在 JS 与 WASM 组件之间保持一致异步语义的库与框架作者。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5059306691878912  
- 规范: https://github.com/WebAssembly/js-promise-integration
