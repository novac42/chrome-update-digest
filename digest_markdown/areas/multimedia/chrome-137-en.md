---
layout: default
title: Area Summary
---

# Area Summary

Chrome 137 introduces a multimedia-focused permission policy that gives embedders explicit control over media playback in iframes that are not rendered. The change is surfaced as an Origin Trial and is aimed at embedder websites that need to pause media in embedded contexts whose CSS display property is set to `none`. This update matters to developers embedding third-party media because it formalizes a control point for playback behavior in non-rendered iframes and is tracked through an Origin Trial and Chromium issue.

## Detailed Updates

Below are the details for the Multimedia change in Chrome 137 and its practical implications for developers.

### Pause media playback on not-rendered iframes

#### What's New
Adds a `media-playback-while-not-rendered` permission policy to allow embedder websites to pause media playback of embedded iframes which aren't rendered—that is, have their display property set to `none`. The release note text in the source is truncated after "improve the p...".

#### Technical Details
- Introduces a permission policy named `media-playback-while-not-rendered`.
- Applies to embedded iframes whose CSS `display` is `none` (definition of "not-rendered" in the note).
- Marked as an Origin Trial in the provided metadata.

#### Use Cases
- Embedders can opt to pause media in non-rendered iframes to better control user experience (as stated).
- Further explanatory text in the source is truncated; consult the Origin Trial and tracking links below for implementation and rollout details.

#### Area-specific implications
- css: Relies on the `display: none` state as the trigger for "not-rendered" behavior.
- webapi: Exposes a permission-policy control surface for embedder pages to govern iframe playback.
- performance: By allowing pausing of non-rendered iframe media, embedders can potentially reduce unnecessary background activity.
- multimedia: Directly affects embedded media playback behavior and embedder-driven playback policies.
- security-privacy: Permission policies are a web-facing control that influence cross-origin embed behavior.
- javascript, graphics-webgpu, devices, pwa-service-worker, webassembly, deprecations: No additional details provided in the source; consult the Origin Trial and tracking bug for any related API interactions or migration guidance.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)
- [Tracking bug #351354996](https://bugs.chromium.org/p/chromium/issues/detail?id=351354996)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5082854470868992)
