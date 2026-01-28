# Chrome 143 Graphics and WebGPU 更新

## 领域摘要

Chrome 143 为 WebGPU 带来了重要的增强功能，提升了纹理操作的灵活性并解决了平台兼容性问题。主要特性是纹理组件混洗（texture component swizzle），它使开发者能够精细控制着色器如何访问纹理颜色通道，从而高效复用单通道纹理实现灰度效果和其他创意应用。此版本还从只读存储纹理中移除了不可移植的 `bgra8unorm` 格式，落实了 Chrome 140 中宣布的弃用，确保更好的跨平台一致性。Dawn 渲染后端收到了针对 Vulkan 上 3D 纹理清除的关键验证修复，展现了对底层图形基础设施的持续改进。

## 详细更新

Chrome 143 引入了三项关键更新，增强了 WebGPU 的纹理处理能力，同时提高了平台兼容性并修复了关键的渲染错误。

### Texture Component Swizzle（纹理组件混洗）

#### 新增内容

WebGPU 现在支持纹理组件混洗，允许开发者在着色器访问纹理时重新排列或替换红、绿、蓝和 alpha 通道的颜色组件。此特性使纹理数据能够创造性地复用，无需纹理复制或格式转换。

#### 技术细节

当 GPUAdapter 中提供 `"texture-component-swizzle"` 特性时，开发者可以请求具有此特性的 GPUDevice，并通过调用带有新 `swizzle` 选项的 `createView()` 来创建 GPUTextureView。swizzle 值是一个四字符字符串，每个字符分别映射到视图的红、绿、蓝和 alpha 组件。

每个字符可以是：
- `"r"`：从纹理的红色通道取值
- `"g"`：从纹理的绿色通道取值
- `"b"`：从纹理的蓝色通道取值
- `"a"`：从纹理的 alpha 通道取值
- `"0"`：强制其值为 0
- `"1"`：强制其值为 1

#### 适用场景

常见用例是将单通道纹理（如灰度图像）转换为可查看的 RGB 纹理，而无需数据复制。通过使用如 `"rrr1"` 的混洗模式，开发者可以将仅有红色通道的纹理映射到所有三个颜色通道，同时将 alpha 强制为 1，创建着色器可以高效处理的灰度图像。

```javascript
const adapter = await navigator.gpu.requestAdapter();
if (!adapter.features.has("texture-component-swizzle")) {
  throw new Error("Texture component swizzle support is not available");
}
// 显式请求纹理组件混洗支持
const device = await adapter.requestDevice({
  requiredFeatures: ["texture-component-swizzle"],
});

// ... 假设 myTexture 是一个仅有红色通道的 GPUTexture。

// 将视图的红、绿、蓝组件映射到 myTexture 的红色通道
// 并将视图的 alpha 组件强制为 1，使着色器将其视为灰度图像
const view = myTexture.createView({ swizzle: "rrr1" });

// 向 GPU 发送适当的命令...
```

#### 参考资料

- [纹理组件混洗规范](https://gpuweb.github.io/gpuweb/#dom-gpufeaturename-texture-component-swizzle)
- [ChromeStatus 条目](https://chromestatus.com/feature/5110223547269120)

### Remove bgra8unorm Read-Only Storage Texture Usage（移除 bgra8unorm 只读存储纹理用法）

#### 新增内容

`"bgra8unorm"` 格式不再允许用于只读存储纹理。此更改强制执行 WebGPU 规范，移除了 Chrome 中存在的不可移植实现错误。

#### 技术细节

WebGPU 规范明确禁止将 `"bgra8unorm"` 格式用于只读存储纹理。Chrome 之前作为错误允许了此用法，但此格式专门用于只写访问，并不能在所有 GPU 实现中移植。使用此格式进行只读存储纹理的开发者需要迁移到支持的格式。

#### 适用场景

此更改主要影响依赖先前允许（但非标准）行为的开发者。移除此功能确保 WebGPU 应用在不同浏览器和 GPU 硬件上的行为一致，防止在 Chrome 中运行但在其他平台上失败的代码。

#### 参考资料

- [Chrome 140 中的先前公告](https://developer.chrome.com/blog/new-in-webgpu-140#deprecate_bgra8unorm_read-only_storage_texture_usage)
- [问题 427681156](https://issues.chromium.org/issues/427681156)

### Dawn Updates（Dawn 更新）

#### 新增内容

Dawn（Chrome 的 WebGPU 实现）收到了针对基于 Vulkan 系统上 3D 纹理清除操作的重要错误修复。

#### 技术细节

在 Vulkan 中清除 3D 纹理时错误引发的验证错误已解决。此修复确保合法的 3D 纹理操作不会被虚假的验证错误阻止，提高了基于 Vulkan 平台（包括许多 Linux 系统和 Android 设备）上 WebGPU 渲染的可靠性。

#### 适用场景

此修复对于在 WebGPU 应用中使用 3D 纹理（体积纹理）的开发者至关重要，特别是针对使用 Vulkan 作为底层图形 API 的平台。执行 3D 纹理清除操作的应用现在可以正常工作，不会遇到验证错误。

#### 参考资料

- [问题 443950688](https://issues.chromium.org/issues/443950688)
- [Dawn 提交的完整列表](https://dawn.googlesource.com/dawn/+log/chromium/7444..chromium/7499?n=1000)
