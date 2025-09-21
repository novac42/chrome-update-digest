# Chrome 140 Storage Update Analysis

## Summary

Chrome 140 introduces a significant deprecation in the **storage** domain affecting WebGPU storage textures. The most notable change is the deprecation of `bgra8unorm` format for read-only storage texture usage, aligning Chrome's implementation with the WebGPU specification to improve portability and correct a previous implementation bug.

## Feature Details

### Deprecate bgra8unorm read-only storage texture usage

**What Changed**:
Chrome 140 deprecates the use of `"bgra8unorm"` format with read-only storage textures in WebGPU. This change corrects a previous implementation bug where Chrome incorrectly allowed this format for read-only storage textures. The WebGPU specification explicitly prohibits this usage because the `bgra8unorm` format is designed exclusively for write-only access. This deprecation ensures better portability across different WebGPU implementations and brings Chrome into compliance with the official WebGPU specification. Developers using this format combination should migrate to appropriate alternative formats that are properly supported for read-only storage texture operations.

**References**:
- [issue 427681156](https://issues.chromium.org/issues/427681156)