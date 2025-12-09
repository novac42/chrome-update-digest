## Area Summary

Chrome 143's Origin Trials focus on testing platform integrations that let websites perform privileged actions with stronger user intent and secure interactions. The two trials here enable credential issuance into mobile wallets and a flexible Web Install API for installing web apps (including cross-origin installs). These experiments advance the web platform by bridging web apps with native credential stores and by simplifying app distribution flows, while requiring careful attention to security and user consent. Developers should register for the trials and evaluate UX, platform compatibility, and threat models before shipping.

## Detailed Updates

Below are the origin-trial features in Chrome 143 that developers should evaluate and prototype against.

### Digital Credentials API (issuance support)

#### What's New
This origin trial lets issuing websites (for example, a university, government agency, or bank) securely initiate the provisioning (issuance) process of digital credentials directly into a user's mobile wallet application. On Android, this capability uses the Android `IdentityCredential` CredMan system.

#### Technical Details
- Issuers can start the issuance/provisioning flow from the web to a mobile wallet-backed credential store.
- Platform integration on Android leverages the IdentityCredential/CredMan subsystem.
- Importance: medium — intended for controlled testing and feedback via the origin trial.

#### Use Cases
- Universities, governments, or banks issuing verifiable credentials to users' mobile wallets.
- Web workflows that need to enroll users into platform-backed credentials without separate native apps.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/385620718093598721)
- [Tracking bug #378330032](https://issues.chromium.org/issues/378330032)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5099333963874304)
- [Spec](https://w3c-fedid.github.io/digital-credentials)

### Web Install API

#### What's New
Provides the ability to install a web app. When invoked, the website installs either itself, or another site from a different origin, as a web app (depending on the provided parameters).

#### Technical Details
- The API exposes an installation flow callable from web contexts, with parameters that can target the current origin or a different origin for installation.
- Designed for experimentation under an origin trial to validate security, UX, and cross-origin installation semantics.
- Importance: medium — allows testing of new install UX and distribution models.

#### Use Cases
- Simplifying PWA installation prompts from the originating site or a partner origin.
- Enterprise or curated stores initiating installs of third-party web apps with user consent.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/2367204554136616961)
- [Tracking bug #333795265](https://issues.chromium.org/issues/333795265)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5183481574850560)
- [Spec](https://github.com/w3c/manifest/pull/1175)

Saved file: digest_markdown/webplatform/Origin trials/chrome-143-stable-en.md