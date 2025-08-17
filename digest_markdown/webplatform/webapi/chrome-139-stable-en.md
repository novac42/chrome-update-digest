---
layout: default
title: Chrome 139 Web API Update Digest (Stable)
---

Save to: digest_markdown/webplatform/Web API/chrome-139-stable-en.md

---

# Chrome 139 Web API Update Digest (Stable)

## 1. Executive Summary

Chrome 139 introduces several significant updates in the Web API area, including enhanced web app manifest capabilities for multi-origin apps, improved standards compliance for JSON MIME type detection, expanded WebGPU feature support, and more granular crash reporting endpoints. These changes collectively advance interoperability, developer control, and platform robustness.

## 2. Key Implications

### Technical Impact

- **Existing Implementations**: Minor adjustments may be needed for apps relying on legacy JSON MIME type detection or crash reporting endpoints.
- **New Capabilities**: 
  - Web apps can now span multiple origins via `scope_extensions`.
  - WebGPU gains explicit support for core features and limits.
  - Developers can target crash reports to dedicated endpoints.
- **Technical Debt**: 
  - Legacy workarounds for JSON MIME sniffing and crash report filtering can be retired.
  - Multi-origin app architectures can be streamlined.

## 3. Risk Assessment

**Critical Risks**:
- No breaking changes identified, but incorrect use of new manifest fields or crash reporting endpoints could lead to misconfiguration.
- Security: Extending app scope across origins increases the need for robust origin association and validation.

**Medium Risks**:
- Deprecation of non-standard JSON MIME handling may affect edge-case integrations.
- Performance impacts are minimal, but multi-origin apps may introduce complexity in resource management.

## 4. Recommended Actions

### Immediate Actions

- Review and update web app manifests to leverage `scope_extensions` where multi-origin support is needed.
- Audit JSON MIME type handling in APIs and ensure compliance with the updated detection logic.
- Specify the `crash-reporting` endpoint if you require only crash reports.

### Short-term Planning

- Refactor legacy code that relied on non-standard JSON MIME types or broad crash reporting endpoints.
- Evaluate WebGPU usage and update feature detection logic to utilize `core-features-and-limits`.

### Long-term Strategy

- Monitor adoption and feedback on multi-origin web app patterns.
- Track further WebGPU and crash reporting API evolutions for future-proofing.
- Continue aligning with evolving web standards for MIME type handling and manifest specifications.

## 5. Feature Analysis

---

### Web app scope extensions

**Impact Level**: 🟡 Important

**What Changed**:
Adds a `scope_extensions` field to the web app manifest, allowing web apps to extend their scope to other origins. This enables sites controlling multiple subdomains or top-level domains to present as a single web app. Association confirmation via a `.well-known` file is required.

**Why It Matters**:
This change simplifies the user experience and developer workflow for organizations managing multi-origin web apps, enabling seamless navigation and unified app identity across domains.

**Implementation Guidance**:
- Update your web app manifest to include `scope_extensions` if your app spans multiple origins.
- Ensure all listed origins implement the required `.well-known` association file.
- Test navigation and install flows across all intended origins.

**References**:
- [Tracking bug #detail?id=1250011](https://issues.chromium.org/issues/detail?id=1250011)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5746537956114432)
- [Spec](https://github.com/WICG/manifest-incubations/pull/113)

---

### Specification-compliant JSON MIME type detection

**Impact Level**: 🟡 Important

**What Changed**:
Chrome now recognizes all valid JSON MIME types per the WHATWG mimesniff specification, including any subtype ending with `+json`, as well as `application/json` and `text/json`. This ensures consistent behavior for web APIs relying on JSON detection.

**Why It Matters**:
This update improves interoperability and standards compliance, reducing the risk of subtle bugs when handling JSON payloads with non-standard MIME types.

**Implementation Guidance**:
- Audit your API endpoints and client code for reliance on legacy or non-standard JSON MIME types.
- Update server responses to use compliant MIME types where necessary.
- Test integrations with third-party APIs for compatibility.

**References**:
- [ChromeStatus.com entry](https://chromestatus.com/feature/5470594816278528)
- [Spec](https://mimesniff.spec.whatwg.org/#json-mime-type)

---

### WebGPU `core-features-and-limits`

**Impact Level**: 🟢 Nice-to-have

**What Changed**:
Introduces the `core-features-and-limits` feature, indicating that a WebGPU adapter and device support the core features and limits defined in the specification.

**Why It Matters**:
This provides developers with a reliable way to detect and utilize the baseline capabilities of WebGPU, improving cross-platform consistency and enabling more robust feature detection.

**Implementation Guidance**:
- Update WebGPU feature detection logic to check for `core-features-and-limits`.
- Adjust fallback or progressive enhancement strategies based on feature support.

**References**:
- [Tracking bug #418025721](https://issues.chromium.org/issues/418025721)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4744775089258496)
- [Spec](https://gpuweb.github.io/gpuweb/#core-features-and-limits)

---

### Crash Reporting API: Specify `crash-reporting` to receive only crash reports

**Impact Level**: 🟡 Important

**What Changed**:
Developers can now specify the `crash-reporting` endpoint to receive only crash reports, rather than the default endpoint which aggregates multiple report types. A separate URL can be supplied to the well-known endpoint for this purpose.

**Why It Matters**:
This change allows for more precise monitoring and handling of crash reports, reducing noise and improving incident response workflows.

**Implementation Guidance**:
- Update your crash reporting configuration to use the `crash-reporting` endpoint if you only require crash data.
- Ensure your backend is prepared to handle reports from the new endpoint.
- Monitor for any changes in report volume or content.

**References**:
- [Tracking bug #414723480](https://issues.chromium.org/issues/414723480)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5129218731802624)
- [Spec](https://wicg.github.io/crash-reporting/#crash-reports-delivery-priority)

---