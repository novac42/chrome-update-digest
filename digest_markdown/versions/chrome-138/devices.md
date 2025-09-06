---
layout: default
title: Chrome 138 - Devices
---

# Chrome 138 - Devices

[← Back to Chrome 138](./) | [View All Devices Updates](/areas/devices/)

## Devices

### Web serial over Bluetooth on Android

This feature lets web pages and web apps connect to serial ports over Bluetooth on Android devices. Chrome on Android now supports Web Serial API over Bluetooth RFCOMM. Existing enterprise policies (`DefaultSerialGuardSetting`, `SerialAllowAllPortsForUrls`, `SerialAllowUsbDevicesForUrls`, `SerialAskForUrls` and `SerialBlockedForUrls`) on other platforms are enabled in future_on states for Android. All policies except `SerialAllowUsbDevicesForUrls` will be enabled after the feature is enabled. `SerialAllowUsbDevicesForUrls` will be enabled in a future launch after Android provides system level support of wired serial ports.

**References:** [Tracking bug #375245353](https://bugs.chromium.org/p/chromium/issues/detail?id=375245353) | [ChromeStatus.com entry](https://chromestatus.com/feature/5085754267189248) | [Spec](https://wicg.github.io/serial/)

### Viewport Segments Enumeration API

The Viewport Segments API allows developers to adapt their web layout to target foldable devices. The viewport segments defines the position and dimensions of a logically separate region of the viewport. Viewport segments are created when the viewport is split by one or more hardware features (such as a fold or a hinge between separate displays) that act as a divider; segments are the regions of the viewport that can be treated as logically distinct by the developer.

**References:** [Tracking bug #1039050](https://bugs.chromium.org/p/chromium/issues/detail?id=1039050) | [ChromeStatus.com entry](https://chromestatus.com/feature/5131631321964544) | [Spec](https://wicg.github.io/visual-viewport/)


---

## Navigation
- [Chrome 138 Overview](./)
- [All Devices Updates](/areas/devices/)
- [Browse Other Areas](./)
