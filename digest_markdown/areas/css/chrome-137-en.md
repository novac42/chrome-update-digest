---
layout: default
title: chrome-137-en
---

## Detailed Updates

Below are the Chrome 137 CSS-area updates that expand expressiveness, accessibility, and rendering capabilities for web developers.

### CSS if() function

#### What's New
The CSS if() function provides a concise way to express conditional values. It accepts a series of condition-value pairs, delimited by semicolons, and returns the value for the first true condition.

#### Technical Details
Evaluates condition-value pairs sequentially and yields the value associated with the first condition that evaluates to true. Specification reference is provided.

#### Use Cases
Simplifies conditional styling in stylesheets without needing custom properties or JS fallbacks — useful for responsive or state-dependent values.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=346977961
- https://chromestatus.com/feature/5084924504915968
- https://www.w3.org/TR/css-values-5/#if-function

### CSS reading-flow, reading-order properties

#### What's New
`reading-flow` controls the order elements are exposed to accessibility tools and tab keyboard focus navigation; `reading-order` lets authors override order within a reading-flow container.

#### Technical Details
These properties affect the logical sequence used by assistive technologies and keyboard navigation in flex, grid, or block layouts, enabling authors to define or override sequential reading/focus order.

#### Use Cases
Improves keyboard and screen-reader navigation for complex layouts (e.g., grid/flex UIs), letting authors ensure logical focus/reading order without changing DOM order.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40932006
- https://chromestatus.com/feature/5061928169472000
- https://drafts.csswg.org/css-display-4/#reading-flow
- https://developer.chrome.com/blog/reading-flow

### Ignore letter spacing in cursive scripts

#### What's New
Adds behavior to ignore the letter-spacing setting for cursive scripts as specified, to avoid disrupting word structure in those scripts.

#### Technical Details
Implements logic aligned with the CSS Text spec so that letter-spacing can be ignored for cursive scripts where spacing would harm legibility and word structure.

#### Use Cases
Improves typographic rendering and readability for cursive-script languages when authors set letter-spacing globally.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40618336
- https://chromestatus.com/feature/5088256061988864
- https://www.w3.org/TR/css-text-3/#letter-spacing-property

### Selection API getComposedRanges and direction

#### What's New
Ships two Selection API additions: `Selection.direction` (returns `none`, `forward`, or `backward`) and `Selection.getComposedRanges()` (returns a list of 0 or 1 composed StaticRange).

#### Technical Details
`Selection.direction` exposes the selection's logical direction. `getComposedRanges()` provides composed StaticRange results usable by authors interacting with selection programmatically; specification link included.

#### Use Cases
Enables richer editing and selection-aware features (custom editors, copy/paste handling, complex selection logic) with reliable selection direction and composed-range access.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40286116
- https://chromestatus.com/feature/5069063455711232
- https://w3c.github.io/selection-api/#dom-selection-getcomposedranges

### Support offset-path: shape()

#### What's New
Supports `offset-path: shape()` to allow using responsive shapes to define animation paths.

#### Technical Details
Implements the shape() function for offset-path so motion-offset/offset-path animations can follow responsive shape-defined paths; spec and tracking links provided.

#### Use Cases
Creates adaptable motion paths for animated elements (e.g., responsive UI animations that follow a shape defined in CSS).

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=389713717
- https://chromestatus.com/feature/5062848242884608
- https://www.w3.org/TR/css-shapes-2/#shape-function

### Support the transform attribute on SVGSVGElement

#### What's New
Enables application of transform properties directly to the `<svg>` root element using its transform attribute.

#### Technical Details
Adds support for the transform attribute on SVGSVGElement so the root `<svg>` can be transformed (scale, rotate, translate, skew) as a whole according to the SVG spec.

#### Use Cases
Simplifies global SVG coordinate system adjustments and whole-SVG transformations without wrapping or additional containers.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40313130
- https://chromestatus.com/feature/5070863647424512
- https://www.w3.org/TR/SVG2/types.html#InterfaceSVGTransformable

### System accent color for accent-color property

#### What's New
Allows authors to use the operating system's accent color via the `accent-color` CSS property so form controls adopt the user's OS accent.

#### Technical Details
`accent-color` can reflect the OS-defined accent, enabling native-looking form elements (checkboxes, radios, progress bars) without manual theming.

#### Use Cases
Keeps form controls visually consistent with platform theming and user preferences, improving perceived integration and UX.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40764875
- https://chromestatus.com/feature/5088516877221888
- https://www.w3.org/TR/css-ui-4/#accent-color

### Allow <use> to reference an external document's root element by omitting the fragment

#### What's New
Loosens `<use>` referencing so omitting the fragment in an external reference resolves to the external document's root element.

#### Technical Details
Previously, external `<use>` required an explicit fragment; Chrome 137 treats an omitted fragment as referencing the external document root when resolving `<use>` targets.

#### Use Cases
Simplifies reusing entire external SVG documents with `<use>` by allowing shorthand references to the root, reducing authoring complexity.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40362369
- https://chromestatus.com/feature/5078775255900160
- https://www.w3.org/TR/SVG2/struct.html#UseElement

### Canvas floating point color types

#### What's New
Introduces floating point pixel formats (instead of 8-bit fixed point) for CanvasRenderingContext2D, OffscreenCanvasRenderingContext2D, and ImageData.

#### Technical Details
Adds support for high-precision floating point color buffers for 2D canvas contexts and ImageData, enabling higher dynamic range and precision where needed.

#### Use Cases
Important for high-fidelity visualizations (medical imaging, scientific visualization), HDR content, and workloads requiring greater color precision than 8-bit channels.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40245602
- https://chromestatus.com/feature/5053734768197632
- https://html.spec.whatwg.org/multipage/canvas.html#the-2d-rendering-context

### view-transition-name: match-element

#### What's New
The `match-element` value for `view-transition-name` generates a unique ID based on an element's identity and renames it for view transitions, aiding animations when elements move in SPAs.

#### Technical Details
`match-element` produces a stable, element-identity-based name used by the view transitions algorithm to match and animate elements that are moved within the document or across SPA navigations.

#### Use Cases
Facilitates smooth transitions for elements relocated by client-side routing or DOM reparenting without manual ID management.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=365997248
- https://chromestatus.com/feature/5092488609931264
- https://drafts.csswg.org/css-view-transitions-2/#view-transition-name-prop

File path for saved digest:
digest_markdown/webplatform/CSS/chrome-137-stable-en.md
