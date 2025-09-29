---
layout: default
title: multimedia-en
---

## Area Summary

Chrome 137 (stable) introduces a targeted multimedia control: an origin-trial permission policy that lets embedders pause media in iframes that are not rendered. The primary theme is giving embedding sites explicit control over playback for hidden iframe content. This change is most impactful for developers who embed third-party or cross-origin media and need predictable playback behavior. It advances the platform by extending permission-policy controls into multimedia playback scenarios, helping embedders manage user experience and resource use.

## Detailed Updates

Below are the Multimedia-area details for Chrome 137 (stable), focused on developer-facing behavior and integration points.

### Pause media playback on not-rendered iframes

#### What's New
Adds a `media-playback-while-not-rendered` permission policy to allow embedder websites to pause media playback of embedded iframes which aren't rendered—that is, have their display property set to `none`.

#### Technical Details
- Exposed as a permission policy named `media-playback-while-not-rendered`.
- Available as an Origin Trial for Chrome 137 (see references).

#### Use Cases
- Enables embedder sites to prevent audio/video from playing inside iframes that are not visually rendered, improving control over embedded content.
- Useful for embedding scenarios where hidden iframes should not consume audio output or playback resources.

#### References
- Origin Trial: https://developer.chrome.com/origintrials/#/trials/active
- Tracking bug #351354996: https://bugs.chromium.org/p/chromium/issues/detail?id=351354996
- ChromeStatus.com entry: https://chromestatus.com/feature/5082854470868992

## Area-Specific Expertise Notes (Multimedia-focused)

- css: Uses the rendered state concept (e.g., display:none) to decide playback suppression.
- webapi: Surface provided via a permission policy mechanism for embedders.
- multimedia: Impacts when codecs and decoders may be kept active for hidden embeds.
- performance: Gives embedders a lever to reduce wasted playback work for non-rendered iframes.
- security-privacy: Permission policy model maintains embedder authority over iframe playback behavior.
- javascript / pwa-service-worker / webassembly / devices / graphics-webgpu / deprecations: No new platform ABI or deprecation indicated in the provided data.
