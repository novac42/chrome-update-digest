---
layout: default
title: webassembly-en
---

## Area Summary

Chrome 137 advances WebAssembly with two targeted updates: JavaScript Promise Integration and Branch Hints. JavaScript Promise Integration (JSPI) lets WebAssembly code play the role of Promise generators and interoperate with Promise-bearing JavaScript APIs, improving async interop patterns. Branch Hints provide runtime hints to the engine to optimize code layout and register allocation, boosting instruction-cache efficiency for compiled WASM code. Together these changes improve both developer ergonomics for async workflows and low-level performance of WebAssembly modules on the web platform.

## Detailed Updates

The items below expand on the summary and highlight developer-facing implications.

### JavaScript promise integration

#### What's New
JavaScript Promise Integration (JSPI) is an API that allows WebAssembly applications to integrate with JavaScript Promises. It allows a WebAssembly program to act as the generator of a Promise, and it allows the WebAssembly program to interact with Promise-bearing APIs. In particular, when an applic...

#### Technical Details
JSPI exposes an integration surface so that WebAssembly code can create and drive Promises and consume Promise-based JavaScript APIs, enabling tighter async interoperability between WASM and JS runtimes.

#### Use Cases
Enables WebAssembly modules to participate directly in JavaScript async flows (e.g., returning Promises, awaiting JS Promise APIs) which simplifies bridging between native-style WASM code and JS-driven async logic.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5059306691878912
- Spec: https://github.com/WebAssembly/js-promise-integration

### Branch Hints

#### What's New
Improves the performance of compiled WebAssembly code by informing the engine that a particular branch instruction is very likely to take a specific path. This allows the engine to make better decisions for code layout (improving instruction cache hits) and register allocation.

#### Technical Details
Branch hints convey likely-branch direction to the engine so the compiler and code layout stages can favor the hot path, impacting instruction cache locality and register assignment in generated machine code.

#### Use Cases
Useful for performance-sensitive WebAssembly modules where branch prediction and code layout influence hot-path execution, yielding measurable improvements in instruction-cache utilization and execution throughput.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5089072889290752
- Spec: https://github.com/WebAssembly/branch-hinting

Save to: digest_markdown/webplatform/WebAssembly/chrome-137-stable-en.md
