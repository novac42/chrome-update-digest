---
layout: default
title: Chrome 144 Stable - HTML/DOM Updates
---

# Chrome 144 Stable - HTML/DOM Updates

## Area Summary

Chrome 144 introduces a significant advancement in permission handling through the new `<geolocation>` element, marking a shift toward declarative, user-activated controls for sensitive capabilities. This feature addresses the long-standing UX problem of JavaScript-triggered permission prompts that lack clear user intent signals. By providing a browser-controlled element that users explicitly interact with, Chrome 144 enables better permission prompt experiences and offers recovery paths for previously denied permissions. This update represents the evolution of the experimental `<permission>` element into a capability-specific implementation that delivers a more powerful and tailored developer experience based on feedback from the web community and browser vendors.

## Detailed Updates

The html-dom area in Chrome 144 focuses on improving the declarative control model for sensitive web capabilities, specifically addressing the geolocation permission flow.

### The `<geolocation>` element

#### What's New

Chrome 144 introduces the `<geolocation>` element, a declarative HTML control that allows users to explicitly grant geolocation access through a browser-controlled UI element. This element handles the permission flow automatically and provides location data directly to the site, often eliminating the need for separate JavaScript API calls.

#### Technical Details

The `<geolocation>` element is embedded directly in the page as a browser-controlled component. When users click the element, their interaction provides a clear, intentional signal of consent, which triggers the permission prompt with better context. This approach fundamentally changes how geolocation permissions are requested by moving from JavaScript-initiated prompts to user-initiated declarative controls.

The element evolved from the more generic `<permission>` element that was previously tested in origin trials. Based on developer feedback and input from other browser vendors, the implementation was refined into this capability-specific version to provide a more tailored experience.

#### Use Cases

This feature particularly benefits scenarios where:
- Sites need to request geolocation access with clear user intent
- Users previously denied geolocation permission and need a recovery path
- Developers want to avoid the negative UX of JavaScript-triggered permission prompts
- Applications need a standardized, browser-native control for location access

The declarative approach improves trust and transparency by making the permission request an explicit user action rather than a potentially unexpected JavaScript prompt.

#### References

- [Tracking bug #435351699](https://issues.chromium.org/issues/435351699)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5125006551416832)
- [Spec](https://wicg.github.io/PEPC/permission-elements.html)
