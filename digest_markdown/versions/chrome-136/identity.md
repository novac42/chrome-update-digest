---
layout: default
title: Chrome 136 Identity Updates - English
---

# Chrome 136 Identity Updates - English

## Area Summary

Chrome 136 introduces significant enhancements to web identity management, focusing on improved user experience and streamlined authentication flows. The release advances Federated Credential Management (FedCM) with multi-provider support, allowing websites to present multiple identity providers in a unified interface. Additionally, WebAuthn conditional create functionality enables seamless passkey upgrades from existing password credentials. These updates collectively strengthen the web platform's identity ecosystem by reducing friction in authentication processes and promoting modern security practices.

## Detailed Updates

Building on the identity-focused improvements outlined above, Chrome 136 delivers two key features that enhance both developer capabilities and user authentication experiences.

### FedCM updates

#### What's New
FedCM now supports displaying multiple identity providers within a single dialog interface, streamlining the authentication process for users who have accounts with different providers. This update also removes support for "add another account" functionality in FedCM passive mode.

#### Technical Details
Developers can now include multiple identity providers in the same `get()` call, which will be presented to users in a unified interface. This eliminates the need for separate authentication flows for each provider and reduces the complexity of implementing multi-provider authentication scenarios.

#### Use Cases
This feature is particularly valuable for websites that support authentication through multiple identity providers (such as Google, Facebook, Apple, etc.), allowing users to see all available options at once. It simplifies the user experience by consolidating provider selection into a single step, reducing cognitive load and improving conversion rates for authentication flows.

#### References
- [Tracking bug #1348262](https://bugs.chromium.org/p/chromium/issues/detail?id=1348262)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5049732142194688)
- [Spec](https://fedidcg.github.io/FedCM/)

### Web authentication conditional create (passkey upgrades)

#### What's New
WebAuthn conditional create requests enable websites to upgrade existing password-based credentials to passkeys, providing a smooth transition path from traditional authentication to modern passwordless solutions.

#### Technical Details
This functionality allows websites to trigger passkey creation conditionally, typically when a user is signing in with a password. The conditional create mechanism respects user preferences and system capabilities, only prompting for passkey creation when appropriate conditions are met.

#### Use Cases
Ideal for websites looking to gradually migrate users from password-based authentication to passkeys without disrupting existing workflows. This feature enables progressive enhancement of security by allowing users to upgrade their credentials at convenient moments, such as during regular sign-in processes, rather than requiring dedicated setup flows.

#### References
- [Tracking bug #377758786](https://bugs.chromium.org/p/chromium/issues/detail?id=377758786)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5097871013068800)
- [Spec](https://w3c.github.io/webauthn/#enum-credentialmediationrequirement)