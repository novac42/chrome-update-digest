---
layout: default
title: Chrome 144 图形和 WebGPU 更新
---

# Chrome 144 图形和 WebGPU 更新

## 领域摘要

Chrome 144 为 WebGPU 带来了两项强大的新 WGSL 语言扩展，显著增强了内存管理灵活性和工作组编程能力。`subgroup_id` 扩展通过提供对工作组内子组标识符的直接访问，实现了更高效的子组级操作，而 `uniform_buffer_standard_layout` 则简化了统一缓冲区和存储缓冲区之间的数据结构共享。此版本还标志着一个重要里程碑，WebGPU 支持扩展到配备 Intel Gen12+ GPU 的 Linux 系统，同时数据传输操作的性能得到大幅提升。这些更新共同巩固了 WebGPU 作为 Web 平台现代高性能图形和计算 API 的地位。

## 详细更新

Chrome 144 引入了五项主要改进，涵盖 WebGPU 语言特性、平台支持和性能优化，增强了开发者能力和应用效率。

### WGSL subgroup_id extension

#### 新增内容

`subgroup_id` WGSL 语言扩展为工作组编程引入了两个新的内置值：`subgroup_id` 和 `num_subgroups`。当启用 `subgroups` 扩展时，这些内置值提供对子组标识信息的直接访问。

#### 技术细节

该扩展提供：
- `subgroup_id`：返回当前工作组中某个调用的子组 ID
- `num_subgroups`：报告工作组中存在的子组总数

