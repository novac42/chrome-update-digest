---
layout: default
title: chrome-139-en
---

## Area Summary

Chrome 139 adds a metadata exposure for audio level on encoded WebRTC frames, enabling developers to read per-frame audio loudness from transmitted encoded audio. The change surfaces encoded-frame audio level via the WebRTC encoded transform pipeline and the RTCEncodedAudioFrameMetadata API, improving observability and enabling level-based features without decoding. This is impactful for real-time analytics, voice activity detection, and adaptive UX while keeping processing on the encoded path for performance. These updates advance the web platform by standardizing a low-cost metadata channel for audio telemetry in peer-to-peer streams.

## Detailed Updates

Below are the detailed changes that implement the summary above and their practical implications for multimedia engineers.

### Audio level for RTC encoded frames

#### What's New
Exposes an audio level value for an encoded audio frame transmitted over RTCPeerConnection and surfaced via the WebRTC encoded transform API, allowing developers to access per-frame loudness metadata.

#### Technical Details
- The spec-defined metadata field is available on RTCEncodedAudioFrameMetadata as an audioLevel attribute (see spec link).
- This operates on encoded frames within the encoded-transform pipeline, so inspection can occur without full decode, reducing CPU and latency compared to decoding for level analysis.
- Implementation integration points: WebRTC encoded transform hooks and RTCPeerConnection encoded frame path; interacts with codec-encoded payloads and their associated metadata.

#### Use Cases
- Real-time voice activity detection and presence indicators in conferencing UIs without additional decoding.
- Lightweight metrics and analytics pipelines that aggregate audio level histograms or trigger events (e.g., mute suggestions, auto-gain) on the sender/transit side.
- Adaptive UX or network strategies that use level metadata to prioritize active speakers or trigger bitrate/silence suppression policies.
- Useful for low-overhead monitoring in large-scale deployments and for client-side visualizations of audio without adding decode cost.

#### Security & Privacy Notes
- Audio level is telemetry that may reveal speech activity patterns; treat as potentially sensitive and follow user consent policies and local privacy regulations.
- Consider CSP/CORS and application-level handling when sending audio-level telemetry to remote servers; ensure appropriate user disclosure.

#### References
- https://issues.chromium.org/issues/418116079
- https://chromestatus.com/feature/5206106602995712
- https://w3c.github.io/webrtc-encoded-transform/#dom-rtcencodedaudioframemetadata-audiolevel

Save to:
```text
digest_markdown/webplatform/Multimedia/chrome-139-stable-en.md
