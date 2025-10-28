## Area Summary

Chrome 140 introduces a focused enhancement in the HTML-DOM area: the `ToggleEvent` gains a `source` attribute that identifies the element that triggered the event. This change helps developers reliably discover the trigger element for toggle-like UI (for example, popovers or command-driven controls). By standardizing trigger attribution on the event object, it reduces custom wiring and makes component logic and accessibility handling simpler. The update is a small but practical step toward more expressive, event-driven UI patterns on the web platform.

## Detailed Updates

The single HTML-DOM change in Chrome 140 is listed below and expands on the summary above.

### `ToggleEvent` source attribute

#### What's New
The `source` attribute of a `ToggleEvent` contains the element that triggered the `ToggleEvent` to be fired, if applicable. The release notes give the example that when a user clicks a `<button>` element with `popovertarget` or `commandfor` to open a popover, the `ToggleEvent` fired on the popover will have the triggering element available via its `source` attribute.

#### Technical Details
This is an event-level attribute on `ToggleEvent` that carries a reference to the element responsible for initiating the toggle action. For full specification details and the precise interface, consult the linked spec.

#### Use Cases
- Determining which control opened a popover or toggled a UI region without relying on DOM traversal or custom attributes.  
- Simplifying component code that must map toggle events back to their originating control (e.g., for focus management or command routing).  
- Making event handlers clearer and less brittle by providing explicit trigger information on the `ToggleEvent`.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5165304401100800)
- [Spec](https://html.spec.whatwg.org/multipage/interaction.html#the-toggleevent-interface)
