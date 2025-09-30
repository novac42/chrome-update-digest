---
layout: default
title: css-en
---

## Area Summary

Chrome 140 (stable) advances CSS with a focus on stronger type-aware math, finer-grained animation control, improved view-transition fidelity, and more explicit scrolling and font controls. Key changes that matter to developers include CSS typed arithmetic for unit-safe calculations, expanded view-transition inheritance and nesting for smoother UI animations, and new scrolling primitives like scroll-target-group and a container option for scrollIntoView. These updates reduce authoring complexity, improve accessibility and animation consistency, and enable more predictable layout and scrolling behavior across complex component trees.

## Detailed Updates

The items below expand on the summary above and list each CSS-area feature exposed in Chrome 140.

### CSS typed arithmetic

#### What's New
Typed arithmetic enables writing unit-aware expressions in CSS (e.g., `calc(10em / 1px)`), allowing conversion between typed and untyped values inside `calc()`.

#### Technical Details
Expressions perform type-checked arithmetic per the CSS Values Level 4 spec, letting authors convert typed values into numbers and recombine units safely.

#### Use Cases
Useful for typography and any layout that needs unit conversions or reuse of typed values in number-accepting properties.

#### References
- https://issues.chromium.org/issues/40768696 (Tracking bug #40768696)  
- https://chromestatus.com/feature/4740780497043456 (ChromeStatus.com entry)  
- https://www.w3.org/TR/css-values-4/#calc-type-checking (Spec)

### CSS `caret-animation` property

#### What's New
Introduces the `caret-animation` property with values `auto` and `manual` to prevent the default caret blink from interfering with `caret-color` animations.

#### Technical Details
`auto` preserves browser default blinking; `manual` disables default blinking so color animations can run smoothly.

#### Use Cases
Animate caret color reliably during custom input animations or editor UIs.

#### References
- https://issues.chromium.org/issues/329301988 (Tracking bug #329301988)  
- https://chromestatus.com/feature/5082469066604544 (ChromeStatus.com entry)  
- https://drafts.csswg.org/css-ui/#caret-animation (Spec)

### highlightsFromPoint API

#### What's New
Adds an API to detect custom highlights at a document point, including within shadow DOM and overlapping highlight regions.

#### Technical Details
The API returns highlights intersecting a point, enabling programmatic interaction with the CSS Highlight API model.

#### Use Cases
Tooling and editors that need to resolve which semantic highlights are present at a pointer location or build precise highlight interactions.

#### References
- https://issues.chromium.org/issues/365046212 (Tracking bug #365046212)  
- https://chromestatus.com/feature/4552801607483392 (ChromeStatus.com entry)  
- https://drafts.csswg.org/css-highlight-api-1/#interactions (Spec)

### `ScrollIntoView` container option

#### What's New
Adds a `container` option to `ScrollIntoViewOptions` to restrict scrolling to the nearest ancestor scroll container.

#### Technical Details
When `container` is used, only the nearest scroll container is scrolled to bring the target into view; higher-level scrolling is not performed.

#### Use Cases
Component-scoped scrolling (e.g., virtualized lists or nested scroll containers) where authors want to avoid scrolling the entire viewport.

#### References
- https://chromestatus.com/feature/5100036528275456 (ChromeStatus.com entry)  
- https://drafts.csswg.org/cssom-view/#dom-scrollintoviewoptions-container (Spec)

### View transitions: Inherit more animation properties

#### What's New
View transitions now inherit additional animation properties through the view-transition pseudo tree: `animation-timing-function`, `animation-iteration-count`, `animation-direction`, and `animation-play-state`.

#### Technical Details
These properties propagate to transition pseudo-elements to better match the originating element animation semantics during view transitions.

#### Use Cases
Creates more consistent cross-fade and motion effects when using the View Transitions API, preserving animation behavior.

#### References
- https://issues.chromium.org/issues/427741151 (Tracking bug #427741151)  
- https://chromestatus.com/feature/5154752085884928 (ChromeStatus.com entry)  
- https://www.w3.org/TR/css-view-transitions-2 (Spec)

