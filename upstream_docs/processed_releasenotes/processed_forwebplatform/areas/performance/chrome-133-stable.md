## Performance

### Freezing on Energy Saver

When Energy Saver is active, Chrome will freeze a "browsing context group" that has been hidden and silent for over five minutes if any subgroup of same-origin frames within it exceeds a CPU usage threshold, unless it:

  * Provides audio- or video-conferencing functionality (detected by identifying microphone, camera or screen/window/tab capture or an RTCPeerConnection with an 'open' RTCDataChannel or a 'live' MediaStreamTrack).
  * Controls an external device (detected with use of WebUSB, Web Bluetooth, WebHID, or Web Serial).
  * Holds a Web Lock or an IndexedDB connection that blocks a version update or a transaction on a different connection.
  * Freezing consists of pausing execution. It is formally defined in the Page Lifecycle API.

The CPU usage threshold will be calibrated to freeze approximately 10% of background tabs when Energy Saver is active.

[Tracking bug #325954772](https://issues.chromium.org/issues/325954772) | [ChromeStatus.com entry](https://chromestatus.com/feature/5158599457767424)

### Expose coarsened cross-origin `renderTime` in element timing and LCP (regardless of `Timing-Allow-Origin`)

Element timing and LCP entries have a `renderTime` attribute, aligned with the first frame in which an image or text was painted.

This attribute is currently guarded for cross-origin images by requiring a `Timing-Allow-Origin` header on the image resource. However, that restriction is easy to work around (for example, by displaying a same-origin and cross-origin image in the same frame).

Since this has been a source of confusion, we instead plan to remove this restriction, and instead coarsen all render times by 4 ms when the document is not cross-origin-isolated. This is seemingly coarse enough to avoid leaking any useful decoding-time information about cross-origin images.

[Tracking bug #373263977](https://issues.chromium.org/issues/373263977) | [ChromeStatus.com entry](https://chromestatus.com/feature/5128261284397056) | [Spec](https://w3c.github.io/paint-timing/#mark-paint-timing)

### Revert `responseStart` and introduce `firstResponseHeadersStart`

With 103 Early Hints enabled, responses have two timestamps:

  * When the Early Hints arrive (103)
  * When the final headers arrive (e.g. 200)
  * When Chrome 115 shipped `firstInterimResponseStart` to allow measuring of these two timestamps, we also changed the meaning of `responseStart` (used by Time to First Byte (TTFB)) to mean "the final headers". This created a web compatibility issue with browsers and tools that did not make a similar change for this commonly used metric.

Chrome 133 reverts this `responseStart` change to resolve this compatibility issue and instead introduces `firstResponseHeadersStart` to allow sites to measure the time to the final headers, while retaining the original definition of TTFB.

[Tracking bug #40251053](https://issues.chromium.org/issues/40251053) | [ChromeStatus.com entry](https://chromestatus.com/feature/5158830722514944) | [Spec](https://w3c.github.io/resource-timing/#dom-performanceresourcetiming-finalresponseheadersstart)
