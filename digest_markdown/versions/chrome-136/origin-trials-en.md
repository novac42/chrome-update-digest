---
layout: default
title: origin-trials-en
---

## Detailed Updates

The items below summarize the active origin trials in Chrome 136 and why developers should try them.

### Audio Output Devices API: setDefaultSinkId()

#### What's New
Adds `setDefaultSinkId()` to `MediaDevices`, enabling the top-level frame to change the default audio output device used by its subframes.

#### Technical Details
This API extension is exposed via an origin trial and attaches a default-sink control to `MediaDevices`, scoped to top-level frames and applied to subframes.

#### Use Cases
Useful for web apps that manage audio across embedded content or cross-frame scenarios (e.g., conferencing apps, embedded widgets) where a top-level context needs to direct subframe audio output to a specific device.

#### References
- Origin Trial: https://developer.chrome.com/origintrials/#/trials/active
- ChromeStatus.com entry: https://chromestatus.com/feature/5066644096548864
- Spec: https://webaudio.github.io/web-audio-api/#dom-mediadevices-setdefaultsinkid

### Enable web applications to understand bimodal performance timings

#### What's New
An origin trial to help web applications detect and reason about bimodal distributions in page load performance (for example, distinguishing cold start vs warmed scenarios).

#### Technical Details
The trial surfaces signals intended to let apps identify when page load timings reflect external factors such as expensive user-agent initialization (cold start), referencing navigation timing semantics.

#### Use Cases
Enables developers to better diagnose and adapt UX for users experiencing slow cold starts, implement conditional instrumentation, and more accurately interpret telemetry driven by Navigation Timing data.

#### References
- Origin Trial: https://developer.chrome.com/origintrials/#/trials/active
- Tracking bug #1413848: https://bugs.chromium.org/p/chromium/issues/detail?id=1413848
- ChromeStatus.com entry: https://chromestatus.com/feature/5037395062800384
- Spec: https://w3c.github.io/navigation-timing/

### Update of Canvas text rendering implementation

#### What's New
An origin trial for a significant change in the internal implementation of canvas text rendering methods (`measureText()`, `fillText()`, and `strokeText()`); the change is not a web-exposed API change but may affect performance.

#### Technical Details
This trial exposes the new internal canvas text rendering implementation to origins so canvas-heavy applications can evaluate performance and behavior differences of the updated rendering pipeline.

#### Use Cases
Canvas-heavy applications (games, editors, rich visualizations) can opt in to validate text-measurement and text-drawing performance, detect regressions, and provide feedback before the implementation ships broadly.

#### References
- Origin Trial: https://developer.chrome.com/origintrials/#/trials/active
- Tracking bug #389726691: https://bugs.chromium.org/p/chromium/issues/detail?id=389726691
- ChromeStatus.com entry: https://chromestatus.com/feature/5104000067985408
