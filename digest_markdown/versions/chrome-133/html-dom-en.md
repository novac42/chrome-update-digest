---
layout: default
title: html-dom-en
---

## Area Summary

Chrome 133's HTML-DOM updates focus on richer popover semantics and developer ergonomics, plus DOM primitives that preserve element state and more flexible clipboard inputs. The popover-related changes (new "hint" value, improved invoker APIs, and nested-invoker behavior fixes) make tooltip-like UI patterns more predictable and easier to implement. The new DOM primitive to move nodes without resetting state enables safer reparenting of heavy elements (iframes, active elements) and can reduce workarounds in frameworks. Allowing ClipboardItem data to be a string or a promise of a string simplifies async clipboard writes and reduces conversions to Blob.

## Detailed Updates

The following details expand on the summary above and list each HTML-DOM feature added in Chrome 133.

### The hint value of the popover attribute

#### What's New
Introduces a third value for the popover attribute: `popover=hint`. This value targets hint/tooltip-like behaviors that differ slightly from existing `auto` and `manual` modes.

#### Technical Details
Per the Popover API, the attribute now accepts `hint` as a semantics-driven option for popovers intended as lightweight hints. The feature documents that hint popovers have slightly different behavior from other popover modes.

#### Use Cases
Implement tooltip-like hints with clearer semantics and less custom behavior. UI components that need lightweight, transient explanatory popovers can adopt `popover=hint` for consistent behavior.

#### References
- [Tracking bug #1416284](https://issues.chromium.org/issues/1416284)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5073251081912320)

### Popover invoker and anchor positioning improvements

#### What's New
Adds an imperative API to establish invoker relationships: `popover.showPopover({source})`, and enables invoker relationships to create implicit anchor element references for positioning.

#### Technical Details
The API provides a programmatic way to set the relationship between a popover and its invoker/source, enabling implicit anchors to be derived from invoker relationships for positioning logic.

#### Use Cases
Dynamic UIs where popovers are shown programmatically (for example, contextual menus or tooltips triggered by complex interactions) can use the imperative API to ensure correct anchoring and positioning.

#### References
- [Tracking bug #364669918](https://issues.chromium.org/issues/364669918)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5120638407409664)

### Popover nested inside invoker shouldn't re-invoke it

#### What's New
Fixes behavior when a popover is nested inside its invoker element so that interacting with the popover itself does not re-invoke or close the popover.

#### Technical Details
Example scenario:
```html
<button popovertarget=foo>Activate
  <div popover id=foo>Clicking me shouldn't close me</div>
</button>
```
Previously, clicks on the nested popover could incorrectly trigger re-invocation behavior; this update prevents that unwanted close/reopen sequence.

#### Use Cases
Button-contained popovers and nested interactive popover content will no longer inadvertently close or re-trigger the invoker, improving UX for nested interactive controls.

#### References
- [Tracking bug #379241451](https://issues.chromium.org/issues/379241451)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4821788884992000)

### DOM state-preserving move

#### What's New
Adds a DOM primitive, `Node.prototype.moveBefore`, to move elements within the DOM without resetting their runtime state.

#### Technical Details
Moving nodes with this primitive preserves element state that would otherwise be lost when removing and reinserting nodes. The documented preserved state includes items such as loaded `<iframe>` elements and other ongoing element state.

#### Use Cases
Frameworks and libraries that reparent nodes for reconciliation or layout changes can move nodes without forcing reloads or resetting active/focus state, reducing workarounds and improving performance for heavy subtrees.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5135990159835136)

### Support creating `ClipboardItem` with `Promise<DOMString>`

#### What's New
The `ClipboardItem` constructor now accepts string values (in addition to Blobs). `ClipboardItemData` may be a Blob, a string, or a Promise resolving to either.

#### Technical Details
This extends the async clipboard `write()` input to accept lazy or asynchronous string data (i.e., `Promise<DOMString>`), reducing the need to convert strings to Blobs before writing.

#### Use Cases
Simplifies writing text or lazily-generated string content to the clipboard in asynchronous flows without intermediate Blob conversion.

#### References
- [Tracking bug #40766145](https://issues.chromium.org/issues/40766145)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4926138582040576)
- [Spec](https://www.w3.org/TR/clipboard-apis/#typedefdef-clipboarditemdata)

Saved to: digest_markdown/webplatform/HTML-DOM/chrome-133-stable-en.md
