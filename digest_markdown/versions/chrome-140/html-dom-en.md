---
layout: default
title: Chrome 140 Stable - HTML-DOM Updates
---

# Chrome 140 Stable - HTML-DOM Updates

## Area Summary

Chrome 140 introduces a focused enhancement to the HTML-DOM area with the addition of the `ToggleEvent` source attribute. This update strengthens the connection between interactive elements and their triggered events, providing developers with better context about user interactions that cause toggleable elements like popovers to change state. The feature represents Chrome's continued effort to make DOM events more informative and actionable for developers building interactive web applications. This enhancement is particularly valuable for complex UI patterns where multiple elements might trigger the same toggleable component.

## Detailed Updates

Building on Chrome's commitment to providing richer event context, this release delivers a targeted improvement to the ToggleEvent interface that enhances developer understanding of user interactions.

### `ToggleEvent` source attribute

#### What's New
The `ToggleEvent` now includes a `source` attribute that identifies which element triggered the toggle event. This provides crucial context about the origin of toggle actions, particularly useful when multiple elements can control the same toggleable component.

#### Technical Details
The `source` attribute contains a reference to the DOM element that initiated the `ToggleEvent`. For example, when a user clicks a `<button>` element with the `popovertarget` or `commandfor` attribute set to open a popover, the resulting `ToggleEvent` fired on the popover will have its `source` attribute pointing to that button element. This creates a clear programmatic link between the trigger and the target.

#### Use Cases
This feature enables developers to:
- Build more sophisticated event handling logic by knowing which specific trigger caused a toggle
- Implement different behaviors based on the source element (e.g., different animations or positioning)
- Create better accessibility experiences by maintaining focus context
- Debug toggle-related interactions more effectively
- Build analytics that track which UI elements are most effective at triggering user actions

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5165304401100800)
- [Spec](https://html.spec.whatwg.org/multipage/interaction.html#the-toggleevent-interface)
