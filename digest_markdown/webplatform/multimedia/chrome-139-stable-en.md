Save to: `digest_markdown/webplatform/Multimedia/chrome-139-stable-en.md`

---

# Chrome 139 Stable – Multimedia Area Digest

## 1. Executive Summary

Chrome 139 introduces a significant update in the Multimedia domain: **Web Authentication immediate mediation** for `navigator.credentials.get()`. This feature refines credential mediation by immediately displaying browser sign-in UI when a passkey or password is available, otherwise rejecting the request. This change enhances user experience and security for web authentication flows, especially in multimedia-rich applications requiring seamless sign-in.

## 2. Key Implications

### Technical Impact

- **Existing Implementations**: Applications using `navigator.credentials.get()` must handle the new immediate mediation mode, which alters the authentication flow by either instantly prompting the user or rejecting the request if no credentials are available.
- **New Capabilities**: Developers can now offer a more streamlined and predictable sign-in experience, reducing unnecessary UI prompts and improving authentication reliability.
- **Technical Debt**: Legacy authentication flows may require refactoring to accommodate the new mediation behavior and error handling (`NotAllowedError`).

## 3. Risk Assessment

**Critical Risks**:
- **Breaking Changes**: Applications not handling the new mediation mode or `NotAllowedError` may experience authentication failures or degraded user experience.
- **Security Considerations**: Immediate mediation reduces exposure to credential enumeration attacks by only prompting when credentials are present.

**Medium Risks**:
- **Deprecations**: Older mediation modes may become less relevant, requiring migration.
- **Performance Impacts**: The change may slightly affect authentication latency due to immediate UI invocation, but overall impact is minimal.

## 4. Recommended Actions

### Immediate Actions

- Audit all uses of `navigator.credentials.get()` for compatibility with immediate mediation.
- Update error handling to gracefully manage `NotAllowedError`.
- Test authentication flows to ensure correct UI behavior.

### Short-term Planning

- Refactor authentication logic to leverage immediate mediation for improved UX.
- Monitor user feedback and authentication metrics post-update.
- Prepare migration guides for teams using legacy mediation modes.

### Long-term Strategy

- Track future changes to Web Authentication specifications and Chromium implementation.
- Invest in adaptive authentication flows that optimize for both security and user experience.
- Collaborate with standards bodies to influence further improvements in credential mediation.

## 5. Feature Analysis

### Web Authentication immediate mediation

**Impact Level**: 🟡 Important

**What Changed**:
A mediation mode for `navigator.credentials.get()` now causes the browser sign-in UI to be displayed immediately if a passkey or password for the site is known to the browser. If no such credential is available, the request is rejected with `NotAllowedError`.

**Why It Matters**:
This change streamlines the authentication process, reducing unnecessary prompts and improving security by only engaging the user when credentials are present. It is particularly relevant for multimedia applications that require fast, reliable sign-in to access protected content or services.

**Implementation Guidance**:
- Update authentication flows to use the new mediation mode.
- Ensure robust error handling for `NotAllowedError`.
- Test across devices and browsers to confirm consistent behavior.
- Communicate changes to users if authentication UI behavior differs from previous versions.

**References**:
- [Tracking bug #408002783](https://issues.chromium.org/issues/408002783)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5164322780872704)
- [Spec](https://github.com/w3c/webauthn/pull/2291)

---