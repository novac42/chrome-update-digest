---
layout: default
title: css-en
---

## Area Summary

Chrome 133 brings a focused set of CSS-platform improvements centered on richer style expressions, new selector and query capabilities, finer text layout control, and animation introspection. The most impactful changes for developers are the CSS Level 5 `attr()` expansion (typed attribute values usable in any property), scroll-state container queries, the `:open` pseudo-class, and new text-box alignment properties — each enabling more declarative, component-friendly styling. These features advance the web platform by reducing JS workarounds, enabling responsive container-driven styles, and giving designers finer control over layout and animations. Teams building component libraries, design systems, or animation-heavy UI should evaluate these APIs for simplification and performance gains.

## Detailed Updates

Below are the CSS-area changes in Chrome 133 with concise technical notes, practical uses, and links to the provided references.

### CSS advanced `attr()` function

#### What's New
Implements the CSS Level 5 augmentation to `attr()`, allowing types besides `<string>` and permitting `attr()` usage in all CSS properties (not just the pseudo-element `content`).

#### Technical Details
`attr()` now supports typed values per the CSS Values 5 notation and can be interpolated into property values across the stylesheet.

#### Use Cases
Use attribute values (typed) to drive property values for components, reduce JS for simple attribute-driven styling, and enable attribute-to-style data flow in web components.

#### References
- https://developer.mozilla.org/en-US/docs/Web/CSS/attr
- https://issues.chromium.org/issues/246571
- https://chromestatus.com/feature/4680129030651904
- https://drafts.csswg.org/css-values-5/#attr-notation

### CSS `:open` pseudo-class

#### What's New
Adds the `:open` pseudo-class to match `<dialog>`, `<details>` when open, and `<select>` / `<input>` when a picker is showing.

#### Technical Details
Selector-level state matching for open/picker-visible states as specified in Selectors Level 4.

#### Use Cases
Style native controls and disclosure elements directly when they are open or showing pickers without scripting.

#### References
- https://issues.chromium.org/issues/324293874
- https://chromestatus.com/feature/5085419215781888
- https://drafts.csswg.org/selectors-4/#open-state

### CSS scroll state container queries

#### What's New
Container queries can now target descendants based on the scroll state of a container (e.g., when a container is a scroll container or affected by one).

#### Technical Details
The query container is either a scroll container or an element affected by a scroll container’s position; specific scroll-related states (e.g., `stuck`) are queryable per the conditional rules draft.

#### Use Cases
Adapt descendant styles in response to scroll-driven states (sticky behavior, scroll offsets) without JS.

#### References
- https://issues.chromium.org/issues/40268059
- https://chromestatus.com/feature/5072263730167808
- https://www.w3.org/TR/css-conditional-5/#scroll-state-container

### CSS `text-box`, `text-box-trim`, and `text-box-edge`

#### What's New
Introduces `text-box-trim`, `text-box-edge`, and the `text-box` shorthand to provide finer control of vertical text alignment and trimming for optimal text balance.

#### Technical Details
Properties allow specifying sides to trim (above/below) and define the text box edge behavior as described in the inline layout draft.

#### Use Cases
Improve vertical rhythm and alignment in typography-heavy layouts, refine baseline/trimming behavior for tight UI text flows.

#### References
- https://issues.chromium.org/issues/1411581
- https://chromestatus.com/feature/5174589850648576
- https://drafts.csswg.org/css-inline-3/#text-edges

### `Animation.overallProgress`

#### What's New
Adds `overallProgress` to provide a consistent representation of how far an animation has progressed across iterations and regardless of its timeline.

#### Technical Details
`overallProgress` surfaces the animation’s cumulative progress so developers don’t need to manually compute iteration-relative progress or account for timeline peculiarities.

#### Use Cases
Simplify synchronization between animations and JS logic, drive UI state or effects based on a single normalized progress metric.

#### References
- https://issues.chromium.org/issues/40914396
- https://chromestatus.com/feature/5083257285378048
- https://drafts.csswg.org/web-animations-2/#the-overall-progress-of-an-animation

### The `pause()` method of the `Atomics` object

#### What's New
Adds `Atomics.pause()` to hint the CPU that current code is executing a spinlock.

#### Technical Details
A platform-level hint on the Atomics namespace as outlined by the microwait proposal.

#### Use Cases
Primarily beneficial for low-level concurrency patterns; may reduce CPU usage during spinlock waits in multithreaded JS contexts (WebWorkers).

#### References
- https://chromestatus.com/feature/5106098833719296
- https://tc39.es/proposal-atomics-microwait

### CSP hash reporting for scripts

#### What's New
Adds mechanisms for reporting hashes of scripts to help web applications track subresources they download and execute for security/audit requirements.

#### Technical Details
Introduces reporting hooks tied to CSP mechanisms (see tracking bug and ChromeStatus entry).

#### Use Cases
Compliance and inventory tracking for loaded scripts, helpful for security audits and standards like PCI-DSS v4.

#### References
- https://issues.chromium.org/issues/377830102
- https://chromestatus.com/feature/6337535507431424

