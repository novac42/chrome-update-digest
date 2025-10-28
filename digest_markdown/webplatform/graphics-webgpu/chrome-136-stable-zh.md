# 领域摘要

Chrome 136（stable）通过围绕设备自省、编译器性能、兼容性控制和原生 Dawn API 清晰度的定向更改，继续完善 WebGPU 堆栈。对开发者影响最大的项包括新的 `GPUAdapterInfo.isFallbackAdapter` 标志用于识别受限适配器、通过 Tint IR 在 D3D12 上加速着色器编译、一个可解除兼容模式限制的实验性 `"core-features-and-limits"` 选项，以及 Dawn 中用于减少关于已取消回调歧义的 API 重命名。这些更新共同提升了运行时可预测性、编译吞吐量和 GPU 驱动的 Web 应用的开发体验。

## 详细更新

下面是对 Chrome 136 中 Graphics and WebGPU 各项更改的简洁、面向开发者的说明，以及这些更改对实现、调试和性能调优的意义。

### GPUAdapterInfo isFallbackAdapter attribute（用于标识回退适配器）

#### 新增内容
在 `GPUAdapterInfo` 上新增了布尔属性 `isFallbackAdapter`，用于指示适配器是否为具有明显性能限制但兼容性或隐私更好的回退适配器。

#### 技术细节
该属性将适配器级别的元数据提供给 WebGPU 使用者，使应用在不通过运行时探测行为的情况下区分全性能 GPU 与回退或受限适配器。

#### 适用场景
- 为回退适配器选择不同的资源预算、着色器路径或功能开关。
- 通过警告用户或自动降低画质改善用户体验。
- 用于遥测和调试，将性能问题与适配器类型相关联。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/403172841)
- [Link](https://groups.google.com/a/chromium.org/g/blink-dev/c/VUkzIOWd2n0)

### Shader compilation time improvements on D3D12（在 D3D12 上的着色器编译时间改进）

#### 新增内容
Tint 为使用 D3D12 后端的设备新增了一个中间表示（IR），以加速着色器编译。

#### 技术细节
该新 IR 位于 Tint 的 AST 与 HLSL 后端写入器之间，支持针对 D3D12/HLSL 代码生成的更高效转换，减少在管线创建期间的编译器工作量。

#### 适用场景
- 在 Windows/D3D12 上更快的管线创建与较少的卡顿。
- 动态着色器负载和迭代式开发工作流下更好的响应性。
- 在 D3D12 设备上为 WebGPU 密集型应用降低延迟。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/42251045)

### Lift compatibility mode restrictions（解除兼容模式限制）

#### 新增内容
一个实验性的 `"core-features-and-limits"` 功能，当其在 `GPUDevice` 上存在并与 chrome://flags/#enable-unsafe-webgpu 标志组合使用时，可解除兼容模式下对功能和限制的约束。

#### 技术细节
此切换提供了一个设备级别的覆盖，用于绕过兼容模式的功能/限制约束，由不安全的 WebGPU 标志控制，并通过引用的 Chromium 问题和 GPUWeb 的兼容模式提案进行跟踪。

#### 适用场景
- 在受控环境中对完整功能集进行测试和基准测量（这些功能在兼容模式下不可用）。
- 调试功能门控行为并在受控环境中验证实现是否符合完整的 WebGPU 规范。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/395855517)
- [GitHub](https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md)
- [Tracking bug](https://issues.chromium.org/issues/395855516)

### Dawn updates（Dawn 更新）

#### 新增内容
回调状态枚举值 `InstanceDropped` 已重命名为 `CallbackCancelled`，以澄清即使后台处理（例如管线编译）可能继续，回调仍被取消的含义。

#### 技术细节
这是 Dawn/webgpu-native 回调状态枚举的命名澄清，旨在减少关于异步操作生命周期和取消语义的歧义。

#### 适用场景
- 在原生集成和绑定中更安全地处理异步回调。
- 当调试或为编译任务进行埋点时，更清晰地将 JavaScript/WebGPU 错误与原生状态映射起来。

#### 参考资料
- [Link](https://webgpu-native.github.io/webgpu-headers/Asynchronous-Operations.html#CallbackStatuses)
- [GitHub](https://github.com/webgpu-native/webgpu-headers/issues/520)
- [GitHub](https://github.com/webgpu-native/webgpu-headers/issues/369)
- [Link](https://dawn.googlesource.com/dawn/+log/chromium/7049..chromium/7103?n=1000)

文件已保存到：digest_markdown/Graphics and WebGPU/chrome-136-stable-en.md