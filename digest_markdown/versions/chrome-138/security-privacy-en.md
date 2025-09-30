---
layout: default
title: security-privacy-en
---

## Area Summary

Chrome 138’s Security-Privacy updates focus on strengthening script integrity guarantees by introducing an Integrity-Policy header. The main developer impact is a standardized way to require Subresource Integrity (SRI) validation for scripts across a site. This advances the web platform by enabling more robust defenses against tampered or unexpected script assets and supports centralized policy enforcement. These updates matter because they reduce supply-chain and third-party script risks and simplify compliance and auditing for web applications.

## Detailed Updates

The single Security-Privacy change in this release tightens how sites can enforce SRI for script resources. Below is the feature detail and direct references.

### Integrity Policy for scripts

#### What's New
Subresource Integrity (SRI) already lets developers verify that assets loaded match expected content. The Integrity-Policy header provides a mechanism for developers to require that scripts are validated using SRI.

#### Technical Details
The feature introduces an Integrity-Policy HTTP header (per the spec) that allows site operators to assert SRI validation requirements for script subresources. When present, the policy influences the browser’s loading behavior to enforce integrity checks according to the policy rules defined in the specification.

#### Use Cases
- Enforce SRI across an entire site to ensure all loaded scripts are integrity-checked.
- Reduce risks from compromised CDNs or third-party script injections by mandating integrity verification.
- Simplify security audits and compliance by centralizing script-integrity requirements via an HTTP header.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5104518463627264
- Spec: https://w3c.github.io/webappsec-csp/#integrityPolicy
