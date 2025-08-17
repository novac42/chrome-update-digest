# WebGPU 121 Release Notes

Source: https://developer.chrome.com/blog/new-in-webgpu-121

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Blog ](https://developer.chrome.com/blog)

#  What's New in WebGPU (Chrome 121)

Stay organized with collections  Save and categorize content based on your preferences. 

![François Beaufort](https://web.dev/images/authors/beaufortfrancois.jpg)

François Beaufort 

[ GitHub ](https://github.com/beaufortfrancois)

## Support WebGPU on Android

The Chrome team is excited to announce that WebGPU is now enabled by default in Chrome 121 on devices running Android 12 and greater powered by Qualcomm and ARM GPUs.

Support will gradually expand to encompass a wider range of Android devices, including those running on Android 11 in a near future. This expansion will be dependent on further testing and optimization to ensure a seamless experience across a broader range of hardware configurations. See [issue chromium:1497815](https://bugs.chromium.org/p/chromium/issues/detail?id=1497815).

![Screenshot of WebGPU sample running on Chrome for Android.](/static/blog/new-in-webgpu-121/image/webgpu-android.png) WebGPU sample running on Chrome for Android.

## Use DXC instead of FXC for shader compilation on Windows

Chrome now uses the power of [DXC](https://github.com/microsoft/DirectXShaderCompiler/wiki) (DirectX Compiler) to compile shaders on Windows D3D12 machines equipped with SM6+ graphics hardware. Previously, WebGPU relied on FXC (FX Compiler) for shader compilation on Windows. While functional, FXC lacked the feature set and performance optimizations present in DXC.

Initial testing shows a 20% average increase in compute shader compilation speed when using DXC compared to FXC.

## Timestamp queries in compute and render passes

[Timestamp queries](https://gpuweb.github.io/gpuweb/#timestamp) allow WebGPU applications to measure precisely (down to the nanosecond) how much time their GPU commands take to execute compute and render passes. They are heavily used to gain insights into the performance and behavior of GPU workloads.

When the `"timestamp-query"` feature is available in a `GPUAdapter`, you can now do the following things:

  * Request a `GPUDevice` with the `"timestamp-query"` feature.
  * Create a `GPUQuerySet` of type `"timestamp"`.
  * Use [`GPUComputePassDescriptor.timestampWrites`](https://gpuweb.github.io/gpuweb/#dom-gpucomputepassdescriptor-timestampwrites) and [`GPURenderPassDescriptor.timestampWrites`](https://gpuweb.github.io/gpuweb/#dom-gpurenderpassdescriptor-timestampwrites) to define where to write timestamp values in `GPUQuerySet`.
  * Resolve timestamp values into a `GPUBuffer` with [`resolveQuerySet()`](https://gpuweb.github.io/gpuweb/#dom-gpucommandencoder-resolvequeryset).
  * Read timestamp values back by copying the results from the `GPUBuffer` to the CPU.
  * Decode timestamp values as a `BigInt64Array`.

See the following example and issue [dawn:1800](https://bugs.chromium.org/p/dawn/issues/detail?id=1800).
    
    
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter.features.has("timestamp-query")) {
      throw new Error("Timestamp query feature is not available");
    }
    // Explicitly request timestamp query feature.
    const device = await adapter.requestDevice({
      requiredFeatures: ["timestamp-query"],
    });
    const commandEncoder = device.createCommandEncoder();
    
    // Create a GPUQuerySet which holds 2 timestamp query results: one for the
    // beginning and one for the end of compute pass execution.
    const querySet = device.createQuerySet({ type: "timestamp", count: 2 });
    const timestampWrites = {
      querySet,
      beginningOfPassWriteIndex: 0, // Write timestamp in index 0 when pass begins.
      endOfPassWriteIndex: 1, // Write timestamp in index 1 when pass ends.
    };
    const passEncoder = commandEncoder.beginComputePass({ timestampWrites });
    // TODO: Set pipeline, bind group, and dispatch work to be performed.
    passEncoder.end();
    
    // Resolve timestamps in nanoseconds as a 64-bit unsigned integer into a GPUBuffer.
    const size = 2 * BigInt64Array.BYTES_PER_ELEMENT;
    const resolveBuffer = device.createBuffer({
      size,
      usage: GPUBufferUsage.QUERY_RESOLVE | GPUBufferUsage.COPY_SRC,
    });
    commandEncoder.resolveQuerySet(querySet, 0, 2, resolveBuffer, 0);
    
    // Read GPUBuffer memory.
    const resultBuffer = device.createBuffer({
      size,
      usage: GPUBufferUsage.COPY_DST | GPUBufferUsage.MAP_READ,
    });
    commandEncoder.copyBufferToBuffer(resolveBuffer, 0, resultBuffer, 0, size);
    
    // Submit commands to the GPU.
    device.queue.submit([commandEncoder.finish()]);
    
    // Log compute pass duration in nanoseconds.
    await resultBuffer.mapAsync(GPUMapMode.READ);
    const times = new BigInt64Array(resultBuffer.getMappedRange());
    console.log(`Compute pass duration: ${Number(times[1] - times[0])}ns`);
    resultBuffer.unmap();
    

Due to [timing attack](https://gpuweb.github.io/gpuweb/#security-timing-device) concerns, timestamp queries are quantized with a resolution of 100 microseconds, which provides a good compromise between precision and security. In Chrome browser, you can disable timestamp quantization by enabling the "WebGPU Developer Features" [flag](/docs/web-platform/chrome-flags#chromeflags) at `chrome://flags/#enable-webgpu-developer-features` during the development of your app. See [Timestamp queries quantization](/blog/new-in-webgpu-120#timestamp_queries_quantization) to learn more.

As GPUs may reset the timestamp counter occasionally, which can result in unexpected values such as negative deltas between timestamps, I recommend you check out the [git diff changes](https://github.com/webgpu/webgpu-samples/compare/d67ae2acb40bebfa7c7705cd28175b44fbb03b59..e59b76695212208600f5bbb5423895e6d440fd90#diff-fe64f06098aed64ad6bbd885ad77dc50f7fa856829bf22545d3aa1baaad1c0b8) that adds timestamp query support to the following [Compute Boids](https://webgpu.github.io/webgpu-samples/samples/computeBoids) sample.

![Screenshot of Compute Boids sample featuring timestamp query.](/static/blog/new-in-webgpu-121/image/compute-boids.png) Compute Boids sample featuring timestamp query.

## Default entry points to shader modules

To improve the developer experience, you can now omit the [`entryPoint`](https://gpuweb.github.io/gpuweb/#dom-gpuprogrammablestage-entrypoint) of your shader module when creating a compute or render pipeline. If no unique entry point for the shader stage is found in the shader code, a [GPUValidationError](https://developer.mozilla.org/docs/Web/API/GPUValidationError) will be triggered. See the following example and [issue dawn:2254](https://bugs.chromium.org/p/dawn/issues/detail?id=2254).
    
    
    const code = `
        @vertex fn vertexMain(@builtin(vertex_index) i : u32) ->
          @builtin(position) vec4f {
           const pos = array(vec2f(0, 1), vec2f(-1, -1), vec2f(1, -1));
           return vec4f(pos[i], 0, 1);
        }
        @fragment fn fragmentMain() -> @location(0) vec4f {
          return vec4f(1, 0, 0, 1);
        }`;
    const module = myDevice.createShaderModule({ code });
    const format = navigator.gpu.getPreferredCanvasFormat();
    const pipeline = await myDevice.createRenderPipelineAsync({
      layout: "auto",
    ~~ vertex: { module, entryPoint: "vertexMain" },~~
    ~~ fragment: { module, entryPoint: "fragmentMain", targets: [{ format }] },~~
    ** vertex: { module },**
    ** fragment: { module, targets: [{ format }] },**
    });
    

## Support display-p3 as GPUExternalTexture color space

You can now set `"display-p3"` destination color space when importing a [GPUExternalTexture](https://developer.mozilla.org/docs/Web/API/GPUExternalTexture) from HDR videos with [`importExternalTexture()`](https://developer.mozilla.org/docs/Web/API/GPUDevice/importExternalTexture). Check out how WebGPU handles [color spaces](https://gpuweb.github.io/gpuweb/#color-spaces). See the following example and issue [chromium:1330250](https://bugs.chromium.org/p/chromium/issues/detail?id=1330250).
    
    
    // Create texture from HDR video.
    const video = document.querySelector("video");
    const texture = myDevice.importExternalTexture({
      source: video,
      colorSpace: "display-p3",
    });
    

## Memory heaps info

To help you anticipate memory limitations when allocating large amounts during the development of your app, [`requestAdapterInfo()`](https://developer.mozilla.org/docs/Web/API/GPUAdapter/requestAdapterInfo) now exposes `memoryHeaps` information such as the size and type of memory heaps available on the adapter. This experimental feature is accessible only when the "WebGPU Developer Features" [flag](/docs/web-platform/chrome-flags#chromeflags) at `chrome://flags/#enable-webgpu-developer-features` is enabled. See the following example and [issue dawn:2249](https://bugs.chromium.org/p/dawn/issues/detail?id=2249).
    
    
    const adapter = await navigator.gpu.requestAdapter();
    const adapterInfo = await adapter.requestAdapterInfo();
    
    for (const { size, properties } of adapterInfo.memoryHeaps) {
      console.log(size); // memory heap size in bytes
      if (properties & GPUHeapProperty.DEVICE_LOCAL)  { /* ... */ }
      if (properties & GPUHeapProperty.HOST_VISIBLE)  { /* ... */ }
      if (properties & GPUHeapProperty.HOST_COHERENT) { /* ... */ }
      if (properties & GPUHeapProperty.HOST_UNCACHED) { /* ... */ }
      if (properties & GPUHeapProperty.HOST_CACHED)   { /* ... */ }
    }
    

![Screenshot of https://webgpureport.org featuring memory heaps in adapter info.](/static/blog/new-in-webgpu-121/image/webgpureport.png) Adapter info memory heaps shown on <https://webgpureport.org>.

## Dawn updates

The `HasWGSLLanguageFeature` and `EnumerateWGSLLanguageFeatures` methods on `wgpu::Instance` have been added to handle WGSL language features. See issue [dawn:2260](https://bugs.chromium.org/p/dawn/issues/detail?id=2260).

The non-standard `wgpu::Feature::BufferMapExtendedUsages` feature lets you create a GPU buffer with `wgpu::BufferUsage::MapRead` or `wgpu::BufferUsage::MapWrite` and any other `wgpu::BufferUsage`. See the following example and issue [dawn:2204](https://bugs.chromium.org/p/dawn/issues/detail?id=2204).
    
    
    wgpu::BufferDescriptor descriptor = {
      .size = 128,
      .usage = wgpu::BufferUsage::MapWrite | wgpu::BufferUsage::Uniform
    };
    wgpu::Buffer uniformBuffer = device.CreateBuffer(&descriptor);
    
    uniformBuffer.MapAsync(wgpu::MapMode::Write, 0, 128,
       [](WGPUBufferMapAsyncStatus status, void* userdata)
       {
          wgpu::Buffer* buffer = static_cast<wgpu::Buffer*>(userdata);
          memcpy(buffer->GetMappedRange(), data, sizeof(data));
       },
       &uniformBuffer);
    

The following features have been documented: [ANGLE Texture Sharing](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/features/angle_texture_sharing.md), [D3D11 multithread protected](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/features/d3d11_multithread_protected.md), [Implicit Device Synchronization](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/features/implicit_device_synchronization.md), [Norm16 texture formats](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/features/norm16_texture_formats.md), [Timestamp Query Inside Passes](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/features/timestamp_query_inside_passes.md), [Pixel Local Storage](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/features/pixel_local_storage.md), [Shader Features](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/features/shader_features.md), and [Multi Planar Formats](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/dawn/features/multi_planar_formats.md).

The Chrome team has created an [official GitHub repository for Dawn](https://github.com/google/dawn).

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/6099..chromium/6167?n=1000).

## What's New in WebGPU

A list of everything that has been covered in the [What's New in WebGPU](/docs/web-platform/webgpu/news) series.

### Chrome 139

  * [3D texture support for BC and ASTC compressed formats](/blog/new-in-webgpu-139#3d_texture_support_for_bc_and_astc_compressed_formats)
  * [New "core-features-and-limits" feature](/blog/new-in-webgpu-139#new_core-features-and-limits_feature)
  * [Origin trial for WebGPU compatibility mode](/blog/new-in-webgpu-139#origin_trial_for_webgpu_compatibility_mode)
  * [Dawn updates](/blog/new-in-webgpu-139#dawn_updates)

### Chrome 138

  * [Shorthand for using buffer as a binding resource](/blog/new-in-webgpu-138#shorthand_for_using_buffer_as_a_binding_resource)
  * [Size requirement changes for buffers mapped at creation](/blog/new-in-webgpu-138#size_requirement_changes_for_buffers_mapped_at_creation)
  * [Architecture report for recent GPUs](/blog/new-in-webgpu-138#architecture_report_for_recent_gpus)
  * [Deprecate GPUAdapter isFallbackAdapter attribute](/blog/new-in-webgpu-138#deprecate_gpuadapter_isfallbackadapter_attribute)
  * [Dawn updates](/blog/new-in-webgpu-138#dawn_updates)

### Chrome 137

  * [Use texture view for externalTexture binding](/blog/new-in-webgpu-137#use_texture_view_for_externaltexture_binding)
  * [Buffers copy without specifying offsets and size](/blog/new-in-webgpu-137#buffers_copy_without_specifying_offsets_and_size)
  * [WGSL workgroupUniformLoad using pointer to atomic](/blog/new-in-webgpu-137#wgsl_workgroupuniformload_using_pointer_to_atomic)
  * [GPUAdapterInfo powerPreference attribute](/blog/new-in-webgpu-137#gpuadapterinfo_powerpreference_attribute)
  * [Remove GPURequestAdapterOptions compatibilityMode attribute](/blog/new-in-webgpu-137#remove_gpurequestadapteroptions_compatibilitymode_attribute)
  * [Dawn updates](/blog/new-in-webgpu-137#dawn_updates)

### Chrome 136

  * [GPUAdapterInfo isFallbackAdapter attribute](/blog/new-in-webgpu-136#gpuadapterinfo_isfallbackadapter_attribute)
  * [Shader compilation time improvements on D3D12](/blog/new-in-webgpu-136#shader_compilation_time_improvements_on_d3d12)
  * [Save and copy canvas images](/blog/new-in-webgpu-136#save_and_copy_canvas_images)
  * [Lift compatibility mode restrictions](/blog/new-in-webgpu-136#lift_compatibility_mode_restrictions)
  * [Dawn updates](/blog/new-in-webgpu-136#dawn_updates)

### Chrome 135

  * [Allow creating pipeline layout with null bind group layout](/blog/new-in-webgpu-135#allow_creating_pipeline_layout_with_null_bind_group_layout)
  * [Allow viewports to extend past the render targets bounds](/blog/new-in-webgpu-135#allow_viewports_to_extend_past_the_render_targets_bounds)
  * [Easier access to the experimental compatibility mode on Android](/blog/new-in-webgpu-135#easier_access_to_the_experimental_compatibility_mode_on_android)
  * [Remove maxInterStageShaderComponents limit](/blog/new-in-webgpu-135#remove_maxinterstageshadercomponents_limit)
  * [Dawn updates](/blog/new-in-webgpu-135#dawn_updates)

### Chrome 134

  * [Improve machine-learning workloads with subgroups](/blog/new-in-webgpu-134#improve_machine-learning_workloads_with_subgroups)
  * [Remove float filterable texture types support as blendable](/blog/new-in-webgpu-134#remove_float_filterable_texture_types_support_as_blendable)
  * [Dawn updates](/blog/new-in-webgpu-134#dawn_updates)

### Chrome 133

  * [Additional unorm8x4-bgra and 1-component vertex formats](/blog/new-in-webgpu-133#additional_unorm8x4-bgra_and_1-component_vertex_formats)
  * [Allow unknown limits to be requested with undefined value](/blog/new-in-webgpu-133#allow_unknown_limits_to_be_requested_with_undefined_value)
  * [WGSL alignment rules changes](/blog/new-in-webgpu-133#wgsl_alignment_rules_changes)
  * [WGSL performance gains with discard](/blog/new-in-webgpu-133#wgsl_performance_gains_with_discard)
  * [Use VideoFrame displaySize for external textures](/blog/new-in-webgpu-133#use_videoframe_displaysize_for_external_textures)
  * [Handle images with non-default orientations using copyExternalImageToTexture](/blog/new-in-webgpu-133#handle_images_with_non-default_orientations_using_copyexternalimagetotexture)
  * [Improving developer experience](/blog/new-in-webgpu-133#improving_developer_experience)
  * [Enable compatibility mode with featureLevel](/blog/new-in-webgpu-133#enable_compatibility_mode_with_featurelevel)
  * [Experimental subgroup features cleanup](/blog/new-in-webgpu-133#experimental_subgroup_features_cleanup)
  * [Deprecate maxInterStageShaderComponents limit](/blog/new-in-webgpu-133#deprecate_maxinterstageshadercomponents_limit)
  * [Dawn updates](/blog/new-in-webgpu-133#dawn_updates)

### Chrome 132

  * [Texture view usage](/blog/new-in-webgpu-132#texture_view_usage)
  * [32-bit float textures blending](/blog/new-in-webgpu-132#32-bit_float_textures_blending)
  * [GPUDevice adapterInfo attribute](/blog/new-in-webgpu-132#gpudevice_adapterinfo_attribute)
  * [Configuring canvas context with invalid format throw JavaScript error](/blog/new-in-webgpu-132#configuring_canvas_context_with_invalid_format_throw_javascript_error)
  * [Filtering sampler restrictions on textures](/blog/new-in-webgpu-132#filtering_sampler_restrictions_on_textures)
  * [Extended subgroups experimentation](/blog/new-in-webgpu-132#extended_subgroups_experimentation)
  * [Improving developer experience](/blog/new-in-webgpu-132#improving_developer_experience)
  * [Experimental support for 16-bit normalized texture formats](/blog/new-in-webgpu-132#experimental_support_for_16-bit_normalized_texture_formats)
  * [Dawn updates](/blog/new-in-webgpu-132#dawn_updates)

### Chrome 131

  * [Clip distances in WGSL](/blog/new-in-webgpu-131#clip_distances_in_wgsl)
  * [GPUCanvasContext getConfiguration()](/blog/new-in-webgpu-131#gpucanvascontext_getconfiguration)
  * [Point and line primitives must not have depth bias](/blog/new-in-webgpu-131#point_and_line_primitives_must_not_have_depth_bias)
  * [Inclusive scan built-in functions for subgroups](/blog/new-in-webgpu-131#inclusive_scan_built-in_functions_for_subgroups)
  * [Experimental support for multi-draw indirect](/blog/new-in-webgpu-131#experimental_support_for_multi-draw_indirect)
  * [Shader module compilation option strict math](/blog/new-in-webgpu-131#shader_module_compilation_option_strict_math)
  * [Remove GPUAdapter requestAdapterInfo()](/blog/new-in-webgpu-131#remove_gpuadapter_requestadapterinfo)
  * [Dawn updates](/blog/new-in-webgpu-131#dawn_updates)

### Chrome 130

  * [Dual source blending](/blog/new-in-webgpu-130#dual_source_blending)
  * [Shader compilation time improvements on Metal](/blog/new-in-webgpu-130#shader_compilation_time_improvements_on_metal)
  * [Deprecation of GPUAdapter requestAdapterInfo()](/blog/new-in-webgpu-130#deprecation_of_gpuadapter_requestadapterinfo)
  * [Dawn updates](/blog/new-in-webgpu-130#dawn_updates)

### Chrome 129

  * [HDR support with canvas tone mapping mode](/blog/new-in-webgpu-129#hdr_support_with_canvas_tone_mapping_mode)
  * [Expanded subgroups support](/blog/new-in-webgpu-129#expanded_subgroups_support)
  * [Dawn updates](/blog/new-in-webgpu-129#dawn_updates)

### Chrome 128

  * [Experimenting with subgroups](/blog/new-in-webgpu-128#experimenting_with_subgroups)
  * [Deprecate setting depth bias for lines and points](/blog/new-in-webgpu-128#deprecate_setting_depth_bias_for_lines_and_points)
  * [Hide uncaptured error DevTools warning if preventDefault](/blog/new-in-webgpu-128#hide_uncaptured_error_devtools_warning_if_preventdefault)
  * [WGSL interpolate sampling first and either](/blog/new-in-webgpu-128#wgsl_interpolate_sampling_first_and_either)
  * [Dawn updates](/blog/new-in-webgpu-128#dawn_updates)

### Chrome 127

  * [Experimental support for OpenGL ES on Android](/blog/new-in-webgpu-127#experimental_support_for_opengl_es_on_android)
  * [GPUAdapter info attribute](/blog/new-in-webgpu-127#gpuadapter_info_attribute)
  * [WebAssembly interop improvements](/blog/new-in-webgpu-127#webassembly_interop_improvements)
  * [Improved command encoder errors](/blog/new-in-webgpu-127#improved_command_encoder_errors)
  * [Dawn updates](/blog/new-in-webgpu-127#dawn_updates)

### Chrome 126

  * [Increase maxTextureArrayLayers limit](/blog/new-in-webgpu-126#increase_maxtexturearraylayers_limit)
  * [Buffer upload optimization for Vulkan backend](/blog/new-in-webgpu-126#buffer_upload_optimization_for_vulkan_backend)
  * [Shader compilation time improvements](/blog/new-in-webgpu-126#shader_compilation_time_improvements)
  * [Submitted command buffers must be unique](/blog/new-in-webgpu-126#submitted_command_buffers_must_be_unique)
  * [Dawn updates](/blog/new-in-webgpu-126#dawn_updates)

### Chrome 125

  * [Subgroups (feature in development)](/blog/new-in-webgpu-125#subgroups_feature_in_development)
  * [Render to slice of 3D texture](/blog/new-in-webgpu-125#render_to_slice_of_3d_texture)
  * [Dawn updates](/blog/new-in-webgpu-125#dawn_updates)

### Chrome 124

  * [Read-only and read-write storage textures](/blog/new-in-webgpu-124#read-only_and_read-write_storage_textures)
  * [Service workers and shared workers support](/blog/new-in-webgpu-124#service_workers_and_shared_workers_support)
  * [New adapter information attributes](/blog/new-in-webgpu-124#new_adapter_information_attributes)
  * [Bug fixes](/blog/new-in-webgpu-124#bug_fixes)
  * [Dawn updates](/blog/new-in-webgpu-124#dawn_updates)

### Chrome 123

  * [DP4a built-in functions support in WGSL](/blog/new-in-webgpu-123#dp4a_built-in_functions_support_in_wgsl)
  * [Unrestricted pointer parameters in WGSL](/blog/new-in-webgpu-123#unrestricted_pointer_parameters_in_wgsl)
  * [Syntax sugar for dereferencing composites in WGSL](/blog/new-in-webgpu-123#syntax_sugar_for_dereferencing_composites_in_wgsl)
  * [Separate read-only state for stencil and depth aspects](/blog/new-in-webgpu-123#separate_read-only_state_for_stencil_and_depth_aspects)
  * [Dawn updates](/blog/new-in-webgpu-123#dawn_updates)

### Chrome 122

  * [Expand reach with compatibility mode (feature in development)](/blog/new-in-webgpu-122#expand_reach_with_compatibility_mode_feature_in_development)
  * [Increase maxVertexAttributes limit](/blog/new-in-webgpu-122#increase_maxvertexattributes_limit)
  * [Dawn updates](/blog/new-in-webgpu-122#dawn_updates)

### Chrome 121

  * [Support WebGPU on Android](/blog/new-in-webgpu-121#support-webgpu-on-android)
  * [Use DXC instead of FXC for shader compilation on Windows](/blog/new-in-webgpu-121#use_dxc_instead_of_fxc_for_shader_compilation_on_windows)
  * [Timestamp queries in compute and render passes](/blog/new-in-webgpu-121#timestamp_queries_in_compute_and_render_passes)
  * [Default entry points to shader modules](/blog/new-in-webgpu-121#default_entry_points_to_shader_modules)
  * [Support display-p3 as GPUExternalTexture color space](/blog/new-in-webgpu-121#support_display-p3_as_gpuexternaltexture_color_space)
  * [Memory heaps info](/blog/new-in-webgpu-121#memory_heaps_info)
  * [Dawn updates](/blog/new-in-webgpu-121#dawn_updates)

### Chrome 120

  * [Support for 16-bit floating-point values in WGSL](/blog/new-in-webgpu-120#support_for_16-bit_floating-point_values_in_wgsl)
  * [Push the limits](/blog/new-in-webgpu-120#push_the_limits)
  * [Changes to depth-stencil state](/blog/new-in-webgpu-120#changes_to_depth-stencil_state)
  * [Adapter information updates](/blog/new-in-webgpu-120#adapter_information_updates)
  * [Timestamp queries quantization](/blog/new-in-webgpu-120#timestamp_queries_quantization)
  * [Spring-cleaning features](/blog/new-in-webgpu-120#spring-cleaning_features)

### Chrome 119

  * [Filterable 32-bit float textures](/blog/new-in-webgpu-119#filterable_32-bit_float_textures)
  * [unorm10-10-10-2 vertex format](/blog/new-in-webgpu-119#unorm10-10-10-2_vertex_format)
  * [rgb10a2uint texture format](/blog/new-in-webgpu-119#rgb10a2uint_texture_format)
  * [Dawn updates](/blog/new-in-webgpu-119#dawn_updates)

### Chrome 118

  * [HTMLImageElement and ImageData support in `copyExternalImageToTexture()`](/blog/new-in-webgpu-118#htmlimageelement_and_imagedata_support_in_copyexternalimagetotexture)
  * [Experimental support for read-write and read-only storage texture](/blog/new-in-webgpu-118#experimental_support_for_read-write_and_read-only_storage_texture)
  * [Dawn updates](/blog/new-in-webgpu-118#dawn_updates)

### Chrome 117

  * [Unset vertex buffer](/blog/new-in-webgpu-117#unset_vertex_buffer)
  * [Unset bind group](/blog/new-in-webgpu-117#unset_bind_group)
  * [Silence errors from async pipeline creation when device is lost](/blog/new-in-webgpu-117#silence_errors_from_async_pipeline_creation_when_device_is_lost)
  * [SPIR-V shader module creation updates](/blog/new-in-webgpu-117#spir-v_shader_module_creation_updates)
  * [Improving developer experience](/blog/new-in-webgpu-117#improving_developer_experience)
  * [Caching pipelines with automatically generated layout](/blog/new-in-webgpu-117#caching_pipelines_with_automatically_generated_layout)
  * [Dawn updates](/blog/new-in-webgpu-117#dawn_updates)

### Chrome 116

  * [WebCodecs integration](/blog/new-in-webgpu-116#webcodecs_integration)
  * [Lost device returned by GPUAdapter `requestDevice()`](/blog/new-in-webgpu-116#lost_device_returned_by_gpuadapter_requestdevice)
  * [Keep video playback smooth if `importExternalTexture()` is called](/blog/new-in-webgpu-116#keep_video_playback_smooth_if_importexternaltexture_is_called)
  * [Spec conformance](/blog/new-in-webgpu-116#spec_conformance)
  * [Improving developer experience](/blog/new-in-webgpu-116#improving_developer_experience)
  * [Dawn updates](/blog/new-in-webgpu-116#dawn_updates)

### Chrome 115

  * [Supported WGSL language extensions](/blog/new-in-webgpu-115#supported_wgsl_language_extensions)
  * [Experimental support for Direct3D 11](/blog/new-in-webgpu-115#experimental_support_for_direct3d_11)
  * [Get discrete GPU by default on AC power](/blog/new-in-webgpu-115#get_discrete_gpu_by_default_on_ac_power)
  * [Improving developer experience](/blog/new-in-webgpu-115#improving_developer_experience)
  * [Dawn updates](/blog/new-in-webgpu-115#dawn_updates)

### Chrome 114

  * [Optimize JavaScript](/blog/new-in-webgpu-114#optimize_javascript)
  * [getCurrentTexture() on unconfigured canvas throws InvalidStateError](/blog/new-in-webgpu-114#getcurrenttexture_on_unconfigured_canvas_throws_invalidstateerror)
  * [WGSL updates](/blog/new-in-webgpu-114#wgsl_updates)
  * [Dawn updates](/blog/new-in-webgpu-114#dawn_updates)

### Chrome 113

  * [Use WebCodecs VideoFrame source in `importExternalTexture()`](/blog/new-in-webgpu-113#use_webcodecs_videoframe_source_in_importexternaltexture)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2024-01-18 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2024-01-18 UTC."],[],[]] 
