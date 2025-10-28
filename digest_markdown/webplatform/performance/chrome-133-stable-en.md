## Area Summary

Chrome 133 advances performance along three practical axes: energy-aware tab freezing, more privacy-conscious timing visibility for element/LCP metrics, and clearer resource-timing semantics around Early Hints — plus a GPU shader-level optimization for WGSL. The most impactful changes for developers are the Energy Saver freeze behavior (affecting background work and media/conferencing pages), the exposure of coarsened cross-origin `renderTime` (improving observability for element timing and LCP), and the introduction of a dedicated timestamp for first response headers (`firstResponseHeadersStart`) to clarify resource timing. Collectively these updates improve power usage, measurement accuracy, and GPU shader throughput while balancing privacy.

## Detailed Updates

The following items expand on the summary above and list actionable notes for Performance-focused teams.

### Freezing on Energy Saver

#### What's New
When Energy Saver is active, Chrome will freeze a "browsing context group" that has been hidden and silent for over five minutes if any subgroup of same-origin frames within it exceeds a CPU usage threshold, with exceptions for pages that provide audio- or video-conferencing functionality (detection described in the feature text).

#### Technical Details
Freezing applies at the browsing-context-group level after a five-minute hidden-and-silent window and considers CPU usage of same-origin frame subgroups to decide when to freeze. Pages that provide live-conferencing functionality are exempted via detection logic as noted in the feature description.

#### Use Cases
Expect background tabs and hidden frames to be frozen more aggressively under Energy Saver; design background tasks, timers, and real-time communication pages to either avoid being silent or to surface activity that prevents freezing when required.

#### References
- [Tracking bug #325954772](https://issues.chromium.org/issues/325954772)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5158599457767424)

### Expose coarsened cross-origin `renderTime` in element timing and LCP (regardless of `Timing-Allow-Origin`)

#### What's New
Element timing and LCP entries expose a `renderTime` attribute (aligned with the first frame in which an image or text was painted). Chrome 133 exposes a coarsened `renderTime` for cross-origin resources even when a `Timing-Allow-Origin` header is not present.

#### Technical Details
The `renderTime` attribute remains aligned to first-paint frame semantics. For cross-origin images the previous requirement for a `Timing-Allow-Origin` header is relaxed by exposing a coarsened value that improves observability while maintaining privacy protections (see feature text and spec reference).

#### Use Cases
Performance measurement for element timing and LCP will gain visibility into cross-origin resource render events without requiring header changes on third-party assets; expect lower precision (coarsened timestamps) but improved coverage for diagnosing perceived paint timing.

#### References
- [Tracking bug #373263977](https://issues.chromium.org/issues/373263977)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5128261284397056)
- [Spec](https://w3c.github.io/paint-timing/#mark-paint-timing)

### Revert `responseStart` and introduce `firstResponseHeadersStart`

#### What's New
Chrome 133 introduces `firstResponseHeadersStart` to represent the timestamp for the first response headers (e.g., Early Hints / 103), and reverts the semantics of `responseStart` to clarify resource-timing measurements.

#### Technical Details
With Early Hints (103) there are distinct timestamps: arrival of Early Hints and arrival of final response headers. Chrome previously introduced `firstInterimResponseStart` and altered `responseStart`; this update adds `firstResponseHeadersStart` to explicitly capture the first headers arrival and reverts `responseStart` semantics for clarity in resource timing APIs.

#### Use Cases
Telemetry and monitoring tools that rely on Resource Timing should migrate to observe `firstResponseHeadersStart` when measuring header arrival (e.g., to account for Early Hints) and update any logic that depended on the prior `responseStart` semantics.

#### References
- [Tracking bug #40251053](https://issues.chromium.org/issues/40251053)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5158830722514944)
- [Spec](https://w3c.github.io/resource-timing/#dom-performanceresourcetiming-finalresponseheadersstart)

### WGSL performance gains with discard

#### What's New
Chrome 133 updates the implementation of the WGSL `discard` statement to use platform-provided semantics for demoting to a helper invocation when available, recovering significant performance in affected rendering scenarios.

#### Technical Details
The change targets cases where `discard` caused performance drops (notably complex screen-space reflections). By leveraging platform semantics for demotion to helper invocations, shader execution paths that previously triggered costly behavior now perform better as described in the feature note.

#### Use Cases
WebGPU shader authors using WGSL (especially effects like SSR) can expect improved performance when using `discard`. Review shaders that used `discard` as a mitigation for other issues — the platform-level optimization may remove prior performance penalties.

#### References
- [discard statement](https://gpuweb.github.io/gpuweb/wgsl/#discard-statement)
- [issue 372714384](https://issues.chromium.org/372714384)

