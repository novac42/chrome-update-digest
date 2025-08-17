---
layout: default
title: Chrome 139 Devices Update Digest
---

---

# Chrome 139 Devices Update Digest

## 1. Executive Summary

Chrome 139 introduces significant advancements in the Devices area, focusing on enhanced performance for WebXR depth sensing and the addition of on-device speech recognition via the Web Speech API. These updates empower developers to build more responsive, privacy-preserving, and performant device-integrated web experiences.

## 2. Key Implications

### Technical Impact

- **WebXR Depth Sensing**: Developers gain granular control over depth buffer behavior, enabling optimized performance for AR/VR applications.
- **On-device Web Speech API**: Speech recognition can now be performed locally, reducing latency and enhancing privacy by avoiding third-party data transmission.
- **New Capabilities**: Customizable depth buffer modes and local speech recognition unlock new use cases and improve user trust.
- **Technical Debt**: Existing implementations may require updates to leverage new APIs and performance optimizations.

## 3. Risk Assessment

**Critical Risks**:
- No breaking changes identified.
- Security: On-device speech recognition reduces data exposure, but developers must ensure proper handling of sensitive data locally.

**Medium Risks**:
- Potential performance regressions if new depth sensing options are misconfigured.
- Feature detection and fallback logic may be needed for speech API availability across devices.

## 4. Recommended Actions

### Immediate Actions

- Evaluate and integrate new WebXR depth sensing options for AR/VR projects.
- Update speech-enabled web applications to detect and utilize on-device recognition where available.

### Short-term Planning

- Benchmark performance and privacy improvements from these features.
- Implement robust feature detection and graceful fallback for speech recognition.

### Long-term Strategy

- Monitor evolving specifications and browser support for device APIs.
- Plan for broader adoption of privacy-preserving, on-device processing capabilities.

## 5. Feature Analysis

### WebXR depth sensing performance improvements

**Impact Level**: 🟡 Important

**What Changed**:
Exposes several new mechanisms to customize the behavior of the depth sensing feature within a WebXR session, aiming to improve the performance of generating or consuming the depth buffer. Key mechanisms include the ability to request raw or smooth depth buffers and additional configuration options.

**Why It Matters**:
Fine-grained control over depth buffer processing allows developers to optimize AR/VR experiences for performance and quality, adapting to device capabilities and application needs.

**Implementation Guidance**:
- Review the new depth buffer configuration options in the WebXR API.
- Profile AR/VR applications to determine optimal settings for raw vs. smooth depth buffers.
- Test across a range of devices to ensure consistent performance and quality.

**References**:
- [Tracking bug #410607163](https://issues.chromium.org/issues/410607163)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5074096916004864)
- [Spec](https://immersive-web.github.io/depth-sensing)

---

### On-device Web Speech API

**Impact Level**: 🟡 Important

**What Changed**:
Adds on-device speech recognition support to the Web Speech API, enabling websites to process speech locally without sending audio or transcripts to third-party services. Websites can query the availability of on-device recognition for specific languages and prompt users accordingly.

**Why It Matters**:
This feature enhances user privacy and reduces latency for speech-enabled applications, making voice interactions more secure and responsive.

**Implementation Guidance**:
- Update speech-enabled applications to detect and prefer on-device recognition when available.
- Provide clear user messaging about privacy benefits.
- Implement fallback mechanisms for devices or languages where on-device recognition is not supported.

**References**:
- [ChromeStatus.com entry](https://chromestatus.com/feature/6090916291674112)
- [Spec](https://webaudio.github.io/web-speech-api)

---