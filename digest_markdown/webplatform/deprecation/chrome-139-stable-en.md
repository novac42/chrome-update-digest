## Area Summary

Chrome 139 focuses on removing legacy behaviors and attack surfaces: legacy request headers, old OS support, and risky charset auto-detection are being deprecated. The most impactful changes for developers are the removal of the legacy Purpose: prefetch header (servers must rely on Sec-Purpose), the end of updates on macOS 11, and the removal of ISO-2022-JP auto-detection due to security concerns. These deprecations simplify the platform, align behavior with modern specs, and reduce security and compatibility burdens. Teams should audit server-side header handling, update macOS test environments, and validate encoding handling for legacy content.

## Detailed Updates

Below are concise, developer-focused descriptions of each deprecation listed above and what teams should consider when preparing for Chrome 139.

### Stop sending Purpose: prefetch header from prefetches and prerenders

#### What's New
Chrome will stop emitting the legacy `Purpose: prefetch` header for prefetches and prerenders; these requests now use the `Sec-Purpose` header. The removal will be gated behind a feature flag/kill switch to avoid broad compatibility breaks.

#### Technical Details
The platform has moved to the `Sec-Purpose` header as the standardized signal for prefetch/prerender intent. Implementations that still parse `Purpose: prefetch` should migrate to recognize `Sec-Purpose`. The change is tracked and coordinated with the nav-speculation prerendering spec to ensure consistent behavior.

#### Use Cases
- Server-side request handlers, analytics, and caching layers should be updated to read `Sec-Purpose`.
- Ad platforms or middleware that branch logic on `Purpose` should add support for `Sec-Purpose` before this header is removed behind the flag.
- QA should validate speculative navigations and prefetching flows against the spec.

#### References
- https://issues.chromium.org/issues/420724819
- https://chromestatus.com/feature/5088012836536320
- https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch

### Remove support for macOS 11

#### What's New
Chrome 138 is the final release supporting macOS 11; starting in Chrome 139, Chrome will no longer support macOS 11 for updates.

#### Technical Details
On systems running macOS 11, Chrome will continue to run but will display a warning infobar and will not receive further updates. Users must upgrade macOS to a supported version to continue receiving Chrome updates.

#### Use Cases
- IT administrators must plan OS upgrades for managed fleets to continue receiving Chrome updates.
- Developers and QA should stop relying on macOS 11 for ongoing browser testing; move test coverage to supported macOS versions.

#### References
- https://chromestatus.com/feature/4504090090143744

### Remove auto-detection of `ISO-2022-JP` charset in HTML

#### What's New
Chrome 139 removes automatic charset detection for `ISO-2022-JP` in HTML due to known security issues and low usage; Safari also does not support this auto-detection.

#### Technical Details
Auto-detection for `ISO-2022-JP` is being dropped to mitigate encoding-differential security risks. Sites relying on implicit detection must explicitly declare their charset to ensure correct rendering. Tracking and coordination for this removal are documented in project issues and platform status entries.

#### Use Cases
- Web developers should ensure pages using `ISO-2022-JP` explicitly declare the charset (e.g., via <meta charset> or HTTP headers).
- Security teams should note this reduces a vector for encoding-based attacks.
- Compatibility testing should verify behavior for legacy Japanese-encoded content in the absence of auto-detection.

#### References
- https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/
- https://issues.chromium.org/issues/40089450
- https://chromestatus.com/feature/6576566521561088
- https://creativecommons.org/licenses/by/4.0/
- https://www.apache.org/licenses/LICENSE-2.0
- https://developers.google.com/site-policies

File saved to: digest_markdown/webplatform/deprecation/chrome-139-stable-en.md