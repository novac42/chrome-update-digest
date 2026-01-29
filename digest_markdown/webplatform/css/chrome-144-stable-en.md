# Chrome 144 Stable - CSS Updates

## Area Summary

Chrome 144 brings a comprehensive set of CSS enhancements focused on improving developer control over visual presentation, scroll behavior, and dynamic styling. The release includes 10 CSS features that advance accessibility, layout positioning, and animation capabilities. Key highlights include find-in-page customization through highlight pseudos, enhanced anchor positioning with transform support, and the new `caret-shape` property for input customization. These updates reflect the platform's ongoing commitment to providing developers with more granular control over user interface styling while maintaining strong alignment with modern CSS specifications and addressing long-standing compatibility issues.

## Detailed Updates

Chrome 144's CSS updates span multiple categories, from accessibility improvements to advanced positioning and animation features. The following features represent significant additions to the CSS toolkit available to web developers.

### CSS find-in-page highlight pseudos

#### What's New
This feature exposes find-in-page search result styling to authors as a highlight pseudo-element, similar to selection and spelling errors. Developers can now customize how search results appear when users use the browser's find functionality.

#### Technical Details
The feature provides a new pseudo-element that allows modification of foreground and background colors or addition of text decorations for find-in-page highlights. This gives developers direct control over search result presentation within their pages.

#### Use Cases
This is especially useful when browser default highlight colors have insufficient contrast with page colors or are otherwise unsuitable. Developers can ensure find-in-page results remain visible and accessible regardless of their site's color scheme, improving the search experience for users with custom themes or specific accessibility needs.

