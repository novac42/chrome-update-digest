---
layout: default
title: storage-en
---

## Area Summary

Chrome 140's storage changes focus on tightening WebGPU behavior by deprecating the use of the "bgra8unorm" format with read-only storage textures. This enforces the WebGPU specification, removing a previous Chrome-specific allowance that was a portability and correctness bug. The most impactful change for developers is to stop using bgra8unorm as a read-only storage texture and to align texture usage with spec-intended (write-only) semantics. This update improves cross-browser compatibility and predictable GPU resource handling on the web platform.

## Detailed Updates

The single update below follows from the summary: Chrome is moving to spec-conformant handling of a WebGPU storage texture format that was previously misallowed.

### Deprecate bgra8unorm read-only storage texture usage

#### What's New
Using "bgra8unorm" format with read-only storage textures is now deprecated. The WebGPU specification explicitly disallows this, and its prior allowance in Chrome was a bug, as this format is intended for write-only access and is not portable.

#### Technical Details
- This enforces WebGPU spec constraints for storage textures: "bgra8unorm" should not be used with read-only storage binding usage.
- Chrome's prior behavior was non-conforming; the change removes that non-portable exception.
- Developers relying on read-only sampling or shader reads from storage textures in bgra8unorm must adjust to spec-compliant formats/usages.

#### Use Cases
- WebGPU graphics and compute workloads that previously used bgra8unorm as a read-only storage texture need to be migrated to supported formats or change texture usage to write-only where appropriate.
- Ensures more consistent behavior across browsers and GPU vendors, reducing platform-specific bugs and improving portability of shader code and resource management.

#### References
- issue 427681156: https://issues.chromium.org/issues/427681156

## Area-Specific Expertise (storage-focused implications)
- graphics-webgpu: This change directly affects WebGPU storage textures and shader resource bindings; update shaders and pipeline layouts to avoid read-only bgra8unorm usage.
- webapi: WebGPU API consumers must validate texture formats and usages against spec rules to prevent runtime errors.
- performance: Moving to spec-compliant patterns avoids undefined behavior that can cause unpredictable GPU performance across devices.
- security-privacy: Spec-conformance reduces platform-specific quirks that could lead to unexpected resource access patterns.
- deprecations: Treat this as a deprecation warning; migrate code to supported formats/usages to maintain future compatibility.

Save file to: digest_markdown/webplatform/storage/chrome-140-stable-en.md
