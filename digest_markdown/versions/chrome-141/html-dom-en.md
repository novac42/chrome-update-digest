---
layout: default
title: html-dom-en
---

## Area Summary

Chrome 141’s HTML-DOM updates center on accessibility reliability and standards-aligned DOM revealing behavior. The new ARIA Notify API gives developers direct, programmatic control over screen reader announcements, improving upon ARIA live regions and decoupling announcements from DOM mutations. Meanwhile, algorithm updates for hidden=until-found and details elements prevent infinite loops during ancestor revealing, improving robustness. Together, these changes advance accessible UX and platform correctness with minimal authoring complexity.

## Detailed Updates

These updates strengthen accessibility ergonomics and ensure spec-compliant, robust DOM revealing behavior.

### ARIA Notify API

#### What's New
Provides a JavaScript API, ariaNotify, that lets content authors instruct screen readers on what to announce, improving reliability over ARIA live regions and enabling announcements not tied to DOM updates.

#### Technical Details
- Programmatic announcement mechanism independent of DOM mutations for more consistent output.
- Improves control and reliability compared to live regions.
- Tracks the W3C ARIA specification work referenced below.

#### Use Cases
- Announcing asynchronous events (e.g., network results) without modifying the DOM.
- Providing clear, immediate alerts or confirmations beyond live region constraints.
- Ensuring consistent accessibility announcements across dynamic UI flows.

#### References
- Tracking bug #326277796: https://issues.chromium.org/issues/326277796
- ChromeStatus.com entry: https://chromestatus.com/feature/5745430754230272
- Spec: https://github.com/w3c/aria/pull/2577

### Update `hidden=until-found` and details ancestor revealing algorithm

#### What's New
Implements spec changes to the revealing algorithms for hidden=until-found and details elements to prevent the browser from entering an infinite loop.

#### Technical Details
- Adjusts the ancestor revealing procedure to avoid infinite loops during reveal logic.
- Aligns Chrome’s behavior with the latest WHATWG HTML specification updates.

#### Use Cases
- More reliable reveal behavior for hidden=until-found content in search/UA reveal flows.
- Predictable details element expansion without risk of hang or loop.
- Improves resilience for applications relying on built-in revealing semantics.

#### References
- Tracking bug #433545121: https://issues.chromium.org/issues/433545121
- ChromeStatus.com entry: https://chromestatus.com/feature/5179013869993984
- Spec: https://github.com/whatwg/html/pull/11457
