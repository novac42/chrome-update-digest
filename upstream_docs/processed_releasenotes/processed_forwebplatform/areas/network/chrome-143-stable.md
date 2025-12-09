## Network

### WebTransport Application Protocol Negotiation

WebTransport Application Protocol Negotiation allows negotiation of the protocol used by the web application within the WebTransport handshake.

A web application can specify a list of application protocols offered when constructing a `WebTransport` object, which are then conveyed to the server using HTTP headers; if the server picks one of those protocols, it can indicate that within response headers, and that reply is available within the WebTransport object.

[Tracking bug #416080492](https://issues.chromium.org/issues/416080492) | [ChromeStatus.com entry](https://chromestatus.com/feature/6521719678042112) | [Spec](https://w3c.github.io/webtransport/#dom-webtransportoptions-protocols)
