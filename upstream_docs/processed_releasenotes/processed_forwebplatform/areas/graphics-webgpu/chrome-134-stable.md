# Graphics and WebGPU - Chrome 134



## Improve machine-learning workloads with subgroups

After a year of development and trials, the subgroups WebGPU feature enabling SIMD-level parallelism is now available. It allows threads in a workgroup to communicate and execute collective math operations, such as calculating a sum of numbers, and offers an efficient method for cross-thread data sharing. See the [original proposal](https://github.com/gpuweb/gpuweb/blob/main/proposals/subgroups.md) and [chromestatus entry](https://chromestatus.com/feature/5126409856221184).

For reference, Google Meet saw 2.3-2.9 times speed increases when benchmarking subgroups against [packed integer dot products](/blog/io24-webassembly-webgpu-2#packed_integer_dot_products) for matrix-vector multiply shaders on some devices during the [origin trial](https://developer.chrome.com/origintrials/#/view_trial/4130363808252166145).

When the `"subgroups"` feature is available in a `GPUAdapter`, request a `GPUDevice` with this feature to get subgroups support in WGSL. It's helpful to check `subgroupMinSize` and `subgroupMaxSize` adapter info values—for example, if you have a hardcoded algorithm that requires a subgroup of a certain size.

You also need to explicitly enable this extension in your WGSL code with `enable subgroups;` to get access to the following built-in values in both compute and fragment shaders stages:

  * `subgroup_invocation_id`: A built-in value for the index of the thread within the subgroup.

  * `subgroup_size`: A built-in value for subgroup size access.

The numerous [subgroup built-in functions](https://gpuweb.github.io/gpuweb/wgsl/#subgroup-builtin-functions) (for example, `subgroupAdd()`, `subgroupBallot()`, `subgroupBroadcast()`, `subgroupShuffle()`) enable efficient communication and computation between invocations within a subgroup. These subgroup operations are classified as single-instruction multiple-thread (SIMT) operations. Additionally, the [quad built-in functions](https://gpuweb.github.io/gpuweb/wgsl/#quad-builtin-functions), which operate on a [quad](https://gpuweb.github.io/gpuweb/wgsl/#quad) of invocations facilitate data communication within the quad.

You can use f16 values with subgroups when you request a `GPUDevice` with both `"shader-f16"` and `"subgroups"` features.

The following sample is a good starting point for exploring subgroups: it shows a shader that uses the `subgroupExclusiveMul()` built-in function to compute factorials without reading or writing memory to communicate intermediate results.

See the Pen [WebGPU subgroups](https://codepen.io/web-dot-dev/pen/emOqWQJ). 


## Remove float filterable texture types support as blendable

Now that the [32-bit float textures blending](/blog/new-in-webgpu-132#32-bit_float_textures_blending) is available with the `"float32-blendable"` feature, the incorrect support for float filterable texture types as blendable is removed. See [issue 364987733](https://issues.chromium.org/issues/364987733).


## Dawn updates

Dawn now requires macOS 11 and iOS 14 and only supports Metal 2.3+. See [issue 381117827](https://crbug.com/381117827).

The new `GetWGSLLanguageFeatures()` method of the `wgpu::Instance` now replaces `EnumerateWGSLLanguageFeatures()`. See [issue 368672124](https://issues.chromium.org/issues/368672124).

The following binding types have an `Undefined` value and their default values in binding layout have been changed. See [issue 377820810](https://issues.chromium.org/issues/377820810).

  * `wgpu::BufferBindingType::Undefined` is now `Uniform`
  * `wgpu::SamplerBindingType::Undefined` is now `Filtering`
  * `wgpu::TextureSampleType::Undefined` is now `Float`
  * `wgpu::StorageTextureAccess::Undefined`is now `WriteOnly`

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/6943..chromium/6998?n=1000).