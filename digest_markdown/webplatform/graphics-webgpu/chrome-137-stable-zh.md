## Area Summary

Chrome 137 在 Graphics 和 WebGPU 方面的更新侧重于开发者体验和跨 GPU 工作流的 API 一致性。主要主题包括简化常见操作（缓冲区复制和 external-texture 处理）、扩展 WGSL 并发原语、公开适配器电源偏好以便诊断，以及用标准化方法替换一个实验性属性。这些更改减少了样板代码，简化了着色器管线的编写与维护，并为性能调优提供了更可预测的适配器信息。对于构建 GPU 加速 Web 应用的团队，这些更新降低了着色器绑定和缓冲区管理的摩擦，同时推动向稳定且标准化的 API 迁移。

## Detailed Updates

Below are the Graphics and WebGPU changes in Chrome 137 that matter to rendering, compute, and media pipelines.

### 1. Texture View for External Texture Binding (将外部纹理绑定替换为纹理视图)

#### What's New
Now allows a compatible `GPUTextureView` to be used in place of a `GPUExternalTexture` binding, simplifying integration between video frames and shader resources.

#### Technical Details
A `GPUTextureView` can be bound where previously only a `GPUExternalTexture` was accepted. This reduces the need for special-case bindings or dynamic shader variants to handle external textures.

#### Use Cases
- Simplifies video effects pipelines that sample video frames in WGSL shaders.
- Reduces dynamic shader compilation and branching when supporting both external and regular texture sources.
- Easier integration of platform video frames into existing render passes.

#### References
No links provided.

### 2. Buffer Copy Simplification (缓冲区复制简化)

#### What's New
A new overload of `copyBufferToBuffer()` allows omitting offsets and size parameters to copy entire buffers with a single call.

#### Technical Details
The overload accepts only source and destination buffer objects, implicitly targeting the full buffer ranges, removing the need to pass explicit offsets and sizes for whole-buffer copies.

#### Use Cases
- Simplifies buffer-to-buffer data moves in resource uploads, staging buffers, and readback flows.
- Reduces accidental mistakes in offset calculations and shortens command encoding code paths for full-buffer operations.

#### References
No links provided.

### 3. WGSL Workgroup Uniform Load (WGSL 工作组一致性加载)

#### What's New
Introduces `workgroupUniformLoad(ptr)` overload for atomic loads that atomically reads a value usable by all workgroup invocations.

#### Technical Details
The new WGSL overload performs an atomic-style load of a workgroup-scoped value so that all invocations in the workgroup get a consistent read, useful after an atomic store by a single invocation.

#### Use Cases
- Synchronizing a value set by one thread (e.g., initializer invocation) and read by all other workgroup threads without additional barriers.
- Cleaner WGSL for patterns where a leader writes a value and others read it atomically.

#### References
No links provided.

### 4. GPUAdapterInfo Power Preference (GPUAdapterInfo 的电源偏好)

#### What's New
A non-standard `powerPreference` attribute is available on `device.adapterInfo` behind the "WebGPU Developer Features" flag, returning `"low-power"` or `"high-performance"`.

#### Technical Details
When the developer feature flag is enabled, adapter information includes a `powerPreference` string indicating the adapter class. This is non-standard and gated for developer experimentation.

#### Use Cases
- Adjusting rendering quality, workload distribution, or power-sensitive behavior based on whether the adapter is low-power (integrated) or high-performance (discrete).
- Diagnostics and telemetry to tune default settings for different hardware classes during development.

#### References
No links provided.

### 5. Removed Compatibility Mode Attribute (移除 Compatibility Mode 属性)

#### What's New
The experimental `compatibilityMode` attribute was removed and replaced by a standardized approach for compatibility.

#### Technical Details
The removal indicates consolidation toward standardized compatibility mechanisms; the experimental attribute no longer exists in this release.

#### Use Cases
- Developers should migrate off the experimental `compatibilityMode` attribute and adopt the standardized compatibility patterns recommended by the platform.
- Reduces fragmentation and encourages use of stable, cross-implementation behaviors.

#### References
No links provided.