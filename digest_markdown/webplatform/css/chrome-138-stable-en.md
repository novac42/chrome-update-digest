## Area Summary

Chrome 138 advances CSS expressiveness with new math and environment features, layout keywords, and sibling-aware functions. Key changes let authors compute values (abs(), sign(), progress()), query sibling position/count, and size elements to exactly fill available space via the stretch keyword, while exposing OS font scaling to CSS for better accessibility. These features reduce reliance on JavaScript for dynamic styling, enable finer control of layout and typography, and improve responsiveness and accessibility. Developers should evaluate where declarative CSS can replace script-driven logic and adjust responsive and accessibility testing to account for OS font scaling.

## Detailed Updates

The following entries expand on the summary above, describing what changed, how it works, practical uses, and links to the tracked issues and specs.

### CSS Sign-Related Functions: abs(), sign()

#### What's New
The sign-related functions `abs()` and `sign()` compute values related to the sign of their argument; `abs(A)` returns the absolute value of A preserving input type.

#### Technical Details
These are math functions added to CSS value handling, defined in CSS Values Level 4. They operate on numeric inputs and return numeric outputs usable inside other value expressions.

#### Use Cases
Use in calc() and other computed-value contexts to normalize values, create symmetric behaviors for animations, or derive conditional styling without JS.

#### References
- MDN Docs:abs() - https://developer.mozilla.org/docs/Web/CSS/abs
- Tracking bug #40253181 - https://bugs.chromium.org/p/chromium/issues/detail?id=40253181
- ChromeStatus.com entry - https://chromestatus.com/feature/5196860094464000
- Spec - https://www.w3.org/TR/css-values-4/#sign-funcs

### Interpolation progress functional notation: CSS progress() function

#### What's New
The `progress()` functional notation returns a `<number>` representing the position of one calculation between a start and end value, enabling interpolation math in CSS.

#### Technical Details
Defined as a math function in CSS Values Level 5, `progress()` computes a normalized progress value between two other calculations and can be embedded in value expressions to drive interpolations.

#### Use Cases
Drive timeline-like interpolations for animations, transition curves, or parameterized styles without external timing code; useful for declarative motion and responsive interpolation.

#### References
- Tracking bug #40944203 - https://bugs.chromium.org/p/chromium/issues/detail?id=40944203
- ChromeStatus.com entry - https://chromestatus.com/feature/5096136905244672
- Spec - https://www.w3.org/TR/css-values-5/#progress-notation

### CSS sibling-index() and sibling-count()

#### What's New
`sibling-index()` and `sibling-count()` return integer values representing an element's position among siblings and the total sibling count, usable directly in CSS property values and in calc().

#### Technical Details
These functions are part of CSS Values Level 5 and provide integer outputs that can be composed into property values, enabling position-aware styles without DOM scripting.

#### Use Cases
Style list items, grid children, or dynamically generated content based on position (e.g., nth-based sizing, staggered animations, or position-driven colors) without adding classes or JS.

#### References
- Tracking bug #40282719 - https://bugs.chromium.org/p/chromium/issues/detail?id=40282719
- ChromeStatus.com entry - https://chromestatus.com/feature/5649901281918976
- Spec - https://www.w3.org/TR/css-values-5/#sibling-functions

### CSS stretch sizing keyword

#### What's New
A sizing keyword that lets properties like `width` and `height` grow to exactly fill the containing block's available space, applied to the element's margin box (unlike percentage sizing tied to box-sizing).

#### Technical Details
Defined in CSS Sizing Level 4, `stretch` computes to fill the available space of the containing block’s margin box, giving a deterministic fill behavior distinct from percentage-based sizing.

#### Use Cases
Use for full-bleed UI elements, layouts that must precisely fill containers including margins, and simplifying responsive sizing without complex calc() expressions.

#### References
- Tracking bug #41253915 - https://bugs.chromium.org/p/chromium/issues/detail?id=41253915
- ChromeStatus.com entry - https://chromestatus.com/feature/5102457485459456
- Spec - https://www.w3.org/TR/css-sizing-4/#valdef-width-stretch

### CSS env variable for OS-level font scale

#### What's New
Exposes the user's preferred OS-level font scale to CSS via an environment variable, allowing pages to detect and adapt to the user's system font-scale preference.

#### Technical Details
Specified in the CSS Environment Variables Module, this env() variable reflects the OS-chosen font scale and can be read in CSS to adjust typographic sizes or layout decisions.

#### Use Cases
Improve accessibility and consistency with user preferences by scaling typographic systems, adjusting line-height and spacing based on system font scale, and avoiding layout breakage when users change OS font settings.

#### References
- Tracking bug #397737223 - https://bugs.chromium.org/p/chromium/issues/detail?id=397737223
- ChromeStatus.com entry - https://chromestatus.com/feature/5106542883938304
- Spec - https://www.w3.org/TR/css-env-1/#os-font-scale

Saved file path: digest_markdown/webplatform/CSS/chrome-138-stable-en.md