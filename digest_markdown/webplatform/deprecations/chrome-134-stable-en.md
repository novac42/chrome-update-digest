## Area Summary

Chrome 134 (stable) removes legacy, nonstandard `goog`-prefixed audio constraints from getUserMedia. The change targets rarely used, Blink-specific constraints (usage reported between 0.000001% and 0.0009%), some of which no longer take effect. For developers, the most impactful result is that any reliance on these obsolete constraints must be audited and migrated to standardized constraints from the W3C spec to ensure cross‑browser compatibility. This cleanup advances the platform by reducing legacy surface area, improving spec conformance, and simplifying media-capture behavior across implementations.

## Detailed Updates

The single deprecation below directly follows from the summary above and requires developers handling media capture to review constraint usage.

### Remove nonstandard `getUserMedia` audio constraints

#### What's New
Blink is removing support for several nonstandard `goog`-prefixed audio constraints previously accepted by getUserMedia.

#### Technical Details
- These were Blink-specific extensions rather than part of the standardized Media Capture constraints.
- Observed usage was extremely low (between 0.000001% and 0.0009% depending on the constraint), and some constraints no longer have any effect due to prior changes.
- Developers should rely on the standardized constraint model defined by the W3C media capture spec.

#### Use Cases
- Audit application code and third-party libraries for `goog`-prefixed getUserMedia constraints and replace them with standardized constraints from the W3C spec.
- Update automated tests that assert behavior tied to these nonstandard constraints.
- Verify cross-browser behavior after migration to ensure consistent audio capture and device selection.

#### References
- Tracking bug #377131184: https://issues.chromium.org/issues/377131184
- ChromeStatus.com entry: https://chromestatus.com/feature/5097536380207104
- Spec: https://w3c.github.io/mediacapture-main/#media-track-constraints
- Creative Commons Attribution 4.0 License: https://creativecommons.org/licenses/by/4.0/
- Apache 2.0 License: https://www.apache.org/licenses/LICENSE-2.0
- Google Developers Site Policies: https://developers.google.com/site-policies

## Area-Specific Expertise (Deprecations-focused guidance)

- css: No direct impact; ensure audio-related UI controls continue to work when constraints change.
- webapi: Replace nonstandard getUserMedia constraints with properties defined in the W3C Media Capture spec.
- graphics-webgpu: Not applicable for this deprecation.
- javascript: Remove or guard code paths that set `goog`-prefixed constraint keys before calling getUserMedia.
- security-privacy: Audit constraint usage to avoid unexpected permission or device-selection differences across browsers.
- performance: Fewer legacy code paths can simplify constraint processing and reduce maintenance overhead.
- multimedia: Validate audio-capture behavior (sample rates, device selection, constraints) after migrating to standard constraints.
- devices: Confirm device enumeration and selection remain correct without Blink-specific constraints.
- pwa-service-worker: No direct effect, but PWAs that capture audio should be tested for media-capture compatibility.
- webassembly: Not directly affected.
- deprecations: Plan a migration path: inventory usages, replace with spec-compliant constraints, update tests, and verify cross-browser behavior.