## CSS and UI

### CSS anchored fallback container queries

Introduces `@container anchored(fallback)` to style descendants of anchor positioned elements based on which of `position-try-fallbacks` is applied.

Such queries can be used to style an anchored element's tether or its animations, based on how the anchor and the anchored element are positioned relative to each other.

[Tracking bug #417621241](https://issues.chromium.org/issues/417621241) | [ChromeStatus.com entry](https://chromestatus.com/feature/5177580990496768) | [Spec](https://drafts.csswg.org/css-anchor-position-2/#anchored-container-queries)

### Side-relative syntax for `background-position-x/y` longhands

Defines the background image's position relative to one of its edges.

This syntax provides a more flexible and responsive mechanism to define the background image position, instead of using fixed values that need to be adapted to the window or frame size.

This feature is applied also to the `-webkit-mask-position` property to ensure webcompat levels are the same.

[Tracking bug #40468636](https://issues.chromium.org/issues/40468636) | [ChromeStatus.com entry](https://chromestatus.com/feature/5073321259565056) | [Spec](https://drafts.csswg.org/css-backgrounds-4/#background-position-longhands)

### Implement CSS property `font-language-override`

Introduces support for `font-language-override` CSS property. The property allows developers to override the system language used for OpenType glyph substitution by specifying a four-character language tag directly in CSS.

This enables fine-grained typographic control, particularly useful for multilingual content or fonts with language-specific glyph variants.

[Tracking bug #41170551](https://issues.chromium.org/issues/41170551) | [ChromeStatus.com entry](https://chromestatus.com/feature/5149766073843712) | [Spec](https://www.w3.org/TR/css-fonts-4/#font-language-override-prop)

### Web App Manifest: specify update eligibility

Specify an update eligibility algorithm in the manifest specification. This makes the update process more deterministic and predictable, giving the dev more control over whether (and when) updates should apply to existing installations, and allowing removal of the _update check throttle_ that user agents currently need to implement to avoid wasting network resources.

[Tracking bug #403253129](https://issues.chromium.org/issues/403253129) | [ChromeStatus.com entry](https://chromestatus.com/feature/5148463647686656)
