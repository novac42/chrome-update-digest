---
layout: default
title: html-dom
---

## HTML and DOM

### Language support for CanvasTextDrawingStyles

The `<canvas>` DOM element, like all DOM elements, accepts a `lang` attribute that is used to define language specific treatment for font selection (when fonts have locale specific glyphs). Browsers respect this attribute. However, when an `OffscreenCanvas` is created there is no way to set locale information, possibly resulting in a state where an offscreen canvas produces rendered results that differ from the canvas in which its output is used. This feature adds a `lang` IDL attribute to `CanvasTextDrawingStyles` to give developers direct control over the language for the text drawing and metrics.

**References:** [Tracking bug #385006131](https://bugs.chromium.org/p/chromium/issues/detail?id=385006131) | [ChromeStatus.com entry](https://chromestatus.com/feature/5101829618114560) | [Spec](https://html.spec.whatwg.org/multipage/canvas.html#canvastextdrawingstyles)
