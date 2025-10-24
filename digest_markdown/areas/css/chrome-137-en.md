---
layout: default
title: chrome-137-en
---

## Area Summary

Chrome 137 advances CSS expressiveness, accessibility, and interoperability across layout, SVG, and UI controls. Key themes include conditional value expressions (if()), improved reading and focus order control, enhanced SVG/CSS integration (transform on <svg>, <use> referencing), and animation/path refinements (offset-path: shape(), view-transition matching). These updates give developers more declarative control for animations, responsive layouts, and platform-consistent UI styling, improving authoring ergonomics and accessibility. They matter because they reduce JS workarounds, enable richer native animations, and align browser behavior with evolving specs.

## Detailed Updates

The following entries expand on the summary above with concise technical and practical guidance for developers.

### CSS if() function

#### What's New
A new CSS function that evaluates condition–value pairs and returns the value for the first true condition, enabling concise conditional expressions in pure CSS.

#### Technical Details
Accepts a series of condition/value pairs delimited by semicolons and evaluates sequentially per the CSS Values 5 spec.

#### Use Cases
Replace JS or custom property hacks for simple conditional value selection (e.g., fallback sizes, theme-based values) directly in CSS.

#### References
- Tracking bug #346977961: https://bugs.chromium.org/p/chromium/issues/detail?id=346977961
- ChromeStatus.com entry: https://chromestatus.com/feature/5084924504915968
- Spec: https://www.w3.org/TR/css-values-5/#if-function

### CSS reading-flow, reading-order properties

#### What's New
Properties to control the order elements are exposed to assistive tech and sequential keyboard navigation inside a reading flow container.

#### Technical Details
Introduces a reading-flow container concept plus reading-order to let authors override logical exposure order in flex, grid, and block layouts per the Display 4 draft.

#### Use Cases
Improve accessibility and keyboard navigation in complex layouts (responsive reflows, multi-column content) without DOM reordering.

#### References
- Tracking bug #40932006: https://bugs.chromium.org/p/chromium/issues/detail?id=40932006
- ChromeStatus.com entry: https://chromestatus.com/feature/5061928169472000
- Spec: https://drafts.csswg.org/css-display-4/#reading-flow
- Use CSS reading-flow for logical sequential focus navigation: https://developer.chrome.com/blog/reading-flow

### Ignore letter spacing in cursive scripts

#### What's New
Letter-spacing can be ignored for cursive scripts as specified, avoiding disruption of word structure for those scripts.

#### Technical Details
Implements spec-guided logic to disregard letter-spacing for designated cursive script text rendering to yield correct word shaping.

#### Use Cases
Better typography for cursive/connected scripts, improving readability and native appearance for languages where inter-letter spacing breaks glyph joins.

#### References
- Tracking bug #40618336: https://bugs.chromium.org/p/chromium/issues/detail?id=40618336
- ChromeStatus.com entry: https://chromestatus.com/feature/5088256061988864
- Spec: https://www.w3.org/TR/css-text-3/#letter-spacing-property

### Selection API getComposedRanges and direction

#### What's New
Ships Selection.direction and Selection.getComposedRanges(), exposing selection direction and composed StaticRange(s) that may cross shadow/slot boundaries.

#### Technical Details
Selection.direction returns none|forward|backward. getComposedRanges() returns up to one composed StaticRange; composed ranges can cross tree boundaries per the selection API spec.

#### Use Cases
Accurate editor/annotation tooling, rich selection handling in web apps, and correct caret/selection behavior in shadow DOM contexts.

#### References
- Tracking bug #40286116: https://bugs.chromium.org/p/chromium/issues/detail?id=40286116
- ChromeStatus.com entry: https://chromestatus.com/feature/5069063455711232
- Spec: https://w3c.github.io/selection-api/#dom-selection-getcomposedranges

### Support offset-path: shape()

#### What's New
Adds support for offset-path: shape(), enabling responsive shapes as animation motion paths.

#### Technical Details
Implements the shape() function for offset-path per the CSS Shapes Level 2 specification to drive offset-position along custom shapes.

