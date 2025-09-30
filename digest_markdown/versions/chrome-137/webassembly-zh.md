---
layout: default
title: webassembly-zh
---

## 区域摘要

Chrome 137 推进了 WebAssembly 的互操作性和运行时性能。本次发布增加了 JavaScript Promise Integration (JSPI)，允许 Wasm 模块直接生成和消费 JS Promises，并引入了 Branch Hints 来改进生成代码的布局和寄存器使用。两项功能共同减少了 Wasm 与现有异步 Web API 集成的摩擦，并促使执行热点使用更少的 CPU 资源并获得更好的指令缓存局部性。这些更新重要在于它们使 Wasm 成为现代 Web 应用架构中更自然的一部分，并为计算密集型工作负载带来可测量的性能提升。

## 详细更新

以下内容扩展了上文摘要，并描述了在 Chrome 137 中使用 WebAssembly 的开发者的实际影响。

### JavaScript promise integration（JavaScript Promise 集成）

#### 新增内容
WebAssembly 现在可以与 JavaScript Promises 集成：Wasm 模块可以作为 Promise 生成者，并更直接地与返回 Promise 的 API 进行交互。

#### 技术细节
JSPI 定义了一个 API 表面，将 Wasm 执行映射到 JS Promise 的生命周期操作，使 Wasm 能够在无需大量 JS 桥接的情况下 resolve、reject 和 await promises。该功能在下方链接的社区维护规范中有定义，并在 ChromeStatus 上跟踪。

#### 适用场景
- 在 Wasm 模块中实现类似原生的异步流程，并可与 Fetch、IndexedDB 等基于 Promise 的 Web API 直接互操作。
- 简化编译到 Wasm 的语言为异步代码生成的绑定（减少自定义运行时 shim）。
- 通过 Promise 的 reject 语义在 Wasm 与 JS 之间实现更清晰的错误传播。

#### 参考资料
- https://chromestatus.com/feature/5059306691878912
- https://github.com/WebAssembly/js-promise-integration

### Branch Hints（分支提示）

#### 新增内容
Branch Hints 允许开发者（通过编译工具链）告知引擎哪些分支方向更可能，从而使运行时能够优化代码布局和寄存器分配。

#### 技术细节
这些提示引导代码布局决策以改善指令缓存局部性，并允许引擎对热点路径偏好寄存器分配。该机制在 branch-hinting 规范中定义，并在 ChromeStatus 上跟踪。

#### 适用场景
- 针对性能敏感的 Wasm 代码（游戏引擎、物理、数值内核）可以标记热点分支以减少误预测和缓存未命中。
- 以 Wasm 为目标的编译器可以输出 branch hints 以保留本地构建的运行时性能特性。
- 减少部署后剖析以查找并手工优化热点路径布局的需要。

#### 参考资料
- https://chromestatus.com/feature/5089072889290752
- https://github.com/WebAssembly/branch-hinting
