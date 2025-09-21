# Chrome 140 存储更新分析

## 摘要

Chrome 140 在**存储**领域引入了一项重要弃用，影响 WebGPU 存储纹理。最显著的变化是弃用 `bgra8unorm` 格式用于只读存储纹理使用，使 Chrome 的实现与 WebGPU 规范保持一致，以提高可移植性并修正之前的实现错误。

## 功能详情

### Deprecate bgra8unorm read-only storage texture usage

**更改内容**：
Chrome 140 弃用在 WebGPU 中将 `"bgra8unorm"` 格式用于只读存储纹理。此更改修正了之前的实现错误，Chrome 错误地允许此格式用于只读存储纹理。WebGPU 规范明确禁止此用法，因为 `bgra8unorm` 格式专为只写访问而设计。此弃用确保在不同 WebGPU 实现之间具有更好的可移植性，并使 Chrome 符合官方 WebGPU 规范。使用此格式组合的开发者应迁移到适当的替代格式，这些格式对只读存储纹理操作提供正确支持。

**参考资料**：
- [issue 427681156](https://issues.chromium.org/issues/427681156)