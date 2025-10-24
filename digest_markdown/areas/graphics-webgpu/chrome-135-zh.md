---
layout: default
title: Chrome 更新分析器 – Graphics and WebGPU（Chrome 135 稳定版）
---

# Chrome 更新分析器 – Graphics and WebGPU（Chrome 135 稳定版）

## 领域摘要

Chrome 135 针对 Graphics 和 WebGPU 栈引入了多项有针对性的改进，重点提升开发者体验、标准一致性以及平台一致性。主要变化包括简化渲染管线布局的创建、在 Android 上更便捷地访问实验性 WebGPU 兼容模式，以及移除冗余的着色器限制。Dawn 实现的更新进一步明确了正确的使用模式，并使 API 结构更加现代化。这些增强措施共同简化了 GPU 编程，降低了跨平台开发的难度，并推动 WebGPU 作为核心网页图形技术的成熟与可靠性。

## 详细更新

以下是 Chrome 135 针对 Graphics 和 WebGPU 的主要更新，并为开发者提供了实用见解。

### Allow creating pipeline layout with null bind group layout（允许使用 null 绑定组布局创建管线布局）

#### 新增内容
开发者现在可以使用 null 绑定组布局创建管线布局，无需显式定义空的绑定组。

#### 技术细节
此前，空绑定组需要一个零绑定的组，过程繁琐。现在，null 绑定组布局在创建管线布局时会被直接忽略，从而简化流程并减少样板代码。

#### 适用场景
此更改简化了管线设置，尤其适用于简单着色器或逐步构建管线配置时。它降低了 WebGPU 应用中的代码复杂度和潜在错误。

#### 参考资料
- [issue 377836524](https://issues.chromium.org/issues/377836524)

---

### Easier access to the experimental compatibility mode on Android（在 Android 上更便捷地访问实验性兼容模式）

#### 新增内容
现在，`chrome://flags/#enable-unsafe-webgpu` 标志可启用 Android 上实验性 WebGPU 兼容模式所需的全部能力。

#### 技术细节
启用该标志后，开发者可直接以兼容模式请求 GPUAdapter，无需额外配置。这统一了各平台的开发体验，使在 Android 设备上测试和部署 WebGPU 功能更加便捷。

#### 适用场景
面向 Android 的开发者可以更轻松地试验和验证 WebGPU 功能，加快跨平台图形开发与测试。

#### 参考资料
- [dawn:389876644](https://issues.chromium.org/issues/389876644)
- [webgpureport.org](https://webgpureport.org)

---

### Remove maxInterStageShaderComponents limit（移除 maxInterStageShaderComponents 限制）

#### 新增内容
WebGPU 已移除 `maxInterStageShaderComponents` 限制。

#### 技术细节
该限制与 `maxInterStageShaderVariables` 重复，后者已负责管理阶段间变量数量。移除此限制简化了规范，减少了混淆，使 Chrome 与不断演进的 WebGPU 标准保持一致。

#### 适用场景
着色器作者和引擎开发者将受益于更清晰、易用且不易出错的 API，减少了需管理的重叠约束。

#### 参考资料
- [intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/i5oJu9lZPAk)
- [issue 364338810](https://issues.chromium.org/issues/364338810)

---

### Dawn updates（Dawn 实现更新）

#### 新增内容
Dawn WebGPU 实现进行了多项更新，包括对深度纹理采样器使用的更严格要求，以及限制结构的变更。

#### 技术细节
- 过滤采样器不再允许采样深度纹理，仅允许非过滤或比较采样器。
- `WGPURequiredLimits` 和 `WGPUSupportedLimits` 结构已更新，以提升清晰度和未来兼容性。
- 本次发布还包含其他错误修复和改进。

#### 适用场景
这些更改强化了正确的使用模式，防止细微的渲染错误，并确保应用持续兼容不断演进的 WebGPU 规范。

#### 参考资料
- [issue 379788112](https://issues.chromium.org/issues/379788112)
- [issue 374263404](https://issues.chromium.org/issues/374263404)
- [issue 42240793](https://issues.chromium.org/issues/42240793)
- [webgpu-headers PR](https://github.com/webgpu-native/webgpu-headers/pull/509)
- [Debugging Dawn](https://dawn.googlesource.com/dawn/+/HEAD/docs/dawn/debugging.md#tracing-native-gpu-api-usage)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/6998..chromium/7049?n=1000)

---

**文件位置：**  
`digest_markdown/webplatform/Graphics and WebGPU/chrome-135-stable-en.md`
