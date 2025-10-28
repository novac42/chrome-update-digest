---
layout: default
title: chrome-140-en
---

## Area Summary

Chrome 140's deprecations focus on removing legacy behaviors that cause compatibility and accessibility issues. The most impactful changes are replacing the legacy Purpose header from prefetch/prerender requests with the standardized Sec-Purpose header, and removing special-case font-size rules for H1 inside certain sectioning elements. These updates reduce ambiguity for feature detection and improve accessibility and consistency across user agents. Developers should audit reliance on the old header and implicit heading sizing and adopt explicit, standards-aligned patterns.

## Detailed Updates

Below are concise, developer-focused descriptions of each deprecation and what to do next.

### Stop sending `Purpose: prefetch` header from prefetches and prerenders

#### What's New
Prefetches and prerenders no longer send the legacy `Purpose: prefetch` request header; they use the standardized `Sec-Purpose` header instead.

#### Technical Details
This change affects speculation rules `prefetch` and `prerender`, `<link rel=prefetch>`, and Chromium's non-standard `<link rel=prerender>`. The legacy `Purpose` header is being removed in favor of the Sec-Purpose header defined by the nav-speculation draft.

#### Use Cases
- Server-side logic that previously relied on `Purpose: prefetch` must be updated to check `Sec-Purpose`.
- Analytics or caching layers that inspect request headers for prefetch behavior should migrate to the new header.
- Feature detection or heuristics based on the old header should be revised to use standard signals.

#### References
- [Tracking bug #420724819](https://issues.chromium.org/issues/420724819)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320)
- [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

### Deprecate special font size rules for H1 within some elements

#### What's New
The HTML spec's legacy special rules that adjust `<h1>` font sizing when nested inside `<article>`, `<aside>`, `<nav>`, or `<section>` are being deprecated due to accessibility concerns.

#### Technical Details
The deprecated rules are those listed in the HTML rendering section for sections and headings. The change removes implicit user-agent sizing exceptions so authors should not rely on built-in special-case scaling for `<h1>` in those elements.

#### Use Cases
- Authors should explicitly control heading sizes in CSS instead of relying on UA special cases.
- Accessibility-focused workflows and automated tests should verify heading semantics and sizing explicitly.
- Component libraries and themes must ensure consistent heading styles across contexts by setting explicit CSS rules.

#### References
- [a list of special rules](https://html.spec.whatwg.org/multipage/rendering.html#sections-and-headings)
- [Tracking bug #394111284](https://issues.chromium.org/issues/394111284)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6192419898654720)
- [Spec](https://github.com/whatwg/html/pull/11102)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)

## Area-Specific Expertise (Deprecations)

- css: Remove reliance on UA special-case heading sizes; set explicit CSS rules for headings in components and themes.
- webapi: Update server-side and client-side logic to read `Sec-Purpose` instead of `Purpose` for prefetch/prerender signals.
- graphics-webgpu: No direct impact from these deprecations.
- javascript: Avoid feature detection that inspects the old `Purpose` header; use standardized fetch request semantics.
- security-privacy: Switching to `Sec-Purpose` aligns with standardized header scoping and intent signalling; update privacy-aware server logic.
- performance: Prefetch/prerender behavior is unchanged functionally, but header change may affect caching/analytics—update pipelines accordingly.
- multimedia: No direct impact from these deprecations.
- devices: No direct impact from these deprecations.
- pwa-service-worker: Service workers that conditionally respond to prefetch requests should look for `Sec-Purpose`.
- webassembly: No direct impact from these deprecations.
- deprecations: Migration paths—replace checks for `Purpose: prefetch` with `Sec-Purpose`, and explicitly style heading sizes rather than relying on deprecated UA rules.
