## DOM

### `ToggleEvent` source attribute

The `source` attribute of a `ToggleEvent` contains the element that triggered the `ToggleEvent` to be fired, if applicable. For example, if a user clicks a `<button>` element with the `popovertarget` or `commandfor` attribute set to open a popover, the `ToggleEvent` fired on the popover will have its source attribute set to the invoking `<button>`.

[ChromeStatus.com entry](https://chromestatus.com/feature/5165304401100800) | [Spec](https://html.spec.whatwg.org/multipage/interaction.html#the-toggleevent-interface)
