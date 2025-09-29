Area 概要

Chrome 137 引入了 JavaScript Promise Integration (JSPI)，使 WebAssembly 与 JavaScript Promises 之间的互操作性更紧密。最重要的变化是 WebAssembly 模块现在可以作为 Promise 的生成者，并直接与返回 Promise 的 API 交互。此项进展通过减少同步 WebAssembly 代码与 JavaScript 异步模式之间的阻抗，简化了将异步 API 集成到由 WASM 驱动的逻辑中，从而推进了 Web 平台。该更新的重要性在于它简化了异步工作流，并使 WebAssembly 在基于 JavaScript 的应用架构中成为更为一等的参与者。

## Detailed Updates

The single JavaScript-area feature in this release focuses on bridging WebAssembly and JavaScript Promises. Below is a concise, developer-focused breakdown.

### JavaScript promise integration (JavaScript Promise 集成)

#### What's New
JavaScript Promise Integration (JSPI) is an API that allows WebAssembly applications to integrate with JavaScript Promises. It allows a WebAssembly program to act as the generator of a Promise, and it allows the WebAssembly program to interact with Promise-bearing APIs.

#### Technical Details
- JSPI exposes an interface for WebAssembly modules to create and resolve/reject JavaScript Promises and to consume APIs that return Promises.
- See the specification and ChromeStatus entry for the canonical technical references (links below).

#### Use Cases
- WebAssembly modules that need to drive asynchronous workflows (e.g., I/O, network requests, or async platform APIs) can now create and manage Promises natively.
- Better interop when embedding WASM into JavaScript applications that rely on Promise-based patterns, simplifying glue code and callback bridging.

#### References
- https://chromestatus.com/feature/5059306691878912 (ChromeStatus.com entry)  
- https://github.com/WebAssembly/js-promise-integration (Spec)

Area-Specific Expertise (JavaScript-focused implications)

- webassembly: 直接使 WASM 模块能够通过生成和交互 Promise 来参与 JS 的异步控制流。
- javascript: 需要 V8 和嵌入者对 JSPI 表面的支持，以在 WASM 执行与 JS Promise 语义之间建立映射。
- performance: 可以减少 JS 与 WASM 之间异步桥接的开销和复杂度，改善开发者体验并可能提升运行时效率。
- webapi, security-privacy, multimedia, graphics-webgpu, devices, pwa-service-worker, webassembly, deprecations: JSPI 的主要影响在于异步集成模式；有关集成和安全方面的考虑，请查阅上方的规范和 ChromeStatus 链接。