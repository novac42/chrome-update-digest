---
layout: default
title: chrome-140-en
---

## Area Summary

Chrome 140 (stable) tightens WebGPU storage texture behavior by deprecating the use of "bgra8unorm" with read-only storage textures. The most impactful change for developers is that existing code relying on this previously-allowed pattern will need to be updated for portability and spec compliance. This aligns Chrome with the WebGPU specification, reducing platform inconsistencies and surprising behavior. These updates improve cross-platform graphics reliability and reduce the risk of subtle rendering or compatibility bugs in GPU-accelerated web apps.

## Detailed Updates

This section expands the summary into the single storage-related change in Chrome 140 and what developers should track.

### Deprecate bgra8unorm read-only storage texture usage

#### What's New
Using "bgra8unorm" format with read-only storage textures is now deprecated in Chrome 140. The WebGPU specification disallows this usage; Chrome's prior allowance was a bug.

#### Technical Details
The deprecation reflects that "bgra8unorm" is intended for write-only access and is not portable across implementations. Chrome's change brings its WebGPU behavior in line with the spec to avoid non-portable usage patterns.

#### Use Cases
- WebGPU-based applications and shaders that relied on read-only storage textures with "bgra8unorm" must be updated to avoid relying on this pattern.
- Developers should audit storage texture usages and switch to spec-compliant access patterns or alternative formats that are explicitly supported for read access to ensure portability across browsers and GPUs.

#### References
- issue 427681156: https://issues.chromium.org/issues/427681156

Output file: digest_markdown/webplatform/storage/chrome-140-stable-en.md
