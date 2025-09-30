---
layout: default
title: javascript-zh
---

## 区域摘要

Chrome 137 稳定版引入了 JavaScript Promise Integration (JSPI)，重点在于加强 WebAssembly 与 JavaScript Promises 之间的互操作性。主要目标是使 WebAssembly 模块能直接参与 JavaScript 的异步模型，作为 Promise 的生成者并与返回 Promise 的 API 交互。此变更对混合使用 Wasm 和 JS 的开发者影响显著，简化了集成模式并澄清了跨语言的异步流程。它通过在 ECMAScript Promises 与 WebAssembly 执行上下文之间形式化一座桥梁，推动了 Web 平台的发展。

## 详细更新

下面列出实现上述摘要的具体更新。

### JavaScript promise integration（JavaScript Promise 集成）

#### 新增内容
JavaScript Promise Integration (JSPI) 是一组 API，允许 WebAssembly 应用与 JavaScript Promises 集成。它使得 WebAssembly 程序可以作为 Promise 的生成者，并与返回 Promise 的 API 交互。

#### 技术细节
该功能以 API 规范的形式定义，桥接 WebAssembly 与 JavaScript Promise 的语义。它规定了 Wasm 程序如何创建/驱动 Promises 并与现有返回 Promise 的 JavaScript API 互操作。（详见链接的规范以获取权威细节。）

#### 适用场景
- 需要发起或返回 JavaScript Promises 的 WebAssembly 模块。  
- 基于 Wasm 的代码在不使用复杂粘合代码的情况下调用现有的异步 JavaScript API。  
- 在混合使用 Wasm 与 JS 组件的应用中实现更清晰的异步控制流。  

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5059306691878912  
- 规范: https://github.com/WebAssembly/js-promise-integration
