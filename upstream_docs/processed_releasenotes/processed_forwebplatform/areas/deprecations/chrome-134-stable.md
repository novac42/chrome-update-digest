## Deprecations and removals

### Remove nonstandard `getUserMedia` audio constraints

Blink supports a number of nonstandard `goog`-prefixed constraints for `getUserMedia` from some time before constraints were properly standardized.

Usage has gone down significantly to between 0.000001% to 0.0009% (depending on the constraint) and some of them don't even have an effect due to changes in the Chromium audio-capture stack. Soon none of them will have any effect due to other upcoming changes.

We don't expect any major regressions due to this change. Applications using these constraints will continue to work, but will get audio with default settings (as if no constraints were passed). They can opt to migrate to standard constraints.

[Tracking bug #377131184](https://issues.chromium.org/issues/377131184) | [ChromeStatus.com entry](https://chromestatus.com/feature/5097536380207104) | [Spec](https://w3c.github.io/mediacapture-main/#media-track-constraints)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-03-04 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-03-04 UTC."],[],[]] 
