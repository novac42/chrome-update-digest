---
layout: default
title: chrome-142-en
---

## Area Summary

Chrome 142 continues to refine CSS-driven UI and interaction surfaces, with notable work on view transitions, scroll-marker pseudo-classes, style-query expressiveness, and platform parity for form controls. The release emphasizes spec-aligned behavior (e.g., `::view-transition` positioning and SVG `<a download>`), new author-facing hooks (`activeViewTransition`, `interestfor`), and richer conditional styling (range syntax for style queries and `if()`). These changes give developers finer control over transitions, responsive behaviors, and consistent rendering across devices, advancing the web platform toward more predictable, declarative UI patterns.

## Detailed Updates

Below are concise, developer-focused breakdowns of each CSS-area change in this release.

### Absolute positioning for the `::view-transition` element

#### What's New
The CSS WG changed the specified positioning for the root view-transition pseudo-element from `fixed` to `absolute`, and Chrome implements that change.

#### Technical Details
The `::view-transition` pseudo subtree is the root used by the View Transitions API. The positioning shift affects layout and stacking behavior during view transitions and aligns Chrome with the updated spec decision.

#### Use Cases
More predictable layout during view transitions, especially when integrating transitions with surrounding layout or when relying on absolute positioning semantics for transition artifacts.

#### References
- [Tracking bug #439800102](https://issues.chromium.org/issues/439800102)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/6155213736116224)  
- [Spec](https://github.com/w3c/csswg-drafts/issues/12116)

### activeViewTransition property on document

#### What's New
A new `activeViewTransition` property is exposed on `document` to surface the active view transition object started via `startViewTransition()`.

#### Technical Details
`startViewTransition()` returns a transition object that exposes promises and methods to track/manipulate transition progress; `document.activeViewTransition` provides a programmatic entry point to observe the current transition state.

#### Use Cases
Single-page apps and frameworks can monitor or coordinate global transition state without threading transition objects through components, enabling centralized logic for overlays, animations, or interruption handling.

#### References
- [Tracking bug #434949972](https://issues.chromium.org/issues/434949972)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5067126381215744)  
- [Spec](https://drafts.csswg.org/css-view-transitions-2)

### `:target-before` and `:target-after` pseudo-classes

#### What's New
New pseudo-classes `:target-before` and `:target-after` match scroll markers located before or after the active scroll marker (`:target-current`) within the same scroll-marker group according to flat tree order.

#### Technical Details
These selectors operate on scroll markers and use flat tree order to determine preceding or succeeding markers relative to the active marker, enabling authors to style items in relation to the current scroll target.

#### Use Cases
Styling previous/next items in a container relative to a navigated target (e.g., highlight the current item and dim others before/after), improved navigational UX tied to scroll position.

#### References
- [Tracking bug #440475008](https://issues.chromium.org/issues/440475008)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5120827674722304)  
- [Spec](https://drafts.csswg.org/css-overflow-5/#active-before-after-scroll-markers)

### Range syntax for style container queries and `if()`

#### What's New
Chrome adds support for range syntax in style queries and the `if()` function, allowing comparisons (e.g., `>`, `<`) rather than only exact value matches.

#### Technical Details
Style queries can now express ranges and comparisons against custom properties or literal values, extending conditional styling beyond equality checks as defined by the conditional spec typedef for style-range.

#### Use Cases
Responsive component styling that adapts based on numeric thresholds (e.g., apply styles when a container size is within a range), more expressive conditional rules without requiring JS.

#### References
- [Tracking bug #408011559](https://issues.chromium.org/issues/408011559)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5184992749289472)  
- [Spec](https://drafts.csswg.org/css-conditional-5/#typedef-style-range)

### Interest Invokers (the `interestfor` attribute)

#### What's New
An `interestfor` attribute is available on `<button>` and `<a>` elements to opt those elements into user "interest" detection that can trigger actions on a target element.

#### Technical Details
When a user "shows interest" (detected by the user agent), behaviors specified via `interestfor` invoke actions such as showing a popover on the referenced target; the user agent determines interest gestures.

#### Use Cases
Declarative triggers for contextual UI (e.g., reveal popovers, previews, or ephemeral UI on hover/focus/peek) without custom event wiring in JavaScript.

#### References
- [Tracking bug #326681249](https://issues.chromium.org/issues/326681249)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/4530756656562176)  
- [Spec](https://github.com/whatwg/html/pull/11006)

### Mobile and desktop parity for select element rendering modes

#### What's New
Chrome works toward parity between mobile and desktop for `<select>` rendering modes (in-page listbox vs. button+popup) controlled by `size` and `multiple`.

#### Technical Details
The `size` and `multiple` attributes determine whether a `<select>` is rendered as an in-page listbox or as a button that opens a popup; this update addresses inconsistent availability of these modes across mobile and desktop.

#### Use Cases
Authors can rely on consistent `<select>` behaviors across form factors, improving responsive forms and reducing platform-specific workarounds.

#### References
- [Tracking bug #439964654](https://issues.chromium.org/issues/439964654)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5412736871825408)  
- [Spec](https://github.com/whatwg/html/pull/11460)

### Support `download` attribute in SVG `<a>` element

#### What's New
Chromium implements the `download` attribute for SVGAElement, aligning behavior with the SVG 2 specification.

#### Technical Details
The `download` attribute on SVG `<a>` elements instructs the user agent to download the hyperlink target rather than navigate to it, mirroring the existing HTML anchor behavior and the SVG2 linking interface.

#### Use Cases
Provide downloadable SVG-linked resources (e.g., assets, generated content) directly from SVG documents without extra scripting.

#### References
- [Tracking bug #40589293](https://issues.chromium.org/issues/40589293)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/6265596395913216)  
- [Spec](https://svgwg.org/svg2-draft/linking.html#InterfaceSVGAElement)

Saved to: digest_markdown/webplatform/CSS/chrome-142-stable-en.md
