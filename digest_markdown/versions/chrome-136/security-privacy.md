---
layout: default
title: Chrome 136 Security-Privacy Updates
---

# Chrome 136 Security-Privacy Updates

## Area Summary

Chrome 136 introduces significant privacy enhancements focused on reducing fingerprinting and improving developer visibility into policy violations. The most impactful change is the reduction of Accept-Language header information, which substantially decreases the fingerprinting surface by limiting language data exposed in HTTP requests. Additionally, new Permissions Policy violation reporting for iframes provides developers with better debugging capabilities for policy conflicts. These updates represent Chrome's continued commitment to strengthening web privacy while maintaining developer tooling quality, advancing the platform toward a more privacy-preserving web ecosystem.

## Detailed Updates

These security and privacy improvements build upon Chrome's ongoing efforts to balance user protection with developer experience, providing both enhanced privacy safeguards and better debugging tools.

### Permissions Policy reports for iframes

#### What's New
Chrome now generates "Potential Permissions Policy violation" reports when there are conflicts between Permissions Policy enforcement and permissions propagated to iframes through the allow attribute.

#### Technical Details
The new violation type specifically examines both regular and report-only Permissions Policy configurations alongside iframe allow attributes to detect mismatches. This reporting mechanism helps identify cases where iframe permissions may not align with the parent document's policy intentions, providing visibility into potential security boundaries that weren't previously monitored.

#### Use Cases
Developers can now debug Permissions Policy configurations more effectively, identifying when iframe allow attributes conflict with parent policies. This is particularly valuable for applications using embedded content or third-party iframes where permission boundaries need careful management. The reports help ensure that security policies are correctly implemented across frame hierarchies.

#### References
- [Tracking bug #40941424](https://bugs.chromium.org/p/chromium/issues/detail?id=40941424)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5061997434142720)
- [Spec](https://w3c.github.io/webappsec-permissions-policy/#reporting)

### Reduce fingerprinting in Accept-Language header information

#### What's New
Chrome now limits the Accept-Language header to only include the user's most preferred language, significantly reducing the fingerprinting information available to websites compared to the previous full language list.

#### Technical Details
Instead of exposing the complete ordered list of user language preferences in HTTP requests and `navigator.languages`, Chrome now sends only the primary language preference in the Accept-Language header. This change reduces the entropy available for browser fingerprinting while maintaining core internationalization functionality for content negotiation.

#### Use Cases
Websites can still perform appropriate content localization using the primary language preference, but with significantly reduced ability to fingerprint users based on their complete language configuration. This is particularly important for privacy-conscious applications and helps comply with anti-fingerprinting requirements while maintaining essential i18n capabilities.

#### References
- [Tracking bug #1306905](https://bugs.chromium.org/p/chromium/issues/detail?id=1306905)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5042348942655488)