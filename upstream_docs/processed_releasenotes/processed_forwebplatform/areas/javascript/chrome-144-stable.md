## JavaScript

### Temporal in ECMA262

The Temporal API in ECMA262 is a new API that provides standard objects and functions for working with dates and times. `Date` has been a long-standing pain point in ECMAScript. This proposes `Temporal`, a global `Object` that acts as a top-level namespace (similar to `Math`), which brings a modern date and time API to the ECMAScript language.

[Tracking bug #detail?id=11544](https://issues.chromium.org/issues/detail?id=11544) | [ChromeStatus.com entry](https://chromestatus.com/feature/5668291307634688) | [Spec](https://tc39.es/proposal-temporal/)

### Support `ping`, `hreflang`, `type`, and `referrerPolicy` for `SVGAElement`

Adds support for `ping`, `hreflang`, `type`, and `referrerPolicy` attributes on `SVGAElement`, aligning its behavior with `HTMLAnchorElement` for consistent link handling across HTML and SVG.

[Tracking bug #40589293](https://issues.chromium.org/issues/40589293) | [ChromeStatus.com entry](https://chromestatus.com/feature/5140707648077824) | [Spec](https://svgwg.org/svg2-draft/linking.html#InterfaceSVGAElement)

### Mirroring of RTL MathML operators

Supports character-level and glyph-level mirroring when rendering MathML operators in right-to-left mode.

When using RTL mode, some operators can be mirrored by changing them to another code point. For example, a right parenthesis becomes a left parenthesis. This is character-level mirroring, with equivalences defined by Unicode's `Bidi_Mirrored` property.

Some operators have no appropriate mirroring character. Glyph-level mirroring applies in this case, with the `rtlm` font feature, where another glyph can replace it in a mirrored context. Some existing implementations mirror the original glyph directly, but this might change the meaning for asymmetrical characters, for example, the clockwise contour integral.

[Tracking bug #40120782](https://issues.chromium.org/issues/40120782) | [ChromeStatus.com entry](https://chromestatus.com/feature/6317308531965952) | [Spec](https://w3c.github.io/mathml-core/#layout-of-operators)

### The `clipboardchange` event

The `clipboardchange` event fires whenever a web app or any other system application changes the system clipboard contents. This lets web apps, for example, remote desktop clients, keep their clipboards synchronized with the system clipboard. It provides an efficient alternative to polling the clipboard (using JavaScript) for changes.

[Tracking bug #41442253](https://issues.chromium.org/issues/41442253) | [ChromeStatus.com entry](https://chromestatus.com/feature/5085102657503232) | [Spec](https://github.com/w3c/clipboard-apis/pull/239)
