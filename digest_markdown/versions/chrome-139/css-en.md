---
layout: default
title: css-en
---

## Area Summary

Chrome 139 continues to advance CSS by adding expressive shape controls, improved font handling, and more robust value evaluation semantics. Key developer-facing changes include corner shaping (superellipse/squircle), CSS custom functions, and improved font descriptors (font-width and @font-face font-feature-settings). These updates make visual design and typography more predictable and powerful, while smaller fixes (var()/attr() short-circuiting, transition continuation, scroll anchoring) reduce edge-case glitches. Together, they push the platform toward richer, animation-friendly, and spec-compliant styling primitives.

## Detailed Updates

The list below expands on the summary above with concise, developer-focused notes for each CSS-area feature in Chrome 139.

### Short-circuiting `var()` and `attr()`

#### What's New
When a fallback is not taken, `var()` and `attr()` evaluate without scanning for cycles in that fallback.

#### Technical Details
Evaluation short-circuits earlier, avoiding unnecessary cycle detection when a fallback is used directly.

#### Use Cases
Reduces surprising cycle errors and improves reliability of custom property and attribute-based values.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/6212939656462336

### Support `font-feature-settings` descriptor in `@font-face` rule

#### What's New
Adds support for the string-based `font-feature-settings` descriptor inside `@font-face` per CSS Fonts Level 4.

#### Technical Details
String syntax is accepted; invalid/unrecognized OpenType feature tags are ignored as specified. Non-standard or binary forms are not supported.

#### Use Cases
Allows font authors and developers to declare OpenType feature preferences at font-face load time, improving typography control.

#### References
- Tracking bug #40398871: https://issues.chromium.org/issues/40398871
- ChromeStatus.com entry: https://chromestatus.com/feature/5102801981800448
- Spec: https://www.w3.org/TR/css-fonts-4/#font-rend-desc

### CSS custom functions

#### What's New
Introduces custom functions that compute values from custom properties, parameters, and conditionals (mixin-like behavior).

#### Technical Details
Custom functions follow the drafts for CSS mixins/custom functions and are tracked in Chromium.

#### Use Cases
Enable reusable, parameterized style logic for complex theming and component libraries without JS.

#### References
- Tracking bug #325504770: https://issues.chromium.org/issues/325504770
- ChromeStatus.com entry: https://chromestatus.com/feature/5179721933651968
- Spec: https://drafts.csswg.org/css-mixins-1/#defining-custom-functions

### Continue running transitions when switching to initial transition value

#### What's New
Active transitions continue with their previous animation state even if transition-* properties change to their initial values.

#### Technical Details
Transition property changes only affect newly started transitions; existing active transitions persist with earlier parameters per spec.

#### Use Cases
Avoids abrupt animation interruptions when toggling transition definitions, improving animation stability during dynamic style changes.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5194501932711936
- Spec: https://www.w3.org/TR/css-transitions-1/#starting

### Corner shaping (`corner-shape`, `superellipse`, `squircle`)

#### What's New
Adds corner-shaping primitives that express corner curvature as superellipses, enabling squircles, notches, scoops, and animated corner morphs.

#### Technical Details
New properties accept shape descriptions (superellipse parameters) and integrate with existing border/corner model to render non-circular corners.

#### Use Cases
Creates smoother, design-driven corners and enables animated transitions between corner shapes without complex SVG or mask workarounds.

#### References
- Tracking bug #393145930: https://issues.chromium.org/issues/393145930
- ChromeStatus.com entry: https://chromestatus.com/feature/5357329815699456
- Spec: https://drafts.csswg.org/css-borders-4/#corner-shaping

### Add `font-width` property and descriptor and make `font-stretch` a legacy alias

#### What's New
Chrome recognizes `font-width` as the standard property/descriptor; `font-stretch` is now a legacy alias.

#### Technical Details
Aligns Chrome with the spec and other browsers by promoting `font-width` for width/condensed/expanded font axes.

#### Use Cases
Use `font-width` in CSS and @font-face to target variable-font width axes, improving cross-browser typography consistency.

#### References
- Tracking bug #356670472: https://issues.chromium.org/issues/356670472
- ChromeStatus.com entry: https://chromestatus.com/feature/5190141555245056

### Support async attribute for SVG `<script>` element

#### What's New
Implements the async attribute on SVG script elements (SVGScriptElement), matching HTMLScriptElement behavior.

#### Technical Details
Scripts in SVG can be executed asynchronously, per SVG 2.0 interface definitions.

#### Use Cases
Improves performance and responsiveness for SVGs that include external or inline script by allowing asynchronous execution.

#### References
- Tracking bug #40067618: https://issues.chromium.org/issues/40067618
- ChromeStatus.com entry: https://chromestatus.com/feature/6114615389585408
- Spec: https://svgwg.org/svg2-draft/interact.html#ScriptElement:~:text=%E2%80%98script%E2%80%99%20element-,SVG%202%20Requirement%3A,Consider%20allowing%20async/defer%20on%20%E2%80%98script%E2%80%99.,-Resolution%3A

### The `request-close` invoker command

#### What's New
Adds the `requestClose()` invoker command behavior to dialog handling so cancel events can be fired and intercepted consistently.

#### Technical Details
Dialogs now map programmatic close requests to the same cancel/close request paths as user actions, enabling prevention via event handlers.

#### Use Cases
Allows developers to intercept and prevent dialog closure consistently across input and programmatic scenarios.

#### References
- Tracking bug #400647849: https://issues.chromium.org/issues/400647849
- ChromeStatus.com entry: https://chromestatus.com/feature/5592399713402880
- Spec: https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-command-request-close-state

### Scroll anchoring priority candidate fix

#### What's New
Modifies scroll anchoring: the priority candidate is used as the scope/root for the regular anchor selection algorithm rather than automatically becoming the anchor.

#### Technical Details
The algorithm now selects the deepest onscreen element within that scope as the anchor, changing anchor selection behavior.

#### Use Cases
Reduces incorrect jumps and improves layout stability during incremental content changes and images loading.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5070370113323008

Saved file path:
digest_markdown/webplatform/CSS/chrome-139-stable-en.md
