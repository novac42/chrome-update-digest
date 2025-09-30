---
layout: default
title: shell
---

## Detailed Updates

The following items expand on the summary above and show practical implications for Graphics and WebGPU work.

### WebGPU: Deprecate GPUAdapter isFallbackAdapter attribute

#### What's New
The `GPUAdapter.isFallbackAdapter` boolean attribute is deprecated in favor of `GPUAdapterInfo.isFallbackAdapter`, removing redundancy.

#### Technical Details
The attribute removal aligns the API surface with the GPU adapter info object model in the spec. This is a minor breaking change for code that reads the attribute directly from `GPUAdapter`.

#### Use Cases
- Code migration: read `adapter.requestAdapterInfo()` or use `adapterInfo.isFallbackAdapter` where applicable.
- Feature detection: rely on `GPUAdapterInfo` for fallback detection rather than adapter-level fields.

#### References
https://bugs.chromium.org/p/chromium/issues/detail?id=409259074
https://chromestatus.com/feature/5125671816847360
https://gpuweb.github.io/gpuweb/#gpu-adapter

### Shorthand for Using Buffer as a Binding Resource

#### What's New
You can now use a `GPUBuffer` directly as a `GPUBindingResource` when creating bind groups.

#### Technical Details
The bind group entries accept a `GPUBuffer` instance directly, removing the need to wrap it into a `GPUBufferBinding` object for common cases.

#### Use Cases
- Simplifies shader resource setup for uniform/storage buffers.
- Reduces boilerplate in JS binding code and aligns buffer bindings with other resource shorthands.

#### References
None

### Size Requirement Changes for Buffers Mapped at Creation

#### What's New
Creating a buffer with `mappedAtCreation: true` now throws a `RangeError` if `size` is not a multiple of 4.

#### Technical Details
Back-end and WebGPU spec expectations require 4-byte alignment for mapped buffer views; Chrome now enforces this at creation time to prevent subtle memory layout issues.

#### Use Cases
- Prevents undefined behavior when mapping buffers for typed-array views.
- Developers should align buffer sizes to 4 bytes; adjust allocations and add padding when necessary.

#### Example
```javascript
// javascript
// Now throws RangeError if size is not multiple of 4
myDevice.createBuffer({
  mappedAtCreation: true,
  size: 42, // will now throw
  usage: GPUBufferUsage.STORAGE,
});
```

#### References
None

### Architecture Report for Recent GPUs

#### What's New
Chrome reports new GPU architecture identifiers:
- Nvidia: "blackwell"
- AMD: "rdna4"

#### Technical Details
These strings appear in adapter/driver reports and improve fine-grained platform/feature detection for GPU vendors and generations.

#### Use Cases
- Runtime feature gates or workarounds can target specific architectures.
- Telemetry and diagnostics gain better granularity for performance tuning.

#### References
None

### Deprecation of GPUAdapter isFallbackAdapter Attribute

#### What's New
A second deprecation note: `GPUAdapter.isFallbackAdapter` is deprecated and replaced by `GPUAdapterInfo.isFallbackAdapter` (introduced in Chrome 136).

#### Technical Details
Reinforces the migration path: move to adapter info objects that centralize adapter metadata.

#### Use Cases
- Audit existing code paths that inspect adapter properties and update to use `GPUAdapterInfo`.

#### References
None

### Dawn Updates

#### What's New
Dawn build and distribution enhancements:
- Emscripten supports Dawn GLFW in CMake builds.
- A "remote" Emdawnwebgpu port included in package releases.
- Switching to Emdawnwebgpu is now a flag change from `emcc -sUSE_WEBGPU` to `emcc --use-port=emdawnwebgpu`.

#### Technical Details
These updates ease native-style builds of WebGPU apps via Emscripten and simplify switching ports for WebAssembly/WebGPU targets.

#### Use Cases
- WebAssembly developers using Dawn can more easily build/test with GLFW and the emdawnwebgpu port.
- CI and local builds can flip a single emcc flag to change ports.

#### Example
```bash
# shell
# Switch to the emdawnwebgpu port
emcc --use-port=emdawnwebgpu
```

#### References
None

Saved to: digest_markdown/webplatform/Graphics and WebGPU/chrome-138-stable-en.md
