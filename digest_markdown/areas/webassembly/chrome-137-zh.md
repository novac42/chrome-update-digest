---
layout: default
title: chrome-137-zh
---

## Area Summary

Chrome 137 稳定版引入了两项针对 WebAssembly 的更新：JavaScript Promise Integration (JSPI) 和 Branch Hints。JSPI 改进了 WebAssembly 模块与 JavaScript Promises 之间的互操作性，使 WASM 能够生成和消费基于 Promise 的结果，从而实现更清晰的异步模式。Branch Hints 通过告知引擎哪些分支路径更可能被采用，在底层提升性能，改善代码布局和寄存器分配。二者共同推进了 WASM 工作负载的异步性和运行时性能，使基于浏览器的本机代码模块更易于集成并在实践中更快。

## Detailed Updates

The items below expand on the summary above and list the changes that matter to developers building with WebAssembly.

### JavaScript promise integration

#### What's New
JavaScript Promise Integration (JSPI) 是一组 API，允许 WebAssembly 应用与 JavaScript Promises 集成。它使 WebAssembly 程序能够作为 Promise 的生成者，并与返回 Promise 的 API 交互。

#### Technical Details
该功能暴露了一个 API 表面，使 WASM 模块能够创建和管理 Promises，并与现有基于 Promise 的 JS API 互操作。See the spec and ChromeStatus entry for authoritative behavior and deployment status.

#### Use Cases
- 允许 WASM 模块以原生 JS Promises 的形式生成异步结果。
- 简化 WASM 与返回 Promises 的 JS 库的集成。
- 在结合 JS 与 WASM 逻辑时，使异步控制流更清晰。

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5059306691878912
- Spec: https://github.com/WebAssembly/js-promise-integration

### Branch Hints

#### What's New
Branch Hints 通过告知引擎某个分支指令很可能走特定路径，从而提高已编译 WebAssembly 代码的性能，进而实现更好的代码布局和寄存器分配。

#### Technical Details
该提示机制向引擎提供有关分支可能性的元数据，使编译器在代码生成期间能够优化指令布局（改善指令缓存局部性）和寄存器分配决策。

#### Use Cases
- 针对存在可预测分支的性能敏感 WASM 模块（热循环、状态机）。
- 编译为 WASM 的本机代码工作负载，可从改善的指令缓存行为和降低寄存器压力中获益。

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5089072889290752
- Spec: https://github.com/WebAssembly/branch-hinting
