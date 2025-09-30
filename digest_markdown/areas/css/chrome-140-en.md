---
layout: default
title: chrome-140-en
---

## Area Summary

Chrome 140 Stable advances CSS with improvements that increase precision (typed arithmetic), animation control (caret-animation and expanded view-transition inheritance), and layout/scrolling ergonomics (scroll-target-group, container-scoped scrollIntoView, and overscroll-behavior changes). Several additions target interactivity and accessibility: highlightsFromPoint, using counters in generated content alt text, and better font variation support in @font-face. Collectively, these changes give developers finer-grained control over layout, animation, and accessibility while aligning Chromium with evolving CSS specs.

## Detailed Updates

Below are the CSS-focused changes in Chrome 140 Stable that follow from the summary above.

### CSS typed arithmetic

#### What's New
Typed arithmetic lets you write expressions in CSS such as `calc(10em / 1px)` or `calc(20% / 0.5em * 1px)`, enabling conversion between typed and untyped values inside calc expressions.

#### Technical Details
Implements type-aware calc expressions per the CSS Values Level 4 spec to allow unit conversions and arithmetic that respect value types.

#### Use Cases
Typography and responsive layout calculations where converting between units (e.g., em to px) or combining percentages with absolute units is useful.

#### References
- https://issues.chromium.org/issues/40768696
- https://chromestatus.com/feature/4740780497043456
- https://www.w3.org/TR/css-values-4/#calc-type-checking

### CSS `caret-animation` property

#### What's New
Introduces the `caret-animation` property with values `auto` and `manual` to control interaction between caret-color animations and the default caret blinking.

#### Technical Details
Provides a mechanism to disable/retain browser-default blinking (`auto`) or opt into manual control (`manual`) so animated caret-color transitions aren’t disrupted by blink timing.

#### Use Cases
Smoothly animating caret color in editors, form inputs, or custom text controls without conflicting blinking behavior.

#### References
- https://issues.chromium.org/issues/329301988
- https://chromestatus.com/feature/5082469066604544
- https://drafts.csswg.org/css-ui/#caret-animation

### highlightsFromPoint API

#### What's New
Adds the `highlightsFromPoint` API to query which custom highlights exist at a document point, including inside shadow DOM.

#### Technical Details
Enables precise detection of overlapping or nested highlights at a coordinate, improving programmatic interaction with the CSS Highlight API.

#### Use Cases
Interactive annotation tools, editor UIs, or accessibility overlays that need to inspect or manipulate highlights under a pointer.

#### References
- https://issues.chromium.org/issues/365046212
- https://chromestatus.com/feature/4552801607483392
- https://drafts.csswg.org/css-highlight-api-1/#interactions

### `ScrollIntoView` container option

#### What's New
Adds a `container` option to ScrollIntoViewOptions so only the nearest ancestor scroll container is scrolled to bring the target into view.

#### Technical Details
Scopes scroll-into-view behavior to the nearest scroll container rather than the viewport or all scrollable ancestors.

#### Use Cases
Component libraries and scrollable widgets that need to bring elements into view without affecting outer page scrolling.

#### References
- https://chromestatus.com/feature/5100036528275456
- https://drafts.csswg.org/cssom-view/#dom-scrollintoviewoptions-container

### View transitions: Inherit more animation properties

#### What's New
View transitions now inherit additional animation properties through the pseudo tree: `animation-timing-function`, `animation-iteration-count`, `animation-direction`, and `animation-play-state`.

#### Technical Details
Extends inherited animation-related properties for the view transition pseudo-elements so transitions better reflect original element animations.

#### Use Cases
More consistent and expressive view transitions that preserve intended timing, iteration, direction, and play-state semantics.

#### References
- https://issues.chromium.org/issues/427741151
- https://chromestatus.com/feature/5154752085884928
- https://www.w3.org/TR/css-view-transitions-2

### View transition pseudos inherit animation-delay.

#### What's New
Adds inheritance of `animation-delay` through the view transition pseudo tree.

#### Technical Details
Ensures the start offset of animations specified by `animation-delay` is preserved during view transitions.

#### Use Cases
Coordinating delays between element animations and view-transition pseudo-elements for smooth staged transitions.

#### References
- https://chromestatus.com/feature/5424291457531904
- https://www.w3.org/TR/css-view-transitions-2

### Nested view transitions groups

#### What's New
View transitions can generate nested pseudo-element trees rather than a flat structure, enabling more faithful visual representation.

#### Technical Details
Nested pseudo trees allow per-element layering that supports clipping, nested 3D transforms, and correct application of effects (opacity, masking) within groups.

#### Use Cases
Complex interfaces using nested transforms or masks that need the view transition to respect element stacking and clipping semantics.

#### References
- https://issues.chromium.org/issues/399431227
- https://chromestatus.com/feature/5162799714795520
- https://www.w3.org/TR/css-view-transitions-2/#view-transition-group-prop

### Propagate viewport `overscroll-behavior` from root

#### What's New
`overscroll-behavior` for the viewport is propagated from the root (`<html>`) element instead of from `<body>`.

#### Technical Details
Aligns Chromium with CSSWG resolution that viewport properties should propagate from the root element, not body, affecting which element’s property affects viewport behavior.

#### Use Cases
Applications relying on overscroll handling (e.g., preventing pull-to-refresh or chaining) will configure behavior on the root element for consistent results.

#### References
- https://issues.chromium.org/issues/41453796
- https://chromestatus.com/feature/6210047134400512
- https://drafts.csswg.org/css-overscroll-behavior-1

### CSS `counter()` and `counters()` in alt text of `content` property

#### What's New
Allows `counter()` and `counters()` inside the alt text of `content`, improving generated content semantics.

#### Technical Details
Expands the allowed expressions for content-generation so counters contribute to the accessible alt text content defined via `content`.

#### Use Cases
Accessible lists, numbered captions, and generated labels where counters should be exposed to assistive technologies.

#### References
- https://issues.chromium.org/issues/417488055
- https://chromestatus.com/feature/5185442420621312
- https://drafts.csswg.org/css-content/#content-property

### CSS `scroll-target-group` property

#### What's New
Introduces the `scroll-target-group` property to mark elements as scroll marker group containers with values like `none` and `auto`.

#### Technical Details
Defines whether an element establishes a scroll marker group container, which affects how scroll snap markers and related behaviors are grouped.

#### Use Cases
Fine-grained control of scroll marker grouping for complex scroll layouts and snap behaviors across nested scroll containers.

#### References
- https://issues.chromium.org/issues/6607668
- https://chromestatus.com/feature/5189126177161216
- https://drafts.csswg.org/css-overflow-5/#scroll-target-group

### Support `font-variation-settings` descriptor in `@font-face` rule

#### What's New
Adds support for the string-based `font-variation-settings` descriptor inside `@font-face` declarations.

#### Technical Details
Enables specifying variable font axis defaults at the font-face level so font variation axes can be configured where the font is declared.

#### Use Cases
Embedded variable fonts that require default axis locations (weight/width/slant) to be defined in @font-face for consistent rendering across elements.

#### References
- https://issues.chromium.org/issues/40398871
- https://chromestatus.com/feature/5221379619946496
- https://www.w3.org/TR/css-fonts-4/#font-rend-desc

Saved to: digest_markdown/webplatform/CSS/chrome-140-stable-en.md
