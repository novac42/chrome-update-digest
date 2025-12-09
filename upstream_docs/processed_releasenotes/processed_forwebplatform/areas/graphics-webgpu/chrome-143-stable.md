# Graphics and WebGPU - Chrome 143



## Texture component swizzle

It's now possible to rearrange or replace the color components from texture's red, green, blue, and alpha channels when accessed by a shader.

When the [`"texture-component-swizzle"`](https://gpuweb.github.io/gpuweb/#dom-gpufeaturename-texture-component-swizzle) feature is available in a GPUAdapter, request a GPUDevice with this feature, and create a GPUTextureView by calling `createView()` with a new `swizzle` option. This value is a string of length four, with each character mapping to the view's red, green, blue, and alpha components, respectively. Each character can be either:

  * `"r"`: Take its value from the red channel of the texture.
  * `"g"`: Take its value from the green channel of the texture.
  * `"b"`: Take its value from the blue channel of the texture.
  * `"a"`: Take its value from the alpha channel of the texture.
  * `"0"`: Force its value to 0.
  * `"1"`: Force its value to 1.

See the following snippet and [chromestatus entry](https://chromestatus.com/feature/5110223547269120).
    
    
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter.features.has("texture-component-swizzle")) {
      throw new Error("Texture component swizzle support is not available");
    }
    // Explicitly request texture component swizzle support.
    const device = await adapter.requestDevice({
      requiredFeatures: ["texture-component-swizzle"],
    });
    
    // ... Assuming myTexture is a GPUTexture with a single red channel.
    
    // Map the view's red, green, blue components to myTexture's red channel
    // and force the view's alpha component to 1 so that the shader sees it as
    // a grayscale image.
    const view = myTexture.createView({ swizzle: "rrr1" });
    
    // Send the appropriate commands to the GPU...
    


## Remove bgra8unorm read-only storage texture usage

As previously [announced](/blog/new-in-webgpu-140#deprecate_bgra8unorm_read-only_storage_texture_usage), using `"bgra8unorm"` format with read-only storage textures is now removed. The WebGPU specification explicitly disallows this, and its prior allowance in Chrome was a bug, as this format is intended for write-only access and is not portable. See [issue 427681156](https://issues.chromium.org/issues/427681156).


## Dawn updates

A validation error raised when clearing a 3D texture in Vulkan has been fixed. See issue [443950688](https://issues.chromium.org/issues/443950688)

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7444..chromium/7499?n=1000).