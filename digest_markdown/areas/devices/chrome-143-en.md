---
layout: default
title: chrome-143-en
---

## Area Summary

Chrome 143 introduces native support for gamepad connection lifecycle event handler attributes in the Devices domain. The update adds ongamepadconnected and ongamepaddisconnected attributes to the WindowEventHandlers mixin, making it simpler to attach handlers on global targets like window and document.body. For developers this reduces boilerplate for detecting gamepad connect/disconnect events and aligns browser behavior with the Gamepad API spec. This change advances the web platform by standardizing a convenient, declarative way to observe hardware connection changes.

## Detailed Updates

Below are the Devices-area changes in Chrome 143 that follow from the summary above.

### Gamepad `ongamepadconnected` and `ongamepaddisconnected` event handler attributes

#### What's New
Adds `ongamepadconnected` and `ongamepaddisconnected` event handlers to the `WindowEventHandlers` interface mixin, enabling support for event handler attributes on global targets (for example, `window.ongamepadconnected` and analogous `document.body` attributes).

#### Technical Details
The change implements the event handler attribute additions specified for the Gamepad API by extending the `WindowEventHandlers` mixin. See the tracking and spec links for authoritative details and implementation status.

#### Use Cases
- Simplified, declarative handling of gamepad connect/disconnect events in web apps and games.
- Easier progressive enhancement and compatibility for pages that rely on global handler attributes rather than addEventListener wiring.
- Useful for quick prototypes, embedded widgets, or pages that want to expose inline handlers on window/document.body.

#### References
- [Tracking bug #40175074](https://issues.chromium.org/issues/40175074)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5109540852989952)  
- [Spec](https://w3c.github.io/gamepad/#extensions-to-the-windoweventhandlers-interface-mixin)