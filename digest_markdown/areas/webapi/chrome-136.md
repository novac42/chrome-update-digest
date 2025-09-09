---
layout: default
title: chrome-136
---

## Web APIs

### Dispatch click events to captured pointer

If a pointer is captured while the `pointerup` event is being dispatched, the click event is now dispatched to the captured target instead of the nearest common ancestor of `pointerdown` and `pointerup` events as per the UI Event spec. For uncaptured pointers, the click target remains unchanged.

**References:** [Tracking bug #40851596](https://bugs.chromium.org/p/chromium/issues/detail?id=40851596) | [ChromeStatus.com entry](https://chromestatus.com/feature/5045063816396800) | [Spec](https://w3c.github.io/uievents/#event-type-click)

### Explicit compile hints with magic comments

Allows attaching of information about which functions should be eager parsed and compiled in JavaScript files. The information is encoded as magic comments.

**References:** [Tracking bug #13917](https://bugs.chromium.org/p/chromium/issues/detail?id=13917) | [ChromeStatus.com entry](https://chromestatus.com/feature/5047772830048256) | [Spec](https://github.com/v8/v8/wiki/Design-Elements#compile-hints)

### Incorporate navigation initiator into the HTTP cache partition key

Chrome's HTTP cache keying scheme is updated to include an `is-cross-site-main-frame-navigation` boolean to mitigate cross-site leak attacks involving top-level navigation. Specifically, this will prevent cross-site attacks in which an attacker can initiate a top-level navigation to a given page and then navigate to a resource known to be loaded by the page in order to infer sensitive information using load timing. This change also improves privacy by preventing a malicious site from using navigations to infer whether a user has visited a given site previously.

**References:** [Tracking bug #398784714](https://bugs.chromium.org/p/chromium/issues/detail?id=398784714) | [ChromeStatus.com entry](https://chromestatus.com/feature/5108419906535424) | [Spec](https://httpwg.org/specs/rfc9110.html#caching)

### Protected audience: text conversion helpers

Protected Audience bidding and scoring scripts that interface with WebAssembly need to efficiently convert string-typed data to (and from) byte arrays (for example, to pass strings into and out of WebAssembly with the "memory" ArrayBuffer). This provides two standalone functions, `protectedAudience.encodeUtf8`, and `protectedAudience.decodeUtf8` to perform these tasks about an order of magnitude more efficiently than doing it in JavaScript.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5099738574602240)

### RegExp.escape

`RegExp.escape` is a static method that takes a string and returns an escaped version that may be used as a pattern inside a regular expression.

**Example:**

```javascript
const str = prompt("Please enter a string");
const escaped = RegExp.escape(str);
const re = new RegExp(escaped, 'g');
// handles reg exp special tokens with the replacement.
console.log(ourLongText.replace(re));
```

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5074350768316416) | [Spec](https://tc39.es/proposal-regex-escaping/)

### Speculation rules: tag field

This enables developers to add `tag` field to speculation rules. This optional field can be used to track the source of speculation rules. For example, to treat them differently at an intermediary server. Any tags associated with a speculation will be sent with the `Sec-Speculation-Tags` header.

**References:** [Tracking bug #381687257](https://bugs.chromium.org/p/chromium/issues/detail?id=381687257) | [ChromeStatus.com entry](https://chromestatus.com/feature/5100969695576064) | [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-tag)

### Update ProgressEvent to use double type for loaded and total

The `ProgressEvent` has attributes `loaded` and `total` indicating the progress, and their type is `unsigned long long` now. With this feature, the type for these two attributes is changed to `double` instead, which gives the developer more control over the value. For example, the developers can now create a `ProgressEvent` with the total of 1 and the loaded increasing from 0 to 1 gradually. This is aligned with the default behavior of the `<progress>` HTML element if the max attribute is omitted.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5084700244254720) | [Spec](https://xhr.spec.whatwg.org/#interface-progressevent)
