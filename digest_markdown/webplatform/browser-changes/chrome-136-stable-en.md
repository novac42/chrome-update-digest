## Area Summary

Chrome 136 introduces a visual refresh for Chromium scrollbars to match the Windows 11 Fluent design language, affecting both overlay and non-overlay scrollbars on Windows and Linux. The most impactful developer-visible change is that non-overlay Fluent scrollbars are enabled by default on those platforms, which can alter how pages look and how custom scrollbar styles interact with system-provided chrome. This update advances the web platform by unifying scrollbar visuals across platforms and reducing friction between native UI expectations and web content. Teams should plan for potential layout and styling differences, and validate accessibility and visual regressions.

## Detailed Updates

Below are the specific Browser changes that follow from the summary above.

### Fluent scrollbars

#### What's New
Chromium scrollbars (both overlay and non-overlay) have been modernized on Windows and Linux to fit the Windows 11 Fluent design language. Non-overlay Fluent scrollbars will be enabled by default in Linux and Windows. (Source content truncated in input.)

#### Technical Details
- Applies to both overlay and non-overlay scrollbar modes on Windows and Linux.
- Non-overlay Fluent scrollbars are enabled by default on those platforms per the release notes.
- Implementation details beyond the provided summary were not included in the source data.

#### Use Cases
- UI consistency: Web apps and sites will render scrollbars that match the updated Fluent look on Windows and Linux, reducing visual mismatch with native controls.
- Developer styling: Teams that use custom scrollbar CSS (e.g., ::-webkit-scrollbar) should test for visual regressions and ensure custom styles remain legible against the new defaults.
- Testing & accessibility: Validate keyboard and assistive technology interactions and visual contrast after the refresh; also re-run visual regression tests where scrollbar visuals affect snapshots.

#### References
- [Tracking bug #1292117](https://bugs.chromium.org/p/chromium/issues/detail?id=1292117)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5023688844812288)

Saved to: digest_markdown/webplatform/Browser changes/chrome-136-stable-en.md