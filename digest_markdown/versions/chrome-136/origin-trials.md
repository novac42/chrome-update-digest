---
layout: default
title: origin-trials
---

## Origin trials

### Audio Output Devices API: setDefaultSinkId()

This feature adds `setDefaultSinkId()` to `MediaDevices`, which enables the top-level frame to change the default audio output device used by its subframes.

**References:** [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [ChromeStatus.com entry](https://chromestatus.com/feature/5066644096548864) | [Spec](https://webaudio.github.io/web-audio-api/#dom-mediadevices-setdefaultsinkid)

### Enable web applications to understand bimodal performance timings

Web applications may suffer from bimodal distribution in page load performance, due to factors outside of the web application's control. For example:
- When a user agent first launches (a "cold start" scenario), it must perform many expensive initialization tasks that compete for resources on the system.
- Browser extensions can affect the performance of a website. For instance, some extensions run additional code on every page you visit, which can increase CPU usage and result in slower response times.
- When a machine is busy performing intensive tasks, it can lead to slower loading of web pages.

A new `confidence` field on the `PerformanceNavigationTiming` object will enable developers to discern if the navigation timings are representative for their web application.

**References:** [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #1413848](https://bugs.chromium.org/p/chromium/issues/detail?id=1413848) | [ChromeStatus.com entry](https://chromestatus.com/feature/5037395062800384) | [Spec](https://w3c.github.io/navigation-timing/)

### Update of Canvas text rendering implementation

This is not a web-exposed change. The implementation of `CanvasRenderingContext2D` `measureText()`, `fillText()`, and `strokeText()` has a drastic change. This might affect performance, so we'd like to run an origin trial so canvas-heavy applications can try out the new implementation.

**References:** [Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #389726691](https://bugs.chromium.org/p/chromium/issues/detail?id=389726691) | [ChromeStatus.com entry](https://chromestatus.com/feature/5104000067985408)
