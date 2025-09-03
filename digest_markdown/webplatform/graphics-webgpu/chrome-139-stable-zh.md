````markdown
digest_markdown/webplatform/Graphics and WebGPU/chrome-139-stable-zh.md

---

# Chrome 139 Graphics and WebGPU 更新摘要

## 1. 执行摘要

Chrome 139 在图形和 WebGPU 领域带来了重要进展，尤其通过兼容模式扩展了 WebGPU 的适用范围，新增了对 3D 纹理压缩格式（BC 和 ASTC）的支持，并优化了适配器和设备的核心特性信号。这些更新提升了跨设备图形能力，改善了开发者体验，并为现代 GPU 加速 Web 应用的广泛采用奠定了基础。

## 2. 关键影响

### 技术影响

- **更广泛的设备支持**：WebGPU 兼容模式允许应用在较旧的硬件和图形 API（OpenGL、Direct3D11）上运行，扩大了潜在用户群。
- **高级纹理压缩**：支持 BC 和 ASTC 压缩的 3D 纹理，有助于在复杂场景中更高效地利用内存并提升渲染质量。
- **特性检测与限制**：引入 `core-features-and-limits`，为查询设备能力提供标准化方式，提高了可靠性和可移植性。
- **API 一致性**：Dawn（WebGPU 实现）的更新提升了回调一致性和共享内存处理，减少了集成障碍。

### 新能力

- 可选启用旧版图形 API 的兼容模式。
- 高效的 3D 纹理压缩，适用于高级渲染。
- 明确标识 WebGPU 核心特性与限制。

### 技术债务考量

- 依赖现代 GPU API 的应用需考虑兼容性约束，以及在旧设备上的特性限制。
- 应规划兼容模式下弃用或受限特性的迁移路径。

## 3. 风险评估

### 关键风险

- **破坏性更改**：启用兼容模式会施加 API 限制；不符合要求的代码可能在旧设备上无法运行。
- **安全考量**：扩展硬件支持会增加攻击面；需确保 GPU 操作的验证和沙箱机制健全。

### 中等风险

- **弃用**：随着兼容模式成熟，旧版 API 可能逐步淘汰；需关注未来的弃用动态。
- **性能影响**：在旧硬件或 API 上运行可能导致性能下降或特性受限。

## 4. 推荐措施

### 立即行动

- 在 Chrome 139 中启用“Experimental Web Platform Features”以试用 WebGPU 兼容模式。
- 更新特性检测逻辑，采用 `core-features-and-limits`。
- 使用 BC 和 ASTC 格式测试 3D 纹理压缩流程。

### 短期规划

- 重构代码库，以优雅应对兼容模式约束。
- 关注 Dawn 更新，集成回调和消息处理改进。
- 为不支持现代 GPU 的设备准备降级策略。

### 长期策略

- 跟踪兼容模式发展，规划逐步迁移离开旧版 API。
- 投资跨平台测试基础设施，确保图形性能一致。
- 向 WebGPU 规范提案和 Chromium 跟踪问题反馈建议。

## 5. 特性分析

---

### 3D texture support for BC and ASTC compressed formats（3D 纹理支持 BC 和 ASTC 压缩格式）

**影响级别**：🟡 重要

**变更内容**：
`"texture-compression-bc-sliced-3d"` 和 `"texture-compression-astc-sliced-3d"` WebGPU 特性新增了对使用块压缩（BC）和自适应可扩展纹理压缩（ASTC）格式的 3D 纹理支持。这使得体积和复杂 3D 场景能够高效压缩。

**重要原因**：
高效的 3D 纹理压缩可降低内存和带宽消耗，带来更丰富的视觉体验和更优性能，尤其适用于科学可视化、游戏和高级渲染。

**实施建议**：
- 更新资源管线以生成 BC/ASTC 压缩的 3D 纹理。
- 测试渲染路径的兼容性和视觉效果。
- 部署前验证目标设备的支持情况。

