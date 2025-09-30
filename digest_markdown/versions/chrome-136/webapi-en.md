---
layout: default
title: webapi-en
---

## Detailed Updates

The following details connect the high-level themes above to concrete changes developers should track and adopt.

### Dispatch click events to captured pointer

#### What's New
When a pointer is captured during dispatch of `pointerup`, the resulting `click` event is now dispatched to the captured target instead of the nearest common ancestor of the `pointerdown` and `pointerup` targets.

#### Technical Details
Behavior is changed to follow the UI Events spec’s semantics for click target resolution when pointer capture is in effect; uncaptured pointers retain the previous click target behavior.

#### Use Cases
More predictable interaction handling for components that use pointer capture (custom drag/drop, drawing tools), avoiding surprising click routing during capture.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40851596
- https://chromestatus.com/feature/5045063816396800
- https://w3c.github.io/uievents/#event-type-click

### Explicit compile hints with magic comments

#### What's New
JavaScript files can include magic comments that encode which functions should be eager-parsed or eagerly compiled.

#### Technical Details
The feature provides an in-band way to attach compile hints to source, enabling the engine (V8) to use those hints during parsing/compilation phases to reduce warm-up or parsing overhead.

#### Use Cases
Large JS codebases and libraries can guide eager compilation for performance-critical functions without changing runtime code; helpful for startup performance tuning.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=13917
- https://chromestatus.com/feature/5047772830048256
- https://github.com/v8/v8/wiki/Design-Elements#compile-hints

### Incorporate navigation initiator into the HTTP cache partition key

#### What's New
Chrome’s HTTP cache keying now includes an `is-cross-site-main-frame-navigation` boolean to the partition key.

#### Technical Details
The cache key change differentiates responses based on whether the navigation was a cross-site top-level initiator, closing a vector for cross-site information leakage via cache probing.

#### Use Cases
Improves privacy and security for sites relying on cache semantics; developers should be aware that cache behavior may vary based on navigation initiator and plan cache expectations accordingly.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=398784714
- https://chromestatus.com/feature/5108419906535424
- https://httpwg.org/specs/rfc9110.html#caching

### Protected audience: text conversion helpers

#### What's New
Adds dedicated helper functions to efficiently convert strings to and from byte arrays for use with WebAssembly memory in Protected Audience bidding/scoring contexts.

#### Technical Details
These standalone functions are intended to avoid ad-hoc conversions and provide efficient interoperability between JS string data and WASM linear memory buffers used by Protected Audience scripts.

#### Use Cases
Advertising and privacy-preserving bidding/scoring flows that run code in WebAssembly and must exchange string-typed data with JS without expensive manual encoding/decoding.

#### References
- https://chromestatus.com/feature/5099738574602240

### RegExp.escape

#### What's New
Introduces `RegExp.escape`, a static method that returns an escaped version of a string safe to use as a regular expression pattern.

#### Technical Details
The method performs escaping of regex metacharacters so untrusted or user-provided strings can be embedded into `RegExp` constructors without altering pattern semantics.

#### Use Cases
Safely building dynamic regular expressions from user input (search boxes, pattern builders) without manual escaping; reduces risk of accidental regex syntax injection.

#### References
- https://chromestatus.com/feature/5074350768316416
- https://tc39.es/proposal-regex-escaping/

### Speculation rules: tag field

#### What's New
Speculation rules may now include an optional `tag` field to label the source or purpose of a speculation rule.

#### Technical Details
Tags attached to speculation rules are transmitted via the `Sec-Speculation-Tags` header, allowing intermediaries or servers to treat speculations differently based on origin.

#### Use Cases
Better observability and routing of prerender/prefetch speculation traffic, allowing intermediaries and servers to apply policy or logging per-tag.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=381687257
- https://chromestatus.com/feature/5100969695576064
- https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-tag

### Update ProgressEvent to use double type for loaded and total

#### What's New
The `loaded` and `total` attributes on `ProgressEvent` are changed from `unsigned long long` to `double`.

#### Technical Details
Using `double` permits fractional and very large values with floating semantics, aligning representation with web developers’ expectations for progress reporting.

#### Use Cases
Enables more precise progress reporting (fractions, partial units) in XHR/Fetch progress handlers and aligns implementations for long-running transfers or aggregated progress computations.

#### References
- https://chromestatus.com/feature/5084700244254720
- https://xhr.spec.whatwg.org/#interface-progressevent

File location to be saved (per spec): digest_markdown/webplatform/Web API/chrome-136-stable-en.md
