---
layout: default
title: chrome-139
---

## DOM

### Allow more characters in JavaScript DOM APIs

The HTML parser has always (or for a long time) allowed elements and attributes to have a wide variety of valid characters and names, but the JavaScript DOM APIs to create the same elements and attributes are more strict and don't match the parser.

This change relaxes the validation of the javascript DOM APIs to match the HTML parser.

[Tracking bug #40228234](https://issues.chromium.org/issues/40228234) | [ChromeStatus.com entry](https://chromestatus.com/feature/6278918763708416) | [Spec](https://dom.spec.whatwg.org/#namespaces)
