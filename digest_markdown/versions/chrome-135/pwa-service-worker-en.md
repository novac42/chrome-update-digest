---
layout: default
title: Chrome 135 PWA and Service Worker Update Digest
---

# Chrome 135 PWA and Service Worker Update Digest

## 1. Area Summary

Chrome 135 introduces targeted improvements to the PWA and service worker ecosystem, focusing on enhanced consistency and standards alignment for client handling. The main themes are improved service worker coverage for embedded content and stricter adherence to the intended semantics of service worker client URLs. These changes reduce edge-case discrepancies, making offline and resource interception behaviors more predictable for developers. By refining how service workers interact with iframes and document history, Chrome 135 advances the reliability and interoperability of modern web applications, especially those leveraging advanced navigation or dynamic content embedding.

## 2. Detailed Updates

Below are the key updates in Chrome 135 for PWA and service worker, with practical insights for developers.

### Create service worker client and inherit service worker controller for srcdoc iframe

#### What's New
Srcdoc iframes (iframes with inline HTML via the `srcdoc` attribute) are now recognized as service worker clients and inherit their parent document's service worker controller.

#### Technical Details
Previously, srcdoc iframes were not treated as service worker clients, leading to inconsistencies such as missing interception of resource requests and incomplete Resource Timing data. With this update, srcdoc iframes are properly registered as clients, and their network requests can be intercepted and managed by the parent’s service worker. This brings their behavior in line with other iframe types and the service worker specification.

#### Use Cases
- Ensures consistent offline and caching behavior for embedded dynamic content.
- Enables accurate resource interception and timing for analytics or debugging.
- Reduces unexpected discrepancies when using srcdoc iframes in PWAs.

#### References
- [Tracking bug #41411856](https://issues.chromium.org/issues/41411856)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5128675425779712)
- [Spec](https://github.com/w3c/ServiceWorker/issues/765)

### Service Worker client URL ignore `history.pushState()` changes

#### What's New
The `Client.url` property for service worker clients now ignores changes made by `history.pushState()` and similar history APIs, reflecting only the original creation URL of the document.

#### Technical Details
Service worker clients previously reported their current URL, including modifications via the History API. This update ensures that `Client.url` remains fixed to the document’s initial URL, as specified in the service worker standard. This change improves consistency across browsers and prevents confusion when tracking or matching clients in service worker scripts.

#### Use Cases
- Simplifies logic for matching clients in service worker code, especially for navigation and messaging.
- Prevents bugs related to dynamic URL changes in single-page applications (SPAs).
- Aligns with the service worker specification for better cross-browser compatibility.

#### References
- [Tracking bug #41337436](https://issues.chromium.org/issues/41337436)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4996996949344256)
- [Spec](https://www.w3.org/TR/service-workers/#client-url)
