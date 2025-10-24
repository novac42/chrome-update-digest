---
layout: default
title: Chrome Payment Area Digest – Chrome 135 Stable
---

# Chrome Payment Area Digest – Chrome 135 Stable

## 1. Area Summary

Chrome 135 introduces a notable enhancement in the Payment domain, focusing on streamlining push payment workflows for web applications. The main theme is improved browser support for signaling pending payments directly to registered payment clients, leveraging new HTML link relations. This update empowers developers to create more seamless and integrated payment experiences, reducing friction for users and enabling faster transaction flows. By advancing the interoperability between web content and payment handlers, Chrome continues to strengthen the web platform’s capabilities for secure and efficient digital payments.

## Detailed Updates

Below is a detailed breakdown of the new feature introduced in Chrome 135 for the Payment area.

### Link `rel=facilitated-payment` to support push payments

#### What's New

Chrome now supports the `<link rel="facilitated-payment" href="...">` element, which acts as a hint for the browser to notify registered payment clients about a pending push payment.

#### Technical Details

This feature allows web developers to include a `<link rel="facilitated-payment" href="...">` tag in their HTML. When present, the browser interprets this as an intent to initiate a push payment and proactively notifies any payment clients that have registered for such events. This mechanism leverages the HTML DOM and payment handler infrastructure, enabling a more direct and standardized way to trigger payment flows from web content.

#### Use Cases

- E-commerce sites can prompt payment apps or wallets to prepare for a transaction as soon as a user lands on a checkout page, reducing steps and wait times.
- Financial service providers can offer smoother push payment experiences, improving conversion rates and user satisfaction.
- Developers benefit from a standardized, declarative approach to integrating payment notifications, reducing the need for custom JavaScript logic.

#### References

- [Tracking bug #1477049](https://issues.chromium.org/issues/1477049)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5198846820352000)
