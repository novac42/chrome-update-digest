---
layout: default
title: chrome-137-zh
---

### 1. 领域摘要

Chrome 137 在 JavaScript 领域的更改集中在 WebAssembly 与 JavaScript Promises 之间的更紧密集成。单一且高影响力的特性 (JavaScript Promise Integration) 使 WebAssembly 模块能够生成并与基于 Promise 的 API 交互，从而降低 WASM 与异步 JavaScript 之间的阻抗。这推动了平台发展，使异步互操作性更明确且更易实现，改善了混合 WASM/JS 应用的开发人员使用体验。这些更新的重要性在于它们简化了常见的异步模式并扩大了面向高性能 Web 应用的可能架构。

## 详细更新

以下是上文所述 JavaScript 领域更改的详细说明；这些内容扩展了摘要并展示了对开发者的实际影响。

### JavaScript promise integration（JavaScript Promise 集成）

#### 新增内容
JavaScript Promise Integration (JSPI) 是一个 API，允许 WebAssembly 应用与 JavaScript Promises 集成。它允许 WebAssembly 程序作为 Promise 的生成者，并且允许该程序与返回 Promise 的 API 交互。

#### 技术细节
- JSPI 暴露了一组 API，使 WebAssembly 模块可以创建并 resolve/reject Promise，并消费返回 Promise 的 JavaScript API。
- 此特性的主要标签为 webassembly 和 javascript，表明在 WASM–JS 边界存在跨切改变。
- 在链接的规范和 ChromeStatus 条目中可以查看进一步的技术规范和跟踪信息。

#### 适用场景
- 需要启动异步工作流（例如 I/O、网络）的 WebAssembly 模块可以直接创建 Promise，并与 JS 代码自然互操作。
- 把在 WASM 中的重计算与浏览器的异步 API（fetch、streams、自定义异步 API）桥接的库，可以简化粘合代码并避免临时的回调模式。
- 使 WASM 与 JS 层之间的异步控制流和错误传播更清晰。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5059306691878912
- 规范: https://github.com/WebAssembly/js-promise-integration
