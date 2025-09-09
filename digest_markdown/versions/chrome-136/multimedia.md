---
layout: default
title: Chrome 136 - Multimedia
---

# Chrome 136 - Multimedia

[← Back to Chrome 136](./) | [View All Multimedia Updates](/areas/multimedia/)

## Images and media

### AudioContext Interrupted State

Adds an "interrupted" state to `AudioContextState`. This new state lets the User Agent pause playback during exclusive audio access (VoIP) or when a laptop lid is closed.

**References:** [Tracking bug #374805121](https://bugs.chromium.org/p/chromium/issues/detail?id=374805121) | [ChromeStatus.com entry](https://chromestatus.com/feature/5087843301908480) | [Spec](https://webaudio.github.io/web-audio-api/#AudioContextState)

### Captured surface control

A Web API that lets web applications:
- Forward wheel events to a captured tab.
- Read and change the zoom level of a captured tab.

**References:** [Tracking bug #1466247](https://bugs.chromium.org/p/chromium/issues/detail?id=1466247) | [ChromeStatus.com entry](https://chromestatus.com/feature/5064816815276032) | [Spec](https://wicg.github.io/captured-surface-control/)

### CapturedSurfaceResolution

Expose pixel ratio of the captured surface while screensharing. This feature helps applications to conserve their system resources or adapt the quality over bandwidth trade-off according to the physical and logical resolutions of the captured surface.

**References:** [Tracking bug #383946052](https://bugs.chromium.org/p/chromium/issues/detail?id=383946052) | [ChromeStatus.com entry](https://chromestatus.com/feature/5100866324422656) | [Spec](https://w3c.github.io/mediacapture-screen-share-extensions/#capturedsurfaceresolution)

### H265 (HEVC) codec support in WebRTC

After this change, HEVC will join VP8, H.264, VP9, and AV1 as supported codecs in WebRTC. Support will be queryable using the MediaCapabilities API.

**References:** [Tracking bug #391903235](https://bugs.chromium.org/p/chromium/issues/detail?id=391903235) | [ChromeStatus.com entry](https://chromestatus.com/feature/5104835309936640) | [Spec](https://www.w3.org/TR/webrtc/#dom-rtcrtpcodeccapability)

### H26x Codec support updates for MediaRecorder

Chromium's MediaRecorder API now supports HEVC encoding, introducing the `hvc1.*` codec string, and adds new codecs (`hev1.*` and `avc3.*`) supporting variable resolution video in MP4. Support for HEVC platform encoding was added in WebCodecs in Chromium M130. As a follow-up, support has been added to the MediaRecorder API in Chromium. The API now supports both MP4 and Matroska muxer types with different HEVC and H.264 mime type specifications. HEVC encoding is only supported if the user's device and operating system provide the necessary capabilities.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5103892473503744)

### Use DOMPointInit for getCharNumAtPosition, isPointInFill, isPointInStroke

This change brings Chromium code in line with the latest W3C specification for `SVGGeometryElement` and `SVGPathElement` in terms of use of `DOMPointInit` over `SVGPoint` for `getCharNumAtPosition`, `isPointInFill`, `isPointInStroke`.

**References:** [Tracking bug #40572887](https://bugs.chromium.org/p/chromium/issues/detail?id=40572887) | [ChromeStatus.com entry](https://chromestatus.com/feature/5084627093929984) | [Spec](https://www.w3.org/TR/SVG2/types.html#InterfaceDOMPointInit)


---

## Navigation
- [Chrome 136 Overview](./)
- [All Multimedia Updates](/areas/multimedia/)
- [Browse Other Areas](./)
