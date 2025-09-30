---
layout: default
title: css-en
---

## Area Summary

Chrome 138 adds a set of CSS primitives that increase authors' ability to express math, layout-awareness, and user-preference-aware sizing directly in stylesheets. Key themes are new math functions (sign-related and progress), sibling-aware functions for position-based styling, a sizing keyword that fills available space, and an env() variable exposing OS font scale for accessibility. These changes reduce reliance on JavaScript for layout and responsive behavior and improve alignment between CSS and user preferences. For developers, the most impactful items are the sibling-index/count and OS font-scale env which enable richer, layout-sensitive and accessibility-aware styling without runtime scripts.

## Detailed Updates

The following entries expand on the summary above and list the Chrome 138 CSS-area features developers should evaluate for immediate impact.

### CSS Sign-Related Functions: abs(), sign()

#### What's New
Adds the sign-related functions `abs()` and `sign()` to CSS math functions.

#### Technical Details
`abs(A)` returns the absolute value of A, preserving the input numeric type; `sign()` computes sign-related results as defined by the spec.

#### Use Cases
Compute magnitudes and conditional math in calc() expressions and other numeric CSS contexts without JavaScript.

#### References
- https://developer.mozilla.org/docs/Web/CSS/abs
- https://bugs.chromium.org/p/chromium/issues/detail?id=40253181
- https://chromestatus.com/feature/5196860094464000
- https://www.w3.org/TR/css-values-4/#sign-funcs

### Interpolation progress functional notation: CSS progress() function

#### What's New
Introduces the `progress()` function that returns a `<number>` representing the interpolation position between two calculations.

#### Technical Details
`progress()` is a math functional notation that computes a progress value between start and end calculations as specified by the Values & Units spec.

#### Use Cases
Drive interpolation-based transitions or computed values where an element’s style should depend on a relative position between two numeric expressions.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40944203
- https://chromestatus.com/feature/5096136905244672
- https://www.w3.org/TR/css-values-5/#progress-notation

### CSS sibling-index() and sibling-count()

#### What's New
Adds `sibling-index()` and `sibling-count()` functions usable as integers in CSS property values.

#### Technical Details
`sibling-index()` yields an element’s position among its siblings; `sibling-count()` yields the total number of siblings. These can be used directly or inside `calc()`.

#### Use Cases
Style elements based on ordinal position (e.g., nth-like rules without selectors), create grid/sequence-aware spacing, or compute responsive offsets based on sibling counts.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40282719
- https://chromestatus.com/feature/5649901281918976
- https://www.w3.org/TR/css-values-5/#sibling-functions

### CSS stretch sizing keyword

#### What's New
Introduces a `stretch` keyword for CSS sizing properties that lets elements grow to exactly fill their containing block’s available space.

#### Technical Details
`stretch` behaves similarly to `100%` but applies to the element’s margin box rather than the box determined by `box-sizing`, per the CSS Sizing spec.

#### Use Cases
Simplify layouts that must fill available container space precisely (including margins) without extra calculations or layout hacks.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=41253915
- https://chromestatus.com/feature/5102457485459456
- https://www.w3.org/TR/css-sizing-4/#valdef-width-stretch

### CSS env variable for OS-level font scale

#### What's New
Exposes an env() variable that reflects the user’s OS-level preferred font scale to CSS.

#### Technical Details
The environment variable provides the OS font scale factor so pages can detect and respond to user-chosen system font scaling.

#### Use Cases
Improve accessibility by scaling UI or typography to match OS preferences, enabling pages to respect user settings without heuristic detection.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=397737223
- https://chromestatus.com/feature/5106542883938304
- https://www.w3.org/TR/css-env-1/#os-font-scale

Saved to: digest_markdown/webplatform/CSS/chrome-138-stable-en.md
