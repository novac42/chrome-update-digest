# Area Summary

Chrome 137's Origin Trials focus on experimental controls for resource management and embedded content behavior, plus two on-device AI text APIs for developers to trial. The most impactful changes are the resource-reservation render-blocking token and a permission policy that lets embedders pause playback in not-rendered iframes, and the Rewriter and Writer APIs that expose on-device language-model capabilities. These updates advance the platform by enabling finer-grained embedder control (security/privacy, multimedia, performance) and by surfacing local AI-powered content transformations for web apps. They matter because origin trials let teams evaluate integration, UX, and privacy implications before wide deployment.

## Detailed Updates

Below are the origin-trial features in Chrome 137, with concise technical and developer-focused details.

### Full frame rate render blocking attribute

#### What's New
Adds a new render-blocking token named full-frame-rate. When the renderer is blocked with this token, the renderer operates at a lower frame rate to reserve more resources for loading.

#### Technical Details
The feature introduces a `full-frame-rate` token for render blocking attributes; when applied the renderer reduces its frame rate to prioritize load work. Implementation and tracking are accessible via the linked Chromium issue and ChromeStatus entry.

#### Use Cases
Use this token when you want the browser to reduce animation/paint frequency during heavy loading to improve perceived load performance and resource allocation.

#### References
- [Tracking bug #397832388](https://bugs.chromium.org/p/chromium/issues/detail?id=397832388)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5109023781429248)

### Pause media playback on not-rendered iframes

#### What's New
Introduces a `media-playback-while-not-rendered` permission policy that allows embedder sites to pause media playback for iframes that are not rendered (e.g., display: none).

#### Technical Details
The permission policy provides an embedder-controlled switch to stop media playback in embedded frames that are not being rendered. This is exposed via an origin trial and tracked through the linked issues and ChromeStatus entry.

#### Use Cases
Embedders can reduce unnecessary media decoding and network usage for hidden iframes, improving power and network efficiency and creating more user-friendly embedding behaviors.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)
- [Tracking bug #351354996](https://bugs.chromium.org/p/chromium/issues/detail?id=351354996)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5082854470868992)

### Rewriter API

#### What's New
An on-device API that transforms and rephrases input text using an on-device AI language model (e.g., removing redundancies, rephrasing for audience/tone).

#### Technical Details
The Rewriter API is exposed as an origin trial. It runs transformations locally via an on-device language model; the origin-trial registration and tracking are available through the provided links and spec.

#### Use Cases
Developers can implement client-side text trimming, tone adjustments, or audience-specific rewrites without server-side roundtrips, reducing latency and keeping text processing local to the device.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)
- [Tracking bug #358214322](https://bugs.chromium.org/p/chromium/issues/detail?id=358214322)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5089854436556800)
- [Spec](https://wicg.github.io/rewriter-api/)

### Writer API

#### What's New
An on-device API for generating new text from a prompt using an on-device AI language model (e.g., composing explanations, expanding descriptions).

#### Technical Details
The Writer API is available via origin trial. It exposes on-device generation capabilities; tracking, spec, and policy/license links are provided for evaluation and integration guidance.

#### Use Cases
Use the Writer API for client-side content generation such as creating product summaries, expanding structured data into text, or drafting UI-facing copy—keeping generation local for latency and privacy considerations.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)
- [Tracking bug #357967382](https://bugs.chromium.org/p/chromium/issues/detail?id=357967382)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5089855470993408)
- [Spec](https://wicg.github.io/writer-api/)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)

Saved to: digest_markdown/webplatform/Origin trials/chrome-137-stable-en.md