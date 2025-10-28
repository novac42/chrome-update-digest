---
layout: default
title: javascript-en
---

## Area Summary

Chrome 141 (stable) focuses on specification alignment and interoperability for JavaScript-accessible WebRTC statistics. The primary change clarifies when RTP statistics objects are created, ensuring consistent behavior across implementations. This improves reliability for developers who observe and analyze media streams via RTP stats, enabling clearer diagnostics and monitoring. The update advances the web platform by tightening spec compliance and reducing ambiguity around stats lifecycle.

## Detailed Updates

Below is the JavaScript-relevant change in Chrome 141, with practical context for developers.

### Align implementations on when RTP stats should be created

#### What's New
RTP stats objects of type "outbound-rtp" or "inbound-rtp" represent a WebRTC stream. The stream is identified by its SSRC (a number). This change aligns Chrome with the specification on when these stats should be created.

#### Technical Details
- The update brings Chrome in line with the W3C WebRTC Stats specification regarding the creation timing of RTP statistics objects.
- Objects are keyed by SSRC and represent "outbound-rtp" or "inbound-rtp" streams within the RTP statistics hierarchy.

#### Use Cases
- More consistent and predictable stats across browsers for monitoring media quality.
- Clearer, spec-aligned behavior that simplifies debugging and analytics for WebRTC applications.
- Improved interoperability for tools that rely on RTP statistics objects.

#### References
- [Tracking bug](https://issues.chromium.org/issues/406585888)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4580748730040320)
- [Link](https://w3c.github.io/webrtc-stats/#the-rtp-statistics-hierarchy)
