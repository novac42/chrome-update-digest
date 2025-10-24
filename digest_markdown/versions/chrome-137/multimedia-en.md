---
layout: default
title: multimedia-en
---

## Area Summary

Chrome 137 introduces a focused Multimedia update: a permission policy to pause media playback in not-rendered iframes. The main developer-facing change is the new `media-playback-while-not-rendered` permission policy, allowing embedders to stop media inside iframes that have `display: none`. This gives sites explicit control over embedded media behavior and is being rolled out via origin trials and tracked in Chromium. These changes matter because they let developers reduce unexpected background playback and better control embedded media lifecycle.

## Detailed Updates

Below are the details for the Multimedia change in Chrome 137 and what developers should know.

### Pause media playback on not-rendered iframes

#### What's New
Adds a `media-playback-while-not-rendered` permission policy to allow embedder websites to pause media playback of embedded iframes which aren't rendered—that is, have their display property set to `none`. 

#### Technical Details
- Exposed as a permission policy named `media-playback-while-not-rendered`.
- Targets iframes that are not rendered (explicitly noted as having `display: none` in the release data).
- Tagged in the release metadata as an origin-trials feature for staged rollout.

#### Use Cases
- Enable embedders to prevent audio/video in hidden iframes from playing.
- Allow developers to implement more predictable embedded-media UX (release notes state this "should allow developers to build more user-friendly experiences").

#### References
- Origin Trial: https://developer.chrome.com/origintrials/#/trials/active
- Tracking bug #351354996: https://bugs.chromium.org/p/chromium/issues/detail?id=351354996
- ChromeStatus.com entry: https://chromestatus.com/feature/5082854470868992

## Area-Specific Expertise (Multimedia-focused notes)

- css: Relies on `display: none` as the signal for "not-rendered"; apply CSS changes intentionally when interacting with this policy.
- webapi: Surface is a permission policy; embedders will opt into controlling iframe media via document-level policy headers or attributes.
- graphics-webgpu: No direct API change for GPU pipelines; pausing media in hidden iframes can reduce rendering pressure in some scenarios.
- javascript: Control remains at embedder policy level; scripts can still toggle iframe rendering states to affect playback behavior.
- security-privacy: Implemented as a permission policy, keeping control with the embedding origin rather than cross-origin content.
- performance: Pausing hidden iframe media helps avoid unnecessary CPU/network use from media elements that users can't see.
- multimedia: Directly affects embedded audio/video playback behavior; useful for reducing unwanted background playback.
- devices: Indirectly reduces device resource consumption by stopping hidden media playback.
- pwa-service-worker: No direct service worker changes, but embedded media lifetime may be more predictable in offline/foreground scenarios.
- webassembly: No change to WASM runtime; benefits are at embedding/DOM level.
- deprecations: Released via origin trial—monitor ChromeStatus and the tracking bug for rollout and migration guidance.
