## Security

### Local network access restrictions

Chrome 142 restricts the ability to make requests to the user's local network, gated behind a permission prompt.

A local network request is any request from a public website to a local IP address or loopback, or from a local website (for example, an intranet) to loopback. Gating the ability for websites to perform these requests behind a permission mitigates the risk of cross-site request forgery attacks against local network devices such as routers, and reduces the ability of sites to use these requests to fingerprint the user's local network.

This permission is restricted to secure contexts. If granted, the permissions additionally relaxes mixed content blocking for local network requests (since many local devices are not able to obtain publicly trusted TLS certificates for various reasons).

Learn more in [New permission prompt for Local Network Access](/blog/local-network-access).

[Tracking bug #394009026](https://issues.chromium.org/issues/394009026) | [ChromeStatus.com entry](https://chromestatus.com/feature/5152728072060928) | [Spec](https://wicg.github.io/local-network-access)