### DOM state-preserving move

#### What's New
Introduces `Node.prototype.moveBefore` to move elements within the DOM without resetting element state.

#### Technical Details
Moving preserves element state such as loaded `<iframe>` contents and active element focus, rather than performing a remove-and-insert.

#### Use Cases
DOM rearrangement for UI updates that must preserve element state (iframes, media playback, focus) without reloading or losing state.

#### References
- https://chromestatus.com/feature/5135990159835136

### Expose `attributionsrc` attribute on `<area>`

#### What's New
Exposes the `attributionsrc` attribute on `<area>`, aligning the DOM exposure with existing processing behavior.

#### Technical Details
The attribute is made available on `<area>` to match browser processing and to treat `<area>` as a navigation surface.

#### Use Cases
Enable use of attribution reporting semantics on image map areas and maintain consistent attribute access across navigation elements.

#### References
- https://issues.chromium.org/issues/379275911
- https://chromestatus.com/feature/6547509428879360
- https://wicg.github.io/attribution-reporting-api/#html-monkeypatches

### The `FileSystemObserver` interface

#### What's New
Adds a `FileSystemObserver` interface to notify sites of changes to files and directories to which the user has granted permission.

#### Technical Details
Observers can watch changes in the local device file system or Bucket File System / Origin Private File System per the tracking entry.

#### Use Cases
Responsive UIs for apps that reflect local file changes, syncing clients, or editors using the origin-private file storage.

#### References
- https://issues.chromium.org/issues/40105284
- https://chromestatus.com/feature/4622243656630272

### Multiple import maps

#### What's New
Allows multiple import maps per document instead of a single import map loaded before any module, addressing fragility and ordering issues.

#### Technical Details
Enables modularized import map usage to avoid a single large blocking import map and to be robust against modules loading early.

#### Use Cases
Large modular apps can compose import maps from multiple sources, improving resilience and load ordering.

#### References
- https://chromestatus.com/feature/5121916248260608

### Storage Access Headers

#### What's New
Adds headers to let authenticated embeds opt in for unpartitioned cookies and indicate if unpartitioned cookies are (or can be) included in a request.

#### Technical Details
Servers can signal and activate previously granted 'storage-access' permissions via these headers per the privacy group draft.

#### Use Cases
Streamline authenticated third-party embed flows that need access to unpartitioned cookies while aligning with privacy constraints.

#### References
- https://issues.chromium.org/issues/329698698
- https://chromestatus.com/feature/6146353156849664
- https://privacycg.github.io/storage-access-headers

### Support creating `ClipboardItem` with `Promise<DOMString>`

#### What's New
`ClipboardItem` constructor now accepts string values and Promises resolving to Blobs or strings as `ClipboardItemData`.

#### Technical Details
The async clipboard `write()` input can now be backed by Promises resolving to string or Blob, per the Clipboard APIs spec.

#### Use Cases
Make clipboard write operations more flexible when preparing textual content asynchronously before writing.

#### References
- https://issues.chromium.org/issues/40766145
- https://chromestatus.com/feature/4926138582040576
- https://www.w3.org/TR/clipboard-apis/#typedefdef-clipboarditemdata

### WebAssembly Memory64

#### What's New
Adds support for 64-bit indexed linear WebAssembly memories larger than 2^32 bits (Memory64 proposal).

#### Technical Details
Extends existing memory/table instructions to accept 64-bit indexes; no new instructions are introduced.

#### Use Cases
Enable large-memory WebAssembly workloads that might interoperate with graphics or data-heavy apps; relevant to high-performance web components.

#### References
- https://chromestatus.com/feature/5070065734516736
- https://github.com/WebAssembly/memory64/blob/main/proposals/memory64/Overview.md

### Web Authentication API: `PublicKeyCredential` `getClientCapabilities()` method

#### What's New
Adds `getClientCapabilities()` to `PublicKeyCredential` for determining supported WebAuthn client features.

#### Technical Details
Method returns a list of supported client capabilities to tailor authentication flows per client features.

#### Use Cases
Improve progressive enhancement of authentication UX by detecting client capabilities before initiating flows.

#### References
- https://issues.chromium.org/issues/360327828
- https://chromestatus.com/feature/5128205875544064
- https://w3c.github.io/webauthn/#sctn-getClientCapabilities

### X25519 algorithm of the Web Cryptography API

#### What's New
Implements the X25519 algorithm identifier in SubtleCrypto for key agreement operations (generate/import/derive/export).

#### Technical Details
Supports X25519 per the WebCrypto spec for key agreement primitives like deriveKey and deriveBits.

#### Use Cases
Enable modern elliptic-curve key agreement flows for secure application cryptography that may integrate with secure transports or key exchange in web apps.

#### References
- https://issues.chromium.org/issues/378856322
- https://chromestatus.com/feature/6291245926973440
- https://w3c.github.io/webcrypto/#x25519

Saved to: digest_markdown/webplatform/CSS/chrome-133-stable-en.md
