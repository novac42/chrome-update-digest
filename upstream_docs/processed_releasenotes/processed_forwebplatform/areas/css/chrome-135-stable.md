## CSS

### `::column` pseudo-element for carousels

A `::column` pseudo-element, which allows applying a limited set of styles to the generated fragments. Specifically, this would be limited to styles which do not affect the layout, and thus can be applied post-layout.

[ChromeStatus.com entry](https://chromestatus.com/feature/5192332683771904)

### `::scroll-button()` pseudo-elements

Allows the creation of interactive scroll buttons as pseudo-elements, for example:
    
    
    .scroller {
      overflow: auto;
    }
    
    .scroller::scroll-button(inline-start) {
      content: "<";
    }
    
    .scroller::scroll-button(inline-end) {
      content: ">";
    }
    

These should be focusable, behaving as a button (including their UA styles). When activated, a scroll should be performed in the direction by some amount. When it is not possible to scroll in that direction, they should be disabled (and styled with `:disabled`), otherwise they are enabled (and styled with `:enabled`).

The selector lets you define buttons in four logical directions: `block-start`, `block-end`, `inline-start`, `inline-end`; as well as four physical directions: `up`, `down`, `left`, `right`.

[Tracking bug #370067113](https://issues.chromium.org/issues/370067113) | [ChromeStatus.com entry](https://chromestatus.com/feature/5093129273999360) | [Spec](https://drafts.csswg.org/css-overflow-5/#scroll-buttons)

### `::scroll-marker` and `::scroll-marker-group`

Adds the `::scroll-marker` and `::scroll-marker-group` pseudo-elements for scrolling containers. They let you create a set of focusable markers for all of the associated items within the scrolling container.

[Tracking bug #332396355](https://issues.chromium.org/issues/332396355) | [ChromeStatus.com entry](https://chromestatus.com/feature/5160035463462912) | [Spec](https://drafts.csswg.org/css-overflow-5/#scroll-markers)

### CSS Inertness—the `interactivity` property

The `interactivity` property specifies whether an element and its flat tree descendants (including text runs) are inert or not.

Making an element inert affects whether it can be focused, edited, selected, and searchable by find-in-page. It also affects whether it is visible in the accessibility tree.

[ChromeStatus.com entry](https://chromestatus.com/feature/5107436833472512) | [Spec](https://github.com/flackr/carousel/tree/main/inert)

### CSS logical overflow

The `overflow-inline` and `overflow-block` CSS properties allow setting overflow in inline and block direction relative to the writing-mode. In a horizontal writing-mode `overflow-inline` maps to `overflow-x`, while in a vertical writing-mode it maps to `overflow-y`.

[Tracking bug #41489999](https://issues.chromium.org/issues/41489999) | [ChromeStatus.com entry](https://chromestatus.com/feature/4728308937523200) | [Spec](https://drafts.csswg.org/css-overflow-3/#overflow-control)

### CSS anchor positioning remembered scroll offset

Add support for the concept of _remembered scroll offset_.

When a positioned element has a default anchor, and is tethered to this anchor at one edge, and against the original containing block at the other edge, the scroll offset will be taken into account when it comes to sizing the element. This way you can use all visible space (using `position-area`) for the anchored element when the document is scrolled at a given scroll offset.

In order to avoid layout (resizing the element) every time the document is scrolled (which is undesired behavior, and also bad for performance), what will be used is a so-called "remembered scroll offset", rather than always using the current scroll offset. The remembered scroll offset is updated at a so-called "anchor recalculation point", which is either:

  * When the positioned element is initially displayed.
  * When a different position option (`position-try-fallbacks`) is chosen.

[Tracking bug #373874012](https://issues.chromium.org/issues/373874012) | [ChromeStatus.com entry](https://chromestatus.com/feature/4710507824807936) | [Spec](https://drafts.csswg.org/css-anchor-position-1/#scroll)

### CSS `shape()` function

The `shape()` function allows responsive free-form shapes in `clip-path`.

You can define a series of verbs, roughly equivalent to the verbs in `path()`, but where the verbs accept responsive units (such as `%` or `vw`), as well as any CSS values such as custom properties.

[Tracking bug #40829059](https://issues.chromium.org/issues/40829059) | [ChromeStatus.com entry](https://chromestatus.com/feature/5172258539307008) | [Spec](https://drafts.csswg.org/css-shapes-2/#shape-function)

### `safe-area-max-inset-*` variables

This feature adds `max-area-safe-inset-*` variables which don't change and represent the maximum possible safe area inset.

The use case this solves is to avoid needing to relayout the page in cases where the footer (for example) can simply slide as the safe area inset value grows, as opposed to changing size.

[Tracking bug #391621941](https://issues.chromium.org/issues/391621941) | [ChromeStatus.com entry](https://chromestatus.com/feature/6393888941801472) | [Spec](https://drafts.csswg.org/css-env-1/#safe-area-max-insets)

### Nested pseudo elements styling

Allows to style pseudo elements that are nested inside other pseudo elements. So far, support is defined for:

  * `::before::marker`
  * `::after::marker`

With `::column::scroll-marker` being supported in the future.

[Tracking bug #373478544](https://issues.chromium.org/issues/373478544) | [ChromeStatus.com entry](https://chromestatus.com/feature/5199947786616832) | [Spec](https://www.w3.org/TR/css-pseudo-4/#marker-pseudo)