#### References
- [Tracking bug #339298411](https://issues.chromium.org/issues/339298411)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5195073796177920)
- [Spec](https://drafts.csswg.org/css-pseudo-4/#selectordef-search-text)

### Non-tree-scoped container-name matching

#### What's New
Container names now match across shadow DOM boundaries, ignoring tree-scope when matching `container-name` for `@container` queries.

#### Technical Details
Previously, `container-name` matching for container queries used tree-scoped names or references for matching. This meant the same name didn't match if the `@container` rule and the `container-type` property originated from different trees, such that the `container-type` declaration came from an inner shadow tree. With this change, container names match regardless of `@container` rule or `container-type` declaration origins.

#### Use Cases
This change enables more predictable and intuitive container query behavior when working with web components and shadow DOM. Developers can now use container queries across component boundaries without worrying about tree-scope limitations, making component-based architectures more flexible.

#### References
- [Tracking bug #440049800](https://issues.chromium.org/issues/440049800)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5194034339512320)
- [Spec](https://drafts.csswg.org/css-conditional-5/#container-name)

### CSS anchor positioning with transforms

#### What's New
When an anchor-positioned element is tethered against an anchor that has a transform, the `anchor()` and `anchor-size()` functions now resolve against the bounding box of the transformed anchor.

#### Technical Details
This update ensures that anchor positioning calculations properly account for transformed anchors or anchors contained by elements with transforms. The positioning system now uses the transformed bounding box rather than the original untransformed coordinates.

#### Use Cases
This enhancement enables developers to create more sophisticated layouts that combine CSS transforms with anchor positioning, such as rotated or scaled anchors with properly positioned tooltips or popovers. It removes a major limitation that previously prevented these features from working together seamlessly.

#### References
- [Tracking bug #382294252](https://issues.chromium.org/issues/382294252)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5201048700583936)
- [Spec](https://drafts.csswg.org/css-anchor-position-1/#anchor-position-size)

### CSS `caret-shape` property

#### What's New
The new `caret-shape` property lets sites choose the shape of the text cursor inside editable elements. The recognized property values are `auto`, `bar`, `block`, and `underscore`.

#### Technical Details
The caret's shape in native applications is most commonly a vertical bar, an underscore, or a rectangular block. Additionally, the shape often varies depending on the input mode, for example, insert or replace. This CSS property brings that same level of control to web applications.

#### Use Cases
This feature is valuable for text editors, code editors, and other applications with rich text input where cursor shape provides meaningful feedback about the editing mode. Developers can now create web-based editors that match the visual conventions of desktop applications, or choose cursor styles that better fit their application's design language.

#### References
- [Tracking bug #353713061](https://issues.chromium.org/issues/353713061)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6106160780017664)
- [Spec](https://drafts.csswg.org/css-ui/#caret-shape)

### SVG2 CSS cascading

#### What's New
Chrome's implementation now aligns with the SVG2 specification for matching CSS rules in `<use>` element trees.

#### Technical Details
Selectors now match against the `<use>` instantiation elements instead of the originating element subtree. This means selectors no longer match ancestor and sibling elements outside the cloned subtree. More importantly, state selectors, for example, `:hover`, now start matching in `<use>` instances.

#### Use Cases
This change enables proper interactive styling of SVG elements referenced through `<use>`, such as hover effects, focus states, and other pseudo-class styling that previously didn't work correctly. Developers can now create more dynamic and interactive SVG graphics with reusable components that respond to user interaction as expected.

#### References
- [Tracking bug #40550039](https://issues.chromium.org/issues/40550039)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5134266027606016)
- [Spec](https://www.w3.org/TR/SVG2/struct.html#UseElement)

### Respect `overscroll-behavior` on non-scrollable scroll containers

#### What's New
The `overscroll-behavior` property now applies to all scroll container elements, regardless of whether those elements currently have overflowing content or are user scrollable.

#### Technical Details
Developers can use `overscroll-behavior` to prevent scroll propagation on an `overflow: hidden` backdrop or an `overflow: auto` element without considering whether it will currently be overflowing. The property is now respected even when the container is not actively scrollable.

#### Use Cases
This simplifies modal dialogs, overlays, and other UI patterns where developers want to prevent scroll chaining without having to dynamically check whether content is overflowing. It provides more predictable scroll behavior across different content states.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5129635997941760)
- [Spec](https://www.w3.org/TR/css-overscroll-1/#propdef-overscroll-behavior)

### Respect `overscroll-behavior` for keyboard scrolls

#### What's New
When you set `overscroll-behavior` to a value other than `auto`, the browser now respects this for keyboard scrolling in addition to mouse and touch scrolling.

#### Technical Details
The browser respects `overscroll-behavior` for mouse or touch scrolling, but keyboard scrolls previously ignored it. This change makes keyboard scrolling also respect `overscroll-behavior`, ensuring consistent behavior across all scroll input methods.

#### Use Cases
This improves accessibility and provides consistent scroll behavior for keyboard users. Developers no longer need separate workarounds to prevent scroll chaining for keyboard navigation, making implementations simpler and more maintainable.

#### References
- [Tracking bug #41378182](https://issues.chromium.org/issues/41378182)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5099117340655616)
- [Spec](https://www.w3.org/TR/css-overscroll-1)

### `@scroll-state` `scrolled` support

#### What's New
This feature lets developers style descendants of containers based on the most recent scrolling direction.

#### Technical Details
The `@scroll-state` conditional rule with `scrolled` support enables CSS to react to scroll state changes, allowing dynamic styling based on whether a container has been scrolled in a particular direction.

#### Use Cases
Developers can create more responsive and context-aware interfaces that adapt styling based on scroll behavior, such as showing or hiding navigation elements, changing header styles based on scroll position, or providing visual feedback about scroll state without requiring JavaScript.

#### References
- [Tracking bug #414556050](https://issues.chromium.org/issues/414556050)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5083137520173056)
- [Spec](https://drafts.csswg.org/css-conditional-5/#scrolled)

### Side-relative syntax for `background-position-x/y` longhands

#### What's New
Developers can now define background image position relative to one of its edges using new side-relative syntax for the `background-position-x` and `background-position-y` longhand properties.

#### Technical Details
This syntax gives developers more flexible and responsive mechanisms to define the background image position, instead of using fixed values that need adaptation to the window or frame size. This feature also applies to the `-webkit-mask-position` property to ensure web compatibility.

#### Use Cases
This enhancement is particularly valuable for responsive designs where background images need to align with specific edges regardless of container size. It eliminates the need for JavaScript or media query workarounds to achieve edge-relative positioning, making responsive background positioning purely declarative.

#### References
- [Tracking bug #40468636](https://issues.chromium.org/issues/40468636)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5073321259565056)
- [Spec](https://drafts.csswg.org/css-backgrounds-4/#background-position-longhands)

### View transitions `waitUntil()` method

#### What's New
A new `waitUntil()` method on the `ViewTransition` object enables advanced control over view transition pseudo-element lifecycle by accepting a promise that delays destruction of the pseudo-tree until it settles.

#### Technical Details
View transitions automatically construct a pseudo-element tree to display and animate participating elements. Per the specification, this subtree is constructed when the view transition starts animating and is destroyed when the animations associated with all view transition pseudo-elements are in the finished state. However, for advanced cases like tying view transitions with Scroll Driven Animations, the subtree needs to persist beyond the animation finish state. The `waitUntil()` function addresses this need.

#### Use Cases
One key example is tying view transitions with Scroll Driven Animations. When a scroll timeline controls the animation, the subtree shouldn't be destroyed when the animations finish because scrolling back should still animate the pseudo elements. This enables sophisticated animation patterns that combine multiple CSS animation features in ways that weren't previously possible.

#### References
- [Tracking bug #346976175](https://issues.chromium.org/issues/346976175)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4812903832223744)
- [Spec](https://drafts.csswg.org/css-view-transitions-2/#dom-viewtransition-waituntil)
