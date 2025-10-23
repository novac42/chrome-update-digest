---
layout: default
title: security-privacy-en
---

## Area Summary

Chrome 141’s Security-Privacy updates tighten cross-origin cookie handling and introduce a provenance-based trust model for web resources. The Storage Access API now adheres strictly to Same Origin Policy, limiting cookie attachment to the exact iframe origin by default, which reduces unintended third-party cookie exposure. Signature-based Integrity adds cryptographic verification of dependencies, letting sites require the browser to validate responses signed with Ed25519 keys. Together, these changes raise the security baseline, reduce supply-chain risk, and give developers clearer, more predictable primitives for secure embedding and dependency management.

## Detailed Updates

These updates focus on stronger origin boundaries for storage and cryptographic assurances for subresources, guiding developers toward safer integration patterns.

### Strict Same Origin Policy for Storage Access API

#### What's New
The Storage Access API now strictly follows Same Origin Policy semantics: using document.requestStorageAccess() in a frame only attaches cookies to requests to that iframe’s origin (not the broader site) by default.

#### Technical Details
- Cookie attachment after requestStorageAccess() is origin-scoped for the embedding frame.
- This narrows behavior from site-level to origin-level, reducing cross-origin cookie bleed.
- Developers relying on cookies for cross-origin subresources within an embedded frame must ensure those requests target the exact iframe origin or adjust policy as appropriate.

#### Use Cases
- Embedded authentication or account widgets that require cookies must align subresource requests with the iframe origin.
- Third-party embeds gain stricter isolation, lowering risk of unintended cookie exposure across related but distinct origins.
- Sites can audit iframe resource graphs to ensure cookie-dependent requests are origin-matching.

#### References
- https://issues.chromium.org/issues/379030052
- https://chromestatus.com/feature/5169937372676096
- https://github.com/privacycg/storage-access/pull/213

### Signature-based Integrity

#### What's New
Servers can sign responses with an Ed25519 key pair, and developers can require the user agent to verify those signatures for dependent resources, establishing cryptographic provenance for site dependencies.

#### Technical Details
- Responses are signed using Ed25519; the browser verifies the signature before accepting the resource when required by the page.
- This provides a cryptographic trust anchor independent of the delivery channel (for example, CDN or cache).
- It complements existing integrity checks by tying resources to an authorized signer rather than only to a hash.

#### Use Cases
- Protect against supply-chain attacks on third-party scripts, WASM modules, styles, and other critical assets.
- Safely consume CDN-hosted assets by validating that they originate from an expected signer.
- Strengthen deployment pipelines where assets traverse untrusted intermediaries.

#### References
- https://issues.chromium.org/issues/375224898
- https://chromestatus.com/feature/5032324620877824
- https://wicg.github.io/signature-based-sri
