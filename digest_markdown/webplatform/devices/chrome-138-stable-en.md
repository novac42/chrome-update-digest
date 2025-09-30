## Area Summary

Chrome 138 (stable) advances the Devices area in two complementary directions: expanded hardware connectivity and improved layout support for foldable hardware. The Web Serial API over Bluetooth RFCOMM on Android broadens serial device access patterns for web apps, while the Viewport Segments Enumeration API formalizes how pages detect and adapt to split viewports on foldables. These features move the platform toward richer device integrations and more predictable multi-segment layouts, enabling web apps that target IoT, device provisioning, and foldable UX. For developers, the changes mean new device pairing surfaces and clearer primitives for responsive layout on non‑rectangular viewports.

## Detailed Updates

Below are the two Devices-area updates in this release and what they mean for implementation and product scenarios.

### Web serial over Bluetooth on Android

#### What's New
Chrome on Android supports the Web Serial API over Bluetooth RFCOMM, allowing web pages and web apps to connect to serial ports via Bluetooth on Android devices.

#### Technical Details
- Enables Web Serial API usage over Bluetooth RFCOMM transport on Android.
- Existing enterprise policies are referenced in the change (e.g., `DefaultSerialGuardSetting`, `SerialAllowAllPortsForUrls`, `SerialAllowUsbDevicesForUrls`, `SerialAsk...`).

#### Use Cases
- Web-based device configuration and provisioning for Bluetooth-capable serial devices (IoT, embedded devices, test equipment).
- In-browser debugging and maintenance tools that communicate with devices over Bluetooth serial links.
- Enterprise-managed deployments that rely on existing serial-related policies for governance.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=375245353
- https://chromestatus.com/feature/5085754267189248
- https://wicg.github.io/serial/

### Viewport Segments Enumeration API

#### What's New
The Viewport Segments API exposes the position and dimensions of logically separate regions (viewport segments) created when hardware features split the viewport, enabling better layout adaptation for foldable devices.

#### Technical Details
- Introduces enumeration of viewport segments that represent distinct regions when the viewport is split by one or more hardware features.
- Provides programmatic access to segment geometry to drive layout and rendering decisions.

#### Use Cases
- Responsive layouts that place content into segments (e.g., multi-panel UIs) and avoid hinge/crease areas.
- Progressive enhancement for foldable and dual-screen devices where segment geometry determines content flow and navigation patterns.
- CSS and rendering-engine integration points to improve multi-segment layout stability and performance.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=1039050
- https://chromestatus.com/feature/5131631321964544
- https://wicg.github.io/visual-viewport/

Saved file: digest_markdown/webplatform/Devices/chrome-138-stable-en.md