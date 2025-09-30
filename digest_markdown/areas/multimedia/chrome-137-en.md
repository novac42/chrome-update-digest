---
layout: default
title: chrome-137-en
---

## Area Summary

Chrome 137 introduces an origin-trial permission policy targeting embedded media playback control for not-rendered iframes. The core change lets embedders pause media in iframes whose display is `none`, enabling more deliberate control over embedded content. This is meaningful for developers who need to optimize user experience and manage resource use for hidden frames. The update advances the web platform by exposing an embedder-controlled hook into media behavior across frame boundaries.

## Detailed Updates

Below are the Multimedia-area changes related to the summary above.

### Pause media playback on not-rendered iframes

#### What's New
Adds a `media-playback-while-not-rendered` permission policy to allow embedder websites to pause media playback of embedded iframes which aren't rendered—that is, have their display property set to `none`. This capability is surfaced as an origin trial.

#### Technical Details
- Introduces the permission policy token `media-playback-while-not-rendered`.
- Allows the embedder to control whether media inside an iframe continues playing when the iframe is not rendered (display: none).
- Delivered via Chrome origin trial machinery (see Origin Trial link for enrollment and details).

#### Use Cases
- Prevent hidden iframe media from continuing to play, improving predictability of audio/video behavior for users.
- Reduce wasted CPU/network and potential battery impact by stopping playback in not-rendered frames.
- Give embedder sites finer-grained control over cross-frame multimedia behavior for UX and resource management.

#### References
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=351354996
- https://chromestatus.com/feature/5082854470868992

File path for this digest:
digest_markdown/webplatform/Multimedia/chrome-137-stable-en.md
