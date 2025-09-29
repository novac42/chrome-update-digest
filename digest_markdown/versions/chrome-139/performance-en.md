---
layout: default
title: Area Summary
---

# Area Summary

Chrome 139 (stable) continues performance-focused improvements that reduce resource usage, expose more control over sensing pipelines, and add finer-grained performance telemetry for navigation-like interactions. The most impactful changes for developers are faster background freezing on Android (shorter background lifetime), added tuning points for WebXR depth sensing to reduce GPU/CPU cost, and a new experimental performance entry for soft navigations that improves measurement fidelity. Together these updates advance the platform by tightening lifecycle/resource policies, enabling lower-latency immersive experiences, and giving developers new telemetry to optimize perceived and actual responsiveness. These changes matter because they affect battery/CPU budgeting, rendering pipelines, and how teams measure and iterate on navigation and immersive scenarios.

## Detailed Updates

The following items expand the summary into actionable details for Performance-focused engineering and optimization.

### Faster background freezing on Android

#### What's New
Background pages and associated workers on Android now freeze sooner: one minute instead of five minutes.

#### Technical Details
The background-freeze timeout was shortened from 5 minutes to 1 minute for Android, reducing the window during which background tasks remain unfrozen.

#### Use Cases
- Mobile web apps and PWAs: reduces unintended CPU/network usage from background pages and workers.
- Devs should verify critical background tasks complete earlier or migrate to more explicit background mechanisms (e.g., service workers with appropriate lifecycle design).

#### References
- Tracking bug #435623337: https://issues.chromium.org/issues/435623337
- ChromeStatus.com entry: https://chromestatus.com/feature/5386725031149568

### WebXR depth sensing performance improvements

#### What's New
Exposes mechanisms to customize depth sensing behavior in a WebXR session to improve performance of depth buffer generation or consumption.

#### Technical Details
The implementation exposes options such as requesting raw versus smoothed depth buffers and other tuning points to influence how depth data is produced or consumed, with the goal of lowering CPU/GPU cost and improving runtime efficiency.

#### Use Cases
- XR applications can choose depth-buffer modes that trade off quality for reduced processing and bandwidth, improving frame rates and latency.
- Developers building mixed-reality features can profile raw vs. smoothed depth to find optimal pipelines for rendering and physics.

#### References
- Tracking bug #410607163: https://issues.chromium.org/issues/410607163
- ChromeStatus.com entry: https://chromestatus.com/feature/5074096916004864
- Spec: https://immersive-web.github.io/depth-sensing

### `SoftNavigation` performance entry

#### What's New
Introduces experimental soft-navigation heuristics to web developers via PerformanceObserver and the performance timeline.

#### Technical Details
This feature reports two new performance entries (including `soft-navigation`) and defines a new timeOrigin to help slice timing for user interactions that navigate the page, enabling developers to observe soft-navigation timing via the performance API.

#### Use Cases
- Measurement: instrument and distinguish soft navigations from full navigations to improve telemetry fidelity.
- Optimization: correlate soft-navigation timings with resource loading and rendering to reduce perceived latency for interaction-driven navigations.

#### References
- Origin Trial: https://developer.chrome.com/origintrials#/view_trial/21392098230009857
- Tracking bug #1338390: https://issues.chromium.org/issues/1338390
- ChromeStatus.com entry: https://chromestatus.com/feature/5144837209194496
- Spec: https://wicg.github.io/soft-navigations

## Area-Specific Expertise (Performance-focused guidance)

- css: Review costly layout/reflow on soft navigations; prefer containment and compositing to reduce re-layout.
- webapi: Use PerformanceObserver to capture `soft-navigation` entries and correlate with resource timing.
- graphics-webgpu: For WebXR depth modes, benchmark raw vs. smoothed depth paths to balance GPU/CPU load.
- javascript: Move nonessential background work to service workers or schedule with idle callbacks given shorter freeze windows.
- security-privacy: Ensure depth-sensing usage follows privacy expectations; check spec guidance before enabling in production.
- performance: Re-baseline telemetry after background-freeze changes; expect shorter background lifetimes.
- multimedia: For XR media streams, prefer depth modes that reduce decoding/processing overhead.
- devices: Test depth-sensing changes across device classes to account for sensor and GPU differences.
- pwa-service-worker: Rely on service workers for continuing background tasks rather than background pages that will freeze sooner.
- webassembly: Profile WASM modules used in depth processing to reduce main-thread stalls.
- deprecations: Validate assumptions about background task lifetimes and migrate long-running tasks to supported background primitives.

File path to save: digest_markdown/webplatform/Performance/chrome-139-stable-en.md
