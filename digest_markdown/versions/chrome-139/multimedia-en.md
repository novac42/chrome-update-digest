---
layout: default
title: multimedia-en
---

## Area Summary

Chrome 139 (stable) advances multimedia by exposing richer runtime metadata and improving credential mediation that affects media UX. The two standout changes are: a new audio-level exposure for encoded WebRTC frames, and an "immediate" mediation mode for navigator.credentials.get(). These updates help developers build more responsive real-time-audio features (metering, VAD, telemetry) and smoother authentication flows that can be important for media apps. Together they push the web platform toward lower-level media observability and faster credential-driven UX.

## Detailed Updates

Below are concise, developer-focused explanations of each Multimedia-area change and why they matter to real-time media applications and services.

### Audio level for RTC encoded frames

#### What's New
This feature exposes the audio level of an encoded audio frame transmitted via RTCPeerConnection and surfaced to web code using WebRTC encoded transforms.

#### Technical Details
The capability is defined in the encoded-transform WebRTC specification for RTCEncodedAudioFrame metadata (see spec link). It surfaces per-frame audio level information from encoded frames so web-level transforms and analytics can access energy/level metrics without decoding raw PCM.

#### Use Cases
- Voice activity detection or mute detection implemented in an encoded-transform without full decode.
- UI-level audio meters and per-participant level telemetry for diagnostics and analytics.
- Adaptive bitrate or codec selection heuristics informed by per-frame energy measurements.
- Content moderation and level-based recording triggers inside encoded transforms.

#### References
- https://issues.chromium.org/issues/418116079
- https://chromestatus.com/feature/5206106602995712
- https://w3c.github.io/webrtc-encoded-transform/#dom-rtcencodedaudioframemetadata-audiolevel

### Web Authentication immediate mediation

#### What's New
Adds an "immediate" mediation mode for navigator.credentials.get() that prompts the browser sign-in UI only when a passkey or password for the site is immediately known to the browser; otherwise the call rejects with NotAllowedError.

#### Technical Details
This mediation mode is surfaced as an additional option to navigator.credentials.get() (origin-trial-tagged in this release). It changes the credential selection UX to be immediate-only, avoiding fallback prompts when no known credential exists. See the linked spec PR and tracking bug for implementation notes and origin-trial status.

#### Use Cases
- Fast sign-in paths for media services where reduced friction improves playback/auth flow.
- Deterministic credential flow in embedded or automated media clients that need to know immediately whether a browser-held credential is available.
- Passwordless/passkey-first UX in media-oriented web apps that must minimize interruption to playback or capture flows.

#### References
- https://issues.chromium.org/issues/408002783
- https://chromestatus.com/feature/5164322780872704
- https://github.com/w3c/webauthn/pull/2291

File saved to: digest_markdown/webplatform/Multimedia/chrome-139-stable-en.md
