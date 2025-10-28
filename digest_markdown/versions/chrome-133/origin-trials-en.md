---
layout: default
title: origin-trials-en
---

## Area Summary

Chrome 133's Origin Trials focus on giving developers targeted control over lifecycle and accessibility behaviors via opt-ins. The two trials enable sites to opt out of Energy Saver freezing and to reference elements across shadow DOM boundaries for ARIA relationships. These changes matter because they preserve interactivity and improve accessible component composition without weakening encapsulation. Developers should evaluate registration for these trials to maintain UX and accessibility in affected scenarios.

## Detailed Updates

Below are the origin-trial features in Chrome 133, with concise technical notes, realistic use cases, and links to the authoritative references.

### Opt out of freezing on Energy Saver

#### What's New
This opt out trial lets sites opt out from the freezing on Energy Saver behavior that ships in Chrome 133.

#### Technical Details
- Origin-trial-capable behavior that modifies the page-lifecycle freezing behavior under Energy Saver.
- Associated spec: Page Lifecycle.
- Primary tags present in the release metadata: webgpu, origin-trials.

#### Use Cases
- Sites that require continued activity (e.g., long-running computations, real-time interactions, or graphics workloads) can register to avoid being frozen when the browser enters Energy Saver modes.
- Useful for PWA and WebGPU-based apps that must maintain execution during low-power modes.

#### References
- [Tracking bug #325954772](https://issues.chromium.org/issues/325954772)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5158599457767424)
- [Spec](https://wicg.github.io/page-lifecycle)

### Reference Target for Cross-root ARIA

#### What's New
Reference Target is a feature to enable using IDREF attributes such as `for` and `aria-labelledby` to refer to elements inside a component's shadow DOM, while maintaining encapsulation of the internal details of the shadow DOM. The main goal of this feature is to enable ARIA to work across shadow ro...

#### Technical Details
- Enables cross-root IDREF resolution for attributes like `for` and `aria-labelledby` to improve ARIA relationships involving shadow DOM components.
- Aims to preserve shadow DOM encapsulation while allowing external accessibility references.
- Primary tags present in the release metadata: webgpu, origin-trials.

#### Use Cases
- Component authors can build accessible web components where labels or describedby relationships span light DOM and shadow DOM without exposing internal implementation details.
- Improves interoperability of ARIA semantics in complex component hierarchies and facilitates more robust screen-reader behavior.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5188237101891584)
