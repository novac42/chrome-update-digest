# Chrome 140 Stable - Deprecation Features

## Summary

Chrome 140 introduces two significant deprecations focused on web standards alignment and accessibility improvements. The release removes the legacy `Purpose: prefetch` header in favor of the standardized `Sec-Purpose` header, and deprecates problematic H1 font size rules that cause accessibility issues in sectioning elements.

## Feature Details

### Stop sending `Purpose: prefetch` header from prefetches and prerenders

**What Changed**:
Chrome is removing the legacy `Purpose: prefetch` header from prefetch and prerender operations, replacing it with the standardized `Sec-Purpose` header. This change affects speculation rules prefetch, speculation rules prerender, `<link rel=prefetch>`, and Chromium's non-standard `<link rel=prerender>`. The deprecation aligns Chrome with web standards and improves consistency across prefetching mechanisms. Developers should update their server-side logic to handle the `Sec-Purpose` header instead of relying on the deprecated `Purpose: prefetch` header.

**References**:
- [Tracking bug #420724819](https://issues.chromium.org/issues/420724819)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320)
- [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

### Deprecate special font size rules for H1 within some elements

**What Changed**:
Chrome is deprecating the HTML specification's special font size rules for `<h1>` elements nested within `<article>`, `<aside>`, `<nav>`, or `<section>` elements. These rules automatically reduce the font size of H1 headings based on their nesting depth within sectioning elements. The deprecation addresses significant accessibility concerns, as these rules can create confusing heading hierarchies that don't match the visual presentation, making content harder to navigate for screen reader users. Developers should explicitly style headings using CSS rather than relying on these automatic size adjustments.

**References**:
- [a list of special rules](https://html.spec.whatwg.org/multipage/rendering.html#sections-and-headings)
- [Tracking bug #394111284](https://issues.chromium.org/issues/394111284)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6192419898654720)
- [Spec](https://github.com/whatwg/html/pull/11102)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)