这消除了之前通过[原子操作](https://gpuweb.github.io/gpuweb/wgsl/#atomic-types)重建子组 ID 以避免重叠内存访问的要求。当使用子组调用 ID 索引内存时，开发者现在可以直接使用 `subgroup_id` 进行更直接的内存管理。该功能在尚不支持原生功能的 D3D 后端上进行模拟，其等价于 `local_invocation_index` 为 `subgroup_invocation_id + subgroup_size * subgroup_id`。请注意，在某些情况下子组可能并不总是满的。

#### 适用场景

可以使用 `navigator.gpu.wgslLanguageFeatures` 进行特性检测。开发者应在 WGSL 着色器代码顶部使用 requires 指令 `requires subgroup_id;` 来标识潜在的不可移植性。使用示例：

```javascript
if (!navigator.gpu.wgslLanguageFeatures.has("subgroup_id")) {
  throw new Error(`WGSL subgroup_id and num_subgroups built-in values are not available`);
}

const adapter = await navigator.gpu.requestAdapter();
if (!adapter.features.has("subgroups")) {
  throw new Error("Subgroups support is not available");
}
const device = await adapter.requestDevice({ requiredFeatures: ["subgroups"] });

const shaderModule = device.createShaderModule({ code: `
  enable subgroups;
  requires subgroup_id;

  @compute @workgroup_size(64, 1, 1)
  fn main(@builtin(subgroup_id) subgroup_id : u32,
          @builtin(num_subgroups) num_subgroups : u32) {
    // TODO: Use subgroup_id and num_subgroups values.
  }`,
});
```

#### 参考资料

- [Intent to ship](https://groups.google.com/a/chromium.org/g/blink-dev/c/SV75BHCUJz0/m/_Ihj4GRCBQAJ)

### WGSL uniform_buffer_standard_layout extension

#### 新增内容

`uniform_buffer_standard_layout` WGSL 语言扩展允许统一缓冲区使用与存储缓冲区相同的内存布局约束，显著简化了两种缓冲区类型之间的数据结构共享。

#### 技术细节

此扩展消除了之前统一缓冲区必须在数组元素上使用 16 字节对齐以及将嵌套结构偏移量填充到 16 字节倍数的要求。启用标准布局后，统一缓冲区可以使用与存储缓冲区约定匹配的更紧凑的内存布局，减少了手动填充或对齐属性的需求。

#### 适用场景

可以使用 `navigator.gpu.wgslLanguageFeatures` 进行特性检测。在 WGSL 着色器代码顶部使用 requires 指令 `requires uniform_buffer_standard_layout;` 来标识潜在的不可移植性。使用示例：

```javascript
if (!navigator.gpu.wgslLanguageFeatures.has("uniform_buffer_standard_layout")) {
  throw new Error(`WGSL uniform buffer standard layout is not available`);
}

const adapter = await navigator.gpu.requestAdapter();
const device = await adapter.requestDevice();

const shaderModule = device.createShaderModule({ code: `
  requires uniform_buffer_standard_layout;

  struct S {
      x: f32
  }
  struct Uniforms {
      a: S,
      b: f32
      // b is at offset 4. Without standard layout, alignment rules would
      // force b to be at offset 16 (or a multiple of 16), and you would have
      // to add extra fields or use an @align attribute.
  }

  @group(0) @binding(0) var<uniform> u: Uniforms;

  @fragment fn fs_main() -> @location(0) vec4<f32> {
      return vec4<f32>(u.a.x);
  }`,
});
```

#### 参考资料

- [Intent to ship](https://groups.google.com/a/chromium.org/g/blink-dev/c/Ww2eL6b74V0/m/D8AT9DWlAQAJ)

### WebGPU on Linux

#### 新增内容

WebGPU 支持正在向 Linux 系统推出，首先支持 Intel Gen12+ GPU，并初步计划扩展对 AMD 和 NVIDIA 设备的支持。

#### 技术细节

该实现采用一种架构，其中 WebGPU 利用 Vulkan，而 Chromium 的其余部分继续使用 OpenGL。这种方法采用了现有的成熟且经过验证的代码路径，在确保稳定性的同时在 Linux 平台上启用现代 GPU 能力。

#### 适用场景

使用 Intel Gen12+ GPU 的 Linux 开发者和用户现在可以访问 WebGPU 功能进行图形和计算工作负载。此扩展为 Linux 生态系统带来了现代 GPU API 能力，支持跨平台 WebGPU 应用开发。

#### 参考资料

- [问题 442791440](https://issues.chromium.org/issues/442791440)

### Faster writeBuffer and writeTexture

#### 新增内容

Chrome 144 为 `writeBuffer()` 和 `writeTexture()` 操作提供了显著的性能优化，与之前版本相比实现了高达 2 倍的性能提升。

#### 技术细节

优化改进因传输数据的大小而异。这些增强影响 [Dawn Wire](https://dawn.googlesource.com/dawn/+/HEAD/docs/dawn/overview.md#dawn-wire) 实现的所有用户，全面提高了数据传输效率。

#### 适用场景

频繁更新 GPU 缓冲区或纹理的应用将立即获得性能优势，特别是那些具有大量数据传输需求的应用。此优化减少了流式纹理更新、动态缓冲区修改和实时数据可视化等场景中的开销。

#### 参考资料

- [问题 441900745](https://issues.chromium.org/issues/441900745)

### Dawn updates

#### 新增内容

Android GPU 团队通过 Jetpack 发布了 Android 上 WebGPU 的 [首个 alpha 版本](https://developer.android.com/jetpack/androidx/releases/webgpu) Kotlin 绑定。

#### 技术细节

`androidx.webgpu` 包为 Android 开发者提供了使用 Kotlin 访问现代 GPU API 能力的途径，避开了 OpenGL 的遗留问题和 Vulkan 的复杂性。这代表了 WebGPU 生态系统的重大发展，将其覆盖范围从 Web 浏览器扩展到原生 Android 应用。

#### 适用场景

Android 开发者现在可以使用熟悉的 Kotlin 语法直接在原生应用中利用 WebGPU 的现代图形和计算能力，而无需处理 OpenGL 的限制或 Vulkan 的陡峭学习曲线。这为 Android 上的高性能图形和计算应用开辟了新的可能性。

#### 参考资料

- [提交列表](https://dawn.googlesource.com/dawn/+log/chromium/7499..chromium/7559?n=1000)
