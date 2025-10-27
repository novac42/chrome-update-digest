---
layout: default
title: chrome-134-en
---

## Area Summary

Chrome 134's Origin Trials focus on two targeted experiments: introducing a Digital Credential API origin trial and running a deprecation trial to restore legacy `<select>` parsing behavior. The Digital Credential API trial lets sites request identity information from mobile wallet apps using Android's IdentityCredential / CredMan system, enabling web-native credential flows. The deprecation trial for SelectParserRelaxation offers a temporary opt-in to the old parser behavior for `<select>` elements to help sites that depend on legacy parsing. Together these trials help developers adopt emerging secure credential integrations while providing a controlled migration path for parser-related regressions.

## Detailed Updates

The items below expand on the summary above and describe the practical implications for developers participating in these origin trials.

### Digital Credential API

#### What's New
Websites can request identity information from mobile wallet apps via an origin trial implementing the Digital Credential API; the feature leverages Android's IdentityCredential / CredMan system and is extensible.

#### Technical Details
The trial exposes a web-facing API that connects sites to mobile wallet credentials rather than relying on ad-hoc mechanisms (custom URL handlers, QR scanning). Implementation notes present in the trial reference Android's IdentityCredential and CredMan integration and point to the WICG spec for API semantics.

#### Use Cases
- Seamless credential retrieval from user wallets for login or identity verification flows.
- Replacing bespoke wallet integrations (QR, URL handlers) with a standardized web API.
- Testing interoperability with Android wallet implementations before broader rollout.

#### References
- [Tracking bug #40257092](https://issues.chromium.org/issues/40257092)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5166035265650688)  
- [Spec](https://wicg.github.io/digital-credentials)

### Deprecation trial for `SelectParserRelaxation`

#### What's New
A deprecation origin trial re-enables the old `<select>` parser behavior, where unsupported content is silently discarded and not included under the `<select>` in the DOM.

#### Technical Details
This trial toggles parser behavior to the legacy mode for `<select>` elements to mitigate breakage from the newer parsing semantics. The trial is intended as a temporary compatibility measure for sites affected by the behavioral change introduced in recent Chrome versions.

#### Use Cases
- Short-term mitigation for sites that rely on the legacy `<select>` parsing semantics.
- Provides time to update server- or authoring-side markup to conform to the newer parser behavior.
- Useful in testing and rollout plans to determine compatibility impacts before full deprecation.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5145948356083712)
