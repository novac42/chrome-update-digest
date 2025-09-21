---
layout: default
title: chrome-140
---

## Removals

### Stop sending `Purpose: prefetch` header from prefetches and prerenders

Prefetches and prerenders now use the `Sec-Purpose` header, therefore the legacy `Purpose: prefetch` header is being removed.

This will be scoped to speculation rules `prefetch`, speculation rules `prerender`, `<link rel=prefetch>`, and Chromium's non-standard `<link rel=prerender>`.

[Tracking bug #420724819](https://issues.chromium.org/issues/420724819) | [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320) | [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

### Deprecate special font size rules for H1 within some elements

The HTML spec contains [a list of special rules](https://html.spec.whatwg.org/multipage/rendering.html#sections-and-headings) for `<h1>` tags nested within `<article>`, `<aside>`, `<nav>`, or `<section>` tags:

These special rules are deprecated, because they cause accessibility issues. Namely, they visually reduce the font size for nested `<h1>` elements so that they "look" like `<h2>` elements, but nothing in the accessibility tree reflects this demotion.

[Tracking bug #394111284](https://issues.chromium.org/issues/394111284) | [ChromeStatus.com entry](https://chromestatus.com/feature/6192419898654720) | [Spec](https://github.com/whatwg/html/pull/11102)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-02 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-09-02 UTC."],[],[],null,[]] 
