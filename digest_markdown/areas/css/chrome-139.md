---
layout: default
title: Chrome 139 - CSS & Styling
---

# Chrome 139 - CSS & Styling

[← Back to CSS & Styling](./) | [View Full Chrome 139 Release](/versions/chrome-139/)

## CSS and UI

### Short-circuiting `var()` and `attr()`

When the fallback is not taken, `var()` and `attr()` functions evaluate without looking for cycles in that fallback.

[ChromeStatus.com entry](https://chromestatus.com/feature/6212939656462336)

### Support `font-feature-settings` descriptor in `@font-face` rule

This feature supports the string-based syntax for `font-feature-settings` as defined in CSS Fonts Level 4. Invalid or unrecognized feature tags will be ignored per specification. No binary or non-standard forms are supported.

As OpenType fonts become more widely adopted, this enhancement will improve typographic control, reduce redundancy, and support a more scalable, modern approach to web design.

[Tracking bug #40398871](https://issues.chromium.org/issues/40398871) | [ChromeStatus.com entry](https://chromestatus.com/feature/5102801981800448) | [Spec](https://www.w3.org/TR/css-fonts-4/#font-rend-desc)

### CSS custom functions

Custom functions are similar to custom properties, but instead of returning a single, fixed value, they return values based on other custom properties, parameters, and conditionals.

[Tracking bug #325504770](https://issues.chromium.org/issues/325504770) | [ChromeStatus.com entry](https://chromestatus.com/feature/5179721933651968) | [Spec](https://drafts.csswg.org/css-mixins-1/#defining-custom-functions)

### Continue running transitions when switching to initial transition value

When the transition related properties change, they are only supposed to affect newly started transitions. This means that if you change the transition properties, unless you also change the properties which have active transition animations, those transition animations will continue with the previously specified duration and easing.

Chrome incorrectly canceled transitions when the transition property was set to `none`, even though it doesn't cancel them if you only change the `transition-duration`. This change makes Chrome consistent with Safari and Firefox, allowing active transitions to continue running, until their property value changes triggering a new transition update.

[ChromeStatus.com entry](https://chromestatus.com/feature/5194501932711936) | [Spec](https://www.w3.org/TR/css-transitions-1/#starting)

### Corner shaping (`corner-shape`, `superellipse`, `squircle`)

Enable styling corners, on top of the existing `border-radius`, by expressing the shape and curvature of the corner as a superellipse.

This allows shapes like squircles, notches, and scoops, and animating between them.

[Tracking bug #393145930](https://issues.chromium.org/issues/393145930) | [ChromeStatus.com entry](https://chromestatus.com/feature/5357329815699456) | [Spec](https://drafts.csswg.org/css-borders-4/#corner-shaping)

### Add `font-width` property and descriptor and make `font-stretch` a legacy alias

Before this change Chrome didn't recognize `font-width` as a valid property, instead using `font-stretch` which is now considered a legacy alias.

This change brings Chrome into line with the specification and other browsers.

[Tracking bug #356670472](https://issues.chromium.org/issues/356670472) | [ChromeStatus.com entry](https://chromestatus.com/feature/5190141555245056)

### Support async attribute for SVG `<script>` element

The `SVGScriptElement` interface in SVG 2.0 introduces the async attribute, similar to the `HTMLScriptElement`. This attribute allows scripts to be executed asynchronously, improving the performance and responsiveness of web applications that use SVG.

[Tracking bug #40067618](https://issues.chromium.org/issues/40067618) | [ChromeStatus.com entry](https://chromestatus.com/feature/6114615389585408) | [Spec](https://svgwg.org/svg2-draft/interact.html#ScriptElement:~:text=%E2%80%98script%E2%80%99%20element-,SVG%202%20Requirement%3A,Consider%20allowing%20async/defer%20on%20%E2%80%98script%E2%80%99.,-Resolution%3A)

### The `request-close` invoker command

Dialog elements can be closed through a variety of mechanisms, sometimes developers want to have the ability to prevent closure. To achieve this dialogs fire a cancel event. Originally this was only fired via a close request (for example, an `ESC` key press), recently a `requestClose()` JavaScript function was added which also fires the cancel event.

The `request-close` command brings that new ability to the declarative invoker commands API.

[Tracking bug #400647849](https://issues.chromium.org/issues/400647849) | [ChromeStatus.com entry](https://chromestatus.com/feature/5592399713402880) | [Spec](https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-command-request-close-state)

### Scroll anchoring priority candidate fix

Changes the scroll anchoring algorithm. Instead of selecting the priority candidate as the anchor, choose the candidate as the scope or root of the regular anchor selection algorithm which will select the deepest onscreen element as the anchor.

[ChromeStatus.com entry](https://chromestatus.com/feature/5070370113323008)


---

## Navigation
- [← Previous Version](./chrome-138) | [Next Version →](./chrome-140)
- [All CSS & Styling Updates](./)
- [All Chrome 139 Updates](/versions/chrome-139/)
