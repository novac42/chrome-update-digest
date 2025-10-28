# Graphics and WebGPU - Chrome 133

## Additional unorm8x4-bgra and 1-component vertex formats

The `"unorm8x4-bgra"` vertex format and the following 1-component vertex formats have been added: `"uint8"`, `"sint8"`, `"unorm8"`, `"snorm8"`, `"uint16"`, `"sint16"`, `"unorm16"`, `"snorm16"`, and `"float16"`. The `"unorm8x4-bgra"` vertex format makes it slightly more convenient to load BGRA-encoded vertex colors while keeping the same shader. Additionally, the 1-component vertex format lets you request only the data that is necessary when previously at least twice as much was required for 8 and 16-bit data types. See the [chromestatus entry](https://chromestatus.com/feature/4609840973086720) and [issue 376924407](https://issues.chromium.org/issues/376924407).


## Allow unknown limits to be requested with undefined value

To make the WebGPU API less brittle as it evolves, you can now request unknown limits with `undefined` value when requesting a GPU device. This is useful in the following application code for example where `adapter.limits.someLimit` can be `undefined` if `someLimit` doesn't exist anymore. See [spec PR 4781](https://github.com/gpuweb/gpuweb/pull/4781).
    
    
    const adapter = await navigator.gpu.requestAdapter();
    
    const device = await adapter.requestDevice({
      requiredLimits: { someLimit: adapter.limits.someLimit }, // someLimit can be undefined
    });
    


## WGSL alignment rules changes

It is no longer possible to provide a too-small alignment value for a struct member as it is now required that `@align(n)` divides [`RequiredAlignOf`](https://gpuweb.github.io/gpuweb/wgsl/#requiredalignof) for all structs. This breaking change simplifies usage of the WGSL language and makes it more compatible with Firefox and Safari. You can find sample code showing differences between Tint, Naga, and WebKit compilers in the [spec PR](https://github.com/gpuweb/gpuweb/pull/4978).


## WGSL performance gains with discard

Due to a significant performance drop observed when rendering a complex screen-space reflections (SSR) effect, the implementation of the [discard statement](https://gpuweb.github.io/gpuweb/wgsl/#discard-statement) uses the platform-provided semantics for demoting to a helper invocation when available. This improves the performance of shaders that use discard. See [issue 372714384](https://issues.chromium.org/372714384).


## Use VideoFrame displaySize for external textures

The `displayWidth` and `displayHeight` dimensions should be used as the apparent size of the GPUExternalTexture when importing a VideoFrame according to the WebGPU spec. However the visible size was incorrectly used causing issues when trying to use `textureLoad()` on a GPUExternalTexture. This is now fixed. See [issue 377574981](https://issues.chromium.org/issues/377574981).


## Handle images with non-default orientations using copyExternalImageToTexture

The `copyExternalImageToTexture()` GPUQueue method is used to copy the contents of an image or canvas into a texture. It now properly handles images with non-default orientations. This was not the case before when the source was an ImageBitmap with `imageOrientation` [`"from-image"`](https://developer.mozilla.org/docs/Web/API/Window/createImageBitmap#from-image) or an image with a non-default orientation. See [issue 384858956](https://issues.chromium.org/issues/384858956).


## Improving developer experience

It can be surprising when `adapter.limits` shows high values, but you don't realize you need to explicitly request a higher limit when requesting a GPU device. Failing to do so can result in unexpectedly hitting limits later on.

To help you, the error messages have been expanded with hints that tell you to explicitly request a higher limit when no limit was specified in `requiredLimits` when calling `requestDevice()`. See [issue 42240683](https://issues.chromium.org/issues/42240683).

The following example shows you an improved error message logged in the DevTools console when creating a GPU buffer with a size exceeding the default max buffer size device limit.
    
    
    const adapter = await navigator.gpu.requestAdapter();
    const device = await adapter.requestDevice();
    
    // Create a GPU buffer with a size exceeding the default max buffer size device limit.
    const size = device.limits.maxBufferSize + 1;
    const buffer = device.createBuffer({ size, usage: GPUBufferUsage.MAP_READ });
    
    device.queue.submit([]);
    
    
    
    ⚠️ Buffer size (268435457) exceeds the max buffer size limit (268435456). This adapter supports a higher maxBufferSize of 4294967296, which can be specified in requiredLimits when calling requestDevice(). Limits differ by hardware, so always check the adapter limits prior to requesting a higher limit.
    - While calling [Device].CreateBuffer([BufferDescriptor]).


## Enable compatibility mode with featureLevel

Requesting a GPU adapter in the [experimental compatibility mode](https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md#webgpu-spec-changes) is now possible by setting the standardized [`featureLevel`](https://gpuweb.github.io/gpuweb/#dom-gpurequestadapteroptions-featurelevel) option to `"compatibility"`. The `"core"` (default) and `"compatibility"` strings are the only values allowed. See the following example and [spec PR 4897](https://github.com/gpuweb/gpuweb/pull/4897).
    
    
    // Request a GPU adapter in compatibility mode
    const adapter = await navigator.gpu.requestAdapter({ featureLevel: "compatibility" });
    
    if (adapter?.featureLevel === "compatibility") {
      // Any devices created from this adapter will support only compatibility mode.
    }
    

The `featureLevel` option replaces the non-standardized `compatibilityMode` option while the non-standardized `featureLevel` attribute replaces the `isCompatibilityMode` attribute.

As it's still experimental, you need to run Chrome with the "Unsafe WebGPU Support" flag at `chrome://flags/#enable-unsafe-webgpu` for now. Check out [webgpureport.org](https://webgpureport.org) to play with it.


## Experimental subgroup features cleanup

The deprecated `"chromium-experimental-subgroups"` and `"chromium-experimental-subgroup-uniform-control-flow"` experimental subgroup features are removed. See [issue 377868468](https://issues.chromium.org/issues/377868468).

The `"subgroups"` experimental feature is all you need now when [experimenting with subgroups](/blog/new-in-webgpu-128#experimenting_with_subgroups). The `"subgroups-f16"` experimental feature is deprecated and will soon be removed. You can use f16 values with subgroups when your application requests both `"shader-f16"` and `"subgroups"` features. See [issue 380244620](https://issues.chromium.org/issues/380244620).


## Deprecate maxInterStageShaderComponents limit

The `maxInterStageShaderComponents` limit is deprecated due to a combination of factors:

  * Redundancy with `maxInterStageShaderVariables`: This limit already serves a similar purpose, controlling the amount of data passed between shader stages.
  * Minor discrepancies: While there are slight differences in how the two limits are calculated, these differences are minor and can be effectively managed within the `maxInterStageShaderVariables` limit.
  * Simplification: Removing `maxInterStageShaderComponents` streamlines the shader interface and reduces complexity for developers. Instead of managing two separate limits with subtle differences, they can focus on the more appropriately named and comprehensive `maxInterStageShaderVariables`.

The goal is to fully remove it in Chrome 135. See [intent to deprecate](https://groups.google.com/a/chromium.org/g/blink-dev/c/i5oJu9lZPAk) and [issue 364338810](https://issues.chromium.org/issues/364338810).


## Dawn updates

The `wgpu::Device::GetAdapterInfo(adapterInfo)` lets you get adapter info directly from a `wgpu::Device`. See [issue 376600838](https://issues.chromium.org/issues/376600838).

The `WGPUProgrammableStageDescriptor` struct has been renamed to `WGPUComputeState` to make compute state consistent with vertex and fragment states. See [issue 379059434](https://issues.chromium.org/issues/379059434).

The `wgpu::VertexStepMode::VertexBufferNotUsed` enum value has been removed. A vertex buffer layout that is not used can now be expressed with `{.stepMode=wgpu::VertexStepMode::Undefined, .attributeCount=0}`. See [issue 383147017](https://issues.chromium.org/issues/383147017).

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/6834..chromium/6943?n=1000).