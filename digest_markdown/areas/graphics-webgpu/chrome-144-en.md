---
layout: default
title: Chrome 144 Graphics and WebGPU Updates
---

# Chrome 144 Graphics and WebGPU Updates

## Area Summary

Chrome 144 brings significant enhancements to WebGPU with two powerful new WGSL language extensions that improve memory management flexibility and workgroup programming capabilities. The `subgroup_id` extension enables more efficient subgroup-level operations by providing direct access to subgroup identifiers within workgroups, while `uniform_buffer_standard_layout` simplifies data structure sharing between uniform and storage buffers. This release also marks an important milestone with WebGPU support expanding to Linux systems with Intel Gen12+ GPUs, alongside substantial performance improvements in data transfer operations. These updates collectively strengthen WebGPU's position as a modern, high-performance graphics and compute API for the web platform.

## Detailed Updates

Chrome 144 introduces five major improvements across WebGPU language features, platform support, and performance optimizations that enhance developer capabilities and application efficiency.

### WGSL subgroup_id extension

#### What's New

The `subgroup_id` WGSL language extension introduces two new built-in values for workgroup programming: `subgroup_id` and `num_subgroups`. These built-ins provide direct access to subgroup identification information when the `subgroups` extension is enabled.

#### Technical Details

The extension provides:
- `subgroup_id`: Returns the ID of an invocation's subgroup within the current workgroup
- `num_subgroups`: Reports the total number of subgroups present in the workgroup

This eliminates the previous requirement to reconstruct subgroup IDs through [atomic operations](https://gpuweb.github.io/gpuweb/wgsl/#atomic-types) to avoid overlapping memory accesses. When indexing memory using subgroup invocation IDs, developers can now directly use `subgroup_id` for more straightforward memory management. The functionality is emulated on the D3D backend where native support is not yet available, with an equivalence to `local_invocation_index` as `subgroup_invocation_id + subgroup_size * subgroup_id`. Note that subgroups may not always be full in certain cases.

#### Use Cases

The extension can be feature-detected using `navigator.gpu.wgslLanguageFeatures`. Developers should use the requires-directive `requires subgroup_id;` at the top of WGSL shader code to signal potential non-portability. Example usage:

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

#### References

- [Intent to ship](https://groups.google.com/a/chromium.org/g/blink-dev/c/SV75BHCUJz0/m/_Ihj4GRCBQAJ)

### WGSL uniform_buffer_standard_layout extension

#### What's New

The `uniform_buffer_standard_layout` WGSL language extension allows uniform buffers to use the same memory layout constraints as storage buffers, significantly simplifying data structure sharing between both buffer types.

#### Technical Details

This extension removes the previous requirement for uniform buffers to have 16-byte alignment on array elements and to pad nested structure offsets to multiples of 16 bytes. With standard layout enabled, uniform buffers can use more compact memory layouts that match storage buffer conventions, reducing the need for manual padding or alignment attributes.

#### Use Cases

The extension can be feature-detected using `navigator.gpu.wgslLanguageFeatures`. Use the requires-directive `requires uniform_buffer_standard_layout;` at the top of WGSL shader code to signal potential non-portability. Example usage:

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

#### References

- [Intent to ship](https://groups.google.com/a/chromium.org/g/blink-dev/c/Ww2eL6b74V0/m/D8AT9DWlAQAJ)

### WebGPU on Linux

#### What's New

WebGPU support is rolling out to Linux systems, starting with Intel Gen12+ GPUs, with tentative plans to expand support to AMD and NVIDIA devices.

#### Technical Details

The implementation uses an architecture where WebGPU leverages Vulkan while the rest of Chromium continues using OpenGL. This approach exercises existing well-known and proven code paths, ensuring stability while enabling modern GPU capabilities on Linux platforms.

#### Use Cases

Linux developers and users with Intel Gen12+ GPUs can now access WebGPU functionality for graphics and compute workloads. This expansion brings modern GPU API capabilities to the Linux ecosystem, enabling cross-platform WebGPU application development.

#### References

- [Issue 442791440](https://issues.chromium.org/issues/442791440)

### Faster writeBuffer and writeTexture

#### What's New

Chrome 144 delivers significant performance optimizations to `writeBuffer()` and `writeTexture()` operations, achieving up to 2X performance improvements compared to the previous version.

#### Technical Details

The optimization improvements vary depending on the size of data being transferred. These enhancements affect all users of the [Dawn Wire](https://dawn.googlesource.com/dawn/+/HEAD/docs/dawn/overview.md#dawn-wire) implementation, improving data transfer efficiency across the board.

#### Use Cases

Applications that frequently update GPU buffers or textures will see immediate performance benefits, particularly those with large data transfer requirements. This optimization reduces overhead in scenarios like streaming texture updates, dynamic buffer modifications, and real-time data visualization.

#### References

- [Issue 441900745](https://issues.chromium.org/issues/441900745)

### Dawn updates

#### What's New

The Android GPU team has released the [first alpha release](https://developer.android.com/jetpack/androidx/releases/webgpu) of Kotlin bindings for WebGPU on Android through Jetpack.

#### Technical Details

The `androidx.webgpu` package provides Android developers access to modern GPU API capabilities using Kotlin, bypassing the legacy issues of OpenGL and the complexity of Vulkan. This represents a significant development for the WebGPU ecosystem, extending its reach beyond web browsers to native Android applications.

#### Use Cases

Android developers can now leverage WebGPU's modern graphics and compute capabilities directly in native applications using familiar Kotlin syntax, without dealing with OpenGL's limitations or Vulkan's steep learning curve. This opens new possibilities for high-performance graphics and compute applications on Android.

#### References

- [List of commits](https://dawn.googlesource.com/dawn/+log/chromium/7499..chromium/7559?n=1000)
