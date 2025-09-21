# Chrome 136 Stable Release - Web API Analysis

## Area Summary

Chrome 136 introduces significant enhancements to Web API functionality, focusing on developer productivity, security improvements, and platform consistency. Key highlights include the new `RegExp.escape` utility for safer regular expression handling, pointer event improvements for better touch interactions, and JavaScript compilation optimizations through explicit compile hints. The release also strengthens security with HTTP cache partitioning updates and enhances performance tracking capabilities with ProgressEvent improvements. These updates collectively advance the web platform by providing developers with more precise control over application behavior while maintaining backwards compatibility.

## Detailed Updates

This release brings several important Web API enhancements that improve both developer experience and application security, ranging from fundamental JavaScript utilities to advanced performance optimizations.

### RegExp.escape

#### What's New
A new static method `RegExp.escape` that safely escapes strings for use as regular expression patterns, eliminating the need for manual escaping and reducing security vulnerabilities.

#### Technical Details
The method takes any string input and returns a version with all special regex characters properly escaped. This ensures that user input or dynamic content can be safely incorporated into regular expressions without unintended pattern matching behavior.

#### Use Cases
Essential for applications that construct regular expressions from user input, search functionality, and template systems. Particularly valuable for preventing regex injection attacks and ensuring predictable pattern matching behavior.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5074350768316416)
- [Spec](https://tc39.es/proposal-regex-escaping/)

### Dispatch click events to captured pointer

#### What's New
Click events are now correctly dispatched to captured pointer targets when pointer capture is active during the `pointerup` event, aligning Chrome's behavior with the UI Event specification.

#### Technical Details
When `setPointerCapture()` is called during pointer interaction, subsequent click events will be sent to the captured element rather than following the default targeting logic. This ensures consistent event handling across different interaction patterns.

#### Use Cases
Critical for drag-and-drop interfaces, custom UI controls, and touch-based applications where precise event targeting is required. Improves reliability of pointer-based interactions in complex web applications.

#### References
- [Tracking bug #40851596](https://bugs.chromium.org/p/chromium/issues/detail?id=40851596)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5045063816396800)
- [Spec](https://w3c.github.io/uievents/#event-type-click)

### Update ProgressEvent to use double type for loaded and total

#### What's New
The `loaded` and `total` attributes of ProgressEvent now use the `double` type instead of `unsigned long long`, providing more precise progress reporting capabilities.

#### Technical Details
This change allows for fractional progress values and removes the limitation of integer-only progress reporting. Developers can now report progress with decimal precision, enabling more accurate progress indicators.

#### Use Cases
Beneficial for file upload/download progress bars, streaming operations, and any scenario requiring fine-grained progress reporting. Particularly useful for large file transfers where byte-level precision matters.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5084700244254720)
- [Spec](https://xhr.spec.whatwg.org/#interface-progressevent)

### Explicit compile hints with magic comments

#### What's New
JavaScript files can now include magic comments that provide hints to the V8 engine about which functions should be eagerly parsed and compiled, optimizing initial load performance.

#### Technical Details
Developers can annotate their JavaScript code with special comments that guide the compilation process. This allows for more intelligent resource allocation during script parsing and can reduce initial execution delays for critical code paths.

#### Use Cases
Valuable for large JavaScript applications where selective compilation can improve startup performance. Particularly useful for frameworks, libraries, and applications with complex initialization sequences.

#### References
- [Tracking bug #13917](https://bugs.chromium.org/p/chromium/issues/detail?id=13917)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5047772830048256)
- [Spec](https://github.com/v8/v8/wiki/Design-Elements#compile-hints)

### Incorporate navigation initiator into the HTTP cache partition key

#### What's New
Chrome's HTTP cache now includes navigation initiator information in its partitioning scheme to prevent cross-site timing attacks through top-level navigation cache probing.

#### Technical Details
The cache key now includes an `is-cross-site-main-frame-navigation` boolean that isolates cache entries based on navigation context. This prevents attackers from using cache timing to infer information about user's browsing history across different sites.

#### Use Cases
Enhances privacy and security for all web applications by preventing sophisticated timing-based attacks. Particularly important for applications handling sensitive data or operating in high-security environments.

#### References
- [Tracking bug #398784714](https://bugs.chromium.org/p/chromium/issues/detail?id=398784714)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5108419906535424)
- [Spec](https://httpwg.org/specs/rfc9110.html#caching)

### Speculation rules: tag field

#### What's New
Speculation rules can now include an optional `tag` field that allows developers to categorize and track different sources of preloading hints, with tags sent via the `Sec-Speculation-Tags` header.

#### Technical Details
The tag field enables better analytics and debugging of speculation rule performance by allowing developers to identify which rules are being triggered and how they perform. Tags are automatically included in relevant HTTP headers for server-side processing.

#### Use Cases
Essential for performance optimization teams tracking the effectiveness of different preloading strategies. Useful for A/B testing speculation rules and understanding navigation patterns in complex applications.

#### References
- [Tracking bug #381687257](https://bugs.chromium.org/p/chromium/issues/detail?id=381687257)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5100969695576064)
- [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-tag)

### Protected audience: text conversion helpers

#### What's New
Protected Audience bidding and scoring scripts now have access to specialized helper functions for efficiently converting between strings and byte arrays when interfacing with WebAssembly modules.

#### Technical Details
These functions, `protectedAudience.textEncoder` and related utilities, provide optimized pathways for data conversion in privacy-preserving advertising contexts. They're specifically designed to work efficiently with WebAssembly's memory model.

#### Use Cases
Critical for advertisers and publishers implementing Privacy Sandbox APIs with WebAssembly components. Enables more efficient ad auction processing while maintaining privacy guarantees.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5099738574602240)