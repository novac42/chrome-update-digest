digest_markdown/webplatform/Graphics and WebGPU/chrome-137-stable-en.md

# Area Summary

Chrome 137 在 Graphics 和 WebGPU 的更新侧重于 API 简化、着色器/工作组原语以及设备信息检查，同时清理了实验性属性。最重要的更改包括允许开发者在外部视频绑定处重用 texture view、简化全缓冲区复制，以及在 WGSL 中引入原子工作组 uniform 加载，从而减少动态着色器编译和同步复杂性。提供一个非标准的 adapter `powerPreference` 字段，有助于在低功耗与高性能 GPU 之间进行调优；而移除实验性的 `compatibilityMode` 属性则推动采用标准化方案。这些变更减少样板代码，提高异构设备上的性能可预测性，并降低高级 GPU 驱动 Web 应用的开发摩擦。

## Detailed Updates

Below are focused descriptions of each Graphics and WebGPU change in Chrome 137, with practical notes for developers.

### 1. Texture View for External Texture Binding

#### What's New
Now allows a compatible `GPUTextureView` to be used in place of a `GPUExternalTexture` binding, simplifying video effect pipelines.

#### Technical Details
A bind group may accept a `GPUTextureView` where previously a `GPUExternalTexture` was required, enabling reuse of standard texture views with existing shader bindings. This reduces the need to create or manage separate external-texture objects and can eliminate runtime shader specialization tied to external texture semantics.

#### Use Cases
- Video post-processing effects that previously required separate external texture bindings can now use existing texture views, simplifying resource management.
- Reduces dynamic shader compilation paths for pipelines that must handle both regular and external textures.

#### References
No links provided.

```javascript
const bindGroup = myDevice.createBindGroup({
  layout: pipeline.getBindGroupLayout(0),...
```

### 2. Buffer Copy Simplification

#### What's New
New overload for `copyBufferToBuffer()` that omits offsets and size parameters to copy entire buffers.

#### Technical Details
A more ergonomic API variant lets developers call `myCommandEncoder.copyBufferToBuffer(srcBuffer, dstBuffer);` to copy whole buffer contents without specifying explicit offsets and size. This reduces API surface friction for common full-buffer operations and avoids manual bookkeeping of buffer sizes.

#### Use Cases
- Quick full-buffer duplication during staging or resource uploads.
- Test and tooling code that frequently copies entire buffers without needing offset precision.
- Simplifies common patterns in GPU compute and resource preparation, improving developer productivity.

#### References
No links provided.

```javascript
// Copy entire buffer without specifying offsets
myCommandEncoder.copyBufferToBuffer(srcBuffer, dstBuffer);
```

### 3. WGSL Workgroup Uniform Load

#### What's New
Introduces `workgroupUniformLoad(ptr)` overload for atomic loads, enabling atomic retrieval of a value across workgroup invocations.

#### Technical Details
The `workgroupUniformLoad` call provides an atomic load semantic for workgroup-shared values so all invocations observe a consistent value after atomicStore by one invocation. This aids synchronization patterns inside WGSL compute shaders and reduces the need for complex manual barriers or extra signaling.

#### Use Cases
- Compute shaders needing a single writer to publish a configuration or sentinel value to all workgroup threads.
- Simplifies atomic-based coordination inside workgroups for tasks such as work dispatching, shared state updates, and deterministic initialization.

#### References
No links provided.

```wgsl
@compute @workgroup_size(1, 1)
fn main(@builtin(local_invocation_index) lid: u32) {
  if (lid == 0) {
    atomicStore(&(wgvar), 42u);
  }
  buffer[lid] = workgroupUniformLoad(&...
```

### 4. GPUAdapterInfo Power Preference

#### What's New
A non-standard `powerPreference` attribute is available (behind "WebGPU Developer Features" flag) on adapterInfo, returning `"low-power"` or `"high-performance"`.

#### Technical Details
The adapterInfo exposes a `powerPreference` string indicating the adapter's power class, useful for runtime heuristics. This is non-standard and gated behind a developer feature flag, intended for diagnostic and tuning scenarios rather than as a stable API.

#### Use Cases
- Adjusting rendering or compute quality based on whether the device is low-power (e.g., integrated GPU) or high-performance (discrete GPU).
- Profiling and telemetry in development environments to validate power-targeted optimizations.

#### References
No links provided.

```javascript
function checkPowerPreferenceForGpuDevice(device) {
  const powerPreference = device.adapterInfo.powerPreference;
  // Adjust settings based on GP...
```

### 5. Removed Compatibility Mode Attribute

#### What's New
The experimental `compatibilityMode` attribute has been removed and replaced by standardized compatibility approaches.

#### Technical Details
Removal of the experimental flag indicates consolidation toward standardized compatibility mechanisms; developers should migrate away from relying on `compatibilityMode` and adopt public, standardized compatibility strategies exposed by the platform.

#### Use Cases
- Audit code that depended on experimental compatibilityMode and refactor to supported, standardized APIs or feature-detection patterns.
- Reduce reliance on browser-specific experimental flags for production workloads.

#### References
No links provided.