## Area Summary

Chrome 133 advances WebAssembly support by landing the Memory64 proposal, which extends linear memories to sizes larger than $2^{32}$. The change does not introduce new instructions; instead it broadens existing memory and table instructions to accept 64‑bit indexes. For developers, this enables WebAssembly modules that require very large linear memories and reduces a previous hard limit on addressable memory. This update matures the platform for high-memory workloads and larger data‑heavy applications running in the browser.

## Detailed Updates

Below are the specific details for the Memory64 update and what it means for WebAssembly developers.

### WebAssembly Memory64

#### What's New
The Memory64 proposal adds support for linear WebAssembly memories with sizes larger than $2^{32}$. There are no new instructions; existing memory and table instructions are extended to allow 64‑bit indexes.

#### Technical Details
- Existing WebAssembly memory and table operations are extended to accept 64‑bit indexes rather than adding new opcodes.
- The change lives in the WebAssembly proposal "memory64" and is tracked for Chrome via the referenced ChromeStatus entry.
- Relevant runtime and embedding layers (WASM runtimes, browser engines) must support 64‑bit addressing for linear memories and tables to expose this capability to modules.

#### Use Cases
- Modules that require very large linear memories (large datasets, in-memory databases, scientific/engineering workloads) can exceed the previous 32‑bit index limit.
- Scenarios that interoperate between WebAssembly and high‑memory graphics or compute pipelines may benefit from the expanded address space.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5070065734516736)
- [Spec](https://github.com/WebAssembly/memory64/blob/main/proposals/memory64/Overview.md)

File saved to: digest_markdown/webplatform/WebAssembly/chrome-133-stable-en.md