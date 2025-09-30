## 区域摘要

Chrome 140（稳定版）通过弃用在只读存储纹理中使用 "bgra8unorm" 来收紧 WebGPU 存储纹理的行为。对开发者影响最大的是，依赖该先前允许模式的现有代码需要为可移植性和规范合规性而更新。此举使 Chrome 与 WebGPU 规范保持一致，减少平台不一致性和意外行为。那些更新提高了跨平台图形的可靠性，并降低了 GPU 加速 Web 应用中出现微妙渲染或兼容性错误的风险。

## 详细更新

本节将摘要扩展为 Chrome 140 中的单个与存储相关的更改以及开发者应注意的事项。

### Deprecate bgra8unorm read-only storage texture usage（弃用 bgra8unorm 的只读存储纹理用法）

#### 新增内容
在只读存储纹理中使用 "bgra8unorm" 格式在 Chrome 140 中现已被弃用。WebGPU 规范不允许这种用法；Chrome 先前的允许是一个错误。

#### 技术细节
该弃用反映了 "bgra8unorm" 旨在用于仅写访问，且在不同实现间不可移植。Chrome 的更改使其 WebGPU 行为与规范一致，以避免不可移植的使用模式。

#### 适用场景
- 依赖在只读存储纹理中使用 "bgra8unorm" 的 WebGPU 应用和着色器必须更新，以避免依赖该模式。
- 开发者应审计存储纹理的使用情况，并切换到符合规范的访问模式或显式支持读访问的替代格式，以确保在不同浏览器和 GPU 之间的可移植性。

#### 参考资料
- 问题 427681156: https://issues.chromium.org/issues/427681156

输出文件：digest_markdown/webplatform/storage/chrome-140-stable-en.md