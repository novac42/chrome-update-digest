## CSS and UI

### Absolute positioning for the `::view-transition` element

View transitions use a pseudo subtree of the element, with `::view-transition` being the root of that transition. Previously, the `::view-transition` element was specified to have `position: fixed`. The CSS Working Group resolved to make this `position: absolute` and so Chrome now reflects that change.

This change shouldn't be noticeable because this element's containing block remains the snapshot containing block in either the absolute or fixed case. The only noticeable difference is in `getComputedStyle`.

[Tracking bug #439800102](https://issues.chromium.org/issues/439800102) | [ChromeStatus.com entry](https://chromestatus.com/feature/6155213736116224) | [Spec](https://github.com/w3c/csswg-drafts/issues/12116)

### `activeViewTransition` property on document

The View Transitions API lets developers start visual transitions between different states. The primary SPA entry point is `startViewTransition()`, which returns a transition object. This object contains several promises and functionality to track transition progress, and lets you manipulate transitions, for example, by skipping the transition or modifying its types.

From Chrome 142, developers no longer need to store this object. A `document.activeViewTransition` property represents this object, or `null` if no transition is ongoing.

This also applies to MPA transitions, where the object is only available through `pageswap` and `pagereveal` events. In this update, `document.activeViewTransition` is set to this object for the duration of the transition.

[Tracking bug #434949972](https://issues.chromium.org/issues/434949972) | [ChromeStatus.com entry](https://chromestatus.com/feature/5067126381215744) | [Spec](https://drafts.csswg.org/css-view-transitions-2)

### `:target-before` and `:target-after` pseudo-classes

These pseudo-classes match scroll markers that are before or after the active marker (matching `:target-current`) within the same scroll marker group, as determined by flat tree order:

  * `:target-before`: Matches all scroll markers that precede the active marker in the flat tree order within the group.
  * `:target-after`: Matches all scroll markers that follow the active marker in the flat tree order within the group.

[Tracking bug #440475008](https://issues.chromium.org/issues/440475008) | [ChromeStatus.com entry](https://chromestatus.com/feature/5120827674722304) | [Spec](https://drafts.csswg.org/css-overflow-5/#active-before-after-scroll-markers)

### Range syntax for style container queries and `if()`

Chrome enhances CSS style queries and the `if()` function by adding support for range syntax.

It extends style queries beyond exact value matching (for example, `style(--theme: dark)`). Developers can use comparison operators (such as `>` and `<`) to compare custom properties, literal values (for example, 10px or 25%), and values from substitution functions like `attr()` and `env()`. For a valid comparison, both sides must resolve to the same data type. It is limited to the following numeric types: `<length>`, `<number>`, `<percentage>`, `<angle>`, `<time>`, `<frequency>`, and `<resolution>`.

[Tracking bug #408011559](https://issues.chromium.org/issues/408011559) | [ChromeStatus.com entry](https://chromestatus.com/feature/5184992749289472) | [Spec](https://drafts.csswg.org/css-conditional-5/#typedef-style-range)

### Interest Invokers (the `interestfor` attribute)

Chrome adds an `interestfor` attribute to `<button>` and `<a>` elements. This attribute adds "interest" behaviors to the element. When a user "shows interest" in the element, actions are triggered on the target element, for example, showing a popover. The user agent detects when a user "shows interest" in the element through methods such as holding the pointer over the element, hitting special hotkeys on the keyboard, or long-pressing the element on touchscreens. When interest is shown or lost, an `InterestEvent` fires on the target, which has default actions for popovers, such as showing and hiding the popover.

[Tracking bug #326681249](https://issues.chromium.org/issues/326681249) | [ChromeStatus.com entry](https://chromestatus.com/feature/4530756656562176) | [Spec](https://github.com/whatwg/html/pull/11006)

### Mobile and desktop parity for select element rendering modes

By using the `size` and `multiple` attributes, the `<select>` element can be rendered as an in-page listbox or a button with a popup. However, these modes don't have consistent availability across mobile and desktop Chrome. In-page listbox rendering is unavailable on mobile, and a button with a popup is unavailable on desktop when the `multiple` attribute is present.

This update adds the listbox to mobile and a multi-select popup to desktop, and ensures that opt-ins with the `size` and `multiple` attributes result in the same rendering mode across mobile and desktop. The changes are summarized as follows:

  * When the `size` attribute has a value greater than `1`, in-page rendering is always used. Mobile devices ignored this before.
  * When the `multiple` attribute is set with no `size` attribute, in-page rendering is used. Mobile devices previously used a popup instead of an in-page listbox.
  * When the `multiple` attribute is set with `size=1`, a popup is used. Desktop devices previously used an in-page listbox.

[Tracking bug #439964654](https://issues.chromium.org/issues/439964654) | [ChromeStatus.com entry](https://chromestatus.com/feature/5412736871825408) | [Spec](https://github.com/whatwg/html/pull/11460)

### Support `download` attribute in SVG `<a>` element

This feature introduces support for the download attribute on the SVGAElement interface in Chromium, aligning with the SVG 2 specification. The download attribute enables authors to specify that the target of an SVG hyperlink should be downloaded rather than navigated to, mirroring the behavior already supported in HTMLAnchorElement. This enhancement promotes interoperability across major browsers and ensures consistent behavior between HTML and SVG link elements, thereby improving developer experience and user expectations.

[Tracking bug #40589293](https://issues.chromium.org/issues/40589293) | [ChromeStatus.com entry](https://chromestatus.com/feature/6265596395913216) | [Spec](https://svgwg.org/svg2-draft/linking.html#InterfaceSVGAElement)
