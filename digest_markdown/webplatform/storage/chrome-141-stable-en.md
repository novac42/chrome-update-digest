digest_markdown/webplatform/storage/chrome-141-stable-en.md

## Area Summary

Chrome 141 (stable) advances storage privacy by enforcing strict Same Origin Policy semantics in the Storage Access API. The key change scopes cookie attachment granted via document.requestStorageAccess() to the exact iframe origin, not the broader site. This strengthens cross-origin isolation, reduces unintended cookie sharing, and makes embedded storage behavior more predictable. Developers embedding third-party content should validate cookie assumptions and adjust integration patterns to align with origin-bound access.

## Detailed Updates

This release focuses on tightening origin boundaries for storage access to improve privacy and predictability for embedded contexts.

### Strict Same Origin Policy for Storage Access API

#### What's New
Adjusts the Storage Access API semantics to strictly follow the Same Origin Policy with regard to security. Using document.requestStorageAccess() in a frame only attaches cookies to requests to the iframe’s origin (not site) by default.

#### Technical Details
- Storage access grants now apply at the origin level, aligning with Same Origin Policy.
- In embedded frames, cookie attachment resulting from document.requestStorageAccess() is limited to requests targeting the iframe’s exact origin.
- This reduces cross-site cookie exposure and standardizes behavior for third-party frames.

#### Use Cases
- Embedding third-party content that requires cookies while minimizing cross-site leakage.
- Implementations needing predictable, origin-scoped cookie behavior in iframes.
- Auditing integrations that previously relied on site-level cookie attachment to ensure compatibility with origin-only scoping.

#### References
- Tracking bug #379030052: https://issues.chromium.org/issues/379030052
- ChromeStatus.com entry: https://chromestatus.com/feature/5169937372676096
- Spec: https://github.com/privacycg/storage-access/pull/213