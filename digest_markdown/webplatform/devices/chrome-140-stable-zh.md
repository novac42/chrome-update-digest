# Chrome 140 稳定版 - 设备更新分析

## 摘要

Chrome 140 在**设备**领域引入了一项重要的 WebGPU 规范合规性更新。关键变更涉及适配器消费行为，WebGPU 适配器现在在成功的设备请求后会被正确标记为"已消费"，根据 WebGPU 规范防止从同一适配器创建多个设备。

## 功能详情

### Device requests consume adapter

**变更内容**：
此更新根据官方规范实现了正确的 WebGPU 适配器状态管理。当 WebGPU 适配器通过 `requestDevice()` 成功创建设备时，适配器现在会被标记为"已消费"，无法用于后续的设备请求。在同一已消费适配器上的任何额外 `requestDevice()` 调用都将导致 Promise 被拒绝，确保符合 WebGPU 规范并防止潜在的资源冲突或未定义行为。

此变更影响使用 WebGPU 应用程序的开发者，他们需要正确管理 GPU 设备创建和适配器生命周期。之前依赖重复使用适配器进行多个设备请求的应用程序需要更新，为每次设备创建请求新的适配器。

**参考资料**：
- [WebGPU specification](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1)
- [issue 415825174](https://issues.chromium.org/issues/415825174)