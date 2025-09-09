---
layout: default
title: chrome-138
---

## JavaScript

### Update QuotaExceededError to a DOMException derived interface

Previously, when the web platform wants to tell you when you've exceeded quota, it will use `DOMException` with the specific name property set to `QuotaExceededError`. However this does not allow carrying additional information. This proposes removing "QuotaExceededError" from the list of built-in DOMException names, and instead creates a class name `QuotaExceededError` from the list of built-in DOMException and has the additional optional properties `quota` and `requested`. We propose all instances of specs that throw "QuotaExceededError" `DOMException`s get upgraded to instead throw `QuotaExceededError`s. For now, such specs would leave the `quota` and `requested` properties at their default value of null, but they could eventually upgrade to include that data, if it's useful for their use case (and isn't, e.g., a privacy leak).

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5647993867927552) | [Spec](https://whatpr.org/dom/1245.html)
