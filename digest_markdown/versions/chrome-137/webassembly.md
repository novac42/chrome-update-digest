---
layout: default
title: webassembly
---

## WebAssembly

### JavaScript promise integration

JavaScript Promise Integration (JSPI) is an API that allows WebAssembly applications to integrate with JavaScript Promises. It allows a WebAssembly program to act as the generator of a Promise, and it allows the WebAssembly program to interact with Promise-bearing APIs. In particular, when an application uses JSPI to call a Promise-bearing (JavaScript) API, the WebAssembly code is suspended; and the original caller to the WebAssembly program is given a Promise that will be fulfilled when the WebAssembly program finally completes.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5059306691878912) | [Spec](https://github.com/WebAssembly/js-promise-integration)

### Branch Hints

Improves the performance of compiled WebAssembly code by informing the engine that a particular branch instruction is very likely to take a specific path. This allows the engine to make better decisions for code layout (improving instruction cache hits) and register allocation.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5089072889290752) | [Spec](https://github.com/WebAssembly/branch-hinting)
