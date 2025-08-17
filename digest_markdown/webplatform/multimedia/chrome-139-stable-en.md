Save to: digest_markdown/webplatform/Multimedia/chrome-139-stable-en.md

---

# Chrome 139 Multimedia Update Digest

## 1. Executive Summary

Chrome 139 introduces a significant update in the Multimedia domain with the addition of the "Web Authentication immediate mediation" feature. This enhancement to the Web Authentication API enables a more streamlined and user-friendly authentication flow by immediately displaying browser sign-in UI when credentials are available, or promptly rejecting the request otherwise. This change impacts both security and user experience for web applications leveraging passkeys or passwords.

## 2. Key Implications

### Technical Impact

- **Effect on Existing Implementations**: Applications using `navigator.credentials.get()` can now opt into immediate mediation, altering the authentication flow. Existing implementations that do not specify this mode remain unaffected, but those adopting it must handle the new rejection behavior.
- **New Capabilities**: Developers can provide a more deterministic and responsive authentication experience, reducing unnecessary UI prompts and improving perceived performance.
- **Technical Debt Considerations**: Teams relying on legacy authentication flows should evaluate migration paths to leverage immediate mediation for better UX and security posture.

## 3. Risk Assessment

**Critical Risks**:
- **Breaking Changes**: None for existing code unless immediate mediation is explicitly adopted.
- **Security Considerations**: The feature tightens control over credential mediation, potentially reducing phishing vectors by minimizing unnecessary credential prompts.

**Medium Risks**:
- **Deprecations**: None directly, but teams should monitor for future deprecations of older mediation modes.
- **Performance Impacts**: Positive impact expected due to reduced UI invocation and faster rejection when no credentials are available.

## 4. Recommended Actions

### Immediate Actions

- Review authentication flows that use `navigator.credentials.get()` and assess the applicability of immediate mediation.
- Update user interface logic to handle `NotAllowedError` rejections gracefully when no credentials are available.

### Short-term Planning

- Plan for user testing to evaluate the impact of immediate mediation on authentication success rates and user satisfaction.
- Monitor Chromium and W3C discussions for further refinements or best practices regarding this mediation mode.

### Long-term Strategy

- Track adoption metrics and feedback to inform broader migration to modern Web Authentication flows.
- Prepare for potential deprecation of legacy mediation modes and ensure codebases remain aligned with evolving standards.

## 5. Feature Analysis

### Web Authentication immediate mediation

**Impact Level**: 🟡 Important

**What Changed**:
A new mediation mode for `navigator.credentials.get()` is introduced. When enabled, the browser will immediately display the sign-in UI if a passkey or password is available for the site. If no such credential is present, the promise is rejected with `NotAllowedError` without showing the UI.

**Why It Matters**:
This feature enables a more predictable and efficient authentication experience. Users are only prompted when credentials are available, reducing confusion and unnecessary UI interruptions. It also enhances security by limiting exposure to credential prompts.

**Implementation Guidance**:
- Evaluate current usage of `navigator.credentials.get()` and consider adopting immediate mediation where appropriate.
- Ensure error handling logic is updated to manage `NotAllowedError` rejections.
- Test authentication flows to confirm that user experience is improved and edge cases are handled.

**References**:
- [Tracking bug #408002783](https://issues.chromium.org/issues/408002783)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5164322780872704)
- [Spec](https://github.com/w3c/webauthn/pull/2291)

---