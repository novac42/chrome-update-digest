---
layout: default
title: devices-en
---

## Area Summary

Chrome 140 (stable) introduces an important WebGPU lifecycle change affecting device creation on devices. The update enforces the WebGPU specification rule that an adapter becomes "consumed" after a successful device request, altering how repeated device requests are handled. This is the most impactful change for Devices developers because it changes device creation patterns and requires explicit handling of adapter state. The change advances the platform by aligning Chromium with the GPUWeb spec, improving clarity of adapter/device lifetimes and resource management.

## Detailed Updates

This section expands on the summary above and explains the concrete change developers must account for.

### Device requests consume adapter

#### What's New
According to the WebGPU specification, an adapter is marked as "consumed" upon a successful device request. Consequently, subsequent `requestDevice()` calls using the same adapter will now result in a rejected promise.

#### Technical Details
- Adapter state transitions now follow the GPUWeb "adapter consumed" semantics: once `requestDevice()` succeeds for an adapter, that adapter is considered consumed.
- Any later `requestDevice()` invocation on the same adapter instance will be rejected rather than returning another device.

#### Use Cases
- Update code and libraries to call `requestDevice()` once per adapter or obtain a new adapter via `requestAdapter()` if another device is needed.
- Add robust promise rejection handling around `requestDevice()` to surface adapter-consumed errors.
- Adjust initialization flows in rendering engines, frameworks, and workers that assumed multiple devices could be created from the same adapter.

#### References
- WebGPU specification: https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1  
- issue 415825174: https://issues.chromium.org/issues/415825174
