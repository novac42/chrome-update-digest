---
layout: default
title: deprecations-en
---

## Area Summary

Chrome 138 deprecates the WebGPU API attribute GPUAdapter.isFallbackAdapter, consolidating fallback information into GPUAdapterInfo.isFallbackAdapter. This reduces redundancy in the WebGPU surface of the platform and requires small migration updates for code that inspected the old attribute. For developers, the most impactful change is updating runtime checks and tests to reference GPUAdapterInfo rather than GPUAdapter. This streamlines the WebGPU API surface and reduces maintenance surface for the platform.

## Detailed Updates

Below are the Deprecations entries relevant to WebGPU in Chrome 138 and what teams should do next.

### WebGPU: Deprecate GPUAdapter isFallbackAdapter attribute

#### What's New
The GPUAdapter.isFallbackAdapter boolean attribute is deprecated because it duplicates the GPUAdapterInfo.isFallbackAdapter attribute.

#### Technical Details
The attribute will be removed in a future change; code should not rely on GPUAdapter.isFallbackAdapter. Instead, obtain fallback information from GPUAdapterInfo.isFallbackAdapter exposed by the adapter info structure.

#### Use Cases
- Update feature detection and runtime checks to read GPUAdapterInfo.isFallbackAdapter.
- Adjust unit and integration tests that assert GPUAdapter.isFallbackAdapter.
- Audit code paths that branch on fallback adapters (e.g., capability workarounds) and migrate them to use adapter info.

#### References
- Tracking bug #409259074: https://bugs.chromium.org/p/chromium/issues/detail?id=409259074
- ChromeStatus.com entry: https://chromestatus.com/feature/5125671816847360
- Spec: https://gpuweb.github.io/gpuweb/#gpu-adapter
