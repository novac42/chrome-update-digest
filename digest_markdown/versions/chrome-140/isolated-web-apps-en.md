---
layout: default
title: isolated-web-apps-en
---

## Area Summary

Chrome 140 stable introduces the Controlled Frame API exclusively for Isolated Web Apps (IWAs). The main trend is extending IWAs' ability to embed and control third-party content that traditional <iframe> embedding blocks. This change is significant for developers building installed web apps that need to integrate external content while keeping the app-level isolation model. It advances the platform by giving IWAs a sanctioned surface for richer embedding scenarios while centralizing control and review via the IWA model.

## Detailed Updates

The short summary above frames the concrete change in this release. Below is the single feature added for Isolated Web Apps in Chrome 140.

### Controlled Frame API (available only to IWAs)

#### What's New
Adds a Controlled Frame API that is available only to Isolated Web Apps. It enables embedding all content, including third-party content that cannot be embedded in a standard <iframe>, and provides programmatic control over the embedded content surface.

#### Technical Details
- The API is scoped to IWAs (installation and packaging model for isolated apps), not to regular webpages.
- The specification and implementation work are tracked via the linked spec and Chromium issue tracker; consult those links for the precise API shape and security model.
- Relevant links:
  - Spec: https://wicg.github.io/controlled-frame
  - Tracking: https://issues.chromium.org/issues/40191772
  - Explainer: https://github.com/WICG/isolated-web-apps/blob/main/README.md
  - ChromeStatus: https://chromestatus.com/feature/5199572022853632

#### Use Cases
- Embedding third-party UI or content inside an IWA when traditional embedding is blocked by frame-ancestors or other restrictions.
- Building hybrid installed apps that combine local, trusted app logic with remote content while keeping the app surface under developer control.
- Scenarios where developers need finer runtime control over embedded content lifecycle and integration points within an IWA packaging model.

#### References
- https://github.com/WICG/isolated-web-apps/blob/main/README.md
- https://issues.chromium.org/issues/40191772
- https://chromestatus.com/feature/5199572022853632
- https://wicg.github.io/controlled-frame

Saved to: digest_markdown/webplatform/Isolated Web Apps/chrome-140-stable-en.md
