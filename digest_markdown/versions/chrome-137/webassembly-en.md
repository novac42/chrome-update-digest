---
layout: default
title: webassembly-en
---

## Area Summary

Chrome 137 stable introduces two focused WebAssembly updates: JavaScript Promise Integration (JSPI) and Branch Hints. JSPI improves interoperability between WebAssembly modules and JavaScript Promises, enabling cleaner async patterns where WASM can produce and consume Promise-based results. Branch Hints offer a low-level performance boost by telling the engine which branch paths are likely, improving code layout and register allocation. Together these changes advance asynchrony and runtime performance for WASM workloads, making browser-based native-code modules easier to integrate and faster in practice.

## Detailed Updates

The items below expand on the summary above and list the changes that matter to developers building with WebAssembly.

### JavaScript promise integration

#### What's New
JavaScript Promise Integration (JSPI) is an API that allows WebAssembly applications to integrate with JavaScript Promises. It allows a WebAssembly program to act as the generator of a Promise, and it allows the WebAssembly program to interact with Promise-bearing APIs.

#### Technical Details
The feature exposes an API surface enabling WASM modules to create and manage Promises and to interoperate with existing JS Promise-based APIs. See the spec and ChromeStatus entry for authoritative behavior and deployment status.

#### Use Cases
- Allow WASM modules to produce async results as native JS Promises.
- Simplify integration of WASM with JS libraries that return Promises.
- Enable clearer async control flow when combining JS and WASM logic.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5059306691878912
- Spec: https://github.com/WebAssembly/js-promise-integration

### Branch Hints

#### What's New
Branch Hints improves the performance of compiled WebAssembly code by informing the engine that a particular branch instruction is very likely to take a specific path, enabling better code layout and register allocation.

#### Technical Details
The hinting mechanism provides metadata to the engine about branch likelihoods so the compiler can optimize instruction placement (improving instruction-cache locality) and register allocation decisions during code generation.

#### Use Cases
- Performance-sensitive WASM modules where predictable branches occur (hot loops, state machines).
- Native-code workloads compiled to WASM that benefit from improved instruction-cache behavior and reduced register pressure.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5089072889290752
- Spec: https://github.com/WebAssembly/branch-hinting
