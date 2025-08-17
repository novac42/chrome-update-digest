digest_markdown/webplatform/network/chrome-139-stable-en.md

---

# Chrome 139 Stable – Network Area Update Digest

## 1. Executive Summary

Chrome 139 introduces two significant network-related updates: a reduction in fingerprinting via the `Accept-Language` header and the randomization of TCP port allocation on Windows. These changes enhance user privacy and network security, aligning with modern web standards and best practices.

## 2. Key Implications

### Technical Impact

- **Existing Implementations**: Applications relying on detailed `Accept-Language` headers or assuming deterministic TCP port allocation may require updates.
- **New Capabilities**: Improved privacy for users and enhanced security against certain network attacks.
- **Technical Debt**: Legacy code that parses or depends on full language lists or static port behavior should be audited and refactored.

## 3. Risk Assessment

**Critical Risks**:
- **Breaking Changes**: Reduced `Accept-Language` header granularity may affect localization or content negotiation logic.
- **Security Considerations**: TCP port randomization may impact systems that expect predictable port assignment.

**Medium Risks**:
- **Deprecations**: Implicit deprecation of detailed language negotiation via headers.
- **Performance Impacts**: Minimal, but possible edge cases in network stack behavior on Windows.

## 4. Recommended Actions

### Immediate Actions

- Audit server-side logic that parses `Accept-Language` headers for assumptions about language list length or order.
- Review network diagnostics and tooling for compatibility with randomized TCP port allocation.

### Short-term Planning

- Update localization and content negotiation strategies to rely less on granular `Accept-Language` data.
- Monitor network error logs on Windows deployments for unexpected port allocation issues.

### Long-term Strategy

- Advocate for privacy-preserving defaults in all network-facing features.
- Plan for further reductions in passive fingerprinting surfaces and continued hardening of network stack behaviors.

## 5. Feature Analysis

### Reduce fingerprinting in Accept-Language header information

**Impact Level**: 🔴 Critical

**What Changed**:
Reduces the amount of information the `Accept-Language` header value string exposes in HTTP requests and in `navigator.languages`. Instead of sending a full list of the user's preferred languages on every HTTP request using the `Accept-Language` header, Chrome only sends the user's most preferred language.

**Why It Matters**:
This change significantly reduces the browser's fingerprinting surface, making it harder for trackers to uniquely identify users based on their language preferences. It also aligns with privacy best practices and regulatory expectations.

**Implementation Guidance**:
- Review any server-side logic that depends on the full list of languages from the `Accept-Language` header.
- Update localization and content negotiation mechanisms to gracefully handle receiving only the primary language.
- Communicate changes to localization teams and update documentation accordingly.

**References**:
- [Tracking bug #1306905](https://issues.chromium.org/issues/1306905)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5188040623390720)

---

### Randomize TCP port allocation on Windows

**Impact Level**: 🟡 Important

**What Changed**:
Enables TCP port randomization on versions of Windows (2020 or later) where rapid port re-use is not expected to cause issues. This mitigates the risk of port collision and certain classes of network attacks related to predictable port assignment.

**Why It Matters**:
Randomizing TCP port allocation increases security by making it more difficult for attackers to predict which ports will be used, reducing the risk of port hijacking and related exploits.

**Implementation Guidance**:
- Test networked applications on Windows 2020+ for compatibility with randomized port allocation.
- Update any scripts or monitoring tools that assume deterministic port assignment.
- Monitor for any unexpected connection failures or timeouts related to port allocation.

**References**:
- [Tracking bug #40744069](https://issues.chromium.org/issues/40744069)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5106900286570496)

---