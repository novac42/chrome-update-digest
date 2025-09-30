# Area Summary

Chrome 139 origin trials focus on expanding platform capabilities for AI interactions, background work, performance observability, authentication UX, rendering resource management, and wider WebGPU reach. The most impactful changes for developers are: a multimodal Prompt API for AI inputs, extended-lifetime SharedWorkers for post-unload work, a new soft-navigation performance entry for richer interaction telemetry, immediate mediation for WebAuth flows, a full-frame-rate render-blocking token to influence renderer behavior, and a compatibility mode to broaden WebGPU device support. Collectively these trials provide new primitives that improve app responsiveness, offline/background workflows, performance measurement, and graphics portability while exposing trade-offs developers must manage.

## Detailed Updates

The following entries expand on the above themes with concise technical context, practical use cases, and links to the origin trial registrations, tracking bugs, and specs.

### Prompt API

#### What's New
An API for interacting with an AI language model using text, image, and audio inputs to enable captioning, visual search, transcription, classification, instruction-following text generation, and extraction.

#### Technical Details
Exposes a web-facing input/output model that accepts multimodal inputs; integrates into the web platform as an origin-trial-guarded web API. Developers should plan for client-side invocation patterns and server-assisted flows where models or billing constraints apply.

#### Use Cases
Image captioning, visual search on-page, client-side audio transcription, multimodal assistants embedded in web apps, and automation workflows that accept user-provided images/audio.

#### References
- https://developer.chrome.com/origintrials/#/register_trial/2533837740349325313
- https://issues.chromium.org/issues/417530643
- https://chromestatus.com/feature/5134603979063296

### Extended lifetime shared workers

#### What's New
Adds `extendedLifetime: true` option to the `SharedWorker` constructor to request the worker be kept alive after all clients unload, enabling asynchronous work that continues beyond a page unload.

#### Technical Details
This origin-trial option changes lifetime semantics of shared workers, allowing background JS execution after client unload events. Developers must handle resource lifecycle, persistence, and potential power/performance impacts; consider integration with service workers and the page's unload sequence.

#### Use Cases
Deferred uploads or analytics flushes after navigation, coordination tasks across multiple pages, and background processing that avoids immediate termination on client unload.

#### References
- https://developer.chrome.com/origintrials/#/register_trial/3056255297124302849
- https://issues.chromium.org/issues/400473072
- https://chromestatus.com/feature/5138641357373440

### `SoftNavigation` performance entry

#### What's New
Exposes experimental soft navigation heuristics through `PerformanceObserver` and the performance timeline, reporting `soft-navigation` entries and a new `timeOrigin` to help slice transition measurements.

#### Technical Details
Adds performance timeline entry types for soft navigations (user interactions that navigate without a full navigation). Developers can observe entries via standard PerformanceObserver APIs and correlate them with other timeline events for accurate interaction-to-render metrics.

#### Use Cases
Measuring and optimizing single-page app navigations, quantifying interaction latency for routing transitions, and improving UX by identifying costly soft navigation paths.

#### References
- https://developer.chrome.com/origintrials#/view_trial/21392098230009857
- https://issues.chromium.org/issues/1338390
- https://chromestatus.com/feature/5144837209194496
- https://wicg.github.io/soft-navigations

### Web Authentication immediate mediation

#### What's New
A mediation mode for `navigator.credentials.get()` that triggers browser sign-in UI when a passkey or password for the site is immediately known; otherwise it rejects with `NotAllowedError`.

#### Technical Details
Adds an immediate mediation mode influencing credential mediation behavior on the client. This modifies the runtime UX path of WebAuthn flows and affects how credential discovery and user prompts are triggered.

#### Use Cases
Streamlined sign-in UX when credentials are already present, conditional credential prompt flows, and improved NUX for sites that want immediate, low-friction authentication when available.

#### References
- https://issues.chromium.org/issues/408002783
- https://chromestatus.com/feature/5164322780872704
- https://github.com/w3c/webauthn/pull/2291

### Full frame rate render blocking attribute

#### What's New
Introduces a render blocking token ("full-frame-rate") as a blocking attribute; when held, the renderer runs at a lower frame rate to reserve resources for loading.

#### Technical Details
Provides a renderer-level token that influences frame-rate budgeting and scheduling to prioritize loading work. Origin-trial gated; developers must balance perceived UI smoothness against resource availability during critical loads.

#### Use Cases
Optimizing critical-path resource loading on heavy pages, reducing jank caused by simultaneous high-frame-rate rendering and loading, and tuning renderer behavior during page transitions.

#### References
- https://developer.chrome.com/origintrials/#/register_trial/3578672853899280385
- https://issues.chromium.org/issues/397832388
- https://chromestatus.com/feature/5207202081800192

### WebGPU compatibility mode

#### What's New
Opt-in, lightly restricted subset of WebGPU that can run on older graphics APIs (e.g., OpenGL, Direct3D11) to extend WebGPU app reach to older devices.

#### Technical Details
Compatibility mode restricts or alters certain WebGPU capabilities so implementations can map to legacy graphics backends. Origin-trial registration allows developers to detect and opt into the mode and gracefully degrade or adjust shaders/workflows.

#### Use Cases
Broader device support for WebGPU apps, progressive enhancement paths where high-end features are conditional, and easing migration of WebGL/OpenGL code paths to WebGPU.

#### References
- https://developer.chrome.com/origintrials/#/register_trial/1489002626799370241
- https://issues.chromium.org/issues/40266903
- https://chromestatus.com/feature/6436406437871616
- https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md

File: digest_markdown/webplatform/Origin trials/chrome-139-stable-en.md