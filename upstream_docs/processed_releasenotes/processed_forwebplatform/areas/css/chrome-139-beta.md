## CSS

This release adds six new CSS and UI features.

### Short-circuiting `var()` and `attr()`

When the fallback is not taken, `var()` and `attr()` functions evaluate without looking for cycles in that fallback. The following CSS works, because `--green` and `--blue` exist.
    
    
    --green: green;
    --blue: blue;
    --a: var(--green, var(--b));
    --b: var(--blue, var(--a));
    

### CSS `caret-animation` property

Chrome already supported animation of the `caret-color` property, but when animated the default blinking behavior of the caret interfered with the animation. The CSS `caret-animation` property has two possible values: `auto` and `manual`, where `auto` means browser default (blinking) and `manual` means the web developer is controlling the caret animation. The property also lets users disable blinking using a user stylesheet.

### Corner shaping

Enable styling corners, on top of the existing `border-radius`, by specifying the shape or curvature of the corner. This lets you create shapes like squircles, notches, and scoops, and animate between them. Learn more in [this post from Amit Sheen](https://frontendmasters.com/blog/understanding-css-corner-shape-and-the-power-of-the-superellipse/).

### Continue running transitions when switching to the initial transition value.

When the transition related properties change, they are only supposed to affect newly started transitions. This means that if you change the transition properties, unless you also change the properties which have active transition animations, those transition animations will continue with the previously specified duration, easing, etc. Blink incorrectly canceled transitions when the transition property was set to "none", even though it doesn't cancel them if you only change the transition-duration. With this feature, blink will be consistent with webkit and gecko, allowing active transitions to continue running, unless or until their property value changes triggering a new transition update.

### CSS Custom Functions

Custom Functions are similar to custom properties, but instead of returning a single, fixed value, they return values based on other custom properties, parameters, and conditionals.
    
    
    @function --negate(--value) {
    result: calc(var(--value) * -1);
    }
    
    div {
    --gap: 1em;
    margin-top: --negate(var(--gap));
    }
    

### Support `width` and `height` as presentation attributes on nested `<svg>` elements

Supports applying `width` and `height` as presentation attributes on nested `<svg>` elements through both SVG markup and CSS. This dual approach provides even greater flexibility, letting you manage and style SVG elements more efficiently within complex designs.
