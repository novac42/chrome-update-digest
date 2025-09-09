---
layout: default
title: chrome-139
---

## Secure Payment Confirmation (SPC)

### The `securePaymentConfirmationAvailability` API

This is a JavaScript API to provide an easier way to check if the Secure Payment Confirmation (SPC) feature is available. With this API, the only way to determine SPC's availability was to create a `PaymentRequest` with the required parameters, which is clunky and difficult in the case where a developer wants to check for SPC before starting to process a payment.

[Tracking bug #40258712](https://issues.chromium.org/issues/40258712) | [ChromeStatus.com entry](https://chromestatus.com/feature/5165040614768640) | [Spec](https://github.com/w3c/secure-payment-confirmation/pull/285)

### Secure Payment Confirmation: Browser Bound Keys

Adds an additional cryptographic signature over Secure Payment Confirmation assertions and credential creation. The corresponding private key is not synced across devices. This helps web developers meet requirements for device binding for payment transactions.

[Tracking bug #377278827](https://issues.chromium.org/issues/377278827) | [ChromeStatus.com entry](https://chromestatus.com/feature/5106102997614592) | [Spec](https://w3c.github.io/secure-payment-confirmation/#sctn-browser-bound-key-store)
