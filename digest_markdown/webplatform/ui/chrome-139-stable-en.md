---
layout: default
title: Chrome 139 UI Update Digest
---

Save to: digest_markdown/webplatform/ui/chrome-139-stable-en.md

---

# Chrome 139 UI Update Digest

## 1. Executive Summary

Chrome 139 introduces two significant UI-related CSS enhancements: short-circuiting for `var()` and `attr()` functions, and advanced corner shaping via new CSS properties. These updates improve both the robustness and expressiveness of UI styling, enabling more creative and performant designs while reducing the risk of cyclic dependency issues in CSS custom properties.

## 2. Key Implications

### Technical Impact

- **Existing Implementations**: The short-circuiting behavior for `var()` and `attr()` reduces unnecessary cycle checks, potentially improving stylesheet evaluation performance and reliability.
- **New Capabilities**: The new corner shaping properties (`corner-shape`, `superellipse`, `squircle`) allow designers and developers to create more complex and visually appealing UI elements, including squircles, notches, and animated transitions between corner shapes.
- **Technical Debt**: Teams relying on workarounds for advanced corner shapes or managing complex CSS variable fallbacks may now simplify their codebases.

## 3. Risk Assessment

**Critical Risks**:
- No breaking changes identified in these features.
- No direct security considerations introduced by these UI/CSS updates.

**Medium Risks**:
- **Deprecations**: None announced, but teams should monitor for future changes in CSS custom property handling.
- **Performance Impacts**: The short-circuiting of `var()` and `attr()` may slightly alter performance characteristics; teams should validate critical rendering paths.

## 4. Recommended Actions

### Immediate Actions

- Review and test existing CSS that uses `var()` and `attr()` to ensure compatibility with the new short-circuiting behavior.
- Experiment with the new corner shaping properties to evaluate their fit for current and upcoming UI designs.

### Short-term Planning

- Refactor custom corner-shaping workarounds to leverage native CSS properties.
- Update design systems and component libraries to expose new corner-shaping capabilities.

### Long-term Strategy

- Monitor CSSWG and ChromeStatus for further enhancements to CSS custom properties and UI expressiveness.
- Plan for broader adoption of advanced CSS features as browser support matures.

## 5. Feature Analysis

### Short-circuiting `var()` and `attr()`

**Impact Level**: 🟡 Important

**What Changed**:
When the fallback is not taken, `var()` and `attr()` functions now evaluate without searching for cycles in the fallback. This optimizes the evaluation process for CSS custom properties and attributes.

**Why It Matters**:
This change reduces unnecessary computation and the risk of false-positive cycle detections, leading to more predictable and performant CSS variable usage. It also simplifies debugging and maintenance of complex stylesheets.

**Implementation Guidance**:
- Audit existing CSS for reliance on fallback cycles; ensure no unintended side effects.
- Test critical UI paths for any changes in rendering or variable resolution.
- Update documentation to reflect the new evaluation behavior.

**References**:
- [ChromeStatus.com entry](https://chromestatus.com/feature/6212939656462336)

---

### Corner shaping (`corner-shape`, `superellipse`, `squircle`)

**Impact Level**: 🔴 Critical

**What Changed**:
Chrome now supports advanced corner shaping via new CSS properties, allowing developers to specify the shape and curvature of corners as superellipses. This enables the creation of shapes such as squircles, notches, and scoops, and supports animating transitions between these shapes.

**Why It Matters**:
This feature unlocks a new level of design flexibility, enabling modern, visually distinctive UI elements without resorting to SVGs or complex clip-paths. It also streamlines animation and theming for rounded elements, aligning web capabilities with native app design trends.

**Implementation Guidance**:
- Replace custom SVG or clip-path solutions for advanced corners with native CSS properties.
- Update design tokens and component APIs to support new corner shapes.
- Test animations and transitions between corner shapes for smoothness and performance.
- Coordinate with design teams to explore new UI possibilities enabled by these properties.

**References**:
- [Tracking bug #393145930](https://issues.chromium.org/issues/393145930)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5357329815699456)
- [Spec](https://drafts.csswg.org/css-borders-4/#corner-shaping)

---