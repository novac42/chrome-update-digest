## Area Summary

Chrome 137 引入了两个针对 WebAssembly 的更新：JavaScript Promise Integration (JSPI) 和 Branch Hints。JSPI 通过允许 WebAssembly 模块生成并与 JavaScript Promise 交互，加强了异步互操作性，从而改善与返回 Promise 的 API 的集成。Branch Hints 向引擎提供显式的分支概率信息，以优化代码布局、指令缓存局部性和寄存器分配，从而带来运行时性能提升。两者结合推进了平台，改善了异步互操作性并降低了对性能敏感的 Wasm 代码的运行时开销。

## Detailed Updates

The items below expand on the summary above and highlight developer-facing implications.

### JavaScript promise integration (JavaScript Promise 集成)

#### What's New
JavaScript Promise Integration (JSPI) is an API that allows WebAssembly applications to integrate with JavaScript Promises. It allows a WebAssembly program to act as the generator of a Promise, and it allows the WebAssembly program to interact with Promise-bearing APIs.

#### Technical Details
Enables WebAssembly modules to participate directly in the JS Promise model by creating and interacting with promise objects from Wasm code, bridging synchronous Wasm execution and async JS APIs.

#### Use Cases
- Better interop for async workflows where Wasm must initiate or consume promise-based APIs.
- Cleaner integration of Wasm libraries with JS ecosystems that rely on Promises (networking, async I/O, sequencing).

#### References
- https://chromestatus.com/feature/5059306691878912 (ChromeStatus.com entry)  
- https://github.com/WebAssembly/js-promise-integration (Spec)

### Branch Hints (分支提示)

#### What's New
Branch Hints improves the performance of compiled WebAssembly code by informing the engine that a particular branch instruction is very likely to take a specific path. This allows the engine to make better decisions for code layout (improving instruction cache hits) and register allocation.

#### Technical Details
Hint metadata attached to branch instructions biases the engine’s compilation and layout heuristics so hot paths are arranged to improve cache locality and register usage, reducing misprediction and layout-induced overhead.

#### Use Cases
- Performance-sensitive Wasm modules (hot loops, compute kernels, game logic) where explicit branch-probability guidance reduces runtime stalls.
- Optimizing compiled code layout for instruction-cache and register-pressure improvements without changing source logic.

#### References
- https://chromestatus.com/feature/5089072889290752 (ChromeStatus.com entry)  
- https://github.com/WebAssembly/branch-hinting (Spec)

已保存到: digest_markdown/webplatform/WebAssembly/chrome-137-stable-en.md