---
layout: default
title: Chrome 139 Stable – JavaScript Area Update
---

Save to: digest_markdown/webplatform/javascript/chrome-139-stable-en.md

---

# Chrome 139 Stable – JavaScript Area Update

## 1. Executive Summary

Chrome 139 introduces a significant update to JavaScript DOM APIs by relaxing the validation rules for element and attribute names. This change aligns the JavaScript DOM APIs more closely with the HTML parser, allowing a broader set of valid characters and names when creating elements and attributes programmatically.

## 2. Key Implications

### Technical Impact

- **Existing Implementations**: Scripts that previously failed when attempting to create elements or attributes with certain characters will now succeed, reducing discrepancies between markup parsing and DOM API behavior.
- **New Capabilities**: Developers can now programmatically create elements and attributes with a wider range of names, matching what is possible in HTML markup.
- **Technical Debt**: Legacy code with workarounds for stricter DOM API validation may be simplified or refactored.

## 3. Risk Assessment

**Critical Risks**:
- **Breaking Changes**: None identified; this is a loosening of restrictions, not a tightening.
- **Security Considerations**: Allowing more characters could introduce edge cases in code that assumes stricter validation. Review input sanitization and security logic around dynamic element/attribute creation.

**Medium Risks**:
- **Deprecations**: None associated with this change.
- **Performance Impacts**: No direct performance impact expected.

## 4. Recommended Actions

### Immediate Actions

- Audit codebases for custom validation or workarounds related to DOM element/attribute creation.
- Test dynamic DOM creation logic, especially where non-standard names are used.

### Short-term Planning

- Update documentation and developer guidelines to reflect the new capabilities.
- Refactor legacy code that relied on previous validation strictness.

### Long-term Strategy

- Monitor for any security or compatibility issues arising from broader character support.
- Stay aligned with evolving DOM and HTML parsing specifications.

## 5. Feature Analysis

### Allow more characters in JavaScript DOM APIs

**Impact Level**: 🟡 Important

**What Changed**:
The validation rules for element and attribute names in JavaScript DOM APIs have been relaxed. Previously, the APIs were more restrictive than the HTML parser, leading to inconsistencies. Now, the APIs allow a wider variety of valid characters and names, matching the HTML parser's behavior.

**Why It Matters**:
This change eliminates a longstanding inconsistency between markup parsing and DOM API usage. Developers can now create elements and attributes programmatically with the same flexibility as when writing HTML, reducing friction and the need for workarounds.

**Implementation Guidance**:
- Review any code that programmatically creates elements or attributes with dynamic names.
- Remove unnecessary validation or error handling that assumed stricter DOM API rules.
- Ensure that security checks (e.g., for XSS) are robust, as more character combinations are now possible.

**References**:
- [Tracking bug #40228234](https://issues.chromium.org/issues/40228234)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6278918763708416)
- [Spec](https://dom.spec.whatwg.org/#namespaces)

---