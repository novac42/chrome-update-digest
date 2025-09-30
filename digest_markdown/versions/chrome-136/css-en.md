---
layout: default
title: css-en
---

## Area Summary

Chrome 136 advances CSS around color management, privacy, and modernized syntax handling. Key changes include HDR brightness control (dynamic-range-limit), standardized print color control (unprefixed print-color-adjust), stricter :visited styling partitioning to prevent history leaks, a rename for `attr()` string types to `raw-string`, and more forgiving `var()` fallbacks. These updates improve developer control over rendering, align with evolving specs, and reduce privacy and interoperability pitfalls. For teams this means small code updates for spec alignment and clearer options for printing, HDR, and custom property fallbacks.

## Detailed Updates

Below are the CSS-area changes in Chrome 136 with concise technical context and developer-focused use cases.

### The dynamic-range-limit property

#### What's New
Enables a page to limit the maximum brightness of HDR content.

#### Technical Details
Provides a CSS property to constrain HDR brightness exposure on a per-page basis (see spec link).

#### Use Cases
Control perceived brightness for HDR images/videos to match site design or accessibility needs.

#### References
https://bugs.chromium.org/p/chromium/issues/detail?id=1470298  
https://chromestatus.com/feature/5023877486493696  
https://www.w3.org/TR/css-color-hdr/#dynamic-range-limit

### Partition :visited links history

#### What's New
To eliminate user browsing history leaks, anchor elements are styled as `:visited` only if they have been clicked from this top-level site and frame origin before. There is an exception for "self-links", where links to a site's own pages can be styled as `:visited` even if they have not been clicked...

#### Technical Details
The behavioral change partitions `:visited` styling by top-level site and frame origin to reduce cross-origin history inference.

#### Use Cases
Prevents sites from inferring cross-site link visit state; developers should not rely on `:visited` for cross-origin UX differences.

#### References
https://bugs.chromium.org/p/chromium/issues/detail?id=1448609  
https://chromestatus.com/feature/5029851625472000  
https://www.w3.org/TR/css-pseudo-4/#visited-pseudo

### Unprefixed print-color-adjust

#### What's New
The `print-color-adjust` property lets you adjust colors in printed web pages. This is the same as Chrome's already-supported `-webkit-print-color-adjust`, but with a standardized name. The `-webkit-` prefixed version is not removed.

#### Technical Details
Adds the unprefixed standard name alongside the existing `-webkit-` prefixed implementation to match the spec.

#### Use Cases
Use the standardized `print-color-adjust` for printing color fidelity; maintain `-webkit-print-color-adjust` for compatibility as needed.

#### References
https://developer.mozilla.org/docs/Web/CSS/print-color-adjust  
https://bugs.chromium.org/p/chromium/issues/detail?id=376381169  
https://chromestatus.com/feature/5090690412953600  
https://www.w3.org/TR/css-color-adjust-1/#print-color-adjust

### Rename string attr() type to raw-string

#### What's New
The CSS Working Group has resolved to replace `string` `attr()` type with `raw-string`. Therefore from Chrome 136 `attr(data-foo string)` becomes `attr(data-foo raw-string)`.

#### Technical Details
Syntax-level rename in `attr()` type annotations to follow the updated spec naming.

#### Use Cases
Update existing `attr(... string)` usages to `attr(... raw-string)` to conform with the spec and ensure forward compatibility.

#### References
https://bugs.chromium.org/p/chromium/issues/detail?id=400981738  
https://chromestatus.com/feature/5110654344216576  
https://www.w3.org/TR/css-values-5/#attr-notation

### Type-agnostic var() fallback

#### What's New
The fallback part of a `var()` function does not validate against the type of the custom property being referenced.

#### Technical Details
`var(--prop, fallback)` no longer enforces type matching between `--prop` and the fallback expression, per the spec decision.

#### Use Cases
Allows more flexible fallbacks for custom properties without requiring exact type matches; simplifies resilient theming and progressive enhancement.

#### References
https://bugs.chromium.org/p/chromium/issues/detail?id=372475301  
https://chromestatus.com/feature/5049845796618240

Saved to: digest_markdown/webplatform/CSS/chrome-136-stable-en.md
