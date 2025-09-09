---
layout: default
title: css
---

## CSS and UI

### CSS Sign-Related Functions: abs(), sign()

The sign-related functions `abs()` and `sign()` compute various functions related to the sign of their argument. The `abs(A)` function contains one calculation A, and returns the absolute value of A, as the same type as the input: if A's numeric value is positive or 0⁺, just A again; otherwise -1 * A. The `sign(A)` function contains one calculation A, and returns -1 if A's numeric value is negative, +1 if A's numeric value is positive, 0⁺ if A's numeric value is 0⁺, and 0⁻ if A's numeric value is 0⁻. The return type is a `<number>`, made consistent with the type of the input calculation.

**References:** [MDN Docs:abs()](https://developer.mozilla.org/docs/Web/CSS/abs) | [Tracking bug #40253181](https://bugs.chromium.org/p/chromium/issues/detail?id=40253181) | [ChromeStatus.com entry](https://chromestatus.com/feature/5196860094464000) | [Spec](https://www.w3.org/TR/css-values-4/#sign-funcs)

### Interpolation progress functional notation: CSS progress() function

The `progress()` functional notation returns a `<number>` value representing the position of one calculation (the progress value) between two other calculations (the progress start value and progress end value). The `progress()` function is a math function.

**References:** [Tracking bug #40944203](https://bugs.chromium.org/p/chromium/issues/detail?id=40944203) | [ChromeStatus.com entry](https://chromestatus.com/feature/5096136905244672) | [Spec](https://www.w3.org/TR/css-values-5/#progress-notation)

### CSS sibling-index() and sibling-count()

The `sibling-index()` and `sibling-count()` functions can be used as integers in CSS property values to style elements based on their position among its siblings, or the total number of siblings respectively. These functions can be used directly as integer values, but more interestingly inside `calc()` expressions.

**References:** [Tracking bug #40282719](https://bugs.chromium.org/p/chromium/issues/detail?id=40282719) | [ChromeStatus.com entry](https://chromestatus.com/feature/5649901281918976) | [Spec](https://www.w3.org/TR/css-values-5/#sibling-functions)

### CSS stretch sizing keyword

A keyword for CSS sizing properties (for example, `width` and `height`) that lets elements grow to exactly fill their containing block's available space. It is similar to '100%', except the resulting size is applied to the element's margin box instead of the box indicated by `box-sizing`. Using this keyword lets the element keep its margins while still being as large as possible. An unprefixed version of `-webkit-fill-available`.

**References:** [Tracking bug #41253915](https://bugs.chromium.org/p/chromium/issues/detail?id=41253915) | [ChromeStatus.com entry](https://chromestatus.com/feature/5102457485459456) | [Spec](https://www.w3.org/TR/css-sizing-4/#valdef-width-stretch)

### CSS env variable for OS-level font scale

Exposes a user's preferred font scale to CSS. Without this, it's not practical for a page to detect if the user has changed their preferred font size using the Operating System's preferences. This CSS environment variable will reflect the scale chosen by the user.

**References:** [Tracking bug #397737223](https://bugs.chromium.org/p/chromium/issues/detail?id=397737223) | [ChromeStatus.com entry](https://chromestatus.com/feature/5106542883938304) | [Spec](https://www.w3.org/TR/css-env-1/#os-font-scale)
