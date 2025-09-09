---
layout: default
title: origin-trials
---

## Origin trials

### Full frame rate render blocking attribute

Adds a new render blocking token `full-frame-rate` to the blocking attributes. When the renderer is blocked with the `full-frame-rate` token, the renderer will work at a lower frame rate so as to reserve more resources for loading.

**References:** [Tracking bug #397832388](https://bugs.chromium.org/p/chromium/issues/detail?id=397832388) | [ChromeStatus.com entry](https://chromestatus.com/feature/5109023781429248)

### Pause media playback on not-rendered iframes

Adds a `media-playback-while-not-rendered` permission policy to allow embedder websites to pause media playback of embedded iframes which aren't rendered—that is, have their display property set to `none`. This should allow developers to build more user-friendly experiences and to also improve the performance by letting the browser handle the playback of content that is not visible to users.

**References:** [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #351354996](https://bugs.chromium.org/p/chromium/issues/detail?id=351354996) | [ChromeStatus.com entry](https://chromestatus.com/feature/5082854470868992)

### Rewriter API

The Rewriter API transforms and rephrases input text in requested ways, backed by an on-device AI language model. Developers may use this API to remove redundancies within a text in order to fit into a word limit, rephrase messages to suit the intended audience or to be more constructive if a message is found to use toxic language, rephrasing a post or article to use simpler words and concepts and more.

**References:** [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #358214322](https://bugs.chromium.org/p/chromium/issues/detail?id=358214322) | [ChromeStatus.com entry](https://chromestatus.com/feature/5089854436556800) | [Spec](https://wicg.github.io/rewriter-api/)

### Writer API

The Writer API can be used for writing new material given a writing task prompt, backed by an on-device AI language model. Developers will be able to use this API to generate textual explanations of structured data, composing a post about a product based on reviews or product description, expanding on pro and con lists into full views and more.

**References:** [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #357967382](https://bugs.chromium.org/p/chromium/issues/detail?id=357967382) | [ChromeStatus.com entry](https://chromestatus.com/feature/5089855470993408) | [Spec](https://wicg.github.io/writer-api/)

---

*Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.*

*Last updated 2025-05-27 UTC.*
