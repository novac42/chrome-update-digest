---
layout: default
title: chrome-137-en
---

## Area Summary

Chrome 137 advances WebAssembly in two complementary directions: better JavaScript interoperability and runtime code-quality hints. The JavaScript Promise Integration feature enables Wasm modules to directly generate and interact with JavaScript Promises, improving async interop. Branch Hints provide the engine with branch-likelihood information to improve code layout and register allocation for compiled Wasm, targeting runtime performance. Together these updates help developers write more interoperable and performant Wasm applications on the web platform.

## Detailed Updates

Below are the WebAssembly-area updates for Chrome 137 that follow from the summary above.

### JavaScript promise integration

#### What's New
JavaScript Promise Integration (JSPI) is an API that allows WebAssembly applications to integrate with JavaScript Promises. It allows a WebAssembly program to act as the generator of a Promise, and it allows the WebAssembly program to interact with Promise-bearing APIs.

#### Technical Details
JSPI exposes an API surface so that a Wasm program can create and manipulate JavaScript Promise objects and participate in Promise-based control flow from within WebAssembly code.

#### Use Cases
Enables Wasm modules to directly produce Promises, consume Promise-returning APIs, and better interoperate with async JavaScript code paths.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5059306691878912)  
- [Spec](https://github.com/WebAssembly/js-promise-integration)

### Branch Hints

#### What's New
Branch Hints improve the performance of compiled WebAssembly code by informing the engine that a particular branch instruction is very likely to take a specific path. This allows the engine to make better decisions for code layout (improving instruction cache hits) and register allocation.

#### Technical Details
The feature supplies branch-likelihood metadata to the engine so the compiler/runtime can adjust code layout and register assignment strategies based on expected branch behavior.

#### Use Cases
Useful for performance-sensitive Wasm code where branch predictability affects instruction-cache locality and register usage, enabling more efficient compiled output.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5089072889290752)  
- [Spec](https://github.com/WebAssembly/branch-hinting)
