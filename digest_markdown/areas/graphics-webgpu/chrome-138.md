---
layout: default
title: Graphics and WebGPU - Chrome 138
---

# Graphics and WebGPU - Chrome 138

## WebGPU Features

### Shorthand for Using Buffer as a Binding Resource

Developers can now use a `GPUBuffer` directly as a `GPUBindingResource`. This simplifies binding and makes it consistent with other binding types:

```javascript
const bindGroup = myDevice.createBindGroup({
  layout: myPipeline.getBindGroupLayout(0),
  entries: [
    { binding: 0, resource: mySampler },
    { binding: 1, resource: myTextureView },
    { binding: 2, resource: myExternalTexture },
    { binding: 3, resource: myBuffer }, // Simplified syntax
    { binding: 4, resource: { buffer: myOtherBuffer, offset: 42 } },
  ],
});
```


### Size Requirement Changes for Buffers Mapped at Creation

Creating a buffer with `mappedAtCreation: true` now throws a `RangeError` if the `size` is not a multiple of 4:

```javascript
myDevice.createBuffer({
  mappedAtCreation: true,
  size: 42, // This will now throw a RangeError
  usage: GPUBufferUsage.STORAGE,
});
```


### Architecture Report for Recent GPUs

New GPU architectures are now reported:
- Nvidia: `"blackwell"`
- AMD: `"rdna4"`


### Deprecation of GPUAdapter isFallbackAdapter Attribute

The `isFallbackAdapter` attribute for `GPUAdapter` is deprecated. It's replaced by the `GPUAdapterInfo.isFallbackAdapter` attribute introduced in Chrome 136.


### Dawn Updates

- Emscripten now supports Dawn GLFW for CMake builds
- A "remote" Emdawnwebgpu port is included in package releases
- Switching to Emdawnwebgpu is now a single flag change from `emcc -sUSE_WEBGPU` to `emcc --use-port=emdawnwebgpu`

<!-- Deduplication: 5 → 5 features -->