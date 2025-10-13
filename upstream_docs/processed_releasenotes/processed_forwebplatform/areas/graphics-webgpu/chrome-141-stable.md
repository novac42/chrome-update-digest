# Graphics and WebGPU - Chrome 141



## Tint IR completed

A long running project (over 2.5 years) to increase the performance of the internals of Tint, the WGSL compiler has been completed. An Intermediate Representation (IR) was inserted into the backend between the current Abstract Syntax Tree (AST) and the backend code generators. The introduction of the IR allowed the Chrome team to remove all of the AST transformations and re-create them as IR transformations which, due to architectural differences, are substantially faster. The internals of Tint, on some platforms saw up to a seven times speed improvement from these changes.

This new IR unlocks significant potential for sophisticated, large-scale shader analysis and transformation, promising not just notable performance gains but also a smoother path for Chrome to deliver exciting new WebGPU features down the line.

From this milestone all backend code generators work from the IR representation, all AST transformations have been deleted, and all of the AST support code to run the transformations has been removed.

As part of the IR improvement work, the SPIR-V frontend (used by applications to convert SPIR-V to WGSL) was converted from generating an AST representation to generating directly to IR. This enhancement also introduces long-awaited features like float 16 support to the SPIR-V frontend.


## Integer range analysis in WGSL compiler

The Chrome team is progressively rolling out a new integer range analysis for Tint, the WebGPU shader language compiler. Integer range analysis estimates the minimum and maximum values an integer variable can take during program execution without actually running the program.

This feature aims to improve efficiency by reducing the need for costly bounds checking and will soon be enabled by default across all platforms. See [issue 348701956](https://issuetracker.google.com/348701956).


## SPIR-V 1.4 update for Vulkan backend

SPIR-V 1.4 support is rolled out where available on Android and ChromeOS devices. This update enables Tint, the WGSL compiler, to take advantage of new SPIR-V features, relaxations, and new instructions for more efficient code generation in certain scenarios when compiling Vulkan shaders. See [issue 427717267](https://issuetracker.google.com/427717267).


## Dawn updates

The standardized [`webgpu.h`](https://github.com/webgpu-native/webgpu-headers/blob/main/webgpu.h) header, which defines the core WebGPU C API, is now finally considered stable. This stability applies specifically to the core API defined upstream, not including implementation extensions (for example, from Dawn or Emdawnwebgpu), so it is best to use the `webgpu.h` provided by the exact implementation you're linking against. While the header is stable, you might still encounter unintended differences between implementations as we continue to fix bugs and address compatibility across the ecosystem. If you do, [file a bug](https://crbug.com/dawn/new).

Thanks to external contributor [William Candillon](https://github.com/wcandillon), you can now find prebuilt Dawn binaries as artifacts on GitHub Actions. Those include static .lib files for Android, an .XCFramework bundle for Apple, and all the necessary header files. See [Dawn PR #39](https://github.com/google/dawn/pull/39) and an [example](https://github.com/google/dawn/actions/runs/17429395587#artifacts) of the artifacts.

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7339..chromium/7390?n=1000).