---
layout: default
title: security-privacy
---

## Privacy and security

### Permissions Policy reports for iframes

Introduces a new violation type called "Potential Permissions Policy violation", which will only look at Permissions Policy (including report-only policy) and the allow attribute set in iframes to detect the conflict between Permissions Policy enforced versus permissions propagated to iframes.

**References:** [Tracking bug #40941424](https://bugs.chromium.org/p/chromium/issues/detail?id=40941424) | [ChromeStatus.com entry](https://chromestatus.com/feature/5061997434142720) | [Spec](https://w3c.github.io/webappsec-permissions-policy/#reporting)

### Reduce fingerprinting in Accept-Language header information

Reduces the amount of information the Accept-Language header value string exposes in HTTP requests and in `navigator.languages`. Instead of sending a full list of the user's preferred languages on every HTTP request, Chrome now sends the user's most preferred language in the Accept-Language header.

**References:** [Tracking bug #1306905](https://bugs.chromium.org/p/chromium/issues/detail?id=1306905) | [ChromeStatus.com entry](https://chromestatus.com/feature/5042348942655488)
