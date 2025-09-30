---
layout: default
title: chrome-139-zh
---

## 领域摘要

Chrome 139 在 Graphics 和 WebGPU 方面的更新侧重于扩展 WebGPU 的能力和互操作性：支持压缩的 3D 纹理（BC/ASTC）、一个用于兼容性协商的新 "core-features-and-limits" 能力、一个用于在兼容性模式下扩大设备覆盖范围的 origin trial，以及对 Dawn 的上游更改。对开发者影响最大的要点是体积/3D 纹理的运行时性能和内存效率改进、用于适配器/设备选择的更清晰能力协商，以及可提前访问的兼容性模式以覆盖较旧设备。总体来说，这些进展降低了 GPU 工作负载的带宽和内存成本，并为基于 WebGPU 的应用提供了更清晰的特性检测和迁移路径。

## 详细更新

下面是本次发布中每个 Graphics 和 WebGPU 功能的简要、面向开发者的摘要。

### 3D texture support for BC and ASTC compressed formats（支持 BC 和 ASTC 压缩格式的 3D 纹理）

#### 新增内容
"texture-compression-bc-sliced-3d" 和 "texture-compression-astc-sliced-3d" WebGPU 功能增加了对使用 BC 和 ASTC 块压缩格式的 3D 纹理的支持，从而使体积数据在 GPU 上的内存使用更高效。

#### 技术细节
通过 WebGPU 功能标志为 texture3D 资源启用 BC 和 ASTC 块压缩，允许支持这些格式的驱动和实现将其暴露给应用程序。

#### 适用场景
体积渲染、医学成像、体积效果，以及任何从 3D 纹理的内存和带宽减少中受益的 GPU 工作负载。

#### 参考资料
- [体积渲染 - Texture 3D WebGPU 示例](https://webgpu.github.io/webgpu-samples/?sample=volumeRenderingTexture3D)  
- [chromestatus 条目](https://chromestatus.com/feature/5080855386783744)

### New "core-features-and-limits" feature（新 "core-features-and-limits" 功能）

#### 新增内容
引入了一个 "core-features-and-limits" 功能，供即将推出的 WebGPU 兼容性模式使用，以表明某个适配器或设备支持 WebGPU 规范定义的核心特性和限制。

#### 技术细节
这是一个由适配器/设备报告的 capability 标志，用于表明符合规范的核心特性集和限制；在实现与 WebGPU API 表面之间进行兼容性协商时很有用。

#### 适用场景
需要在实现间保持稳定基线 WebGPU 功能的库和引擎的特性检测与能力协商。

#### 参考资料
- [说明](https://gist.github.com/greggman/0dea9995e33393c546a4c2bd2a12e50e)  
- [问题 418025721](https://issues.chromium.org/issues/418025721)

### Origin trial for WebGPU compatibility mode（WebGPU 兼容性模式的 origin trial）

#### 新增内容
一个暴露 WebGPU 兼容性模式的 origin trial，旨在通过提供以兼容性为导向的执行路径来覆盖缺乏现代本地图形 API 的设备。

#### 技术细节
origin trial 允许开发者在源上选择加入以启用 WebGPU 兼容性模式，便于在该特性评估期间扩大可以运行 WebGPU 内容的设备集合。

#### 适用场景
需要覆盖更广设备人群、评估兼容性行为并在全面平台启用前生成反馈的网站的渐进式推出。

#### 参考资料
- [requestAdapter()](https://developer.mozilla.org/docs/Web/API/GPU/requestAdapter)  
- [小幅调整](https://webgpufundamentals.org/webgpu/lessons/webgpu-compatibility-mode.html)  
- [Generate Mipmap WebGPU 示例](https://webgpu.github.io/webgpu-samples/?sample=generateMipmap)

### Dawn updates（Dawn 更新）

#### 新增内容
与 Dawn 相关的更改包括为 `WGPUQueueWorkDoneCallback` 添加一个 `message` 参数以与其他接受状态的回调保持一致，以及当 emdawnwebgpu 与 `-sSHARED_MEMORY` 链接时的构建/运行时调整。

#### 技术细节
API 头文件和 Dawn 的 CL 更新调整了回调签名并解决了 emscripten/shared-memory 构建交互；Dawn Chromium 分支中有一系列提交随这些更改一起发布。

#### 适用场景
库和引擎维护者在更新本地/网页绑定以匹配头文件/API 更改，并在以共享内存配置构建基于 Dawn 的 WebGPU 后端时确保行为正确。

#### 参考资料
- [webgpu-headers PR](https://github.com/webgpu-native/webgpu-headers/pull/528)  
- [Dawn CL 244075](https://dawn-review.googlesource.com/c/dawn/+/244075)  
- [提交列表](https://dawn.googlesource.com/dawn/+log/chromium/7204..chromium/7258?n=1000)

## 领域专门知识说明

- graphics-webgpu: 压缩的 3D 纹理支持直接减少了体积工作负载的 GPU 内存和带宽——这对实时渲染和内存受限的移动设备尤为重要。  
- webapi: "core-features-and-limits" 标志简化了适配器选择的能力检测和优雅回退。  
- devices: origin trial 通过启用兼容性路径来针对设备碎片化，从而覆盖较旧的 GPU 或操作系统 API 级别。  
- performance: 块压缩的 3D 纹理和与规范对齐的特性协商都能推动可预测的性能和更低的资源使用。  
- webassembly / javascript / engines: Dawn 和头文件的更新要求引擎作者和绑定在面向 emscripten/shared-memory 配置时对签名和构建标志进行对齐。  
- security-privacy, pwa-service-worker, multimedia, css, deprecations: 通过 origin trial 和 Chromestatus 条目监控平台推出，以规划渐进增强和迁移策略。

已保存到：digest_markdown/webplatform/Graphics and WebGPU/chrome-139-stable-en.md
