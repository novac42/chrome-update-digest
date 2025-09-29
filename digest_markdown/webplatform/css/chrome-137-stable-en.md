## Area Summary

Chrome 137 introduces a set of CSS-focused improvements that emphasize conditional styling, accessibility-aware layout ordering, richer SVG/CSS integration, and animation/transition ergonomics. Standout changes for developers include the CSS if() function for inline conditional values, reading-flow/reading-order for logical focus and assistive-order control, and view-transition-name: match-element for SPA animation continuity. These features advance the platform by enabling more expressive, accessible, and animation-friendly CSS primitives without heavy JS workarounds. The updates reduce implementation friction for common UI patterns (accessibility, responsive animation paths, system theming) and improve interoperability with web platform specs.

## Detailed Updates

The following items expand on the summary above and provide practical and technical context for each CSS-area feature shipped in Chrome 137.

### CSS if() function

#### What's New
The CSS `if()` function provides a concise way to express conditional values using a series of condition-value pairs separated by semicolons. It evaluates conditions sequentially and returns the value associated with the first true condition.

#### Technical Details
Implements the spec-defined `if()` from the CSS Values Level 5 draft, handling condition/value pairs in CSS expressions.

#### Use Cases
Inline conditional styling without needing CSS custom properties + JS workarounds; useful for fallback styles, responsive variations, and simplifying complex calc/chaining scenarios.

