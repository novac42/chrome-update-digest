---
layout: default
title: Chrome 140 Stable - Devices Updates
---

# Chrome 140 Stable - Devices Updates

## Area Summary

Chrome 140 brings an important WebGPU specification compliance update that affects device management workflows for developers working with GPU acceleration. The key change involves implementing proper adapter consumption semantics, where WebGPU adapters are now correctly marked as "consumed" after successful device requests. This update ensures Chrome's WebGPU implementation aligns with the official specification, providing more predictable behavior for applications that rely on GPU device management. While this is a single focused change, it represents a critical step toward full WebGPU specification compliance and will help developers build more robust graphics applications.

## Detailed Updates

This release focuses on a crucial WebGPU specification alignment that impacts how developers handle GPU device requests in their applications.

### Device requests consume adapter

#### What's New
WebGPU adapters are now properly marked as "consumed" after a successful device request, aligning Chrome's implementation with the official WebGPU specification. This means subsequent `requestDevice()` calls on the same adapter will be rejected with a promise rejection.

#### Technical Details
According to the WebGPU specification, when an adapter successfully creates a device through `requestDevice()`, the adapter transitions to a "consumed" state. This prevents multiple device requests from the same adapter instance, ensuring proper resource management and preventing potential conflicts in GPU device allocation.

#### Use Cases
This change is particularly important for developers building WebGPU applications that need to:
- Implement proper error handling for device request failures
- Manage multiple GPU adapters in complex graphics applications
- Ensure predictable behavior when working with GPU resources across different browser implementations
- Build robust WebGPU applications that comply with the specification

#### References
- [WebGPU specification](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1)
- [issue 415825174](https://issues.chromium.org/issues/415825174)
```

The digest has been saved to `digest_markdown/webplatform/Devices/chrome-140-stable-en.md`.
