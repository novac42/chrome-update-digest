区域摘要

Chrome 137（stable）在 WebGPU 方面引入了一组以开发者易用性和可预测 GPU 行为为重点的增量改进。主要趋势包括 API 简化（缓冲区复制重载、对外部纹理使用纹理视图）、改进的 WGSL 工作组同步原语，以及通过非标准的 powerPreference 字段实现的设备感知。这些更改减少了样板代码，简化了着色器逻辑和编译，并允许针对特定设备进行调优以获得更好的性能与功耗权衡。构建视频管线、计算着色器和跨设备 GPU 工作负载的开发者将获得最直接的收益。

## 详细更新

下面的条目扩展了上述摘要，说明了更改内容、工作方式以及适用场景。

### 1. Texture View for External Texture Binding (允许用纹理视图绑定外部纹理)

#### 新增内容
现在允许使用兼容的 `GPUTextureView` 替代 `GPUExternalTexture` 绑定。

#### 技术细节
符合外部纹理约定的 `GPUTextureView` 可以在此前要求 `GPUExternalTexture` 的位置进行绑定，减少了对特殊绑定和着色器排列组合的需求。

#### 适用场景
简化了视频效果管线中的着色器逻辑，减少了仅为处理外部纹理绑定而动态编译或切换着色器的需要。

#### 参考资料
未提供。

### 2. Buffer Copy Simplification (缓冲区复制简化)

#### 新增内容
为 `copyBufferToBuffer()` 提供了新的方法重载，允许省略偏移和大小参数。

#### 技术细节
`copyBufferToBuffer()` 的一个重载仅接受源和目标缓冲区以复制全部内容，从而移除了为整缓冲区复制重复传入零偏移和显式大小的模式。

```javascript
// Copy entire buffer without specifying offsets
myCommandEncoder.copyBufferToBuffer(srcBuffer, dstBuffer);
```

#### 适用场景
简化了资源上传、暂存缓冲区使用和读回流程中的常见整缓冲区复制操作；减少了 API 面并降低了越界或大小出错的风险。

#### 参考资料
未提供。

### 3. WGSL Workgroup Uniform Load (WGSL 工作组统一加载)

#### 新增内容
新增 `workgroupUniformLoad(ptr)` 重载，用于原子加载，能以原子方式为所有工作组调用加载一个值。

#### 技术细节
`workgroupUniformLoad(&wgvar)` 提供类似原子读取的重载，使得由某个调用（例如工作组 leader）初始化的值在整个工作组内一致可见，而无需手动同步模式。

```wgsl
@compute @workgroup_size(1, 1)
fn main(@builtin(local_invocation_index) lid: u32) {
  if (lid == 0) {
    atomicStore(&(wgvar), 42u);
  }
  buffer[lid] = workgroupUniformLoad(&wgvar);
}
```

#### 适用场景
使常见的工作组广播模式更安全、更简单——对在整个工作组中使用单个调用计算出的参数（例如调度元数据、共享常量）的计算着色器特别有用。

#### 参考资料
未提供。

### 4. GPUAdapterInfo Power Preference (GPUAdapterInfo 电源偏好)

#### 新增内容
非标准的 `powerPreference` 属性可在 “WebGPU Developer Features” 标志下使用，并返回 `"low-power"` 或 `"high-performance"`。

#### 技术细节
`device.adapterInfo.powerPreference` 暴露了适配器的电源提示；这是非标准的并且受开发者功能标志控制，旨在用于实验性的设备感知调优。

```javascript
function checkPowerPreferenceForGpuDevice(device) {
  const powerPreference = device.adapterInfo.powerPreference;
  // Adjust settings based on GPU power preference
}
```

#### 适用场景
允许开发者根据适配器的功耗配置调整工作负载决策（质量与性能之间的取舍）——对移动设备与独立 GPU 的启发式判断，以及在适配期间的分析/遥测很有用。

#### 参考资料
未提供。

### 5. Removed Compatibility Mode Attribute (移除兼容模式属性)

#### 新增内容
实验性的 `compatibilityMode` 属性已被移除，并由一种标准化的兼容性方法替代。

#### 技术细节
该属性的移除表明正在向标准的、非实验性的兼容机制整合；依赖该实验属性的代码必须迁移到标准化路径（在可用时）。

#### 适用场景
开发者应移除对该实验性属性的使用，并遵循标准化的兼容方法以实现前向兼容并降低维护成本。

#### 参考资料
未提供。