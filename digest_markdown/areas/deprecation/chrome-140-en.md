---
layout: default
title: Chrome 140 Stable - Deprecation Updates
---

# Chrome 140 Stable - Deprecation Updates

## Area Summary

Chrome 140 introduces two significant deprecations that modernize web platform behaviors while improving accessibility and standardization. The removal of the legacy `Purpose: prefetch` header completes the transition to the standardized `Sec-Purpose` header for all prefetch and prerender operations. Additionally, Chrome deprecates problematic font size rules for H1 elements nested within sectioning elements, addressing long-standing accessibility concerns where heading hierarchy became visually misleading. These changes reflect Chrome's commitment to web standards compliance and inclusive design principles.

## Detailed Updates

These deprecations represent important steps toward a more consistent and accessible web platform, removing legacy behaviors that have caused developer confusion and user experience issues.

### Stop sending `Purpose: prefetch` header from prefetches and prerenders

#### What's New
Chrome 140 removes the legacy `Purpose: prefetch` header from all prefetch and prerender operations, completing the migration to the standardized `Sec-Purpose` header introduced in earlier versions.

#### Technical Details
This change affects multiple prefetching mechanisms across the platform:
- Speculation rules `prefetch` and `prerender`
- `<link rel=prefetch>` elements
- Chromium's non-standard `<link rel=prerender>` elements

All these mechanisms now exclusively use the `Sec-Purpose` header, eliminating the redundant legacy header that was previously sent alongside the modern standard.

#### Use Cases
Developers who have built server-side logic around detecting prefetch requests should ensure their code relies on the `Sec-Purpose` header rather than the deprecated `Purpose` header. This standardization improves interoperability and aligns with current web specifications for resource loading hints.

#### References
- [Tracking bug #420724819](https://issues.chromium.org/issues/420724819)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320)
- [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

### Deprecate special font size rules for H1 within some elements

#### What's New
Chrome 140 deprecates the HTML specification's special font size rules that reduce the size of `<h1>` elements when nested within `<article>`, `<aside>`, `<nav>`, or `<section>` tags.

#### Technical Details
The HTML specification historically included rules that would progressively reduce the font size of `<h1>` elements based on their nesting depth within sectioning elements. These rules created a visual hierarchy that didn't match the semantic meaning of the heading levels, leading to accessibility problems where screen readers and other assistive technologies would interpret the document structure differently from its visual presentation.

#### Use Cases
This deprecation addresses critical accessibility issues where users relying on assistive technologies experienced confusion due to the mismatch between visual and semantic heading hierarchy. Developers should explicitly use appropriate heading levels (`<h1>` through `<h6>`) to create proper document structure rather than relying on these automatic font size adjustments. This change encourages better semantic HTML practices and improves the experience for users with disabilities.

#### References
- [a list of special rules](https://html.spec.whatwg.org/multipage/rendering.html#sections-and-headings)
- [Tracking bug #394111284](https://issues.chromium.org/issues/394111284)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6192419898654720)
- [Spec](https://github.com/whatwg/html/pull/11102)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)
```

The analysis has been saved to: `digest_markdown/webplatform/deprecation/chrome-140-stable-en.md`
