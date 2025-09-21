# Chrome 140 Stable - Devices Update Analysis

## Summary

Chrome 140 introduces an important WebGPU specification compliance update in the **Devices** area. The key change involves adapter consumption behavior, where WebGPU adapters are now properly marked as "consumed" after successful device requests, preventing multiple device creations from the same adapter as per the WebGPU specification.

## Feature Details

### Device requests consume adapter

**What Changed**:
This update implements proper WebGPU adapter state management according to the official specification. When a WebGPU adapter successfully creates a device through `requestDevice()`, the adapter is now marked as "consumed" and cannot be used for subsequent device requests. Any additional `requestDevice()` calls on the same consumed adapter will result in a rejected promise, ensuring compliance with the WebGPU specification and preventing potential resource conflicts or undefined behavior.

This change affects developers working with WebGPU applications who need to manage GPU device creation and adapter lifecycle properly. Applications that previously relied on reusing adapters for multiple device requests will need to be updated to request fresh adapters for each device creation.

**References**:
- [WebGPU specification](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1)
- [issue 415825174](https://issues.chromium.org/issues/415825174)