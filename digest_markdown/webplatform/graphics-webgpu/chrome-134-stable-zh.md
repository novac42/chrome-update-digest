## 领域摘要

Chrome 134 (stable) 专注于推进 WebGPU 能力和运行时正确性：新增的 subgroups 功能启用 SIMD 级并行，能更高效地进行跨线程数学运算；修正了浮点纹理的可混合性处理；Dawn 实现更新了操作系统和 API 要求。对开发者影响最显著的是 subgroups 支持，它可以显著提升 GPU 上的机器学习与并行计算内核性能。浮点纹理可混合性修复消除了在明确要求 "float32-blendable" 功能存在时的不正确行为，从而改善渲染正确性。Dawn 更新收紧了平台要求并现代化了 WGSLLanguage 功能 API，影响原生构建和着色器工具链。

## 详细更新

Below are the Graphics and WebGPU area updates from Chrome 134 that follow directly from the summary above.

### Improve machine-learning workloads with subgroups（使用 subgroups 提升机器学习工作负载）

#### 新增内容
经过一年的开发和试验，subgroups WebGPU 功能（启用 SIMD 级并行）现已可用。它允许工作组内的线程进行通信并执行集合数学运算，例如计算数值之和。

#### 技术细节
Subgroups 在 WGSL 层暴露跨线程的集合操作（包括 subgroup 和 quad 的内置函数），相较于在内核中模拟 SIMD，可实现更细粒度的并行并减少同步开销。

#### 适用场景
- 需要快速归约、扫描或其他集合数学运算的机器学习内核。
- 受益于 SIMD 风格通信的高吞吐量计算着色器。
- 在不改变宿主端并行策略的情况下优化 GPU 计算性能。

#### 参考资料
- [原始提案](https://github.com/gpuweb/gpuweb/blob/main/proposals/subgroups.md)
- [Chromestatus 条目](https://chromestatus.com/feature/5126409856221184)
- [origin trial（实验）](https://developer.chrome.com/origintrials/#/view_trial/4130363808252166145)
- [subgroup 内置函数](https://gpuweb.github.io/gpuweb/wgsl/#subgroup-builtin-functions)
- [quad 内置函数](https://gpuweb.github.io/gpuweb/wgsl/#quad-builtin-functions)
- [quad](https://gpuweb.github.io/gpuweb/wgsl/#quad)
- [WebGPU subgroups 示例](https://codepen.io/web-dot-dev/pen/emOqWQJ)

### Remove float filterable texture types support as blendable（移除将可滤波浮点纹理视为可混合的支持）

#### 新增内容
随着 [32 位浮点纹理混合](/blog/new-in-webgpu-132#32-bit_float_textures_blending) 与 "float32-blendable" 功能可用，先前将可滤波浮点纹理错误地视为可混合的支持已被移除。

#### 技术细节
此更改强制对可混合浮点纹理格式使用正确的功能门控行为，避免在需要显式 float32-blendable 能力时出现隐含或错误的混合假设。

#### 适用场景
- 依赖错误混合可用性行为的渲染管线和合成现在会遵循显式的能力检查。
- 开发者应在适当的功能门控下使用浮点混合，而不应假设可滤波浮点纹理默认可混合。

#### 参考资料
- [问题 364987733](https://issues.chromium.org/issues/364987733)

### Dawn updates（Dawn 更新）

#### 新增内容
Dawn 现在要求 macOS 11 和 iOS 14，并且仅支持 Metal 2.3+。`wgpu::Instance` 的 `GetWGSLLanguageFeatures()` 方法取代了 `EnumerateWGSLLanguageFeatures()`。

#### 技术细节
- 平台最低要求更新为较新的 macOS/iOS 版本和 Metal 2.3+，这影响使用 Dawn 的原生构建所支持的硬件和操作系统目标。
- Dawn C++ 封装的 API 更改调整了 WGSLLanguage 功能发现的查询方式，使用旧的 Enumerate 方法的代码需要修改。

#### 适用场景
- 嵌入 Dawn 的原生应用和浏览器移植需要对齐构建目标并更新代码以使用新的 WGSLLanguage 功能 API。
- 着色器工具链和构建脚本应验证与更新后的 Metal 和操作系统要求的兼容性。

#### 参考资料
- [问题 381117827](https://crbug.com/381117827)
- [问题 368672124](https://issues.chromium.org/issues/368672124)
- [问题 377820810](https://issues.chromium.org/issues/377820810)
- [提交列表](https://dawn.googlesource.com/dawn/+log/chromium/6943..chromium/6998?n=1000)

将此摘要保存为：
```text
digest_markdown/webplatform/Graphics and WebGPU/chrome-134-stable-en.md
```