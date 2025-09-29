---
layout: default
title: css-en
---

### 1. Area Summary

Chrome 139's CSS-area updates focus on richer typographic control, more expressive corner shapes, improved animation and scroll stability, and new CSS-level primitives (custom functions, short-circuiting semantics). The most impactful changes for developers are the new font and corner-shaping features, deterministic transition behavior, and support for async SVG scripts—each reduces workarounds and improves rendering fidelity. Together these advances bring Chrome closer to modern CSS specifications (Fonts, Borders, Transitions, Mixins), enabling more predictable animations, finer typographic and UI design, and better performance for SVG-driven experiences. These updates matter because they reduce platform fragmentation and let authors implement advanced designs without polyfills or hacks.

## Detailed Updates

The list below expands on the summary with precise, developer-focused details for each CSS-area feature in Chrome 139.

### Short-circuiting `var()` and `attr()`

#### What's New
When a fallback value is not used, `var()` and `attr()` evaluate without searching for cycles in that fallback.

#### Technical Details
Evaluation short-circuits: if the primary value is taken, cycle detection does not traverse into the fallback expression. This aligns evaluation cost and cycle-detection scope with practical usage patterns.

#### Use Cases
Avoids false-positive cycle detection and reduces overhead when fallbacks are present but not taken; more predictable custom-property usage.

#### References
- https://chromestatus.com/feature/6212939656462336

### Support `font-feature-settings` descriptor in `@font-face` rule

#### What's New
Adds support for the string-based `font-feature-settings` descriptor inside `@font-face` as defined by CSS Fonts Level 4.

#### Technical Details
Chrome accepts string syntax, ignores invalid/unrecognized OpenType feature tags per spec, and does not implement binary/non-standard forms.

#### Use Cases
Allows font authors and developers to declare OpenType feature settings at font-face load time for precise typographic control without relying on runtime CSS hacks.

#### References
- https://issues.chromium.org/issues/40398871
- https://chromestatus.com/feature/5102801981800448
- https://www.w3.org/TR/css-fonts-4/#font-rend-desc

### CSS custom functions

#### What's New
Introduces custom functions: parameterized, conditional value generators akin to custom properties but capable of returning computed values.

#### Technical Details
Custom functions can depend on custom properties, accept parameters, and include conditionals as specified by the CSS Mixins/custom-functions draft. Implementation follows the referenced tracking and spec work.

#### Use Cases
Enables reusable, parameterized value composition for themes, design systems, and component libraries without JS-based value computation.

#### References
- https://issues.chromium.org/issues/325504770
- https://chromestatus.com/feature/5179721933651968
- https://drafts.csswg.org/css-mixins-1/#defining-custom-functions

### Continue running transitions when switching to initial transition value

#### What's New
Active transitions continue running with their prior parameters when transition-* properties change; transition property changes only affect newly started transitions.

#### Technical Details
Behavior aligns with the transitions spec: updates to transition-related properties do not implicitly restart or cancel in-flight transitions; they apply to future transitions only.

#### Use Cases
Produces stable, predictable animations when toggling transition declarations at runtime (reduces unintended restarts/jank).

#### References
- https://chromestatus.com/feature/5194501932711936
- https://www.w3.org/TR/css-transitions-1/#starting

### Corner shaping (`corner-shape`, `superellipse`, `squircle`)

#### What's New
Adds corner-shaping primitives (e.g., `corner-shape`, superellipse / squircle) to express corner curvature beyond `border-radius`.

#### Technical Details
Corners can be expressed as superellipse-based shapes and animated between different corner-shape values as defined by the Borders Level 4 draft.

#### Use Cases
Creates squircles, notches, scoops, and animatable corner geometry for modern UI design without SVG or layered masking hacks.

#### References
- https://issues.chromium.org/issues/393145930
- https://chromestatus.com/feature/5357329815699456
- https://drafts.csswg.org/css-borders-4/#corner-shaping

### Add `font-width` property and descriptor and make `font-stretch` a legacy alias

#### What's New
Chrome recognizes the `font-width` property and descriptor; `font-stretch` is treated as a legacy alias.

#### Technical Details
Aligns Chrome with the CSS Fonts specification and other browsers by mapping the standardized `font-width` to font matching and @font-face descriptors while retaining backward compatibility via the legacy alias.

#### Use Cases
Improves variable-font width selection and declarative width control in CSS, clarifying intent in font loading and matching.

#### References
- https://issues.chromium.org/issues/356670472
- https://chromestatus.com/feature/5190141555245056

### Support async attribute for SVG `<script>` element

#### What's New
Adds support for the `async` attribute on SVG `<script>` via the SVGScriptElement interface per SVG 2.0.

#### Technical Details
SVG scripts with `async` behave similarly to HTMLScriptElement `async`, allowing script execution without blocking parser/rendering.

#### Use Cases
Non-blocking SVG scripts for interactive graphics and icons embedded inline or via <object>/<embed>, improving load responsiveness.

#### References
- https://issues.chromium.org/issues/40067618
- https://chromestatus.com/feature/6114615389585408
- https://svgwg.org/svg2-draft/interact.html#ScriptElement:~:text=%E2%80%98script%E2%80%99%20element-,SVG%202%20Requirement%3A,Consider%20allowing%20async/defer%20on%20%E2%80%98script%E2%80%99.,-Resolution%3A

### The `request-close` invoker command

#### What's New
Introduces the `request-close` invoker semantics so programmatic close requests can be treated like user-initiated close requests that fire cancel events.

#### Technical Details
Programmatic invocations that request closure will dispatch the same cancel/close lifecycle events (so handlers can call preventDefault()), matching the form-elements spec behavior for request-close state.

#### Use Cases
Allows dialogs and custom UI to programmatically request closure while still giving pages the opportunity to intercept and prevent the close (confirmation flows, unsaved-work protection).

#### References
- https://issues.chromium.org/issues/400647849
- https://chromestatus.com/feature/5592399713402880
- https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-command-request-close-state

### Scroll anchoring priority candidate fix

#### What's New
Updates the scroll-anchoring algorithm: the priority candidate is now used as the scope/root for the standard anchor selection, rather than being directly selected as the anchor.

#### Technical Details
Selecting the candidate as the search scope allows the regular algorithm to pick the deepest onscreen element as the actual anchor, improving selection correctness when layout changes occur.

#### Use Cases
Reduces unexpected viewport jumps during dynamic content changes, making scroll anchoring more robust for SPA and content-insertion scenarios.

#### References
- https://chromestatus.com/feature/5070370113323008

Area-specific expertise mapping (developer impact)
- css / layout engines: corner-shaping, font-width, font-feature-settings, and custom functions enable richer, spec-aligned layout and rendering primitives.
- webapi / javascript: `request-close` and SVG `async` affect DOM scripting and lifecycle interactions.
- performance: async SVG scripts and short-circuiting `var()`/`attr()` reduce render-blocking and evaluation cost.
- security-privacy: `request-close` preserves cancel semantics so apps can enforce user-consent patterns; no new surface increases permissions.
- performance / rendering: transition continuation and scroll anchoring fixes improve smoothness and visual stability.
- deprecations: `font-stretch` treated as legacy alias; migrate to `font-width` per spec.

Saved to: digest_markdown/webplatform/CSS/chrome-139-stable-en.md
