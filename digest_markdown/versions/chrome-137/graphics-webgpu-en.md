---
layout: default
title: graphics-webgpu-en
---

## Detailed Updates

The items below expand on the summary above and show what changed, how it works, and where it helps.

### 1. Texture View for External Texture Binding

#### What's New
Now allows a compatible `GPUTextureView` to be used in place of a `GPUExternalTexture` binding.

#### Technical Details
A `GPUTextureView` that matches the external texture contract can be bound where `GPUExternalTexture` was previously required, reducing the need for special-case bindings and shader permutations.

#### Use Cases
Simplifies shader logic in video effects pipelines and reduces the need for dynamically compiling or switching shaders solely to handle external-texture bindings.

#### References
None provided.

### 2. Buffer Copy Simplification

#### What's New
New method overload allows omitting offsets and size parameters in `copyBufferToBuffer()`.

#### Technical Details
An overload of `copyBufferToBuffer()` accepts only source and destination buffers to copy the entire contents, removing the repetitive pattern of passing zero offsets and explicit size for full-buffer copies.

```javascript
// Copy entire buffer without specifying offsets
myCommandEncoder.copyBufferToBuffer(srcBuffer, dstBuffer);
```

#### Use Cases
Simplifies common full-buffer copy operations in resource uploads, staging buffer usage, and readback flows; reduces API surface and potential for off-by-one or size-errors.

#### References
None provided.

### 3. WGSL Workgroup Uniform Load

#### What's New
New `workgroupUniformLoad(ptr)` overload for atomic loads that atomically loads a value for all workgroup invocations.

#### Technical Details
`workgroupUniformLoad(&wgvar)` provides an atomic-read style overload so a value initialized by one invocation (e.g., the workgroup leader) is observed consistently across the workgroup without manual synchronization patterns.

```wgsl
@compute @workgroup_size(1, 1)
fn main(@builtin(local_invocation_index) lid: u32) {
  if (lid == 0) {
    atomicStore(&(wgvar), 42u);
  }
  buffer[lid] = workgroupUniformLoad(&wgvar);
}
```

#### Use Cases
Makes common workgroup broadcast patterns safer and simpler — useful for compute shaders where a single invocation computes a parameter used by the whole workgroup (e.g., dispatch metadata, shared constants).

#### References
None provided.

### 4. GPUAdapterInfo Power Preference

#### What's New
A non-standard `powerPreference` attribute is available behind the "WebGPU Developer Features" flag and returns `"low-power"` or `"high-performance"`.

#### Technical Details
`device.adapterInfo.powerPreference` exposes the adapter's power hint; it's non-standard and gated by a developer feature flag, intended for experimental device-aware tuning.

```javascript
function checkPowerPreferenceForGpuDevice(device) {
  const powerPreference = device.adapterInfo.powerPreference;
  // Adjust settings based on GPU power preference
}
```

#### Use Cases
Allows developers to adapt workload decisions (quality vs. performance) based on the adapter's power profile — useful for mobile vs. discrete GPU heuristics, and for profiling/telemetry during adaptation.

#### References
None provided.

### 5. Removed Compatibility Mode Attribute

#### What's New
The experimental `compatibilityMode` attribute was removed and replaced by a standardized approach for compatibility.

#### Technical Details
The removal indicates consolidation toward a standard, non-experimental compatibility mechanism; code relying on the experimental attribute must migrate to the standardized path once available.

#### Use Cases
Developers should remove use of the experimental attribute and follow the standardized compatibility approach for forward compatibility and reduced maintenance.

#### References
None provided.
