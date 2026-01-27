# Graphics and WebGPU - Chrome 144



## WGSL subgroup_id extension

The WGSL language extension `subgroup_id` lets you use the following new built-in values in workgroups when the `subgroups` extension is enabled:

  * `subgroup_id`: Provides the ID of an invocation's subgroup within the current workgroup.
  * `num_subgroups`: Reports the number of subgroups present in the workgroup.

Previously, to index memory using subgroup invocation IDs, you had to reconstruct a subgroup ID (typically through[ atomic operations](https://gpuweb.github.io/gpuweb/wgsl/#atomic-types)) to avoid overlapping memory accesses. You can now use `subgroup_id` to fill the other half of that equation. Because this functionality is not available on the D3D backend yet, it's emulated there. It should be safe to create an equivalence to `local_invocation_index` as `subgroup_invocation_id + subgroup_size * subgroup_id`. Note that there might be cases where subgroups are not full.

This language extension can be feature-detected using `navigator.gpu.wgslLanguageFeatures`. It's recommended to use a requires-directive to signal the potential for non-portability with `requires subgroup_id;` at the top of your WGSL shader code. See the following example and the [intent to ship](https://groups.google.com/a/chromium.org/g/blink-dev/c/SV75BHCUJz0/m/_Ihj4GRCBQAJ).
    
    
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
    


## WGSL uniform_buffer_standard_layout extension

The WGSL language extension `uniform_buffer_standard_layout` lets uniform buffers use the same memory layout constraints as storage buffers, which makes it easier to share data structures in both kinds of buffers. This means uniform buffers are no longer required to have 16-byte alignment on array elements, or to pad nested structure offsets to a multiple of 16 bytes.

This language extension can be feature-detected using `navigator.gpu.wgslLanguageFeatures`. It's recommended to use a requires-directive to signal the potential for non-portability with `requires uniform_buffer_standard_layout;` at the top of your WGSL shader code. See the following example and the [intent to ship](https://groups.google.com/a/chromium.org/g/blink-dev/c/Ww2eL6b74V0/m/D8AT9DWlAQAJ).
    
    
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
    


## WebGPU on Linux

The Chrome team is carefully rolling out WebGPU for Linux, starting with support for Intel Gen12+ GPUs but with a tentative plan to expand it to more devices (AMD, NVIDIA). This implementation uses an architecture where WebGPU uses Vulkan and the rest of Chromium stays on OpenGL, exercising existing well known good code paths. See [issue 442791440](https://issues.chromium.org/issues/442791440).


## Faster writeBuffer and writeTexture

`writeBuffer()` and `writeTexture()` have been optimized in Chrome, resulting in performance gains up to 2X better than the previous version, depending on the size of the data being transferred. This change affects all users of the [Dawn Wire](https://dawn.googlesource.com/dawn/+/HEAD/docs/dawn/overview.md#dawn-wire) implementation as well. See [issue 441900745](https://issues.chromium.org/issues/441900745).


## Dawn updates

The Android GPU team has published the [first alpha release](https://developer.android.com/jetpack/androidx/releases/webgpu) of Kotlin bindings for WebGPU on Android available using Jetpack. The `androidx.webgpu` package gives Android developers access to a modern GPU API using Kotlin, bypassing the legacy issues of OpenGL or the complexity of Vulkan—an exciting development for the ecosystem!

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7499..chromium/7559?n=1000).