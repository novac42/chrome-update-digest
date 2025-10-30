---
layout: default
title: chrome-142-en
---

## Area Summary

Chrome 142 tightens how JSON module imports are validated by enforcing stricter MIME token rules when matching `*+json`. The change rejects JSON module script responses whose MIME type's type or subtype contain non-HTTP token code points (for example, spaces), improving interoperability with other engines and aligning Chrome with the MIME Sniffing specification. For developers, the most impactful effect is that misconfigured servers sending malformed MIME types will cause JSON module imports to fail, prompting fixes to server headers. Overall, this advances platform consistency and reduces ambiguity in module loading behavior.

## Detailed Updates

This section expands the summary into actionable detail for JavaScript developers and platform engineers.

### Stricter `*+json` MIME token validation for JSON modules

#### What's New
Chrome now rejects JSON module script responses when the MIME type's type or subtype contains non-HTTP token code points while matching `*+json`. This makes JSON module MIME handling stricter and spec-compliant.

#### Technical Details
When matching the `*+json` pattern, the browser validates that both the type and subtype are composed of valid HTTP token code points. If either part contains invalid characters (e.g., spaces), the response is rejected for JSON module scripts. This behavior follows the MIME Sniffing specification and aligns Chrome with other engines under the Interop2025 modules effort.

#### Use Cases
- Ensures consistent module import behavior across browsers by rejecting malformed MIME types.
- Helps surface server misconfigurations early: developers should ensure server Content-Type headers use valid token characters for type/subtype.
- Improves security and interoperability for systems delivering JSON modules.

#### References
- [Tracking bug #440128360](https://issues.chromium.org/issues/440128360)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5182756304846848)  
- [Spec](https://mimesniff.spec.whatwg.org/#parse-a-mime-type)

Save as: digest_markdown/webplatform/JavaScript/chrome-142-stable-en.md
