---
layout: default
title: Chrome 139 Deprecation Update Digest
---

Save to: digest_markdown/webplatform/deprecation/chrome-139-stable-en.md

---

# Chrome 139 Deprecation Update Digest

## 1. Executive Summary

Chrome 139 introduces several significant deprecations impacting web platform compatibility and security. The most notable changes include the removal of the legacy `Purpose: prefetch` header in favor of the `Sec-Purpose` header, the end of support for macOS 11, and the discontinuation of auto-detection for the `ISO-2022-JP` charset in HTML. These updates aim to streamline browser behavior, enhance security, and encourage migration to modern standards.

## 2. Key Implications

### Technical Impact

- **Existing Implementations**: Sites relying on the deprecated `Purpose: prefetch` header or charset auto-detection for `ISO-2022-JP` may experience compatibility issues. Chrome will no longer update on macOS 11, potentially exposing users to security risks.
- **New Capabilities**: The shift to `Sec-Purpose` header aligns Chrome with modern navigation speculation standards, improving interoperability and security.
- **Technical Debt**: Continued reliance on deprecated features increases maintenance burden and security exposure. Migration is necessary to avoid future breakages.

## 3. Risk Assessment

**Critical Risks**:
- **Breaking Changes**: Removal of support for macOS 11 and charset auto-detection for `ISO-2022-JP` may break legacy workflows or content.
- **Security Considerations**: The removal of insecure charset auto-detection addresses known vulnerabilities.

**Medium Risks**:
- **Deprecations**: The transition from `Purpose: prefetch` to `Sec-Purpose` may require backend and infrastructure updates.
- **Performance Impacts**: Minimal, but improper handling of headers or charsets could degrade user experience.

## 4. Recommended Actions

### Immediate Actions

- Audit codebases for usage of the `Purpose: prefetch` header and update to use `Sec-Purpose`.
- Identify any dependencies on `ISO-2022-JP` charset auto-detection and migrate to explicit charset declarations.
- Notify macOS 11 users of end-of-support and encourage OS upgrades.

### Short-term Planning

- Update documentation and developer guides to reflect deprecations.
- Monitor user reports for issues related to these changes.
- Plan phased rollouts or feature flagging for header changes to minimize disruption.

### Long-term Strategy

- Establish processes for early detection of upcoming deprecations.
- Encourage adoption of modern web standards and proactive migration.
- Regularly review platform support policies to minimize technical debt.

## 5. Feature Analysis

### Stop sending Purpose: prefetch header from prefetches and prerenders

**Impact Level**: 🟡 Important

**What Changed**:
Chrome will stop sending the legacy `Purpose: prefetch` header for prefetch and prerender requests. The modern `Sec-Purpose` header will be used instead. This change is controlled by a feature flag/kill switch to mitigate compatibility issues during rollout.

**Why It Matters**:
This aligns Chrome with current navigation speculation standards, reduces legacy header usage, and improves security and interoperability with other browsers and services.

**Implementation Guidance**:
- Update server-side logic to recognize and handle the `Sec-Purpose` header instead of `Purpose: prefetch`.
- Test prefetch and prerender workflows to ensure compatibility.
- Monitor for any unexpected behavior during the transition period.

**References**:
- [Tracking bug #420724819](https://issues.chromium.org/issues/420724819)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320)
- [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

---

### Remove support for macOS 11

**Impact Level**: 🔴 Critical

**What Changed**:
Chrome 138 was the last release to support macOS 11. Starting with Chrome 139, macOS 11 is no longer supported. Chrome will continue to function on macOS 11 but will not receive updates, and users will see a warning infobar.

**Why It Matters**:
Users on unsupported OS versions will not receive security or feature updates, increasing their exposure to vulnerabilities and compatibility issues.

**Implementation Guidance**:
- Inform users and stakeholders about the end of support for macOS 11.
- Encourage and assist users in upgrading to a supported macOS version.
- Update internal documentation and support materials accordingly.

**References**:
- [ChromeStatus.com entry](https://chromestatus.com/feature/4504090090143744)

---

### Remove auto-detection of `ISO-2022-JP` charset in HTML

**Impact Level**: 🟡 Important

**What Changed**:
Chrome 139 removes support for auto-detecting the `ISO-2022-JP` charset in HTML documents due to known security issues and low usage. Explicit charset declarations are now required.

**Why It Matters**:
This change mitigates security vulnerabilities associated with charset auto-detection and aligns Chrome with Safari, which does not support this feature.

**Implementation Guidance**:
- Audit and update any web content relying on auto-detection of `ISO-2022-JP` to use explicit charset declarations (e.g., `<meta charset="ISO-2022-JP">`).
- Test affected pages to ensure correct rendering and encoding.
- Communicate changes to content authors and localization teams.

**References**:
- [known security issues](https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/)
- [Tracking bug #40089450](https://issues.chromium.org/issues/40089450)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6576566521561088)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)

---