Save to: digest_markdown/webplatform/Performance/chrome-139-stable-en.md

---

# Chrome 139 Performance Update Digest

## 1. Executive Summary

Chrome 139 introduces significant enhancements in the Performance area, focusing on both immersive web experiences and resource management on Android. Notably, WebXR depth sensing now offers customizable mechanisms to optimize depth buffer handling, directly improving performance for AR/VR applications. Additionally, background page freezing on Android is now triggered after one minute instead of five, leading to more aggressive resource savings for backgrounded tabs and workers.

## 2. Key Implications

### Technical Impact

- **Existing Implementations**: WebXR applications can now fine-tune depth sensing for better performance, potentially requiring updates to leverage new buffer options. Android web apps may see background tasks suspended sooner, impacting long-running background operations.
- **New Capabilities**: Developers gain granular control over WebXR depth buffer behavior, enabling tailored performance optimizations. Android users benefit from improved device resource utilization.
- **Technical Debt**: Applications relying on extended background execution on Android may need refactoring to handle earlier freezing. WebXR apps should audit depth buffer usage to maximize new performance options.

## 3. Risk Assessment

**Critical Risks**:
- No breaking changes or direct security concerns identified for these features.

**Medium Risks**:
- **Deprecations**: None announced, but earlier background freezing may indirectly deprecate patterns relying on longer background activity.
- **Performance Impacts**: Aggressive background freezing could disrupt background tasks if not handled properly. WebXR depth buffer changes may require testing to avoid regressions.

## 4. Recommended Actions

### Immediate Actions

- Review and update WebXR applications to utilize new depth buffer customization options for optimal performance.
- Audit Android web apps for background activity dependencies; ensure critical tasks complete within one minute or migrate to foreground execution.

### Short-term Planning

- Monitor user feedback and performance metrics for both WebXR and Android background freezing changes.
- Update documentation and onboarding materials to reflect new background freezing behavior on Android.

### Long-term Strategy

- Invest in adaptive background task management strategies for Android to future-proof against further reductions in background execution time.
- Continue to track WebXR performance features and align application architecture with evolving depth sensing capabilities.

## 5. Feature Analysis

### WebXR depth sensing performance improvements

**Impact Level**: 🟡 Important

**What Changed**:
Exposes several new mechanisms to customize the behavior of the depth sensing feature within a WebXR session, with the goal of improving the performance of the generation or consumption of the depth buffer. Key mechanisms include the ability to request raw or smooth depth buffers and additional configuration options.

**Why It Matters**:
This change empowers developers to optimize AR/VR experiences by selecting the most suitable depth buffer type for their use case, reducing unnecessary processing and improving frame rates or battery life.

**Implementation Guidance**:
- Evaluate current WebXR depth sensing usage and determine if raw or smooth buffers are more appropriate for your application.
- Update session initialization code to request the desired buffer type.
- Test performance and visual quality impacts across supported devices.

**References**:
- [Tracking bug #410607163](https://issues.chromium.org/issues/410607163)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5074096916004864)
- [Spec](https://immersive-web.github.io/depth-sensing)

---

### Faster background freezing on Android

**Impact Level**: 🟡 Important

**What Changed**:
Shortens the time to freezing background pages (and associated workers) from five minutes to one minute on Android.

**Why It Matters**:
This change significantly reduces background resource usage, improving device battery life and system performance. However, it may disrupt applications that rely on extended background processing.

**Implementation Guidance**:
- Identify any background tasks in your Android web applications that require more than one minute to complete.
- Refactor critical background operations to complete within the new one-minute window or trigger them in the foreground.
- Monitor for unexpected suspensions or user experience regressions.

**References**:
- [Tracking bug #435623337](https://issues.chromium.org/issues/435623337)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5386725031149568)

---