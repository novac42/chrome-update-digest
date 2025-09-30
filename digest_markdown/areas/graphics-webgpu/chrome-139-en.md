---
layout: default
title: chrome-139-en
---

## Area Summary

Chrome 139's Graphics and WebGPU updates focus on expanding WebGPU capability and interoperability: support for compressed 3D textures (BC/ASTC), a new "core-features-and-limits" capability for compatibility negotiation, an origin trial to broaden device reach for compatibility mode, and Dawn upstream changes. The most impactful items for developers are improved runtime performance and memory efficiency for volume/3D textures, clearer capability negotiation for adapter/device selection, and early access to a compatibility mode to reach older devices. Together these advances reduce bandwidth and memory costs for GPU workloads, and provide clearer feature detection and migration paths for WebGPU-based applications.

## Detailed Updates

Below are concise, developer-focused summaries of each Graphics and WebGPU feature in this release.

### 3D texture support for BC and ASTC compressed formats

#### What's New
The "texture-compression-bc-sliced-3d" and "texture-compression-astc-sliced-3d" WebGPU features add support for 3D textures using BC and ASTC block-compressed formats, enabling more efficient GPU memory use for volumetric data.

#### Technical Details
Enables BC and ASTC block compression for texture3D resources via WebGPU feature flags, allowing drivers and implementations that support these formats to expose them to applications.

#### Use Cases
Volume rendering, medical imaging, volumetric effects, and any GPU workloads that benefit from reduced memory footprint and bandwidth for 3D textures.

#### References
- [Volume Rendering - Texture 3D WebGPU sample](https://webgpu.github.io/webgpu-samples/?sample=volumeRenderingTexture3D)  
- [chromestatus entry](https://chromestatus.com/feature/5080855386783744)

### New "core-features-and-limits" feature

#### What's New
Introduces a "core-features-and-limits" feature used by an upcoming WebGPU compatibility mode to indicate that an adapter or device supports the core features and limits defined by the WebGPU spec.

#### Technical Details
A capability flag reported by adapters/devices to signal compliance with the spec’s core feature set and limits; useful during compatibility negotiations between implementations and the WebGPU API surface.

#### Use Cases
Feature detection and capability negotiation for libraries and engines that need a stable baseline of WebGPU features across implementations.

#### References
- [explainer](https://gist.github.com/greggman/0dea9995e33393c546a4c2bd2a12e50e)  
- [issue 418025721](https://issues.chromium.org/issues/418025721)

### Origin trial for WebGPU compatibility mode

#### What's New
An origin trial exposing a WebGPU compatibility mode, intended to reach devices lacking modern native graphics APIs by offering a compatibility-oriented execution path.

#### Technical Details
Origin trial allows developers to opt-in on origins to exercise WebGPU compatibility mode while the feature is evaluated; this helps broaden the set of devices that can run WebGPU content.

#### Use Cases
Progressive rollout for sites that need to reach wider device populations, evaluate compatibility behavior, and generate feedback before full platform enablement.

#### References
- [requestAdapter()](https://developer.mozilla.org/docs/Web/API/GPU/requestAdapter)  
- [minor adjustments](https://webgpufundamentals.org/webgpu/lessons/webgpu-compatibility-mode.html)  
- [Generate Mipmap WebGPU sample](https://webgpu.github.io/webgpu-samples/?sample=generateMipmap)

### Dawn updates

#### What's New
Dawn-related changes include adding a `message` argument to `WGPUQueueWorkDoneCallback` for consistency with other status-taking callbacks, plus build/runtime adjustments when emdawnwebgpu is linked with `-sSHARED_MEMORY`.

#### Technical Details
API header and Dawn CL updates adjust callback signatures and address emscripten/shared-memory build interactions; a range of commits in the Dawn Chromium branch accompany these changes.

#### Use Cases
Library and engine maintainers updating native/web bindings to match header/API changes and to ensure correct behavior when building Dawn-based WebGPU backends with shared memory configurations.

#### References
- [webgpu-headers PR](https://github.com/webgpu-native/webgpu-headers/pull/528)  
- [Dawn CL 244075](https://dawn-review.googlesource.com/c/dawn/+/244075)  
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7204..chromium/7258?n=1000)

## Area-Specific Expertise Notes

- graphics-webgpu: Compressed 3D texture support directly reduces GPU memory and bandwidth for volumetric workloads—important for real-time rendering and mobile where memory is constrained.  
- webapi: The "core-features-and-limits" flag simplifies capability detection for adapter selection and graceful fallback.  
- devices: The origin trial targets device fragmentation by enabling compatibility paths to reach older GPUs or OS API levels.  
- performance: Block-compressed 3D textures and spec-aligned feature negotiation both drive predictable performance and reduced resource usage.  
- webassembly / javascript / engines: Dawn and header updates require engine authors and bindings to align signatures and build flags when targeting emscripten/shared-memory configurations.  
- security-privacy, pwa-service-worker, multimedia, css, deprecations: Monitor platform rollout via origin trial and Chromestatus entries to plan progressive enhancement and migration strategies.

Saved to: digest_markdown/webplatform/Graphics and WebGPU/chrome-139-stable-en.md
