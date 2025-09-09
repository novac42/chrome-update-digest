---
layout: default
title: Graphics and WebGPU - Chrome 137
---

# Graphics and WebGPU - Chrome 137

## Graphics (from Chrome Release Notes)

### GPUTextureView for externalTexture binding

A `GPUTextureView` is now allowed to be used for an `externalTexture` binding when creating a `GPUBindGroup`.

**References:** [Tracking bug #398752857](https://bugs.chromium.org/p/chromium/issues/detail?id=398752857) | [ChromeStatus.com entry](https://chromestatus.com/feature/5107071463104512) | [Spec](https://gpuweb.github.io/gpuweb/#gpubindgroup)


### copyBufferToBuffer overload

The `GPUCommandEncoder` `copyBufferToBuffer()` method now includes a simpler way to copy entire buffers using a new overload with optional offsets and size parameters.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5103419089608704) | [Spec](https://gpuweb.github.io/gpuweb/#dom-gpucommandencoder-copybuffertobuffer)


## WebGPU Features

### 1. Texture View for External Texture Binding
- Now allows a compatible `GPUTextureView` to be used in place of a `GPUExternalTexture` binding
- Simplifies shader logic in video effects pipelines
- Reduces need for dynamically compiling shaders

```javascript
const bindGroup = myDevice.createBindGroup({
  layout: pipeline.getBindGroupLayout(0),
  entries: [
    { binding: 0, resource: texture.createView() }, // Texture view for external texture
    { binding: 1, resource: { buffer: myBuffer } },
  ],
});
```


### 2. Buffer Copy Simplification
- New method overload allows omitting offsets and size parameters in `copyBufferToBuffer()`
- Simplifies copying entire buffers

```javascript
// Copy entire buffer without specifying offsets
myCommandEncoder.copyBufferToBuffer(srcBuffer, dstBuffer);
```


### 3. WGSL Workgroup Uniform Load
- New `workgroupUniformLoad(ptr)` overload for atomic loads
- Atomically loads value for all workgroup invocations

```wgsl
@compute @workgroup_size(1, 1)
fn main(@builtin(local_invocation_index) lid: u32) {
  if (lid == 0) {
    atomicStore(&(wgvar), 42u);
  }
  buffer[lid] = workgroupUniformLoad(&wgvar);
}
```


### 4. GPUAdapterInfo Power Preference
- Non-standard `powerPreference` attribute available with "WebGPU Developer Features" flag
- Returns `"low-power"` or `"high-performance"`

```javascript
function checkPowerPreferenceForGpuDevice(device) {
  const powerPreference = device.adapterInfo.powerPreference;
  // Adjust settings based on GPU power preference
}
```


### 5. Removed Compatibility Mode Attribute
- Experimental `compatibilityMode` attribute removed
- Replaced by standardized approach for compatibility

<!-- Deduplication: 7 → 7 features -->