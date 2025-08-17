---
layout: default
title: Chrome 139 Stable – CSS Update Digest
---

Save to: `digest_markdown/webplatform/css/chrome-139-stable-en.md`

---

# Chrome 139 Stable – CSS Update Digest

## 1. Executive Summary

Chrome 139 introduces significant advancements in CSS, focusing on enhanced font feature support, new custom function capabilities, improved corner shaping, and better alignment with evolving specifications. Notable highlights include support for CSS custom functions, the `font-width` property, advanced corner shaping with `superellipse` and `squircle`, and optimizations in transition and scroll anchoring behaviors. These updates collectively empower developers with greater expressiveness, performance, and standards compliance in modern web design.

## 2. Key Implications

### Technical Impact

- **Existing Implementations**: Most changes are additive or standards-aligned, minimizing breakage but requiring awareness for property and descriptor updates (e.g., `font-width` vs. `font-stretch`).
- **New Capabilities**: Developers can now leverage custom CSS functions, advanced font features, and expressive corner shapes, enabling richer UI and typography.
- **Technical Debt**: Legacy usage of properties like `font-stretch` should be reviewed and updated to maintain forward compatibility.

## 3. Risk Assessment

**Critical Risks**:
- No explicit breaking changes or security issues identified in this release.

**Medium Risks**:
- **Deprecations**: `font-stretch` is now a legacy alias; continued reliance may lead to future compatibility issues.
- **Performance Impacts**: Introduction of async SVG scripts and new CSS functions may affect rendering or script execution timing if not managed carefully.

## 4. Recommended Actions

### Immediate Actions

- Audit codebases for usage of `font-stretch` and begin migration to `font-width`.
- Experiment with new corner shaping and custom function features in non-critical UI components.
- Review transition and scroll anchoring behaviors in complex layouts.

### Short-term Planning

- Update style guides and component libraries to incorporate new CSS features.
- Monitor browser compatibility tables for adoption of these features across other engines.
- Educate team members on the implications of custom functions and advanced font descriptors.

### Long-term Strategy

- Phase out legacy CSS patterns in favor of standards-aligned properties and descriptors.
- Plan for progressive enhancement strategies leveraging new CSS capabilities.
- Track ongoing CSS specification changes to anticipate future browser updates.

## 5. Feature Analysis

---

### Short-circuiting `var()` and `attr()`

**Impact Level**: 🟡 Important

**What Changed**:
When the fallback is not taken, `var()` and `attr()` functions now evaluate without searching for cycles in the fallback, improving efficiency and predictability.

**Why It Matters**:
This change optimizes CSS variable and attribute function evaluation, reducing unnecessary computation and potential for cyclic dependency issues.

**Implementation Guidance**:
- Refactor CSS to avoid unnecessary fallbacks in `var()` and `attr()` where possible.
- Test for any edge cases where fallback cycles may have previously masked issues.

