---
layout: default
title: chrome-143-en
---

### 1. Area Summary

Chrome 143 introduces a targeted WebRTC signaling change that stabilizes RTP header extension ordering across subsequent offer/answer exchanges. The main theme is increased determinism in WebRTC negotiation to avoid unintended remapping of header extensions, reducing breakage for real-time multimedia apps and middleboxes. This change is most impactful for developers of WebRTC SDKs, SFUs, and complex peer-to-peer apps that rely on stable extension slot assignments. By aligning implementation with the spec, the platform improves interoperability and simplifies developer reasoning about RTP extension handling during renegotiation.

## Detailed Updates

The single Multimedia update in this release tightens how RTP header extensions are handled across offers/answers; details and practical implications are listed below.

### WebRTC RTP header extension behavior change

#### What's New
The offer/answer behavior is changed so that subsequent offers or answers do not permute (reorder or remap) RTP header extensions already negotiated unless the user explicitly requests such modification.

#### Technical Details
- Implements the specification change in the WebRTC extensions draft to keep extension mapping stable across renegotiation by default.
- Affects the SDP/RTCPeerConnection offer/answer flow and how header extension IDs and mappings are preserved.
- Intention is to prevent implicit permutation of negotiated extension slots, reducing surprising runtime remapping.

#### Use Cases
- SFUs and media servers that rely on consistent header extension indices to process features like audio level, MID, or timestamp offsets will see fewer disruptions on renegotiation.
- WebRTC SDKs and applications that programmatically manipulate offers/answers can assume stable extension mappings unless they opt into change.
- Simplifies debugging and avoids transient media-processing issues caused by unexpected extension remapping during mid-call renegotiation.

#### References
- [Tracking bug #439514253](https://issues.chromium.org/issues/439514253)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5135528638939136)  
- [Spec](https://w3c.github.io/webrtc-extensions/#rtp-header-extension-control-modifications)

Saved to: digest_markdown/webplatform/Multimedia/chrome-143-stable-en.md
