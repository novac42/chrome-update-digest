---
layout: default
title: Chrome 137 - CSS & Styling
---

# Chrome 137 - CSS & Styling

[← Back to Chrome 137](./) | [View All CSS & Styling Updates](/areas/css/)

## CSS and UI

### CSS if() function

The CSS `if()` function provides a concise way to express conditional values. It accepts a series of condition-value pairs, delimited by semicolons. The function evaluates each condition sequentially and returns the value associated with the first true condition. If none of the conditions evaluate to true, the function returns an empty token stream. This lets you express complex conditional logic in a simple and concise way.

**Example:**
```css
div {
  color: var(--color);
  background-color: if(style(--color: white): black; else: white);
}
.dark { --color: black; }
.light { --color: white; }
```

```html
<div class="dark">dark</div>
<div class="light">light</div>
```

**References:** [Tracking bug #346977961](https://bugs.chromium.org/p/chromium/issues/detail?id=346977961) | [ChromeStatus.com entry](https://chromestatus.com/feature/5084924504915968) | [Spec](https://www.w3.org/TR/css-values-5/#if-function)

### CSS reading-flow, reading-order properties

The `reading-flow` CSS property controls the order in which elements in a flex, grid, or block layout are exposed to accessibility tools and focused using tab keyboard focus navigation. The `reading-order` CSS property allows authors to manually-override the order within a reading flow container. It is an integer with default value of 0. Learn more about these properties in [Use CSS reading-flow for logical sequential focus navigation](https://developer.chrome.com/blog/reading-flow), and try out some examples.

**References:** [Tracking bug #40932006](https://bugs.chromium.org/p/chromium/issues/detail?id=40932006) | [ChromeStatus.com entry](https://chromestatus.com/feature/5061928169472000) | [Spec](https://drafts.csswg.org/css-display-4/#reading-flow)

### Ignore letter spacing in cursive scripts

This feature adds logic to ignore the letter-spacing setting for cursive scripts as specified by the developer, in line with the specification, to ensure that letter spacing does not disrupt word structure and aims to produce better user experience for users relying on cursive scripts. With this feature, Chrome ensures that cursive scripts will be readable and properly spaced, even if the fonts don't have advanced typographic features. The scripts this applies to in Chromium are Arabic, Hanifi Rohingya, Mandaic, Mongolian, N'Ko, Phags Pa, and Syriac as these scripts are considered cursive as per the specification.

**References:** [Tracking bug #40618336](https://bugs.chromium.org/p/chromium/issues/detail?id=40618336) | [ChromeStatus.com entry](https://chromestatus.com/feature/5088256061988864) | [Spec](https://www.w3.org/TR/css-text-3/#letter-spacing-property)

### Selection API getComposedRanges and direction

This feature ships two new API methods for the Selection API:
- `Selection.direction` which returns the selection's direction as either `none`, `forward`, or `backward`
- `Selection.getComposedRanges()` which returns a list of 0 or 1 composed StaticRange

A composed StaticRange is allowed to cross shadow boundaries, which a normal Range cannot.

**Example:**
```javascript
const range = getSelection().getComposedRanges({shadowRoots: [root]});
```

If the selection crosses a shadow root boundary that isn't provided in the shadowRoots list, then the endpoints of the StaticRange will be rescoped to be outside that tree. This makes sure Chrome doesn't expose unknown shadow trees.

**References:** [Tracking bug #40286116](https://bugs.chromium.org/p/chromium/issues/detail?id=40286116) | [ChromeStatus.com entry](https://chromestatus.com/feature/5069063455711232) | [Spec](https://w3c.github.io/selection-api/#dom-selection-getcomposedranges)

### Support offset-path: shape()

Support `offset-path: shape()`, to allow using responsive shapes to set the animation path.

**References:** [Tracking bug #389713717](https://bugs.chromium.org/p/chromium/issues/detail?id=389713717) | [ChromeStatus.com entry](https://chromestatus.com/feature/5062848242884608) | [Spec](https://www.w3.org/TR/css-shapes-2/#shape-function)

### Support the transform attribute on SVGSVGElement

This feature enables the application of transformation properties—such as scaling, rotation, translation, and skewing—directly to the `<svg>` root element using its transform attribute. This enhancement lets you manipulate the entire SVG coordinate system or its contents as a whole, providing greater flexibility in creating dynamic, responsive, and interactive vector graphics. By supporting this attribute, the `<svg>` element can be transformed without requiring additional wrapper elements or complex CSS workarounds, streamlining the process of building scalable and animated web graphics.

**References:** [Tracking bug #40313130](https://bugs.chromium.org/p/chromium/issues/detail?id=40313130) | [ChromeStatus.com entry](https://chromestatus.com/feature/5070863647424512) | [Spec](https://www.w3.org/TR/SVG2/types.html#InterfaceSVGTransformable)

### System accent color for accent-color property

This lets you use the operating system's accent color for form elements. By using the `accent-color` CSS property, you can ensure that form elements such as checkboxes, radio buttons, and progress bars automatically adopt the accent color defined by the user's operating system. This has been supported on macOS since 2021, and is now supported on Windows and ChromeOS.

**References:** [Tracking bug #40764875](https://bugs.chromium.org/p/chromium/issues/detail?id=40764875) | [ChromeStatus.com entry](https://chromestatus.com/feature/5088516877221888) | [Spec](https://www.w3.org/TR/css-ui-4/#accent-color)

### Allow <use> to reference an external document's root element by omitting the fragment

This feature streamlines the SVG `<use>` element by loosening referencing requirements. Before Chrome 137, you had to explicitly reference fragments within the SVG document. If no fragment ID is given `<use>` won't be able to resolve the target and nothing will be rendered or referred.

**Example:**
A `<use>` element referencing an external file with fragment identifier:
```html
<svg>
  <use xlink:href="myshape.svg#icon"></use>
</svg>
```

In this example, `#icon` is the fragment identifier pointing to an element with `id="icon"` within `myshape.svg`.

Without a fragment identifier:
```html
<svg>
  <use xlink:href="myshape.svg"></use>
</svg>
```

With this feature, omitting fragments or just giving the external svg file name will automatically reference the root element, eliminating the need for you to alter the referenced document just to assign an ID to the root. This enhancement simplifies this manual editing process and improves efficiency.

**References:** [Tracking bug #40362369](https://bugs.chromium.org/p/chromium/issues/detail?id=40362369) | [ChromeStatus.com entry](https://chromestatus.com/feature/5078775255900160) | [Spec](https://www.w3.org/TR/SVG2/struct.html#UseElement)

### Canvas floating point color types

Introduces the ability to use floating point pixel formats (as opposed to 8-bit fixed point) with `CanvasRenderingContext2D`, `OffscreenCanvasRenderingContext2D`, and `ImageData`. This is necessary for high precision applications (for example, medical visualization), high dynamic range content, and linear working color spaces.

**References:** [Tracking bug #40245602](https://bugs.chromium.org/p/chromium/issues/detail?id=40245602) | [ChromeStatus.com entry](https://chromestatus.com/feature/5053734768197632) | [Spec](https://html.spec.whatwg.org/multipage/canvas.html#the-2d-rendering-context)

### view-transition-name: match-element

The `match-element` value generates a unique ID based on the element's identity and renames the same for this element. This is used in Single Page App cases where the element is being moved around and you want to animate it with a view transition.

**References:** [Tracking bug #365997248](https://bugs.chromium.org/p/chromium/issues/detail?id=365997248) | [ChromeStatus.com entry](https://chromestatus.com/feature/5092488609931264) | [Spec](https://drafts.csswg.org/css-view-transitions-2/#view-transition-name-prop)


---

## Navigation
- [Chrome 137 Overview](./)
- [All CSS & Styling Updates](/areas/css/)
- [Browse Other Areas](./)
