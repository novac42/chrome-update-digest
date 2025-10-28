Area Summary

Chrome 137 introduces two on-device language-model APIs—Rewriter API and Writer API—exposed to web developers via origin trials and WICG specs. These features enable in-browser text transformation and generation powered by on-device AI models, giving developers programmatic tools for rewriting and composing text. By standardizing these capabilities as web APIs, Chrome advances the platform toward richer, privacy-aware language features accessible from web pages and apps. The origin trial and spec links indicate a staged rollout where developers can test and provide feedback.

## Detailed Updates

Below are the On-device AI features added in Chrome 137, each described with what’s new, technical notes, developer use cases, and links to the spec, origin trial, and tracking issues.

### Rewriter API

#### What's New
The Rewriter API provides an interface to transform and rephrase input text in requested ways, backed by an on-device AI language model.

#### Technical Details
- API surface defined by the WICG Rewriter spec.
- Enabled for testing via an origin trial.
- Tracking and implementation progress are tracked through the provided Chromium issue.

#### Use Cases
- Remove redundancies to fit text into a word limit.
- Rephrase messages to suit an intended audience.
- Make messages more constructive or adjust tone.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)
- [Tracking bug](https://bugs.chromium.org/p/chromium/issues/detail?id=358214322)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5089854436556800)
- [Spec](https://wicg.github.io/rewriter-api/)

### Writer API

#### What's New
The Writer API enables generation of new text given a writing task prompt, using an on-device AI language model.

#### Technical Details
- API is specified in the WICG Writer spec.
- Available for experimentation via an origin trial.
- Implementation and progress tracked in the linked Chromium issue.
- Associated licensing and site-policy references are provided for content and spec reuse.

#### Use Cases
- Generate textual explanations of structured data.
- Compose posts about products using reviews or product descriptions.
- Programmatically produce writing based on developer-provided prompts.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active)
- [Tracking bug](https://bugs.chromium.org/p/chromium/issues/detail?id=357967382)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5089855470993408)
- [Spec](https://wicg.github.io/writer-api/)
- [Link](https://creativecommons.org/licenses/by/4.0/)
- [Link](https://www.apache.org/licenses/LICENSE-2.0)
- [Link](https://developers.google.com/site-policies)

Area-Specific Expertise (On-device AI implications)

- css: Minimal direct impact; UI for rewrite/write controls should follow responsive layout and accessible form controls when embedding editor widgets.
- webapi: These APIs extend the web platform surface for natural-language processing, requiring careful API ergonomics and promise/async patterns consistent with existing DOM APIs.
- graphics-webgpu: On-device model acceleration may leverage GPU compute; teams should coordinate inference resource use with graphics workloads to avoid contention.
- javascript: Integration will be via standard JS promises/events; developers should manage async task lifecycles and memory when handling generated content.
- security-privacy: On-device execution reduces network exposure; developers must still handle user consent, content policies, and potential PII in inputs/outputs.
- performance: Local inference shifts latency characteristics—expect lower round-trip times but consider CPU/GPU and power impacts on client devices.
- multimedia: Text generation can be combined with TTS or captioning pipelines; ensure synchronization and format compatibility when producing multimedia outputs.
- devices: Hardware variability matters; feature availability and performance will depend on device ML capabilities and vendor drivers.
- pwa-service-worker: PWAs can cache prompts and manage offline UX, but service workers should not block UI threads during model-driven tasks.
- webassembly: Where on-device models expose native runtimes, WASM can be an integration path for custom model runtimes or pre/post-processing.
- deprecations: No deprecations introduced here; migration guidance should focus on adopting these new APIs over ad-hoc JS libraries.

Save file to: digest_markdown/webplatform/On-device AI/chrome-137-stable-en.md