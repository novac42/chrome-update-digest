---
layout: default
title: network-en
---

## Area Summary

Chrome 142 introduces a focused security change that restricts web-origin requests to the user's local network by gating them behind a permission prompt. The main trend is tighter control over cross-origin access to local and loopback IPs to reduce unwanted device probing and information leakage. For developers, the most impactful change is that requests from public sites to local IPs (and from local sites to loopback) may now require explicit user permission, which can affect device discovery, admin consoles, and LAN-based integrations. This advances the web platform by standardizing user-consent semantics for local-network access and aligning browser behavior with the WICG local-network-access specification.

## Detailed Updates

Below are the specific Network-area updates and what development teams should plan for based on the summary above.

### Local network access restrictions

#### What's New
Chrome 142 restricts the ability to make requests to the user's local network and loopback addresses; such requests are now gated behind a permission prompt.

#### Technical Details
A "local network request" is defined as any request from a public website to a local IP address or loopback, or from a local website (for example, an intranet) to loopback. The browser will present a permission prompt to the user before allowing these cross-boundary requests. The behavior follows the WICG "local-network-access" specification; see tracking and status links for implementation progress.

#### Use Cases
- Web apps that discover or control LAN devices (IoT, printers, cameras) must handle denied permissions and provide fallback UX or alternative connection flows.
- Intranet and admin tools that rely on loopback access should detect and surface a permissions request, and document required user actions.
- Testing and CI environments that simulate local-device interactions may need configuration changes to grant permissions or run with policies that allow local-network access.

#### References
- [Tracking bug #394009026](https://issues.chromium.org/issues/394009026)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5152728072060928)  
- [Spec](https://wicg.github.io/local-network-access)
