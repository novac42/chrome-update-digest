---
layout: default
title: graphics-webgpu-zh
---

## 领域摘要

Chrome 137 稳定版继续改进 WebGPU 可用性和 WGSL 能力，侧重于小且有意义的 API 和着色器可用性改进。本次发布着重于简化常见的开发者工作流（纹理绑定、缓冲区拷贝和 workgroup 原子式加载）、在开发者标志后公开适配器电源偏好元数据，以及移除一个实验性的兼容性属性。这些更改减少了着色器和命令编码的样板代码，改善了设备选择的诊断信息，并使 API 面向标准化方法保持一致。对于图形和 WebGPU 工程师而言，更新降低了视频/纹理管线和计算着色器的摩擦，同时缩减了遗留的实验性表面。

## 详细更新

以下是 Chrome 137 中与图形和 WebGPU 相关的更新，扩展了上述摘要内容。

### 1. Texture View for External Texture Binding (外部纹理绑定的纹理视图)

#### 新增内容
- 允许兼容的 `GPUTextureView` 用于替代 `GPUExternalTexture` 绑定。
- 简化视频特效管线中的着色器逻辑，减少动态编译着色器的需求。

#### 技术细节
- 与外部纹理绑定兼容的 `GPUTextureView` 现在可以在 bind group 和着色器绑定中替代 `GPUExternalTexture`。
- 示例（来源已截断）：
```javascript
// javascript
const bindGroup = myDevice.createBindGroup({
  layout: pipeline.getBindGroupLayout(0),...
```

#### 适用场景
- 以前需要 `GPUExternalTexture` 的视频处理和后期特效管线现在可以直接使用纹理视图，简化绑定设置和着色器变体管理。

#### 参考资料
- 未提供链接。

### 2. Buffer Copy Simplification

#### 新增内容
- 为 `copyBufferToBuffer()` 提供新的方法重载，允许省略偏移和大小参数以拷贝整个缓冲区。

#### 技术细节
- API 现在支持简化的调用签名，其中源/目的偏移和拷贝大小为可选，从而允许用单次调用拷贝整个缓冲区。
- 示例：
```javascript
// javascript
// Copy entire buffer without specifying offsets
myCommandEncoder.copyBufferToBuffer(srcBuffer, dstBuffer);
```

#### 适用场景
- 在 GPU 缓冲区之间传输完整缓冲区时减少样板代码，适用于资源上传、暂存传输和简单缓冲克隆。

#### 参考资料
- 未提供链接。

### 3. WGSL Workgroup Uniform Load (WGSL 工作组统一加载)

#### 新增内容
- 添加了 `workgroupUniformLoad(ptr)` 重载，用于对工作组共享数据执行原子式样的统一加载。

#### 技术细节
- 新的重载使得在工作组调用中以原子方式加载值成为可能，从而使单个存储的值可以被工作组中的所有线程一致地读取。
- 示例（来源已截断）：
```wgsl
// wgsl
@compute @workgroup_size(1, 1)
fn main(@builtin(local_invocation_index) lid: u32) {
  if (lid == 0) {
    atomicStore(&(wgvar), 42u);
  }
  buffer[lid] = workgroupUniformLoad(&...
```

#### 适用场景
- 需要单一权威工作组写入值的计算着色器（例如初始化标志或共享常量）可以可靠地读取该值，而无需复杂的同步模式。

#### 参考资料
- 未提供链接。

### 4. GPUAdapterInfo Power Preference (GPU 适配器信息的电源偏好)

#### 新增内容
- 在 "WebGPU Developer Features" 标志后引入了非标准的 `powerPreference` 属性到 `adapterInfo`，返回 `"low-power"` 或 `"high-performance"`。

#### 技术细节
- 当启用该开发者功能标志时，`device.adapterInfo.powerPreference` 会向用户代码公开适配器的电源目标分类。
- 示例（来源已截断）：
```javascript
// javascript
function checkPowerPreferenceForGpuDevice(device) {
  const powerPreference = device.adapterInfo.powerPreference;
  // Adjust settings based on GP...
```

#### 适用场景
- 允许开发者工具和运行时启发式根据适配器的电源特性调整渲染/计算配置（例如在高性能适配器上优先使用性能设置）。

#### 参考资料
- 未提供链接。

### 5. Removed Compatibility Mode Attribute

#### 新增内容
- 实验性的 `compatibilityMode` 属性已被移除。

#### 技术细节
- `compatibilityMode` 不再存在；它已被标准化的方法所取代（源中未提供详细信息）。

#### 适用场景
- 移除开发者可能依赖的实验性表面，鼓励迁移到标准化的兼容性机制。

#### 参考资料
- 未提供链接。

Saved to: digest_markdown/webplatform/Graphics and WebGPU/chrome-137-stable-en.md
