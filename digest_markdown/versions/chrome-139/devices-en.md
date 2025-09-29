---
layout: default
title: devices-en
---

## Detailed Updates

The following details connect the summary above to the specific features in Chrome 139 for the Devices area.

### On-device Web Speech API

#### What's New
On-device speech recognition support is added to the Web Speech API, allowing websites to ensure that neither audio nor transcribed speech are sent to a third‑party service for processing. Sites can query availability for specific languages and invoke local recognition where supported.

#### Technical Details
This feature integrates local speech recognition engines with the existing Web Speech API surface so the browser can perform recognition without networking the audio or transcripts to external services. The platform exposes availability discovery per language to allow progressive enhancement.

#### Use Cases
- Privacy-sensitive voice input where audio and transcripts must remain on-device.
- Offline voice interactions and speech-driven UI in constrained-network scenarios.
- Progressive enhancement paths that detect device capability and fall back to cloud services when unavailable.

#### References
- https://chromestatus.com/feature/6090916291674112
- https://webaudio.github.io/web-speech-api

### WebXR depth sensing performance improvements

#### What's New
Chrome 139 exposes new mechanisms to customize depth sensing behavior inside a WebXR session, aiming to improve performance of depth buffer generation and consumption.

#### Technical Details
The update provides controls to request different depth buffer representations such as raw or smooth depth, and additional tuning options to influence how depth data is produced and consumed by an application. These controls let developers balance quality and performance based on device capabilities.

#### Use Cases
- AR applications that need lower-latency or lower-cost depth data for rendering or occlusion.
- Mobile/embedded device scenarios where developers must choose between raw sensor fidelity and smoothed depth for performance.
- Apps that adapt depth sensing strategy dynamically to conserve power or meet runtime frame‑rate targets.

#### References
- https://issues.chromium.org/issues/410607163
- https://chromestatus.com/feature/5074096916004864
- https://immersive-web.github.io/depth-sensing
