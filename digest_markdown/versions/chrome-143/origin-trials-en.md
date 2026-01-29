---
layout: default
title: Chrome 143 Origin Trials
---

# Chrome 143 Origin Trials

## Area Summary

Chrome 143 introduces two significant origin trials that expand the web platform's capabilities in credential management and application installation. The Digital Credentials API gains issuance support, enabling secure provisioning of digital credentials from issuing authorities directly into user wallets through native credential management systems. The Web Install API debuts, providing websites with the ability to programmatically install web applications either from their own origin or cross-origin, advancing the installation experience beyond traditional manual flows. Both features represent important steps in bridging web and native platform capabilities while maintaining security and privacy standards through the origin trial program.

## Detailed Updates

These origin trials enable new patterns for credential issuance and application installation that were previously unavailable on the web platform.

### Digital Credentials API (issuance support)

#### What's New

This feature enables issuing websites such as universities, government agencies, or banks to securely initiate the provisioning process of digital credentials directly into a user's mobile wallet application. The API provides a standardized way to issue credentials from the web to native credential storage systems.

#### Technical Details

The implementation leverages platform-specific credential management systems for secure storage. On Android, it uses the Android `IdentityCredential` CredMan system (Credential Manager), which provides system-level credential storage and management. On Desktop platforms, the feature uses cross-device approaches through the CTAP (Client to Authenticator Protocol), similar to how Digital Credentials presentation works. This architecture ensures that credentials are issued securely while maintaining compatibility across different device types and operating systems.

#### Use Cases

This API enables critical use cases for digital identity and credentials:
- Universities can issue digital student IDs and diplomas directly to student devices
- Government agencies can provision digital driver's licenses, national IDs, and other official documents
- Banks and financial institutions can issue digital payment credentials, account access tokens, and verification credentials
- Healthcare providers can distribute digital health cards and vaccination records

The API standardizes what was previously a fragmented landscape of proprietary credential issuance mechanisms, making it easier for developers to build cross-platform credential solutions.

#### References

- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/385620718093598721)
- [Tracking bug #378330032](https://issues.chromium.org/issues/378330032)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5099333963874304)
- [Spec](https://w3c-fedid.github.io/digital-credentials)

### Web Install API

#### What's New

The Web Install API provides websites with the ability to programmatically install web applications. When invoked, the API can install either the calling website itself or another site from a different origin as a web app, depending on the provided parameters. This represents a significant advancement in web app installation capabilities.

#### Technical Details

The API extends the existing web app manifest specification with new installation capabilities. The feature supports both same-origin and cross-origin installation scenarios, allowing for flexible installation patterns. When a website invokes the API, it triggers the browser's web app installation flow programmatically rather than requiring users to manually discover and use browser-specific installation UI. The API respects all existing web app manifest configurations and security policies, ensuring that programmatic installation maintains the same security guarantees as manual installation.

#### Use Cases

This API enables several important installation patterns:
- App stores and catalog sites can install web apps from other origins, creating web-native app distribution platforms
- Websites can provide prominent "Install App" buttons that directly trigger installation without requiring users to find browser menus
- Progressive Web App onboarding flows can programmatically install the app at optimal moments in the user journey
- Cross-promotion between related web apps becomes possible, where one app can recommend and install another

The API is particularly valuable for improving web app discoverability and reducing friction in the installation process, which has been a key challenge for PWA adoption.

#### References

- [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/2367204554136616961)
- [Tracking bug #333795265](https://issues.chromium.org/issues/333795265)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5183481574850560)
- [Spec](https://github.com/w3c/manifest/pull/1175)