### View transition pseudos inherit animation-delay.

#### What's New
`animation-delay` is now inherited through the view transition pseudo tree so delays on source elements apply to transition pseudo-elements.

#### Technical Details
Propagation of `animation-delay` aligns timing of pseudo-elements with source animations during view transitions.

#### Use Cases
Preserves intended animation timing when using view transitions that depend on delays.

#### References
- https://chromestatus.com/feature/5424291457531904 (ChromeStatus.com entry)  
- https://www.w3.org/TR/css-view-transitions-2 (Spec)

### Nested view transitions groups

#### What's New
View transitions can generate a nested pseudo-element tree instead of a flat one, enabling more faithful reproduction of element nesting.

#### Technical Details
Nested pseudo trees allow nested clipping, 3D transforms, and correct application of effects such as opacity and masking within view transitions.

#### Use Cases
Complex UI transitions that rely on nested transforms, clipping, or stacking contexts benefit from more accurate visual fidelity.

#### References
- https://issues.chromium.org/issues/399431227 (Tracking bug #399431227)  
- https://chromestatus.com/feature/5162799714795520 (ChromeStatus.com entry)  
- https://www.w3.org/TR/css-view-transitions-2/#view-transition-group-prop (Spec)

### Propagate viewport `overscroll-behavior` from root

#### What's New
`overscroll-behavior` is propagated from the root (`<html>`) element to the viewport, aligning with the CSS Working Group resolution.

#### Technical Details
This change stops relying on `<body>` for viewport propagation and instead uses the root element as the source for viewport-level `overscroll-behavior`.

#### Use Cases
More predictable overscroll behavior across pages and components; authors should apply viewport-level controls on `:root`/`<html>`.

#### References
- https://issues.chromium.org/issues/41453796 (Tracking bug #41453796)  
- https://chromestatus.com/feature/6210047134400512 (ChromeStatus.com entry)  
- https://drafts.csswg.org/css-overscroll-behavior-1 (Spec)

### CSS `counter()` and `counters()` in alt text of `content` property

#### What's New
`counter()` and `counters()` can now be used within the alt text portion of the `content` property, enabling richer accessible text generation.

#### Technical Details
The `content` property's alt text subsystem accepts counter functions, allowing dynamic counter values to be included in generated content.

#### Use Cases
Improves accessibility for generated content like lists or annotated items where counters convey semantic order or numbering.

#### References
- https://issues.chromium.org/issues/417488055 (Tracking bug #417488055)  
- https://chromestatus.com/feature/5185442420621312 (ChromeStatus.com entry)  
- https://drafts.csswg.org/css-content/#content-property (Spec)

### CSS `scroll-target-group` property

#### What's New
Introduces `scroll-target-group` to mark elements as scroll marker group containers with values like `none` and `auto`.

#### Technical Details
The property controls group formation for scroll markers per the CSS Overflow Module Level 5 draft.

#### Use Cases
Authors can control scroll marker grouping to influence scroll-snapping, markers, or related scrolling behavior across container groups.

#### References
- https://issues.chromium.org/issues/6607668 (Tracking bug #6607668)  
- https://chromestatus.com/feature/5189126177161216 (ChromeStatus.com entry)  
- https://drafts.csswg.org/css-overflow-5/#scroll-target-group (Spec)

### Support `font-variation-settings` descriptor in `@font-face` rule

#### What's New
Adds support for the string-based `font-variation-settings` descriptor inside `@font-face` rules in Chromium.

#### Technical Details
The descriptor allows authors to specify default variable font axis settings at font-face declaration time rather than only via element-level properties.

#### Use Cases
Improves typographic control by enabling authors to register @font-face variants with specific variation axis defaults for consistent rendering.

#### References
- https://issues.chromium.org/issues/40398871 (Tracking bug #40398871)  
- https://chromestatus.com/feature/5221379619946496 (ChromeStatus.com entry)  
- https://www.w3.org/TR/css-fonts-4/#font-rend-desc (Spec)

Saved to: digest_markdown/webplatform/CSS/chrome-140-stable-en.md
