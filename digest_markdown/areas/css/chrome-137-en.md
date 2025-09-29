---
layout: default
title: chrome-137-en
---

## Area Summary

Chrome 137 advances CSS expressivity, accessibility, SVG integration, and rendering precision. Key themes include conditional value support (if()), improved reading-flow and focus order controls, richer animation paths and view transitions, and higher-fidelity rendering via floating point canvas colors. These changes give developers clearer control over layout semantics, animations, and graphics fidelity while improving accessibility and OS integration (accent-color). Together they expand what can be expressed declaratively in CSS and reduce the need for JavaScript workarounds.

## Detailed Updates

The items below expand on the summary above, focusing on what shipped, how it works at a high level, and practical developer uses.

### CSS if() function

#### What's New
The CSS `if()` function provides a concise way to express conditional values. It accepts a series of condition-value pairs and returns the value associated with the first true condition.

#### Technical Details
The function evaluates condition-value pairs sequentially; if none evaluate true the behavior follows the specification. See the spec for formal syntax and evaluation rules.

#### Use Cases
Replace verbose calc- or custom-property-based conditionals and simplify responsive, state-dependent property values directly in CSS.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=346977961 (Tracking bug #346977961)  
- https://chromestatus.com/feature/5084924504915968 (ChromeStatus.com entry)  
- https://www.w3.org/TR/css-values-5/#if-function (Spec)

### CSS reading-flow, reading-order properties

#### What's New
`reading-flow` controls the order elements are exposed to accessibility tools and tab navigation; `reading-order` allows manual overrides within a reading flow container.

#### Technical Details
These properties affect the logical sequential exposure of elements for focus and assistive technologies in flex, grid, or block layouts per the drafts.

#### Use Cases
Improve keyboard navigation, accessibility semantics, and control over sequential focus in complex layouts without DOM reordering.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40932006 (Tracking bug #40932006)  
- https://chromestatus.com/feature/5061928169472000 (ChromeStatus.com entry)  
- https://drafts.csswg.org/css-display-4/#reading-flow (Spec)  
- https://developer.chrome.com/blog/reading-flow (Use CSS reading-flow for logical sequential focus navigation)

### Ignore letter spacing in cursive scripts

#### What's New
Letter-spacing can be ignored for cursive scripts to avoid disrupting word structure, aligning behavior with the specification and improving readability for cursive-script users.

#### Technical Details
The implementation conditionally disregards the `letter-spacing` setting for cursive scripts as specified in the CSS Text spec.

#### Use Cases
Typography-sensitive interfaces and internationalized text rendering where letter-spacing should not break cursive script legibility.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40618336 (Tracking bug #40618336)  
- https://chromestatus.com/feature/5088256061988864 (ChromeStatus.com entry)  
- https://www.w3.org/TR/css-text-3/#letter-spacing-property (Spec)

### Selection API getComposedRanges and direction

#### What's New
Adds `Selection.direction` (returns `none`, `forward`, or `backward`) and `Selection.getComposedRanges()` (returns 0 or 1 composed StaticRange).

#### Technical Details
`getComposedRanges()` yields a composed StaticRange that may cross shadow DOM or other boundaries as permitted by the Selection spec; `direction` exposes selection traversal direction.

#### Use Cases
Improved programmatic selection handling for editors, rich text controls, and complex DOM (including shadow DOM) scenarios where selection direction and composed ranges matter.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40286116 (Tracking bug #40286116)  
- https://chromestatus.com/feature/5069063455711232 (ChromeStatus.com entry)  
- https://w3c.github.io/selection-api/#dom-selection-getcomposedranges (Spec)

### Support offset-path: shape()

#### What's New
Support for `offset-path: shape()` enables using responsive shapes to define animation motion paths.

#### Technical Details
`shape()` allows specifying a CSS shape as an offset path so animated elements can follow declarative, responsive geometry.

#### Use Cases
Declarative motion along complex, responsive paths for UI animations, without relying on JavaScript-generated keyframes.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=389713717 (Tracking bug #389713717)  
- https://chromestatus.com/feature/5062848242884608 (ChromeStatus.com entry)  
- https://www.w3.org/TR/css-shapes-2/#shape-function (Spec)

### Support the transform attribute on SVGSVGElement

#### What's New
Enables applying transformation properties (scale, rotate, translate, skew) directly to the `<svg>` root element via its `transform` attribute.

#### Technical Details
Applying `transform` to the SVG root affects the entire SVG coordinate system or its contents, aligning SVG root transformability with the SVG2 spec.

#### Use Cases
Global transformations of SVG documents without wrapping content, simplifying animations and coordinate-space adjustments.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40313130 (Tracking bug #40313130)  
- https://chromestatus.com/feature/5070863647424512 (ChromeStatus.com entry)  
- https://www.w3.org/TR/SVG2/types.html#InterfaceSVGTransformable (Spec)

### System accent color for accent-color property

#### What's New
`accent-color` can use the operating system's accent color so form elements adopt the user's OS-defined accent automatically.

#### Technical Details
Form controls such as checkboxes, radios, and progress bars will reflect the system accent color when `accent-color` is set to use it, per the CSS UI spec.

#### Use Cases
Native-integrated theming of form controls to match user preferences and OS-level theming, improving visual consistency.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40764875 (Tracking bug #40764875)  
- https://chromestatus.com/feature/5088516877221888 (ChromeStatus.com entry)  
- https://www.w3.org/TR/css-ui-4/#accent-color (Spec)

### Allow <use> to reference an external document's root element by omitting the fragment

#### What's New
Loosens `<use>` referencing so omitting a fragment can reference an external document's root element, simplifying external SVG reuse.

#### Technical Details
Previously a fragment ID was required; this change allows `<use>` to resolve to the external document root when no fragment is provided, per the SVG struct spec.

#### Use Cases
Easier inclusion and reuse of external SVG documents’ root content via `<use>` without needing fragment identifiers.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40362369 (Tracking bug #40362369)  
- https://chromestatus.com/feature/5078775255900160 (ChromeStatus.com entry)  
- https://www.w3.org/TR/SVG2/struct.html#UseElement (Spec)

### Canvas floating point color types

#### What's New
Introduces floating point pixel formats for `CanvasRenderingContext2D`, `OffscreenCanvasRenderingContext2D`, and `ImageData` to enable higher precision and HDR workflows.

#### Technical Details
Allows float-based pixel formats instead of 8-bit fixed point, supporting high dynamic range and high-precision rendering scenarios as described in the canvas spec.

#### Use Cases
Medical visualization, HDR imaging, scientific visualizations, and any application requiring greater color precision than 8-bit.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40245602 (Tracking bug #40245602)  
- https://chromestatus.com/feature/5053734768197632 (ChromeStatus.com entry)  
- https://html.spec.whatwg.org/multipage/canvas.html#the-2d-rendering-context (Spec)

### view-transition-name: match-element

#### What's New
The `match-element` value generates a unique ID based on an element's identity and renames it for use in view transitions, aiding animations when elements move in single-page apps.

#### Technical Details
`match-element` produces a consistent identifier for an element so it can be matched across view transitions even as the element moves within the app, following the view transitions draft.

#### Use Cases
Smooth element-preserving animations in SPAs where DOM reparenting or reordering occurs, enabling coherent view transitions without manual ID management.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=365997248 (Tracking bug #365997248)  
- https://chromestatus.com/feature/5092488609931264 (ChromeStatus.com entry)  
- https://drafts.csswg.org/css-view-transitions-2/#view-transition-name-prop (Spec)

Saved to: digest_markdown/webplatform/CSS/chrome-137-stable-en.md
