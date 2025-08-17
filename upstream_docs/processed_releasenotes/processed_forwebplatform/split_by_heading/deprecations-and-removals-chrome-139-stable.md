## Deprecations and removals

### Stop sending Purpose: prefetch header from prefetches and prerenders

Now that prefetches and prerenders are using the `Sec-Purpose` header for prefetches and prerenders, we will move to remove the legacy Purpose: prefetch header that is still currently passed. This will be behind a feature flag/ kill switch to prevent compat issues.

This will be scoped to speculation rules prefetch, speculation rules prerender, `<link rel=prefetch>`, and Chrome's non-standard `<link rel=prerender>`.

[Tracking bug #420724819](https://issues.chromium.org/issues/420724819) | [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320) | [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

### Remove support for macOS 11

Chrome 138 is the last release to support macOS 11. From Chrome 139 macOS 11 is not supported.

On Macs running macOS 11, Chrome will continue to work, showing a warning infobar, but won't update any further. To update Chrome, you need to update their computer to a supported version of macOS.

For new installations from Chrome 139, macOS 12 or greater will be required.

[ChromeStatus.com entry](https://chromestatus.com/feature/4504090090143744)

### Remove auto-detection of `ISO-2022-JP` charset in HTML

There are [known security issues](https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/) around charset auto-detection for `ISO-2022-JP`. Given that the usage is very low, and Safari does not support auto-detection of `ISO-2022-JP`, support is removed from Chrome 139.

[Tracking bug #40089450](https://issues.chromium.org/issues/40089450) | [ChromeStatus.com entry](https://chromestatus.com/feature/6576566521561088)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-08-05 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-08-05 UTC."],[],[]] 
