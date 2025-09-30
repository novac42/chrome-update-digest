### 1. Area Summary

Chrome 139 introduces focused improvements to Secure Payment Confirmation (SPC) that simplify feature detection and strengthen cryptographic device-binding for payments. The most impactful changes for developers are a new JavaScript availability API that avoids constructing a full PaymentRequest just to check SPC support, and browser-bound keys that add a non-synced cryptographic signature to SPC assertions. Together these changes advance the web payments platform by improving developer ergonomics for capability detection and by raising the security posture for device-bound payment credentials. These updates matter because they reduce integration friction and help sites meet stronger device-binding and fraud-resistance requirements.

## Detailed Updates

Below are the Payment-specific updates in Chrome 139 that follow from the summary above.

### The `securePaymentConfirmationAvailability` API

#### What's New
A small JavaScript API to check whether Secure Payment Confirmation (SPC) is available without creating a PaymentRequest.

#### Technical Details
- Exposes an explicit availability check for SPC so callers do not need to construct PaymentRequest objects and parameters just to detect support.
- Reduces the previous clunky flow where feature detection required building and querying a PaymentRequest.

#### Use Cases
- Progressive enhancement: conditionally enable SPC UX only when available.
- Performance and UX: avoid creating and tearing down PaymentRequest instances solely for capability checks.
- Cleaner feature-detection logic in payment flows and integrations.

#### References
- https://issues.chromium.org/issues/40258712
- https://chromestatus.com/feature/5165040614768640
- https://github.com/w3c/secure-payment-confirmation/pull/285

### Secure Payment Confirmation: Browser Bound Keys

#### What's New
Adds an additional cryptographic signature over SPC assertions and credential creation where the corresponding private key is browser-bound and not synced across devices.

#### Technical Details
- Introduces a browser-bound key stored locally (not synced) to sign SPC assertions/credential creation, providing an extra layer of device binding.
- Helps align SPC credentials with requirements for proving that a transaction is tied to a specific device rather than merely a synced credential.

#### Use Cases
- Stronger fraud resistance for high-value or regulatory-sensitive payments that require device-bound proof.
- Compliance scenarios where provenance of the signing key must be constrained to a single device.
- Developers can rely on enhanced attestation semantics from the browser without implementing custom device-binding logic.

#### References
- https://issues.chromium.org/issues/377278827
- https://chromestatus.com/feature/5106102997614592
- https://w3c.github.io/secure-payment-confirmation/#sctn-browser-bound-key-store

Output file: digest_markdown/webplatform/Payment/chrome-139-stable-en.md