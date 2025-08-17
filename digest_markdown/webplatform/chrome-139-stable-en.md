---
layout: default
title: Chrome 139 Stable Release – Web Platform Digest
---

# Chrome 139 Stable Release – Web Platform Digest

## 1. Executive Summary

Chrome 139 delivers a substantial set of updates across CSS, Web APIs, graphics (WebGPU), JavaScript, security, performance, multimedia, device APIs, PWA/service worker, WebAssembly, and deprecations. This release focuses on modernizing web standards compliance, enhancing developer ergonomics, improving security and privacy, and expanding device and performance capabilities. Notable highlights include advanced CSS features, significant WebGPU and WebXR improvements, privacy and security hardening, and several impactful deprecations.

## 2. Key Implications

### Technical Impact

- **CSS**: Enhanced expressiveness and control with new properties (e.g., `corner-shape`, `font-width`), custom functions, and improved transition handling.
- **WebGPU & Graphics**: Expanded compatibility and feature set, including 3D texture compression, compatibility mode, and core feature/limit compliance.
- **Web APIs & JavaScript**: Broader standards alignment (e.g., JSON MIME detection, relaxed DOM API character rules), new APIs for payments and crash reporting, and improved worker lifecycle management.
- **Security & Privacy**: Reduced fingerprinting, stricter CSP error handling, and window.name isolation.
- **Performance**: Faster background freezing, new soft navigation metrics, and render blocking optimizations.
- **Deprecations**: Removal of legacy headers, charset auto-detection, and macOS 11 support.

### New Capabilities

- Advanced CSS layout and animation primitives.
- WebGPU compatibility for older hardware.
- On-device speech recognition.
- Secure Payment Confirmation enhancements.
- AI-powered Prompt API (origin trial).
- Extended lifetime for shared workers.

### Technical Debt Considerations

- Migration required for deprecated features (e.g., `Purpose: prefetch` header, ISO-2022-JP charset, macOS 11).
- Review and update of code relying on legacy behaviors or removed APIs.

## 3. Risk Assessment

**Critical Risks:**
- **Breaking Changes**:
  - Removal of macOS 11 support.
  - Removal of auto-detection for ISO-2022-JP charset.
  - Removal of legacy `Purpose: prefetch` header.
- **Security Considerations**:
  - Stricter CSP error event handling.
  - Reduced Accept-Language header granularity.
  - Window.name isolation on cross-site navigation.

**Medium Risks:**
- **Deprecations**:
  - Legacy font-stretch aliasing.
  - Legacy headers and charsets.
- **Performance Impacts**:
  - Faster background freezing may affect long-running background tasks.
  - Render blocking attribute changes could impact animation smoothness.

## 4. Recommended Actions

### Immediate Actions

- Audit and update code for deprecated/removed features (headers, charsets, OS support).
- Test CSS and WebGPU features for compatibility and performance.
- Review Accept-Language and window.name usage for privacy compliance.
- Evaluate impact of background freezing on Android.

### Short-term Planning

- Plan migration away from deprecated APIs and behaviors.
- Experiment with new CSS and WebGPU features for upcoming projects.
- Participate in relevant origin trials (Prompt API, extended shared workers, soft navigation metrics).
- Update documentation and onboarding for new security/privacy defaults.

### Long-term Strategy

- Monitor adoption and browser support for new CSS and WebGPU standards.
- Invest in progressive enhancement strategies for advanced features.
- Track further deprecations and plan for proactive migration.
- Leverage new APIs (e.g., Prompt API, on-device speech) for innovative user experiences.

## 5. Feature Analysis

---

### Short-circuiting `var()` and `attr()`

**Impact Level**: 🟡 Important

**What Changed**:  
`var()` and `attr()` functions now evaluate without searching for cycles in their fallback when the fallback is not taken, improving performance and predictability.

**Why It Matters**:  
Reduces unnecessary computation and aligns Chrome with CSS spec behavior, improving efficiency in complex stylesheets.

**Implementation Guidance**:
- Refactor CSS custom property usage to rely on this more predictable evaluation.
- Test for edge cases where fallbacks were previously evaluated.

