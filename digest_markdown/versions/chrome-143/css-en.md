---
layout: default
title: css-en
---

## Area Summary

Chrome 143's CSS updates focus on giving developers finer, more deterministic control over layout, background positioning, and typography, while also standardizing update behavior for web apps. The most impactful changes are anchored fallback container queries for anchor-positioned elements and side-relative background-position longhands, which improve responsive and tethered layouts. The addition of `font-language-override` enables precise OpenType language behavior for multi-language typography. Together these updates advance the platform by expanding responsive layout primitives and typographic control, and by making app update behavior more predictable.

## Detailed Updates

The following items expand on the summary above with concise, developer-focused details and references.

### CSS anchored fallback container queries

#### What's New
Introduces `@container anchored(fallback)` to style descendants of anchor-positioned elements based on which `position-try-fallbacks` is applied.

#### Technical Details
Enables container queries scoped to anchored elements so styles can react to the fallback positioning behavior of anchors and anchored elements.

#### Use Cases
Style tethers, animations, or layout of anchored elements depending on which fallback positioning is used at runtime.

#### References
- [Tracking bug #417621241](https://issues.chromium.org/issues/417621241)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5177580990496768)
- [Spec](https://drafts.csswg.org/css-anchor-position-2/#anchored-container-queries)

### Side-relative syntax for `background-position-x/y` longhands

#### What's New
Defines side-relative syntax for background image positioning, allowing positions to be specified relative to an edge rather than fixed values.

#### Technical Details
Provides a more flexible, responsive mechanism for background positioning that adapts to window or frame size; the feature is also applied to related vendor-prefixed longhands.

#### Use Cases
Responsive background placements that need to align relative to an element edge without recalculating fixed offsets for different viewport sizes.

#### References
- [Tracking bug #40468636](https://issues.chromium.org/issues/40468636)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5073321259565056)
- [Spec](https://drafts.csswg.org/css-backgrounds-4/#background-position-longhands)

### Implement CSS property `font-language-override`

#### What's New
Adds support for the `font-language-override` CSS property to override the system language used for OpenType glyph substitution via a four-character language tag.

#### Technical Details
The property lets authors specify a direct language tag in CSS to influence OpenType substitutions, giving stylesheet-level control over language-specific typographic features.

#### Use Cases
Fine-grained typographic control for multilingual content, ensuring consistent glyph selection and shaping across platforms.

#### References
- [Tracking bug #41170551](https://issues.chromium.org/issues/41170551)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5149766073843712)
- [Spec](https://www.w3.org/TR/css-fonts-4/#font-language-override-prop)

### Web App Manifest: specify update eligibility

#### What's New
Adds a way to specify an update eligibility algorithm in the Web App Manifest to make update applicability more deterministic.

#### Technical Details
The manifest-level setting gives developers control over whether and when updates apply to existing installations, enabling removal of the _update check throttle_.

#### Use Cases
Predictable update rollouts for installed web apps where developers need deterministic control over update timing and eligibility.

#### References
- [Tracking bug #403253129](https://issues.chromium.org/issues/403253129)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5148463647686656)

Saved to: digest_markdown/webplatform/CSS/chrome-143-stable-en.md
