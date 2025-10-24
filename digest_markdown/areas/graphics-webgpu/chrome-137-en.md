---
layout: default
title: chrome-137-en
---

## Area Summary

Chrome 137 stable continues to refine WebGPU ergonomics and WGSL capabilities, focusing on small but meaningful API and shader usability improvements. The release centers on simplifying common developer workflows (texture binding, buffer copies, and atomic workgroup loads), exposing adapter power preference metadata behind a developer flag, and removing an experimental compatibility attribute. These changes reduce boilerplate shader and command-encoding code, improve device selection diagnostics for developers, and align the API surface toward standardized approaches. For Graphics and WebGPU engineers, the updates lower friction for video/texture pipelines and compute shaders while trimming legacy experimental surface area.

## Detailed Updates

Below are the Graphics and WebGPU updates in Chrome 137 that expand on the summary above.

### 1. Texture View for External Texture Binding

#### What's New
- Allows a compatible `GPUTextureView` to be used in place of a `GPUExternalTexture` binding.
- Simplifies shader logic in video effects pipelines and reduces the need for dynamically compiled shaders.

#### Technical Details
- A `GPUTextureView` compatible with the external texture binding can now substitute for `GPUExternalTexture` in bind groups and shader bindings.
- Example (truncated in source):
```javascript
// javascript
const bindGroup = myDevice.createBindGroup({
  layout: pipeline.getBindGroupLayout(0),...
```

#### Use Cases
- Video processing and post‑effect pipelines that previously required `GPUExternalTexture` can use texture views directly, simplifying binding setup and shader variations.

#### References
- No links provided.

### 2. Buffer Copy Simplification

#### What's New
- New method overload for `copyBufferToBuffer()` allows omitting offsets and size parameters to copy entire buffers.

#### Technical Details
- The API now supports a simplified call signature where source/destination offsets and copy size are optional to enable copying whole buffers in one call.
- Example:
```javascript
// javascript
// Copy entire buffer without specifying offsets
myCommandEncoder.copyBufferToBuffer(srcBuffer, dstBuffer);
```

#### Use Cases
- Reduces boilerplate when transferring complete buffers between GPU buffers, useful in resource uploads, staging transfers, and simple buffer cloning.

#### References
- No links provided.

### 3. WGSL Workgroup Uniform Load

#### What's New
- Adds a `workgroupUniformLoad(ptr)` overload to perform atomic-style uniform loads for workgroup-shared data.

#### Technical Details
- The new overload enables atomically loading a value across workgroup invocations so a single stored value can be read consistently by all threads in the workgroup.
- Example (truncated in source):
```wgsl
// wgsl
@compute @workgroup_size(1, 1)
fn main(@builtin(local_invocation_index) lid: u32) {
  if (lid == 0) {
    atomicStore(&(wgvar), 42u);
  }
  buffer[lid] = workgroupUniformLoad(&...
```

#### Use Cases
- Compute shaders that need a single authoritative workgroup-written value (e.g., initialization flags or shared constants) can read it reliably without complex synchronization patterns.

#### References
- No links provided.

### 4. GPUAdapterInfo Power Preference

#### What's New
- Introduces a non-standard `powerPreference` attribute on `adapterInfo` available behind the "WebGPU Developer Features" flag, returning `"low-power"` or `"high-performance"`.

#### Technical Details
- When the developer feature flag is enabled, `device.adapterInfo.powerPreference` exposes the adapter's power target classification to user code.
- Example (truncated in source):
```javascript
// javascript
function checkPowerPreferenceForGpuDevice(device) {
  const powerPreference = device.adapterInfo.powerPreference;
  // Adjust settings based on GP...
```

#### Use Cases
- Allows developer tooling and runtime heuristics to adjust rendering/compute configurations based on adapter power characteristics (e.g., preferring performance settings on high-performance adapters).

#### References
- No links provided.

### 5. Removed Compatibility Mode Attribute

#### What's New
- The experimental `compatibilityMode` attribute has been removed.

#### Technical Details
- `compatibilityMode` is no longer present; it has been replaced by a standardized approach (details not provided in source).

#### Use Cases
- Removes an experimental surface that developers might have relied on, encouraging migration to the standardized compatibility mechanism.

#### References
- No links provided.

Saved to: digest_markdown/webplatform/Graphics and WebGPU/chrome-137-stable-en.md
