---
layout: default
title: Chrome 136 Graphics and WebGPU Updates
---

# Chrome 136 Graphics and WebGPU Updates

## Area Summary

Chrome 136 brings significant enhancements to WebGPU, focusing on developer experience, performance optimization, and user accessibility. The most impactful changes include the introduction of the `isFallbackAdapter` attribute for better GPU adapter detection, substantial shader compilation improvements on Windows through Tint's new intermediate representation, and the ability for users to save WebGPU canvas content directly through context menus. These updates collectively advance the web platform by making WebGPU more predictable for library developers, faster for Windows users, and more user-friendly for content creation workflows.

## Detailed Updates

Building on the foundation of previous WebGPU releases, Chrome 136 delivers both developer-facing API improvements and behind-the-scenes performance enhancements that strengthen WebGPU's position as a premier graphics API for the web.

### GPUAdapterInfo isFallbackAdapter attribute

#### What's New
The `GPUAdapterInfo` interface now includes a boolean `isFallbackAdapter` attribute that indicates whether a GPU adapter has significant performance limitations in exchange for wider compatibility, more predictable behavior, or improved privacy.

#### Technical Details
This attribute helps developers and libraries identify when they're working with fallback adapters that may not deliver optimal performance. The addition addresses a critical need for libraries that accept user-provided `GPUDevice` objects and need to make informed decisions about feature usage and performance expectations.

#### Use Cases
WebGPU libraries can now programmatically detect fallback adapters and adjust their behavior accordingly, potentially selecting different rendering paths or warning users about performance implications. This is particularly valuable for graphics-intensive applications that need to balance compatibility with performance.

#### References
- [issue 403172841](https://issues.chromium.org/issues/403172841)
- [intent to ship](https://groups.google.com/a/chromium.org/g/blink-dev/c/VUkzIOWd2n0)

### Shader compilation time improvements on D3D12

#### What's New
Chrome's WebGPU implementation now features significant shader compilation performance improvements on Windows systems using the D3D12 backend through enhancements to the Tint shader compiler.

#### Technical Details
The improvement comes from adding an intermediate representation (IR) to Tint, positioned between the abstract syntax tree (AST) and the HLSL backend writer. This new IR layer makes the compiler architecture more efficient and opens up opportunities for additional optimizations in future releases.

#### Use Cases
Developers building WebGPU applications on Windows will experience faster shader compilation times, leading to reduced loading times and smoother development workflows. This is particularly beneficial for applications with complex shader programs or those that compile shaders at runtime.

#### References
- [issue 42251045](https://issues.chromium.org/issues/42251045)

### Lift compatibility mode restrictions

#### What's New
An experimental `"core-features-and-limits"` feature allows developers to lift all WebGPU compatibility mode restrictions when the unsafe WebGPU flag is enabled, providing access to the full range of WebGPU features and limits.

#### Technical Details
When the `chrome://flags/#enable-unsafe-webgpu` flag is enabled and the experimental feature is available on a `GPUDevice`, developers can bypass the limitations typically imposed by compatibility mode. This experimental feature is designed for testing and development scenarios where maximum WebGPU capability is needed.

#### Use Cases
This feature is primarily intended for advanced developers and researchers who need access to cutting-edge WebGPU features for testing, prototyping, or pushing the boundaries of what's possible with web-based graphics. It's particularly useful for applications that want to leverage the latest GPU capabilities without waiting for full specification stabilization.

#### References
- [issue 395855517](https://issues.chromium.org/issues/395855517)
- [WebGPU compatibility mode](https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md)
- [issue 395855516](https://issues.chromium.org/issues/395855516)

### Dawn updates

#### What's New
The Dawn WebGPU implementation receives updates to callback status handling, with the `InstanceDropped` enum value being renamed to `CallbackCancelled` for improved clarity.

#### Technical Details
The callback status enum change clarifies that when a callback is cancelled, any background processing associated with the event (such as pipeline compilation) may still continue. This naming change better reflects the actual behavior and helps developers understand the implications of callback cancellation.

#### Use Cases
Developers working with asynchronous WebGPU operations will benefit from clearer documentation and more predictable behavior when handling callback cancellations. This is particularly important for applications that manage complex asynchronous workflows or need to handle cleanup scenarios gracefully.

#### References
- [callback status](https://webgpu-native.github.io/webgpu-headers/Asynchronous-Operations.html#CallbackStatuses)
- [issue 520](https://github.com/webgpu-native/webgpu-headers/issues/520)
- [issue 369](https://github.com/webgpu-native/webgpu-headers/issues/369)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7049..chromium/7103?n=1000)

### Save and copy canvas images

#### What's New
Chrome users can now right-click on WebGPU canvas elements to access standard context menu options including "Save Image As…" and "Copy Image", bringing WebGPU canvases in line with traditional web content.

#### Technical Details
This feature extends the standard browser context menu functionality to WebGPU canvas elements, allowing users to interact with GPU-rendered content using familiar browser patterns. The implementation ensures that complex GPU-rendered scenes can be captured and saved just like any other web image.

#### Use Cases
This enhancement significantly improves the user experience for WebGPU applications, particularly those focused on content creation, data visualization, or artistic expression. Users can now easily save screenshots of 3D scenes, share visualizations, or collect reference images without requiring specialized application features.

#### References
- [issue 40902474](https://issues.chromium.org/issues/40902474)
