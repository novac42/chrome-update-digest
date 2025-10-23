---
layout: default
title: chrome-141-en
---

## Area Summary

Chrome 141’s Graphics and WebGPU updates center on compiler/toolchain maturity and backend capability upgrades. Key themes include the completion of a major Tint IR refactor, rollout of integer range analysis in the WGSL compiler, SPIR-V 1.4 support on Vulkan backends where available, and stabilization of the upstream WebGPU C API header. These changes primarily improve shader compilation efficiency, enable more capable code generation paths, and provide greater API stability for native integrations. Together, they strengthen the WebGPU ecosystem and advance predictable, performant graphics and compute on the web.

## Detailed Updates

Building on the themes above, the following features highlight concrete improvements developers can leverage in Chrome 141.

### Tint IR completed

#### What's New
A multi-year effort added an Intermediate Representation (IR) inside Tint, the WGSL compiler, between the AST and backend code generators to increase internal performance.

#### Technical Details
- The IR sits between the existing AST and backend code generation stages.
- This architectural layer enables more efficient internal transformations and optimizations during shader compilation.

#### Use Cases
- Faster and more scalable shader compilation pipelines for complex WGSL codebases.
- A foundation for future compiler optimizations and backend improvements without changing WGSL source.

#### References


### Integer range analysis in WGSL compiler

#### What's New
Chrome is progressively rolling out integer range analysis in Tint to estimate the minimum and maximum values an integer variable can take without executing the program.

#### Technical Details
- Static analysis pass infers integer value bounds across program paths.
- The results can inform safer and more efficient code generation decisions in the compiler pipeline.

#### Use Cases
- More informed optimizations in shaders that use integer-heavy control flow or indexing.
- Potential for reduced conservatism in generated code where value ranges are proven.

#### References
- https://issuetracker.google.com/348701956 (issue 348701956)

### SPIR-V 1.4 update for Vulkan backend

#### What's New
SPIR-V 1.4 support is rolled out where available on Android and ChromeOS devices, enabling Tint to leverage newer SPIR-V features, relaxations, and instructions for certain Vulkan compilation scenarios.

#### Technical Details
- When targeting Vulkan, Tint can emit SPIR-V 1.4 to take advantage of compatible device/driver capabilities.
- Newer instructions and relaxations can yield more efficient shader code generation paths.

#### Use Cases
- Improved shader generation on Vulkan-capable Android and ChromeOS devices that support SPIR-V 1.4.
- Potential performance and efficiency gains in shaders benefiting from 1.4 features.

#### References
- https://issuetracker.google.com/427717267 (issue 427717267)

### Dawn updates

#### What's New
The standardized webgpu.h header that defines the core WebGPU C API is considered stable for the upstream core API (excluding implementation extensions).

#### Technical Details
- Stability applies to the upstream-defined core API surface only.
- Implementation-specific extensions are not covered by this stability statement.

#### Use Cases
- More predictable native integrations and tooling that target the stable core WebGPU C API.
- Easier maintenance and compatibility for projects binding to Dawn via webgpu.h.

#### References
- https://github.com/webgpu-native/webgpu-headers/blob/main/webgpu.h (`webgpu.h`)
- https://crbug.com/dawn/new (file a bug)
- https://github.com/wcandillon (William Candillon)
- https://github.com/google/dawn/pull/39 (Dawn PR #39)
- https://github.com/google/dawn/actions/runs/17429395587#artifacts (example)
- https://dawn.googlesource.com/dawn/+log/chromium/7339..chromium/7390?n=1000 (list of commits)
