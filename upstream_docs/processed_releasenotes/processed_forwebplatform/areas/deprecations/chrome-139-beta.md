## Deprecations and removals

This version of Chrome introduces the deprecations and removals listed below. Visit ChromeStatus.com for lists of planned deprecations, current deprecations and previous removals.

This release of Chrome removes two features.

### Remove support for macOS 11

Chrome 138 is the last release to support macOS 11. From Chrome 139 macOS 11 is not supported, as it is outside of its support window with Apple. Running on a supported operating system is essential to maintaining security. On Macs running macOS 11, Chrome will continue to work, showing a warning infobar, but will not update any further. If a user wishes to update Chrome, they need to update their computer to a supported version of macOS. For new installations of Chrome 139 and up, macOS 12 or greater will be required.

### Remove auto-detection of ISO-2022-JP charset in HTML

There are [known security issues](https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/) around charset auto-detection for ISO-2022-JP. Given that the usage is very low, and Safari does not support auto-detection of ISO-2022-JP, Chrome removes support for it to eliminate the security issues.
