---
layout: default
title: chrome-137-zh
---

## 领域摘要

Chrome 137 在两个互补方向上推进 WebAssembly：更好的 JavaScript 互操作性和运行时代码质量提示。JavaScript Promise Integration 功能使 Wasm 模块能够直接生成并与 JavaScript Promise 交互，从而改善异步互操作。Branch Hints 向引擎提供分支概率信息，以改进已编译 Wasm 的代码布局和寄存器分配，旨在提升运行时性能。上述更新共同帮助开发者在 Web 平台上编写更具互操作性和更高性能的 Wasm 应用。

## 详细更新

下面是基于上述摘要的 Chrome 137 的 WebAssembly 领域更新。

### JavaScript promise integration（与 JavaScript Promise 的集成）

#### 新增内容
JavaScript Promise Integration (JSPI) 是一组 API，允许 WebAssembly 应用与 JavaScript Promise 集成。它使 WebAssembly 程序能够作为 Promise 的生成者，并能与返回 Promise 的 API 交互。

#### 技术细节
JSPI 暴露了一个 API 表面，以便 Wasm 程序可以创建和操作 JavaScript Promise 对象，并从 WebAssembly 代码内部参与基于 Promise 的控制流。

#### 适用场景
使 Wasm 模块能够直接产生 Promise、调用返回 Promise 的 API，并更好地与异步 JavaScript 代码路径互操作。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5059306691878912)  
- [规范](https://github.com/WebAssembly/js-promise-integration)

### Branch Hints（分支提示）

#### 新增内容
Branch Hints 通过告知引擎某个分支指令很可能走特定路径来提升已编译 WebAssembly 代码的性能。这使引擎能为代码布局（提高指令缓存命中）和寄存器分配做出更好的决策。

#### 技术细节
该功能向引擎提供分支概率元数据，以便编译器/运行时根据预期的分支行为调整代码布局和寄存器分配策略。

#### 适用场景
适用于对性能敏感的 Wasm 代码，在这些代码中分支可预测性影响指令缓存局部性和寄存器使用，从而实现更高效的编译输出。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5089072889290752)  
- [规范](https://github.com/WebAssembly/branch-hinting)
