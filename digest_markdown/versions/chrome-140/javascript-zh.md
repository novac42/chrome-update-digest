---
layout: default
title: javascript-zh
---

## 领域摘要

Chrome 140 继续增强 JavaScript 的易用性和动画时序。此版本新增内建的二进制缓冲区与 base64/hex 之间的转换支持，并调整了 view transition finished promise 的时序以避免动画结束时的闪烁。这些更改减少了二进制编码/解码的样板代码，并修复了视图过渡的一个细微渲染时序问题，提升了开发者对视觉连续性的控制。两项更新通过弥补面向开发者的 API（binary handling 和 animation lifecycle）中的跨领域缺口，减少了平台级的变通做法，从而推动平台前进。

## 详细更新

上面的简要摘要对应本次发布中针对 JavaScript 的具体更改。下面每个功能块列出变更内容、与 JavaScript/运行时和浏览器集成相关的关键技术要点、实际使用场景，以及原始链接。

### `Uint8Array` to and from base64 and hex（与 base64/hex 互转）

#### 新增内容
内建能力，可在 `Uint8Array`（二进制数据）与 base64/hex 字符串编码之间互相转换，免去使用临时性辅助函数。

#### 技术细节
- 添加了将 ArrayBuffer/Uint8Array 编码为 base64 和 hex，以及将其解码回二进制的标准化方法。
- 与 ArrayBuffer 生态系统以及由规范链接的 ECMAScript-level proposal 相连通。
- 涉及将二进制数据用于存储、网络或互操作时，JavaScript 引擎与 WebAPI 边界之间的数据封送。

#### 适用场景
- 简化对接受 base64/hex 的 API（例如 data URI、JSON 有效负载）的客户端序列化。
- 减少 web 应用、service worker 和类似 Node 的工具中对手动循环或全局辅助函数的依赖。
- 对此前使用非标准辅助函数或中间字符串的性能敏感代码路径有利。

#### 参考资料
- [ChromeStatus.com entry](https://chromestatus.com/feature/6281131254874112)
- [Link](https://tc39.es/proposal-arraybuffer-base64/spec)

### View transition finished promise timing change（finished promise 时序更改）

#### 新增内容
调整了 view transition finished promise 的时序，使得 promise 在解析时不在移除视图过渡的最后一帧之后运行，从而防止动画结束时由脚本引起的闪烁。

#### 技术细节
- 之前，finished promise 的解析发生在渲染生命周期的步骤内，解析回调可能在移除过渡的视觉帧生成之后执行。
- 此次时序变更将 promise 的解析移动到避免在该最终移除帧之后运行开发者脚本的位置，使脚本执行与视觉连续性对齐。
- 影响暴露给 JavaScript 的动画生命周期语义，并与帧生成和渲染管线中的任务调度相互作用。

#### 适用场景
- 防止在过渡后期的 promise 处理程序操作布局或执行 DOM 更改时出现闪烁。
- 使依赖 promise 回调来完成状态或触发后续动画的复杂 UI 的视图过渡更可预测。
- 对于需要尽量减少末帧脚本工作的性能敏感页面有帮助，从而保持流畅性。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/430018991)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5143135809961984)