#### References
- [Tracking bug #346977961](https://bugs.chromium.org/p/chromium/issues/detail?id=346977961)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5084924504915968)  
- [Spec](https://www.w3.org/TR/css-values-5/#if-function)

### CSS reading-flow, reading-order properties

#### What's New
Adds `reading-flow` to control the order elements are exposed to accessibility tools and tab focus, and `reading-order` to let authors override order inside a reading flow container.

#### Technical Details
Implements the reading-flow model from Display Level 4 drafts to influence logical sequence used by accessibility APIs and sequential focus navigation.

#### Use Cases
Control keyboard/tab order and assistive technology reading order for complex layouts (flex, grid, block) without rearranging DOM; improves accessibility for rotated, multi-column, or visual-only ordering.

#### References
- [Tracking bug #40932006](https://bugs.chromium.org/p/chromium/issues/detail?id=40932006)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5061928169472000)  
- [Spec](https://drafts.csswg.org/css-display-4/#reading-flow)  
- [Use CSS reading-flow for logical sequential focus navigation](https://developer.chrome.com/blog/reading-flow)

### Ignore letter spacing in cursive scripts

#### What's New
Adds behavior to ignore `letter-spacing` for cursive scripts when specified by the developer, aligning with the CSS Text spec to avoid disrupting word shape and readability.

#### Technical Details
Implements the text module guidance to selectively ignore letter-spacing for cursive/script fonts where spacing would harm script integrity.

#### Use Cases
Improves typography for cursive and script languages by preventing developer-applied letter-spacing from breaking glyph joining and word recognition; important for localization-sensitive UI.

#### References
- [Tracking bug #40618336](https://bugs.chromium.org/p/chromium/issues/detail?id=40618336)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088256061988864)  
- [Spec](https://www.w3.org/TR/css-text-3/#letter-spacing-property)

### Selection API getComposedRanges and direction

#### What's New
Ships two Selection API additions: `Selection.direction` (returns `none`, `forward`, or `backward`) and `Selection.getComposedRanges()` (returns 0 or 1 composed StaticRange, which may cross shadow boundaries).

#### Technical Details
Aligns Selection behavior with the Selection API draft to expose selection gravity and a composed range abstraction useful in shadow/slot contexts.

#### Use Cases
Improved programmatic handling of user text selection in rich components and shadow DOM, enabling accurate caret/selection logic for editors and accessibility tools.

#### References
- [Tracking bug #40286116](https://bugs.chromium.org/p/chromium/issues/detail?id=40286116)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5069063455711232)  
- [Spec](https://w3c.github.io/selection-api/#dom-selection-getcomposedranges)

### Support offset-path: shape()

#### What's New
Supports `offset-path: shape()` to allow animation motion paths driven by responsive shapes.

#### Technical Details
Implements the `shape()` function for `offset-path` as defined in CSS Motion Path / Shapes Level specs, enabling paths that adapt to layout.

#### Use Cases
Create motion-path animations that follow layout-aware shapes (e.g., bounding boxes or responsive shapes) without manual path recalculation.

#### References
- [Tracking bug #389713717](https://bugs.chromium.org/p/chromium/issues/detail?id=389713717)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5062848242884608)  
- [Spec](https://www.w3.org/TR/css-shapes-2/#shape-function)

### Support the transform attribute on SVGSVGElement

#### What's New
Enables the use of the `transform` attribute on the `<svg>` root element to apply transforms (scale, rotate, translate, skew) to the entire SVG coordinate system or its contents.

#### Technical Details
Implements SVG2 transformability for the root `<svg>` element, aligning behavior with the InterfaceSVGTransformable spec.

#### Use Cases
Simplifies global SVG transformations without extra wrapper elements; useful for scaling/rotating entire SVGs from CSS or attributes.

#### References
- [Tracking bug #40313130](https://bugs.chromium.org/p/chromium/issues/detail?id=40313130)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5070863647424512)  
- [Spec](https://www.w3.org/TR/SVG2/types.html#InterfaceSVGTransformable)

### System accent color for accent-color property

#### What's New
`accent-color` can now use the operating system's accent color so form controls (checkboxes, radios, progress bars) automatically adopt the user’s OS accent.

#### Technical Details
Brings `accent-color` behavior in line with CSS UI Level 4, mapping system accent tokens to form element rendering.

#### Use Cases
Ensure native-consistent theming for built-in controls, improving visual integration with platform UI and reducing custom styling needs.

#### References
- [Tracking bug #40764875](https://bugs.chromium.org/p/chromium/issues/detail?id=40764875)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088516877221888)  
- [Spec](https://www.w3.org/TR/css-ui-4/#accent-color)

### Allow <use> to reference an external document's root element by omitting the fragment

#### What's New
Loosens `<use>` referencing requirements so that omitting a fragment when referencing an external SVG document resolves to that document's root element.

#### Technical Details
Adjusts `<use>` resolution logic for cross-document references to accept external document root targets when no fragment is provided, per SVG2 struct rules.

#### Use Cases
Simplifies reuse of entire external SVG documents via `<use>` without requiring internal fragment IDs; improves SVG composition workflows.

#### References
- [Tracking bug #40362369](https://bugs.chromium.org/p/chromium/issues/detail?id=40362369)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5078775255900160)  
- [Spec](https://www.w3.org/TR/SVG2/struct.html#UseElement)

### Canvas floating point color types

#### What's New
Adds support for floating point pixel formats (instead of 8-bit) with Canvas 2D contexts and ImageData, enabling higher precision color representations.

#### Technical Details
Extends CanvasRenderingContext2D, OffscreenCanvasRenderingContext2D, and ImageData to support floating point color types per HTML Canvas spec extensions.

#### Use Cases
Necessary for high-dynamic-range or high-precision rendering scenarios (medical visualization, scientific imaging, HDR workflows) where 8-bit color quantization is insufficient.

#### References
- [Tracking bug #40245602](https://bugs.chromium.org/p/chromium/issues/detail?id=40245602)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5053734768197632)  
- [Spec](https://html.spec.whatwg.org/multipage/canvas.html#the-2d-rendering-context)

### view-transition-name: match-element

#### What's New
The `match-element` value for `view-transition-name` generates a unique ID based on an element’s identity, enabling consistent naming during view transitions for moved elements in SPAs.

#### Technical Details
Implements the view transitions naming mechanism from the View Transitions Level 2 draft to match elements that move in the DOM without requiring manual IDs.

#### Use Cases
Simplifies creating seamless transitions for elements that are moved or reparented during client-side navigation (common in SPA routing), improving animation continuity without DOM ID management.

#### References
- [Tracking bug #365997248](https://bugs.chromium.org/p/chromium/issues/detail?id=365997248)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5092488609931264)  
- [Spec](https://drafts.csswg.org/css-view-transitions-2/#view-transition-name-prop)