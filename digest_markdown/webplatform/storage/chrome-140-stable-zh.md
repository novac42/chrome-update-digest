# Chrome 140 Storage Updates - Expert Analysis

## Area Summary

Chrome 140 带来了对 WebGPU 存储纹理处理的重要更正，专门解决了只读存储纹理的 `bgra8unorm` 格式弃用问题。此更改通过移除对之前版本中错误允许的格式的支持，使 Chrome 与 WebGPU 规范保持一致。此次更新体现了 Chrome 对图形 API 规范合规性和跨平台可移植性的承诺。虽然这是一个单一更改，但它代表了确保 WebGPU 应用程序在不同实现和硬件平台上表现一致的关键步骤。

## Detailed Updates

此版本专注于纠正 WebGPU 存储纹理使用中的长期规范偏差，使 Chrome 完全符合官方 WebGPU 标准。

### Deprecate bgra8unorm read-only storage texture usage

#### What's New
Chrome 140 弃用了在 WebGPU 中对只读存储纹理使用 `"bgra8unorm"` 格式。此格式将不再支持只读存储纹理操作，修正了之前的实现错误。

#### Technical Details
尽管 WebGPU 规范明确禁止此用法，但在早期 Chrome 版本中错误地允许了 `bgra8unorm` 格式用于只读存储纹理。此格式专门设计用于只写访问模式，缺乏跨不同 GPU 架构进行读取操作所需的可移植性特征。此弃用确保 Chrome 的 WebGPU 实现严格遵守规范要求。

#### Use Cases
使用 WebGPU 存储纹理的开发者应该从只读操作中迁移出 `bgra8unorm` 格式。此更改主要影响：
- 从存储纹理读取的 GPU 计算着色器
- 使用存储纹理进行数据采样的图形管线
- 需要一致行为的跨平台 WebGPU 应用程序

此弃用为开发者提供了时间来更新代码，然后该功能将在未来版本中完全移除。

#### References
- [issue 427681156](https://issues.chromium.org/issues/427681156)