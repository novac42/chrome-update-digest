digest_markdown/webplatform/deprecation/chrome-139-stable-en.md
---

# Chrome Update Analyzer – Deprecation Area Digest

## Chrome 139 (Stable) – Deprecation

---

### 1. Executive Summary

Chrome 139 introduces several notable deprecations impacting web platform compatibility and security. Key changes include the removal of the legacy `Purpose: prefetch` header in favor of the standardized `Sec-Purpose` header, the end of support for macOS 11, and the discontinuation of auto-detection for the `ISO-2022-JP` charset in HTML. These updates aim to streamline browser behavior, enhance security, and reduce technical debt.

---

### 2. Key Implications

#### Technical Impact

- **Header Changes**: Prefetch and prerender requests will no longer send the legacy `Purpose: prefetch` header, relying solely on the `Sec-Purpose` header. This may affect server-side logic that depends on the old header.
- **Platform Support**: Chrome will not update on macOS 11, requiring users to upgrade their OS for continued browser updates.
- **Charset Detection**: Removal of auto-detection for `ISO-2022-JP` reduces attack surface but may affect legacy content relying on this encoding.

#### New Capabilities

- Improved alignment with web standards (Sec-Purpose header).
- Enhanced security posture by removing risky charset auto-detection.

#### Technical Debt Considerations

- Legacy code relying on deprecated headers or charset detection should be refactored.
- Infrastructure must be updated to support only currently supported OS versions.

---

### 3. Risk Assessment

**Critical Risks:**

- **Breaking Changes**: Removal of the `Purpose: prefetch` header and charset auto-detection may break integrations or legacy content.
- **Security Considerations**: The charset change addresses known vulnerabilities, reducing risk for users.

**Medium Risks:**

- **Deprecations**: End of macOS 11 support may leave some users on outdated, insecure browser versions.
- **Performance Impacts**: Minimal, but server-side logic may need updates to avoid unnecessary processing.

---

### 4. Recommended Actions

#### Immediate Actions

- Audit server logic for reliance on the `Purpose: prefetch` header; migrate to `Sec-Purpose`.
- Notify macOS 11 users of end-of-support and encourage OS upgrades.
- Review any content or systems relying on `ISO-2022-JP` auto-detection.

#### Short-term Planning

- Update documentation and developer guides to reflect header and charset changes.
- Monitor user feedback and error logs for issues related to these deprecations.

#### Long-term Strategy

- Continue to track browser deprecations and proactively refactor legacy code.
- Plan for OS support lifecycle in deployment strategies.

---

### 5. Feature Analysis

---

### Stop sending Purpose: prefetch header from prefetches and prerenders

**Impact Level**: 🔴 Critical

**What Changed**:
Chrome will stop sending the legacy `Purpose: prefetch` header for prefetch and prerender requests, transitioning fully to the standardized `Sec-Purpose` header. This change is controlled by a feature flag/kill switch to mitigate compatibility issues.

**Why It Matters**:
This deprecation aligns Chrome with modern web standards and reduces ambiguity in request handling. Server-side logic depending on the old header may break, requiring updates.

**Implementation Guidance**:
- Update server logic to detect and handle the `Sec-Purpose` header instead of `Purpose: prefetch`.
- Test prefetch and prerender workflows to ensure compatibility.
- Monitor for any regressions or unexpected behavior.

**References**:
- [Tracking bug #420724819](https://issues.chromium.org/issues/420724819)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320)
- [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

---

### Remove support for macOS 11

**Impact Level**: 🟡 Important

**What Changed**:
Chrome 139 drops support for macOS 11. Users on this OS will not receive further updates and will see a warning infobar. Updating Chrome requires upgrading to a supported macOS version.

**Why It Matters**:
Ensures Chrome users benefit from the latest security and feature updates. Organizations must plan for OS upgrades to maintain browser support.

**Implementation Guidance**:
- Communicate the change to affected users and stakeholders.
- Update deployment and support documentation.
- Encourage migration to supported macOS versions.

**References**:
- [ChromeStatus.com entry](https://chromestatus.com/feature/4504090090143744)

---

### Remove auto-detection of `ISO-2022-JP` charset in HTML

**Impact Level**: 🔴 Critical

**What Changed**:
Chrome no longer auto-detects the `ISO-2022-JP` charset in HTML documents due to known security issues and low usage. This brings Chrome in line with Safari, which does not support this auto-detection.

**Why It Matters**:
Addresses security vulnerabilities associated with charset auto-detection, reducing risk for users and developers. May impact legacy content relying on this encoding.

**Implementation Guidance**:
- Audit and update any legacy content or systems that depend on `ISO-2022-JP` auto-detection.
- Explicitly specify charset in HTML documents where necessary.
- Monitor for encoding-related issues post-update.

**References**:
- [known security issues](https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/)
- [Tracking bug #40089450](https://issues.chromium.org/issues/40089450)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6576566521561088)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)

---

**End of Digest**