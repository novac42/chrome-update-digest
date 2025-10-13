## Area Summary

Chrome 141’s Multimedia updates center on WebRTC media processing and audio capture controls. WebRTC Encoded Transform (V2) enables processing of encoded media flowing through RTCPeerConnection and aligns Chrome with the latest specification and other browsers. The new echoCancellationMode for getUserMedia() refines audio input behavior by extending existing constraints with additional values. Together, these changes improve cross‑browser interoperability and give developers finer, standards-aligned control over real-time media quality.

## Detailed Updates

These updates build on the themes of interoperable real-time media processing and improved audio capture configurability.

### WebRTC Encoded Transform (V2)

#### What's New
Enables processing of encoded media as it flows through an RTCPeerConnection, updating Chrome to the newer version of the API.

#### Technical Details
- Chrome previously shipped an early version of this API in 2020; the specification has since changed.
- Other browsers have already shipped the updated version (Safari in 2022 and Firefox in 2023).
- This launch aligns Chrome with the updated specification and cross‑browser behavior.

#### Use Cases
- Real-time handling of encoded media in WebRTC pipelines for scenarios that need access to encoded data.

#### References
- Tracking bug #354881878: https://issues.chromium.org/issues/354881878
- ChromeStatus.com entry: https://chromestatus.com/feature/5175278159265792
- Spec: https://github.com/w3c/webrtc-encoded-transform

### `echoCancellationMode` for `getUserMedia()`

#### What's New
Extends the echoCancellation behavior of the MediaTrackConstraints dictionary to accept the values "all" and "remote-only" in addition to true/false.

#### Technical Details
- Applies to audio tracks received from microphones.
- Provides additional modes to modify echo cancellation behavior.

#### Use Cases
- Fine-tuned control over microphone echo cancellation to suit application audio needs.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5585747985563648
- Spec: https://www.w3.org/TR/mediacapture-streams/#dom-echocancellationmodeenum