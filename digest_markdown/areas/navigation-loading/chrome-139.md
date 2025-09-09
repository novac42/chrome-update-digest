---
layout: default
title: chrome-139
---

## Navigation

### Clear window name for cross-site navigations that switches browsing context group

Clears the value of the `window.name` property when navigation switches browsing context groups, to avoid leaking information that could be used as a tracking vector.

[Tracking bug #1090128](https://issues.chromium.org/issues/1090128) | [ChromeStatus.com entry](https://chromestatus.com/feature/5962406356320256) | [Spec](https://html.spec.whatwg.org/multipage/browsing-the-web.html#resetBCName)
