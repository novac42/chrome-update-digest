---
layout: default
title: origin-trials-en
---

## Area Summary

Chrome 137's Origin Trials focus on experimental controls for rendering performance, media behavior in embeds, and on-device generative text APIs. The most impactful changes let developers manage rendering resource allocation (full-frame-rate token), pause invisible iframe media playback via a permission policy, and test two new AI-backed text APIs (Rewriter and Writer) on-device. These updates advance the platform by exposing developer controls for performance and embed behavior while iterating on privacy- and resource-conscious on-device ML capabilities. Teams should evaluate origin trial enrollment to prototype integrations and assess privacy, UX, and performance trade-offs early.

## Detailed Updates

Below are the Chrome 137 origin-trial features with succinct developer-focused explanations and relevant links.

### Full frame rate render blocking attribute

#### What's New
Adds a new render blocking token named `full-frame-rate`. When a renderer is blocked with this token, it runs at a lower frame rate to reserve resources for loading.

#### Technical Details
This is an origin-trial-level flag that exposes a render-blocking attribute. The renderer will reduce frame rate when the `full-frame-rate` token is present, affecting the compositor/rendering pipeline and scheduling to favor loading tasks over high-frequency rendering.

#### Use Cases
- Improve perceived load performance by reducing rendering overhead during heavy network/CPU loads.
- Better resource allocation on complex pages where loading priority should temporarily trump smooth animation.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=397832388
- https://chromestatus.com/feature/5109023781429248

### Pause media playback on not-rendered iframes

#### What's New
Introduces a `media-playback-while-not-rendered` permission policy that allows embedders to pause media playback in iframes that are not rendered (e.g., `display:none`).

#### Technical Details
This permission policy extends the embedder control surface (Permissions Policy) and hooks into media playback semantics for nested browsing contexts. User agents can suspend playback when computed display is none, reducing CPU/multimedia decoding usage for non-visible iframes.

#### Use Cases
- Reduce CPU and battery usage by pausing audio/video in hidden embeds.
- Improve UX by preventing unexpected audio from offscreen or hidden third-party content.
- Useful for performance-sensitive pages and PWAs that embed third-party media.

#### References
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=351354996
- https://chromestatus.com/feature/5082854470868992

### Rewriter API

#### What's New
An origin-trial API that transforms and rephrases input text using an on-device AI language model (e.g., shorten, rephrase, make constructive).

#### Technical Details
Exposes a web API to perform text transformations locally via an on-device model. Integration touches webapi surface (new DOM interfaces), privacy controls, and may interact with resource management (CPU/GPU usage for model inference). Spec available from WICG; enrollment required via the origin trials dashboard.

#### Use Cases
- Inline UI for summarizing or shortening user-generated content before submission.
- Client-side rephrasing for tone adjustments or audience adaptation without server roundtrips.
- Localized preprocessing to enforce content length limits and improve UX.

#### References
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=358214322
- https://chromestatus.com/feature/5089854436556800
- https://wicg.github.io/rewriter-api/

### Writer API

#### What's New
An origin-trial API to generate new textual content from a writing task prompt using an on-device AI language model.

#### Technical Details
Provides an on-device generative API surface for creating text given structured prompts. As an origin trial, it involves webapi work for request/response interfaces, privacy considerations around local model usage, and potentially licensing/policy implications. Specs and policy/license references are provided for developer review.

#### Use Cases
- Generate explanations of structured data for user-facing content.
- Auto-compose product descriptions or expand outlines in client-side editors.
- Assistive writing tools integrated directly in web apps without server-side generation.

#### References
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=357967382
- https://chromestatus.com/feature/5089855470993408
- https://wicg.github.io/writer-api/
- https://creativecommons.org/licenses/by/4.0/
- https://www.apache.org/licenses/LICENSE-2.0
- https://developers.google.com/site-policies

Saved file path:
digest_markdown/webplatform/Origin trials/chrome-137-stable-en.md
