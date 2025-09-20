## CSS

### CSS typed arithmetic

Typed arithmetic lets you write expressions in CSS such as `calc(10em / 1px)` or `calc(20% / 0.5em * 1px)`. This is useful in, for example, typography, as it lets you convert a typed value into an untyped one and reuse it for number accepting properties. Another use case is to multiply the unitless value by another type. For example, you can now cast from pixels to degrees.

[Tracking bug #40768696](https://issues.chromium.org/issues/40768696) | [ChromeStatus.com entry](https://chromestatus.com/feature/4740780497043456) | [Spec](https://www.w3.org/TR/css-values-4/#calc-type-checking)

### CSS `caret-animation` property

Chromium supports animation of the `caret-color` property. However, when animated, the caret's default blinking behavior interferes with the animation.

The CSS `caret-animation` property has two possible values: `auto` and `manual`. `auto` means browser default (blinking), and `manual` means the developer controls the caret animation. Additionally, users who are disturbed by or have adverse reactions to blinking or flashing visuals can disable the blinking with a user stylesheet.

[Tracking bug #329301988](https://issues.chromium.org/issues/329301988) | [ChromeStatus.com entry](https://chromestatus.com/feature/5082469066604544) | [Spec](https://drafts.csswg.org/css-ui/#caret-animation)

### highlightsFromPoint API

The `highlightsFromPoint` API lets developers interact with custom highlights. It detects which highlights exist at a specific point within a document. This interactivity is valuable for complex web features where multiple highlights may overlap or exist within shadow DOM. By providing precise point-based highlight detection, the API empowers developers to manage dynamic interactions with custom highlights more effectively. For example, developers can respond to user clicks or hover events on highlighted regions to trigger custom tooltips, context menus, or other interactive features.

[Tracking bug #365046212](https://issues.chromium.org/issues/365046212) | [ChromeStatus.com entry](https://chromestatus.com/feature/4552801607483392) | [Spec](https://drafts.csswg.org/css-highlight-api-1/#interactions)

### `ScrollIntoView` container option

The `ScrollIntoViewOptions` container option allows developers to perform a `scrollIntoView` operation that only scrolls the nearest ancestor scroll container. For example, the following snippet only scrolls the scroll container of `target` to bring `target` into view, but won't scroll all of the scroll containers to the viewport:
    
    
    target.scrollIntoView({container: 'nearest'});
    

[ChromeStatus.com entry](https://chromestatus.com/feature/5100036528275456) | [Spec](https://drafts.csswg.org/cssom-view/#dom-scrollintoviewoptions-container)

### View transitions: Inherit more animation properties

Adds more animation properties to inherit through the view transition pseudo tree:

  * `animation-timing-function`
  * `animation-iteration-count`
  * `animation-direction`
  * `animation-play-state`

[Tracking bug #427741151](https://issues.chromium.org/issues/427741151) | [ChromeStatus.com entry](https://chromestatus.com/feature/5154752085884928) | [Spec](https://www.w3.org/TR/css-view-transitions-2)

### View transition pseudos inherit animation-delay.

In addition to the previous update, the `animation-delay` property is now inherited through the view transition pseudo tree.

[ChromeStatus.com entry](https://chromestatus.com/feature/5424291457531904) | [Spec](https://www.w3.org/TR/css-view-transitions-2)

### Nested view transitions groups

This feature allows view transitions to generate a nested pseudo-element tree rather than a flat one. This allows the view transition to appear more in line with its original elements and visual intent. It enables clipping, nested 3D transforms, and proper application of effects like opacity, masking, and filters.

[Tracking bug #399431227](https://issues.chromium.org/issues/399431227) | [ChromeStatus.com entry](https://chromestatus.com/feature/5162799714795520) | [Spec](https://www.w3.org/TR/css-view-transitions-2/#view-transition-group-prop)

### Propagate viewport `overscroll-behavior` from root

This change propagates `overscroll-behavior` from the root instead of the body.

The CSS working group resolved not to propagate properties from the `<body>` to the viewport. Instead, properties of the viewport propagate from the root (`<html>`) element. As such, `overscroll-behavior` should propagate from the root element. However, Chrome has had a longstanding issue: it propagates `overscroll-behavior` from the `<body>` rather than the root. This behavior is not interoperable with other browsers. This change makes Chrome comply with the specification and become interoperable with other implementations.

[Tracking bug #41453796](https://issues.chromium.org/issues/41453796) | [ChromeStatus.com entry](https://chromestatus.com/feature/6210047134400512) | [Spec](https://drafts.csswg.org/css-overscroll-behavior-1)

### CSS `counter()` and `counters()` in alt text of `content` property

This feature adds the ability to use `counter()` and `counters()` in the alt text of the `content` property. This provides more meaningful information to improve accessibility.

[Tracking bug #417488055](https://issues.chromium.org/issues/417488055) | [ChromeStatus.com entry](https://chromestatus.com/feature/5185442420621312) | [Spec](https://drafts.csswg.org/css-content/#content-property)

### CSS `scroll-target-group` property

The `scroll-target-group` property specifies whether the element is a scroll marker group container. It accepts one of the following values:

  * 'none': The element does not establish a scroll marker group container.
  * 'auto': The element establishes a scroll marker group container forming a scroll marker group containing all of the scroll marker elements for which this is the nearest ancestor scroll marker group container.

Establishing a scroll marker group container lets any anchor HTML elements with a fragment identifier that are inside such a container to be the HTML equivalent of `::scroll-marker` pseudo-elements. The anchor element whose scroll target is currently in view can be styled using the `:target-current` pseudo-class.

[Tracking bug #6607668](https://issues.chromium.org/issues/6607668) | [ChromeStatus.com entry](https://chromestatus.com/feature/5189126177161216) | [Spec](https://drafts.csswg.org/css-overflow-5/#scroll-target-group)

### Support `font-variation-settings` descriptor in `@font-face` rule

CSS allows developers to adjust a font's weight, width, slant, and other axes using the `font-variation-settings` property on individual elements. However, Chromium-based browsers lack support for this property within `@font-face` declarations. This feature supports the string-based syntax for `font-variation-settings` as defined in CSS Fonts Level 4. Invalid or unrecognized feature tags are ignored per specification. No binary or non-standard forms are supported. Variable fonts are becoming more widely adopted for both performance and typographic flexibility. Adding support for this descriptor in Chromium enhances control, reduces repetition, and supports a more scalable, modern approach to web typography.

[Tracking bug #40398871](https://issues.chromium.org/issues/40398871) | [ChromeStatus.com entry](https://chromestatus.com/feature/5221379619946496) | [Spec](https://www.w3.org/TR/css-fonts-4/#font-rend-desc)
