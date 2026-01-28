---
layout: default
title: chrome-143-en
---

## Area Summary

Chrome 143 (stable) introduces a Web Smart Card API targeted to Isolated Web Apps (IWA). The core theme is enabling smart card (PC/SC) applications to migrate to the Web platform by granting IWAs access to the host OS PC/SC stack and card reader drivers. Administrators can control the API’s availability (source content truncated for details). This update advances the platform by bridging native smart‑card hardware and web-deployed isolated apps, improving options for hardware-backed authentication and enterprise migration paths.

## Detailed Updates

Below are the isolated-web-apps changes that follow from the summary above.

### Web Smart Card API for Isolated Web Apps

#### What's New
Enables smart card (PC/SC) applications to move to the Web platform for Isolated Web Apps, providing access to the host OS PC/SC implementation and card reader drivers.

#### Technical Details
- Available only to Isolated Web Apps (IWA).
- Grants IWAs access to the PC/SC implementation and the card reader drivers present on the host operating system.
- Administrators can control the availability of this API (source content is truncated and does not include the full admin configuration details).

#### Use Cases
- Allows migration of existing PC/SC smart card applications to run as IWAs while maintaining access to host smart‑card infrastructure.
- Supports scenarios where web apps need direct access to OS-level smart card services without exposing the API to non-isolated contexts.

#### References
- [Tracking bug #1386175](https://issues.chromium.org/issues/1386175)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/6411735804674048)  
- [Spec](https://wicg.github.io/web-smart-card)

Saved file: digest_markdown/webplatform/Isolated Web Apps/chrome-143-stable-en.md