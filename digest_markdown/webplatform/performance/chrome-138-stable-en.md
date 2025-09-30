# Area Summary

Chrome 138 (stable) introduces focused improvements in prerendering and caching control that directly affect page load strategies and resource lifecycle management. The most impactful changes let developers clear prefetch and prerender caches via Clear-Site-Data and provide finer hints for navigation speculation with a new target_hint field. These updates advance the web platform by giving sites deterministic controls over background fetch/prerender artifacts and by improving prerender activation accuracy. They matter because they help teams optimize perceived performance while maintaining predictable resource and privacy behavior.

## Detailed Updates

Below are the Performance-specific changes from Chrome 138 that connect to the summary above.

### Add prefetchCache and prerenderCache to Clear-Site-Data header

#### What's New
Two new values for the Clear-Site-Data header let developers target clearing the prerender and prefetch caches: "prefetchCache" and "prerenderCache".

#### Technical Details
These are additive cache-directive values for the Clear-Site-Data header as defined by the Clear Site Data spec. When sent by a site, the header instructs the browser to clear the specified caches (now including prefetch and prerender caches), enabling more precise resource cleanup.

#### Use Cases
- Invalidate prefetched or prerendered resources after authentication changes or privacy-sensitive actions.
- Ensure stale prerendered pages do not get activated after a significant state change.
- Better lifecycle control for aggressive prefetch/prerender strategies used to optimize perceived load time.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=398149359 — Tracking bug #398149359
- https://chromestatus.com/feature/5110263659667456 — ChromeStatus.com entry
- https://w3c.github.io/webappsec-clear-site-data/#grammardef-cache-directive — Spec

### Speculation rules: target_hint field

#### What's New
Speculation rules syntax is extended to allow a target_hint field that provides a hint indicating the target navigable where a prerendered page will eventually be activated (e.g., `_blank`).

#### Technical Details
The target_hint is a hint-only directive within the nav-speculation rules grammar. It communicates expected activation targets to the browser so prerendering decisions and activation paths can be better aligned with developer intent.

#### Use Cases
- Improve prerender activation accuracy when a link is expected to open in a new browsing context (such as `_blank`).
- Reduce wasted prerendering by aligning speculation rules with intended navigation targets.
- Help developers coordinate prerendering with UI patterns that open pages in specific targets or windows.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40234240 — Tracking bug #40234240
- https://chromestatus.com/feature/5084493854924800 — ChromeStatus.com entry
- https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-target-hint — Spec

Saved to: digest_markdown/webplatform/Performance/chrome-138-stable-en.md