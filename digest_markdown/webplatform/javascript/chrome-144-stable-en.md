# Chrome 144 Stable - JavaScript Updates

## Area Summary

Chrome 144 brings significant JavaScript enhancements focused on modernizing date/time handling, improving SVG/HTML API consistency, and expanding clipboard interaction capabilities. The standout addition is the Temporal API, a comprehensive replacement for JavaScript's long-problematic Date object, providing developers with a robust, modern foundation for temporal operations. Additional updates enhance cross-platform compatibility through improved SVG element support, strengthen MathML rendering for RTL languages, and introduce clipboard monitoring capabilities that enable advanced synchronization scenarios for web applications like remote desktop clients.

## Detailed Updates

Chrome 144's JavaScript improvements span fundamental language features, DOM API consistency, and specialized rendering capabilities, reflecting the platform's continued evolution toward feature completeness and cross-specification alignment.

### Temporal in ECMA262

#### What's New

The Temporal API introduces a modern, comprehensive solution for working with dates and times in JavaScript, addressing the long-standing pain points of the legacy Date object. Temporal provides a new global namespace (similar to Math) with standard objects and functions designed for precise, timezone-aware temporal operations.

#### Technical Details

Temporal replaces the problematic Date API with a suite of specialized types for different temporal concepts: Instant (fixed point in time), ZonedDateTime (with timezone), PlainDate, PlainTime, PlainDateTime, Duration, and Calendar. The API is immutable by design, avoiding the mutation pitfalls of Date, and provides explicit handling of timezones, calendars, and temporal arithmetic. All operations are precisely defined according to the ECMA262 specification.

#### Use Cases

Developers can now handle complex date/time scenarios with confidence: scheduling across timezones, calendar-aware date arithmetic (accounting for DST transitions), precise duration calculations, and locale-specific date formatting. The immutable design prevents common bugs related to unintended date mutations. Applications requiring reliable temporal logic—such as booking systems, calendar apps, or international scheduling tools—benefit from Temporal's robust foundation.

#### References

- [Tracking bug #detail?id=11544](https://issues.chromium.org/issues/detail?id=11544)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5668291307634688)
- [Spec](https://tc39.es/proposal-temporal/)

### Support `ping`, `hreflang`, `type`, and `referrerPolicy` for `SVGAElement`

#### What's New

Chrome 144 adds support for the `ping`, `hreflang`, `type`, and `referrerPolicy` attributes on `SVGAElement`, aligning SVG anchor elements with their HTML counterparts for consistent link behavior across both markup languages.

#### Technical Details

Previously, `SVGAElement` lacked several attributes available on `HTMLAnchorElement`, creating inconsistencies when working with links in SVG contexts. This update implements the `ping` attribute (for link tracking endpoints), `hreflang` (indicating linked resource language), `type` (MIME type hint), and `referrerPolicy` (controlling referrer information sent with requests). These additions ensure SVG links behave identically to HTML links in terms of navigation metadata and privacy controls.

#### Use Cases

Developers building SVG-based interactive graphics, data visualizations, or mixed HTML/SVG interfaces can now apply uniform link handling patterns. Analytics implementations using the `ping` attribute work consistently across both HTML and SVG links. Internationalized applications can properly annotate SVG links with language information, and privacy-conscious sites can enforce referrer policies uniformly across all link types.

#### References

- [Tracking bug #40589293](https://issues.chromium.org/issues/40589293)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5140707648077824)
- [Spec](https://svgwg.org/svg2-draft/linking.html#InterfaceSVGAElement)

### Mirroring of RTL MathML operators

#### What's New

Chrome 144 implements character-level and glyph-level mirroring for MathML operators when rendering in right-to-left (RTL) mode, ensuring correct visual representation of mathematical notation in RTL language contexts.

#### Technical Details

The implementation handles two mirroring strategies: character-level mirroring uses Unicode's `Bidi_Mirrored` property to swap operators with their directional equivalents (e.g., right parenthesis becomes left parenthesis in RTL). For operators without appropriate mirroring characters, glyph-level mirroring applies the `rtlm` OpenType font feature, allowing fonts to provide mirrored glyphs. This approach preserves semantic correctness for asymmetrical operators (such as the clockwise contour integral) where simple horizontal flipping would alter mathematical meaning.

#### Use Cases

Content authors creating mathematical documents in Arabic, Hebrew, or other RTL languages can now rely on correct operator rendering without manual intervention. Educational platforms, scientific publications, and mathematical notation tools serving international audiences benefit from proper bidirectional math support. The implementation respects mathematical semantics while adapting to directional context, ensuring both visual correctness and preserved meaning.

#### References

- [Tracking bug #40120782](https://issues.chromium.org/issues/40120782)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6317308531965952)
- [Spec](https://w3c.github.io/mathml-core/#layout-of-operators)

### The `clipboardchange` event

#### What's New

The `clipboardchange` event provides notification whenever the system clipboard contents are modified by any application, enabling web applications to respond to clipboard changes without polling.

#### Technical Details

This event fires on clipboard content changes regardless of the source—whether from the web app itself, native system applications, or other programs. The event eliminates the need for inefficient JavaScript polling loops that repeatedly check clipboard contents. Applications can register event listeners on the appropriate scope and receive immediate notification when clipboard state changes, enabling efficient synchronization patterns.

#### Use Cases

Remote desktop clients can keep local and remote clipboards synchronized in real-time, responding immediately to clipboard changes on either end. Collaborative editing tools can detect when users copy content from external sources, triggering appropriate formatting or security checks. Clipboard manager extensions can maintain history without constant polling overhead. Password managers can detect copy operations and offer to clear sensitive clipboard contents after a timeout.

#### References

- [Tracking bug #41442253](https://issues.chromium.org/issues/41442253)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5085102657503232)
- [Spec](https://github.com/w3c/clipboard-apis/pull/239)
