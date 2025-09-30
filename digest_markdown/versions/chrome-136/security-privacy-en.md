---
layout: default
title: security-privacy-en
---

### 1. Area Summary

Chrome 136 Stable introduces targeted privacy and reporting improvements in the Security-Privacy area: a new Permissions Policy report type for iframes and reduced fingerprinting from the Accept-Language header. The most impactful changes for developers are finer-grained detection of iframe permission propagation issues and a shift in how language preferences are conveyed to servers and exposed via navigator.languages. These updates advance the web platform by improving observability of policy violations and limiting passive fingerprinting vectors. They matter because they enable more accurate security diagnostics while reducing user-identifying information in routine requests.

## Detailed Updates

The following items expand on the summary above and focus on developer-facing technical and practical implications.

### Permissions Policy reports for iframes

#### What's New
Introduces a new violation type called "Potential Permissions Policy violation" that inspects Permissions Policy (including report-only policy) and the allow attribute set in iframes to detect conflicts between the enforced Permissions Policy and permissions propagated to iframes.

#### Technical Details
The new violation type evaluates the effective Permissions Policy and the iframe's allow attribute to flag cases where propagated permissions conflict with what the top-level policy enforces. Reporting follows the Permissions Policy reporting model from the spec linked below.

#### Use Cases
- Detect and report iframe permission propagation misconfigurations during development and in production.
- Improve security monitoring by surfacing potential policy mismatches that could lead to unintended permission grants.
- Aid compliance and debugging where report-only policies are deployed to test policy changes.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40941424
- https://chromestatus.com/feature/5061997434142720
- https://w3c.github.io/webappsec-permissions-policy/#reporting

### Reduce fingerprinting in Accept-Language header information

#### What's New
Reduces the amount of information the Accept-Language header value string exposes in HTTP requests and in `navigator.languages`. Instead of sending a full list of the user's preferred languages on every HTTP request, Chrome now sends the user's most preferred language in the Accept-Language header.

#### Technical Details
Chrome limits the Accept-Language header to the single top-preference language when issuing HTTP requests and reduces the granularity exposed via navigator.languages to mitigate passive fingerprinting. This change reduces cross-request leakage of a user's full language preference list.

#### Use Cases
- Improves end-user privacy by reducing a common cross-request fingerprinting vector.
- May affect server-side locale detection and analytics that rely on the full Accept-Language list; developers should validate locale fallback logic.
- Useful for privacy-focused features and threat models where minimizing per-request entropy is required.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=1306905
- https://chromestatus.com/feature/5042348942655488
