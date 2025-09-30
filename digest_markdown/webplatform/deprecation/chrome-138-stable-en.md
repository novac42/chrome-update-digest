## Area Summary

Chrome 138 (stable) includes a focused deprecation in the WebGPU surface: the removal of the redundant `GPUAdapter.isFallbackAdapter` attribute in favor of the `GPUAdapterInfo.isFallbackAdapter` field. This change is a minor breaking change for code that reads the attribute directly from `GPUAdapter`; developers should migrate accesses to `GPUAdapterInfo`. Consolidating the API reduces duplication and clarifies the adapter information model, improving API consistency and long-term maintainability of WebGPU implementations. Teams relying on adapter feature detection should update code paths and tests to avoid runtime regressions.

## Detailed Updates

The single deprecation below follows from the summary above and explains the technical impact and migration guidance.

### WebGPU: Deprecate GPUAdapter isFallbackAdapter attribute

#### What's New
The boolean attribute `GPUAdapter.isFallbackAdapter` on `GPUAdapter` is deprecated and slated for removal because the same boolean is available on `GPUAdapterInfo` as `isFallbackAdapter`.

#### Technical Details
- The attribute is redundant with `GPUAdapterInfo.isFallbackAdapter`.
- Code that previously read `adapter.isFallbackAdapter` should instead obtain `adapter.adapterInfo` (or the equivalent API) and read `isFallbackAdapter` from the `GPUAdapterInfo` structure.
- This is described as a minor breaking change; update points in initialization and capability-detection paths.

#### Use Cases
- Migration: Replace direct reads of `GPUAdapter.isFallbackAdapter` with reads from `GPUAdapterInfo.isFallbackAdapter`.
- Tests & Feature Detection: Update unit and integration tests that assert adapter properties; ensure tools that serialize adapter info use the `GPUAdapterInfo` field.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=409259074
- https://chromestatus.com/feature/5125671816847360
- https://gpuweb.github.io/gpuweb/#gpu-adapter