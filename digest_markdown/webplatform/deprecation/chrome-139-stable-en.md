## Area Summary

Chrome 139 deprecations focus on removing legacy behaviors and platform support that pose security, compatibility, or maintenance costs. Key themes are retiring legacy request headers (prefetch Purpose), ending support for older macOS (11), and removing risky charset auto-detection (ISO-2022-JP). The most impactful changes for developers are potential behavioral differences in speculative prefetches/prerenders, update limitations on older Macs, and stricter encoding handling that can surface mis-declared pages. These changes advance the web platform by reducing attack surface, simplifying implementation invariants, and encouraging explicit developer control over encoding and platform support.

## Detailed Updates

The following entries expand on the summary above and provide technical and practical guidance for development teams.

### Stop sending Purpose: prefetch header from prefetches and prerenders

#### What's New
Chrome is removing the legacy Purpose: prefetch request header for prefetches and prerenders; these requests will use the Sec-Purpose header instead.

#### Technical Details
The legacy header removal will be controlled by a feature flag/kill switch to avoid compatibility issues. The change is scoped to speculative navigation features (prefetches and prerenders) per the nav-speculation interaction with fetch.

#### Use Cases
- Ensure server-side logic that depended on Purpose: prefetch instead reads Sec-Purpose.
- Update analytics or access-control rules that inspect request headers for prefetch/prerender signals.
- Use this change to simplify header handling by standardizing on Sec-Purpose.

#### References
- [Tracking bug #420724819](https://issues.chromium.org/issues/420724819)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320)
- [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

### Remove support for macOS 11

#### What's New
Chrome 139 drops support for macOS 11. Chrome 138 is the last release to support that OS.

#### Technical Details
On macOS 11 devices, Chrome will continue to run but will show a warning infobar and will no longer receive updates. Users must upgrade their OS to receive new Chrome releases.

#### Use Cases
- Plan testing and support baselines: CI and QA should move macOS test runners to supported macOS versions.
- Communicate to users and operations teams about necessary OS upgrades to continue receiving Chrome updates.
- Consider auto-update and enterprise management workflows that target supported macOS versions.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/4504090090143744)

### Remove auto-detection of `ISO-2022-JP` charset in HTML

#### What's New
Chrome 139 removes auto-detection support for the ISO-2022-JP charset in HTML due to known security issues and very low usage.

#### Technical Details
Auto-detection for ISO-2022-JP is removed; pages must explicitly declare their encoding. The decision aligns with other browsers (Safari does not support this auto-detection) and mitigates risks described in security analyses.

#### Use Cases
- Audit pages that rely on charset auto-detection and ensure explicit charset declarations (Content-Type header or <meta charset>).
- For legacy content in ISO-2022-JP, convert files to UTF-8 or serve an explicit charset header.
- Update server- and build-pipelines to enforce correct charset metadata to avoid misinterpretation.

#### References
- [known security issues](https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/)
- [Tracking bug #40089450](https://issues.chromium.org/issues/40089450)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6576566521561088)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)

