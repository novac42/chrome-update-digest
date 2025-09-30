## Area Summary

Chrome 136 adds language/locale awareness to Canvas text drawing styles, closing a gap between main-thread <canvas> and OffscreenCanvas rendering. The most impactful change for developers is improved internationalization for text rendering in worker contexts, enabling correct font selection and locale-specific glyphs when drawing to OffscreenCanvas. This aligns OffscreenCanvas behavior with the existing DOM canvas, improving consistency across threading models and advancing platform support for multilingual typography. These updates matter for apps that render text off the main thread (e.g., canvas-based editors, games, and server-side rendering) where consistent glyph choice and layout are important.

## Detailed Updates

Below are the specific changes that implement the summary above.

### Language support for CanvasTextDrawingStyles

#### What's New
The canvas text drawing behavior now respects language/locale information for CanvasTextDrawingStyles in contexts where it was previously unavailable (notably OffscreenCanvas), providing locale-specific font selection and glyph treatment.

#### Technical Details
- <canvas> elements already accept a lang attribute which influences font selection for glyphs with locale variants.
- OffscreenCanvas previously lacked a mechanism to carry locale information to text rendering.
- This update bridges that gap so OffscreenCanvas text drawing can receive the same language context as DOM canvas rendering, ensuring consistent font fallback and glyph selection.

#### Use Cases
- Accurate internationalized text rendering in workers using OffscreenCanvas.
- Consistent typography between main-thread and off-thread canvas rendering for web apps, games, and graphics tools.
- Improved rendering fidelity for languages with locale-specific glyph variants (e.g., CJK, Arabic, Indic scripts) when drawing in background threads.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=385006131
- https://chromestatus.com/feature/5101829618114560
- https://html.spec.whatwg.org/multipage/canvas.html#canvastextdrawingstyles

## Area-Specific Expertise (HTML-DOM focus)

- css: This change affects font selection and fallback behavior in the rendering pipeline; expected to improve layout stability when glyph variants depend on locale.
- webapi: Aligns OffscreenCanvas text drawing semantics with DOM canvas APIs by propagating language context.
- graphics-webgpu: OffscreenCanvas users combining GPU-backed rendering with text layers will get more predictable glyph outcomes across threads.
- javascript: Worker-based drawing scripts can now rely on locale-aware text metrics and glyph selection when using OffscreenCanvas.
- security-privacy: No new surface introduced; follows existing canvas model for language metadata only.
- performance: Enables safer off-main-thread text rendering without losing localization correctness, preserving responsiveness while maintaining fidelity.
- multimedia: Improves textual overlays and captions rendered via canvas in localized media experiences.
- devices: Benefits device-agnostic rendering pipelines that use workers for compositing text onto graphics.
- pwa-service-worker: PWAs using service worker contexts for rendering/offscreen tasks will render locale-accurate text.
- webassembly: WASM modules that drive OffscreenCanvas text rendering can depend on consistent locale-driven glyph choices.
- deprecations: No deprecations associated; this is an enhancement that reduces the need for workarounds.

File saved to: digest_markdown/webplatform/HTML-DOM/chrome-136-stable-en.md