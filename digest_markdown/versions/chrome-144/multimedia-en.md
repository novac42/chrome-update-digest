---
layout: default
title: Chrome 144 Stable - Multimedia Updates
---

# Chrome 144 Stable - Multimedia Updates

## Area Summary

Chrome 144 introduces a significant enhancement to WebRTC's video adaptation capabilities with the new `maintain-framerate-and-resolution` degradation preference. This update empowers developers to implement custom video adaptation strategies by disabling the browser's built-in automatic adjustments for framerate and resolution. The feature addresses a critical need for applications requiring fine-grained control over video quality parameters, particularly in scenarios where application-level adaptation logic can make more informed decisions than the browser's default behavior. This addition aligns with the WebRTC MediaStreamTrack Content Hints specification and represents an important step toward giving developers more control over real-time communication quality management.

## Detailed Updates

This release focuses on expanding developer control over WebRTC video streaming behavior, providing a new mechanism to prevent conflicts between application-level and browser-level adaptation strategies.

### `RTCDegradationPreference` enum value `maintain-framerate-and-resolution`

#### What's New

Chrome 144 adds the `maintain-framerate-and-resolution` value to the `RTCDegradationPreference` enum, which disables WebRTC's internal video adaptation mechanism. This allows applications to implement their own custom adaptation logic without interference from the browser's automatic quality adjustments.

#### Technical Details

When `maintain-framerate-and-resolution` is set, the browser maintains both framerate and resolution regardless of video quality concerns. The user agent will not prefer reducing either parameter for quality or performance reasons. However, the browser may still drop frames before encoding if necessary to avoid overusing network and encoder resources. This prevents the internal adaptation system from conflicting with application-level adaptation strategies while still providing a safety mechanism for extreme resource constraints.

#### Use Cases

This feature is particularly valuable for:
- Applications implementing sophisticated adaptive bitrate streaming algorithms that require full control over video parameters
- Scenarios where the application has better context about network conditions or user preferences than the browser's heuristics can provide
- Professional video conferencing systems that need deterministic behavior for quality management
- Broadcasting and live streaming applications where maintaining specific framerate and resolution characteristics is critical

#### References

- [Tracking bug #450044904](https://issues.chromium.org/issues/450044904)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5156290162720768)
- [Spec](https://www.w3.org/TR/mst-content-hint/#dom-rtcdegradationpreference-maintain-framerate-and-resolution)
