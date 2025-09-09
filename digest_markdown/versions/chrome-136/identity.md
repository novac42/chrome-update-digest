---
layout: default
title: identity
---

## Identity

### FedCM updates

Allows FedCM to show multiple identity providers in the same dialog, by having all providers in the same `get()` call. This provides developers with a convenient way to present all supported identity providers to users. Chrome 136 also removes support for add another account in FedCM passive mode. This feature allows showing a use another account button alongside other IdP accounts in the chooser. The feature is currently unused, and UX conversations have led us to believe that supporting this leads to a more complicated flow without much benefit. This feature will still work in FedCM active mode.

**References:** [Tracking bug #1348262](https://bugs.chromium.org/p/chromium/issues/detail?id=1348262) | [ChromeStatus.com entry](https://chromestatus.com/feature/5049732142194688) | [Spec](https://fedidcg.github.io/FedCM/)

### Web authentication conditional create (passkey upgrades)

WebAuthn conditional create requests let websites upgrade existing password credentials to a passkey.

**References:** [Tracking bug #377758786](https://bugs.chromium.org/p/chromium/issues/detail?id=377758786) | [ChromeStatus.com entry](https://chromestatus.com/feature/5097871013068800) | [Spec](https://w3c.github.io/webauthn/#enum-credentialmediationrequirement)
