digest_markdown/webplatform/Performance/chrome-139-stable-en.md

---

# Chrome 139 Performance Update Digest

## 1. Executive Summary

Chrome 139 introduces three notable updates in the Performance area: enhanced WebXR depth sensing customization, experimental soft navigation performance entries, and significantly faster background freezing for Android. These changes collectively improve resource management, developer observability, and real-time performance optimization capabilities across web applications.

## 2. Key Implications

### Technical Impact

- **Existing Implementations**: Applications leveraging WebXR depth sensing can now fine-tune buffer behavior for improved performance. Sites using navigation heuristics gain new observability tools. Android web apps must adapt to more aggressive background freezing.
- **New Capabilities**: Developers can request raw/smooth depth buffers in WebXR, observe soft navigation events via the performance timeline, and rely on quicker resource release for backgrounded Android pages.
- **Technical Debt Considerations**: Legacy code relying on longer background lifetimes on Android may require refactoring. Monitoring and analytics systems should be updated to utilize new performance entries.

## 3. Risk Assessment

**Critical Risks**:
- No breaking changes or direct security concerns identified in these features.

**Medium Risks**:
- **Deprecations**: The reduced background freezing window on Android may deprecate patterns relying on extended background activity.
- **Performance Impacts**: Misuse of new WebXR depth buffer options could lead to suboptimal performance if not properly configured.

## 4. Recommended Actions

### Immediate Actions

- Audit Android web apps for background activity dependencies; refactor as needed for the new 1-minute freeze window.
- Experiment with the `SoftNavigation` performance entry via Origin Trial to enhance navigation analytics.
- Review WebXR depth sensing usage and update buffer requests for optimal performance.

### Short-term Planning

- Update monitoring and analytics dashboards to incorporate new performance entries.
- Educate development teams on the implications of faster background freezing for Android.
- Evaluate and document best practices for WebXR depth buffer configuration.

### Long-term Strategy

- Track adoption and feedback for `SoftNavigation` and WebXR depth sensing improvements.
- Monitor Chrome’s roadmap for further changes to background process management.
- Plan for broader rollout and standardization of experimental features as they stabilize.

## 5. Feature Analysis

---

### WebXR depth sensing performance improvements

**Impact Level**: 🟡 Important

**What Changed**:
Exposes several new mechanisms to customize the behavior of the depth sensing feature within a WebXR session, aiming to improve the performance of generating or consuming the depth buffer. Developers can now request raw or smooth depth buffers and adjust other parameters for optimized resource usage.

**Why It Matters**:
Fine-grained control over depth buffer behavior enables developers to balance performance and quality in immersive experiences, reducing latency and resource consumption for AR/VR applications.

**Implementation Guidance**:
- Review current WebXR depth sensing usage and determine if raw or smooth buffers are more appropriate for your use case.
- Test performance impacts of different buffer configurations in real-world scenarios.
- Monitor for updates in the spec and browser support.

**References**:
- [Tracking bug #410607163](https://issues.chromium.org/issues/410607163)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5074096916004864)
- [Spec](https://immersive-web.github.io/depth-sensing)

---

### `SoftNavigation` performance entry

**Impact Level**: 🟡 Important

**What Changed**:
Introduces experimental soft navigation heuristics to web developers via `PerformanceObserver` and the performance timeline. Reports two new performance entries: `soft-navigation` (for user interactions that navigate the page) and a new `timeOrigin` to help slice timing data for these events.

**Why It Matters**:
Provides developers with deeper insight into navigation events that do not trigger full page reloads, enabling more accurate performance measurement and optimization for single-page applications and dynamic navigation patterns.

**Implementation Guidance**:
- Enroll in the Origin Trial to test and integrate `SoftNavigation` entries.
- Update performance monitoring tools to capture and analyze these new entries.
- Use the new `timeOrigin` to segment and optimize navigation-related metrics.

**References**:
- [Origin Trial](https://developer.chrome.com/origintrials#/view_trial/21392098230009857)
- [Tracking bug #1338390](https://issues.chromium.org/issues/1338390)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5144837209194496)
- [Spec](https://wicg.github.io/soft-navigations)

---

### Faster background freezing on Android

**Impact Level**: 🔴 Critical

**What Changed**:
Reduces the time before background pages and associated workers are frozen on Android from five minutes to one minute, accelerating resource release and improving device performance.

**Why It Matters**:
This change significantly impacts web apps that rely on background activity, such as periodic sync or deferred processing. Developers must ensure critical tasks complete within the new, shorter window to avoid unexpected interruptions.

**Implementation Guidance**:
- Audit background tasks in Android web apps to ensure completion within one minute.
- Refactor long-running background processes to fit the new freeze timeline.
- Monitor user experience for any regressions related to background freezing.

**References**:
- [Tracking bug #435623337](https://issues.chromium.org/issues/435623337)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5386725031149568)

---