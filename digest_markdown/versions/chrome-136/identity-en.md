---
layout: default
title: identity-en
---

## Area Summary

Chrome 136 advances Identity by improving federated sign-in UI and by enabling WebAuthn flows that migrate passwords to passkeys. The FedCM change lets a single get() call surface multiple identity providers in one dialog and removes "add another account" in passive mode. WebAuthn conditional create (passkey upgrades) lets sites upgrade existing password credentials to passkeys, simplifying migration. These updates reduce authentication friction and help developers move users toward stronger, phishing-resistant credentials.

## Detailed Updates

The items below expand on the summary and explain practical developer impact and technical notes.

### FedCM updates

#### What's New
FedCM can present multiple identity providers in the same dialog when all providers are returned in a single get() call. Chrome 136 also removes support for "add another account" in FedCM passive mode.

#### Technical Details
- A single FedCM get() call can include multiple providers so the browser UI can show them together.
- Passive-mode behavior was tightened by removing the "add another account" flow (details and rationale in linked tracking bug).

#### Use Cases
- Sites that support multiple federated IdPs can present a unified selection UI without multiple round trips.
- Simplifies implementing multi-provider sign-up/sign-in flows and reduces UX fragmentation.

#### References
- Tracking bug #1348262: https://bugs.chromium.org/p/chromium/issues/detail?id=1348262
- ChromeStatus.com entry: https://chromestatus.com/feature/5049732142194688
- Spec: https://fedidcg.github.io/FedCM/

### Web authentication conditional create (passkey upgrades)

#### What's New
WebAuthn conditional create requests enable websites to upgrade existing password credentials to passkeys.

#### Technical Details
- Conditional create is a WebAuthn mediation mode that lets the user agent offer authenticator creation in context, enabling credential upgrade flows from passwords to passkeys (see tracking bug and spec links).

#### Use Cases
- Gradual migration of user accounts from password-based authentication to passkeys with lower user friction.
- Implement in account settings or sign-in flows to prompt users to create a passkey when a password credential is detected.

#### References
- Tracking bug #377758786: https://bugs.chromium.org/p/chromium/issues/detail?id=377758786
- ChromeStatus.com entry: https://chromestatus.com/feature/5097871013068800
- Spec: https://w3c.github.io/webauthn/#enum-credentialmediationrequirement
