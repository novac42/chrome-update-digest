---
layout: default
title: deprecation-en
---

## Area Summary

Chrome 140 (stable) continues targeted deprecations that reduce legacy behaviors and improve security, privacy, and accessibility. The release removes the legacy Purpose: prefetch header in favor of Sec-Purpose for speculation-related fetches, and deprecates special HTML font-size rules for H1 inside certain sectioning elements. These changes remove inconsistent or legacy behaviors, simplify the platform surface, and reduce accessibility and fingerprinting risks. Teams should plan migrations to Sec-Purpose and update CSS/author styles to avoid relying on the deprecated H1 rules.

## Detailed Updates

The items below expand on the summary above and provide actionable details for developers and implementers.

### Stop sending `Purpose: prefetch` header from prefetches and prerenders

#### What's New
Chromium will stop sending the legacy `Purpose: prefetch` header for prefetch and prerender speculation; these will use the `Sec-Purpose` header instead.

#### Technical Details
This change applies to speculation rules `prefetch` and `prerender`, `<link rel=prefetch>`, and Chromium's non-standard `<link rel=prerender>`. The behavioral change replaces an older header with the standardized `Sec-Purpose` signal to convey intent for speculative fetches.

#### Use Cases
- Reduce fingerprinting and standardize intent signaling for speculative fetches.
- Servers and analytics should switch to inspect `Sec-Purpose` rather than `Purpose: prefetch`.
- Feature gating or server-side optimizations tied to the old header must be migrated.

#### References
- https://issues.chromium.org/issues/420724819
- https://chromestatus.com/feature/5088012836536320
- https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch

### Deprecate special font size rules for H1 within some elements

#### What's New
The special-casing of `<h1>` font-size when nested inside `<article>`, `<aside>`, `<nav>`, or `<section>` as per legacy HTML rendering rules is being deprecated.

#### Technical Details
The deprecation removes author-agent special rules that altered H1 presentation based on sectioning ancestor elements. This is being done because those rules cause accessibility and consistency problems across user agents and assistive technologies.

#### Use Cases
- Developers should not rely on UA-specific font-size adjustments for H1 in these containers; instead, use explicit CSS to control heading sizes.
- Accessibility-focused teams should audit heading semantics and styles to ensure consistent reading order and size expectations.
- Migration: add explicit CSS rules targeting headings in your document structure rather than relying on deprecated UA defaults.

#### References
- https://html.spec.whatwg.org/multipage/rendering.html#sections-and-headings
- https://issues.chromium.org/issues/394111284
- https://chromestatus.com/feature/6192419898654720
- https://github.com/whatwg/html/pull/11102
- https://creativecommons.org/licenses/by/4.0/
- https://www.apache.org/licenses/LICENSE-2.0
- https://developers.google.com/site-policies

File to save: digest_markdown/webplatform/deprecation/chrome-140-stable-en.md
