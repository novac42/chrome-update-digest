---
layout: default
title: chrome-138
---

## Performance

### Add prefetchCache and prerenderCache to Clear-Site-Data header

Two new values for the Clear-Site-Data header to help developers target clearing the prerender and prefetch cache: "prefetchCache" and "prerenderCache".

**References:** [Tracking bug #398149359](https://bugs.chromium.org/p/chromium/issues/detail?id=398149359) | [ChromeStatus.com entry](https://chromestatus.com/feature/5110263659667456) | [Spec](https://w3c.github.io/webappsec-clear-site-data/#grammardef-cache-directive)

### Speculation rules: target_hint field

This extends speculation rules syntax to allow developers to specify the target_hint field. This field provides a hint to indicate a target navigable where a prerendered page will eventually be activated. For example, when `_blank` is specified as a hint, a prerendered page can be activated for a navigable opened by `window.open()`. The field has no effect on prefetching. The specification allows this field to accept any strings that are valid as navigable target name or keyword as the value, but this launch supports only one of "_self" or "_blank" strings. If the hint is not specified, it's treated like "_self" is specified.

**References:** [Tracking bug #40234240](https://bugs.chromium.org/p/chromium/issues/detail?id=40234240) | [ChromeStatus.com entry](https://chromestatus.com/feature/5084493854924800) | [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-target-hint)
