---
layout: default
title: Area Summary
---

# Area Summary

Chrome 142 introduces a focused Security-Privacy change that restricts web requests to the user's local network by placing them behind an explicit permission prompt. The main theme is tightening cross-origin access to local IPs and loopback interfaces to reduce inadvertent or malicious local network probing. The most impactful change for developers is the need to handle a new permission flow for requests targeting local addresses or loopback. This advance hardens the web platform by reducing silent access to local resources and intranet hosts.

## Detailed Updates

Below are the Security-Privacy updates in Chrome 142 relevant to developers working with local network access.

### Local network access restrictions

#### What's New
Chrome 142 restricts the ability to make requests to the user's local network, gated behind a permission prompt.

#### Technical Details
A local network request is any request from a public website to a local IP address or loopback, or from a local website (for example, an intranet) to loopback. Gating the ability for web...

#### Use Cases
- Web apps that contact local devices, services, or intranet endpoints will encounter a permission prompt for such requests.
- Developers should detect and handle permission-denied scenarios and surface clear messaging or fallbacks when access to local addresses is blocked.

#### References
- [Tracking bug #394009026](https://issues.chromium.org/issues/394009026)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5152728072060928)  
- [Spec](https://wicg.github.io/local-network-access)

Saved file: digest_markdown/webplatform/Security-Privacy/chrome-142-stable-en.md
