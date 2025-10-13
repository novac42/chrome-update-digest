## Security

### Strict Same Origin Policy for Storage Access API

Adjusts the Storage Access API semantics to strictly follow the Same Origin Policy with regard to security. That is, using `document.requestStorageAccess()` in a frame only attaches cookies to requests to the iframe's origin (not site) by default.

**Note:** The `CookiesAllowedForUrls` policy or Storage Access Headers may still be used to unblock cross-site cookies.

[Tracking bug #379030052](https://issues.chromium.org/issues/379030052) | [ChromeStatus.com entry](https://chromestatus.com/feature/5169937372676096) | [Spec](https://github.com/privacycg/storage-access/pull/213)

### Signature-based Integrity

This feature provides web developers with a mechanism to verify the provenance of resources they depend upon, creating a technical foundation for trust in a site's dependencies. In short: servers can sign responses with a Ed25519 key pair, and web developers can require the user agent to verify the signature using a specific public key. This offers a helpful addition to URL-based checks offered by Content Security Policy on the one hand, and Subresource Integrity's content-based checks on the other.

[Tracking bug #375224898](https://issues.chromium.org/issues/375224898) | [ChromeStatus.com entry](https://chromestatus.com/feature/5032324620877824) | [Spec](https://wicg.github.io/signature-based-sri)
