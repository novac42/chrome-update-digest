## Area Summary

Chrome 137's JavaScript-area update centers on JavaScript Promise Integration (JSPI), a bridge between WebAssembly and JavaScript Promises. The most impactful change lets WebAssembly modules both generate Promises and interact directly with Promise-bearing APIs, simplifying async interoperability. This advances the platform by reducing glue code and enabling cleaner async patterns across the JS/WASM boundary. These updates matter for teams building performance-sensitive or compute-heavy modules in WebAssembly that need to participate in JavaScript's async ecosystem.

## Detailed Updates

Below are the JavaScript-area changes relevant to developers working with WebAssembly and async JavaScript.

### JavaScript promise integration

#### What's New
JavaScript Promise Integration (JSPI) is an API that allows WebAssembly applications to integrate with JavaScript Promises. It allows a WebAssembly program to act as the generator of a Promise, and it allows the WebAssembly program to interact with Promise-bearing APIs.

#### Technical Details
- Enables WebAssembly code to produce and consume JavaScript Promises, formalizing async interop across the WASM/JS boundary.
- Primary tags associated with the feature: webassembly, javascript.

#### Use Cases
- WebAssembly modules that need to expose async operations to JavaScript consumers as Promises.
- WASM code that must call into JavaScript async APIs and handle Promise results without heavy JS wrapper layers.
- Cleaner async control flow in mixed JS + WASM applications (e.g., compute tasks returning Promise-based results).

#### References
- https://chromestatus.com/feature/5059306691878912
- https://github.com/WebAssembly/js-promise-integration

## Area-Specific Expertise (JavaScript-focused)

- javascript / webassembly: Direct relevance — JSPI targets WASM↔JS async integration.
- webapi: Impacts how WASM interacts with promise-bearing browser APIs.
- performance: Reduces JS glue and can improve async call paths for compute-heavy WASM modules.
- pwa-service-worker: Enables WASM to participate in Promise-based service-worker flows (fetch, caching) more directly.
- deprecations: N/A for this feature; focus is additive interoperability.