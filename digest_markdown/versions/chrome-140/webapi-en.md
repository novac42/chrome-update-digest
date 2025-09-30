---
layout: default
title: webapi-en
---

## Detailed Updates

The following details expand on the summary above and list each Web API change in Chrome 140 with concise technical notes, developer use cases, and references.

### `ReadableStreamBYOBReader` `min` option

#### What's New
This feature introduces a `min` option to the existing `ReadableStreamBYOBReader.read(view)` method, allowing callers to request that reads resolve only after a minimum number of elements have been written into the provided `ArrayBufferView`.

#### Technical Details
The `read(view)` call already accepts an `ArrayBufferView` to receive data; adding `min` provides a contract that the returned promise should not resolve until at least `min` elements are written. See the Streams specification for authoritative behavior and semantics.

#### Use Cases
Useful where consumers require a guaranteed minimum amount of binary data before processing (e.g., framing/binary protocols or bulk buffer processing) to avoid repeated short reads and simplify buffer management.

#### References
- https://issues.chromium.org/issues/40942083
- https://chromestatus.com/feature/6396991665602560
- https://streams.spec.whatwg.org/#byob-reader-read

### Get Installed Related Apps API on desktop

#### What's New
The Get Installed Related Apps API (navigator.getInstalledRelatedApps) is now available on desktop, giving sites access to whether corresponding related applications are installed, subject to established associations between the web origin and the application.

#### Technical Details
Sites may call navigator.getInstalledRelatedApps only when the application has an established association with the web origin. The API was originally launched in earlier Chrome versions and is now extended to desktop contexts.

#### Use Cases
Enables progressive enhancement flows where a site can detect a user’s installed native apps to offer deep links, install prompts, or alternative UX paths when a related app exists.

#### References
- https://issues.chromium.org/issues/895854
- https://chromestatus.com/feature/5695378309513216
- https://wicg.github.io/get-installed-related-apps/spec

### Http cookie prefix

#### What's New
Introduces an HTTP cookie prefix mechanism to help distinguish cookies set by the server from those set by client-side code. This helps defend against unexpected or malicious cookies being introduced by XSS, extensions, or other client-side actors.

#### Technical Details
By adopting a cookie prefix convention, servers can mark cookies that are expected to be server-set, enabling more reliable server-side handling and policy decisions when cookie provenance matters.

#### Use Cases
Useful for server-driven cookies that must not be spoofed by client scripts—for example authentication or integrity cookies where server certainty about origin improves security posture.

#### References
- https://issues.chromium.org/issues/426096760
- https://chromestatus.com/feature/5170139586363392
- https://github.com/httpwg/http-extensions/pull/3110

Saved to: digest_markdown/webplatform/Web API/chrome-140-stable-en.md
