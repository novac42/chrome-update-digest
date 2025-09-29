---
layout: default
title: Chrome 140 Storage Updates - Expert Analysis
---

# Chrome 140 Storage Updates - Expert Analysis

## Area Summary

Chrome 140 brings a focused but important correction to WebGPU storage texture handling, specifically addressing the deprecation of `bgra8unorm` format for read-only storage textures. This change aligns Chrome with the WebGPU specification by removing support for a format that was incorrectly allowed in previous versions. The update emphasizes Chrome's commitment to spec compliance and cross-platform portability in graphics APIs. While this is a single change, it represents a critical step toward ensuring WebGPU applications behave consistently across different implementations and hardware platforms.

## Detailed Updates

This release focuses on correcting a longstanding specification deviation in WebGPU storage texture usage, bringing Chrome into full compliance with the official WebGPU standard.

### Deprecate bgra8unorm read-only storage texture usage

#### What's New
Chrome 140 deprecates the use of `"bgra8unorm"` format with read-only storage textures in WebGPU. This format will no longer be supported for read-only storage texture operations, correcting a previous implementation bug.

#### Technical Details
The `bgra8unorm` format was incorrectly allowed for read-only storage textures in earlier Chrome versions, despite the WebGPU specification explicitly prohibiting this usage. This format is designed exclusively for write-only access patterns and lacks the portability characteristics required for read operations across different GPU architectures. The deprecation ensures that Chrome's WebGPU implementation strictly adheres to the specification requirements.

#### Use Cases
Developers using WebGPU storage textures should migrate away from `bgra8unorm` format for read-only operations. This change primarily affects:
- GPU compute shaders that read from storage textures
- Graphics pipelines using storage textures for data sampling
- Cross-platform WebGPU applications requiring consistent behavior

The deprecation provides time for developers to update their code before the feature is fully removed in future releases.

#### References
- [issue 427681156](https://issues.chromium.org/issues/427681156)