**References**:  
[ChromeStatus.com entry](https://chromestatus.com/feature/6212939656462336)

---

### Support `font-feature-settings` descriptor in `@font-face` rule

**Impact Level**: 🟡 Important

**What Changed**:  
Adds support for string-based `font-feature-settings` in `@font-face`, ignoring invalid tags per spec.

**Why It Matters**:  
Enables advanced typographic control and aligns with CSS Fonts Level 4, supporting modern font workflows.

**Implementation Guidance**:
- Use string-based syntax for font features in `@font-face`.
- Remove reliance on non-standard or binary forms.

**References**:  
[Tracking bug #40398871](https://issues.chromium.org/issues/40398871) | [ChromeStatus.com entry](https://chromestatus.com/feature/5102801981800448) | [Spec](https://www.w3.org/TR/css-fonts-4/#font-rend-desc)

---

### CSS custom functions

**Impact Level**: 🟡 Important

**What Changed**:  
Introduces custom CSS functions, allowing dynamic values based on parameters and conditionals.

**Why It Matters**:  
Greatly increases CSS expressiveness and reusability, paving the way for more maintainable and dynamic styles.

**Implementation Guidance**:
- Explore defining and using custom functions for repetitive or complex style logic.
- Monitor browser support for cross-browser compatibility.

**References**:  
[Tracking bug #325504770](https://issues.chromium.org/issues/325504770) | [ChromeStatus.com entry](https://chromestatus.com/feature/5179721933651968) | [Spec](https://drafts.csswg.org/css-mixins-1/#defining-custom-functions)

---

### Continue running transitions when switching to initial transition value

**Impact Level**: 🟡 Important

**What Changed**:  
Transitions continue running even if `transition` is set to `none`, unless the transitioned property value changes.

**Why It Matters**:  
Aligns Chrome with Safari and Firefox, ensuring consistent animation behavior across browsers.

**Implementation Guidance**:
- Review transition logic to ensure expected behavior when toggling transition properties.
- Test animations for cross-browser consistency.

**References**:  
[ChromeStatus.com entry](https://chromestatus.com/feature/5194501932711936) | [Spec](https://www.w3.org/TR/css-transitions-1/#starting)

---

### Corner shaping (`corner-shape`, `superellipse`, `squircle`)

**Impact Level**: 🟡 Important

**What Changed**:  
Adds new CSS properties for advanced corner shaping, enabling superellipses, squircles, and animated transitions between shapes.

**Why It Matters**:  
Unlocks modern UI design patterns and richer visual effects beyond standard border-radius.

**Implementation Guidance**:
- Experiment with new corner shapes for distinctive UI elements.
- Animate between shapes for engaging transitions.

**References**:  
[Tracking bug #393145930](https://issues.chromium.org/issues/393145930) | [ChromeStatus.com entry](https://chromestatus.com/feature/5357329815699456) | [Spec](https://drafts.csswg.org/css-borders-4/#corner-shaping)

---

### Add `font-width` property and descriptor and make `font-stretch` a legacy alias

**Impact Level**: 🟡 Important

**What Changed**:  
Introduces `font-width` as the standard property, with `font-stretch` now a legacy alias.

**Why It Matters**:  
Improves standards compliance and future-proofs font styling.

**Implementation Guidance**:
- Update stylesheets to use `font-width`.
- Phase out `font-stretch` where possible.

**References**:  
[Tracking bug #356670472](https://issues.chromium.org/issues/356670472) | [ChromeStatus.com entry](https://chromestatus.com/feature/5190141555245056)

---

### Support async attribute for SVG `<script>` element

**Impact Level**: 🟢 Nice-to-have

**What Changed**:  
SVG `<script>` elements now support the `async` attribute, enabling asynchronous script execution.

**Why It Matters**:  
Improves SVG performance and responsiveness, especially for complex graphics.

**Implementation Guidance**:
- Use `async` for non-blocking SVG scripts.
- Test for compatibility with existing SVG workflows.

**References**:  
[Tracking bug #40067618](https://issues.chromium.org/issues/40067618) | [ChromeStatus.com entry](https://chromestatus.com/feature/6114615389585408) | [Spec](https://svgwg.org/svg2-draft/interact.html#ScriptElement:~:text=%E2%80%98script%E2%80%99%20element-,SVG%202%20Requirement%3A,Consider%20allowing%20async/defer%20on%20%E2%80%98script%E2%80%99.,-Resolution%3A)

---

### The `request-close` invoker command

**Impact Level**: 🟢 Nice-to-have

**What Changed**:  
Adds a declarative command for dialogs to request closure, firing the cancel event as with `requestClose()`.

**Why It Matters**:  
Improves dialog control and accessibility, aligning with modern HTML standards.

**Implementation Guidance**:
- Use the `request-close` command for custom dialog workflows.
- Ensure cancel event handling is robust.

**References**:  
[Tracking bug #400647849](https://issues.chromium.org/issues/400647849) | [ChromeStatus.com entry](https://chromestatus.com/feature/5592399713402880) | [Spec](https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-command-request-close-state)

---

### Scroll anchoring priority candidate fix

**Impact Level**: 🟢 Nice-to-have

**What Changed**:  
Refines scroll anchoring algorithm to select the deepest onscreen element as anchor.

**Why It Matters**:  
Reduces scroll jumps and improves user experience during dynamic content updates.

**Implementation Guidance**:
- Test scroll behavior in dynamic layouts.
- Monitor for regressions in scroll anchoring.

**References**:  
[ChromeStatus.com entry](https://chromestatus.com/feature/5070370113323008)

---

### WebXR depth sensing performance improvements

**Impact Level**: 🟡 Important

**What Changed**:  
Exposes new controls for depth buffer behavior in WebXR, including raw/smooth buffers and buffer suspension.

**Why It Matters**:  
Enables more efficient and performant AR/VR experiences.

**Implementation Guidance**:
- Use new depth buffer options for optimized XR rendering.
- Profile performance impacts in XR applications.

**References**:  
[Tracking bug #410607163](https://issues.chromium.org/issues/410607163) | [ChromeStatus.com entry](https://chromestatus.com/feature/5074096916004864) | [Spec](https://immersive-web.github.io/depth-sensing)

---

### Allow more characters in JavaScript DOM APIs

**Impact Level**: 🟢 Nice-to-have

**What Changed**:  
Relaxes validation in DOM APIs to match the HTML parser, allowing a wider range of element and attribute names.

**Why It Matters**:  
Improves standards compliance and developer flexibility.

**Implementation Guidance**:
- Use extended character sets in custom elements/attributes as needed.
- Test for compatibility with other browsers.

**References**:  
[Tracking bug #40228234](https://issues.chromium.org/issues/40228234) | [ChromeStatus.com entry](https://chromestatus.com/feature/6278918763708416) | [Spec](https://dom.spec.whatwg.org/#namespaces)

---

### WebGPU: 3D texture support for BC and ASTC compressed formats

**Impact Level**: 🟡 Important

**What Changed**:  
Adds 3D texture support for BC and ASTC compressed formats in WebGPU.

**Why It Matters**:  
Enables efficient 3D graphics and texture compression for advanced web games and visualization.

**Implementation Guidance**:
- Use compressed 3D textures for performance-critical graphics.
- Test on target hardware for compatibility.

**References**:  
[Tracking bug #342840940](https://issues.chromium.org/issues/342840940) | [ChromeStatus.com entry](https://chromestatus.com/feature/5080855386783744) | [Spec](https://gpuweb.github.io/gpuweb/#texture-compression-bc-sliced-3d)

---

### Detailed WebGPU Updates

**Impact Level**: 🟢 Nice-to-have

**What Changed**:  
General updates and improvements to WebGPU as detailed in the Chrome Developers blog.

**Why It Matters**:  
Stay informed on the latest WebGPU capabilities and best practices.

**Implementation Guidance**:
- Review blog for new features and migration tips.

**References**:  
[Chrome for Developers](https://developer.chrome.com/) | [Blog](https://developer.chrome.com/blog)

---

### Enable the feature (WebGPU compatibility mode)

**Impact Level**: 🟢 Nice-to-have

**What Changed**:  
WebGPU compatibility mode can be enabled via flags or origin trial for broader device support.

**Why It Matters**:  
Allows WebGPU apps to run on older hardware.

**Implementation Guidance**:
- Enable compatibility mode for wider reach.
- Participate in the origin trial for early feedback.

**References**:  
[WebGPU compatibility mode](https://chromestatus.com/feature/6436406437871616)

---

### The `securePaymentConfirmationAvailability` API

**Impact Level**: 🟢 Nice-to-have

**What Changed**:  
New API to check Secure Payment Confirmation (SPC) availability without creating a PaymentRequest.

**Why It Matters**:  
Simplifies payment flows and improves user experience.

**Implementation Guidance**:
- Use the API to conditionally offer SPC-based payments.

**References**:  
[Tracking bug #40258712](https://issues.chromium.org/issues/40258712) | [ChromeStatus.com entry](https://chromestatus.com/feature/5165040614768640) | [Spec](https://github.com/w3c/secure-payment-confirmation/pull/285)

---

### Secure Payment Confirmation: Browser Bound Keys

**Impact Level**: 🟡 Important

**What Changed**:  
Adds device-bound cryptographic keys for Secure Payment Confirmation, not synced across devices.

**Why It Matters**:  
Enhances payment security and compliance with device binding requirements.

**Implementation Guidance**:
- Use browser-bound keys for high-security payment flows.

**References**:  
[Tracking bug #377278827](https://issues.chromium.org/issues/377278827) | [ChromeStatus.com entry](https://chromestatus.com/feature/5106102997614592) | [Spec](https://w3c.github.io/secure-payment-confirmation/#sctn-browser-bound-key-store)

---

### On-device Web Speech API

**Impact Level**: 🟡 Important

**What Changed**:  
Adds on-device speech recognition, keeping audio and transcripts local.

**Why It Matters**:  
Improves privacy and enables offline speech recognition.

**Implementation Guidance**:
- Query for on-device support and prompt users to install resources as needed.
- Offer fallback to cloud-based recognition if unavailable.

**References**:  
[ChromeStatus.com entry](https://chromestatus.com/feature/6090916291674112) | [Spec](https://webaudio.github.io/web-speech-api)

---

### Clear window name for cross-site navigations that switches browsing context group

**Impact Level**: 🟡 Important

**What Changed**:  
Clears `window.name` on cross-site navigation to prevent tracking.

**Why It Matters**:  
Reduces cross-site tracking vectors and improves privacy.

**Implementation Guidance**:
- Avoid relying on `window.name` for cross-site data persistence.

**References**:  
[Tracking bug #1090128](https://issues.chromium.org/issues/1090128) | [ChromeStatus.com entry](https://chromestatus.com/feature/5962406356320256) | [Spec](https://html.spec.whatwg.org/multipage/browsing-the-web.html#resetBCName)

---

### Reduce fingerprinting in Accept-Language header information

**Impact Level**: 🟡 Important

**What Changed**:  
Only the user's most preferred language is sent in the `Accept-Language` header and exposed in `navigator.languages`.

**Why It Matters**:  
Reduces fingerprinting surface and enhances user privacy.

**Implementation Guidance**:
- Do not rely on full language lists for localization or analytics.

**References**:  
[Tracking bug #1306905](https://issues.chromium.org/issues/1306905) | [ChromeStatus.com entry](https://chromestatus.com/feature/5188040623390720)

---

### Randomize TCP port allocation on Windows

**Impact Level**: 🟢 Nice-to-have

**What Changed**:  
Enables TCP port randomization on Windows 2020+ to reduce port reuse predictability.

**Why It Matters**:  
Improves network security and mitigates certain attack vectors.

**Implementation Guidance**:
- No action needed unless relying on predictable port allocation.

**References**:  
[Tracking bug #40744069](https://issues.chromium.org/issues/40744069) | [ChromeStatus.com entry](https://chromestatus.com/feature/5106900286570496)

---

### Faster background freezing on Android

**Impact Level**: 🟡 Important

**What Changed**:  
Reduces background freezing delay from five minutes to one minute on Android.

**Why It Matters**:  
Improves device resource management but may affect background tasks.

**Implementation Guidance**:
- Ensure critical background work completes within one minute.
- Use service workers for persistent background tasks.

**References**:  
[Tracking bug #435623337](https://issues.chromium.org/issues/435623337) | [ChromeStatus.com entry](https://chromestatus.com/feature/5386725031149568)

---

### Fire error event for Content Security Policy (CSP) blocked worker

**Impact Level**: 🟡 Important

**What Changed**:  
Chrome now fires an error event asynchronously for CSP-blocked workers, instead of throwing an exception.

**Why It Matters**:  
Aligns with the CSP spec and improves error handling consistency.

**Implementation Guidance**:
- Listen for error events on worker creation.
- Update error handling logic as needed.

**References**:  
[Tracking bug #41285169](https://issues.chromium.org/issues/41285169) | [ChromeStatus.com entry](https://chromestatus.com/feature/5177205656911872) | [Spec](https://www.w3.org/TR/CSP3/#fetch-integration)

---

### Audio level for RTC encoded frames

**Impact Level**: 🟢 Nice-to-have

**What Changed**:  
Exposes audio level metadata for encoded frames in WebRTC.

**Why It Matters**:  
Enables advanced audio processing and analytics in real-time communications.

**Implementation Guidance**:
- Use audio level data for adaptive UI or analytics.

**References**:  
[Tracking bug #418116079](https://issues.chromium.org/issues/418116079) | [ChromeStatus.com entry](https://chromestatus.com/feature/5206106602995712) | [Spec](https://w3c.github.io/webrtc-encoded-transform/#dom-rtcencodedaudioframemetadata-audiolevel)

---

### Web app scope extensions

**Impact Level**: 🟡 Important

**What Changed**:  
Adds `scope_extensions` to web app manifests, allowing apps to span multiple origins.

**Why It Matters**:  
Enables unified experiences across subdomains and domains.

**Implementation Guidance**:
- Configure `.well-known/web-app-origin-association` for associated origins.
- Update manifests to use `scope_extensions` as needed.

**References**:  
[Tracking bug #detail?id=1250011](https://issues.chromium.org/issues/detail?id=1250011) | [ChromeStatus.com entry](https://chromestatus.com/feature/5746537956114432) | [Spec](https://github.com/WICG/manifest-incubations/pull/113)

---

### Specification-compliant JSON MIME type detection

**Impact Level**: 🟡 Important

**What Changed**:  
Chrome now recognizes all valid JSON MIME types per WHATWG mimesniff spec.

**Why It Matters**:  
Ensures consistent JSON detection and interoperability.

**Implementation Guidance**:
- Use correct MIME types for JSON payloads.
- Test APIs for expected behavior with custom JSON types.

**References**:  
[ChromeStatus.com entry](https://chromestatus.com/feature/5470594816278528) | [Spec](https://mimesniff.spec.whatwg.org/#json-mime-type)

---

### WebGPU `core-features-and-limits`

**Impact Level**: 🟡 Important

**What Changed**:  
WebGPU adapters/devices now indicate support for core features and limits.

**Why It Matters**:  
Improves feature detection and compatibility for advanced graphics.

**Implementation Guidance**:
- Query for core feature support before using advanced WebGPU features.

**References**:  
[Tracking bug #418025721](https://issues.chromium.org/issues/418025721) | [ChromeStatus.com entry](https://chromestatus.com/feature/4744775089258496) | [Spec](https://gpuweb.github.io/gpuweb/#core-features-and-limits)

---

### Crash Reporting API: Specify `crash-reporting` to receive only crash reports

**Impact Level**: 🟢 Nice-to-have

**What Changed**:  
Allows developers to direct crash reports to a dedicated endpoint.

**Why It Matters**:  
Improves crash report management and separation from other reports.

**Implementation Guidance**:
- Update reporting endpoints to use `crash-reporting` as needed.

**References**:  
[Tracking bug #414723480](https://issues.chromium.org/issues/414723480) | [ChromeStatus.com entry](https://chromestatus.com/feature/5129218731802624) | [Spec](https://wicg.github.io/crash-reporting/#crash-reports-delivery-priority)

---

### Prompt API

**Impact Level**: 🟡 Important

**What Changed**:  
Introduces an API for multimodal AI interactions (text, image, audio), with structured output and Chrome Extension support (origin trial).

**Why It Matters**:  
Enables advanced AI-powered features and integrations directly in the browser.

**Implementation Guidance**:
- Participate in the origin trial to experiment with AI features.
- Consider privacy and enterprise policy implications.

**References**:  
[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/2533837740349325313) | [Tracking bug #417530643](https://issues.chromium.org/issues/417530643) | [ChromeStatus.com entry](https://chromestatus.com/feature/5134603979063296)

---

### Extended lifetime shared workers

**Impact Level**: 🟡 Important

**What Changed**:  
Adds `extendedLifetime: true` option to `SharedWorker`, allowing workers to persist after all clients unload (origin trial).

**Why It Matters**:  
Enables asynchronous work post-unload without service workers.

**Implementation Guidance**:
- Use extended lifetime for background tasks that outlive page sessions.
- Monitor for memory/resource impacts.

**References**:  
[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/3056255297124302849) | [Tracking bug #400473072](https://issues.chromium.org/issues/400473072) | [ChromeStatus.com entry](https://chromestatus.com/feature/5138641357373440)

---

### `SoftNavigation` performance entry

**Impact Level**: 🟡 Important

**What Changed**:  
Exposes soft navigation heuristics and new performance entries for user interactions and contentful paint (origin trial).

**Why It Matters**:  
Enables better measurement and optimization of single-page app navigation performance.

**Implementation Guidance**:
- Use new performance entries for SPA metrics and optimization.
- Participate in the origin trial for early access.

**References**:  
[Origin Trial](https://developer.chrome.com/origintrials#/view_trial/21392098230009857) | [Tracking bug #1338390](https://issues.chromium.org/issues/1338390) | [ChromeStatus.com entry](https://chromestatus.com/feature/5144837209194496) | [Spec](https://wicg.github.io/soft-navigations)

---

### Web Authentication immediate mediation

**Impact Level**: 🟢 Nice-to-have

**What Changed**:  
Adds a mediation mode for `navigator.credentials.get()` to show sign-in UI only if credentials are immediately available.

**Why It Matters**:  
Improves sign-in flows and user experience.

**Implementation Guidance**:
- Use immediate mediation for streamlined authentication.

**References**:  
[Tracking bug #408002783](https://issues.chromium.org/issues/408002783) | [ChromeStatus.com entry](https://chromestatus.com/feature/5164322780872704) | [Spec](https://github.com/w3c/webauthn/pull/2291)

---

### Full frame rate render blocking attribute

**Impact Level**: 🟢 Nice-to-have

**What Changed**:  
Adds a render blocking token to reduce frame rate during loading (origin trial).

**Why It Matters**:  
Improves resource allocation during heavy loads.

**Implementation Guidance**:
- Use the attribute to optimize loading performance.

**References**:  
[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/3578672853899280385) | [Tracking bug #397832388](https://issues.chromium.org/issues/397832388) | [ChromeStatus.com entry](https://chromestatus.com/feature/5207202081800192)

---

### WebGPU compatibility mode

**Impact Level**: 🟡 Important

**What Changed**:  
Adds a compatibility mode for WebGPU, supporting older graphics APIs (origin trial).

**Why It Matters**:  
Expands WebGPU reach to legacy hardware.

**Implementation Guidance**:
- Opt into compatibility mode for broader device support.
- Review constraints and test thoroughly.

**References**:  
[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/1489002626799370241) | [Tracking bug #40266903](https://issues.chromium.org/issues/40266903) | [ChromeStatus.com entry](https://chromestatus.com/feature/6436406437871616) | [Spec](https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md)

---

### Stop sending Purpose: prefetch header from prefetches and prerenders

**Impact Level**: 🟡 Important

**What Changed**:  
Removes legacy `Purpose: prefetch` header in favor of `Sec-Purpose`.

**Why It Matters**:  
Modernizes prefetch/prerender signaling and aligns with standards.

**Implementation Guidance**:
- Update server logic to rely on `Sec-Purpose` instead of `Purpose`.
- Test prefetch/prerender workflows for compatibility.

**References**:  
[Tracking bug #420724819](https://issues.chromium.org/issues/420724819) | [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320) | [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

---

### Remove support for macOS 11

**Impact Level**: 🔴 Critical

**What Changed**:  
Chrome 139 drops support for macOS 11; new installs require macOS 12+.

**Why It Matters**:  
Users on macOS 11 will no longer receive updates, posing security and compatibility risks.

**Implementation Guidance**:
- Advise users to upgrade to macOS 12+.
- Update documentation and support policies.

**References**:  
[ChromeStatus.com entry](https://chromestatus.com/feature/4504090090143744)

---

### Remove auto-detection of ISO-2022-JP charset in HTML

**Impact Level**: 🔴 Critical

**What Changed**:  
Removes auto-detection for ISO-2022-JP charset due to security issues and low usage.

**Why It Matters**:  
Mitigates security risks and aligns with other browsers.

**Implementation Guidance**:
- Explicitly declare charset in HTML documents.
- Audit legacy content for ISO-2022-JP reliance.

**References**:  
[known security issues](https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/) | [Tracking bug #40089450](https://issues.chromium.org/issues/40089450) | [ChromeStatus.com entry](https://chromestatus.com/feature/6576566521561088) | [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/) | [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0) | [Google Developers Site Policies](https://developers.google.com/site-policies)

---

**End of Digest**