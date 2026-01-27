## WebRTC

### `RTCDegradationPreference` enum value `maintain-framerate-and-resolution`

`maintain-framerate-and-resolution` disables WebRTC's internal video adaptation. This lets the application implement its own adaptation logic and prevents interference from the internal adaptation.

From the WebRTC MediaStreamTrack Content Hints specification:

Maintain framerate and resolution regardless of video quality. The user agent shouldn't prefer reducing the framerate or resolution for quality and performance reasons, but might drop frames before encoding if necessary not to overuse network and encoder resources.

[Tracking bug #450044904](https://issues.chromium.org/issues/450044904) | [ChromeStatus.com entry](https://chromestatus.com/feature/5156290162720768) | [Spec](https://www.w3.org/TR/mst-content-hint/#dom-rtcdegradationpreference-maintain-framerate-and-resolution)
