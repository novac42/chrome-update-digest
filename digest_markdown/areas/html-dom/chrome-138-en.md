---
layout: default
title: chrome-138-en
---

## Area Summary

Chrome 138 introduces a focused change in HTML-DOM: the QuotaExceededError will be converted from a string-named DOMException case into a DOMException-derived interface. This enables quota-related errors to carry structured, extensible information beyond a name string. For developers, the change improves error handling and diagnostics for APIs that report quota exceedance. Overall, it advances the web platform by making exception objects more expressive and interoperable.

## Detailed Updates

The single update below expands on the summary and explains developer impacts and references.

### Update QuotaExceededError to a DOMException derived interface

#### What's New
QuotaExceededError is being moved away from being represented only as a DOMException with a specific name string; instead it will be represented by a DOMException-derived interface so that additional structured information can be carried with the error.

#### Technical Details
The proposal removes "QuotaExceededError" from the list of built-in DOMException name-only cases and defines a dedicated DOMException-derived interface for quota-exceeded conditions. This lets implementers surface properties or structured fields on the exception object rather than relying solely on the name property.

#### Use Cases
- APIs that need to signal quota exceedance can provide richer error details for programmatic handling and diagnostics.
- Developers can implement finer-grained recovery or reporting logic based on structured fields exposed by the new exception interface.

#### References
- https://chromestatus.com/feature/5647993867927552
- https://whatpr.org/dom/1245.html
