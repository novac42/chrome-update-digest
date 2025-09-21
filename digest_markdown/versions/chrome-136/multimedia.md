---
layout: default
title: Chrome 136 Multimedia Updates - Developer Analysis
---

# Chrome 136 Multimedia Updates - Developer Analysis

## Area Summary

Chrome 136 delivers significant advancements in multimedia capabilities, focusing on enhanced audio management, screen capture control, and codec support expansion. The most impactful changes include the new AudioContext interrupted state for better audio session handling, comprehensive captured surface control APIs for screen sharing applications, and expanded codec support with H265/HEVC integration in WebRTC and MediaRecorder. These updates collectively strengthen Chrome's position as a platform for high-quality multimedia applications, providing developers with more granular control over audio contexts, advanced screen sharing capabilities, and broader codec compatibility for modern video streaming and recording workflows.

## Detailed Updates

Building on Chrome's multimedia foundations, this release introduces several developer-focused enhancements that expand control and compatibility across audio, video, and screen capture domains.

### AudioContext Interrupted State

#### What's New
Introduces a new "interrupted" state to the AudioContextState enumeration, allowing User Agents to pause audio playbook during exclusive audio access scenarios or hardware events like laptop lid closure.

#### Technical Details
The interrupted state extends the existing AudioContext state machine, providing a standardized way for browsers to handle audio interruptions without terminating the entire audio context. This state preserves the audio graph while temporarily suspending playback, enabling seamless resumption when the interruption ends.

#### Use Cases
- VoIP applications can gracefully handle exclusive audio access requirements
- Media players can respond appropriately to hardware events like lid closure
- Audio applications gain better integration with system-level audio management
- Developers can implement more robust audio session handling

#### References
[Tracking bug #374805121](https://bugs.chromium.org/p/chromium/issues/detail?id=374805121) | [ChromeStatus.com entry](https://chromestatus.com/feature/5087843301908480) | [Spec](https://webaudio.github.io/web-audio-api/#AudioContextState)

### Captured Surface Control

#### What's New
A comprehensive Web API that enables web applications to interact with captured surfaces by forwarding wheel events and managing zoom levels of captured tabs during screen sharing sessions.

#### Technical Details
The API provides direct control mechanisms for captured surfaces, allowing applications to relay user interactions like wheel scrolling to the captured content and programmatically adjust zoom levels. This creates a more interactive screen sharing experience by bridging the gap between the capturing and captured contexts.

#### Use Cases
- Screen sharing applications can enable interactive remote desktop experiences
- Collaborative tools can allow participants to navigate shared content directly
- Remote support applications gain enhanced control capabilities
- Video conferencing platforms can offer more engaging screen sharing features

#### References
[Tracking bug #1466247](https://bugs.chromium.org/p/chromium/issues/detail?id=1466247) | [ChromeStatus.com entry](https://chromestatus.com/feature/5064816815276032) | [Spec](https://wicg.github.io/captured-surface-control/)

### CapturedSurfaceResolution

#### What's New
Exposes the pixel ratio of captured surfaces during screen sharing, providing applications with detailed information about both physical and logical resolutions of the shared content.

#### Technical Details
This feature reveals the relationship between physical pixels and logical units on the captured surface, enabling applications to make informed decisions about resource allocation and quality optimization. Applications can now adapt their processing pipeline based on the actual resolution characteristics of the captured content.

#### Use Cases
- Video conferencing applications can optimize bandwidth usage based on actual pixel density
- Screen recording tools can adjust quality settings to match source resolution
- Remote desktop applications can implement intelligent scaling algorithms
- Streaming platforms can adapt compression parameters for optimal visual quality

#### References
[Tracking bug #383946052](https://bugs.chromium.org/p/chromium/issues/detail?id=383946052) | [ChromeStatus.com entry](https://chromestatus.com/feature/5100866324422656) | [Spec](https://w3c.github.io/mediacapture-screen-share-extensions/#capturedsurfaceresolution)

### H265 (HEVC) codec support in WebRTC

#### What's New
Adds H265/HEVC codec support to WebRTC, expanding the available codec options alongside VP8, H.264, VP9, and AV1. Support is discoverable through the MediaCapabilities API for runtime codec availability detection.

#### Technical Details
HEVC integration in WebRTC provides superior compression efficiency compared to older codecs, potentially reducing bandwidth requirements while maintaining video quality. The implementation follows WebRTC codec capability standards and integrates with existing codec negotiation mechanisms.

#### Use Cases
- Video conferencing applications can leverage superior compression for bandwidth-constrained scenarios
- Live streaming platforms gain access to more efficient encoding options
- Mobile applications can reduce data usage while maintaining video quality
- Enterprise video solutions can optimize network utilization

#### References
[Tracking bug #391903235](https://bugs.chromium.org/p/chromium/issues/detail?id=391903235) | [ChromeStatus.com entry](https://chromestatus.com/feature/5104835309936640) | [Spec](https://www.w3.org/TR/webrtc/#dom-rtcrtpcodeccapability)

### H26x Codec support updates for MediaRecorder

#### What's New
MediaRecorder API now supports HEVC encoding with the `hvc1.*` codec string and introduces new codec variants (`hev1.*` and `avc3.*`) that support variable resolution video in MP4 containers.

#### Technical Details
This update builds on the HEVC platform encoding support added to WebCodecs in Chrome 130, extending codec support to MediaRecorder for consistent video recording capabilities. The new codec strings provide more granular control over encoding parameters and container compatibility.

#### Use Cases
- Screen recording applications can leverage HEVC's compression efficiency
- Video editing tools gain access to modern codec variants
- Content creation platforms can offer improved recording quality
- Mobile applications can create smaller video files with maintained quality

#### References
[ChromeStatus.com entry](https://chromestatus.com/feature/5103892473503744)

### Use DOMPointInit for getCharNumAtPosition, isPointInFill, isPointInStroke

#### What's New
Updates SVGGeometryElement and SVGPathElement methods to use DOMPointInit instead of SVGPoint for `getCharNumAtPosition`, `isPointInFill`, and `isPointInStroke` methods, aligning with the latest W3C specifications.

#### Technical Details
This change modernizes the SVG API surface by adopting the more flexible DOMPointInit interface, which provides better integration with modern web platform APIs and improved developer ergonomics for point-based operations in SVG contexts.

#### Use Cases
- SVG manipulation libraries benefit from modernized API interfaces
- Graphics applications gain more consistent point handling across web APIs
- Developer tools can provide better SVG interaction capabilities
- Animation frameworks can leverage improved SVG geometry methods

#### References
[Tracking bug #40572887](https://bugs.chromium.org/p/chromium/issues/detail?id=40572887) | [ChromeStatus.com entry](https://chromestatus.com/feature/5084627093929984) | [Spec](https://www.w3.org/TR/SVG2/types.html#InterfaceDOMPointInit)