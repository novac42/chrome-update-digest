## 领域摘要

Chrome 140 在存储方面的更改侧重于通过弃用在只读存储纹理中使用 "bgra8unorm" 格式来收紧 WebGPU 的行为。这一举措强制执行 WebGPU 规范，移除了此前 Chrome 的特殊允许，该允许在可移植性和正确性上是一个 bug。对开发者影响最大的变化是停止将 bgra8unorm 用作只读存储纹理，并使纹理用法与规范意图（写入专用）语义一致。此更新提高了跨浏览器的兼容性并使网页平台上的 GPU 资源处理更加可预测。

## 详细更新

下面的单一更新来源于摘要：Chrome 正在将先前被误允的 WebGPU 存储纹理格式的处理迁移到与规范一致的方式。

### Deprecate bgra8unorm read-only storage texture usage（弃用 bgra8unorm 只读存储纹理用法）

#### 新增内容
在只读存储纹理中使用 "bgra8unorm" 格式现在被弃用。WebGPU 规范明确禁止这样做，Chrome 之前的允许是一个 bug，因为该格式是为写入专用访问设计且不可移植。

#### 技术细节
- 这强制执行 WebGPU 对存储纹理的规范约束：不应在只读存储绑定使用中使用 "bgra8unorm"。
- Chrome 之前的行为不符合规范；此次更改移除了该不可移植的例外。
- 依赖于对 bgra8unorm 存储纹理进行只读采样或着色器读取的开发者必须调整为符合规范的格式/用法。

#### 适用场景
- 此前将 bgra8unorm 用作只读存储纹理的 WebGPU 图形和计算工作负载需要迁移到受支持的格式，或在适当情况下将纹理用法改为写入专用。
- 确保在不同浏览器和 GPU 供应商之间表现更一致，减少平台特定的 bug，并提高着色器代码和资源管理的可移植性。

#### 参考资料
- 问题 427681156: https://issues.chromium.org/issues/427681156

## 领域特定专业知识（存储相关影响）
- graphics-webgpu: 此更改直接影响 WebGPU 存储纹理和着色器资源绑定；请更新着色器和流水线布局以避免只读 bgra8unorm 用法。
- webapi: WebGPU API 使用者必须根据规范规则验证纹理格式和用法，以防止运行时错误。
- performance: 迁移到符合规范的模式可避免未定义行为，而未定义行为可能导致不同设备上 GPU 性能不可预测。
- security-privacy: 符合规范可以减少可能导致意外资源访问模式的平台特定特性。
- deprecations: 将此视为弃用警告；将代码迁移到受支持的格式/用法以保持未来兼容性。

保存文件至：digest_markdown/webplatform/storage/chrome-140-stable-en.md