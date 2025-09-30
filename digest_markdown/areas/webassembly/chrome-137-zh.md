---
layout: default
title: chrome-137-zh
---

## 领域摘要

Chrome 137 通过两个有针对性的更新推进 WebAssembly：JavaScript Promise Integration 和 Branch Hints。JavaScript Promise Integration (JSPI) 允许 WebAssembly 代码充当 Promise 的生成者并与返回 Promise 的 JavaScript API 互操作，从而改进异步互操作模式。Branch Hints 向引擎提供运行时提示以优化代码布局和寄存器分配，提高已编译 WASM 代码的指令缓存效率。二者共同改善了异步工作流的开发体验和 Web 平台上 WebAssembly 模块的底层性能。

## 详细更新

下面的条目扩展了摘要并强调面向开发者的影响。

### JavaScript promise integration (JavaScript Promise 集成)

#### 新增内容
JavaScript Promise Integration (JSPI) 是一组 API，允许 WebAssembly 应用与 JavaScript 的 Promise 集成。它允许 WebAssembly 程序充当 Promise 的生成者，并使 WebAssembly 程序能够与返回 Promise 的 API 交互。特别是，当一个 applic...

#### 技术细节
JSPI 暴露了一套集成界面，使 WebAssembly 代码能够创建和驱动 Promises 并使用基于 Promise 的 JavaScript API，从而在 WASM 和 JS 运行时之间实现更紧密的异步互操作性。

#### 适用场景
使 WebAssembly 模块能够直接参与 JavaScript 的异步流程（例如返回 Promises、等待 JS Promise API），从而简化原生风格 WASM 代码与由 JS 驱动的异步逻辑之间的桥接。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5059306691878912
- 规范: https://github.com/WebAssembly/js-promise-integration

### Branch Hints (分支提示)

#### 新增内容
通过告知引擎某个分支指令很可能走特定路径，从而提升已编译 WebAssembly 代码的性能。这使得引擎能够为代码布局（提高指令缓存命中率）和寄存器分配做出更优决定。

#### 技术细节
分支提示将可能的分支方向传达给引擎，以便编译器和代码布局阶段偏好热路径，从而影响生成机器码的指令缓存局部性和寄存器分配。

#### 适用场景
对于对性能敏感的 WebAssembly 模块很有用，尤其当分支预测和代码布局影响热路径执行时，可在指令缓存利用率和执行吞吐量上获得可测量的改进。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5089072889290752
- 规范: https://github.com/WebAssembly/branch-hinting

保存到: digest_markdown/webplatform/WebAssembly/chrome-137-stable-en.md