**References**:
- [ChromeStatus.com entry](https://chromestatus.com/feature/6212939656462336)

---

### Support `font-feature-settings` descriptor in `@font-face` rule

**Impact Level**: 🟡 Important

**What Changed**:
Chrome now supports the string-based syntax for `font-feature-settings` in `@font-face`, per CSS Fonts Level 4. Invalid or unrecognized tags are ignored, and only standard forms are supported.

**Why It Matters**:
Enables fine-grained typographic control directly in font-face declarations, aligning with modern font technologies and specifications.

**Implementation Guidance**:
- Use string-based `font-feature-settings` in `@font-face` for advanced typography.
- Validate feature tags for correctness to avoid silent failures.

**References**:
- [Tracking bug #40398871](https://issues.chromium.org/issues/40398871)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5102801981800448)
- [Spec](https://www.w3.org/TR/css-fonts-4/#font-rend-desc)

---

### CSS custom functions

**Impact Level**: 🔴 Critical

**What Changed**:
Custom functions allow authors to define reusable CSS logic that returns values based on parameters, other custom properties, and conditionals.

**Why It Matters**:
This is a major step toward dynamic, DRY (Don't Repeat Yourself) CSS, enabling more maintainable and expressive stylesheets.

**Implementation Guidance**:
- Begin prototyping with custom functions for repetitive or parameterized style logic.
- Ensure fallback strategies for browsers that do not yet support this feature.

**References**:
- [Tracking bug #325504770](https://issues.chromium.org/issues/325504770)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5179721933651968)
- [Spec](https://drafts.csswg.org/css-mixins-1/#defining-custom-functions)

---

### Continue running transitions when switching to initial transition value

**Impact Level**: 🟡 Important

**What Changed**:
Transition-related property changes now only affect newly started transitions. Ongoing transitions continue unaffected unless their animated properties change.

**Why It Matters**:
Improves animation predictability and aligns with the CSS Transitions specification, reducing unexpected animation interruptions.

**Implementation Guidance**:
- Review transition logic to ensure intended behaviors, especially when dynamically updating transition properties.
- Test complex animation sequences for consistency.

**References**:
- [ChromeStatus.com entry](https://chromestatus.com/feature/5194501932711936)
- [Spec](https://www.w3.org/TR/css-transitions-1/#starting)

---

### Corner shaping (`corner-shape`, `superellipse`, `squircle`)

**Impact Level**: 🟡 Important

**What Changed**:
Adds support for advanced corner shaping beyond `border-radius`, including superellipse and squircle shapes, and enables animation between them.

**Why It Matters**:
Unlocks new creative possibilities for UI design, allowing for more organic and visually appealing shapes.

**Implementation Guidance**:
- Experiment with `corner-shape` and related properties in design prototypes.
- Consider accessibility and rendering performance when using complex shapes.

**References**:
- [Tracking bug #393145930](https://issues.chromium.org/issues/393145930)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5357329815699456)
- [Spec](https://drafts.csswg.org/css-borders-4/#corner-shaping)

---

### Add `font-width` property and descriptor and make `font-stretch` a legacy alias

**Impact Level**: 🟡 Important

**What Changed**:
Chrome now recognizes `font-width` as the standard property, with `font-stretch` relegated to a legacy alias, aligning with current specifications.

**Why It Matters**:
Ensures consistency with the CSS Fonts specification and other browsers, reducing cross-browser inconsistencies.

**Implementation Guidance**:
- Update stylesheets to use `font-width` instead of `font-stretch`.
- Monitor for any rendering differences during migration.

**References**:
- [Tracking bug #356670472](https://issues.chromium.org/issues/356670472)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5190141555245056)

---

### Support async attribute for SVG `<script>` element

**Impact Level**: 🟢 Nice-to-have

**What Changed**:
SVG `<script>` elements now support the `async` attribute, allowing scripts to execute asynchronously, similar to HTML.

**Why It Matters**:
Improves performance and responsiveness for SVG-heavy applications by enabling non-blocking script execution.

**Implementation Guidance**:
- Use `async` on SVG scripts where execution order is not critical.
- Test for any race conditions or dependencies in SVG scripting.

**References**:
- [Tracking bug #40067618](https://issues.chromium.org/issues/40067618)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6114615389585408)
- [Spec](https://svgwg.org/svg2-draft/interact.html#ScriptElement:~:text=%E2%80%98script%E2%80%99%20element-,SVG%202%20Requirement%3A,Consider%20allowing%20async/defer%20on%20%E2%80%98script%E2%80%99.,-Resolution%3A)

---

### The `request-close` invoker command

**Impact Level**: 🟢 Nice-to-have

**What Changed**:
Dialog elements can now be closed via a `requestClose()` JavaScript function, firing a cancel event and allowing developers to prevent closure if needed.

**Why It Matters**:
Provides more granular control over dialog lifecycle and user interactions, enhancing accessibility and UX.

**Implementation Guidance**:
- Use `requestClose()` for dialogs requiring conditional closure logic.
- Ensure cancel event handlers are robust and accessible.

**References**:
- [Tracking bug #400647849](https://issues.chromium.org/issues/400647849)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5592399713402880)
- [Spec](https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-command-request-close-state)

---

### Scroll anchoring priority candidate fix

**Impact Level**: 🟡 Important

**What Changed**:
The scroll anchoring algorithm now selects the deepest onscreen element as the anchor, improving scroll stability during dynamic content changes.

**Why It Matters**:
Reduces unexpected scroll jumps, especially in content-rich or dynamically updated layouts.

**Implementation Guidance**:
- Test scroll behavior in dynamic or infinite-scroll interfaces.
- Adjust layout strategies if scroll anchoring changes affect UX.

**References**:
- [ChromeStatus.com entry](https://chromestatus.com/feature/5070370113323008)

---