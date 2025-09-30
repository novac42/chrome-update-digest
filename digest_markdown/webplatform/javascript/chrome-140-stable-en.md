## Area Summary

Chrome 140 stable introduces two focused JavaScript-area changes: built-in conversion between Uint8Array and base64/hex representations, and an adjustment to the view transition finished promise timing. The Uint8Array conversion feature reduces the need for custom utilities for binary ↔ text encoding, improving interoperability and developer ergonomics. The view transition timing change targets a visual flicker caused by promise resolution ordering, improving animation robustness and perceived performance. Both updates tighten platform primitives so developers can rely less on ad-hoc workarounds.

## Detailed Updates

Below are concise, developer-focused breakdowns of each JavaScript-area change and why they matter.

### `Uint8Array` to and from base64 and hex

#### What's New
Adds the ability and methods to convert between Uint8Array binary data and base64/hex text encodings.

#### Technical Details
This feature standardizes conversion APIs for binary <-> textual encodings; see the language-level spec for exact method shapes and semantics.

#### Use Cases
- Encoding binary data for transport or storage (e.g., embedding images, sending compact payloads).
- Decoding base64/hex payloads into typed arrays for processing with Web APIs (crypto, WebAssembly, fetch response handling).
- Reduces dependency on utility libraries and custom encoder/decoder code paths.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/6281131254874112  
- Spec: https://tc39.es/proposal-arraybuffer-base64/spec

### View transition finished promise timing change

#### What's New
The timing for the view transition finished promise has been changed to address cases where promise resolution occurs inside rendering lifecycle steps and causes a visible flicker at the end of the animation.

#### Technical Details
The adjustment targets when the finished promise resolves relative to the rendering lifecycle so that scripts reacting to completion do not run after the visual frame that removes the view transition, avoiding an end-of-animation visual glitch.

#### Use Cases
- Smoother view transition flows where post-transition scripts manipulate DOM or styles.
- Reliable animation endpoints for frameworks and libraries that await the finished promise before performing final layout or cleanup.
- Reduces need for fragile timing hacks and forceful reflows to avoid flicker.

#### References
- Tracking bug #430018991: https://issues.chromium.org/issues/430018991  
- ChromeStatus.com entry: https://chromestatus.com/feature/5143135809961984

Saved file path: digest_markdown/webplatform/JavaScript/chrome-140-stable-en.md