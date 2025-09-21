# Graphics and WebGPU - Chrome 135



## Allow creating pipeline layout with null bind group layout

Previously, creating an empty bind group layout required adding a bind group with zero bindings, which was inconvenient. This is no longer necessary as null bind group layouts are now allowed and ignored when creating a pipeline layout. This should make development easier.

For example, you might want to create a pipeline that uses only bind group layouts 0 and 2. You could assign bind group layout 1 to fragment data and bind group layout 2 to vertex data, and then render without a fragment shader. See [issue 377836524](https://issues.chromium.org/issues/377836524).
    
    
    const bgl0 = myDevice.createBindGroupLayout({ entries: myGlobalEntries });
    const bgl1 = myDevice.createBindGroupLayout({ entries: myFragmentEntries });
    const bgl2 = myDevice.createBindGroupLayout({ entries: myVertexEntries });
    
    // Create a pipeline layout that will be used to render without a fragment shader.
    const myPipelineLayout = myDevice.createPipelineLayout({
      bindGroupLayouts: [bgl0, null, bgl2],
    });
    


## Allow viewports to extend past the render targets bounds

The requirements for viewport validation have been relaxed to allow viewports to go beyond the render target boundaries. This is especially useful for drawing 2D elements such as UI that may extend outside the current viewport. See [issue 390162929](https://issues.chromium.org/issues/390162929).
    
    
    const passEncoder = myCommandEncoder.beginRenderPass({
      colorAttachments: [
        {
          view: myColorTexture.createView(),
          loadOp: "clear",
          storeOp: "store",
        },
      ],
    });
    
    // Set a viewport that extends past the render target's bounds by 8 pixels
    // in all directions.
    passEncoder.setViewport(
      /*x=*/ -8,
      /*y=*/ -8,
      /*width=*/ myColorTexture.width + 16,
      /*height=*/ myColorTexture.height + 16,
      /*minDepth=*/ 0,
      /*maxDepth=*/ 1,
    );
    
    // Draw geometry and complete the render pass as usual.
    


## Easier access to the experimental compatibility mode on Android

The `chrome://flags/#enable-unsafe-webgpu` flag alone now enables all capabilities required for the experimental [WebGPU compatibility mode](/blog/new-in-webgpu-122#expand_reach_with_compatibility_mode_feature_in_development) on Android. With that, you can request a GPUAdapter in compatibility mode with the `featureLevel: "compatibility"` option and even get access to the OpenGL ES backend on devices lacking support for Vulkan. See the following example and issue [dawn:389876644](https://issues.chromium.org/issues/389876644).
    
    
    // Request a GPUAdapter in compatibility mode.
    const adapter = await navigator.gpu.requestAdapter({ featureLevel: "compatibility" });
    

![WebGPU report page shows a GPUAdapter in compatibility mode on Android device.](/static/blog/new-in-webgpu-135/image/compatibility-mode-android.jpg) Compatibility mode adapter info in [webgpureport.org](https://webgpureport.org).


## Remove maxInterStageShaderComponents limit

As [previously announced](/blog/new-in-webgpu-133#deprecate_maxinterstageshadercomponents_limit), the maxInterStageShaderComponents limit is removed due to a combination of factors:

  * Redundancy with `maxInterStageShaderVariables`: This limit already serves a similar purpose, controlling the amount of data passed between shader stages.
  * Minor discrepancies: While there are slight differences in how the two limits are calculated, these differences are minor and can be effectively managed within the `maxInterStageShaderVariables` limit.
  * Simplification: Removing `maxInterStageShaderComponents` streamlines the shader interface and reduces complexity for developers. Instead of managing two separate limits with subtle differences, they can focus on the more appropriately named and comprehensive `maxInterStageShaderVariables`.

See [intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/i5oJu9lZPAk) and [issue 364338810](https://issues.chromium.org/issues/364338810).


## Dawn updates

It's no longer possible to use a filtering sampler to sample a depth texture. As a reminder, a depth texture can only be used with a non filtering or a comparison sampler. See [issue 379788112](https://issues.chromium.org/issues/379788112).

The `WGPURequiredLimits` and `WGPUSupportedLimits` structures have been flattened into `WGPULimits`. See [issue 374263404](https://issues.chromium.org/issues/374263404).

The following structs have been renamed. See [issue 42240793](https://issues.chromium.org/issues/42240793).

  * `WGPUImageCopyBuffer` is now `WGPUTexelCopyBufferInfo`
  * `WGPUImageCopyTexture` is now `WGPUTexelCopyTextureInfo`
  * `WGPUTextureDataLayout` is now `WGPUTexelCopyBufferLayout`

The `subgroupMinSize` and `subgroupMaxSize` members have been added to the `WGPUAdapterInfo` struct. See [webgpu-headers PR](https://github.com/webgpu-native/webgpu-headers/pull/509).

Tracing Dawn API usage in Metal is now possible when running your program with the `DAWN_TRACE_FILE_BASE` environment variable which saves a .gputrace file that can be loaded later into XCode's Metal Debugger. See the [Debugging Dawn](https://dawn.googlesource.com/dawn/+/HEAD/docs/dawn/debugging.md#tracing-native-gpu-api-usage) documentation.

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/6998..chromium/7049?n=1000).