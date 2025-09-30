# Area Summary

Chrome 136 introduces multimedia features focused on better platform parity for codecs, finer control of captured surfaces, and improved audio and SVG hit-testing semantics. The most impactful changes are HEVC (H.265) support across WebRTC and MediaRecorder and new screen-capture controls (captured surface control and resolution), which enable higher-quality conferencing, recording, and adaptive streaming workflows. AudioContext gains an "interrupted" state to reflect exclusive audio use cases, improving UX and resource handling for VoIP and lid-close scenarios. These updates advance the web platform by exposing device and codec capabilities to web apps, aligning implementations with specs, and enabling more efficient media handling.

## Detailed Updates

The entries below connect the above summary to practical implementation and developer considerations.

### AudioContext Interrupted State

#### What's New
Adds an "interrupted" value to the AudioContextState enum to represent temporary pauses from exclusive audio access (e.g., VoIP) or system actions like closing a laptop lid.

#### Technical Details
- Extends the Web Audio API's AudioContextState per the WebAudio spec.
- Allows user agents to signal non-terminal pauses distinct from "suspended" or "closed".

#### Use Cases
- Conferencing apps can detect interruption vs. normal suspend and adapt UI/behavior.
- Media players can preserve playback state and restore it after exclusive audio ends.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=374805121
- https://chromestatus.com/feature/5087843301908480
- https://webaudio.github.io/web-audio-api/#AudioContextState

### Captured surface control

#### What's New
Introduces a Web API that permits forwarding wheel events to a captured tab and reading/changing the zoom level of a captured tab.

#### Technical Details
- API targets scenarios where the capturing context needs fine-grained control over user interactions and visual scaling of the remote/captured surface.
- Follows the WICG proposal for captured surface control.

#### Use Cases
- Screen-sharing UIs that want to forward scroll gestures into the captured content.
- Remote-control flows that need to adjust zoom to improve legibility or bandwidth usage.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=1466247
- https://chromestatus.com/feature/5064816815276032
- https://wicg.github.io/captured-surface-control/

### CapturedSurfaceResolution

#### What's New
Exposes the pixel ratio of the captured surface during screen sharing so apps can account for physical vs. logical resolution.

#### Technical Details
- Surface pixel ratio information allows callers to know devicePixelRatio or equivalent for the captured source.
- Spec aligns with mediacapture-screen-share-extensions extension points.

#### Use Cases
- Adaptive encoders can choose resolution/bitrate trade-offs based on source pixel density.
- Recording and streaming apps can avoid unnecessary up/downscaling and conserve CPU/GPU resources.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=383946052
- https://chromestatus.com/feature/5100866324422656
- https://w3c.github.io/mediacapture-screen-share-extensions/#capturedsurfaceresolution

### H265 (HEVC) codec support in WebRTC

#### What's New
HEVC (H.265) is added to the set of codecs available for WebRTC; support is discoverable via the MediaCapabilities API.

#### Technical Details
- HEVC becomes a queryable codec capability alongside VP8/VP9/H.264/AV1.
- Integration follows RTCRtpCodecCapability semantics in the WebRTC spec.

#### Use Cases
- Enterprises and workflows that prefer HEVC for efficiency on supported hardware can negotiate it in peer connections.
- MediaCapabilities queries enable adaptive UX: choose codecs based on hardware/software availability.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=391903235
- https://chromestatus.com/feature/5104835309936640
- https://www.w3.org/TR/webrtc/#dom-rtcrtpcodeccapability

### H26x Codec support updates for MediaRecorder

#### What's New
MediaRecorder now supports HEVC encoding with the `hvc1.*` codec string and adds `hev1.*` and `avc3.*` codec strings for variable-resolution MP4 support. This follows platform encoding support added to WebCodecs in earlier releases.

#### Technical Details
- Expands MediaRecorder's output codec identifiers to reflect modern container and codec signaling.
- Enables recording workflows that rely on platform HEVC encoders when available.

#### Use Cases
- High-efficiency local recording with HEVC for lower storage or bandwidth.
- Recording variable-resolution MP4 outputs that interoperate with downstream tools expecting `avc3`/`hev1`/`hvc1` tags.

#### References
- https://chromestatus.com/feature/5103892473503744

### Use DOMPointInit for getCharNumAtPosition, isPointInFill, isPointInStroke

#### What's New
Chromium updated SVGGeometryElement and SVGPathElement APIs to use DOMPointInit instead of SVGPoint for getCharNumAtPosition, isPointInFill, and isPointInStroke, aligning with the latest W3C spec.

#### Technical Details
- API surface change to accept DOMPointInit (plain object) rather than SVGPoint instances.
- Improves consistency with modern DOM point handling and reduces legacy API dependencies.

#### Use Cases
- SVG hit-testing and text layout code can pass simple JS objects for point coordinates.
- Easier interop with other DOM APIs and less reliance on legacy SVG object creation.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40572887
- https://chromestatus.com/feature/5084627093929984
- https://www.w3.org/TR/SVG2/types.html#InterfaceDOMPointInit

Saved file:
digest_markdown/webplatform/Multimedia/chrome-136-stable-en.md