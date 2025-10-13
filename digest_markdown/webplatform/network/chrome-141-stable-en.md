## Area Summary

Chrome 141’s Network updates center on tightening security for local network access by introducing permission-gated requests. The most impactful change is a restriction on initiating requests to a user’s local network, paired with an origin trial that temporarily permits access from non-secure contexts. This shift advances the web platform by reinforcing security and privacy boundaries around local resources while providing developers a transition path. These updates matter because they affect how applications discover or communicate with devices and services on local networks, especially during development or in legacy non-secure deployments.

## Detailed Updates

This release emphasizes secure-by-default local network access while offering a temporary origin trial to reduce breakage and provide migration time.

### Local network access restrictions

#### What's New
- Chrome 141 restricts the ability to make requests to the user’s local network, gated behind a permission prompt.
- An origin trial temporarily allows access to local network resources from non-secure contexts to provide developers more time to adjust.

#### Technical Details
- Access to local network endpoints now requires explicit user permission via a prompt.
- A time-limited origin trial enables continued access from non-secure contexts, allowing staged migration toward secure contexts and updated network access patterns.

#### Use Cases
- Sites that contact services or devices on a user’s local network and need to continue functioning while migrating to secure setups.
- Applications transitioning from non-secure contexts that require temporary access to local resources during development or phased rollouts.

#### References
- Tracking bug #394009026: https://issues.chromium.org/issues/394009026
- ChromeStatus.com entry: https://chromestatus.com/feature/5152728072060928
- Spec: https://wicg.github.io/local-network-access