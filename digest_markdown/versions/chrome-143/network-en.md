---
layout: default
title: network-en
---

## Area Summary

Chrome 143 (stable) introduces WebTransport Application Protocol Negotiation as the main Network-area update. This enables web applications to offer a list of application protocols during the WebTransport handshake so the server can select an appropriate protocol. The change gives developers explicit, handshake-level control over application protocol selection for WebTransport connections. It advances the web platform by standardizing how application-layer protocols are negotiated over WebTransport, improving interoperability and deployability.

## Detailed Updates

Below are the Network-area details that follow from the summary above.

### WebTransport Application Protocol Negotiation

#### What's New
WebTransport Application Protocol Negotiation allows negotiation of the protocol used by the web application within the WebTransport handshake. A web application can specify a list of application protocols offered when constructing a `WebTransport` object, which are then conveyed to the server during the handshake.

#### Technical Details
- The feature exposes an option on `WebTransport` construction to provide application protocol identifiers that the client offers to the server.
- These offered protocols are transmitted to the server as part of the WebTransport handshake so the server can choose an appropriate application protocol.
- Implementation and specification details are tracked in the linked spec and Chromium tracking bug.

#### Use Cases
- Letting clients advertise supported application protocols so servers can pick the best match at connection time.
- Enabling explicit application-protocol negotiation for services built on top of WebTransport, improving compatibility and deployment choices.
- Supporting scenarios that require different application-layer protocols without separate connection establishment logic.

#### References
- [Tracking bug #416080492](https://issues.chromium.org/issues/416080492)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/6521719678042112)  
- [Spec](https://w3c.github.io/webtransport/#dom-webtransportoptions-protocols)

Saved to: digest_markdown/webplatform/Network/chrome-143-stable-en.md
