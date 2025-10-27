---
layout: default
title: graphics-webgpu-en
---

## Area Summary

Chrome 134 (stable) focuses on advancing WebGPU capability and runtime correctness: a new subgroups feature enables SIMD-level parallelism for more efficient cross-thread math operations, blendability handling for float textures was corrected, and the Dawn implementation updated OS and API requirements. The most impactful change for developers is the subgroups support, which can significantly improve machine-learning and parallel compute kernels on the GPU. The float texture blendability fix reduces incorrect behavior now that the explicit "float32-blendable" feature exists, improving rendering correctness. Dawn updates tighten platform requirements and modernize the WGSLLanguage feature API, affecting native build and shader tooling.

## Detailed Updates

Below are the Graphics and WebGPU area updates from Chrome 134 that follow directly from the summary above.

### Improve machine-learning workloads with subgroups

#### What's New
After a year of development and trials, the subgroups WebGPU feature enabling SIMD-level parallelism is now available. It allows threads in a workgroup to communicate and execute collective math operations, such as calculating a sum of numbers.

#### Technical Details
Subgroups expose cross-thread collective operations at the WGSL level (including subgroup and quad built-ins), enabling finer-grained parallelism and reduced synchronization overhead compared to emulating SIMD in kernels.

#### Use Cases
- Machine-learning kernels that need fast reductions, scans, or other collective math.
- High-throughput compute shaders that benefit from SIMD-style communication.
- Optimizing GPU compute performance without changing host-side parallelism.

#### References
- [original proposal](https://github.com/gpuweb/gpuweb/blob/main/proposals/subgroups.md)
- [chromestatus entry](https://chromestatus.com/feature/5126409856221184)
- [origin trial](https://developer.chrome.com/origintrials/#/view_trial/4130363808252166145)
- [subgroup built-in functions](https://gpuweb.github.io/gpuweb/wgsl/#subgroup-builtin-functions)
- [quad built-in functions](https://gpuweb.github.io/gpuweb/wgsl/#quad-builtin-functions)
- [quad](https://gpuweb.github.io/gpuweb/wgsl/#quad)
- [WebGPU subgroups](https://codepen.io/web-dot-dev/pen/emOqWQJ)

### Remove float filterable texture types support as blendable

#### What's New
Now that the [32-bit float textures blending](/blog/new-in-webgpu-132#32-bit_float_textures_blending) is available with the "float32-blendable" feature, the incorrect support for float filterable texture types as blendable is removed.

#### Technical Details
The change enforces correct feature-gated behavior for blendable float texture formats, avoiding implicit or incorrect blending assumptions when the explicit float32-blendable capability is required.

#### Use Cases
- Rendering pipelines and compositing that relied on incorrect blendability behavior will now follow explicit capability checks.
- Developers should gate use of float blending behind the proper feature rather than assuming blendability for filterable float textures.

#### References
- [issue 364987733](https://issues.chromium.org/issues/364987733)

### Dawn updates

#### What's New
Dawn now requires macOS 11 and iOS 14 and only supports Metal 2.3+. The `GetWGSLLanguageFeatures()` method of `wgpu::Instance` replaces `EnumerateWGSLLanguageFeatures()`.

#### Technical Details
- Platform minimums updated to modern macOS/iOS releases and Metal 2.3+, which affects supported hardware and OS targets for native builds using Dawn.
- API change in Dawn's C++ wrapper adjusts how WGSLLanguage feature discovery is queried, requiring code changes where the older Enumerate method was used.

#### Use Cases
- Native applications and browser ports that embed Dawn must align build targets and update code to the new WGSLLanguage feature API.
- Shader toolchains and build scripts should verify compatibility with the updated Metal and OS requirements.

#### References
- [issue 381117827](https://crbug.com/381117827)
- [issue 368672124](https://issues.chromium.org/issues/368672124)
- [issue 377820810](https://issues.chromium.org/issues/377820810)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/6943..chromium/6998?n=1000)

Save this digest to:
```text
digest_markdown/webplatform/Graphics and WebGPU/chrome-134-stable-en.md