**参考资料**：
- [Volume Rendering - Texture 3D WebGPU sample](https://webgpu.github.io/webgpu-samples/?sample=volumeRenderingTexture3D)
- [chromestatus entry](https://chromestatus.com/feature/5080855386783744)

---

### New "core-features-and-limits" feature（新增 "core-features-and-limits" 特性）

**影响级别**：🟡 重要

**变更内容**：
WebGPU 兼容模式引入了新的 `"core-features-and-limits"` 特性，表明适配器或设备支持 WebGPU 规范的核心特性和限制。

**重要原因**：
该特性标准化了特性检测流程，使开发者能够可靠地查询设备能力，并据此调整应用行为。

**实施建议**：
- 使用 `core-features-and-limits` 控制高级特性和降级逻辑。
- 在资源分配前确保进行兼容性检查。

**参考资料**：
- [explainer](https://gist.github.com/greggman/0dea9995e33393c546a4c2bd2a12e50e)
- [issue 418025721](https://issues.chromium.org/issues/418025721)

---

### Origin trial for WebGPU compatibility mode（WebGPU 兼容模式的 Origin Trial）

**影响级别**：🔴 关键

**变更内容**：
WebGPU 兼容模式现可通过 origin trial 启用，使 WebGPU 应用能够在不支持现代图形 API（如 Vulkan、Metal、Direct3D 12）的设备上运行。

**重要原因**：
此举极大扩展了 WebGPU 应用的覆盖范围，包括较旧的 Windows 和 Android 设备。

**实施建议**：
- 注册 origin trial 以在生产环境启用兼容模式。
- 审查兼容性约束并调整应用逻辑。
- 关注用户反馈和设备覆盖情况。

**参考资料**：
- [requestAdapter()](https://developer.mozilla.org/docs/Web/API/GPU/requestAdapter)
- [minor adjustments](https://webgpufundamentals.org/webgpu/lessons/webgpu-compatibility-mode.html)
- [Generate Mipmap WebGPU sample](https://webgpu.github.io/webgpu-samples/?sample=generateMipmap)

---

### Enable the feature（启用该特性）

**影响级别**：🟡 重要

**变更内容**：
WebGPU 兼容模式在 Chrome 139 中默认未启用，可通过“Experimental Web Platform Features”标志在本地激活。

**重要原因**：
开发者可在广泛部署前测试和验证兼容模式，提前做好应对未来变更的准备。

**实施建议**：
- 在开发环境中启用该标志。
- 在兼容模式约束下验证应用行为。

**参考资料**：
- [WebGPU compatibility mode](https://chromestatus.com/feature/6436406437871616)

---

### Dawn updates（Dawn 更新）

**影响级别**：🟢 可选优化

**变更内容**：
`WGPUQueueWorkDoneCallback` 函数新增了 `message` 参数以提升一致性。链接 emdawnwebgpu 并使用 `-sSHARED_MEMORY` 时，共享内存处理得到改进。

**重要原因**：
更一致的回调和内存管理可减少集成错误，提升开发体验。

**实施建议**：
- 更新回调实现以处理新的 `message` 参数。
- 检查 WebGPU 集成中的共享内存使用情况。

**参考资料**：
- [webgpu-headers PR](https://github.com/webgpu-native/webgpu-headers/pull/528)
- [Dawn CL 244075](https://dawn-review.googlesource.com/c/dawn/+/244075)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7204..chromium/7258?n=1000)

---

### WebGPU compatibility mode（WebGPU 兼容模式）

**影响级别**：🔴 关键

**变更内容**：
引入了可选的 WebGPU API 受限子集，可在旧版图形 API（OpenGL、Direct3D11）上运行，扩展了应用对旧设备的支持。

**重要原因**：
使 WebGPU 应用能够在更多设备上运行，减少碎片化，提升可访问性。

**实施建议**：
- 启用兼容模式并遵循其 API 约束。
- 检查代码是否符合受限特性要求。
- 跟踪规范和实现的最新变更。

**参考资料**：
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/1489002626799370241)
- [Tracking bug #40266903](https://issues.chromium.org/issues/40266903)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6436406437871616)
- [Spec](https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md)

---

### WebGPU `core-features-and-limits`（WebGPU `core-features-and-limits`）

**影响级别**：🟡 重要

**变更内容**：
`core-features-and-limits` 特性表明 WebGPU 适配器和设备支持规范的核心特性和限制。

**重要原因**：
为特性检测提供可靠机制，提升跨设备兼容性，减少运行时错误。

**实施建议**：
- 在初始化流程中集成特性检测。
- 参考官方规范和跟踪问题获取最新信息。

**参考资料**：
- [Tracking bug #418025721](https://issues.chromium.org/issues/418025721)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4744775089258496)
- [Spec](https://gpuweb.github.io/gpuweb/#core-features-and-limits)

---
````