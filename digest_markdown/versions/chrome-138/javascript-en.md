---
layout: default
title: javascript-en
---

## Area Summary

Chrome 138 introduces a change in how quota-exceeded errors are represented: moving from using a generic DOMException with a name of "QuotaExceededError" to a dedicated DOMException-derived interface. This allows quota errors to carry structured, additional information beyond the legacy name string. For developers, the most impactful result is improved programmatic error handling and richer diagnostics when storage or quota limits are hit. Overall, the update standardizes error semantics and enables more expressive platform APIs.

## Detailed Updates

Below are the JavaScript-focused details that follow from the summary above.

### Update QuotaExceededError to a DOMException derived interface

#### What's New
Previously the platform signaled quota errors by throwing a DOMException whose name property was set to "QuotaExceededError". The change introduces a DOMException-derived interface specifically for quota-exceeded situations so the error can carry additional information.

#### Technical Details
The proposal replaces the ad-hoc use of DOMException with name="QuotaExceededError" by defining a distinct interface that extends DOMException. This lets implementations attach structured data (fields or properties) to the error object rather than relying only on the name string.

#### Use Cases
- More reliable programmatic detection of quota conditions in storage-related APIs.
- Richer diagnostic data available on the thrown error to support better recovery or telemetry.
- Cleaner, spec-driven error surface for web APIs that need to report quota problems.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5647993867927552  
- Spec: https://whatpr.org/dom/1245.html
