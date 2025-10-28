## HTML and DOM

### The hint value of the popover attribute

The Popover API specifies the behavior for two values of the popover attribute: auto and manual. This feature describes a third value, `popover=hint`. Hints, which are most often associated with "tooltip" type behaviors, have slightly different behaviors. Primarily, the difference is that a hint is subordinate to auto when opening nested stacks of popovers. So it is possible to open an unrelated hint popover while an existing stack of auto popovers stays open.

The canonical example is that a `<select>` picker is open (`popover=auto`) and a hover-triggered tooltip (`popover=hint`) is shown. That action does not close the `<select>` picker.

[Tracking bug #1416284](https://issues.chromium.org/issues/1416284) | [ChromeStatus.com entry](https://chromestatus.com/feature/5073251081912320)

### Popover invoker and anchor positioning improvements

Adds an imperative way to set invoker relationships between popovers with `popover.showPopover({source})`. Enables invoker relationships to create implicit anchor element references.

[Tracking bug #364669918](https://issues.chromium.org/issues/364669918) | [ChromeStatus.com entry](https://chromestatus.com/feature/5120638407409664)

### Popover nested inside invoker shouldn't re-invoke it

In the following case clicking the button properly activates the popover, however, clicking on the popover itself after that shouldn't close the popover.
    
    
    <button popovertarget=foo>Activate
      <div popover id=foo>Clicking me shouldn't close me</div>
    </button>
    

Previously this happened, because the popover click bubbles to the `<button>` and activates the invoker, which toggles the popover closed. This has now been changed to the expected behavior.

[Tracking bug #https://crbug.com/379241451](https://issues.chromium.org/issues/https://crbug.com/379241451) | [ChromeStatus.com entry](https://chromestatus.com/feature/4821788884992000)
