---
layout: default
title: devices-en
---

## Detailed Updates

Below are the Devices-area updates from the Chrome 138 stable release, with concise technical context and developer-focused use cases.

### Web serial over Bluetooth on Android

#### What's New
Chrome on Android supports the Web Serial API over Bluetooth RFCOMM, letting web pages and web apps connect to serial ports exposed over Bluetooth on Android devices. Existing enterprise policies such as DefaultSerialGuardSetting, SerialAllowAllPortsForUrls, and SerialAllowUsbDevicesForUrls apply.

#### Technical Details
Implementation enables Web Serial API transport over Bluetooth RFCOMM on Chromium for Android, following the Web Serial spec for enumerating and opening serial ports over this transport.

#### Use Cases
- Web UIs that communicate with microcontrollers, sensors, or legacy serial peripherals via Bluetooth.
- Enterprise and managed-device scenarios where policies govern serial-port access from web apps.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=375245353
- https://chromestatus.com/feature/5085754267189248
- https://wicg.github.io/serial/

### Viewport Segments Enumeration API

#### What's New
The Viewport Segments API enables developers to adapt layouts for foldable and multi-segment displays by exposing the position and dimensions of logically separate viewport regions. Viewport segments are created when the viewport is split by one or more hardware features.

#### Technical Details
The API provides enumeration of viewport segments produced by hardware-driven splits (hinges, folds, cutouts), allowing apps to query segment geometry and react to segmented viewports as defined by the Visual Viewport work.

#### Use Cases
- Responsive two-pane or multi-pane layouts for foldable devices.
- Dynamic placement of interactive UI across hinge/fold boundaries to avoid occlusion.
- Improved media and content layout strategies on split viewports.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=1039050
- https://chromestatus.com/feature/5131631321964544
- https://wicg.github.io/visual-viewport/
