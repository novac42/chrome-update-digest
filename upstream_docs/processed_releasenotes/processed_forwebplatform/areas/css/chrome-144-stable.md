## CSS and UI

### CSS find-in-page highlight pseudos

This feature exposes _find-in-page_ search result styling to authors as a highlight pseudo-element, similar to selection and spelling errors. This lets developers change foreground and background colors or add text decorations. This is especially useful if browser defaults have insufficient contrast with page colors or are otherwise unsuitable.

[Tracking bug #339298411](https://issues.chromium.org/issues/339298411) | [ChromeStatus.com entry](https://chromestatus.com/feature/5195073796177920) | [Spec](https://drafts.csswg.org/css-pseudo-4/#selectordef-search-text)

### Non-tree-scoped container-name matching

Ignore tree-scope when matching `container-name` for `@container` queries.

Previously, `container-name` matching for container queries used tree-scoped names or references for matching. This meant the same name didn't match if the `@container` rule and the `container-type` property originated from different trees, such that the `container-type` declaration came from an inner shadow tree.

With this change, container names match regardless of `@container` rule or `container-type` declaration origins.

[Tracking bug #440049800](https://issues.chromium.org/issues/440049800) | [ChromeStatus.com entry](https://chromestatus.com/feature/5194034339512320) | [Spec](https://drafts.csswg.org/css-conditional-5/#container-name)

### CSS anchor positioning with transforms

When an anchor-positioned element is tethered against an anchor that has a transform (or is contained by an element with a transform), resolve `anchor()` and `anchor-size()` functions against the bounding box of the transformed anchor.

[Tracking bug #382294252](https://issues.chromium.org/issues/382294252) | [ChromeStatus.com entry](https://chromestatus.com/feature/5201048700583936) | [Spec](https://drafts.csswg.org/css-anchor-position-1/#anchor-position-size)

### CSS `caret-shape` property

The caret's shape in native applications is most commonly a vertical bar, an underscore, or a rectangular block. Additionally, the shape often varies depending on the input mode, for example, insert or replace. The CSS `caret-shape` property lets sites choose one of these shapes for the caret inside editable elements, or leave the choice to the browser. The recognized property values are `auto`, `bar`, `block`, and `underscore`.

[Tracking bug #353713061](https://issues.chromium.org/issues/353713061) | [ChromeStatus.com entry](https://chromestatus.com/feature/6106160780017664) | [Spec](https://drafts.csswg.org/css-ui/#caret-shape)

### SVG2 CSS cascading

Align the Chrome implementation with the SVG2 specification for matching CSS rules in `<use>` element trees.

Match selectors against the `<use>` instantiation elements instead of the originating element subtree. This means selectors no longer match ancestor and sibling elements outside the cloned subtree. More importantly, state selectors, for example, `:hover`, now start matching in `<use>` instances.

[Tracking bug #40550039](https://issues.chromium.org/issues/40550039) | [ChromeStatus.com entry](https://chromestatus.com/feature/5134266027606016) | [Spec](https://www.w3.org/TR/SVG2/struct.html#UseElement)

### Respect `overscroll-behavior` on non-scrollable scroll containers

The `overscroll-behavior` property applies to all scroll container elements, regardless of whether those elements currently have overflowing content or are user scrollable. Developers can use `overscroll-behavior` to prevent scroll propagation on an `overflow: hidden` backdrop or an `overflow: auto` element without considering whether it will currently be overflowing.

[ChromeStatus.com entry](https://chromestatus.com/feature/5129635997941760) | [Spec](https://www.w3.org/TR/css-overscroll-1/#propdef-overscroll-behavior)

### Respect `overscroll-behavior` for keyboard scrolls

When you set `overscroll-behavior` to a value other than `auto`, the browser shouldn't perform scroll chaining. The browser respects this for mouse or touch scrolling, but keyboard scrolls ignored it. This change makes keyboard scrolling also respect `overscroll-behavior`.

[Tracking bug #41378182](https://issues.chromium.org/issues/41378182) | [ChromeStatus.com entry](https://chromestatus.com/feature/5099117340655616) | [Spec](https://www.w3.org/TR/css-overscroll-1)

### `@scroll-state` `scrolled` support

Lets developers style descendants of containers based on the most recent scrolling direction.

[Tracking bug #414556050](https://issues.chromium.org/issues/414556050) | [ChromeStatus.com entry](https://chromestatus.com/feature/5083137520173056) | [Spec](https://drafts.csswg.org/css-conditional-5/#scrolled)

### Side-relative syntax for `background-position-x/y` longhands

Defines the background image position relative to one of its edges.

This syntax gives developers more flexible and responsive mechanisms to define the background image position, instead of using fixed values that need adaptation to the window or frame size.

This feature also applies to the `-webkit-mask-position` property to ensure web compatibility.

[Tracking bug #40468636](https://issues.chromium.org/issues/40468636) | [ChromeStatus.com entry](https://chromestatus.com/feature/5073321259565056) | [Spec](https://drafts.csswg.org/css-backgrounds-4/#background-position-longhands)

### View transitions `waitUntil()` method

View transitions automatically construct a pseudo-element tree to display and animate participating elements in the transition. Per the specification, this subtree is constructed when the view transition starts animating and is destroyed when the animations associated with all view transition pseudo-elements are in the finished state (or more precisely, in a non-running, non-paused state).

This works for most cases and provides a seamless experience for developers. However, for more advanced cases, this is insufficient because developers sometimes want the view transition pseudo-tree to persist beyond the animation finish state.

One example is tying view transitions with Scroll Driven Animations. When a scroll timeline controls the animation, the subtree shouldn't be destroyed when the animations finish because scrolling back should still animate the pseudo elements.

To enable advanced uses of view transition, this intent adds a `waitUntil()` function on the `ViewTransition` object that takes a promise. This promise delays destruction of the pseudo-tree until it settles.

[Tracking bug #346976175](https://issues.chromium.org/issues/346976175) | [ChromeStatus.com entry](https://chromestatus.com/feature/4812903832223744) | [Spec](https://drafts.csswg.org/css-view-transitions-2/#dom-viewtransition-waituntil)
