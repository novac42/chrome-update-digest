# Graphics and WebGPU - Chrome 140



## Device requests consume adapter

According to the [WebGPU specification](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1), an adapter is marked as "consumed" upon a successful device request. Consequently, any subsequent `requestDevice()` calls using the same adapter will now result in a rejected promise. Previously, these calls would return a device that was lost at creation. See [issue 415825174](https://issues.chromium.org/issues/415825174).
    
    
    const adapter = await navigator.gpu.requestAdapter();
    const device = await adapter.requestDevice();
    
    await adapter.requestDevice(); // Fails because adapter has been consumed.
    


## Shorthand for using texture where texture view is used

A [GPUTexture](https://gpuweb.github.io/gpuweb/#gputexture) can now be used directly as a [GPUBindingResource](https://gpuweb.github.io/gpuweb/#typedefdef-gpubindingresource) to expose to the shader for binding. It can also be used as a GPURenderPassColorAttachment `view`, a GPURenderPassColorAttachment `resolveTarget`, and a GPURenderPassDepthStencilAttachment `view` for improved ergonomics. This offers a simpler approach than using a [GPUTextureView](https://gpuweb.github.io/gpuweb/#dictdef-gpubufferbinding) to get a default view. See[ issue 425906323](https://issues.chromium.org/issues/425906323).
    
    
    const bindGroup = myDevice.createBindGroup({
      layout: myPipeline.getBindGroupLayout(0),
      entries: [
        { binding: 0, resource: mySampler },
        { binding: 1, resource: myTexture }, // Same as myTexture.createView()
        { binding: 2, resource: myExternalTexture },
        { binding: 3, resource: myBuffer },
      ],
    });
    


## WGSL textureSampleLevel supports 1D textures

1D textures can now be [sampled](https://gpuweb.github.io/gpuweb/wgsl/#texturesamplelevel) using `textureSampleLevel()` for consistency with 2D textures. This lets you sample a 1D texture from a vertex shader which was previously only possible from a fragment shader with `textureSample()`. See[ issue 382514673](https://issues.chromium.org/issues/382514673).


## Deprecate bgra8unorm read-only storage texture usage

Using `"bgra8unorm"` format with read-only storage textures is now deprecated. The WebGPU specification explicitly disallows this, and its prior allowance in Chrome was a bug, as this format is intended for write-only access and is not portable. See [issue 427681156](https://issues.chromium.org/issues/427681156).


## Remove GPUAdapter isFallbackAdapter attribute

As previously [announced](/blog/new-in-webgpu-138#deprecate_gpuadapter_isfallbackadapter_attribute), the GPUAdapter `isFallbackAdapter` attribute is now removed. It's replaced by the GPUAdapterInfo `isFallbackAdapter` attribute that was introduced in Chrome 136. See [intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/Wzr22XXV3s8).


## Dawn updates

The `wgpuInstanceGetWGSLLanguageFeatures()` function is used to get a list of WGSL language features supported by the instance. Previously it returned a `WGPUStatus` value. It has been updated to not return a value since it can't fail. See [issue 429178774](https://issues.chromium.org/issues/429178774).

The `wgpuSurfacePresent()` function now returns a `WGPUStatus` error if the surface doesn't have a current texture. See [issue 425930323](https://issues.chromium.org/issues/425930323)

The new `wgpu::InstanceFeatureName::MultipleDevicesPerAdapter` feature lets adapters create multiple devices without being "consumed". See [issue 415825174](https://issues.chromium.org/issues/415825174).

The `dump_shaders_on_failure` device toggle lets you dump shaders only on failure for [debugging purposes](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/debugging.md). It applies exclusively to D3 backends, though future expansion to other backends is possible. See [issue 429187478](http://issues.chromium.org/issues/429187478).

Multiple changes have been made to the Vulkan backend to reduce overhead when submitting render passes, especially for improved performance on mobile GPUs. For example: [caching VkFramebuffers](https://dawn.googlesource.com/dawn/+/ddf2e1f61d20171ecd10ae3be70acb750a56686d).

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7258..chromium/7339?n=1000).