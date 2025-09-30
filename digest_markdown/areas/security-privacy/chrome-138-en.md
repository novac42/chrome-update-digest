---
layout: default
title: chrome-138-en
---

## Area Summary

Chrome 138's Security-Privacy updates center on strengthening script integrity guarantees by introducing an Integrity-Policy mechanism. The most impactful change for developers is a server-controlled way to assert that scripts are validated with Subresource Integrity (SRI), closing gaps where SRI might not be consistently applied. This advances the web platform by enabling enforceable integrity requirements for script loading, reducing risk from supply-chain tampering and unintended script substitution. These updates matter because they give teams a deployable policy tool to raise baseline script security without changing individual script tags.

## Detailed Updates

Below are the Security-Privacy changes relevant to developers and security engineers, focused on enforceable script integrity.

### Integrity Policy for scripts

#### What's New
Subresource-Integrity (SRI) enables developers to verify that loaded assets match expected content. The Integrity-Policy header gives developers the ability to assert that scripts are validated using SRI.

#### Technical Details
- The feature introduces a server-sent policy (Integrity-Policy header) that signals the requirement or expectation that fetched scripts are accompanied by SRI metadata.
- Implementation and exact header semantics are specified in the webappsec CSP-related spec (see References). Use the spec and ChromeStatus entry for compatibility and deployment notes.

#### Use Cases
- Enforce SRI for all scripts on sensitive pages (payment, authentication) without modifying each <script> tag.
- Reduce risk from compromised CDNs or injected script modifications by making integrity validation a deployable policy.
- Aid audits and automated checks by providing a single header-based assertion of integrity requirements.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5104518463627264
- Spec: https://w3c.github.io/webappsec-csp/#integrityPolicy

Save to: digest_markdown/webplatform/Security-Privacy/chrome-138-stable-en.md
