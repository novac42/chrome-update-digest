---
layout: default
title: Area Summary
---

# Area Summary

Chrome 136 (stable) continues to mature the WebGPU stack with focused changes around device introspection, compiler performance, compatibility controls, and native Dawn API clarity. The most impactful items for developers are the new GPUAdapterInfo.isFallbackAdapter flag for identifying constrained adapters, shader compilation speedups on D3D12 via a Tint IR, an experimental "core-features-and-limits" option that can lift compatibility-mode restrictions, and API renames in Dawn that reduce ambiguity around canceled callbacks. Together these updates improve runtime predictability, compilation throughput, and developer ergonomics for GPU-powered web apps.

## Detailed Updates

Below are concise, developer-focused explanations of each Graphics and WebGPU change in Chrome 136 and how they matter for implementation, debugging, and performance tuning.

### GPUAdapterInfo isFallbackAdapter attribute

#### What's New
A new boolean attribute, `isFallbackAdapter`, on GPUAdapterInfo indicates whether an adapter is a fallback with notable performance limitations but better compatibility or privacy.

#### Technical Details
This attribute surfaces adapter-level metadata to WebGPU consumers so applications can distinguish full-performance GPUs from fallback or constrained adapters without probing runtime behavior.

#### Use Cases
- Choose different resource budgets, shader paths, or feature gates for fallback adapters.
- Improve UX by warning users or automatically reducing quality on fallback devices.
- Telemetry and debugging to correlate performance issues with adapter types.

#### References
- [Tracking bug](https://issues.chromium.org/issues/403172841)
- [Link](https://groups.google.com/a/chromium.org/g/blink-dev/c/VUkzIOWd2n0)

### Shader compilation time improvements on D3D12

#### What's New
Tint adds an intermediate representation (IR) for devices using the D3D12 backend to speed shader compilation.

#### Technical Details
The new IR sits between Tint's AST and the HLSL backend writer, enabling more efficient transformations targeted at D3D12/HLSL code generation and reducing compiler work during pipeline creation.

#### Use Cases
- Faster pipeline creation and reduced jank when creating shaders on Windows/D3D12.
- Better responsiveness for dynamic shader workloads and iterative developer workflows.
- Lower latency for WebGPU-heavy applications on D3D12 devices.

#### References
- [Tracking bug](https://issues.chromium.org/issues/42251045)

### Lift compatibility mode restrictions

#### What's New
An experimental `"core-features-and-limits"` feature, when present on a GPUDevice and combined with the chrome://flags/#enable-unsafe-webgpu flag, lifts compatibility-mode restrictions on features and limits.

#### Technical Details
This toggle exposes a device-level override to bypass compatibility-mode feature/limit restrictions, controlled by the unsafe WebGPU flag and tracked via the referenced Chromium issues and the GPUWeb compatibility-mode proposal.

#### Use Cases
- Testing and benchmarking apps against full feature sets not available under compatibility mode.
- Debugging feature-gating behavior and validating implementations against the full WebGPU spec in controlled environments.

#### References
- [Tracking bug](https://issues.chromium.org/issues/395855517)
- [GitHub](https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md)
- [Tracking bug](https://issues.chromium.org/issues/395855516)

### Dawn updates

#### What's New
The callback status enum value `InstanceDropped` has been renamed to `CallbackCancelled` to clarify that callbacks were cancelled even if background processing (e.g., pipeline compilation) may continue.

#### Technical Details
This is a naming clarification in the Dawn/webgpu-native callback status enum to reduce ambiguity about the lifecycle and cancellation semantics of asynchronous operations.

#### Use Cases
- Safer handling of asynchronous callbacks in native integrations and bindings.
- Clearer mapping between JavaScript/WebGPU errors and native statuses when debugging or instrumenting compile tasks.

#### References
- [Link](https://webgpu-native.github.io/webgpu-headers/Asynchronous-Operations.html#CallbackStatuses)
- [GitHub](https://github.com/webgpu-native/webgpu-headers/issues/520)
- [GitHub](https://github.com/webgpu-native/webgpu-headers/issues/369)
- [Link](https://dawn.googlesource.com/dawn/+log/chromium/7049..chromium/7103?n=1000)

File saved to: digest_markdown/webplatform/Graphics and WebGPU/chrome-136-stable-en.md