#### Use Cases
Create complex, responsive motion-path animations in CSS without SVG path fallbacks or JS calculations.

#### References
- Tracking bug #389713717: https://bugs.chromium.org/p/chromium/issues/detail?id=389713717
- ChromeStatus.com entry: https://chromestatus.com/feature/5062848242884608
- Spec: https://www.w3.org/TR/css-shapes-2/#shape-function

### Support the transform attribute on SVGSVGElement

#### What's New
Enables using the transform attribute on the <svg> root element to apply transforms to the entire SVG coordinate system and contents.

#### Technical Details
Adds support consistent with SVG2 transformable interfaces so the root <svg> can accept transformations like other SVG transformable elements.

#### Use Cases
Rotate/scale/translate entire SVG graphics declaratively, simplifying layout and animation scenarios that affect full SVG content.

#### References
- Tracking bug #40313130: https://bugs.chromium.org/p/chromium/issues/detail?id=40313130
- ChromeStatus.com entry: https://chromestatus.com/feature/5070863647424512
- Spec: https://www.w3.org/TR/SVG2/types.html#InterfaceSVGTransformable

### System accent color for accent-color property

#### What's New
accent-color can adopt the operating system's accent color, letting form controls match user theme preferences.

#### Technical Details
accent-color integrates with the OS accent color on supported platforms, applying it to controls like checkboxes, radios, and progress bars according to the CSS UI 4 spec.

#### Use Cases
Make UI controls feel native and consistent with user themes without platform-specific code or images.

#### References
- Tracking bug #40764875: https://bugs.chromium.org/p/chromium/issues/detail?id=40764875
- ChromeStatus.com entry: https://chromestatus.com/feature/5088516877221888
- Spec: https://www.w3.org/TR/css-ui-4/#accent-color

### Allow <use> to reference an external document's root element by omitting the fragment

#### What's New
Allows <use> referencing of an external SVG document’s root element when no fragment identifier is provided.

#### Technical Details
Loosens previous requirements so omitting a fragment can resolve to the external document root, aligning with the SVG2 structuring rules.

#### Use Cases
Simplifies reusing entire external SVG documents without requiring an explicit fragment ID, streamlining asset composition.

#### References
- Tracking bug #40362369: https://bugs.chromium.org/p/chromium/issues/detail?id=40362369
- ChromeStatus.com entry: https://chromestatus.com/feature/5078775255900160
- Spec: https://www.w3.org/TR/SVG2/struct.html#UseElement

### Canvas floating point color types

#### What's New
Introduces floating point pixel formats for CanvasRenderingContext2D, OffscreenCanvasRenderingContext2D, and ImageData for higher precision rendering.

#### Technical Details
Supports floating point pixel buffers instead of 8-bit fixed formats to enable HDR and high-precision workflows per the HTML Canvas spec.

#### Use Cases
Medical visualization, HDR imaging, scientific visualization, and any use case needing high dynamic range or precision beyond 8-bit channels.

#### References
- Tracking bug #40245602: https://bugs.chromium.org/p/chromium/issues/detail?id=40245602
- ChromeStatus.com entry: https://chromestatus.com/feature/5053734768197632
- Spec: https://html.spec.whatwg.org/multipage/canvas.html#the-2d-rendering-context

### view-transition-name: match-element

#### What's New
The match-element value generates a unique ID for an element based on identity, supporting view transitions when elements move between positions in SPAs.

#### Technical Details
Generates and assigns unique match IDs for elements to be used by view transitions, aiding in element matching even when DOM positions change, per the View Transitions Level 2 draft.

#### Use Cases
Smoothly animate elements that are relocated in the DOM during client-side navigation (SPAs) without manual ID management.

#### References
- Tracking bug #365997248: https://bugs.chromium.org/p/chromium/issues/detail?id=365997248
- ChromeStatus.com entry: https://chromestatus.com/feature/5092488609931264
- Spec: https://drafts.csswg.org/css-view-transitions-2/#view-transition-name-prop

Save as: digest_markdown/webplatform/CSS/chrome-137-stable-en.md
