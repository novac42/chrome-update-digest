---
layout: default
title: network
---

## Network

### Reduce fingerprinting in Accept-Language header information

Reduces the amount of information the `Accept-Language` header value string exposes in HTTP requests and in `navigator.languages`. Instead of sending a full list of the user's preferred languages on every HTTP request using the `Accept-Language` header, Chrome only sends the user's most preferred language.

[Tracking bug #1306905](https://issues.chromium.org/issues/1306905) | [ChromeStatus.com entry](https://chromestatus.com/feature/5188040623390720)

### Randomize TCP port allocation on Windows

This launch enables TCP port randomization on versions of Windows (2020 or later) where we don't expect to see issues with re-use of prior ports occurring too fast (causing rejection due to timeouts on port re-use). The rapid port re-use issue arises from the Birthday problem, where the probability of randomly re-picking a port already seen rapidly converges with 100% for each new port chosen when compared to port re-use in a sequential model.

[Tracking bug #40744069](https://issues.chromium.org/issues/40744069) | [ChromeStatus.com entry](https://chromestatus.com/feature/5106900286570496)
