---
layout: default
title: deprecations-en
---

## Detailed Updates

A short list of the deprecations above, with concise technical context and practical migration notes.

### Deprecate WebGPU limit `maxInterStageShaderComponents`

#### What's New
The `maxInterStageShaderComponents` limit is deprecated; Chrome intends to remove it in Chrome 135. The deprecation is driven by redundancy with `maxInterStageShaderVariables` and other factors noted in the announcement.

#### Technical Details
This deprecation removes an overlapping GPU feature-limit that controlled data passed between shader stages. Implementations should rely on the remaining `maxInterStageShaderVariables` limit and canonical WebGPU limits going forward. Expect the runtime to stop reporting or enforcing this separate limit upon removal.

#### Use Cases
- Shader authors and engine developers should audit inter-stage data usage and migrate any checks or fallbacks that referenced `maxInterStageShaderComponents` to the canonical variable-based limits.
- Graphics test suites should stop asserting the deprecated limit and validate behavior against the remaining limits.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/4853767735083008)

### Remove `<link rel=prefetch>` five-minute rule

#### What's New
Chrome no longer applies a special five-minute exception that ignored cache semantics for prefetched resources. Prefetch now obeys normal HTTP caching semantics immediately.

#### Technical Details
Previously, a prefetched resource's `max-age` and `no-cache` directives were temporarily overridden for the first use within five minutes to avoid refetching. That exception has been removed; the browser will honor cache-control headers per standard HTTP semantics on first use.

#### Use Cases
- Developers relying on prefetch to bypass server cache-control for short-term reuse should update strategies to respect cache headers (e.g., adjust server-side cache-control, use service workers for more control).
- Performance tooling and audits should be updated to reflect that prefetch no longer provides a temporary cache override.

#### References
- [Tracking bug #40232065](https://issues.chromium.org/issues/40232065)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5087526916718592)

### Remove Chrome Welcome page triggering with initial prefs first run tabs

#### What's New
Including chrome://welcome in the `first_run_tabs` property of the `initial_preferences` file will no longer trigger the Welcome page. This behavior is removed because the Welcome page is redundant with the desktop First Run Experience.

#### Technical Details
The `first_run_tabs` hook in initial preferences previously allowed administrators or installers to open chrome://welcome on first run; that hook is now ignored for this URL. The change affects desktop platform first-run flows and simplifies the product-level onboarding triggers.

#### Use Cases
- Administrators or OEMs who relied on injecting chrome://welcome via initial preferences should remove that customization and use supported First Run Experience configuration mechanisms.
- Update any automation or provisioning scripts that expect the Welcome page to open via `first_run_tabs`.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5118328941838336)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)

File path to save this digest:
digest_markdown/webplatform/Deprecations/chrome-133-stable-en.md
