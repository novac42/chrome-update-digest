---
layout: default
title: chrome-140-en
---

## Area Summary

Chrome 140 Stable introduces the Controlled Frame API targeted exclusively at Isolated Web Apps (IWAs). The main trend is expanding safe embedding capabilities for IWAs by allowing embedding of content that standard <iframe> rejects, while giving the host app control over that content. This change is impactful for developers who need to integrate third‑party or legacy content into an IWA without sacrificing isolation guarantees. It advances the web platform by providing a new, IWA‑scoped web API that balances richer integration with explicit app-level control.

## Detailed Updates

The single feature below directly follows from the summary and highlights practical implications for IWA developers.

### Controlled Frame API (available only to IWAs)

#### What's New
Controlled Frame is a new API available only to Isolated Web Apps that enables embedding all content — including third‑party content that cannot be embedded in a standard <iframe> — and provides programmatic control over that embedded content.

#### Technical Details
- Scope: API surface restricted to IWAs only (per the IWA model).
- Purpose: bypasses iframe embedding restrictions by providing a controlled embedding primitive; control semantics and security model are defined by the spec.
- Key references and spec text are available in the linked explainer and spec for implementation and behavior details.

Relevance to platform areas:
- webapi / javascript: introduces a new JS API for IWAs to instantiate and control embedded frames.
- security-privacy: changes the embedding model within IWAs; expect explicit IWA-scoped isolation semantics rather than broad cross-origin iframe behavior.
- performance / graphics-webgpu / css: embedding arbitrary content can affect layout and rendering pipelines; developers should profile render and paint costs.
- pwa-service-worker: IWAs using service workers may need to consider resource routing and caching for controlled-frame content.
- deprecations: this does not remove iframe but provides an alternate IWA-only primitive for cases where iframe embedding is blocked.

#### Use Cases
- Integrating third‑party widgets or legacy pages inside an IWA where traditional <iframe> embedding is blocked.
- Building kiosk or managed‑content viewers inside an IWA that need fine‑grained control over embedded navigation and UI.
- Creating secure, sandboxed hosting of remote content with explicit app-level control hooks (e.g., navigation, input mediation).

#### References
- https://github.com/WICG/isolated-web-apps/blob/main/README.md — Isolated Web Apps explainer
- https://issues.chromium.org/issues/40191772 — 'Tracking bug #40191772'
- https://chromestatus.com/feature/5199572022853632 — ChromeStatus.com entry
- https://wicg.github.io/controlled-frame — Spec
