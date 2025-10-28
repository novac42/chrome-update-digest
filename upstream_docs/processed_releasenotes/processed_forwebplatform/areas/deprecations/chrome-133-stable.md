## Deprecations and removals

### Deprecate WebGPU limit `maxInterStageShaderComponents`

The `maxInterStageShaderComponents limit` is deprecated due to a combination of factors. The intended removal date in Chrome 135.

  * Redundancy with `maxInterStageShaderVariables`: This limit already serves a similar purpose, controlling the amount of data passed between shader stages.
  * Minor discrepancies: While there are slight differences in how the two limits are calculated, these differences are minor and can be effectively managed within the `maxInterStageShaderVariables` limit.
  * Simplification: Removing `maxInterStageShaderComponents` streamlines the shader interface and reduces complexity for developers. Instead of managing two separate limits with subtle differences, they can focus on the more appropriately named and comprehensive `maxInterStageShaderVariables`.

[ChromeStatus.com entry](https://chromestatus.com/feature/4853767735083008)

### Remove `<link rel=prefetch>` five-minute rule

Previously, when a resource was prefetched using `<link rel=prefetch>`, Chrome ignored its cache semantics (namely `max-age` and `no-cache`) for the first use within five minutes, to avoid refetching. Now, Chrome removes this special case and uses normal HTTP cache semantics.

This means web developers need to include appropriate caching headers (Cache-Control or Expires) to see benefits from `<link rel=prefetch>`.

This also affects the nonstandard `<link rel=prerender>`.

[Tracking bug #40232065](https://issues.chromium.org/issues/40232065) | [ChromeStatus.com entry](https://chromestatus.com/feature/5087526916718592)

### Remove Chrome Welcome page triggering with initial prefs first run tabs

Including `chrome://welcome` in the `first_run_tabs` property of the `initial_preferences` file will now have no effect. This is removed because that page is redundant with the First Run Experience that triggers on desktop platforms.

[ChromeStatus.com entry](https://chromestatus.com/feature/5118328941838336)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-02-04 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-02-04 UTC."],[],[]] 
