## Area Summary

Chrome 139's Origin trials focus on expanding experimental platform capabilities for developers to opt into new APIs and behaviors before they are standardized. Key themes include multimodal AI interaction (Prompt API), longer-lived background JavaScript (extended SharedWorker lifetime), finer-grained performance telemetry (SoftNavigation), streamlined authentication UX (WebAuth immediate mediation), renderer resource control (full-frame-rate render blocking), and broader device support for GPU workloads (WebGPU compatibility mode). These trials let teams prototype and validate integration patterns, performance implications, and security/compatibility constraints before features ship broadly, helping shape the web platform while minimizing risk.

## Detailed Updates

Below are the origin-trialized features in Chrome 139 that development teams can opt into to experiment and gather feedback.

### Prompt API

#### What's New
An API for interacting with an AI language model using text, image, and audio inputs. It supports generating image captions, visual searches, audio transcription, sound-event classification, guided text generation, and extraction use cases.

#### Technical Details
Exposes multimodal input handling (text, image, audio) to web apps via an experimental interface for model interaction. Origin trial registration is required to test the capability.

#### Use Cases
- Integrate on-device or cloud AI features: captioning, visual search, transcription.
- Prototype multimodal UIs that combine audio, image, and text inputs.
- Evaluate privacy, latency, and UX for AI-driven features before public launch.

#### References
- Origin Trial — https://developer.chrome.com/origintrials/#/register_trial/2533837740349325313
- Tracking bug #417530643 — https://issues.chromium.org/issues/417530643
- ChromeStatus.com entry — https://chromestatus.com/feature/5134603979063296

### Extended lifetime shared workers

#### What's New
Adds an `extendedLifetime: true` option to the `SharedWorker` constructor to request keeping a shared worker alive after all current clients unload.

#### Technical Details
The new constructor option signals the browser to retain the shared worker for post-unload asynchronous work. Pages opting into this origin trial can exercise lifecycle behaviors that persist beyond the last connected client.

#### Use Cases
- Perform background cleanup, telemetry uploads, or finalization tasks after page unload.
- Support multi-tab coordination and late-arriving asynchronous work that cannot complete before unload.
- Evaluate memory and power trade-offs for longer-lived worker lifecycles.

#### References
- Origin Trial — https://developer.chrome.com/origintrials/#/register_trial/3056255297124302849
- Tracking bug #400473072 — https://issues.chromium.org/issues/400473072
- ChromeStatus.com entry — https://chromestatus.com/feature/5138641357373440

### `SoftNavigation` performance entry

#### What's New
Exposes experimental soft navigation heuristics via `PerformanceObserver` and the performance timeline, reporting a `soft-navigation` entry and related timing slicing.

#### Technical Details
Reports new performance entries (including `soft-navigation`) and defines a new `timeOrigin` to help slice time ranges for soft navigations. The feature is observable through standard performance APIs while under origin trial control.

#### Use Cases
- Measure and optimize user-initiated navigations that reuse the page context (soft navigations).
- Correlate interaction timing with rendering and network activity for SPA-style transitions.
- Enhance performance analytics and RUM tooling to account for in-page navigation semantics.

#### References
- Origin Trial — https://developer.chrome.com/origintrials#/view_trial/21392098230009857
- Tracking bug #1338390 — https://issues.chromium.org/issues/1338390
- ChromeStatus.com entry — https://chromestatus.com/feature/5144837209194496
- Spec — https://wicg.github.io/soft-navigations

### Web Authentication immediate mediation

#### What's New
A mediation mode for `navigator.credentials.get()` that displays browser sign-in UI immediately if the browser knows a passkey or password for the site; otherwise it rejects with `NotAllowedError`.

#### Technical Details
Immediate mediation changes the get() mediation behavior to proactively surface sign-in UI only when a credential is immediately available to the browser; absence of a known credential leads to a deterministic rejection rather than fallthrough behavior.

#### Use Cases
- Streamline sign-in flows where the browser can offer a known credential immediately.
- Avoid unnecessary discoverability prompts when no credential exists, improving UX and security clarity.
- Test integration with passkey-driven authentication flows and measure UX impact.

#### References
- Tracking bug #408002783 — https://issues.chromium.org/issues/408002783
- ChromeStatus.com entry — https://chromestatus.com/feature/5164322780872704
- Spec — https://github.com/w3c/webauthn/pull/2291

### Full frame rate render blocking attribute

#### What's New
Adds a new render-blocking token `full-frame-rate` to blocking attributes so the renderer can be blocked with that token and run at a lower frame rate to reserve resources for loading.

#### Technical Details
This attribute introduces a render-blocking token that signals the renderer should lower its frame rate while blocked, allowing more resources to be allocated to loading work. The capability is available via origin trial registration.

#### Use Cases
- Improve loading performance on resource-constrained devices by reducing compositor/render budget during critical load periods.
- Evaluate trade-offs between visual smoothness and faster content readiness.
- Integrate into adaptive loading strategies that throttle rendering to prioritize network and parse work.

#### References
- Origin Trial — https://developer.chrome.com/origintrials/#/register_trial/3578672853899280385
- Tracking bug #397832388 — https://issues.chromium.org/issues/397832388
- ChromeStatus.com entry — https://chromestatus.com/feature/5207202081800192

### WebGPU compatibility mode

#### What's New
An opt-in, lightly restricted subset of the WebGPU API that can run on older graphics backends (e.g., OpenGL, Direct3D11), enabling WebGPU apps to reach older devices.

#### Technical Details
Compatibility mode provides a constrained WebGPU subset and requires developers to opt in and obey specific constraints. This allows implementations to map the mode to legacy graphics APIs while preserving a defined surface of WebGPU functionality.

#### Use Cases
- Improve reach of WebGPU-based applications to devices without modern graphics drivers.
- Prototype fallback strategies and measure performance/feature gaps between native WebGPU and compatibility-mode implementations.
- Validate shader/workload portability and developer tooling for broader device support.

#### References
- Origin Trial — https://developer.chrome.com/origintrials/#/register_trial/1489002626799370241
- Tracking bug #40266903 — https://issues.chromium.org/issues/40266903
- ChromeStatus.com entry — https://chromestatus.com/feature/6436406437871616
- Spec — https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md

Saved to: digest_markdown/webplatform/Origin trials/chrome-139-stable-en.md