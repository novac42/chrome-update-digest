---
layout: default
title: chrome-139-en
---

### 1. Area Summary

Chrome 139’s deprecations focus on tightening security and modernizing platform behavior by removing legacy behaviors and old-platform support. Key changes remove legacy fetch headers (Purpose: prefetch), drop support for macOS 11, and eliminate auto-detection for the ISO-2022-JP charset. These changes reduce attack surface and compatibility complexity, encourage use of standardized headers and modern OS versions, and align Chrome with other browsers’ safer defaults. Developers should plan migrations for header checks, update-targeted macOS support matrices, and ensure correct charset declarations.

## Detailed Updates

Below are the deprecations introduced in Chrome 139 that follow from the summary above, with concise technical notes and links for follow-up.

### Stop sending Purpose: prefetch header from prefetches and prerenders

#### What's New
Chrome will stop sending the legacy Purpose: prefetch header for prefetch and prerender requests; Sec-Purpose is used for these speculative requests instead. The removal is gated behind a feature flag/kill switch to mitigate compatibility regressions.

#### Technical Details
- The change migrates speculative fetch signaling to the Sec-Purpose header.
- Rollout guarded by a feature flag/kill switch to allow rollback if compatibility issues arise.
- Developers relying on Purpose: prefetch should observe Sec-Purpose semantics and update server-side logic.

#### Use Cases
- Server-side analytics or routing logic that previously inspected Purpose: prefetch must migrate to Sec-Purpose.
- Improves clarity of fetch intent for prerender/prefetch handling and aligns with the navigation speculation spec.

#### References
- https://issues.chromium.org/issues/420724819
- https://chromestatus.com/feature/5088012836536320
- https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch

### Remove support for macOS 11

#### What's New
Chrome 138 is the last release supporting macOS 11; starting in Chrome 139, macOS 11 is no longer supported. Chrome will continue to run on macOS 11 but will show a warning infobar and will not receive further updates.

#### Technical Details
- Systems remaining on macOS 11 will not receive Chrome updates on the stable channel; users must upgrade macOS to continue receiving Chrome updates.
- This change reduces testing and maintenance burden for older OS versions.

#### Use Cases
- Update project compatibility matrices and minimum supported macOS version notes.
- CI and automation that run browser tests on macOS should move to supported macOS versions to continue receiving Chrome updates.

#### References
- https://chromestatus.com/feature/4504090090143744

### Remove auto-detection of `ISO-2022-JP` charset in HTML

#### What's New
Chrome 139 removes auto-detection for the ISO-2022-JP charset in HTML due to known security concerns and very low usage; Safari already does not support such auto-detection.

#### Technical Details
- Auto-detection for ISO-2022-JP is disabled to mitigate encoding-based security differentials.
- Pages relying on auto-detection must explicitly declare character encoding via proper Content-Type headers or meta charset declarations.

#### Use Cases
- Audit legacy Japanese-content pages and ensure explicit charset declarations (e.g., meta charset or HTTP header) to avoid rendering regressions.
- Security-sensitive applications should prefer explicit encodings to eliminate ambiguity.

#### References
- https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/
- https://issues.chromium.org/issues/40089450
- https://chromestatus.com/feature/6576566521561088
- https://creativecommons.org/licenses/by/4.0/
- https://www.apache.org/licenses/LICENSE-2.0
- https://developers.google.com/site-policies
