---
layout: default
title: chrome-139-en
---

## Area Summary

Chrome 139 (stable) introduces targeted performance improvements for WebXR depth sensing in the Devices area. The release exposes several mechanisms that let developers customize depth buffer behavior (notably the ability to request raw or smooth depth buffers) to reduce the cost of generating or consuming depth. These changes give XR and device-focused teams finer control over latency vs. quality trade-offs and enable more efficient rendering and sensor pipelines on constrained hardware. For developers, this advances the web platform by exposing lower-level depth options that can translate directly into better runtime performance and more predictable resource usage on devices.

## Detailed Updates

The following update expands on the summary above and highlights practical implications for device- and XR-focused development teams.

### WebXR depth sensing performance improvements

#### What's New
Exposes several new mechanisms to customize the behavior of the depth sensing feature within a WebXR session, with the goal of improving the performance of the generation or consumption of the depth buffer. The key mechanisms exposed include the ability to request the raw or smooth depth buffer.

#### Technical Details
The feature surfaces options that change what form of depth data is produced or delivered to a WebXR session consumer (raw vs. smoothed). These options let implementers and web apps trade processing (smoothing, filtering) for lower-latency, lower-overhead depth data consumption. See the spec and tracking links for the authoritative API shape and status.

#### Use Cases
- AR/VR apps that need lower latency depth for occlusion or interaction can request raw depth to reduce pre-processing cost.  
- Applications that need visually stable depth for effects can opt for smoothed depth where quality matters more than minimal latency.  
- Device teams and engine integrators can tune depth production to match GPU/CPU budgets on constrained devices, improving frame rates and power usage.

#### References
- [Tracking bug](https://issues.chromium.org/issues/410607163)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5074096916004864)
- [Link](https://immersive-web.github.io/depth-sensing)

Saved file: digest_markdown/webplatform/Devices/chrome-139-stable-en.md
