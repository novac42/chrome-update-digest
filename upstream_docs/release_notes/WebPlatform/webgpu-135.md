# WebGPU 135 Release Notes

Source: https://developer.chrome.com/blog/new-in-webgpu-135

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Blog ](https://developer.chrome.com/blog)

#  What's New in WebGPU (Chrome 135)

Stay organized with collections  Save and categorize content based on your preferences. 

![François Beaufort](https://web.dev/images/authors/beaufortfrancois.jpg)

François Beaufort 

[ GitHub ](https://github.com/beaufortfrancois)

Published: March 26, 2025 

**Experimental:** WebGPU integration with WebXR is now available for developer testing on Windows and Android. Learn more at[ Experimenting with WebGPU in WebXR](https://toji.dev/2025/03/03/experimenting-with-webgpu-in-webxr.html).

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

Last updated 2025-03-26 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-03-26 UTC."],[],[]] 
