---
layout: default
title: chrome-138-en
---

### 1. Area Summary

Chrome 138 introduces a change in how quota exceedance errors are represented: moving from a name-based DOMException entry to a DOMException-derived interface for QuotaExceededError. This enables carrying structured, additional information with quota errors, improving diagnosability and programmatic handling in JavaScript. The change advances the web platform by making exception objects more extensible and aligned with WebIDL-derived interfaces. Developers should plan for more robust error handling and prefer capability checks over brittle string comparisons.

## Detailed Updates

Below is the JavaScript-area update in Chrome 138 and its implications for developers.

### Update QuotaExceededError to a DOMException derived interface

#### What's New
A proposal to stop treating "QuotaExceededError" as only a DOMException name value and instead define it as a DOMException-derived interface that can carry additional information.

#### Technical Details
The change removes "QuotaExceededError" from the list of built-in DOMException name strings and replaces it with a proper DOMException-derived interface. This allows the exception to expose additional properties beyond the legacy name property, enabling richer structured data to be attached to quota errors.

#### Use Cases
- Storage and quota-related APIs can return quota errors with contextual data for better diagnostics.
- Client code can perform more precise programmatic handling of quota conditions (rather than relying solely on string matching).

#### Developer Guidance
Audit code that checks error.name === "QuotaExceededError" and prepare to adopt feature detection or instanceof-style checks once the interface lands. Favor handling richer exception properties where available.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5647993867927552
- Spec: https://whatpr.org/dom/1245.html
