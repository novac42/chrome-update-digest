---
layout: default
title: Chrome Update Analyzer - Area-Specific Expert Analysis (English)
---

# Chrome Update Analyzer - Area-Specific Expert Analysis (English)

## Area Summary

Chrome 136's **HTML-DOM** updates focus on enhancing canvas text rendering capabilities and improving SVG API consistency with W3C specifications. The most significant addition is language support for CanvasTextDrawingStyles, which enables proper locale-specific font selection in OffscreenCanvas contexts—addressing a long-standing gap in internationalization support. Additionally, updates to SVG geometry methods align Chromium with modern W3C standards by adopting DOMPointInit interfaces. These changes collectively advance web platform capabilities for graphics rendering and international content handling, providing developers with more robust tools for creating accessible, localized web applications.

## Detailed Updates

These updates strengthen Chrome's DOM implementation with improved internationalization and standards compliance, building on the platform's commitment to consistent cross-browser behavior.

### Language support for CanvasTextDrawingStyles

#### What's New
Chrome 136 introduces language attribute support for OffscreenCanvas text rendering, enabling locale-specific font selection and glyph treatment in canvas contexts that previously lacked internationalization capabilities.

#### Technical Details
The `<canvas>` DOM element has long supported the `lang` attribute for language-specific font selection, allowing browsers to choose appropriate locale-specific glyphs when available in fonts. However, when creating an `OffscreenCanvas` (which exists independently of the DOM), there was no mechanism to specify locale information. This update extends the CanvasTextDrawingStyles interface to respect language settings, ensuring consistent internationalization behavior across all canvas contexts.

#### Use Cases
This enhancement is particularly valuable for applications that:
- Render text in multiple languages using OffscreenCanvas for performance optimization
- Generate graphics with locale-specific typography in web workers
- Create internationalized data visualizations or dynamic text rendering
- Build canvas-based games or applications that need proper font selection for different languages

#### References
- [Tracking bug #385006131](https://bugs.chromium.org/p/chromium/issues/detail?id=385006131)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5101829618114560)
- [Spec](https://html.spec.whatwg.org/multipage/canvas.html#canvastextdrawingstyles)

### Use DOMPointInit for getCharNumAtPosition, isPointInFill, isPointInStroke

#### What's New
Chromium now uses `DOMPointInit` instead of the legacy `SVGPoint` interface for the `getCharNumAtPosition`, `isPointInFill`, and `isPointInStroke` methods in SVG geometry elements, aligning with the latest W3C specifications.

#### Technical Details
This change updates `SVGGeometryElement` and `SVGPathElement` methods to accept `DOMPointInit` parameters, which is the modern, standardized interface for representing 2D and 3D points in web APIs. The `DOMPointInit` interface provides better type safety and consistency across different Web APIs compared to the legacy `SVGPoint` interface, representing part of the broader web platform modernization effort.

#### Use Cases
Developers working with SVG will benefit from:
- More consistent API patterns when working with point-based calculations in SVG
- Better TypeScript support and type checking for SVG geometry operations
- Simplified code when using these methods alongside other modern Web APIs that already use DOMPointInit
- Future-proofed code that aligns with current web standards

#### References
- [Tracking bug #40572887](https://bugs.chromium.org/p/chromium/issues/detail?id=40572887)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5084627093929984)
- [Spec](https://www.w3.org/TR/SVG2/types.html#InterfaceDOMPointInit)
