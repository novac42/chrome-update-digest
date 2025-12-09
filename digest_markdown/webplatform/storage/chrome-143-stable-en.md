## Area Summary

Chrome 143 (stable) removes support for using the "bgra8unorm" format with read-only storage textures in WebGPU. This change aligns Chrome with the WebGPU specification by eliminating a prior allowance that was a browser bug. For developers, the most impactful result is that shaders and binding layouts that relied on read-only storage textures with this format will need to be updated to use a different format or usage pattern. This update increases cross-browser consistency for WebGPU and reduces surprising platform-specific behavior.

## Detailed Updates

The item below expands on the summary and explains developer impact and remediation.

### Remove bgra8unorm read-only storage texture usage

#### What's New
Chrome no longer permits using the "bgra8unorm" texture format for read-only storage textures in WebGPU. The prior behavior in Chrome that allowed this was a bug and has been removed.

#### Technical Details
The WebGPU specification explicitly disallows "bgra8unorm" for read-only storage texture usage, and Chrome's implementation has been changed to match the spec. Expect errors or validation failures for pipeline or bind-group setups that attempted this combination; update texture formats or usages to conform to the spec.

#### Use Cases
- Graphics/WebGPU: Update shaders and bind group layouts that assumed read-only storage access to bgra8unorm textures.
- WebAPI & JavaScript: Adjust resource creation and validation logic in apps and libraries to avoid creating disallowed texture usages.
- Performance & Portability: Aligning with the spec prevents platform-specific fallbacks and ensures predictable cross-browser behavior.

#### References
- [issue 427681156](https://issues.chromium.org/issues/427681156)

File saved to: digest_markdown/webplatform/storage/chrome-143-stable-en.md