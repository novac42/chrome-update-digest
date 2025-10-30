# Graphics and WebGPU - Chrome 142



## Texture format support capabilities extended

The new[ "texture-formats-tier1"](https://gpuweb.github.io/gpuweb/#texture-formats-tier1) GPU feature lets developers port existing content to the web without needing to rewrite it for WebGPU's lower capabilities. It supports new `"r16unorm"`, `"r16snorm"`, `"rg16unorm"`, `"rg16snorm"`, `"rgba16unorm"`, and `"rgba16snorm"` texture formats with render attachment, blendable, multisampling capabilities and `"read-only"` or `"write-only"` storage texture access. It also allows existing `"r8snorm"`, `"rg8snorm"`, `"rgba8snorm"` texture formats with render attachment, blendable, multisampling and resolve capabilities. More texture formats can also be used with `"read-only"` or `"write-only"` storage texture access.

The new[ "texture-formats-tier2"](https://gpuweb.github.io/gpuweb/#texture-formats-tier2) GPU feature enables `"read-write"` storage texture access for specific formats, crucial for projects like porting Unreal Engine to the web. Note that enabling `"texture-formats-tier2"` at device creation automatically enables `"texture-formats-tier1"`.

See the following snippet and [chromestatus entry](https://chromestatus.com/feature/5116926821007360).
    
    
    const adapter = await navigator.gpu.requestAdapter();
    
    const requiredFeatures = [];
    if (adapter.features.has("texture-format-tier1")) {
      requiredFeatures.push("texture-format-tier1");
    }
    if (adapter.features.has("texture-format-tier2")) {
      requiredFeatures.push("texture-format-tier2");
    }
    const device = await adapter.requestDevice({ requiredFeatures });
    
    // Later on, when dealing with "r8unorm" texture formats for example...
    if (device.features.has("texture-format-tier2")) {
      // Use "read-write" storage texture access...
    } else if (device.features.has("texture-format-tier1")) {
      // Use "read-only" or "write-only" storage texture access...
    } else {
      // Fallback: Use another texture format...
    }
    

Big thanks to the Intel folks for their work!


## Primitive index in WGSL

The [`primitive_index`](https://gpuweb.github.io/gpuweb/wgsl/#built-in-values-primitive_index) is a built-in WGSL value that uniquely identifies the current primitive (for example, a point, line, or triangle) being processed by a fragment shader. It begins at 0, increments by 1 after every primitive is processed, and resets to 0 between each instance drawn.

When the `"primitive-index"` feature is available in a GPUAdapter, request a GPUDevice with this feature to get primitive index support in WGSL, and explicitly enable this extension in your WGSL code with `enable primitive_index;`. Once enabled, use the `primitive_index` built-in integer value in your fragment shader to access per-primitive data or perform logic that varies for each distinct geometric shape being rendered for example.

The following code snippet shows a fragment shader that renders the second primitive in red, and all other primitives in blue.
    
    
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter.features.has("primitive-index")) {
      throw new Error("Primitive index support is not available");
    }
    // Explicitly request primitive index support.
    const device = await adapter.requestDevice({
      requiredFeatures: ["primitive-index"],
    });
    
    const fragmentShaderModule = device.createShaderModule({ code: `
      enable primitive_index;
    
      @fragment
      fn main(@builtin(primitive_index) i : u32) -> @location(0) vec4f {
        if (i == 1) {
          return vec4f(1, 0, 0, 1);
        }
        return vec4f(0, 1, 0, 1);
      }`,
    });
    // Send the appropriate commands to the GPU...
    

Explore more by checking out the [Primitive Picking sample](https://webgpu.github.io/webgpu-samples/?sample=primitivePicking), and see the [chromestatus entry](https://chromestatus.com/feature/6467722716250112).

![The 3D teapot model triangles are colored based on their primitive index values.](/static/blog/new-in-webgpu-142/image/primitive-picking-sample.png) The Primitive Picking sample in "primitive indexes" mode.


## Dawn updates

The `DAWN_BUILD_MONOLITHIC_LIBRARY` CMake variable used to handle the type of monolithic library to build has changed its default value from `OFF` to `STATIC` such that, by default the `libwebgpu*` files will be generated.

Dawn now handles properly `wgpu::PresentMode::Undefined` defaulting when configuring a `wgpu::Surface`. See [issue 441410668](https://issues.chromium.org/issues/441410668).

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7390..chromium/7444?n=1000).