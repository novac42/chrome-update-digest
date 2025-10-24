---
layout: default
title: security-privacy-en
---

## Area Summary

Chrome 137 fixes a WebAuthn error-type mismatch for payment credential creation, aligning runtime behavior with the WebAuthn specification. The change converts a previously thrown SecurityError into a NotAllowedError when creating a payment credential in a cross-origin iframe without user activation. This improves interoperability and makes error handling more predictable for developers implementing payment and authentication flows across frames. Developers should review error handling and tests for cross-origin payment WebAuthn scenarios to avoid misclassifying failures.

## Detailed Updates

The single Security-Privacy update below follows from the summary above and focuses on making WebAuthn error semantics consistent with the spec.

### Align error type thrown for payment WebAuthn credential creation: SecurityError becomes NotAllowedError

#### What's New
Creating a payment credential in a cross-origin iframe without a user activation now throws NotAllowedError instead of SecurityError, matching the WebAuthn spec.

#### Technical Details
This corrects a historical specification mismatch: the runtime now reports the error type the spec requires for this scenario. The change affects the WebAuthn credential creation path for payment credentials when invoked from a cross-origin iframe and lacking user activation.

#### Use Cases
- Payment integrations that create WebAuthn credentials in iframes should update error handling to expect NotAllowedError for user-activation-related failures.
- Automated tests and error classification logic should be adjusted so that these cases aren’t treated as broader security-policy violations.

#### References
- Tracking bug #41484826: https://bugs.chromium.org/p/chromium/issues/detail?id=41484826  
- ChromeStatus.com entry: https://chromestatus.com/feature/5096945194598400  
- Spec: https://w3c.github.io/webauthn/#sctn-creating-a-credential
