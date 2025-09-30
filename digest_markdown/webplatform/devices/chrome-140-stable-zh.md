## 区域摘要

Chrome 140 (stable) 引入了一个重要的 WebGPU 生命周期更改，影响在设备上创建 device 的方式。该更新强制执行 WebGPU 规范中关于适配器在成功请求设备后会被“consumed”的规则，改变了重复请求设备的处理方式。对于 Devices 开发者而言，这是最具影响力的更改，因为它改变了设备创建模式并要求显式处理适配器状态。此更改通过使 Chromium 与 GPUWeb 规范保持一致，提升了适配器/设备生命周期和资源管理的清晰性，从而推进了平台的发展。

## 详细更新

本节对上述摘要做进一步说明，并解释开发者必须考虑的具体更改。

### Device requests consume adapter（设备请求会消耗适配器）

#### 新增内容
根据 WebGPU 规范，适配器在成功请求设备后会被标记为“consumed”。因此，随后对同一适配器调用 `requestDevice()` 的调用现在将导致 promise 被拒绝。

#### 技术细节
- 适配器状态转换现在遵循 GPUWeb 的“adapter consumed”语义：一旦对某个适配器的 `requestDevice()` 成功，该适配器即被视为 consumed。
- 以后对同一适配器实例的任何 `requestDevice()` 调用将被拒绝，而不是返回另一个 device。

#### 适用场景
- 更新代码和库以对每个适配器只调用一次 `requestDevice()`，或在需要另一个 device 时通过 `requestAdapter()` 获取新的适配器。
- 在 `requestDevice()` 周围增加稳健的 promise 拒绝处理，以暴露适配器已被 consumed 的错误。
- 调整渲染引擎、框架和 worker 的初始化流程，这些流程曾假定可以从同一适配器创建多个设备。

#### 参考资料
- WebGPU specification: https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1  
- 问题 415825174: https://issues.chromium.org/issues/415825174