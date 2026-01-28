---
layout: default
title: graphics-webgpu-en
---

### 1. Area Summary

Chrome 143 (stable) continues to mature WebGPU and graphics platform behavior by adding shader-level texture component swizzling, removing a non-conforming allowance for bgra8unorm read-only storage textures, and rolling up Dawn fixes that address Vulkan validation issues. The most impactful changes for developers are the new swizzle capability (enabling shader-side channel rearrangement) and the spec-aligned removal of a previously permitted but incorrect format usage. Together these updates improve cross-platform correctness, reduce platform-specific workarounds, and increase runtime validation and stability for GPU workloads. Developers should audit texture usages and consider leveraging swizzle for format portability while updating pipelines affected by the bgra8unorm removal.

## Detailed Updates

Below are the individual Graphics and WebGPU changes in Chrome 143, with practical technical notes for developers.

### Texture component swizzle

#### What's New
Shaders can now rearrange or replace texture color components (R, G, B, A) when sampling textures, via the texture component swizzle capability.

#### Technical Details
This capability is exposed when the `"texture-component-swizzle"` feature is available on a GPUAdapter. It provides shader-accessible remapping of texture channels at the API level, reducing the need for shader-side manual reordering or additional texture copies.

#### Use Cases
- Porting content between different pixel formats (e.g., BGRA vs RGBA) without extra texture uploads.
- Simplifying shaders that previously had to swizzle channels manually.
- Reducing GPU memory & bandwidth by avoiding duplicate textures for different channel orders.

#### References
- ["texture-component-swizzle"](https://gpuweb.github.io/gpuweb/#dom-gpufeaturename-texture-component-swizzle)
- [chromestatus entry](https://chromestatus.com/feature/5110223547269120)

### Remove bgra8unorm read-only storage texture usage

#### What's New
Support for using the `"bgra8unorm"` format with read-only storage textures has been removed in Chrome 143; this usage was previously tolerated but is disallowed by the WebGPU specification.

#### Technical Details
The WebGPU spec explicitly disallows `"bgra8unorm"` for read-only storage texture usage. Chrome's prior acceptance of that combination was a bug and has now been corrected to match the spec, which may cause validation or creation failures for pipelines that relied on the old behavior.

#### Use Cases
- Developers must update shaders and resource bindings that used bgra8unorm as read-only storage textures.
- Migration typically involves switching to a permitted format or changing the resource usage model (e.g., sampled texture vs storage texture).

#### References
- [issue 427681156](https://issues.chromium.org/issues/427681156)

### Dawn updates

#### What's New
Dawn includes fixes addressing a Vulkan validation error that occurred when clearing 3D textures, among other stability and correctness fixes.

#### Technical Details
A specific validation error in Vulkan when clearing 3D textures has been resolved. The Dawn commit log linked below contains the complete set of changes rolled into this Chrome update.

#### Use Cases
- Improved stability for WebGPU workloads that allocate or clear 3D textures on Vulkan backends.
- Fewer platform-specific validation failures during development and CI, aiding cross-driver portability.

#### References
- [443950688](https://issues.chromium.org/issues/443950688)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7444..chromium/7499?n=1000)

Saved to: digest_markdown/webplatform/Graphics and WebGPU/chrome-143-stable-en.md