## Area Summary

Chrome 137 advances WebAssembly interoperability and runtime performance. The release adds JavaScript Promise Integration (JSPI) to let Wasm modules produce and consume JS Promises directly, and introduces Branch Hints to improve generated code layout and register use. Together these features reduce friction integrating Wasm with existing async web APIs and push execution hotspots to use fewer CPU resources and better instruction-cache locality. These updates matter because they make Wasm a more natural part of modern web application architectures and enable measurable performance wins for compute-heavy workloads.

## Detailed Updates

The following details expand on the summary above and describe practical impact for developers working with WebAssembly in Chrome 137.

### JavaScript promise integration

#### What's New
WebAssembly can now integrate with JavaScript Promises: Wasm modules can act as Promise generators and interact with Promise-bearing APIs more directly.

#### Technical Details
JSPI defines an API surface that maps Wasm execution to JS Promise lifecycle operations, enabling Wasm to resolve, reject, and await promises without heavy JS glue. The feature is specified in a community-maintained spec linked below and tracked in ChromeStatus.

#### Use Cases
- Native-like async flows in Wasm modules that directly interoperate with Fetch, IndexedDB, and other promise-based web APIs.
- Simpler bindings for languages compiling to Wasm that emit async code (reduces custom runtime shims).
- Cleaner error propagation between Wasm and JS via Promise rejection semantics.

#### References
- https://chromestatus.com/feature/5059306691878912
- https://github.com/WebAssembly/js-promise-integration

### Branch Hints

#### What's New
Branch Hints let developers (via compilation toolchains) inform the engine which branch directions are very likely, enabling the runtime to optimize code layout and register allocation.

#### Technical Details
Hints guide code layout decisions to improve instruction-cache locality and allow the engine to favor register allocations for hot paths. The mechanism is defined in the branch-hinting spec and tracked by ChromeStatus.

#### Use Cases
- Performance-sensitive Wasm code (game engines, physics, numerical kernels) can mark hot branches to reduce misprediction and cache misses.
- Compilers targeting Wasm can emit branch hints to preserve runtime performance characteristics of native builds.
- Reduces need for post-deployment profiling to find and hand-optimize hot-path layout.

#### References
- https://chromestatus.com/feature/5089072889290752
- https://github.com/WebAssembly/branch-hinting