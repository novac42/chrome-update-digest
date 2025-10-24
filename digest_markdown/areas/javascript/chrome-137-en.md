---
layout: default
title: chrome-137-en
---

## Area Summary

Chrome 137 introduces JavaScript Promise Integration (JSPI), a focused enhancement that bridges WebAssembly and JavaScript async models. The key change lets WebAssembly modules act as generators of JavaScript Promises and interact directly with Promise-bearing APIs. This reduces friction for authors who need true async interop between WASM and the web platform, enabling more native-feeling async workflows in WASM code. For developers, it simplifies wiring between JS and WASM and opens clearer migration paths for async logic into WebAssembly.

## Detailed Updates

The single update below follows directly from the summary and highlights developer-facing implications.

### JavaScript promise integration

#### What's New
JavaScript Promise Integration (JSPI) is an API that enables WebAssembly applications to integrate with JavaScript Promises. It allows a WebAssembly program to act as the generator of a Promise and to interact with Promise-bearing APIs.

#### Technical Details
- Enables WASM modules to produce and manipulate JavaScript Promise objects and to participate in Promise-based control flow.
- Supports bidirectional interop: WebAssembly can be a Promise generator and can consume existing Promise-returning browser APIs.
- Implementation and specification work is tracked in the provided spec and ChromeStatus entry.

#### Use Cases
- WebAssembly modules that need to initiate asynchronous operations and expose Promise-based APIs to JS callers.
- Consuming Promise-returning browser APIs directly from WASM without complex hand-written glue code.
- Library and framework authors who want consistent async semantics across JS and WASM components.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5059306691878912  
- Spec: https://github.com/WebAssembly/js-promise-integration
