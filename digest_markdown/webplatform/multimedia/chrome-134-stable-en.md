### 1. Area Summary

Chrome 134 removes legacy, nonstandard goog-prefixed audio constraints from getUserMedia in Blink, reflecting very low usage and alignment with standards. The most impactful change for developers is that any reliance on these legacy constraints will stop working; migrate to the standardized Media Track Constraints defined by the W3C. This narrows the browser surface area, simplifying WebRTC audio capture behavior and reducing maintenance and privacy attack surface. Overall, the change advances the web platform by enforcing a single, spec-compliant constraints model across implementations.

## Detailed Updates

Below are the Multimedia-specific details and practical guidance for teams that use getUserMedia audio constraints.

### Remove nonstandard `getUserMedia` audio constraints

#### What's New
Chrome 134 removes support for several nonstandard, goog-prefixed audio constraints previously supported by Blink. Usage had fallen to between 0.000001% and 0.0009% depending on the constraint, and some constraints were already inert.

#### Technical Details
- Blink historically accepted goog-prefixed constraints that predated constraint standardization. Chrome 134 eliminates those legacy short-cuts to conform to the W3C media capture constraints model.
- Developers must use the standardized Media Track Constraints (see Spec link) exposed via navigator.mediaDevices.getUserMedia.
- This is a deprecation-driven simplification that reduces implementation divergence and potential privacy/permission edge cases.

Relevant area mappings: webapi (getUserMedia constraint model), multimedia (audio capture semantics), security-privacy (smaller legacy surface), performance (reduced legacy handling), devices (audio input handling), deprecations (migration required).

#### Use Cases
- Migration: Replace any goog-prefixed constraint checks with standard constraint names or feature-detect via specification-compliant APIs.
- Interop testing: Validate audio capture behavior across browsers using the W3C constraint names.
- Maintenance: Remove guard code paths for goog-prefixed constraints to simplify media capture logic and permission UX.

#### References
- Tracking bug #377131184: https://issues.chromium.org/issues/377131184
- ChromeStatus.com entry: https://chromestatus.com/feature/5097536380207104
- Spec: https://w3c.github.io/mediacapture-main/#media-track-constraints
- Creative Commons Attribution 4.0 License: https://creativecommons.org/licenses/by/4.0/
- Apache 2.0 License: https://www.apache.org/licenses/LICENSE-2.0
- Google Developers Site Policies: https://developers.google.com/site-policies

Filename: digest_markdown/webplatform/Multimedia/chrome-134-stable-en.md