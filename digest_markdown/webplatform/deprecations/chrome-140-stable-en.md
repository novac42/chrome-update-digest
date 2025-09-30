## Area Summary

Chrome 140 deprecations focus on removing legacy behavior and improving platform consistency and accessibility. The release stops sending the legacy `Purpose: prefetch` header in favor of the standardized `Sec-Purpose` header, and deprecates special-case font-size rules for `<h1>` nested in certain sectioning elements. These changes reduce fragmentation between implementations and address accessibility concerns, respectively. They matter because maintainers of servers, middleware, and CSS/UA logic should update expectations to preserve correct behavior and accessibility across browsers.

## Detailed Updates

The following items expand on the summary above and point to the primary references for migration and implementation guidance.

### Stop sending `Purpose: prefetch` header from prefetches and prerenders

#### What's New
Prefetches and prerenders now use the `Sec-Purpose` header; the legacy `Purpose: prefetch` header is being removed. This change is scoped to speculation rules `prefetch`, speculation rules `prerender`, `<link rel=prefetch>`, and Chromium's non-standard `<link rel=prerender>`.

#### Technical Details
The header emitted with prefetch/prerender fetches is transitioning from `Purpose: prefetch` to `Sec-Purpose`. Implementations and server-side logic that inspected the legacy header must recognize and handle `Sec-Purpose` instead.

#### Use Cases
Servers, proxies, analytics, or feature-gating middleware that relied on `Purpose: prefetch` should migrate their detection and handling to `Sec-Purpose` to maintain correct behavior for speculative fetches and prerenders.

#### References
- https://issues.chromium.org/issues/420724819 (Tracking bug #420724819)  
- https://chromestatus.com/feature/5088012836536320 (ChromeStatus.com entry)  
- https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch (Spec)  

### Deprecate special font size rules for H1 within some elements

#### What's New
The HTML specification's special rules for rendering `<h1>` elements when nested inside `<article>`, `<aside>`, `<nav>`, or `<section>` are deprecated due to accessibility issues.

#### Technical Details
The deprecation targets the rules documented in the HTML spec's "sections and headings" rendering guidance. The rationale cited accessibility concerns with these implicit special-case sizing behaviors; implementers and authors should consult the spec and tracking discussion for details.

#### Use Cases
Authors and user-agent implementers should avoid relying on these deprecated implicit rules for heading sizing. Where consistent presentation is required, prefer explicit CSS sizing or structured markup rather than implicit special-case behaviors.

#### References
- https://html.spec.whatwg.org/multipage/rendering.html#sections-and-headings (a list of special rules)  
- https://issues.chromium.org/issues/394111284 (Tracking bug #394111284)  
- https://chromestatus.com/feature/6192419898654720 (ChromeStatus.com entry)  
- https://github.com/whatwg/html/pull/11102 (Spec)  
- https://creativecommons.org/licenses/by/4.0/ (Creative Commons Attribution 4.0 License)  
- https://www.apache.org/licenses/LICENSE-2.0 (Apache 2.0 License)  
- https://developers.google.com/site-policies (Google Developers Site Policies)