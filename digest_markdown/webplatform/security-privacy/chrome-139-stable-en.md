Save to: digest_markdown/webplatform/Security-Privacy/chrome-139-stable-en.md

---

# Chrome 139 Security-Privacy Update Digest

## 1. Executive Summary

Chrome 139 introduces a significant update in the Security-Privacy domain: error events are now fired asynchronously when Content Security Policy (CSP) blocks the creation of a Worker or SharedWorker. This change aligns Chrome's behavior with the CSP specification, improving consistency and predictability for developers handling worker instantiation under restrictive security policies.

## 2. Key Implications

### Technical Impact

- **Existing Implementations**: Applications relying on synchronous exceptions for CSP-blocked workers must update their error handling logic to respond to asynchronous error events instead.
- **New Capabilities**: Developers can now reliably listen for error events when CSP blocks worker creation, enabling more robust fallback and logging strategies.
- **Technical Debt**: Legacy code that expects exceptions may fail silently or behave unpredictably. Refactoring is required to ensure compatibility with the new event-driven error model.

## 3. Risk Assessment

**Critical Risks**:
- **Breaking Changes**: Code expecting synchronous exceptions for CSP-blocked workers will not function as before. This may lead to missed error handling and degraded user experience.
- **Security Considerations**: The change strengthens adherence to CSP standards, reducing ambiguity and potential security loopholes in worker instantiation.

**Medium Risks**:
- **Deprecations**: The previous exception-based error handling is effectively deprecated in favor of event-driven handling.
- **Performance Impacts**: Asynchronous error events may introduce minor latency in error detection, but this is unlikely to affect overall application performance.

## 4. Recommended Actions

### Immediate Actions

- Audit all usages of `new Worker(url)` and `new SharedWorker(url)` for CSP-blocked scenarios.
- Refactor error handling logic to listen for error events rather than catching exceptions.

### Short-term Planning

- Update documentation and developer guides to reflect the new error event model.
- Monitor application logs for missed worker instantiation errors and adjust error reporting as needed.

### Long-term Strategy

- Advocate for consistent CSP error handling across all web APIs.
- Track future CSP specification changes and browser implementations to maintain compatibility.

## 5. Feature Analysis

### Fire error event for Content Security Policy (CSP) blocked worker

**Impact Level**: 🔴 Critical

**What Changed**:
Chrome now checks CSP during the fetch phase and fires an error event asynchronously when a script attempts to create a Worker or SharedWorker that is blocked by CSP. Previously, Chrome threw a synchronous exception in these cases.

**Why It Matters**:
This change brings Chrome into compliance with the CSP specification, ensuring consistent and predictable error handling for worker instantiation. Developers can now rely on the error event mechanism, improving the robustness of security-sensitive applications and reducing the risk of silent failures.

**Implementation Guidance**:
- Replace any try/catch logic around `new Worker(url)` and `new SharedWorker(url)` with event listeners for the `error` event.
- Test worker creation under various CSP configurations to ensure proper error detection and handling.
- Update automated tests to verify that error events are fired as expected when CSP blocks worker creation.

**References**:
- [Tracking bug #41285169](https://issues.chromium.org/issues/41285169)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5177205656911872)
- [Spec](https://www.w3.org/TR/CSP3/#fetch-integration)

---