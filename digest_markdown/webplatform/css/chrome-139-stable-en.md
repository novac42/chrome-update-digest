digest_markdown/webplatform/css/chrome-139-stable-en.md
```markdown
# Chrome 139 Stable - CSS Update Digest

## 1. Executive Summary

Chrome 139 introduces several significant CSS enhancements, including custom functions, advanced corner shaping, improved font feature support, and updates to font property handling. These changes align Chrome more closely with evolving CSS specifications, enhance design flexibility, and improve interoperability with other browsers. Developers gain new expressive tools for layout, typography, and animation, while some legacy behaviors are deprecated for standards compliance.

## 2. Key Implications

### Technical Impact

- **Existing Implementations**: Minor adjustments may be required for font property usage and transition behaviors. Legacy reliance on `font-stretch` should be reviewed.
- **New Capabilities**: Custom CSS functions, superellipse/squircle corners, and async SVG scripting expand design and performance options.
- **Technical Debt**: Deprecated or legacy features (e.g., `font-stretch` aliasing) should be refactored to avoid future compatibility issues.

## 3. Risk Assessment

**Critical Risks**:
- No major breaking changes identified, but improper migration from `font-stretch` to `font-width` could cause rendering inconsistencies.
- Security: No direct CSS-related security concerns in this release.

**Medium Risks**:
- Deprecation of legacy font property aliases may impact older codebases.
- Performance: Async SVG scripting and scroll anchoring algorithm changes may affect rendering performance in edge cases.

## 4. Recommended Actions

### Immediate Actions

- Audit usage of `font-stretch` and migrate to `font-width` where appropriate.
- Test custom functions and corner shaping features in staging environments.
- Review transition behaviors for animations relying on property changes.

### Short-term Planning

- Update design systems to leverage new corner shaping and font feature settings.
- Refactor SVG scripts to utilize the async attribute for improved performance.
- Monitor scroll anchoring behavior in complex layouts.

### Long-term Strategy

- Align all font property usage with current specifications.
- Incorporate custom functions into reusable CSS frameworks.
- Stay updated on further CSS mixins and border enhancements.

## 5. Feature Analysis

### Short-circuiting `var()` and `attr()`

**Impact Level**: 🟡 Important

**What Changed**:
`var()` and `attr()` functions now evaluate without searching for cycles in their fallback when the fallback is not taken.

**Why It Matters**:
Improves performance and predictability in CSS variable resolution, reducing unnecessary computation.

**Implementation Guidance**:
- Refactor complex variable chains to leverage this optimization.
- Test for edge cases where fallback cycles may have previously caused issues.

**References**:
- [ChromeStatus.com entry](https://chromestatus.com/feature/6212939656462336)

---

### Support `font-feature-settings` descriptor in `@font-face` rule

**Impact Level**: 🟡 Important

**What Changed**:
String-based syntax for `font-feature-settings` is now supported in `@font-face` rules, per CSS Fonts Level 4. Invalid tags are ignored; only standard forms are accepted.

**Why It Matters**:
Enables fine-grained typographic control and better OpenType feature support, aligning with modern font usage.

**Implementation Guidance**:
- Use string-based `font-feature-settings` in font definitions.
- Validate feature tags to ensure compatibility.

**References**:
- [Tracking bug #40398871](https://issues.chromium.org/issues/40398871)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5102801981800448)
- [Spec](https://www.w3.org/TR/css-fonts-4/#font-rend-desc)

---

### CSS custom functions

**Impact Level**: 🔴 Critical

**What Changed**:
Custom functions allow dynamic value computation in CSS, using parameters, custom properties, and conditionals.

**Why It Matters**:
Greatly increases CSS expressiveness and reusability, enabling advanced design patterns and logic directly in stylesheets.

**Implementation Guidance**:
- Experiment with custom functions for theme and layout logic.
- Ensure fallback strategies for browsers without support.

**References**:
- [Tracking bug #325504770](https://issues.chromium.org/issues/325504770)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5179721933651968)
- [Spec](https://drafts.csswg.org/css-mixins-1/#defining-custom-functions)

---

### Continue running transitions when switching to initial transition value

**Impact Level**: 🟡 Important

**What Changed**:
Transition property changes only affect new transitions; existing animations continue unaffected unless their animated properties change.

**Why It Matters**:
Improves animation consistency and aligns with CSS Transitions specification.

**Implementation Guidance**:
- Review animation logic to ensure expected behavior when transition properties are updated.
- Test for unintended animation persistence.

**References**:
- [ChromeStatus.com entry](https://chromestatus.com/feature/5194501932711936)
- [Spec](https://www.w3.org/TR/css-transitions-1/#starting)

---

### Corner shaping (`corner-shape`, `superellipse`, `squircle`)

**Impact Level**: 🟡 Important

**What Changed**:
New properties enable advanced corner shapes (superellipse, squircle, etc.) beyond standard `border-radius`.

**Why It Matters**:
Expands design possibilities for UI elements, supporting modern aesthetics and smooth shape transitions.

**Implementation Guidance**:
- Update component libraries to support new corner shapes.
- Animate between corner shapes for enhanced UI effects.

**References**:
- [Tracking bug #393145930](https://issues.chromium.org/issues/393145930)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5357329815699456)
- [Spec](https://drafts.csswg.org/css-borders-4/#corner-shaping)

---

### Add `font-width` property and descriptor and make `font-stretch` a legacy alias

**Impact Level**: 🟡 Important

**What Changed**:
Chrome now recognizes `font-width` as per spec; `font-stretch` is deprecated as a legacy alias.

**Why It Matters**:
Improves standards compliance and interoperability with other browsers.

**Implementation Guidance**:
- Replace `font-stretch` with `font-width` in all stylesheets.
- Test font rendering for consistency across browsers.

**References**:
- [Tracking bug #356670472](https://issues.chromium.org/issues/356670472)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5190141555245056)

---

### Support async attribute for SVG `<script>` element

**Impact Level**: 🟢 Nice-to-have

**What Changed**:
SVG `<script>` elements now support the async attribute, allowing asynchronous script execution.

**Why It Matters**:
Improves SVG performance and responsiveness, especially for interactive graphics.

**Implementation Guidance**:
- Use async attribute for non-blocking SVG scripts.
- Test for compatibility with existing SVG workflows.

**References**:
- [Tracking bug #40067618](https://issues.chromium.org/issues/40067618)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6114615389585408)
- [Spec](https://svgwg.org/svg2-draft/interact.html#ScriptElement:~:text=%E2%80%98script%E2%80%99%20element-,SVG%202%20Requirement%3A,Consider%20allowing%20async/defer%20on%20%E2%80%98script%E2%80%99.,-Resolution%3A)

---

### The `request-close` invoker command

**Impact Level**: 🟢 Nice-to-have

**What Changed**:
Dialogs can now be closed via a `requestClose()` JavaScript function, firing a cancel event for developer control.

**Why It Matters**:
Enhances dialog management and user experience by allowing more granular control over dialog closure.

**Implementation Guidance**:
- Use `requestClose()` for custom dialog workflows.
- Handle cancel events to prevent unwanted closures.

**References**:
- [Tracking bug #400647849](https://issues.chromium.org/issues/400647849)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5592399713402880)
- [Spec](https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-command-request-close-state)

---

### Scroll anchoring priority candidate fix

**Impact Level**: 🟡 Important

**What Changed**:
Scroll anchoring algorithm now selects the deepest onscreen element as anchor, improving scroll stability.

**Why It Matters**:
Reduces unexpected scroll jumps during dynamic content changes, enhancing user experience.

**Implementation Guidance**:
- Test scroll behavior in dynamic layouts.
- Adjust anchor candidates if custom scroll logic is used.

**References**:
- [ChromeStatus.com entry](https://chromestatus.com/feature/5070370113323008)
```
