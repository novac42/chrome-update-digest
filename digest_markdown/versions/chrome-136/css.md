---
layout: default
title: css
---

## CSS and UI

### The dynamic-range-limit property

Enables a page to limit the maximum brightness of HDR content.

**References:** [Tracking bug #1470298](https://bugs.chromium.org/p/chromium/issues/detail?id=1470298) | [ChromeStatus.com entry](https://chromestatus.com/feature/5023877486493696) | [Spec](https://www.w3.org/TR/css-color-hdr/#dynamic-range-limit)

### Partition :visited links history

To eliminate user browsing history leaks, anchor elements are styled as `:visited` only if they have been clicked from this top-level site and frame origin before. There is an exception for "self-links", where links to a site's own pages can be styled as `:visited` even if they have not been clicked on in this exact top-level site and frame origin before. This exemption is only enabled in top-level frames or subframes which are same-origin with the top-level frame. The privacy benefits are still achieved because sites already know which of its subpages a user has visited, so no new information is exposed. This was a community-requested exception which improves user experience.

**References:** [Tracking bug #1448609](https://bugs.chromium.org/p/chromium/issues/detail?id=1448609) | [ChromeStatus.com entry](https://chromestatus.com/feature/5029851625472000) | [Spec](https://www.w3.org/TR/css-pseudo-4/#visited-pseudo)

### Unprefixed print-color-adjust

The `print-color-adjust` property lets you adjust colors in printed web pages. This is the same as Chrome's already-supported `-webkit-print-color-adjust`, but with a standardized name. The `-webkit-` prefixed version is not removed.

**References:** [MDN Docs](https://developer.mozilla.org/docs/Web/CSS/print-color-adjust) | [Tracking bug #376381169](https://bugs.chromium.org/p/chromium/issues/detail?id=376381169) | [ChromeStatus.com entry](https://chromestatus.com/feature/5090690412953600) | [Spec](https://www.w3.org/TR/css-color-adjust-1/#print-color-adjust)

### Rename string attr() type to raw-string

The CSS Working Group has resolved to replace `string` `attr()` type with `raw-string`. Therefore from Chrome 136 `attr(data-foo string)` becomes `attr(data-foo raw-string)`.

**References:** [Tracking bug #400981738](https://bugs.chromium.org/p/chromium/issues/detail?id=400981738) | [ChromeStatus.com entry](https://chromestatus.com/feature/5110654344216576) | [Spec](https://www.w3.org/TR/css-values-5/#attr-notation)

### Type-agnostic var() fallback

The fallback part of a `var()` function does not validate against the type of the custom property being referenced.

**References:** [Tracking bug #372475301](https://bugs.chromium.org/p/chromium/issues/detail?id=372475301) | [ChromeStatus.com entry](https://chromestatus.com/feature/5049845796618240)
