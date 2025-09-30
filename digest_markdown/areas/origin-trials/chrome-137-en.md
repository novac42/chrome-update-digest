---
layout: default
title: chrome-137-en
---

## Area Summary

Chrome 137's Origin Trials focus on giving developers finer control over resource usage and experimenting with on-device AI text-generation APIs. The most impactful updates are the resource-management controls (a render-blocking token and a media playback permission policy) and two experimental on-device language APIs (Rewriter and Writer). These trials advance the platform by enabling origin-scoped experimentation with performance, multimedia behavior, and integrated AI capabilities while surfacing developer impact before wider rollout. Teams should evaluate UX, privacy, and performance trade-offs under the origin trial tokens.

## Detailed Updates

Below are the origin-trial features in Chrome 137 with concise technical notes and developer-facing use cases.

### Full frame rate render blocking attribute

#### What's New
Adds a new render blocking token `full-frame-rate` to the blocking attributes. When the renderer is blocked with the `full-frame-rate` token, the renderer will work at a lower frame rate to reserve more resources for loading.

#### Technical Details
- Introduces a render-blocking token named `full-frame-rate`.
- When applied, the renderer reduces frame rate while blocked, reallocating resources toward loading tasks.

#### Use Cases
- Improve loading performance by deprioritizing visual frame updates during heavy resource loads.
- Useful for pages that want to trade transient smoothness for faster load times.

#### References
- [Tracking bug #397832388](https://bugs.chromium.org/p/chromium/issues/detail?id=397832388)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5109023781429248)

### Pause media playback on not-rendered iframes

#### What's New
Adds a `media-playback-while-not-rendered` permission policy to allow embedder websites to pause media playback of embedded iframes which aren't rendered (i.e., have `display: none`).

#### Technical Details
- New permission-policy directive: `media-playback-while-not-rendered`.
- Gives embedders the ability to control whether non-rendered iframes continue media playback.

#### Use Cases
- Prevent hidden iframes from consuming CPU/audio resources.
- Improve user experience and resource usage for pages embedding third-party media.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)  
- [Tracking bug #351354996](https://bugs.chromium.org/p/chromium/issues/detail?id=351354996)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5082854470868992)

### Rewriter API

#### What's New
The Rewriter API transforms and rephrases input text in requested ways, backed by an on-device AI language model. It can remove redundancies, fit word limits, or rephrase tone.

#### Technical Details
- New web API (origin-trial gated) providing text transformation powered by an on-device model.
- Exposes programmatic rephrasing and text-normalization capabilities to pages during the trial.

#### Use Cases
- Auto-condense or adapt user-generated text to constraints (e.g., character limits).
- Assistive editing features that rephrase for clarity or tone in-app.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)  
- [Tracking bug #358214322](https://bugs.chromium.org/p/chromium/issues/detail?id=358214322)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5089854436556800)  
- [Spec](https://wicg.github.io/rewriter-api/)

### Writer API

#### What's New
The Writer API generates new textual material from a writing-task prompt, backed by an on-device AI language model. It supports tasks like composing posts, generating explanations, or expanding descriptions.

#### Technical Details
- Origin-trial gated API that produces text outputs from prompts using an on-device model.
- Comes with associated spec and governance links provided in the trial materials.

#### Use Cases
- Generate product descriptions, summaries, or explanatory text from structured input.
- Assistive authoring tools within web apps that need programmatic content generation.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)  
- [Tracking bug #357967382](https://bugs.chromium.org/p/chromium/issues/detail?id=357967382)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5089855470993408)  
- [Spec](https://wicg.github.io/writer-api/)  
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)  
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)  
- [Google Developers Site Policies](https://developers.google.com/site-policies)

Area-specific implications and considerations (origin trials focus)
- css: The full-frame-rate token affects render timing and paint cadence; audit layout/animation behavior when frame rate is reduced.  
- webapi / javascript: Rewriter and Writer expose new JS APIs under origin trials — design graceful fallback paths for non-trial clients.  
- graphics-webgpu / performance: Lowering renderer frame rate reallocates GPU/CPU cycles; measure render vs. load trade-offs.  
- multimedia: The iframe playback policy gives embedder control to stop hidden media and reduce resource usage.  
- security-privacy: On-device AI models (Rewriter/Writer) shift data processing to the client device, impacting data flow and privacy considerations.  
- devices: On-device APIs will consume local compute; profile device capabilities and battery impact.  
- pwa-service-worker / webassembly / deprecations: No deprecations listed; consider integration points with PWAs or local compute strategies where applicable.
