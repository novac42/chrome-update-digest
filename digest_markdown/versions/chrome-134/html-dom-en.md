---
layout: default
title: html-dom-en
---

### 1. Area Summary

Chrome 134's HTML-DOM updates focus on giving developers finer control over built-in UI primitives and evolving the HTML parser to be more permissive for real-world markup. The most impactful changes are customizable rendering for <select>, a parser relaxation that accepts additional tags inside <select>, and new light-dismiss control for <dialog> via a closedby attribute. These updates advance the platform by expanding CSS-driven customization, aligning dialog behavior with the Popover API, and introducing a transitional parser policy to manage compatibility. Developers should note the temporary gating of parser relaxation and plan migrations before the policy ends.

## Detailed Updates

Below are the HTML-DOM changes in Chrome 134 that flow directly from the summary above.

### Customizable `<select>` Element

#### What's New
Customizable `<select>` allows developers to take complete control of the rendering of `<select>` elements by adding the `appearance: base-select` CSS property and value. This feature relies on the `SelectParserRelaxation` flag, which changes the HTML parser to allow more tags within the `<select>`...

#### Technical Details
- CSS: introduces `appearance: base-select` to opt a `<select>` into a renderable baseline that page styles can fully control.
- Parser dependency: the feature depends on the parser change surfaced by the SelectParserRelaxation flag to permit additional child tags.
- Implementation note: the change is tied to Chromium feature gating.

#### Use Cases
- Allows building custom-styled select controls while keeping native form semantics.
- Enables richer UI compositions where developers need complete visual control over select rendering.

#### References
- [Tracking bug #40146374](https://issues.chromium.org/issues/40146374)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5737365999976448)
- [Spec](https://github.com/whatwg/html/issues/9799)

### Select parser relaxation

#### What's New
This change makes the HTML parser allow additional tags in `<select>` besides `<option>`, `<optgroup>`, and `<hr>`. This feature is gated by the temporary policy (`SelectParserRelaxationEnabled`). This is a temporary transition period, and the policy will stop working from Chrome 141.

#### Technical Details
- DOM/parser: relaxes the parser's permitted content model for `<select>`, changing how the DOM tree is produced for malformed or extended markup.
- Policy: controlled by a temporary policy named `SelectParserRelaxationEnabled`; developers should be prepared for the policy to be removed by Chrome 141.
- Compatibility: intended as a transition to reduce breakage for existing pages that include nonstandard children inside `<select>`.

#### Use Cases
- Improves robustness for pages with legacy or nonconforming markup inside `<select>`.
- Facilitates adoption of `appearance: base-select` by ensuring the parser permits richer child structures.

#### References
- [Tracking bug #335456114](https://issues.chromium.org/issues/335456114)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5145948356083712)
- [Spec](https://github.com/whatwg/html/pull/10557)

### Dialog light dismiss

#### What's New
One of the nice features of the Popover API is its light dismiss behavior. This behavior is now part of `<dialog>`, with a new `closedby` attribute controlling the behavior:

  * `<dialog closedby="none">`: No user-triggered closing of dialogs at all.
  * `<dialog closedby="closerequest">`: Pressing...

#### Technical Details
- Web API / DOM: adds a `closedby` content attribute on `<dialog>` to control light-dismiss semantics, aligning dialog behavior with the Popover API interaction model.
- Usability: provides a declarative way to opt dialogs into or out of user-triggered dismiss gestures.
- Interop: follows the HTML spec entry for the new attribute to standardize behavior.

#### Use Cases
- Fine-grained control over whether dialogs should respond to outside clicks, Escape, or other dismissal gestures.
- Matches developer expectations coming from Popover API usage and makes dialog behavior more predictable.

#### References
- [Tracking bug #376516550](https://issues.chromium.org/issues/376516550)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5097714453577728)
- [Spec](https://html.spec.whatwg.org/#attr-dialog-closedby)
