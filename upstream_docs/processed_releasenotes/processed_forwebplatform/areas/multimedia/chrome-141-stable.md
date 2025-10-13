## WebRTC

### WebRTC Encoded Transform (V2)

This API allows processing of encoded media flowing through an `RTCPeerConnection`. Chrome shipped an early version of this API in 2020. Since then, the specification has changed and other browsers have shipped the updated version (Safari in 2022 and Firefox in 2023). This launch aligns Chrome with the updated specification as part of Interop 2025.

This launch does not cover the `generateKeyFrame method`, which is still under discussion.

[Tracking bug #354881878](https://issues.chromium.org/issues/354881878) | [ChromeStatus.com entry](https://chromestatus.com/feature/5175278159265792) | [Spec](https://github.com/w3c/webrtc-encoded-transform)

### `echoCancellationMode` for `getUserMedia()`

Extends the `echoCancellation` behavior of the `MediaTrackConstraints` dictionary. his previously accepted `true` or `false` and now additionally accepts the values `"all"` and `"remote-only"`. This lets clients modify echo cancellation behavior applied to audio tracks received from microphones, controlling how much of the user system playout (all, or only audio received from `PeerConnections`) is removed from the microphone signal.

[ChromeStatus.com entry](https://chromestatus.com/feature/5585747985563648) | [Spec](https://www.w3.org/TR/mediacapture-streams/#dom-echocancellationmodeenum)
