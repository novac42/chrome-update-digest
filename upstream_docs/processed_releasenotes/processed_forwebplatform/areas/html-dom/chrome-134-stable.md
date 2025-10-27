## HTML and DOM

### Customizable `<select>` Element

Customizable `<select>` allows developers to take complete control of the rendering of `<select>` elements by adding the `appearance: base-select` CSS property and value.

This feature relies on the `SelectParserRelaxation` flag, which changes the HTML parser to allow more tags within the `<select>` tag.

[Tracking bug #40146374](https://issues.chromium.org/issues/40146374) | [ChromeStatus.com entry](https://chromestatus.com/feature/5737365999976448) | [Spec](https://github.com/whatwg/html/issues/9799)

### Select parser relaxation

This change makes the HTML parser allow additional tags in `<select>` besides `<option>`, `<optgroup>`, and `<hr>`.

This feature is gated by the temporary policy (`SelectParserRelaxationEnabled`). This is a temporary transition period, and the policy will stop working from Chrome 141.

If you are experiencing problems that you believe are caused by this change, there's a reverse origin trial to disable the parser relaxation.

[Tracking bug #335456114](https://issues.chromium.org/issues/335456114) | [ChromeStatus.com entry](https://chromestatus.com/feature/5145948356083712) | [Spec](https://github.com/whatwg/html/pull/10557)

### Dialog light dismiss

One of the nice features of the Popover API is its light dismiss behavior. This behavior is now part of `<dialog>`, with a new `closedby` attribute controlling the behavior:

  * `<dialog closedby="none">`: No user-triggered closing of dialogs at all.
  * `<dialog closedby="closerequest">`: Pressing `Esc` (or other close trigger) closes the dialog
  * `<dialog closedby="any">`: Clicking outside the dialog, or pressing `Esc`, closes the dialog. Akin to `popover="auto"` behavior.

[Tracking bug #376516550](https://issues.chromium.org/issues/376516550) | [ChromeStatus.com entry](https://chromestatus.com/feature/5097714453577728) | [Spec](https://html.spec.whatwg.org/#attr-dialog-closedby)
