# Chrome 143 Graphics and WebGPU Updates

## Area Summary

Chrome 143 brings important enhancements to WebGPU that improve texture manipulation flexibility and address platform compatibility issues. The headline feature is texture component swizzle, which gives developers fine-grained control over how texture color channels are accessed in shaders, enabling efficient reuse of single-channel textures for grayscale effects and other creative applications. This release also removes the non-portable `bgra8unorm` format from read-only storage textures, following through on the deprecation announced in Chrome 140 and ensuring better cross-platform consistency. The Dawn rendering backend receives a critical validation fix for 3D texture clearing on Vulkan, demonstrating continued refinement of the underlying graphics infrastructure.

## Detailed Updates

Chrome 143 introduces three key updates that enhance WebGPU's texture handling capabilities while improving platform compatibility and fixing critical rendering bugs.

### Texture Component Swizzle

#### What's New

WebGPU now supports texture component swizzle, allowing developers to rearrange or replace color components from a texture's red, green, blue, and alpha channels when accessed by a shader. This feature enables creative reuse of texture data without requiring texture duplication or format conversion.

#### Technical Details

When the `"texture-component-swizzle"` feature is available in a GPUAdapter, developers can request a GPUDevice with this feature and create a GPUTextureView by calling `createView()` with a new `swizzle` option. The swizzle value is a four-character string, with each character mapping to the view's red, green, blue, and alpha components respectively.

Each character can be:
- `"r"`: Take its value from the red channel of the texture
- `"g"`: Take its value from the green channel of the texture
- `"b"`: Take its value from the blue channel of the texture
- `"a"`: Take its value from the alpha channel of the texture
- `"0"`: Force its value to 0
- `"1"`: Force its value to 1

#### Use Cases

A common use case is converting single-channel textures (like grayscale images) into viewable RGB textures without data duplication. By using a swizzle pattern like `"rrr1"`, developers can map a red-channel-only texture to all three color channels while forcing the alpha to 1, creating a grayscale image that shaders can process efficiently.

```javascript
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
```

#### References

- [Texture component swizzle specification](https://gpuweb.github.io/gpuweb/#dom-gpufeaturename-texture-component-swizzle)
- [ChromeStatus entry](https://chromestatus.com/feature/5110223547269120)

### Remove bgra8unorm Read-Only Storage Texture Usage

#### What's New

The `"bgra8unorm"` format is no longer allowed for read-only storage textures. This change enforces the WebGPU specification and removes a non-portable implementation bug that existed in Chrome.

#### Technical Details

The WebGPU specification explicitly disallows using the `"bgra8unorm"` format with read-only storage textures. Chrome previously allowed this usage as a bug, but this format is intended exclusively for write-only access and is not portable across all GPU implementations. Developers who were using this format for read-only storage textures will need to migrate to a supported format.

#### Use Cases

This change primarily impacts developers who were relying on the previously allowed (but non-standard) behavior. The removal ensures that WebGPU applications behave consistently across different browsers and GPU hardware, preventing code that works in Chrome but fails on other platforms.

#### References

- [Previous announcement in Chrome 140](https://developer.chrome.com/blog/new-in-webgpu-140#deprecate_bgra8unorm_read-only_storage_texture_usage)
- [Issue 427681156](https://issues.chromium.org/issues/427681156)

### Dawn Updates

#### What's New

Dawn, Chrome's implementation of WebGPU, receives an important bug fix for 3D texture clearing operations on Vulkan-based systems.

#### Technical Details

A validation error that was incorrectly raised when clearing 3D textures in Vulkan has been resolved. This fix ensures that legitimate 3D texture operations are not blocked by spurious validation errors, improving the reliability of WebGPU rendering on Vulkan-based platforms (including many Linux systems and Android devices).

#### Use Cases

This fix is critical for developers working with 3D textures (volume textures) in WebGPU applications, particularly those targeting platforms that use Vulkan as the underlying graphics API. Applications that perform 3D texture clearing operations will now work correctly without encountering validation errors.

#### References

- [Issue 443950688](https://issues.chromium.org/issues/443950688)
- [Full list of Dawn commits](https://dawn.googlesource.com/dawn/+log/chromium/7444..chromium/7499?n=1000)
