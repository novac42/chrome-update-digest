## CSS

### CSS advanced `attr()` function

Implements the augmentation to `attr()` specified in CSS Level 5, which allows types besides `<string>` and use in all CSS properties (in addition to the existing support for the pseudo-element content).

[MDN attr()](https://developer.mozilla.org/en-US/docs/Web/CSS/attr) | [Tracking bug #246571](https://issues.chromium.org/issues/246571) | [ChromeStatus.com entry](https://chromestatus.com/feature/4680129030651904) | [Spec](https://drafts.csswg.org/css-values-5/#attr-notation)

### CSS `:open` pseudo-class

The `:open` pseudo-class matches `<dialog>` and `<details>` when they are in their open state, and matches `<select>` and `<input>` when they are in modes which have a picker and the picker is showing.

[Tracking bug #324293874](https://issues.chromium.org/issues/324293874) | [ChromeStatus.com entry](https://chromestatus.com/feature/5085419215781888) | [Spec](https://drafts.csswg.org/selectors-4/#open-state)

### CSS scroll state container queries

Use container queries to style descendants of containers based on their scroll state.

The query container is either a scroll container, or an element affected by the scroll position of a scroll container. The following states can be queried:

  * `stuck`: A sticky positioned container is stuck to one of the edges of the scroll box.
  * `snapped`: A scroll snap aligned container is currently snapped horizontally or vertically.
  * `scrollable`: Whether a scroll container can be scrolled in a queried direction.

A new container-type: `scroll-state` lets containers be queried.

[Tracking bug #40268059](https://issues.chromium.org/issues/40268059) | [ChromeStatus.com entry](https://chromestatus.com/feature/5072263730167808) | [Spec](https://www.w3.org/TR/css-conditional-5/#scroll-state-container)

### CSS `text-box`, `text-box-trim`, and `text-box-edge`

To achieve optimal balance of text content, the `text-box-trim` and text-box-edge properties, along with the text-box shorthand property, make finer control of vertical alignment of text possible.

The `text-box-trim` property specifies the sides to trim, above or below, and the `text-box-edge` property specifies how the edge should be trimmed.

These properties let you control vertical spacing precisely by using the font metrics.

[Tracking bug #1411581](https://issues.chromium.org/issues/1411581) | [ChromeStatus.com entry](https://chromestatus.com/feature/5174589850648576) | [Spec](https://drafts.csswg.org/css-inline-3/#text-edges)

### Web APIs

### `Animation.overallProgress`

Provides developers with a convenient and consistent representation of how far along an animation has advanced across its iterations and regardless of the nature of its timeline. Without the `overallProgress` property, you need to manually compute how far an animation has advanced, factoring in the number of iterations of the animation and whether the `currentTime` of the animation is a percentage of total time (as in the case of scroll-driven animations) or an absolute time quantity (as in the case of time-driven animations).

[Tracking bug #40914396](https://issues.chromium.org/issues/40914396) | [ChromeStatus.com entry](https://chromestatus.com/feature/5083257285378048) | [Spec](https://drafts.csswg.org/web-animations-2/#the-overall-progress-of-an-animation)

### The `pause()` method of the `Atomics` object

Adds the `pause()` method to the `Atomics` namespace object, to hint the CPU that the current code is executing a spinlock.

[ChromeStatus.com entry](https://chromestatus.com/feature/5106098833719296) | [Spec](https://tc39.es/proposal-atomics-microwait)

### CSP hash reporting for scripts

Complex web applications often need to keep track of the subresources that they download, for security purposes.

In particular, upcoming industry standards and best practices (for example, PCI-DSS v4) require that web applications keep an inventory of all the scripts they download and execute.

This feature builds on CSP and the Reporting API to report the URLs and hashes (for CORS/same-origin) of all the script resources that the document loads.

[Tracking bug #377830102](https://issues.chromium.org/issues/377830102) | [ChromeStatus.com entry](https://chromestatus.com/feature/6337535507431424)

### DOM state-preserving move

Adds a DOM primitive (`Node.prototype.moveBefore`) that lets you move elements around a DOM tree, without resetting the element's state.

When moving instead of removing and inserting, following state such as the following is preserved:

  * `<iframe>` elements remain loaded.
  * The active element remains focus.
  * Popovers, fullscreen, and modal dialogs remain open.
  * CSS transitions and animations continue.

[ChromeStatus.com entry](https://chromestatus.com/feature/5135990159835136)

### Expose `attributionsrc` attribute on `<area>`.

Aligns exposure of the `attributionsrc` attribute on `<area>` with the existing processing behavior of the attribute, even when it wasn't exposed.

Additionally, it makes sense to support the attribute on `<area>`, as that element is a first-class navigation surface, and Chrome already supports this on the other surfaces of `<a>` and `window.open`.

[Tracking bug #379275911](https://issues.chromium.org/issues/379275911) | [ChromeStatus.com entry](https://chromestatus.com/feature/6547509428879360) | [Spec](https://wicg.github.io/attribution-reporting-api/#html-monkeypatches)

### The `FileSystemObserver` interface

The `FileSystemObserver` interface notifies websites of changes to the file system. Sites observe changes to files and directories, to which the user has previously granted permission, in the user's local device, or in the Bucket File System (also known as the Origin Private File System), and are notified of basic change info, such as the change type.

[Tracking bug #40105284](https://issues.chromium.org/issues/40105284) | [ChromeStatus.com entry](https://chromestatus.com/feature/4622243656630272)

### Multiple import maps

Import maps currently have to load before any ES module and there can only be a single import map per document. That makes them fragile and potentially slow to use in real-life scenarios: Any module that loads before them breaks the entire app, and in apps with many modules they become a large blocking resource, as the entire map for all possible modules needs to load first.

This feature enables multiple import maps per document, by merging them in a consistent and deterministic way.

[ChromeStatus.com entry](https://chromestatus.com/feature/5121916248260608)

### Storage Access Headers

Offers an alternate way for authenticated embeds to opt in for unpartitioned cookies. These headers indicate whether unpartitioned cookies are (or can be) included in a given network request, and allow servers to activate 'storage-access' permissions they have already been granted. Giving an alternative way to activate the 'storage-access' permission allows usage by non-iframe resources, and can reduce latency for authenticated embeds.

[Tracking bug #329698698](https://issues.chromium.org/issues/329698698) | [ChromeStatus.com entry](https://chromestatus.com/feature/6146353156849664) | [Spec](https://privacycg.github.io/storage-access-headers)

### Support creating `ClipboardItem` with `Promise<DOMString>`

The `ClipboardItem`, which is the input to the async clipboard `write()` method, now accepts string values in addition to Blobs in its constructor. `ClipboardItemData` can be a Blob, a string, or a Promise that resolves to either a Blob or a string.

[Tracking bug #40766145](https://issues.chromium.org/issues/40766145) | [ChromeStatus.com entry](https://chromestatus.com/feature/4926138582040576) | [Spec](https://www.w3.org/TR/clipboard-apis/#typedefdef-clipboarditemdata)

### WebAssembly Memory64

The memory64 proposal adds support for linear WebAssembly memories with size larger than 2^32 bits. It provides no new instructions, but instead extends the existing instructions to allow 64-bit indexes for memories and tables.

[ChromeStatus.com entry](https://chromestatus.com/feature/5070065734516736) | [Spec](https://github.com/WebAssembly/memory64/blob/main/proposals/memory64/Overview.md)

### Web Authentication API: `PublicKeyCredential` `getClientCapabilities()` method

The `PublicKeyCredential` `getClientCapabilities()` method lets you determine which WebAuthn features are supported by the user's client. The method returns a list of supported capabilities, allowing developers to tailor authentication experiences and workflows based on the client's specific functionality.

[Tracking bug #360327828](https://issues.chromium.org/issues/360327828) | [ChromeStatus.com entry](https://chromestatus.com/feature/5128205875544064) | [Spec](https://w3c.github.io/webauthn/#sctn-getClientCapabilities)

### X25519 algorithm of the Web Cryptography API

The "X25519" algorithm provides tools to perform key agreement using the X25519 function specified in [RFC7748]. The "X25519" algorithm identifier can be used in the SubtleCrypto interface to access the implemented operations: generateKey, importKey, exportKey, deriveKey and deriveBits.

[Tracking bug #378856322](https://issues.chromium.org/issues/378856322) | [ChromeStatus.com entry](https://chromestatus.com/feature/6291245926973440) | [Spec](https://w3c.github.io/webcrypto/#x25519)
