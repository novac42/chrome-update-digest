## Origin trials

### Digital Credential API

Websites can and do get credentials from mobile wallet apps through a variety of mechanisms today, for example, custom URL handlers and QR code scanning. This feature lets sites request identity information from wallets using Android's `IdentityCredential` `CredMan` system. It is extensible to support multiple credential formats (for example, ISO mDoc and W3C verifiable credential) and allows multiple wallet apps to be used. Mechanisms are being added to help reduce the risk of ecosystem-scale abuse of real-world identity.

The origin trial starting in Chrome 134 adds support for this API on desktop platform, where Chrome on Desktop will securely communicate with the digital wallet on the Android phone to fetch the requested credentials.

[Origin Trial](/origintrials#/view_trial/3139571890230657025) | [Tracking bug #40257092](https://issues.chromium.org/issues/40257092) | [ChromeStatus.com entry](https://chromestatus.com/feature/5166035265650688) | [Spec](https://wicg.github.io/digital-credentials)

### Deprecation trial for `SelectParserRelaxation`

This is a deprecation trial, which re-enables the old parser behavior for parsing `<select>` tags. Under that old behavior, non-supported content is silently discarded and not included in the DOM content underneath the `<select>`. This trial can be used in case the new behavior enabled from Chrome 135 breaks a site.

[Origin Trial](/origintrials#/view_trial/182958734861926401) | [ChromeStatus.com entry](https://chromestatus.com/feature/5145948356083712)
