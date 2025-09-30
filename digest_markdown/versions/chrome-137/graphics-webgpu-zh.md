---
layout: default
title: 领域摘要
---

# 领域摘要

Chrome 137（stable）为 WebGPU 及相关图形基元提供了针对性的增量改进，简化了常见的开发者工作流。主要主题包括 API 易用性（更简单的缓冲区复制、可绑定的纹理视图）、WGSL 中更安全的并发原语，以及通过适配器功耗提示实现更清晰的设备检测。这些更改减少了着色器/运行时样板代码，使视频和计算代码路径更易于编写和优化。对于开发者来说，更新在处理外部视频纹理、整个缓冲区操作和工作组范围的原子加载时降低了摩擦。

## 详细更新

以下条目对上文摘要进行了扩展，提供开发者可采取行动的简明说明。

### 1. Texture View for External Texture Binding（外部纹理绑定的纹理视图）

#### 新增内容
- 现在允许使用兼容的 `GPUTextureView` 来替代 `GPUExternalTexture` 绑定。
- 简化了视频效果管线中的着色器逻辑。
- 减少了动态编译着色器的需要。

#### 技术细节
- 以前需要 `GPUExternalTexture` 的绑定现在可以接受兼容的 `GPUTextureView`，从而允许在外部内容管线中重用现有的纹理视图对象。

#### 适用场景
- 视频效果着色器可以直接从 `GPUTextureView` 采样，减少运行时着色器变体和动态编译。
- 在外部帧与常规纹理之间切换的管线可以共享 bind group 布局。

#### 参考资料
- 无提供链接。

#### 示例
```javascript
const bindGroup = myDevice.createBindGroup({
  layout: pipeline.getBindGroupLayout(0),...
```

### 2. Buffer Copy Simplification（缓冲区复制简化）

#### 新增内容
- 新的方法重载允许在 `copyBufferToBuffer()` 中省略偏移量和大小参数。
- 简化了整个缓冲区的复制操作。

#### 技术细节
- 提供了更简短的重载 `copyBufferToBuffer(srcBuffer, dstBuffer)`，用于表达整缓冲区复制意图，而无需显式的偏移/大小。

#### 适用场景
- 简化需要复制或移动整个缓冲区的命令编码器代码，无需计算缓冲区长度或零偏移。
- 减少实用工具和测试代码中的样板代码。

#### 参考资料
- 无提供链接。

#### 示例
```javascript
// Copy entire buffer without specifying offsets
myCommandEncoder.copyBufferToBuffer(srcBuffer, dstBuffer);
```

### 3. WGSL Workgroup Uniform Load（WGSL 工作组统一加载）

#### 新增内容
- 新的 `workgroupUniformLoad(ptr)` 重载用于原子加载。
- 为所有工作组调用原子地加载值。

#### 技术细节
- WGSL 重载提供一种来自工作组存储的原子风格统一加载，以便所有调用获得由单个调用可原子写入的一致值。

#### 适用场景
- 一次调用存储哨兵或配置值而所有其它调用需要可靠读取且无竞争的场景。
- 简化依赖于工作组共享状态的计算着色器中的同步逻辑。

#### 参考资料
- 无提供链接。

#### 示例
```wgsl
@compute @workgroup_size(1, 1)
fn main(@builtin(local_invocation_index) lid: u32) {
  if (lid == 0) {
    atomicStore(&(wgvar), 42u);
  }
  buffer[lid] = workgroupUniformLoad(&...
```

### 4. GPUAdapterInfo Power Preference（GPUAdapterInfo 能耗偏好）

#### 新增内容
- 非标准的 `powerPreference` 属性在启用 “WebGPU Developer Features” 标志时可用。
- 返回值为 `"low-power"` 或 `"high-performance"`。

#### 技术细节
- 适配器/设备检测包含一个 `powerPreference` 字段（在开发者功能之后面），指示适配器的偏好类别。

#### 适用场景
- 用于基于适配器能耗类别选择质量/功能等级、节流工作负载或调整渲染选项的启发式方法。
- 当启用功能标志时，对诊断和仅开发者调优非常有用。

#### 参考资料
- 无提供链接。

#### 示例
```javascript
function checkPowerPreferenceForGpuDevice(device) {
  const powerPreference = device.adapterInfo.powerPreference;
  // Adjust settings based on GP...
```

### 5. Removed Compatibility Mode Attribute（移除兼容性模式属性）

#### 新增内容
- 实验性的 `compatibilityMode` 属性已移除。
- 被标准化的兼容性方法取代。

#### 技术细节
- 该实验性属性已不再存在；开发者应使用替代该属性的标准化兼容性机制。

#### 适用场景
- 清理实验性表面减少了 API 面并引导开发者使用标准化的兼容路径。

#### 参考资料
- 无提供链接。

文件已保存到: digest_markdown/webplatform/Graphics and WebGPU/chrome-137-stable-en.md
