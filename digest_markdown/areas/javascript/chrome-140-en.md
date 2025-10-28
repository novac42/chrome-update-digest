---
layout: default
title: chrome-140-en
---

## Area Summary

Chrome 140 continues to strengthen JavaScript ergonomics and animation timing. The release adds built-in conversion support between binary buffers and base64/hex and adjusts the timing of the view transition finished promise to avoid end-of-animation flicker. These changes reduce boilerplate for binary encoding/decoding and fix a subtle rendering-timing gotcha for view transitions, improving developer control over visual continuity. Both updates advance the platform by closing cross-cutting gaps in developer-facing APIs (binary handling and animation lifecycle), reducing platform-level workarounds.

## Detailed Updates

The brief summary above connects to the specific JavaScript-focused changes in this release. Each feature below lists what changed, key technical notes relevant to JavaScript/runtime and browser integration, practical use cases, and the original links.

### `Uint8Array` to and from base64 and hex

#### What's New
Built-in ability to convert between Uint8Array (binary data) and base64/hex string encodings, removing the need for ad-hoc helpers.

#### Technical Details
- Adds standardized methods for encoding ArrayBuffer/Uint8Array to base64 and hex and decoding back to binary.
- Ties into the ArrayBuffer ecosystem and the ECMAScript-level proposal linked by the spec.
- Relevant to the JavaScript engine and WebAPI boundary where binary data is marshaled for storage, network, or interop.

#### Use Cases
- Simplifies client-side serialization for APIs that accept base64/hex (e.g., data URIs, JSON payloads).
- Reduces dependency on manual loops or global helpers for encoding in web apps, service workers, and node-like utilities.
- Beneficial for performance-sensitive code paths that previously used nonstandard helpers or intermediate strings.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/6281131254874112)
- [Link](https://tc39.es/proposal-arraybuffer-base64/spec)

### View transition finished promise timing change

#### What's New
The timing of the view transition finished promise has been changed so promise resolution does not run after the final frame that removes the view transition, preventing end-of-animation script-induced flicker.

#### Technical Details
- Previously, the finished promise resolved within the rendering lifecycle steps such that resolution callbacks could execute after the visual frame that removed the transition was produced.
- The timing change shifts promise resolution to avoid running developer script after that final removal frame, aligning script execution with visual continuity.
- Impacts animation lifecycle semantics exposed to JavaScript and interacts with frame production and task scheduling in the rendering pipeline.

#### Use Cases
- Prevents flicker when post-transition promise handlers manipulate layout or perform DOM changes.
- Makes view transitions more predictable for complex UIs that rely on promise callbacks to finalize state or trigger follow-up animations.
- Useful for performance-sensitive pages where minimizing late-frame script work preserves smoothness.

#### References
- [Tracking bug](https://issues.chromium.org/issues/430018991)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5143135809961984)
