---
layout: default
title: javascript-en
---

### 1. Area Summary

Chrome 137’s JavaScript-area change centers on closer integration between WebAssembly and JavaScript Promises. The single, high-impact feature (JavaScript Promise Integration) enables WebAssembly modules to generate and interact with Promise-based APIs, reducing impedance between WASM and async JavaScript. This advances the platform by making async interoperability more explicit and easier to implement, improving developer ergonomics for hybrid WASM/JS apps. These updates matter because they simplify common async patterns and broaden possible architectures for performant web applications.

## Detailed Updates

Below are the detailed notes for the JavaScript-area change called out above; these expand on the summary and show practical implications for developers.

### JavaScript promise integration

#### What's New
JavaScript Promise Integration (JSPI) is an API that allows WebAssembly applications to integrate with JavaScript Promises. It allows a WebAssembly program to act as the generator of a Promise, and it allows the WebAssembly program to interact with Promise-bearing APIs.

#### Technical Details
- JSPI exposes an API surface so a WebAssembly module can create and resolve/reject Promises and consume Promise-returning JavaScript APIs.
- Primary tags for this feature are webassembly and javascript, indicating cross-cutting changes in the WASM–JS boundary.
- Further technical specification and tracking are available in the linked spec and ChromeStatus entry.

#### Use Cases
- WebAssembly modules that need to initiate async workflows (e.g., I/O, network) can create Promises directly and interoperate naturally with JS code.
- Libraries that bridge heavy compute in WASM with async browser APIs (fetch, streams, custom async APIs) can simplify glue code and avoid ad-hoc callback patterns.
- Enables clearer async control flow and error propagation between WASM and JS layers.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5059306691878912
- Spec: https://github.com/WebAssembly/js-promise-integration
