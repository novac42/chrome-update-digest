# Area Summary

Chrome 135 introduces a robust set of CSS enhancements focused on interactive UI elements, improved layout flexibility, and advanced styling capabilities. Key themes include expanded pseudo-element support for scrollable interfaces, new logical properties for internationalization, and more expressive shape and positioning tools. These updates empower developers to create richer, more accessible, and adaptable web experiences with less reliance on JavaScript or complex workarounds. By aligning closely with evolving CSS specifications, Chrome 135 advances the web platform’s ability to deliver modern, performant, and visually engaging applications.

## Detailed Updates

Below is a breakdown of each new CSS feature in Chrome 135, highlighting their technical details and practical developer benefits.

### `::column` pseudo-element for carousels

#### What's New
Enables the use of the `::column` pseudo-element to apply a limited set of styles to generated column fragments, particularly useful in multi-column layouts and carousels.

#### Technical Details
The `::column` pseudo-element allows styling of column fragments after layout, but only with properties that do not affect layout itself. This ensures performance and predictability.

#### Use Cases
- Styling backgrounds or borders of columns in carousels or multi-column text layouts.
- Enhancing visual separation without impacting flow or reflow.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5192332683771904)

---

### `::scroll-button()` pseudo-elements

#### What's New
Introduces interactive scroll buttons as pseudo-elements, such as `::scroll-button(inline-start)` and `::scroll-button(inline-end)`, for scrollable containers.

#### Technical Details
Developers can define content and styles for scroll buttons directly in CSS, enabling native-feeling scroll controls without custom JavaScript.

#### Use Cases
- Adding accessible, customizable scroll buttons to carousels or overflow containers.
- Improving navigation for horizontally or vertically scrollable content.

#### References
- [Tracking bug #370067113](https://issues.chromium.org/issues/370067113)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5093129273999360)
- [Spec](https://drafts.csswg.org/css-overflow-5/#scroll-buttons)

---

### `::scroll-marker` and `::scroll-marker-group`

#### What's New
Adds `::scroll-marker` and `::scroll-marker-group` pseudo-elements for scroll containers, enabling focusable markers for associated items.

#### Technical Details
These pseudo-elements allow developers to visually indicate and style scroll positions or item groupings within a scrollable area.

#### Use Cases
- Creating visual markers for chapters, sections, or items in a long scrollable list.
- Enhancing navigation and accessibility in complex scroll containers.

#### References
- [Tracking bug #332396355](https://issues.chromium.org/issues/332396355)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5160035463462912)
- [Spec](https://drafts.csswg.org/css-overflow-5/#scroll-markers)

---

### CSS Inertness—the `interactivity` property

#### What's New
Introduces the `interactivity` property to control whether an element and its descendants are inert (non-interactive).

#### Technical Details
Setting `interactivity: none` makes elements unfocusable, uneditable, unselectable, and removes them from the accessibility tree and find-in-page results.

#### Use Cases
- Temporarily disabling UI regions for modal dialogs or overlays.
- Improving accessibility and user experience by managing focus and interaction states.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5107436833472512)
- [Spec](https://github.com/flackr/carousel/tree/main/inert)

---

### CSS logical overflow

#### What's New
Adds `overflow-inline` and `overflow-block` properties for controlling overflow in logical directions, adapting to writing modes.

#### Technical Details
`overflow-inline` and `overflow-block` map to `overflow-x` and `overflow-y` based on the document’s writing mode, supporting better internationalization.

#### Use Cases
- Creating layouts that adapt seamlessly to different languages and writing directions.
- Reducing the need for conditional CSS in multilingual applications.

#### References
- [Tracking bug #41489999](https://issues.chromium.org/issues/41489999)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4728308937523200)
- [Spec](https://drafts.csswg.org/css-overflow-3/#overflow-control)

---

### CSS anchor positioning remembered scroll offset

#### What's New
Supports "remembered scroll offset" for anchor positioning, improving how positioned elements respond to scrolling.

#### Technical Details
When an element is anchored and tethered between an anchor and its containing block, the scroll offset is considered in sizing calculations, leading to more predictable positioning.

#### Use Cases
- Tooltips, popovers, or dropdowns that remain correctly positioned during scroll events.
- Complex UI overlays that need to track anchor elements accurately.

#### References
- [Tracking bug #373874012](https://issues.chromium.org/issues/373874012)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4710507824807936)
- [Spec](https://drafts.csswg.org/css-anchor-position-1/#scroll)

---

### CSS `shape()` function

#### What's New
Introduces the `shape()` function for defining responsive, free-form shapes in `clip-path`.

#### Technical Details
`shape()` accepts verbs similar to `path()`, but supports responsive units (like `%`, `vw`) and CSS custom properties, enabling dynamic and adaptable shapes.

#### Use Cases
- Creating complex, responsive masks and clipping paths for images or UI elements.
- Enhancing visual design with fluid, adaptable shapes.

#### References
- [Tracking bug #40829059](https://issues.chromium.org/issues/40829059)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5172258539307008)
- [Spec](https://drafts.csswg.org/css-shapes-2/#shape-function)

---

### `safe-area-max-inset-*` variables

#### What's New
Adds `max-area-safe-inset-*` CSS environment variables representing the maximum possible safe area inset.

#### Technical Details
These variables remain constant, allowing layouts to anticipate the largest possible safe area (e.g., for notches or rounded corners) without triggering relayouts as the safe area changes.

#### Use Cases
- Designing footers or headers that smoothly adapt to device safe areas.
- Preventing unnecessary layout shifts on devices with dynamic safe area insets.

#### References
- [Tracking bug #391621941](https://issues.chromium.org/issues/391621941)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6393888941801472)
- [Spec](https://drafts.csswg.org/css-env-1/#safe-area-max-insets)

---

### Nested pseudo elements styling

#### What's New
Enables styling of pseudo-elements nested within other pseudo-elements, such as `::before::marker` and `::after::marker`.

#### Technical Details
This feature allows more granular and expressive styling of list markers and other generated content, with future support planned for additional combinations.

#### Use Cases
- Customizing list markers within generated content for advanced typographic effects.
- Achieving design requirements that previously required extra markup or scripting.

#### References
- [Tracking bug #373478544](https://issues.chromium.org/issues/373478544)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5199947786616832)
- [Spec](https://www.w3.org/TR/css-pseudo-4/#marker-pseudo)