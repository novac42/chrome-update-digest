---
layout: default
title: deprecation-en
---

### 1. Area Summary

Chrome 138 deprecations focus on streamlining the WebGPU API surface by removing a redundant attribute. The most impactful change is the deprecation of the GPUAdapter.isFallbackAdapter attribute in favor of GPUAdapterInfo.isFallbackAdapter (introduced in Chrome 136), a minor breaking change for WebGPU consumers. This reduces API duplication and clarifies where adapter metadata belongs, aiding portability and spec conformance. Developers using WebGPU should migrate checks to GPUAdapterInfo to avoid future breakage.

## Detailed Updates

Below are the deprecation items in Chrome 138 relevant to WebGPU and migration guidance.

### WebGPU: Deprecate GPUAdapter isFallbackAdapter attribute

#### What's New
Deprecates the GPUAdapter `isFallbackAdapter` boolean attribute because it is redundant with `GPUAdapterInfo.isFallbackAdapter`.

#### Technical Details
The attribute removal is an intentional API simplification: adapter fallback information is consolidated under `GPUAdapterInfo`. The change is a minor breaking change for code that reads `GPUAdapter.isFallbackAdapter`.

#### Use Cases
Update WebGPU code that inspects adapter fallback status to use `GPUAdapter.requestAdapter()` → examine `adapter.adapterInfo.isFallbackAdapter` (or the equivalent `GPUAdapterInfo` surface) to remain compatible.

#### References
https://bugs.chromium.org/p/chromium/issues/detail?id=409259074
https://chromestatus.com/feature/5125671816847360
https://gpuweb.github.io/gpuweb/#gpu-adapter

### Deprecation of GPUAdapter isFallbackAdapter Attribute

#### What's New
The `isFallbackAdapter` attribute for `GPUAdapter` is deprecated and replaced by `GPUAdapterInfo.isFallbackAdapter`, introduced in Chrome 136.

#### Technical Details
The deprecation directs developers to the `GPUAdapterInfo` attribute as the canonical source of fallback metadata for adapters, consolidating adapter metadata.

#### Use Cases
Migrate any direct reads of `GPUAdapter.isFallbackAdapter` to the `GPUAdapterInfo.isFallbackAdapter` field to avoid future incompatibilities.

#### References
None provided.

File to save:
```text
digest_markdown/webplatform/deprecation/chrome-138-stable-en.md
