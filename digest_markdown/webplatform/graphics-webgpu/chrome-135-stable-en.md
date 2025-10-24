# Chrome Update Analyzer – Graphics and WebGPU (Chrome 135 Stable)

## Area Summary

Chrome 135 introduces several targeted improvements to the Graphics and WebGPU stack, focusing on developer ergonomics, standards alignment, and platform consistency. Notable changes include streamlined pipeline layout creation, easier access to experimental WebGPU compatibility on Android, and the removal of redundant shader limits. Updates to the Dawn implementation further clarify correct usage patterns and modernize API structures. Collectively, these enhancements simplify GPU programming, reduce friction for cross-platform development, and help advance the maturity and reliability of WebGPU as a core web graphics technology.

## Detailed Updates

Below are the key updates in Chrome 135 for Graphics and WebGPU, with practical insights for developers.

### Allow creating pipeline layout with null bind group layout

#### What's New
Developers can now create pipeline layouts with null bind group layouts, eliminating the need to explicitly define empty bind groups.

#### Technical Details
Previously, an empty bind group required a group with zero bindings, which was cumbersome. Now, null bind group layouts are simply ignored during pipeline layout creation, streamlining the process and reducing boilerplate.

#### Use Cases
This change simplifies pipeline setup, especially for simple shaders or when incrementally building up pipeline configurations. It reduces code complexity and potential errors in WebGPU applications.

#### References
- [issue 377836524](https://issues.chromium.org/issues/377836524)

---

### Easier access to the experimental compatibility mode on Android

#### What's New
The `chrome://flags/#enable-unsafe-webgpu` flag now enables all necessary capabilities for experimental WebGPU compatibility mode on Android.

#### Technical Details
With this flag, developers can request a GPUAdapter in compatibility mode without additional configuration. This unifies the developer experience across platforms and makes it easier to test and deploy WebGPU features on Android devices.

#### Use Cases
Developers targeting Android can more easily experiment with and validate WebGPU features, accelerating cross-platform graphics development and testing.

#### References
- [dawn:389876644](https://issues.chromium.org/issues/389876644)
- [webgpureport.org](https://webgpureport.org)

---

### Remove maxInterStageShaderComponents limit

#### What's New
The `maxInterStageShaderComponents` limit has been removed from WebGPU.

#### Technical Details
This limit was redundant with `maxInterStageShaderVariables`, which already governs the number of inter-stage variables. Its removal simplifies the specification and reduces confusion, aligning Chrome with the evolving WebGPU standard.

#### Use Cases
Shader authors and engine developers benefit from a clearer, less error-prone API surface, with fewer overlapping constraints to manage.

#### References
- [intent to remove](https://groups.google.com/a/chromium.org/g/blink-dev/c/i5oJu9lZPAk)
- [issue 364338810](https://issues.chromium.org/issues/364338810)

---

### Dawn updates

#### What's New
Several updates to the Dawn WebGPU implementation, including stricter sampler usage for depth textures and changes to limit structures.

#### Technical Details
- Filtering samplers can no longer sample depth textures; only non-filtering or comparison samplers are allowed.
- The `WGPURequiredLimits` and `WGPUSupportedLimits` structures have been updated for better clarity and future compatibility.
- Additional bug fixes and improvements are included in this release.

#### Use Cases
These changes enforce correct usage patterns, prevent subtle rendering bugs, and ensure that applications remain compatible with the evolving WebGPU specification.

#### References
- [issue 379788112](https://issues.chromium.org/issues/379788112)
- [issue 374263404](https://issues.chromium.org/issues/374263404)
- [issue 42240793](https://issues.chromium.org/issues/42240793)
- [webgpu-headers PR](https://github.com/webgpu-native/webgpu-headers/pull/509)
- [Debugging Dawn](https://dawn.googlesource.com/dawn/+/HEAD/docs/dawn/debugging.md#tracing-native-gpu-api-usage)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/6998..chromium/7049?n=1000)

---

**File location:**  
`digest_markdown/webplatform/Graphics and WebGPU/chrome-135-stable-en.md`