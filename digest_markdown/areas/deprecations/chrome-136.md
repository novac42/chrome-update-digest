---
layout: default
title: chrome-136
---

## Deprecations and removals

### Remove HTMLFencedFrameElement.canLoadOpaqueURL()

The `HTMLFencedFrameElement` method `canLoadOpaqueURL()` was replaced with `navigator.canLoadAdAuctionFencedFrame()` in 2023, and calling it has resulted in a deprecation console warning ever since pointing to the new API. The method is removed from Chrome 136.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5083847901667328)

---

*Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.*

*Last updated 2025-04-29 UTC.*
